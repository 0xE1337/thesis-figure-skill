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

**你画的每一张图，都要让读者第一眼就觉得：这个作者很用心。**

不是"能看就行"，不是"信息完整就好"——你要追求的是**让人想多看两眼的图**。顶会论文的配图之所以好看，不是因为它们没有 bug，而是因为设计者在信息密度、视觉层次、空间节奏上都下了功夫。你要像设计师一样思考，而不是像程序员一样堆代码。

执行任务时不要陷入惯性——不是所有图都该用 TikZ，不是所有架构都该自下而上，不是遇到编译错误就反复微调同一行代码。带着目标进入，边画边判断，遇到问题就诊断根因，发现方向错了就换方案——全程围绕「这张图要传达什么信息」和「怎么让它好看」做决策。

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
- **"改了 3 轮了差不多了吧"** → 标准不会因为你努力了就降低。30/30 就是 30/30
- **"这个小重叠用户应该看不出来"** → 用户永远能看出来。你觉得"小"的问题在 300dpi 下清清楚楚
- **"坐标差 0.2cm 应该没关系"** → 0.2cm 在渲染图上是 24 像素，人眼对这种"差一点没对齐"极其敏感

### 设计野心（最重要的一节）

**你最大的敌人不是 bug，而是平庸。** 一张没有 bug 但平淡无奇的图，不如一张有点小瑕疵但设计感十足的图。过度追求"安全"会杀死设计感——不要因为怕出错就选最简单的方案。

#### 最低设计门槛

以下是**及格线**，达不到就不要开始写代码：

| 维度 | 最低要求 | 死板的标志（不合格） |
|------|---------|-------------------|
| **信息密度** | 一张图 ≥ 15 个视觉元素（节点+连线+标签+装饰） | 全图只有 6-8 个方框直连 |
| **视觉层次** | 至少 3 级大小差异（大框/中框/小标注） | 所有框一样大、一样的圆角矩形 |
| **连线丰富度** | 至少 2 种线型（实线+虚线/粗细/颜色区分） | 全部黑色实线直连 |
| **空间利用** | 画面填充率 ≥ 70%，四角不能全空 | 内容缩在中间一团，四周大面积空白 |
| **信息附加值** | 除了原文信息外，图至少额外传达 1 个洞察（对比、趋势、层次关系） | 纯粹是文字转方框，没有任何视觉增值 |

#### 让图"活"起来的技巧

不要画"示意图"，要画"信息图"——区别在于：
- **示意图**：A→B→C→D，四个一样大的框，四条一样的箭头。读者看了想打哈欠
- **信息图**：A 是小输入框，B 是大处理模块（内含子结构），C 有嵌入的数据可视化，D 用强调色标出。读者看了觉得"这张图信息量真大"

具体做法：
1. **大小对比**：核心模块的框要比辅助模块**大 2 倍以上**，不要所有框一样大
2. **嵌入子结构**：复杂模块内部展示子组件（如 Transformer 里面画出 Multi-Head Attention + FFN），不要只写一行文字
3. **数据可视化嵌入**：论文中有数值的地方（准确率、损失、对比数据），**主动嵌入**柱状图/曲线/热力图，不要等用户要求
4. **装饰有度**：背景色 zone、阴影、渐变标题栏——这些让图看起来像精心设计的，而不是 AI 随手生成的。但装饰必须有信息含义（颜色区分层级、阴影区分前后），纯粹装饰不要加
5. **紧凑排列**：元素之间间距"刚好能呼吸"就够了——学术配图的美感来自**紧凑饱满**，不是**宽敞松散**
6. **详情展开框**：如果一个模块内部结构复杂，用虚线框在**紧邻位置**展开详情——展开框要**紧贴**被展开的模块，不能隔很远用虚线连

#### 反面案例（这样的图不合格）

