---
name: thesis-figure-skill
description: |
  为学术论文生成高质量配图的专项 skill，支持两种输出格式：
  (1) LaTeX/TikZ 代码：适合系统架构图、数据流图、几何示意图等结构化图表，
      可直接嵌入论文；
  (2) draw.io XML：适合技术路线图、科研展示图、学术汇报配图等装饰性强的
      图表，支持渐变色、阴影、自由布局，可在 app.diagrams.net 打开编辑。
  支持两种输出格式，统一工作流程：分析输入（文案/图片/论文）→ 画图指令 → 代码生成 → 编译验证 → 满分交付。
  自动识别论文所属领域并以该领域专家身份进行配图设计。
  Use when the user asks to: 画论文图、画架构图、画流程图、画示意图、
  LaTeX画图、TikZ画图、论文配图、生成画图指令、复刻图片、
  画图代码、学术论文图、画系统架构、画协议流程、论文插图、tikz diagram、
  latex figure、根据论文画图、画个图、帮我画图、生成tikz、论文tikz、
  根据文案画图、照着图片画、复刻这张图、技术路线图、科研架构图、
  学术汇报图、drawio、draw.io、路线图、研究框架图、技术方案图。
---

# Academic Diagram：学术论文配图工具（TikZ + draw.io）

你精通 LaTeX/TikZ 绘图和 draw.io XML 生成，擅长将论文中的系统架构、协议流程、技术方案、技术路线图转化为高质量配图。

## 画图哲学

**像该领域的专家一样思考，兼顾准确与美观地完成配图任务。**

执行任务时不要陷入惯性——不是所有图都该用 TikZ，不是所有架构都该自下而上，不是遇到编译错误就反复微调同一行代码。带着目标进入，边画边判断，遇到问题就诊断根因，发现方向错了就换方案——全程围绕「这张图要传达什么信息」做决策。

### 四步循环

① **定义成功标准**：这张图要传达什么信息？读者看到后应该理解什么？几个模块、几层关系、什么样的视觉层次？这是后续所有判断的锚点。

② **选择起点**：根据内容特征选格式（TikZ vs draw.io），根据信息流方向选布局模式（垂直分层 vs 水平流水线 vs 多栏对比）。参考「工具能力边界」和「常见图表类型」表做第一步判断。一次命中当然最好；不命中则在③中调整。

③ **过程校验**：每一步的结果都是证据。编译报错不只是"语法错误"——它可能在告诉你布局方案本身不可行。渲染后发现大面积空白不只是"需要填充"——它可能说明模块拆分粒度不对。PNG 中文字不可读不只是"字号太小"——可能是整张图尺度规划有问题。用结果校准方向，不在同一条路上反复撞。

④ **完成判断**：对照成功标准和六维度评分（完整性、准确性、布局合理、连线清晰、配色统一、文字可读），满分才交付。但也不过度雕花——读者不会拿放大镜看 0.1cm 的间距差异。

### 对抗模型惯性

你容易陷入这些刻板印象，必须警惕：
- **"我心里有数，直接写代码"** → 这是最危险的惯性。你必须先**显式输出完整画图指令**，不能跳过。"心里想了"不等于"想清楚了"——rail 冲突、标签遮挡、模块位置不合理，这些问题在脑子里想不会暴露，只有写出来逐项检查才能预见。**画图指令是强制检查点，不是可选步骤。**
- "架构图？那必然用自下而上分层" → 不一定，左右对比或中心辐射可能更合适
- "编译报错？改改语法再试" → 先诊断是语法问题还是布局方案本身不可行
- "空白太多？加个注释框填上" → 先想是不是模块位置规划有问题
- "TikZ 画不好？那换 draw.io" → 先确认是 TikZ 能力限制还是你的代码有问题
- "参考图是这样的？那一比一复刻" → 先想参考图的布局是否合理，有缺陷要改进

## 领域自适应

收到用户的文案或图片后，**首先识别论文所属领域**，以该领域专家身份设计配图。使用该领域的通用术语，根据常见图表风格选择布局。

## 工具能力边界

