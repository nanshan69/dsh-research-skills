# 英文期刊投稿规范

适用于英文论文、投英文期刊的稿件、英文摘要和审稿回复。与中文稿共用的规则（图表自明、术语统一、
引文一一对应、伦理声明、翻译和润色的适用边界）见 `text-conventions.md`；文风见 `../../academic-humanizer-en/SKILL.md`。

## 0. 先定目标期刊的体例

1. 用户的明确要求优先，例如字体（见 `../../research-toolkit/SKILL.md`）；与期刊要求冲突时先说明差异，由用户决定。
2. 目标期刊的 Instructions for Authors 和投稿系统要求：字数、摘要格式、参考文献格式、图表格式、声明。
   投稿前逐条核对，不凭印象。
3. 期刊采用的体例手册。生物医学期刊多遵循 ICMJE Recommendations，体例常见四类：

| 体例 | 常见期刊 | 识别特征 |
|---|---|---|
| AMA 第 11 版 | JAMA 系列及很多医学期刊 | 上标编号引文；*P* = .03（无前导0）；mean (SD) |
| NEJM | NEJM | 方括号或上标编号；P<0.001（有前导0） |
| Lancet | The Lancet 系列 | 居中小数点 0·5；p=0·03 |
| APA 第 7 版 | 心理学、护理、部分公共卫生期刊 | 作者-年代引文；*p* < .001 |

期刊没写明体例时，按该刊近期发表的同类文章统一。下文默认按 AMA，其他体例的差异逐项注明。
标注“待核”的条目没能在线核对体例原文，投稿前按目标期刊作者须知确认。

## 1. 投稿材料

- **Title page**：标题、作者全名、单位（院系、机构、城市、邮编、国家）、通讯作者及邮箱、ORCID、
  字数统计（正文和摘要分开）、关键词、running title（如期刊要求）。
- **标题**：写清研究对象和设计，不写结论；RCT 写 randomized。标题中不用非通用缩写。
- **摘要**：按期刊要求用结构化或非结构化摘要，字数上限以作者须知为准（各刊具体上限待核；已发表摘要常超出网上流传的上限，
  不能据此反推）。常见标题：
  - IMRaD 式：Background/Objective、Methods、Results、Conclusions；
  - JAMA 式：Importance、Objective 或 Objectives（待核）、Design, Setting, and Participants、
    Interventions（观察性研究用 Exposures，待核）、Main Outcomes and Measures、Results、Conclusions and Relevance；
    临床试验另加 Trial Registration。
  - Results 写主要结局的效应量、95% CI 和样本量；摘要中不引文献，缩写在摘要内单独定义；临床试验写注册号。
- **要点框**：按期刊要求写，例如 JAMA 的 Key Points（Question、Findings、Meaning，已发表实例约 100 词），
  Lancet 的 Research in context。
- **Keywords**：3～10 个，优先用 MeSH 词。
- **Cover letter、审稿回复**：写法见 `../SKILL.md` 第 4、5 节。
- **报告规范清单**：按设计附 CONSORT、STROBE、PRISMA 2020、STARD、TRIPOD、ARRIVE 2.0、CARE 等清单和流程图，
  并在清单中标出稿件页码或行号。

## 2. 投稿版式

- 多数期刊要求审稿稿：双倍行距、12 pt、页边距 2.5 cm（1 inch）、连续行号、页码；字体按期刊要求。
  `md2docx` 默认是中文稿版式（五号字、1.5倍行距、无行号），生成后在 Word 中改：
  全选设为 12 pt 和双倍行距，布局 → 行号 → 连续。交付时说明这一步。
- 正文顺序常见为：Title page → Abstract → Main text → Acknowledgments/Declarations → References →
  Tables（每表一页）→ Figure legends。图片文件单独上传。按期刊要求调整。
- 补充材料按期刊命名编号：eTable 1、eFigure 1（JAMA）或 Table S1、Figure S1（多数期刊），正文中引用到。

## 3. 拼写、语法与文风