```
❌ 死板图：
  [Input] → [Process A] → [Process B] → [Process C] → [Output]
  五个一样大的框，五条一样的箭头，没有任何视觉变化

✅ 好图：
  ┌─小─┐      ┌─── 大框（含子结构）───┐      ┌─强调色─┐
  │Input│ ──→  │ Module A              │ ══→  │Output │
  └────┘      │  ┌──┐ ┌──┐ ┌──┐      │      │★83.5% │
              │  │子│→│子│→│子│      │      └───────┘
              │  └──┘ └──┘ └──┘      │
              │  [嵌入: 损失曲线📉]   │
              └──────────────────────┘
  核心模块大、有子结构、有数据嵌入；输出模块用红色强调结果
```

### 质量红线

以下行为是硬伤，必须避免（但不要因为怕犯这些错就把图画得过于简单）：
1. **跳过画图指令直接写代码** — 返工率 100%
2. **不看 PNG 就打满分** — 代码正确 ≠ 渲染正确
3. **溢出/重叠/穿越交付** — 文字溢出、标签重叠、连线穿文字 = 质量事故

### 对抗性自审

渲染出 PNG 后，评分前做两轮自审：

**第一轮：找 bug**（防守）— 有没有重叠、溢出、方向错？有就修。

**第二轮：找平庸**（进攻）— 问自己：
1. **"这张图有没有让人想多看两眼的地方？"** — 如果没有，加大核心模块、加子结构、加嵌入可视化
2. **"所有框看起来是不是差不多大？"** — 如果是，拉开大小差异
3. **"信息密度配得上论文复杂度吗？"** — 5 层架构不能只画 8 个框

**第三轮：找排版问题**（精度）— 回头对照 ASCII 草图检查：
1. **"草图中同一行的元素，在渲染图中还是同一行吗？"** — 水平对齐有没有偏移？
2. **"草图中等宽的面板，在渲染图中还是等宽吗？"** — 宽度/高度是否一致？
3. **"左右两半看起来一样重吗？"** — 遮住左半边看右半边，再遮住右半边看左半边，感觉均衡吗？
4. **"同级元素之间的间距一致吗？"** — 比如三个并排面板之间的间距应该一样，不能一个 0.5cm 另一个 2cm

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

## 环境依赖自动检测

首次画图时自动检测并安装缺失依赖，无需用户手动操作：

```bash
# 1. TeX 编译环境（不自动安装，太大了，提示用户）
which xelatex || echo "⚠️ 请安装 TeX Live: brew install --cask mactex-no-gui (macOS) 或 apt install texlive-xetex (Linux)"

# 2. PDF 转 PNG 工具（不自动安装，提示用户）
which pdftoppm || echo "⚠️ 请安装 poppler: brew install poppler (macOS) 或 apt install poppler-utils (Linux)"

# 3. Python 质检工具（自动安装）
python3 -c "import pdfplumber" 2>/dev/null || pip3 install pdfplumber
python3 -c "import pathfinding" 2>/dev/null || pip3 install pathfinding
```

**规则**：
- `xelatex`、`pdftoppm`、CJK 字体：体积大，只提示不自动装，告知用户安装命令
- `pdfplumber`、`pathfinding`：体积小，缺失时直接 `pip3 install` 自动安装
- 检测只在**首次编译前**执行一次，后续跳过

## 统一工作流程

无论用户提供的是**文案、图片、还是论文PDF**，都走同一个流程：

