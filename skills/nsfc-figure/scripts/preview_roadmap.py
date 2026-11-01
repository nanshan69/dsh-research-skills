#!/usr/bin/env python3
"""把未压缩的 .drawio 渲染成 SVG 预览（纯标准库，端侧无 Draw.io Desktop 时用）。

这不是官方渲染，只做几何与文字的近似重排，用于在设备上快速检查：
  1) 卡片文字会不会溢出 / 被裁切；
  2) 箭头方向、连线是否穿过文字区；
  3) 整体在申请书插图宽度下是否还能读。

字体度量用近似值（中文按 1 个字号宽，西文按 0.55 个字号宽），
所以**最终验收仍须在装了 Draw.io Desktop 的电脑上打开官方导出件**。

用法：
  python(file=".../nsfc-figure/scripts/run_nsfc.py",
         args=["preview_roadmap", "图.drawio", "--out", "图_预览.svg"])
"""

import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, replace
from html.parser import HTMLParser
from pathlib import Path

CJK = re.compile(r"[\u2e80-\u9fff\uff00-\uffef\u3000-\u303f]")


def parse_style(style: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for token in (style or "").split(";"):
        token = token.strip()
        if not token:
            continue
        if "=" in token:
            key, value = token.split("=", 1)
            out[key.strip()] = value.strip()
        else:
            out[token] = "1"
    return out


@dataclass(frozen=True)
class LabelRun:
    text: str
    size: float
    bold: bool
    family: str


class LabelParser(HTMLParser):
    """保留源单元默认值及 HTML 片段的字体继承，不换成本机字体。"""

    def __init__(self, base: LabelRun):
        super().__init__(convert_charrefs=True)
        self.stack = [("", base)]
        self.lines: list[list[LabelRun]] = [[]]

    def line_break(self) -> None:
        if self.lines[-1]:
            self.lines.append([])

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self.line_break()
            return
        if tag in ("div", "p"):
            self.line_break()
        attributes = dict(attrs)
        css = {}
        for declaration in (attributes.get("style") or "").split(";"):
            if ":" in declaration:
                key, value = declaration.split(":", 1)
                css[key.strip().lower()] = value.strip()
        current = self.stack[-1][1]
        family = css.get("font-family") or attributes.get("face") or current.family
        size_match = re.fullmatch(r"([0-9.]+)(?:px)?", css.get("font-size", ""))
        size = float(size_match.group(1)) if size_match else current.size
        weight = css.get("font-weight", "").lower()
        bold = current.bold or tag in ("b", "strong")
        if weight:
            bold = weight in ("bold", "bolder", "600", "700", "800", "900")
        self.stack.append((tag, LabelRun("", size, bold, family)))

    def handle_endtag(self, tag: str) -> None:
        if tag in ("div", "p"):
            self.line_break()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        for index, text in enumerate(data.split("\n")):
            if index:
                self.line_break()
            if text:
                self.lines[-1].append(replace(self.stack[-1][1], text=text))


def label_segments(value: str, base: LabelRun) -> list[list[LabelRun]]:
    parser = LabelParser(base)
    parser.feed(value)
    parser.close()
    return [line for line in parser.lines if line]


def char_width(char: str) -> float:
    return 1.0 if CJK.match(char) else 0.55


def estimate_width(runs: list[LabelRun]) -> float:
    return sum(char_width(ch) * run.size for run in runs for ch in run.text)


def wrap_runs(runs: list[LabelRun], width: float) -> list[list[LabelRun]]:
    """按片段字号估算宽度；折行后保留原字体，西文尽量在空格处断开。"""
    lines: list[list[LabelRun]] = []
    current: list[LabelRun] = []
    for run in runs:
        for char in run.text:
            item = replace(run, text=char)
            if current and estimate_width(current + [item]) > width:
                spaces = [index for index, part in enumerate(current) if part.text == " "]
                if char.isascii() and char.isalnum() and spaces and spaces[-1] > 0:
                    split = spaces[-1]
                    lines.append(current[:split])
                    current = current[split + 1:]
                else:
                    lines.append(current)
                    current = []
            current.append(item)
    if current:
        lines.append(current)
    # 合并连续同样式片段，避免每个字都生成一个 tspan。
    merged: list[list[LabelRun]] = []
    for line in lines:
        compact: list[LabelRun] = []
        for run in line:
            if compact and replace(compact[-1], text="") == replace(run, text=""):
                compact[-1] = replace(run, text=compact[-1].text + run.text)
            else:
                compact.append(run)
        merged.append(compact)
    return merged


def num(value: str | None, default: float = 0.0) -> float:
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render(path: Path, out: Path) -> list[str]:
    warnings: list[str] = []
    tree = ET.parse(path)
    mxfile = tree.getroot()
    diagram = mxfile.find("diagram")
    if diagram is None:
        raise ValueError("找不到 <diagram> 节点")
    model = diagram.find("mxGraphModel")
    if model is None:
        raise ValueError("只支持未压缩的 mxGraphModel（本技能生成器默认就是未压缩）")

    page_w = num(model.get("pageWidth"), 1200)
    page_h = num(model.get("pageHeight"), 780)
    root = model.find("root")
    if root is None:
        raise ValueError("找不到 <root> 节点")

    cells = {cell.get("id"): cell for cell in root.findall("mxCell")}
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{page_w:.0f}" height="{page_h:.0f}" '
        f'viewBox="0 0 {page_w:.0f} {page_h:.0f}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
    ]

    def geometry(cell: ET.Element) -> ET.Element | None:
        return cell.find("mxGeometry")

    def center_point(cell: ET.Element, fx: float, fy: float) -> tuple[float, float]:
        geo = geometry(cell)
        if geo is None:
            return (0.0, 0.0)
        return (
            num(geo.get("x")) + num(geo.get("width")) * fx,
            num(geo.get("y")) + num(geo.get("height")) * fy,
        )

    # 先画节点，再画边：保证箭头压在卡片之上，和 Draw.io 的默认观感接近。
    for cell in root.findall("mxCell"):
        if cell.get("vertex") != "1":
            continue
        geo = geometry(cell)
        if geo is None:
            continue
        x, y = num(geo.get("x")), num(geo.get("y"))
        w, h = num(geo.get("width")), num(geo.get("height"))
        style = parse_style(cell.get("style", ""))
        fill = style.get("fillColor", "#FFFFFF")
        stroke = style.get("strokeColor", "none")
        stroke_w = num(style.get("strokeWidth"), 1.0)
        rounded = style.get("rounded") == "1" or style.get("arcSize") is not None
        rx = min(w, h) * 0.08 if rounded else 0.0
        is_ellipse = style.get("shape") == "ellipse" or style.get("ellipse") == "1"

        if is_ellipse:
            parts.append(
                f'<ellipse cx="{x + w / 2:.1f}" cy="{y + h / 2:.1f}" rx="{w / 2:.1f}" ry="{h / 2:.1f}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'
            )
        else:
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'
            )

        base_size = num(style.get("fontSize"), 12.0)
        color = style.get("fontColor", "#243746")
        base_bold = bool(int(num(style.get("fontStyle"))) & 1)
        base_family = style.get("fontFamily", "SimSun, Songti SC")
        segments = label_segments(
            cell.get("value", ""), LabelRun("", base_size, base_bold, base_family)
        )
        if not segments:
            continue
        padding = num(style.get("spacing"), 4.0)
        usable = max(w - 2 * padding, base_size)
        wrapped = [line for segment in segments for line in wrap_runs(segment, usable)]
        line_sizes = [max(run.size for run in line) for line in wrapped]
        total_h = sum(size * 1.35 for size in line_sizes)
        if total_h > h + 1:
            first_text = "".join(run.text for run in wrapped[0])
            warnings.append(
                f"'{first_text[:14]}…' 估算文字高 {total_h:.0f}px > 卡片高 {h:.0f}px（可能溢出）"
            )

        align = style.get("align", "center")
        valign = style.get("verticalAlign", "middle")
        if valign == "middle":
            cursor_y = y + (h - total_h) / 2
        else:
            cursor_y = y + padding
        for line, size in zip(wrapped, line_sizes):
            baseline = cursor_y + size * 0.95
            if align == "left":
                tx, anchor = x + padding, "start"
            elif align == "right":
                tx, anchor = x + w - padding, "end"
            else:
                tx, anchor = x + w / 2, "middle"
            spans = "".join(
                f'<tspan font-family="{esc(run.family)}" font-size="{run.size:.1f}" '
                f'font-weight="{700 if run.bold else 400}">{esc(run.text)}</tspan>'
                for run in line
            )
            parts.append(
                f'<text x="{tx:.1f}" y="{baseline:.1f}" xml:space="preserve" '
                f'fill="{color}" text-anchor="{anchor}">{spans}</text>'
            )
            cursor_y += size * 1.35

    for cell in root.findall("mxCell"):
        if cell.get("edge") != "1":
            continue
        source = cells.get(cell.get("source", ""))
        target = cells.get(cell.get("target", ""))
        if source is None or target is None:
            warnings.append(f"边 {cell.get('id')} 的端点不存在")
            continue
        style = parse_style(cell.get("style", ""))
        start = center_point(
            source,
            num(style.get("exitX"), 0.5),
            num(style.get("exitY"), 0.5),
        )
        end = center_point(
            target,
            num(style.get("entryX"), 0.5),
            num(style.get("entryY"), 0.5),
        )
        geo = geometry(cell)
        points = [start]
        if geo is not None:
            array = geo.find("Array")
            if array is not None:
                for point in array.findall("mxPoint"):
                    points.append((num(point.get("x")), num(point.get("y"))))
        points.append(end)
        path_d = " ".join(
            ("M" if index == 0 else "L") + f" {px:.1f} {py:.1f}"
            for index, (px, py) in enumerate(points)
        )
        dash = ' stroke-dasharray="6 5"' if style.get("dashed") == "1" else ""
        color = style.get("strokeColor", "#AAB7C4")
        width = num(style.get("strokeWidth"), 1.0)
        parts.append(
            f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="{width}"'
            f'{dash} marker-end="url(#arrow)"/>'
        )

    parts.insert(
        2,
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#AAB7C4"/></marker></defs>',
    )
    parts.append("</svg>")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts), encoding="utf-8")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="把 .drawio 渲染成近似 SVG 预览")
    parser.add_argument("drawio", type=Path, help="输入的未压缩 .drawio 文件")
    parser.add_argument("--out", type=Path, help="输出 SVG 路径（默认同名 _预览.svg）")
    args = parser.parse_args()

    out = args.out or args.drawio.with_name(args.drawio.stem + "_预览.svg")
    try:
        warnings = render(args.drawio, out)
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    print(f"Preview written: {out}")
    print("提醒：这是几何近似预览，不是官方渲染；最终版式须在 Draw.io Desktop 导出后人工验收。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