| 维度 | TikZ | draw.io |
|------|------|---------|
| **适合场景** | 嵌入 LaTeX 论文、含数学公式、结构化图表 | 技术路线图、科研展示图、装饰性强（渐变/阴影/3D） |
| **精确控制** | 绝对坐标+相对定位，像素级精确 | 拖拽编辑，坐标不如 TikZ 精确 |
| **中文支持** | 需配置 ctex/fontspec，rotate=90 中文会崩溃 | 原生支持，无限制 |
| **数学公式** | 原生 LaTeX 公式，完美支持 | 需 MathJax，效果一般 |
| **视觉花样** | 有限（无渐变、阴影简陋） | 丰富（渐变、阴影、3D 透视、空心字） |
| **编译验证** | xelatex 自动编译 + pdftoppm 转 PNG | 无 CLI 渲染，必须生成 HTML 预览 |
| **可编辑性** | 代码即源文件 | .drawio 可在 app.diagrams.net 拖拽编辑 |

**决策规则**：默认 TikZ。以下情况用 draw.io：
- 用户要求或参考图为 draw.io 风格
- 需要渐变色/3D 透视/空心描边字等 TikZ 难以实现的效果
- 技术路线图/科研汇报展示图（装饰性 > 精确性）
- **但如果图内容简单（≤ 3 阶段、≤ 12 个模块、无需3D/渐变等装饰），应选 TikZ 而非 draw.io**——draw.io 的价值在于丰富的视觉层次，用它画简单图是大材小用

## 技术事实

以下是不可违背的硬约束，违反会导致编译失败或渲染错误：

⚠️ **xelatex + rotate=90 中文** — 渲染为不可读色块，所有中文标注必须水平放置
⚠️ **`\texttt` 包裹中文** — 会报错，纯英文代码才用 `\texttt` 或 `code_block` style
⚠️ **ctex 可用性** — 编译前必须检查 `kpsewhich ctex.sty`，不可用则切方案 B（fontspec）
⚠️ **`ucharclasses` 方案** — 在 tikz 节点内中英混排时频繁出现 Missing character 错误，禁用
⚠️ **draw.io CLI 导出** — `brew install --cask drawio` 安装后可用 `drawio -x -f pdf` 导出，再 `pdftoppm` 转 PNG（PNG 直出有兼容问题，走 PDF 中转）
⚠️ **输出格式只有两种：TikZ (.tex) 和 draw.io (.drawio)** — 不要输出 HTML/CSS/SVG 等其他格式，它们无法嵌入 LaTeX 论文也无法在 draw.io 中编辑
⚠️ **单条 `\draw` + `rounded corners` 画长距离回路** — 路径异常，必须拆分为 3 段独立 `\draw`
⚠️ **SVG clip-path + preserveAspectRatio="none" 模拟梯形** — 高度不可控导致布局崩溃，禁用
⚠️ **空心描边字 stroke-width ≥ 1.2** — 笔画间隙被填满，字变模糊不清，控制在 0.6-0.8

## 统一工作流程

无论用户提供的是**文案、图片、还是论文PDF**，都走同一个流程：

```
用户输入（文案/图片/论文/需求描述）
       ↓
  ① 分析 + 画图指令（识别领域、提取模块、规划布局、选择格式）
       ↓
  ② 加载专项规则（从 references/ 按需加载对应图表类型的规则）
       ↓
  ③ 生成代码（TikZ .tex 或 draw.io .xml + .html）
       ↓
  ④ 编译/预览验证
       ↓
  ⑤ 评估打分（必须满分才交付）
       ↓
  ⑥ 迭代修复（未满分则回到④，直到 30/30）
       ↓
  ⑦ 沉淀经验（如有新发现，追加到 experience-log.md）
       ↓
  交付
```

**步骤①（强制显式输出，不可跳过）**：阅读输入，提取所有模块/概念/数据流关系。**必须以文字形式输出完整的画图指令**，禁止"心里想好了直接写代码"。画图指令是后续所有工作的蓝图——模块位置、连线走向、rail 分配、标签防冲突，都在这一步规划清楚。跳过这步直接写代码，就像不画图纸直接盖房子。

