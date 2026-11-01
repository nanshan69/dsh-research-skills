---
name: nsfc-figure
description: 为 NSFC 申请书、基金标书或研究方案创建/重绘概念图、研究内容关系图和技术路线图；产出可编辑、可验证的 Draw.io XML。本机为 DSHM 端侧适配版（python 工具 + scripts/run_nsfc.py 调用，含离线预览脚本）；纯数据统计图、照片处理、论文原图复用不触发本 skill。
whenToUse: 需要画技术路线图/概念图/研究内容关系图，或要把方案正文压缩成一张可编辑的 .drawio 图时；也用于检查已有 .drawio 的结构与导出元数据。
---

# NSFC 申请书图示（DSHM 端侧适配版）

目标是让图在脱离正文时仍能传达一个明确结论，并同时交付可编辑、可追溯的源图。
默认使用未压缩的 `.drawio` XML；只有数据驱动的统计图才优先考虑 Python 绘图
（统计图请改用 `research-toolkit` 的 `figures.py`）。

## 0. 本机怎么跑（先读这一节）

本机（HarmonyOS + DSHM）**没有** `python3`、`git`、`drawio` 命令；脚本一律用 Agent 的
`python` 工具 + 本目录的运行器调用：

```python
python(file="/data/storage/el2/base/haps/phone/files/dsh/home/skills/nsfc-figure/scripts/run_nsfc.py",
       args=["generate_roadmap",
             "--config", "/绝对路径/roadmap.json",
             "--output", "/绝对路径/roadmap.drawio"])
```

可用工具（不带参数运行 runner 会列出）：

| 工具 | 用途 | 典型 args |
|---|---|---|
| `generate_roadmap` | JSON 配置 → 未压缩 .drawio | `["generate_roadmap","--config","配置.json","--output","图.drawio"]` |
| `validate_drawio` | 结构校验（根单元、ID 唯一、边引用、几何、页界） | `["validate_drawio","图.drawio"]`（可加 `--json`） |
| `preview_roadmap` | 生成近似 SVG 预览，查文字溢出/连线走向 | `["preview_roadmap","图.drawio","--out","图_预览.svg"]` |
| `check_export_metadata` | 查 SVG/PNG 是否嵌入完整编辑源 | `["check_export_metadata","图.svg","图.png"]` |

三条硬规矩：

1. **路径一律写绝对路径**：`python` 工具的 cwd 是 `/`，相对路径会解析到别处。
2. **不要**用 `python(file=".../generate_roadmap.py")` 直接跑原脚本：工具会把脚本路径塞进
   `sys.argv[1:]` 且不把脚本目录加入 `sys.path`，必然报 `unrecognized arguments` 或
   `No module named 'validate_drawio'`。必须走 `run_nsfc.py`。
3. 脚本里**不要加** `from __future__ import annotations`：本机 python 工具是包装执行，
   该语句不在文件第一行会直接 `SyntaxError`（上游原版正因此跑不起来，已移除）。

## 1. 工作流

1. 先从正文提炼"对象/问题 → 研究阶段或内容 → 验证 → 预期认识"的信息骨架。
   **不得**为了版式美观虚构研究内容、证据或因果关系。
2. 根据主要关系选择布局：
   - 递进过程：横向或纵向技术路线；
   - 多项内容共同支撑目标：并列分栏后汇聚；
   - 理论与实验反复校正：闭环，但仅在正文确有反馈关系时绘制回路；
   - 时间与任务：甘特图，不要硬套流程图。
3. 将正文压缩为两级文本。卡片标题表达动作或产物，说明文字只保留区分该卡片所需的信息；
   避免把段落搬进图中。三栏时单卡说明宜 ≤45 个中文字符，四栏 ≤35 个。
4. 生成或编辑 Draw.io 源文件（配置 schema 见 `references/drawio-authoring.md`）：

   ```python
   python(file=".../scripts/run_nsfc.py",
          args=["generate_roadmap",
                "--config", ".../assets/three-stage-roadmap.json",
                "--output", "/绝对路径/roadmap.drawio"])
   ```

   三/四阶段的分栏技术路线可直接用脚本；需要自由构图、实验装置或复杂示意时，
   从生成结果继续在 diagrams.net / Draw.io Desktop 中编辑，不要退化成不可编辑截图。
5. 结构验证：

   ```python
   python(file=".../scripts/run_nsfc.py", args=["validate_drawio", "/绝对路径/roadmap.drawio"])
   ```

