# 端侧适配说明（DSHM / HarmonyOS）

本目录是上游 [njzjz/nsfc-agent-skills](https://github.com/njzjz/nsfc-agent-skills) 的
`nsfc-figure` 技能，按本机（HarmonyOS + DSHM 内嵌 Python 3.12）实际能跑通的方式改过。
上游原样安装**跑不起来**，原因是下面三条，改法也照这三条。

## 改了什么

| # | 上游原状 | 本机事实 | 适配 |
|---|---|---|---|
| 1 | 三个脚本都带 `from __future__ import annotations`（紧跟在 docstring 后） | `python` 工具的 file 模式是包装执行，会把脚本内容包进 `-c`，导致该语句不在文件第一行 → `SyntaxError: from __future__ imports must occur at the beginning of the file` | 三个脚本**删除**该行；本机 Python 3.12 支持 `list[str]` / `X \| None` 等写法，删掉不影响运行 |
| 2 | `SKILL.md` 教人用 `python nsfc-figure/scripts/generate_roadmap.py ...` | 本机没有 `python3` 命令；`python` 工具 file 模式会把脚本路径塞进 `sys.argv[1:]`，且**不会**把脚本所在目录加入 `sys.path` | 新增 `scripts/run_nsfc.py` 运行器（runpy 分发 + 注入 `sys.path`），`SKILL.md` 全部改成经由它调用 |
| 3 | 交付流程要求"用官方 Draw.io Desktop 导出 SVG/PDF/PNG 并检查" | 本机无 `drawio` CLI，也无 PIL/cairosvg/matplotlib（C 扩展装不上），无法官方渲染 | 新增 `scripts/preview_roadmap.py`：纯标准库把未压缩 `.drawio` 渲染成近似 SVG，用于查文字溢出/连线走向；`SKILL.md` 明确要求交付时标注"XML 已验证、渲染未在本机执行、待视觉验收" |

另外的本机约定：

- `SKILL.md` 增补了 `whenToUse`、本机能力边界表、资源路由（指向本说明）。
- `references/drawio-authoring.md` 保留 PC 端导出说明，`check_export_metadata` 示例经 `run_nsfc.py` 调用。
- **科研字体**：Word／PPT 的中文正文写宋体、中文标题（含副标题）写黑体；图片中的中文正文写字体栈 `SimSun, Songti SC`，中文标题及副标题写字体栈 `SimHei, STHeiti`。字体栈先尝试 Windows 名称，再尝试 macOS 名称；英文和数字只用 `Times New Roman`。生成器对混排文本使用显式 HTML `span`；图题、副标题、阶段标题、卡片短标题及产出／目标前缀使用标题字体栈，说明和产出内容使用正文字体栈，数字编号用 Times New Roman。只改全局 `fontFamily` 不能完成混排分配。
- **近似预览字体**：读取单元 `fontFamily`，解析 HTML `div`／`span` 的字体继承与 `font face`，将分段字体栈、字号和加粗原样写入 SVG `tspan`。SVG 根节点不指定系统字体，也不把源字体改成 HarmonyOS Sans SC。字体度量和布局仍是近似值。
- `assets/three-stage-roadmap.drawio` 和 `examples/fictional-technical-roadmap.drawio` 已同步上述字体，保留原有内容、几何和连线。现成 PNG 未改，是字体修订前的官方导出旧预览，不能用于确认当前源图字体。

## 没改、但要知道的

- **字体文件与实际渲染**：脚本不安装、嵌入字体。本机未确认 SimSun、Songti SC、SimHei、STHeiti 和 Times New Roman 是否可用；缺字时查看器可能自行回退。源文件和 SVG 字体栈属性正确不代表实际字形已确认；应在具备字体栈相应候选及 Times New Roman 的机器上官方导出，并检查断行和裁切。
- **`validate_drawio.py` 的能力**：只证明 XML 结构与图不变量成立（根单元、ID 唯一、边引用、
  几何、页界），**不能**证明版式好看。近似预览同理。
- **`check_export_metadata.py`**：检查 SVG/PNG 里是否嵌入了完整 `mxfile` 编辑源。上游示例 PNG
  的检查结果为 `CLEAN`（仅 `date:create` / `date:modify`）。

## 自检（装完想确认能用）

在本技能的 `scripts/` 目录下，用 Agent 的 `python` 工具依次跑：

```python
# 1) 生成
python(file=".../scripts/run_nsfc.py",
       args=["generate_roadmap", "--config", ".../assets/three-stage-roadmap.json", "--output", "/绝对路径/t.drawio"])
# 2) 结构校验
python(file=".../scripts/run_nsfc.py", args=["validate_drawio", "/绝对路径/t.drawio"])
# 3) 近似预览
python(file=".../scripts/run_nsfc.py", args=["preview_roadmap", "/绝对路径/t.drawio", "--out", "/绝对路径/t.svg"])
# 4) 导出元数据
python(file=".../scripts/run_nsfc.py", args=["check_export_metadata", ".../examples/fictional-technical-roadmap.png"])
```

预期：1) `Generated editable Draw.io document: ...`；2) `OK: ... (1 diagram(s), 23 vertices, 5 edges)`；
3) `Preview written: ...`；4) `CLEAN: ...`。（2026-10-28 实测通过。）

## 以后怎么升级

上游更新时：重新下 zip（本机没有 git，用 `wget https://codeload.github.com/njzjz/nsfc-agent-skills/zip/refs/heads/master`），
把 `nsfc-figure/` 覆盖到本目录，然后**重做上表第 1 条**（删 `from __future__` 行），
确认 `run_nsfc.py`、`preview_roadmap.py` 仍在，保留宋体／黑体／Times New Roman 的混排生成与预览规则及两份源图，再跑一遍上面的自检。