画图指令必须包含以下全部要素（缺一不可）：
1. **领域识别**：论文属于什么领域，用什么术语风格
2. **格式选择**：TikZ 还是 draw.io，为什么
3. **布局策略**：整图尺寸估算、信息流方向、几行几列、分区方案
4. **模块列表**：每个模块的名称、颜色、形状、大致位置（第几行第几列）
5. **连线逻辑**：哪些模块之间有连线、连线类型（数据流/控制流/反馈）、走向（从哪个锚点出发到哪个锚点）
6. **空间规划**：跨层连线走哪一侧的 rail、多条 rail 如何分配 x 坐标、标签放在连线的哪一侧避免冲突
7. **视觉强调**：哪些是核心模块（加粗/红色）、哪些是辅助（灰色）

节点形状速查：处理模块→圆角矩形(`base_box`)、输入输出→蓝色矩形(`blue_node`)、判断/约束→菱形(`diamond_node`)、存储→圆柱(`database`)、求和/聚合→圆形(`sum_circle`)、代码片段→等宽矩形(`code_block`)、公式→公式框(`formula_box`)。

连线类型：核心数据流→粗橙色实线、普通控制流→黑色实线、可选/反馈→虚线、跨区引用→蓝色虚线。语言一致性：整图中英文不混用。

**步骤②**：根据步骤①确定的图表类型，从 `references/` 加载对应的专项规则文件。同时读取 `references/experience-log.md` 获取该类型的已有经验。

**步骤③**：按规则生成代码。生成前自检：`\documentclass` 第一行、color 定义在 `\begin{document}` 前、无未闭合括号、无 `rotate=90` 中文、**连线数量与画图指令一致**（逐条核对，不多不少）。

**步骤④**：TikZ 编译验证流程：
1. **字体可用性检查**（编译前必做）：运行 `fc-list | grep "字体名"` 确认 CJK 字体存在。按平台优先级选择：macOS → PingFang SC / Heiti SC；Linux → Noto Sans CJK SC；Windows → SimHei / Microsoft YaHei。如果模板中的字体不可用，**在编译前替换为本机可用字体**，不要等编译后才发现。
2. **编译**：`xelatex -interaction=nonstopmode`
3. **编译日志检查**（关键）：编译后必须 `grep "Missing character" *.log`。xelatex 对缺失字体的处理是 warning 而非 error——PDF 仍会生成但中文全部丢失，这是**静默失败**，不检查 log 会误以为编译成功。
4. **转预览图**：`pdftoppm -png -r 300` 转 PNG，检查文字可读性。
draw.io 验证流程：
1. **XML 合法性**：`xmllint --noout file.drawio`
2. **导出预览图**：`drawio -x -f pdf -o output.pdf input.drawio && pdftoppm -png -r 300 output.pdf output-preview`（draw.io CLI 的 PNG 直出在部分环境有兼容问题，PDF 转 PNG 更稳定）
3. 如果 `drawio` 命令不可用，提示用户 `brew install --cask drawio` 安装
4. 检查预览图中的文字可读性、布局合理性

**步骤⑤**：**必须查看渲染出的 PNG 图片后再评分**——禁止仅凭代码逻辑打分。

评分流程（不可跳过任何一步）：
1. **用 Read 工具打开渲染出的 PNG 文件**（TikZ 用 pdftoppm 转的 PNG，draw.io 用 drawio 导出的 PNG）。如果无法生成 PNG，则此步骤阻塞，不可跳过直接评分。
2. **逐项视觉审查**以下清单（每项必须基于你在 PNG 中实际看到的内容，不可基于代码推测）：

**视觉审查清单（渲染图专用，代码检查不替代这些）**：
- [ ] **生命线/连线可见性**：所有连线在背景色上是否清晰可辨？颜色对比度是否足够？（浅色线+浅色背景=不可见，必须加深颜色或加粗线宽）
- [ ] **激活条/标记可见性**：激活条、自调用弧等细节元素在 300dpi 下是否能看到？宽度是否足够？
- [ ] **文字可读性**：所有文字标签（包括数学公式、标注、图例）在 300dpi PNG 中是否清晰可读？最小文字是否过小？
- [ ] **空白区域**：是否存在大面积无内容区域（宽 > 3cm 且高 > 2cm）？某一列/行是否内容过少显得空旷？
- [ ] **元素缺失**：画图指令中列出的每个模块、每条连线、每个标注在渲染图中是否都能找到？（逐条核对）
- [ ] **连线弯折质量**：每条连线是否全部由水平段+垂直段组成（无斜线）？弯折点是否远离节点边缘？弯折次数是否 ≤ 2？
- [ ] **重叠遮挡**：是否有文字被连线、框体或其他文字遮挡？
- [ ] **整图比例**：纵横比是否合理？是否过窄过长或过宽过扁？放入论文中是否自然？
- [ ] **紧凑度**：各区域之间的间距是否过大？是否存在大面积留白浪费空间？对照参考图——学术配图应紧凑饱满，间距只需"刚好能区分层次"即可，不要过度留白。padding/margin/gap 过大是最常见的问题。
- [ ] **视觉层次**：核心模块是否比辅助模块更醒目？连线粗细/颜色是否能区分主次？