6. **预览与视觉验收**——本机**没有** Draw.io Desktop，做不到官方渲染导出：
   - 先用 `preview_roadmap` 生成近似 SVG，检查文字是否溢出、箭头是否穿过文字、整体是否可读；
   - 交付时必须如实写"**XML 已验证、渲染导出未在本机执行**"，并把图标记为"待视觉验收"，
     **不得**称为可直接使用；
   - 最终由用户在装 Draw.io Desktop 的电脑上导出 SVG/PDF/PNG，并按申请书实际尺寸打开检查；
     导出命令见 `references/drawio-authoring.md`。
7. 拿到最终 SVG/PNG 后，检查是否意外嵌入完整编辑源：

   ```python
   python(file=".../scripts/run_nsfc.py", args=["check_export_metadata", "/绝对路径/图.svg"])
   ```

## 2. Draw.io 交付约束

- 保留未压缩 XML，便于版本审查、局部修改和错误定位。
- 所有 `mxCell` ID 唯一；顶层包含 `0`、`1` 两个根单元；边必须引用存在的源/目标节点。
- 给节点写明几何尺寸，使用正交连接线，主阅读方向一致并避免交叉。
- 统一字体规则：Word／PPT 的中文正文写宋体、中文标题（含副标题）写黑体；本技能输出图片时，中文正文写字体栈 `SimSun, Songti SC`，中文标题及副标题写字体栈 `SimHei, STHeiti`，以兼顾 Windows 与 macOS；英文和数字只用 `Times New Roman`。生成器用 HTML `span` 分配混排片段的字体；手工编辑时保留这些片段和字体栈，不能只改全局 `fontFamily`。圆角、边框和语义色保持一致。颜色负责区分研究阶段，不负责装饰。
- 图片若不可避免，应嵌入文件或使用可移交的相对资源；禁止保留仅在作者机器有效的绝对路径。
- 涉及未公开申请书时优先用本地桌面版编辑，不把 `.drawio` 源文件或完整正文上传到未经授权的在线服务。
- 图中术语、编号和正文逐项核对。图注解释"图说明什么"，不要重复图内全部文字。
- 内部工作包同时保留 `.drawio` 源文件和矢量预览；正式提交或公开分发的 SVG/PNG 不应嵌入完整编辑源，
  且必须检查隐藏图层、画布外对象和元数据。只有投稿系统限制时才用高分辨率 PNG。

## 3. 资源路由

- 版式、配色、字号、导出格式：`references/drawio-authoring.md`。
- 快速搭分栏技术路线：复制 `assets/three-stage-roadmap.json` 改内容，再跑 `generate_roadmap`。
- 生成器完整用例：`examples/fictional-technical-roadmap.json` + 同名 `.drawio`；源图已同步宋体／黑体／Times New Roman。现成 PNG 是字体修订前的官方导出旧预览，未重新导出，不代表当前源图字体（示例为虚构内容，只用于验证工作流）。
- 本机适配改了什么、以后怎么升级：`references/dshm-adaptation.md`。

## 4. 本机能力边界（别踩）

| 事项 | 事实 | 处置 |
|---|---|---|
| `python3` / `git` 命令 | 不存在（`command not found`） | 用 `python` 工具 + `run_nsfc.py`；仓库文件用 `wget` 下 zip |
| Draw.io Desktop CLI | 未安装，无法官方导出 | `preview_roadmap` 只做几何近似；最终渲染交给用户 PC |
| PIL / cairosvg / matplotlib | 装不上（C 扩展被拒） | 不要试；PNG/TIFF 转换在 PC 上做 |
| 字体 | 图片默认正文 `SimSun, Songti SC`、标题及副标题 `SimHei, STHeiti`、英文／数字 `Times New Roman`；本机未确认这些字体可用 | 近似 SVG 原样保留源单元及 HTML 字体栈，不强制改用系统字体；不安装字体。查看器可能回退，最终导出须在具备相应字体的机器上核对 |
| 中文路径 | 可用，但拼路径时注意引号与空格 | 一律绝对路径 + 引号 |

## 5. 验收

- 只看图，能否说出核心问题、研究阶段、验证方式和最终汇聚点？
- 缩放到申请书中的实际宽度后，最小文字是否仍可读？
- 箭头是否表达真实依赖，而非仅为了连接所有卡片？
- XML 验证是否通过？近似预览有无溢出/压字？
- 是否已如实标注"渲染待视觉验收"？最终 SVG/PDF/PNG 是否已在官方 Draw.io 里打开确认无裁切、
  无溢出、无字体替换、无连接线错位、无意外嵌入的编辑源？
- 图与正文的术语、顺序、编号和预期产出是否一致？
