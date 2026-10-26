# dsh-research-skills

DSHM（DSH on HarmonyOS）的**科研技能包**：8 个技能，装完开机自动铺到 `$DSH_HOME/skills/`。

这些技能用于做课题、写论文、查文献、跑统计、生成 Word/PPT。**与酒馆（dsh-tavern）无关** ——
从 `dsh-tavern-gate` 里拆出来单独成包，就是为了让两边各管各的。

## 包含的技能

### 文献与证据

| 技能 | 用途 |
|---|---|
| `research-pubmed-search` | PICO 拆解、PubMed/Europe PMC/ClinicalTrials.gov 检索式构造、PRISMA-S 留痕、标题摘要与全文筛选、OA 全文获取、引文核对与 Vancouver 参考文献 |
| `research-evidence-extraction` | 文献证据卡结构化提取、偏倚风险评估（RoB 2 / ROBINS-I / SYRCLE / AMSTAR 2）、GRADE 证据分级、证据表维护 |

### 写作与投稿

| 技能 | 用途 |
|---|---|
| `research-paper-writing` | IMRaD 骨架、CONSORT/STROBE/PRISMA/SPIRIT 报告规范、标题与结构化摘要、期刊分档、cover letter、审稿回复逐条写法、参考文献格式 |
| `academic-humanizer-zh` | 中文学术写作去 AI 腔：论文正文/摘要/讨论/审稿回复、研究方案、基金标书。保留全部数字、引用、术语与作者声音 |
| `academic-humanizer-en` | 英文学术写作与基金申请（NSF Project Summary/Description、NIH Specific Aims）的清晰度与声音 |
| `translate-paper-pdf-to-md` | 英文论文 PDF → 目标语言 Markdown，保留图、表、公式、引文、结构与领域术语 |

### 统计与工具链

| 技能 | 用途 |
|---|---|
| `research-stats-plan` | 样本量/效能计算、统计分析计划（SAP）：分析集、主要分析、缺失与伴发事件、多重性、模型假设、报告规范 |
| `research-toolkit` | 纯 Python 工具链（无 pandoc/LibreOffice）：Markdown→DOCX（封面/页眉/目录/三线表）、Markdown/DSL→PPTX、DOCX/PDF 读取检索、CSV↔XLSX、SVG 图表、样本量与统计核对、PubMed 检索 |

`research-toolkit` 自带 10 个脚本 + 一个 PPTX 模板（`scripts/_pptx_template.pptx`），
总计约 240 KB，是本包里最大的部分。

## 安装

DSHM「设置 → 插件」里贴本仓库地址，或：

```sh
pnpm add github.com/nanshan69/dsh-research-skills
```

**装完必须完全重启 DSHM** 才会铺技能。

## 它怎么工作

`index.js` 的 `apply()` 只做一件事：调用 `syncBundledSkills()` 把包内 `skills/` 同步到
`$DSH_HOME/skills/`。没有 UI、没有 HTTP 路由、不注入任何服务 —— 技能是纯数据，
铺好之后由 DSH 的技能加载器接管。

同步规则（幂等）：

- 目标不存在 → 写入
- 内容完全相同 → 不写盘（正常启动零 IO 写）
- 内容不同 → 旧文件先备份到 `$DSH_HOME/skills-backup/<时间戳>/` 再覆盖
- `preserve: ['ohos-']` → 不动 DSHM 环境自带的 `ohos-*` 说明
- **不删除**用户自己放在 `$DSH_HOME/skills/` 下的任何技能

升级时（重贴链接或覆盖包目录）新版本技能会一并刷新。

## 手动铺（不用插件通道）

把 `skills/` 下 8 个目录/文件直接复制到 `$DSH_HOME/skills/` 即可，效果相同。

## 从酒馆里拆出来的原因

此前这 8 个技能内嵌在 `dsh-tavern-gate/skills/`（酒馆开关插件）里。问题：

1. **语义错位** —— 装酒馆的人不一定是做科研的，却会收到一堆科研工具
2. **体积** —— 占 gate 包的大半
3. **耦合** —— 改科研技能要动酒馆仓库
4. **升级不独立** —— 两个东西绑在一个版本号上

拆开后：酒馆仓库只留 `ohos-*` 环境说明（与 DSHM 本身强相关），科研技能单独升级。

## License

MIT（技能文档部分）；`research-toolkit/scripts/` 下的 Python 脚本随本仓库同许可证。