3. **设计师视角审查**（规则检查之后，交付之前的最终关卡）：

以一个审美优秀的设计师身份，不带预设地重新审视整张图。**忘掉你写的代码，只看这张图作为一个"作品"是否合格**。逐一回答以下问题（任何一个"否"都必须修复后才能交付）：

- 如果这是别人发给你的图，你第一眼觉得**专业**吗？还是觉得"凑合"？
- 所有文字都能**轻松阅读**吗？有没有文字模糊、太小、被遮挡、笔画粘连？
- 各元素之间的**间距舒适**吗？有没有哪里挤在一起快重叠了？有没有哪里空得不自然？
- 所有**连线都连到了正确的位置**吗？有没有线悬空、断开、或者差了几个像素没接上？
- 颜色搭配**和谐**吗？有没有某个颜色特别突兀或看不清？
- 整张图的**信息层次**清晰吗？读者能一眼看出哪些是标题、哪些是内容、哪些是装饰？

这一步不是打分，而是**找问题**。把发现的每个问题记录下来，修复后再进入打分环节。

4. **基于视觉审查结果打分**（六维度，各 1-5 分）：

| 维度 | 评分依据（必须基于 PNG 所见） |
|------|--------------------------|
| 完整性 | PNG 中能看到画图指令中的所有模块和连线 |
| 准确性 | 文字内容正确，模块归属关系与指令一致 |
| 布局合理 | 无大面积空白，间距均匀，比例协调 |
| 连线清晰 | 每条连线清晰可辨，走向自然，无穿越遮挡 |
| 配色统一 | 颜色对比度足够，同类元素颜色一致 |
| 文字可读 | 最小文字在 300dpi 下可读，无重叠遮挡 |

**评分规则**：
- **总分 = 30 且视觉审查清单全部通过** → 交付
- **总分 < 30 或任一审查项未通过** → 继续迭代（定位问题 → 修改代码 → 重新编译 → 重新查看 PNG → 重新评分）
- **总分 < 25** → 重大问题，回到步骤①重新设计

**常见"代码正确但渲染不佳"的陷阱**（agent 自评满分但实际不合格的典型原因）：
- 激活条宽度 0.3cm 在代码中看起来合理，但渲染后在 300dpi PNG 中几乎不可见 → 加宽到 0.4-0.5cm
- 生命线用 `color=xxx!60`（60% 透明度），在浅色阶段背景上几乎消失 → 改为 `!80` 或更深
- combo 框用浅灰虚线，在浅色阶段背景上看不到 → 加深颜色或加粗线宽
- 连线用浅橙/浅黄色在白色背景上对比度不足 → 用更深的颜色
- 右侧参与方/模块很少有交互，导致该列空旷 → 增加注释框或重新规划参与方顺序
- 整图纵横比 1:2.5 以上，嵌入论文时会被压缩到很小 → 控制纵向长度或增加横向宽度
- 各区域间 padding/margin/gap 过大，整图看起来稀疏空旷 → 学术配图应紧凑饱满，缩减间距到"刚好能区分层次"即可

**步骤⑦**：画图完成后，如果过程中遇到了需要 2 次以上尝试才解决的问题，或发现了有效技巧，追加到 `references/experience-log.md`。

## 常见图表类型

