"""nsfc-figure 运行器：用 Agent 的 `python` 工具（file 模式）跑本目录脚本。

为什么需要它：本机 `python` 工具的 file 模式会把脚本路径塞进 sys.argv[1:]，
且不会自动把脚本目录加入 sys.path。直接跑 generate_roadmap.py 会报
"unrecognized arguments" 或 "No module named 'validate_drawio'"。

用法（Agent 侧）：
    python(file="<skills>/nsfc-figure/scripts/run_nsfc.py",
           args=["generate_roadmap", "--config", "配置.json", "--output", "图.drawio"])

不带参数运行会列出可用工具。
"""
import os
import runpy
import sys

_argv = list(sys.argv[1:])
_self = ""
if _argv and _argv[0].endswith("run_nsfc.py"):
    _self = _argv.pop(0)
if not _self:
    _self = globals().get("__file__", "")
TOOLS = os.path.dirname(os.path.abspath(_self)) if _self else "."
sys.path.insert(0, TOOLS)

if not _argv:
    tools = sorted(
        f[:-3] for f in os.listdir(TOOLS)
        if f.endswith(".py") and not f.startswith("_") and f not in ("run_nsfc.py", "preview_roadmap.py")
    )
    print("用法: run_nsfc.py <工具名> [参数...]")
    print("可用工具: generate_roadmap, validate_drawio, check_export_metadata, preview_roadmap")
    raise SystemExit(2)

tool, rest = _argv[0], _argv[1:]
script = os.path.join(TOOLS, tool + ".py")
if not os.path.exists(script):
    print("没有这个工具: " + tool, file=sys.stderr)
    raise SystemExit(2)
sys.argv = [tool + ".py"] + rest
runpy.run_path(script, run_name="__main__")
