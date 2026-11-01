"""research-toolkit 运行器：用插件的 python 工具（file 模式）跑同目录的工具脚本。

用法（Agent 侧；<技能目录> 是 skill 工具加载本技能时显示的 Base directory）：
    python(file="<技能目录>/scripts/run_tool.py",
           args=["md2docx", "输入.md", "--out", "输出.docx"])

不带参数运行会列出全部可用工具。输出路径建议用绝对路径（工具默认以工作目录解析相对路径）。
"""
import os
import runpy
import sys

_argv = list(sys.argv[1:])
_self = ""
if _argv and _argv[0].endswith("run_tool.py"):
    _self = _argv.pop(0)
if not _self:
    _self = globals().get("__file__", "")
# 运行器自己所在的目录优先：常驻解释器里 DSH_TOOL_DIR 会保留上一次运行的值，
# 不同设备形态的两份技能副本交替运行时，按环境变量会用到另一份副本的脚本
_here = os.path.dirname(os.path.abspath(_self)) if _self else ""
TOOLS = _here or os.environ.get("DSH_TOOL_DIR") or "."
os.environ["DSH_TOOL_DIR"] = TOOLS
if TOOLS in sys.path:
    sys.path.remove(TOOLS)
sys.path.insert(0, TOOLS)
# python 工具是常驻解释器：按模块名清掉本目录各脚本的缓存（含从另一份副本加载的同名模块），
# 改过的 _util 等才会重新加载
for _f in os.listdir(TOOLS):
    if _f.endswith(".py"):
        sys.modules.pop(_f[:-3], None)

if not _argv:
    tools = sorted(f[:-3] for f in os.listdir(TOOLS)
                   if f.endswith(".py") and not f.startswith("_") and f != "run_tool.py")
    print("用法: run_tool.py <工具名> [参数...]")
    print("可用工具: " + ", ".join(tools))
    raise SystemExit(2)

tool, rest = _argv[0], _argv[1:]
script = os.path.join(TOOLS, tool + ".py")
if not os.path.exists(script):
    print("没有这个工具: " + tool)
    raise SystemExit(2)
sys.argv = [tool + ".py"] + rest
runpy.run_path(script, run_name="__main__")