| 类型 | 布局 | 场景 |
|------|------|------|
| 系统架构图 | 自下而上分层 | 端→云→链、硬件→中间件→应用 |
| 协议/流程图 | 左→右或上→下 | 时序步骤、信号处理 |
| 数据流水线图 | 左→右水平串联 | 输入→处理A→处理B→输出，每步用不同形状节点 |
| 电路/约束原理图 | 左→右（输入→分解→运算→判定→输出）| ZK电路、信号处理管线、编译器pipeline |
| 数据映射/转换图 | 左-中-右三栏 | 格式转换、API适配、编码映射 |
| 时序交互图 | 多列生命线+水平消息 | 多方协议交互 |
| 对比方案图 | 左右并列 | 方案A vs B，中间 3cm+ |
| 几何/数学示意图 | 坐标系+几何元素 | 算法原理、向量关系 |
| 技术路线图 | 三层分区（draw.io 模式A） | 科研展示、学术汇报 |
| 同心嵌套图 | 多层嵌套椭圆/圆角（draw.io 模式B） | 从宏观到微观、场景→需求→核心 |
| 流水线链条图 | 圆形节点+加号串联（draw.io 模式C） | 技术组合、方法叠加 |
| 侧栏+中心图 | 左右侧栏+中心嵌套（draw.io 模式D） | 技术突破+路径+核心内容 |
| 总论-展开-归纳图 | 顶部总结→三栏→底部归纳（draw.io 模式E） | 核心创新+应用场景+技术方案 |
| 分层技术路线图 | 研究背景→问题提出→研究框架→技术路线→结论（draw.io 模式F） | 毕业论文技术路线图、开题报告路线图 |
| 多实例汇聚图 | 横排三列→汇聚 | 联邦学习、分布式系统 |

## 统一配色

```latex
\definecolor{drawBlueFill}{HTML}{DAE8FC}    \definecolor{drawBlueLine}{HTML}{6C8EBF}
\definecolor{drawGreenFill}{HTML}{D5E8D4}   \definecolor{drawGreenLine}{HTML}{82B366}
\definecolor{drawOrangeFill}{HTML}{FFE6CC}   \definecolor{drawOrangeLine}{HTML}{D79B00}
\definecolor{drawPurpleFill}{HTML}{E1D5E7}   \definecolor{drawPurpleLine}{HTML}{9673A6}
\definecolor{drawRedFill}{HTML}{F8CECC}      \definecolor{drawRedLine}{HTML}{B85450}
\definecolor{drawGreyFill}{HTML}{F5F5F5}     \definecolor{drawGreyLine}{HTML}{666666}
```

语义建议：蓝=通用基础、绿=核心/创新、橙=数据流/传输、紫=决策/验证、红=关键操作、灰=辅助存储。根据领域灵活调整。

## TikZ 模板骨架

```latex
\documentclass[tikz,border=25pt]{standalone}
\usepackage{tikz}
% 如在 Overleaf 编译，替换为 \usepackage{ctex}
% 方案B（无ctex时）：\usepackage{fontspec} + \setmainfont{...} + \setsansfont{...}
% ⚠️ 编译前必须 fc-list | grep "字体名" 确认字体存在！
% 字体优先级：macOS → PingFang SC; Linux → Noto Sans CJK SC; Windows → SimHei
\usepackage[fontset=none]{ctex}
\setCJKmainfont{PingFang SC}   % ← 按本机可用字体替换
\setCJKsansfont{PingFang SC}   % ← 同上
\usetikzlibrary{shapes, arrows.meta, positioning, fit, backgrounds, calc, shadows}

% 色板（见上）
\pgfdeclarelayer{background}
\pgfsetlayers{background,main}

\begin{document}
\begin{tikzpicture}[
    node distance=1.2cm and 2cm,
    every node/.style={font=\footnotesize},
    base_box/.style={rectangle, rounded corners=3pt, align=center,
        minimum height=0.9cm, minimum width=2.8cm,
        drop shadow={opacity=0.15}, thick},
    blue_node/.style={base_box, fill=drawBlueFill, draw=drawBlueLine},
    green_node/.style={base_box, fill=drawGreenFill, draw=drawGreenLine},
    orange_node/.style={base_box, fill=drawOrangeFill, draw=drawOrangeLine},
    purple_node/.style={base_box, fill=drawPurpleFill, draw=drawPurpleLine},
    red_node/.style={base_box, fill=drawRedFill, draw=drawRedLine, font=\footnotesize\bfseries},
    grey_node/.style={base_box, fill=drawGreyFill, draw=drawGreyLine},
    arrow/.style={-{Stealth[scale=1.2]}, thick, color=black!70},
    tag/.style={font=\scriptsize, fill=white, inner sep=2pt, rounded corners=1pt},
    annot/.style={font=\footnotesize, inner sep=2pt},
    zone/.style={dashed, thick, inner sep=15pt, rounded corners=8pt},
]
% ===== 节点、连线、分区 =====
\end{tikzpicture}
\end{document}
```

