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
8. **可视化嵌入决策**（混合图的关键）：逐个模块扫描——这个模块有没有适合用迷你可视化表达的信息？判断依据：

| 论文中出现的信息 | 嵌入什么可视化 | 模块框尺寸 |
|----------------|-------------|----------|
| 具体数值对比（准确率、F1、损失值） | 柱状图或横条图 | 加宽至 ≥5cm |
| 注意力机制 / 相关性矩阵 | 热力图（N×N 色块） | 加高至 ≥4cm |
| 时序信号 / 波形 / 频谱 | 波形曲线或频谱柱状图 | 加高至 ≥4cm |
| 分类/聚类结果 | 散点图（带颜色聚类） | 加宽加高 |
| 训练过程 / 收敛曲线 | 双线折线图（train/val） | 加宽至 ≥5cm |
| 空间分布 / 地理数据 | 网格热图（彩色方格） | ≥4cm×4cm |
| 模型对比（多个基线） | 分组柱状图或雷达图 | ≥5cm 宽 |
| 概率分布 / 直方图 | 柱状分布图 | ≥4cm 宽 |
| 无具体数值，纯文字描述 | 不嵌入——用普通框+文字 | 标准尺寸 |

**原则**：不是每个模块都要嵌入可视化——只在有**具体数值或可量化信息**时嵌入。纯流程/逻辑模块保持普通框。一张图中嵌入可视化的模块占 30-50% 最佳——全部嵌入太密，全部不嵌入又回到纯框图。嵌入可视化的模块框要比普通框大 1.5-2 倍，给可视化留足空间。

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

加载 `references/review-checklist.md`，按其中的视觉审查清单、设计师视角审查、具体检查方向（40 项）、六维度评分逐项执行。总分 30 分且全部审查项通过才交付。

**步骤⑥**：迭代修复（未满分则回到④，直到 30/30）。

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
| 数据可视化混合图 | 框图内嵌波形/柱状图/热力图 | 信号处理、深度学习注意力、频谱分析 |

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
| 含数据可视化的图 | `references/data-visualization.md` | 波形、频谱柱状图、热力图矩阵、前后对比 |
| draw.io 科研展示图 | `references/drawio-modes.md` | 6 种模式（A-F）、视觉花样库、XML 骨架 |
| 步骤⑤评估打分 | `references/review-checklist.md` | 视觉审查清单、设计师审查、40项检查、评分标准 |
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