```
用户输入（文案/图片/论文/需求描述）
       ↓
  ⓪ 环境依赖检测（首次自动执行，缺失则安装/提示）
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
4. **模块列表**：每个模块的名称、颜色、形状、大致位置（第几行第几列）。**核心模块必须比辅助模块大 2 倍以上**——不要所有框一样大
5. **连线逻辑**：哪些模块之间有连线、连线类型（数据流/控制流/反馈）、走向。**至少 2 种线型**（粗细/实虚/颜色）区分主次
6. **空间规划**：跨层连线走哪一侧的 rail、多条 rail 如何分配 x 坐标、标签放在连线的哪一侧避免冲突
7. **视觉强调**：哪些是核心模块（加粗/加大/强调色）、哪些是辅助（灰色/小框）——**拉开视觉层次差异**
8. **设计野心检查**：对照"设计野心"一节的最低设计门槛，不达标则主动丰富设计
9. **ASCII 布局草图（排版的关键）**：用 ASCII 字符画出整图的空间分配草图。这一步是**视觉思考**——让你在写代码前就能"看到"布局是否合理。

ASCII 草图的画法：
- 用 `┌┐└┘─│` 画框，用 `→↓←↑` 画连线方向
- 标注每个区域的相对大小（[小]、[中]、[大]）
- 标注对齐关系（同一行的元素写在同一行，同一列的元素上下对齐）
- 标注面板分割方式（如"底部三等分"、"右侧 1/3 用于面板"）

示例（ResNet 混合图的布局草图）：
```
┌──────────────────────────────────────────────┐
│ [小]Input→Conv→Pool  [中]S1→S2               │ 管线行
│              ┌──────────────────┐             │
│              │ [大] Stage 3     │→[中]S4      │ 英雄行
│              │  内部Bottleneck  │  ↓          │
│              └──────────────────┘ GAP→FC→Out  │ 分类行
├──────────────┬──────────────┬────────────────┤
│  热力图 1/3  │ 训练曲线 1/3 │ 准确率柱 1/3  │ 面板行（等宽）
└──────────────┴──────────────┴────────────────┘
```

草图画完后做三项排版检查：
- **对齐组**：同一行的元素是否水平对齐？同一列的是否垂直对齐？在草图中就能看出来
- **视觉平衡**：左右两半的"重量"大致相当吗？上下是否头重脚轻？
- **间距节奏**：同级元素之间的间距是否一致？（如面板行的三个面板应该等宽等高等间距）

草图不合理就重画草图，**不要带着烂布局进入编码**。

10. **可视化嵌入决策**（混合图的关键）：逐个模块扫描——这个模块有没有适合用迷你可视化表达的信息？判断依据：

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

**步骤②**：根据步骤①确定的图表类型，从 `references/` 加载对应的专项规则文件。同时加载：
- `references/experience-log.md` — 该类型的踩坑经验（避免重复犯错）
- `references/evolution.md` — 该类型的已验证最佳参数（**直接使用这些参数作为起点，不从零试错**）

进化基线是 25 批次 157 张图的结晶。如果你打算用一个和基线不同的参数值，**你必须有充分理由**——"我觉得这样好"不是理由，"这种特殊场景下基线值会导致 XX 问题"才是。

**步骤③**：按规则生成代码。**生成前强制预检（Pre-flight Checklist）**——逐项确认后才动笔写代码：

| # | 检查项 | 确认方式 |
|---|--------|---------|
| P1 | 画图指令已显式输出，包含全部 8 项要素 | 回看指令，缺项则补 |
| P2 | 每个框的坐标已规划，同行框 y 一致 | 列出所有框的 (x,y)，检查同行 y 相等 |
| P3 | 每条连线的起止锚点已规划，方向与数据流一致 | 列出 A.anchor → B.anchor，确认方向感 |
| P4 | 嵌入可视化的框已预留足够尺寸 | 逐框计算：标题+内容+轴标签+padding |
| P5 | 跨层/跨区连线的 rail 已分配，无交叉 | 画出 rail 的 x 坐标列表 |
| P6 | zone 边界已计算，覆盖所有内容+padding | 列出 zone 的四角坐标 |
| P7 | 易犯错误已对照 experience-log.md 排查 | 读取该图表类型的经验条目 |

任何一项不通过就**停下来补完**，不要"先写代码再说"。代码阶段的 bug 修复成本是指令阶段的 5 倍。

代码规范自检：`\documentclass` 第一行、color 定义在 `\begin{document}` 前、无未闭合括号、无 `rotate=90` 中文、**连线数量与画图指令一致**（逐条核对，不多不少）。

**步骤③.5a（可选：自动路径规划）**：当图中连线 ≥ 8 条且有交叉风险时，可用路径规划器自动计算避障路径：
```bash
# 1. 将节点位置和连线需求写成 JSON
# 2. 运行路径规划器
python3 references/tikz-path-router.py routing-spec.json
# 3. 将输出的 \draw 代码替换手写的连线代码
```
路径规划器基于 A* 算法自动避开所有节点矩形，输出正交路径（水平+垂直线段，圆角弯折）。适用于底层基础设施、电路图等连线密集的区域。连线少的简单图不需要用。

**步骤③.5b（编译前自动验证）**：生成 .tex 代码后、编译前，运行坐标验证器：
```bash
python3 references/tikz-validator.py <file.tex>
```
验证器自动检测：微斜线（相邻坐标不共享 x 或 y）、容器溢出（node 超出 zone）、标签碰撞（bounding box 重叠）、箭头方向反转（中间点超越目标）。
- **ERROR** → 必须修复后才能编译，不要浪费编译时间
- **WARN** → 建议修复，编译后在 PNG 中重点关注
- **PASS** → 进入编译

**步骤④**：TikZ 编译验证流程：
1. **环境与字体检查**（编译前必做）：如首次执行，先运行⓪环境依赖检测。然后 `fc-list | grep "字体名"` 确认 CJK 字体存在。按平台优先级选择：macOS → PingFang SC / Heiti SC；Linux → Noto Sans CJK SC；Windows → SimHei / Microsoft YaHei。如果模板中的字体不可用，**在编译前替换为本机可用字体**，不要等编译后才发现。
2. **编译**：`xelatex -interaction=nonstopmode`
3. **编译日志检查**（关键）：编译后必须 `grep "Missing character" *.log`。xelatex 对缺失字体的处理是 warning 而非 error——PDF 仍会生成但中文全部丢失，这是**静默失败**，不检查 log 会误以为编译成功。
4. **转预览图**：`pdftoppm -png -r 300` 转 PNG。
5. **编译后重叠检测**（关键）：在 PDF 生成后、评分前运行：
```bash
python3 references/pdf-overlap-checker.py <file.pdf>
```
检测器基于 PDF 内部精确文字坐标（pdfplumber），自动发现文字-文字重叠、文字溢出容器、间距过小。
- **ERROR** → 必须修复后才能进入评分
- **WARN** → 在 PNG 中目视确认，确实有问题则修复
- **PASS** → 进入评分
这是比肉眼审查**更可靠**的重叠检测——模型自己审查自己容易遗漏，但 PDF 坐标不会骗人。
draw.io 验证流程：
1. **XML 合法性**：`xmllint --noout file.drawio`
2. **导出预览图**：`drawio -x -f pdf -o output.pdf input.drawio && pdftoppm -png -r 300 output.pdf output-preview`（draw.io CLI 的 PNG 直出在部分环境有兼容问题，PDF 转 PNG 更稳定）
3. 如果 `drawio` 命令不可用，提示用户 `brew install --cask drawio` 安装
4. 检查预览图中的文字可读性、布局合理性

**步骤⑤**：**必须查看渲染出的 PNG 图片后再评分**——禁止仅凭代码逻辑打分。

执行顺序（不可调换）：
1. 加载 `references/review-checklist.md`
2. **对抗性自审**：假设"一定有问题"，强制找出至少 3 个可改进之处并修复（见上方"强制对抗性自审"）
3. 修复后重新编译渲染，再按审查清单逐项检查
4. 视觉审查清单（12 项）+ 设计师视角审查（三遍法）+ 具体检查方向（44 项）+ 六维度评分
5. 总分 30/30 且全部审查项通过 → 执行**交付前宣誓**（review-checklist.md 底部）→ 全部确认后交付
6. 未通过 → 进入步骤⑥迭代修复（压力升级）

**步骤⑥**：迭代修复（未满分则回到④，直到 30/30）。**压力升级机制**——迭代次数越多，审查越严：

| 迭代轮次 | 审查强度 | 要求 |
|---------|---------|------|
| 第 1 轮 | 常规审查 | 按 review-checklist.md 逐项执行 |
| 第 2 轮 | 加严审查 | 除常规外，放大 200% 逐元素检查间距和对齐 |
| 第 3 轮 | 怀疑一切 | 假设你之前的修复引入了新问题，**全图从头审查**，不只看修改区域 |
| 第 4 轮+ | **回到步骤①重新设计** | 如果 3 轮修不好，说明布局方案本身有问题，打补丁无法拯救，必须推翻重来 |

**绝不允许"凑合交付"**：不要因为迭代了 3 轮就降低标准——"改了这么多次差不多了吧"是最危险的想法。标准不会因为你努力了就降低。

**步骤⑦**：画图完成后：
- 如果遇到了需要 2 次以上尝试才解决的问题，追加到 `references/experience-log.md`
- 如果发现了比当前基线更优的参数值，更新 `references/evolution.md`（只升不降）
- 如果某个基线参数在本次画图中被证明不适用，在 evolution.md 中标注适用范围，而不是删除

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
        inner sep=10pt,                          % 防御：文字不贴框边（原6pt）
        drop shadow={opacity=0.15}, thick},
    blue_node/.style={base_box, fill=drawBlueFill, draw=drawBlueLine},
    green_node/.style={base_box, fill=drawGreenFill, draw=drawGreenLine},
    orange_node/.style={base_box, fill=drawOrangeFill, draw=drawOrangeLine},
    purple_node/.style={base_box, fill=drawPurpleFill, draw=drawPurpleLine},
    red_node/.style={base_box, fill=drawRedFill, draw=drawRedLine, font=\footnotesize\bfseries},
    grey_node/.style={base_box, fill=drawGreyFill, draw=drawGreyLine},
    arrow/.style={-{Stealth[scale=1.2]}, thick, color=black!70,
        shorten >=2pt, shorten <=1pt},           % 防御：箭头不刺入框内
    tag/.style={font=\scriptsize, fill=white, inner sep=2pt, rounded corners=1pt},
    annot/.style={font=\footnotesize, inner sep=2pt},
    zone/.style={dashed, thick, inner sep=15pt, rounded corners=8pt},
]
% ===== 节点、连线、分区 =====

% 防御性写法（必须遵守）：
%
% 1. 箭头连接优先用 -| 或 |- （自动 L 形），不手动算中间点：
%    ✅ \draw[arrow] (A.east) -| (B.north);     % TikZ 自动算拐点
%    ✅ \draw[arrow] (A.south) |- (B.west);     % 先下再右
%    ❌ \draw[arrow] (A.east) -- (3.5,-8) -- (B.west);  % 手动拐点容易撞框边
%    只有当 -|/|- 的自动拐点位置不理想时，才用手动坐标（且拐点离目标框 ≥1.5cm）
%
% 2. 树状分叉必须用连续路径画主干+横杆，避免断连：
%    % 第一步：主干+横杆一笔画完（无 arrow、无 shorten）
%    \draw[thick, color=black!70]
%        (A.south) -- ++(0,-1.5)           % 主干向下
%        -| ++(3,0) coordinate(right_end)  % 横杆向右
%        (A.south) ++(0,-1.5) -| ++(-3,0) coordinate(left_end);  % 横杆向左
%    % 第二步：各分支独立画（带 arrow + shorten）
%    \draw[arrow] (left_end) -- (B.north);
%    \draw[arrow] (A.south |- left_end) -- (C.north);  % 中间分支
%    \draw[arrow] (right_end) -- (D.north);
%    ❌ 不要用多个独立 \draw 画主干+横杆——shorten 会让交叉点出现间隙
%    ❌ 不要在分叉点用 circle/rectangle 小节点——会出现"空心方块"
%
% 3. zone 标题用 label= 避免标题和内容重叠：
%    \node[zone, label={[font=\small\bfseries, yshift=3pt]above:标题}] ...
%
% 4. 装饰性 fill（网格、热力图色块、背景色）放 background 层，文字放 main 层：
%    \begin{pgfonlayer}{background}
%      \fill[blue!20] (0,0) rectangle (2,2);  % 色块在底层
%    \end{pgfonlayer}
%    \node at (1,1) {标签};                    % 文字在上层，不被遮挡
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
| 步骤⑤评估打分 | `references/review-checklist.md` | 视觉审查清单、设计师审查、44项检查、评分标准、失败模式路由 |
| 任何图表完成后 | `references/experience-log.md` | 读取已有经验 + 追加新发现 |
| 步骤②同时加载 | `references/evolution.md` | 已验证最佳实践参数（间距、箭头、文字、配色基线值） |

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