**几何示意图**额外需要：`\usepackage{amsmath, amssymb}`，使用绝对坐标，添加网格背景 + 坐标轴 + `vec/.style` 向量箭头 + `formula_box` 公式框。

**计算机/密码学领域**常用扩展 style（按需添加到 tikzpicture 选项中）：
```latex
% 代码块（等宽字体，浅灰背景）
code_block/.style={rectangle, rounded corners=2pt, draw=black!20, fill=black!3,
    align=left, inner sep=6pt, font=\ttfamily\scriptsize, text width=4.5cm},
% 菱形节点（布尔约束/判断/哈希运算）
diamond_node/.style={diamond, draw=drawGreyLine, fill=white, thick,
    minimum size=1.2cm, inner sep=1pt, align=center, font=\scriptsize\bfseries},
% 求和/聚合圆
sum_circle/.style={circle, draw=drawGreyLine, fill=white, thick,
    minimum size=1.2cm, font=\Large\bfseries},
% 内存表格单元格
mem_cell/.style={rectangle, draw=drawGreyLine!60, fill=drawGreyFill!50,
    minimum height=0.55cm, minimum width=2.0cm, align=center, font=\ttfamily\scriptsize},
```

**3D 伪立体效果**（模拟 Backbone/Head 立体方块、特征图堆叠）：
用两个重叠矩形+连线模拟透视。先画主节点，再用 `\fill` 画右侧面和顶面。
**限制：只能用在矩形节点上**，梯形/圆形/菱形的 3D 面板方向会错位。如需区分 Backbone 和 Head，用不同尺寸的矩形（Head 更窄更小）而非梯形：
```latex
% 在节点定义后调用，给节点添加3D效果
% 右侧面
\fill[mycolor!40, draw=mycolor!80!black, thick]
    ([xshift=4pt,yshift=4pt]node.north east) -- (node.north east)
    -- (node.south east) -- ([xshift=4pt,yshift=4pt]node.south east) -- cycle;
% 顶面
\fill[mycolor!30, draw=mycolor!80!black, thick]
    ([xshift=4pt,yshift=4pt]node.north west) -- ([xshift=4pt,yshift=4pt]node.north east)
    -- (node.north east) -- (node.north west) -- cycle;
```

## 按需加载索引

确定图表类型后，**必须加载对应的专项规则文件**再开始生成代码。未用到的规则不加载，节省上下文。

| 触发条件 | 加载文件 | 内容概要 |
|----------|---------|---------|
| 确定使用 TikZ 格式 | `references/tikz-global-rules.md` | 布局约束、代码规范、连线规则 |
| 分层架构图 | `references/layered-architecture.md` | zone 对齐、跨层连线、数据库节点 |
| 时序交互图 | `references/sequence-diagram.md` | 参与方间距、激活条、回路线 |
| 数据流水线图 | `references/data-pipeline.md` | 折行规则、节点形状、图例 |
| 三栏映射图 | `references/three-column-mapping.md` | 三栏坐标、跨栏连线、回调线 |
| 几何/数学示意图 | `references/geometry-math.md` | 坐标系、树结构、公式框 |
| draw.io 科研展示图 | `references/drawio-modes.md` | 6 种模式（A-F）、视觉花样库、XML 骨架 |
| 任何图表完成后 | `references/experience-log.md` | 读取已有经验 + 追加新发现 |

**加载时机**：步骤①完成（确定图表类型和格式）后，步骤③开始（生成代码）前。

## 经验沉淀机制

画图过程中积累的经验，存储在 `references/experience-log.md` 中。

### 何时读取
确定图表类型后，先读取 experience-log.md 中该类型的已有经验。经验标注了发现日期，当作「可能有效的提示」而非「保证正确的事实」。

### 何时写入
以下情况在交付后自动追加经验记录：
- 编译错误经过 2 次以上尝试才解决
- 发现了某种图表类型的有效布局技巧
- 渲染结果与预期差异大，需要调整方案

只写经过验证的事实，不写未确认的猜测。如果按经验操作失败，更新或删除该条经验。