- 美式或英式拼写全篇一种，按期刊（randomized/randomised、tumor/tumour、analyze/analyse）。
- 时态：Methods 和 Results 用过去时；已确立的知识、图表说明和结论用现在时。
- 用主动语态还是被动语态按期刊惯例；施动者不重要时用被动语态。可以用 we。
- significant 只表示统计学意义；一般意义上用 important、substantial、marked 等。
- data 按复数处理（the data were），按期刊。
- 以人为先的写法：patients with diabetes，不写 diabetics；不用带歧视或标签化的词。
  报告性别、种族和民族时，说明分类方式和数据来源（参照 SAGER 指南和期刊政策）。
- 文风和主张-证据匹配按 `academic-humanizer-en`；句中不用 em dash。

## 4. 标点

- 全部用半角标点。替换中文稿常见的全角字符：，。（）：；“”～ 改为 , . ( ) : ; " " 和 to 或 en dash。
- 句号后空一格。括号前空一格：mean age (SD)，不写 age(SD)。
- serial comma（A, B, and C）：AMA、APA 使用；英式期刊多不使用，按期刊。
- 复合形容词放在名词前时加连字符：a 12-week trial、follow-up visit；名词形式 follow up 按词义。
- 数值范围：正文用 to 或 from…to、between…and（10 to 20 mg）；表格和括号内可用 en dash 或连字符（按期刊），
  如 AMA 的 95% CI, 0.5%-3.5%。% 和 °C 在范围两端都写：0.5%-3.5%、37.5°C-37.9°C。
  出现负值时用 to（−0.84 to −0.001），负号用真正的减号“−”；AMA 要求同一张表中有负值时整张表都用 to。
- 引号：美式句号和逗号放在引号内，英式放在引号外。
- 缩写标点按体例：AMA 写 eg、ie、vs，不加句点，eg 和 ie 只用在括号内并后接逗号，如 (eg, kidney)；
  APA 写 e.g.、i.e.、vs.。et al 是否加句点也按体例。

## 5. 数字

- AMA 中，除句首和少数习惯用法外，数字一般用阿拉伯数字。NEJM 已发表文章中，小于 10 的计数也写数字
  （in 2 patients），只有 two groups 这类非数据计数拼写，规则原文待核。APA 中 0～9 一般拼写，
  但带单位的计量、统计量、百分数、年龄等用数字。拿不准时按目标期刊近期文章。
- 句首不用阿拉伯数字：拼写出来，或改写语序（Forty-five patients…；In total, 45 patients…）。
- 千位分隔（依据各刊已发表文章的排版，体例手册原文待核）：AMA/JAMA 四位数不分节（1500），
  五位及以上用窄空格分节（12 345，JAMA 用窄不换行空格 U+202F），不用逗号；NEJM 四位数不分节（1500），
  五位及以上用逗号（12,345）；APA 7 从四位数起用逗号（1,500；12,345）。按目标期刊。
- 小数点用点（Lancet 用居中点 0·5）。不会大于1的统计量（*P*、相关系数）是否写前导0按体例：
  AMA 和 APA 不写（*P* = .03），NEJM 写（P=0.03）；其他数值一律写前导0（0.5 mg）。
- 百分数配分子和分母：45 of 120 patients (37.5%)。百分数的小数位与样本量相称，样本量小时不保留过多小数，
  具体按期刊（部分期刊规定 n<100 时不保留小数）。
- 日期：美式 January 5, 2024；英式 5 January 2024。不用 2024/1/5 这类格式。
- 乘号用 ×（3 × 10⁸），不用字母 x 或 *。

## 6. 单位

- 用 SI 单位；部分期刊要求同时给出传统单位，按期刊。
- 数值和单位之间空一格（5 mg、2.5 h）；% 紧贴数字（30%）。摄氏度按体例：AMA 写 37°C，SI 写 37 °C。
- 升写大写 L：mL、mmol/L、μL；微写 μ，不写 u；中文稿的 ℃（单字符）改为 °C。
- 时间：s、min、h 可以缩写；day、week、month、year 在正文中一般拼写，表格中按期刊（AMA 允许 d、wk、mo、y）。
- 复合单位不连用斜线：mg/kg per day 或 mg·kg⁻¹·d⁻¹，不写 mg/kg/d。
- 血压单位：AMA 写 mm Hg，其他期刊多写 mmHg，按期刊。
- 药物用国际非专利名（INN）或期刊指定的通用名，小写；商品名首字母大写，需要时注明生产商。

## 7. 统计表述

- 统计量符号用斜体：*P*/*p*、*t*、*F*、*r*、*R*²、*n*、*N*、*z*、*U*、χ²。APA 中 *M*、*SD*、*SE* 也用斜体。
- *P* 值写法：

| 体例 | 一般写法 | 很小的值 | 小数位 |
|---|---|---|---|
| AMA | *P* = .03 | *P* < .001；最大写 *P* > .99 | *P* > .01 时最多2位，*P* < .01 时最多3位；四舍五入会跨过 .05 时可保留3位（可选，待核） |
| NEJM | P=0.03 | P<0.001 | 大于 0.01 用2位，0.001～0.01 用3位（待核） |
| Lancet | p=0·03（等号两侧不空格） | p<0·0001 | 按期刊，已发表实例有 p=0·0045 |
| APA | *p* = .03 | *p* < .001 | 2～3位 |

  不写 *P* = .000；不只写 *P* < .05 或 NS；不写 marginally significant、trend toward significance。
- 均值与离散度：AMA 写 mean (SD)，例如 62.3 (8.1) years，不用 ±；APA 写 *M* = 62.3, *SD* = 8.1。
  偏态数据写 median (IQR)，例如 45 (32-60)。
- 效应量和置信区间：AMA 写 mean difference, 1.2 (95% CI, 0.4-2.0)；有负值时写 −1.5 to 2.0；
  NEJM 写 (95% CI, 0.4 to 2.0)；Lancet 写 HR 0·80 [95% CI 0·69–0·93]（方括号，CI 后不加逗号）；
  APA 写 95% CI [0.4, 2.0]。CI 首次出现时可写 confidence interval (CI)。
- 统计方法写检验方法、单侧或双侧、α 水准、多重比较校正、软件及版本（R version 4.3.2、Stata 18）。
- 精度与样本量相称，不报告超过测量精度的小数位。RCT 基线表不写 *P* 值。
- 结果写法和解读纪律见 `../../research-stats-plan/SKILL.md`。

## 8. 表、图与图注

- 正文中按顺序引用：Table 1、Figure 1（部分期刊写 Fig. 1）。引用时首字母大写。
- 表：每表一页，表题在上；不用竖线，横线尽量少；单位写在栏目中，例如 Age, mean (SD), y。
  表注定义全部缩写，并说明统计方法；脚注符号按期刊（AMA 用上标 a、b、c；也常见 *、†、‡、§、‖、¶）。
- 图：图题和图注（figure legend）集中写在稿件末尾或按期刊放置，说明误差线表示 SD、SE 还是 95% CI，
  定义全部缩写和符号。图片按期刊格式和分辨率提交，例如 Elsevier：照片类 300 dpi、照片与线条组合图 500 dpi、
  线条图 1000 dpi。
- 图中文字按期刊要求的字体和字号。部分期刊要求无衬线字体，例如 Nature：Helvetica 或 Arial，5～7 pt，
  分图标号用 8 pt 粗体小写 a、b、c。与用户默认字体（Times New Roman）不同时，先向用户说明，由用户决定。
- 每张图表单独看也能读懂；正文只概括关键结果，不重复表中全部数字。

## 9. 术语、缩写和命名

- 缩写首次出现写 full term (ABBR)，之后一律用缩写；摘要、正文、每张图表分别定义。
  只出现1～2次的术语不缩写；句首不用缩写；标题中不用非通用缩写。期刊列出的标准缩写（DNA、CI、OR）可直接使用。
- 基因用斜体、蛋白用正体，按 HGNC（人）和 MGI（小鼠）命名：*TP53*/p53、*Trp53*。
- 物种学名用斜体：*Escherichia coli*，之后 *E. coli*。
- 试剂、仪器写 name (manufacturer, city, country) 或按期刊；软件写名称和版本。
- 同一概念全文用同一个术语，不为避免重复换词。

## 10. 参考文献

- 格式严格按期刊。生物医学期刊常见两类：
  - Vancouver/ICMJE（NLM）：按引用顺序编号；作者超过6人时列前6人加 et al.（NLM 数据库现已列出全部作者，
    稿件中按期刊）；期刊名用 NLM 缩写，不用斜体。
    示例：Smith J, Lee K, Wang L, Chen Y, Zhao M, Liu H, et al. Title of article. N Engl J Med. 2023;388(5):412-21.
  - AMA：上标编号；作者不超过6人时全列，超过6人时列前3人加 et al（6 人阈值待核）；期刊名缩写用斜体，页码写全。
    示例：Smith J, Lee K, Wang L, et al. Title of article. *N Engl J Med*. 2023;388(5):412-421. doi:10.1056/NEJMoa0000000
  - APA 7：作者-年代制；参考文献最多列 20 位作者；DOI 写成 https://doi.org/… 形式。
- 正文编号与文末列表一一对应；引文放在相关语句处，标点与上标的先后按期刊。
- 引原始研究；不引已撤稿文献（投稿前用 Retraction Watch 或 PubMed 核对）；预印本注明 preprint。
- 用 `pubmed cite` 生成初稿、`pubmed verify` 核对；不得编造文献，规则见 `../../research-pubmed-search/SKILL.md`。
- 中文文献：用英文著录并在末尾注明 (in Chinese)，或按期刊要求。

## 11. 声明

按期刊要求逐项写，常见项目：
- Ethics approval：伦理委员会名称、批准号；Informed consent：知情同意方式；动物研究写 IACUC 或等效机构及 ARRIVE。
- Trial registration：注册库和注册号。ICMJE 要求在首例受试者签署入组知情同意时或之前注册，
  注册日期以首次提交注册材料的日期为准。
- Data sharing statement：数据是否、何时、如何共享。ICMJE 要求：2018-07-01 起，报告试验结果的稿件须附此声明；
  2019-01-01 起开始入组的试验，须在注册时写明数据共享计划。
- Conflict of interest：按期刊或 ICMJE 披露表填写。
- Funding：资助机构的官方英文名和项目编号（如 National Natural Science Foundation of China, grant No. xxxxxxxx），
  说明资助方在研究中的作用。
- Author contributions：多数期刊用 CRediT 角色；作者资格符合 ICMJE 四条标准。
- AI 使用披露：按期刊政策和 ICMJE Recommendations（2026 年 1 月版第 V 节 Use of AI by Authors）。
  投稿时披露是否使用 AI 辅助技术：用于写作辅助的在致谢中说明，用于数据收集、分析或作图的在方法中说明。
  AI 不能列为作者，也不能作为一手来源引用；作者对全部内容负责；未披露可能被视为学术不端。
- 致谢：列出不符合作者标准的贡献者，事先征得同意。

## 12. 中国作者常见问题

- 全角字符混入英文稿：，。（）：；“”～、℃ 和全角空格。交付前检索替换。
- 括号前缺空格，句号后无空格；中文标点后接英文。
- 冠词和单复数：a/an/the 漏用或误用，不可数名词加 s。
- 中式表达：with the development of…、more and more、play an important role in、has been paid more attention。
  改为具体陈述。
- 滥用 obviously、significantly、very；“such as…, etc.” 重复（such as 后不加 etc.）。
- 句子过长、主语过远；一句只讲一件事。
- 作者姓名：名在前、姓在后（Xiaoming Wang），全篇及与 ORCID 一致；单位用官方英文名称。
- 中文基金、医院、伦理委员会名称用官方英文名，不自行意译。

## 13. 投稿前自查

- [ ] 已按目标期刊的 Instructions for Authors 核对字数、摘要、参考文献、图表格式和声明
- [ ] 全篇无全角标点和全角空格；拼写为美式或英式其中一种
- [ ] *P* 值、CI、mean (SD) 写法统一，符合期刊体例
- [ ] 数值与单位间距、单位符号（mL、μ、°C）正确
- [ ] 缩写在摘要、正文和图表中首次出现时都已定义
- [ ] 图表按顺序引用，图注说明误差线和缩写，图片分辨率符合要求
- [ ] 参考文献格式统一，编号与正文一一对应，无撤稿文献
- [ ] 伦理、注册、数据共享、利益冲突、资助、作者贡献、AI 使用声明齐全
- [ ] 审稿版式（双倍行距、行号、页码）已在 Word 中设置
- [ ] 报告规范清单和流程图已准备好
