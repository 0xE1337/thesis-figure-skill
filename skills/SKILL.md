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

## 领域自适应

收到用户的文案或图片后，**首先识别论文所属领域**，以该领域专家身份设计配图。使用该领域的通用术语，根据常见图表风格选择布局。

---

## 输出格式选择

| 场景 | 格式 | 理由 |
|------|------|------|
| 嵌入 LaTeX 论文、含数学公式、结构化图表 | **TikZ** | 编译可控，公式精确 |
| 技术路线图、科研展示图、装饰性强（渐变/阴影/3D） | **draw.io** | 视觉效果好，可拖拽编辑 |
| 用户明确指定 | 遵循用户要求 | — |

默认 TikZ。效果不满意再切换 draw.io。

---

## 统一工作流程

无论用户提供的是**文案、图片、还是论文PDF**，都走同一个流程：

```
用户输入（文案/图片/论文/需求描述）
       ↓
  ① 分析 + 画图指令（识别领域、提取模块、规划布局、选择格式）
       ↓
  ② 生成代码（TikZ .tex 或 draw.io .xml + .html）
       ↓
  ③ 编译/预览验证
       ↓
  ④ 评估打分（必须满分才交付）
       ↓
  ⑤ 迭代修复（未满分则回到③，直到 30/30）
       ↓
  交付
```

**步骤①详解**：

- **输入是文案**：阅读文案，提取所有模块/概念/数据流关系，输出画图指令
- **输入是图片**：分析图片中的模块形状/位置/颜色/文字/箭头，输出画图指令
- **输入是论文PDF**：阅读相关章节，理解系统架构，输出画图指令

三种输入最终都汇聚到同一份**画图指令**，格式统一：领域识别 → 布局策略 → 模块列表（名称+颜色+形状）→ 连线逻辑 → 视觉强调点。

**格式自动选择**在步骤①中完成：根据内容特征判断用 TikZ 还是 draw.io。用户也可以直接指定。

**draw.io 特殊规则**：由于无 CLI 渲染，必须同时生成 `.drawio` 文件和 **HTML 预览文件**供聊天中查看。

---

## TikZ 全局约束

### 语言
- 简体中文，标签简洁准确
- 不用引号，不在标签中括号补英文（除非用户要求）
- **禁止 rotate=90 中文**——xelatex 会渲染为不可读色块，所有标注水平放置

### 布局
- **字号与画布比例**：图的纵向总长度超过 12cm 时，全局默认字号必须用 `\small`（不能用 `\footnotesize`）；标注字号用 `\footnotesize`（不能用 `\scriptsize`）。纵向 ≤ 12cm 的紧凑图可以用 `\footnotesize` + `\scriptsize`。**渲染成 PNG 后检查：最小文字在 200dpi 下是否可读**
- **空白区域填充**：生成后检查是否存在大面积空白（宽度 > 3cm 且高度 > 2cm 的无内容区域）。如果存在，用注释框（note）、公式框（formula_box）、或图例（legend）填充。注释框优先放在两个主要元素之间的空白区域，而非图的最外侧
- **绝对坐标 vs 相对定位**：当需要精确控制多列等间距时（如时序图的参与方、对比图的左右栏），优先用绝对坐标 `at (x,y)` 而非 `right=Xcm of`——相对定位在多层嵌套时间距会累积偏差
- 优先垂直分层布局，控制横向宽度
- 模块间留合理间距，箭头避免交叉
- **多实例并列**用横排三列（不要纵向堆叠），列间距 2.5–3cm
- **层标题**：用独立 `\node` + `anchor` 放置（不用 `fit` 的 `label`），与相邻层框边界间距 ≥ 0.5cm；节点密集时放框内角落
- 左右对比图中间通道 ≥ 3cm
- **标注防重叠**：同一区域内，tag 标注和 annot 标注之间至少 0.3cm；密集区域的标注优先放在节点上方或下方（而非侧面），避免与箭头路径上的其他标注冲突；如果标注过多导致无法避免重叠，删减次要标注或缩短文字
- **模块位置决定连线美观度**：如果发现某条连线需要绕很远（跨3个以上分区框），优先考虑**移动源/目标模块的位置**使其更近，而非强行画长距离绕行线。例如：IKS 模块如果要连到 M_t，应把 IKS 放在 M_t 附近（如 CPR 下方），而非放在最底层强行绕行
- **多层 zone 背景框必须左右对齐**：当图有多个分层 zone（如端-边-云-链四层架构），各 zone 因 `fit` 包裹不同节点导致宽度不同，必须用**隐形锚点**统一左右边界。做法：在所有节点之后、zone 之前，创建两个 `inner sep=0pt, minimum size=0pt` 的隐形节点 `anchor_L` 和 `anchor_R`，x 坐标分别取所有节点最左-1cm 和最右+1cm。每个 zone 的 `fit` 列表中加入 `(anchor_L |- 某层底部节点.south)(anchor_R |- 某层顶部节点.north)`，这样所有 zone 共享同一左右边界
- **层标题胶囊用绝对 x 坐标对齐**：多层分区图的左侧层标题不要用 `$(zone.west)+(-2,0)$`——各 zone 宽度不同会导致标题 x 坐标不一致。改为所有层标题共用同一个绝对 x 坐标（如 `at (-4.5, y)`），y 取该层的垂直中心
- **连线绝不穿越节点框**（反复踩坑）：画跨层连线时，必须检查路径上是否经过其他节点的矩形区域。特别是从底层上行到高层时，竖直线段容易穿过中间层的节点。解决方法：计算路径上所有 y 值对应的 x 范围内有哪些节点，如果有冲突则将出发点的 x 坐标移到两个节点之间的空隙中
- **短距离弯折连线走空白侧**：当源节点和目标节点在垂直或对角方向相邻（间距 < 3cm），连线不要从源节点正下方/正上方直接弯折到目标——这样弯折点容易紧贴节点边缘或和其他连线挤在一起。正确做法：从源节点出发后**先水平走到附近的空白区域**（远离其他节点和连线的一侧），再转弯到达目标。用 `|- ` 或 `-|` 保证最后一段完全水平/垂直进入目标锚点，避免微小斜线

### 代码规范
- `standalone` 文档类，`border=25pt`（有外部回路时 35pt）
- 中文支持优先 `ctex`（`\usepackage[fontset=none]{ctex}` + Noto Sans CJK SC），不可用则退回方案 B：`\usepackage{fontspec}` + `\setmainfont{Noto Sans CJK SC}` + `\setsansfont{Noto Sans CJK SC}`（**不要用 `ucharclasses` 方案**——实测中 `\setDefaultTransitions` 在 tikz 节点内的中英混排场景下频繁出现 Missing character 错误）
- 所有节点用 `style` 定义 + `positioning` 相对定位（**几何图例外：允许绝对坐标**）
- 编译：`xelatex -interaction=nonstopmode`
- 箭头旁标注用 `tag` 样式（`fill=white`），独立标注用 `annot` 样式（不带 `fill`）
- **回路必须拆分为 3 段独立 `\draw`**，禁止单条 `\draw` + `rounded corners` 画长距离回路
- 回路终止于分区框边界（如 `target_zone.west`），不穿入框内
- 多条回路分配到不同侧，同侧间距 ≥ 1.5cm
- 跨区箭头在空白区域中转（L 型路径），不直接刺穿虚线框
- **层标题与箭头标注防冲突**：当垂直箭头穿过层间空隙时，箭头 tag 标注和层标题必须放在不同侧——标注在 `right` 则标题用 `anchor=north west`（左下角），反之亦然。生成后必须检查每个层标题附近是否有箭头标注，有则错开
- **同侧多条回路/跳连的 rail 分配**：最外侧 rail 距框边界 ≥ 2.0cm，内侧 rail ≥ 0.8cm，两条 rail 间距 ≥ 1.0cm。每条回路用不同颜色区分。禁止两条回路共用同一 rail x 坐标
- **跨两层以上的连线**（如底层模块→顶层模块，中间隔了一个或多个分区框）：必须用 L 型路径走框外侧，禁止用单条 `-|` 或 `|-` 直接跨越中间分区框。具体做法：从源节点侧面（`.west` 或 `.east`）出发 → 走外侧主干竖直上行 → 从目标节点侧面（`.west` 或 `.east`）进入
- **虚线/辅助线（如损失函数连线、对比学习连线）绝对不穿越分区框**：这是最常见的遗漏。当虚线需要从一个分区内的节点连到分区外的标注时，必须先从节点侧面出框（`.west` / `.east` / `.south`），在分区框边界外侧空白区域中转，再到达目标。绕行路径用 `rounded corners=6pt` 保持美观。宁可路径长一点也不穿框
- **绕行 rail 必须与分区框边界保持 ≥ 1.0cm 间距**：如果 rail 紧贴框边界（如只有 0.5cm），虚线和框的虚线在视觉上会混淆不清。**跨越多个分区的长距离 rail 必须放在画面中所有元素（包括独立节点如 Training Data）的最外侧**，而不仅是某个分区框外侧。计算 rail x 坐标时，取所有相关节点和分区框的最左/最右边界，再外推至少 1.0cm
- **虚线出口和入口方向选择**（反复踩坑的规则）：出口方向必须指向空白区域，不能指向其他节点所在方向。例如：从 VAE 连到右下方的损失标签，应从 VAE `.south` 向下出框底部再水平右行，而非从 `.west` 水平左行（会穿过左侧节点文字）。入口方向优先选择目标节点的**空闲侧**（没有其他连线的一侧），避免进入方向与已有箭头重叠
- **虚线出口必须留足间距**：从节点出来后至少走 **1.0cm 以上的直线段**再转弯，否则转弯点紧贴节点边缘看起来很突兀。入口处同理——到达目标节点附近时，先在旁边转弯对齐，再直线进入，形成清晰的 L 型弯折
- **连线出口/入口选择节点的自然锚点**：向下连接用 `.south`（底部中间），向右用 `.east`，向左用 `.west`。禁止从角落（`.south west` / `.north east`）出发，角落出口看起来不自然。入口同理——从目标节点最近的正面（`.west` / `.north` / `.east`）进入，不从角落进

---

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

---

## TikZ 模板骨架

```latex
\documentclass[tikz,border=25pt]{standalone}
\usepackage{tikz}
% 如在 Overleaf 编译，替换为 \usepackage{ctex}
% 方案B（无ctex时）：\usepackage{fontspec} + \setmainfont{Noto Sans CJK SC} + \setsansfont{Noto Sans CJK SC}
\usepackage[fontset=none]{ctex}
\setCJKmainfont{Noto Sans CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
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

---

## 各步骤说明

### ① 分析输入 + 画图指令

无论输入是文案还是图片，都输出统一格式的画图指令。

**文案输入时的布局决策**（核心环节）

文案驱动时，需要自主决定图的结构。按以下流程思考：

1. **识别信息流方向**：文案描述的是"A经过B变成C"（水平数据流）还是"底层支撑上层"（垂直分层）？
2. **识别关键实体**：提取所有名词性概念，判断它们是"处理模块"（矩形）、"数据/信号"（平行四边形或带标注的箭头）、"判断/约束"（菱形）、还是"存储"（圆柱体）
3. **识别并行 vs 串行**：多个实体是同时发生（并列排放）还是有先后顺序（串联排放）
4. **选择布局模式**（对照常见图表类型表选择）

**节点形状决策表**（文案驱动时最容易出错的环节）：

| 文案中的概念类型 | 推荐节点形状 | TikZ style |
|---------------|-----------|------------|
| 处理步骤/算法模块 | 圆角矩形 | `base_box` |
| 输入/输出数据 | 矩形（蓝色） | `blue_node` |
| 判断/约束/验证 | 菱形 | `diamond_node` |
| 数据库/存储 | 圆柱体 | `database` |
| 求和/聚合运算 | 圆形 + 符号 | `sum_circle` |
| 代码/配置片段 | 等宽字体矩形 | `code_block` |
| 数学公式/理论 | 公式框 | `formula_box` |
| 二选一结果 | 小圆 | `out_circle` |
| 加密/哈希操作 | 菱形（深色） | `diamond_node` |
| 分解/拆分操作 | 梯形 | `trapezium` |

**连线决策规则**：
- 数据流（核心路径）→ 粗橙色实线 `arrow_data`
- 普通控制流 → 黑色实线 `arrow`
- 可选/异步/反馈 → 虚线 `arrow_dash`
- 跨区引用 → 蓝色虚线 `arrow_blue`
- **控制信号（如"选择哪些参数更新"）**：可以画连线但必须同时在被控模块上加文字标注（如"IKS: Top-K"），让读者一看就知道这条线的语义。连线走位规则和数据流一样——走框外侧不穿框。如果控制信号连线过长或路径复杂，宁可只用标注不画线
- **语言一致性**：如果整张图是英文，所有标注、标签、标题必须全英文，禁止混入中文（反之亦然）

输出结构化指令后直接进入步骤②。

**图片输入时**：识别所有模块形状/位置/文字/颜色/箭头，映射到统一色板。

### ② 生成代码 + 自检清单

生成前检查：
- `\documentclass` 第一行，color 定义在 `\begin{document}` 前
- 无未闭合括号、无未定义节点引用、无 `rotate=90` 中文
- 回路用分段绘制，跨区箭头不刺穿虚线框
- 回路主干距节点边缘 ≥ 0.7cm
- 所有标注在 border 范围内不被裁切
- **同一区域内的多个标注（tag + annot）之间无重叠**，密集处用 `anchor` 错开方向
- **标注防重叠优先级**：当空间紧张时，(1) 先尝试换到箭头另一侧（above↔below）；(2) 再尝试增加偏移（pos=0.3 而非 0.5）；(3) 最后缩短标注文字
- **虚线框（校验回路、分区等）不能与内容节点/标签重叠**：画虚线框时必须用 `$(...)+(-offset, -offset)$` 精确控制边界，而非凭感觉估算。生成后在 PNG 预览中逐像素检查虚线框与最近节点的间距
- **monospace 文本不使用 `\texttt` 包裹中文**（会报错），纯英文代码用 `\texttt` 或 `code_block` style

### ③ 编译验证

首次编译前确保 ctex 可用（`kpsewhich ctex.sty`，不可用则 `apt-get install texlive-lang-chinese`，失败则切方案 B）。编译成功后 `pdftoppm -png -r 300` 转预览图。

### ④ 评估打分

查看 PNG，逐项检查：文字重叠、箭头落点、回路完整性、层标题归属、分区框边界、间距均匀、虚线穿越、**层标题与箭头标注是否同侧冲突**、**同侧多条回路是否交叉**。

六维度评分（各 1-5 分）：完整性、准确性、布局合理、连线清晰、配色统一、文字可读。
- **总分 = 30 且无缺陷** → 交付给用户
- **总分 < 30** → 必须继续迭代修复，不展示给用户
- **总分 < 25** → 重大问题，回到步骤①重新设计布局

### ⑤ 迭代修改

精确定位问题，最小化改动，每次说明改了什么，回到③重新编译。

---

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
| 多实例汇聚图 | 横排三列→汇聚 | 联邦学习、分布式系统 |

---

## 分层系统架构图专项规则

分层系统架构图用于展示端-边-云-链、硬件-中间件-应用等多层系统结构，是论文中最常见的图表类型之一。

### 适用场景

用户提及"系统架构""分层架构""端边云""四层架构""N层堆叠"，或文案描述的是自下而上的多层系统结构。

### 布局核心原则

**每层内部结构**：不要只放3个平铺节点——每层应有主模块（`base_box`）+ 子组件（`small_box`），主模块在上，子组件在下方排列。例如"联邦学习协调器"（主）下挂"参数服务器""GPU Worker Pool"（子）。这样才能体现层内的复杂性。

**层间距**：相邻 zone 之间留 1.5–2.0cm 间隙，用于放置协议标签（MQTT/gRPC/RESTful）和跨层连线的弯折中转。

**zone 对齐**（关键教训）：所有 zone 必须左右对齐，用隐形锚点方案：
```latex
\node[inner sep=0pt, minimum size=0pt] (anchor_L) at (-2.5, 0) {};
\node[inner sep=0pt, minimum size=0pt] (anchor_R) at (16.5, 0) {};
% 每个zone的fit中加入：
fit=(anchor_L |- 底部节点.south)(anchor_R |- 顶部节点.north)(其他节点...)
```

**层标题胶囊**：用绝对 x 坐标（如 `at (-4.5, y)`），y 取该层中心。不要用 `$(zone.west)+(-2,0)$`。

### 跨层连线规则（反复踩坑总结）

1. **上行数据流线不穿越中间层节点**：从底层 SDK 出来的竖直线，必须检查路径上方每一层是否有节点。出发点的 x 坐标应选在两个节点列之间的空隙。例如三列节点在 x=0, 6, 12 时，上行线应走 x=3 或 x=9 的空隙
2. **多条上行线间距 ≥ 3cm**：从同一横跨节点（如 SDK）出发的多条上行线，出发 x 坐标间距至少 3cm，避免视觉上平行重叠
3. **协议标签放在层间空隙的右侧空白处**：不要放在上行线路径上，会被连线遮挡
4. **双向通路（如模型下发/梯度回传）走独立 rail**：在所有内容区域的最左侧或最右侧，距 zone 边界 ≥ 1.5cm
5. **反向连线（如 Oracle 预言机、事件回调）走 zone 外侧**：从源节点侧面出框，沿 zone 外边界走 rail，不穿越任何 zone。优先走左侧 rail 给 Oracle 预言机，右侧 rail 给事件回调，左右分开避免交叉
6. **短距离弯折走空白侧**：源和目标斜向相邻时，先水平走到空白区域再 `|-` 弯折进入目标，不要直接从 `.south` 弯折——会紧贴其他节点

### 数据库节点

用 `cylinder` 形状（`shape border rotate=90, aspect=0.25`）区分存储类组件（HDFS/Redis/缓存），比矩形节点更有辨识度。注意 cylinder 的 `.west`/`.east` 锚点在圆弧上，连线入口方向用 `.north`/`.south` 更自然。

### 自检清单（分层架构图专用）

- [ ] 所有 zone 左右边界对齐（用隐形锚点）
- [ ] 层标题胶囊 x 坐标统一
- [ ] 上行数据流线不穿越任何节点框
- [ ] 多条上行线间距 ≥ 3cm
- [ ] 反向连线走 zone 外侧 rail，不穿越 zone
- [ ] 每条连线的弯折处在空白区域，不紧贴节点边缘
- [ ] 最后进入目标节点的一段是纯水平或纯垂直（用 `|-` 或 `-|` 保证）
- [ ] 协议标签不被连线遮挡
- [ ] cylinder 节点的连线入口方向自然

---

## 数据映射/转换三栏图专项规则

数据映射/转换图用于展示数据从源系统经中间适配层到目标系统的完整转换流程，常见于跨链协议、API网关、数据集成等场景。

### 适用场景

用户提及"三栏""映射""转换""适配""源→中→目标""跨链""格式转换"，或文案描述的是左-中-右三阶段的数据处理流程。

### 布局核心原则

**三栏绝对坐标**：左栏 x=0，中栏 x=7，右栏 x=14。三栏间距 7cm，足够放跨栏连线和标签。

**左右栏节点y坐标对齐**：左栏和右栏的节点必须在相同的y坐标上（如 -1.8, -3.6, -5.4, -7.2），形成水平对应关系。

**中栏节点间距 ≥ 1.5cm**（关键教训）：中栏通常比左右栏多1-2个节点。如果间距太小（< 1.2cm），节点下方的标注文字会和下一个节点重叠。中栏5个节点推荐间距1.6cm。

**标注放置规则**：
- 左右栏标注放节点正下方（`at (x, y-0.7)`），间距0.7cm足够
- 中栏标注也放节点正下方，间距0.65cm。**不要放节点右侧**——会和跨栏传输线的标签冲突
- 标注和zone底边距离 ≥ 0.5cm。用隐形锚点 `aBot` 控制zone底边位置

**辅助组件（消息队列/状态机）放在中栏两侧空隙**：
- 左侧辅助（如消息队列）放 x≈3.8（左栏和中栏之间）
- 右侧辅助（如状态机）放 x≈10.2（中栏和右栏之间）
- **不要两个辅助组件放同侧**——会互相挤压并和跨栏连线冲突

### 跨栏连线规则

1. **顶部水平直连**：源栏第一个节点 → 中栏第一个节点 → 目标栏第一个节点，用 `arrow_data` 水平连接，标签放 `pos=0.5, above=2pt`
2. **底部数据传递**：源栏最后一个节点 → 中栏最后一个节点，水平直连
3. **中间层到目标栏的L型连线**：中栏处理完后输出到目标栏的非第一个节点时，用 `-- ++(offset,0) |- target.west` 走L型路径
4. **跨栏标签不和节点标注重叠**：跨栏线的tag放在连线中点上方或空白区域，不要放在任何节点的标注文字附近

### 回调与回滚

- **回调线**走底部通道（zone下方），从目标栏最后一个节点.south → 水平左行 → 源栏某节点.south
- **回滚线**走最底部（回调线下方1-2cm），用红色虚线。左侧回滚和右侧回滚的y坐标错开
- 回调线和回滚线之间间距 ≥ 1.0cm

### 图例

三栏图因为用了4种连线类型（正常流/跨栏传输/回调/回滚），**必须**在底部添加图例框说明。图例用 `rectangle, rounded corners=4pt, draw=drawGreyLine!50, fill=drawGreyFill`。

### 三栏zone等高

用隐形锚点 `aTop` 和 `aBot` 统一三栏zone的顶部和底部y坐标：
```latex
\node[inner sep=0pt, minimum size=0pt] (aTop) at (0, 0.8) {};
\node[inner sep=0pt, minimum size=0pt] (aBot) at (0, -9.0) {};
% 每个zone的fit中加入 (aTop -| ...) 和 (aBot -| ...)
```

### 自检清单（三栏图专用）

- [ ] 左右栏节点y坐标水平对齐
- [ ] 中栏节点间距 ≥ 1.5cm，标注不和下方节点重叠
- [ ] 辅助组件（消息队列/状态机）分布在中栏两侧，不在同侧
- [ ] 跨栏标签不和节点标注重叠
- [ ] 三栏zone等高（用隐形锚点）
- [ ] 回调线和回滚线y坐标错开 ≥ 1.0cm
- [ ] 底部图例包含所有线型说明
- [ ] 标注和zone底边距离 ≥ 0.5cm

---

## 时序交互图专项规则

时序交互图（Sequence Diagram）用于展示多方协议交互流程，在区块链、密码学、分布式系统论文中极为常见。

### 适用场景

用户提及"时序图""交互流程""多方协议""消息传递""生命线"，或文案描述的是 A→B→C→D 的多方消息交换过程。

### 布局核心原则

**字号必须足够大**——时序图通常纵向很长（15cm+），如果用 `\footnotesize` 作全局默认，渲染成 PNG 后文字会非常小。规则：
- 参与方标题：`\small\bfseries`
- 消息标注（箭头上方的 tag）：`\footnotesize`
- 自调用弧旁标注：`\footnotesize`
- 注释框内容：`\footnotesize`
- 阶段标签：`\small\bfseries`
- **禁止**在时序图中使用 `\scriptsize` 或 `\tiny` 作为主要标注字号

**参与方水平间距**：用绝对坐标（`at (0,0)`, `at (5.5,0)`, `at (11,0)`, ...），间距 5–6cm。不要用 `right=3.8cm of` 等相对定位——容易导致间距过大而内容区域空旷。4 个参与方总宽度控制在 16–17cm。

**垂直间距紧凑**：
- 同一阶段内的消息/自调用弧间距 0.5–0.6cm
- 阶段之间间距 0.8–1.0cm（不超过 1.2cm）
- 整图纵向总长度控制在 17–20cm（6 个阶段以内）

**填充中间空白**——时序图最常见的问题是"阶段二三只有用户自调用，中间几列完全空着"。解决方法：
- 自调用弧加宽到 2.0cm（而非默认的 1.2cm），标注文字放在弧的右侧
- **注释框（note）放在两条生命线之间的空白区域**（如 edge 和 chain 之间），而非放在最右侧被裁切
- 注释框 `text width` 设为 3.8–4.2cm，能填满两列之间的空间

### 必备视觉元素

| 元素 | style | 说明 |
|------|-------|------|
| 参与方标题框 | `participant` | 圆角矩形，各方用不同颜色，含角色名和数学符号 |
| 生命线 | `lifeline` | 竖直虚线，颜色与参与方一致（`color=#1!60`） |
| 激活条 | `activation` | 窄矩形（宽 0.3cm），表示该方正在处理，`fill=#1!25, draw=#1!70` |
| 消息箭头 | `msg` | 实线带箭头，颜色与发送方一致；虚线表示异步/可选 |
| 自调用弧 | `selfcall` | 从激活条右侧伸出的 U 型弧，表示内部处理步骤 |
| 阶段标签 | `phase` | 左侧红色圆角框，标注"阶段N：XXX" |
| 注释框 | `note` | 黄色圆角框，放在生命线之间的空白区域，补充说明 |
| 阶段背景色 | `\fill[...Fill!15]` | 每个阶段一个浅色背景横条，增加层次感 |

### 回路/重试线规则

时序图中的回路线（如"验证失败→重新生成"）：
- **rail 竖直线必须在所有阶段标签的外侧**，距离用户生命线 2.5cm 以上
- rail 与阶段标签之间间距 ≥ 0.5cm，避免视觉混淆
- "重试"等标签用水平放置的 `tag`（不用 `rotate=90`，竖排在时序图中可读性差）
- 回路线用 `dashed, rounded corners=6pt`，颜色用 `drawRedLine!50`（半透明避免喧宾夺主）
- `border` 设为 25pt 以上，确保回路线不被裁切

### 异常分支

在正常流程之后添加"异常"阶段（灰色阶段标签），用红色虚线箭头表示失败路径。异常分支的消息方向通常是反向的（Chain→Edge→User）。

### style 定义模板

```latex
participant/.style={rectangle, rounded corners=4pt, align=center,
    minimum height=1.1cm, minimum width=2.8cm,
    drop shadow={opacity=0.15}, thick, font=\small\bfseries},
msg/.style={-{Stealth[scale=1.0]}, thick, color=#1},
tag/.style={font=\footnotesize, fill=white, inner sep=2pt, rounded corners=1pt},
phase/.style={font=\small\bfseries, text=drawRedLine, fill=drawRedFill,
    inner sep=5pt, rounded corners=3pt, draw=drawRedLine, thick},
lifeline/.style={dashed, thick, color=#1!60},
activation/.style={fill=#1!25, draw=#1!70, thick, rounded corners=1pt},
selfcall/.style={-{Stealth[scale=0.9]}, thick, rounded corners=3pt, color=#1},
note/.style={rectangle, rounded corners=3pt, draw=drawGreyLine!60, fill=drawYellowFill,
    align=left, font=\footnotesize, inner sep=6pt, text width=3.8cm},
```

### 自检清单（时序图专用）

- [ ] 全局字号 ≥ `\small`，标注字号 ≥ `\footnotesize`
- [ ] 参与方间距 5–6cm，总宽度 ≤ 17cm
- [ ] 每个阶段内垂直间距 ≤ 0.6cm，阶段间 ≤ 1.0cm
- [ ] 无大面积空白区域（注释框已填充到生命线之间）
- [ ] 自调用弧宽度 ≥ 2.0cm
- [ ] 回路线 rail 在阶段标签外侧，标签水平放置
- [ ] border ≥ 25pt，回路线不被裁切
- [ ] 阶段背景色覆盖完整，无间隙无重叠

---

## 几何/数学示意图专项规则

几何/数学示意图用于展示算法原理、密码学构造、数学关系的可视化，常见于理论性较强的论文章节。

### 适用场景

用户提及"原理图""示意图""坐标系""数学可视化"，或文案描述的是几何关系（椭圆曲线、向量空间、树结构）与公式的结合。

### 布局核心原则

**多区域组合图**（如椭圆曲线+Merkle树+公式）的布局：
- 用绝对坐标划分区域：左半部分 x∈[0,7]、右半部分 x∈[8,18]、底部公式跨全宽
- 两个区域之间留 0.5–1cm 间隙，用不同背景色区分（`\fill[...Fill!8]`）
- 区域标题用带底色的圆角框放在区域上方，不用无框的裸文字

**坐标系绘制**：
- 轴线 `thick, -{Stealth}`，网格 `drawGreyLine!12, thin`
- 网格画在 `background` 层，避免遮盖节点
- 曲线用 `smooth, samples=80` 保证平滑，`domain` 必须精确控制避免曲线穿入其他区域

**树结构绘制**：
- 普通连线用 `black!35, semithick`（浅灰细线），高亮路径用 `very thick` 彩色箭头
- **高亮路径必须走不同锚点**（关键教训）：当高亮路径和普通连线连接同一对节点时，两条线必须走不同的锚点。例如 h2→h23 普通线走 `h23.south west`，红色高亮走 `h23.south`；h23→root 普通线走 `root.south east`，红色高亮走 `root.south`。否则两条线完全重叠，粗线盖住细线，视觉混乱
- **左右子树连线必须对称**：左子节点走父节点 `.south west`，右子节点走 `.south east`，两侧结构保持镜像对称
- 兄弟节点标注用**侧向小标签框**（`anchor=west/east`，带底色），不用箭头指向节点——箭头容易和树的连线视觉冲突
- 验证路径等关键信息用独立的标注框放在树的侧面空白处（不放在其他区域内部）
- **虚线框内的标签不能碰边界**：框内的点和文字标签必须距框边界 ≥ 0.3cm，标签用 `anchor=west`（侧向）而非 `anchor=north`（下方），避免文字和虚线重叠。框的 `minimum height` 要留足内容空间

### 跨区域连接线规则（重要教训）

当多个区域需要连接到底部共享区域（如公式框）时：
- **禁止**用长距离斜向虚线直连——视觉混乱
- **正确做法**：从上方区域的底部元素出发，先向下走短直线（0.3–0.5cm），再用 `-|` 或 `|-` 加 `rounded corners=10pt` 弯折到目标框的 `.north west` / `.north east`
- 连接线用半透明颜色（`drawBlueLine!60`），不能比主体内容还抢眼
- 标注（如"配对运算""公共输入"）放在弯折起点旁，不放在连线中段

### 公式框规则

- 公式用 `formula_box` style，`inner sep=8pt`，大公式用 `\normalsize`
- 公式分解标注（"证明元素""可信设置"等）放在公式框下方，每个标注用对应颜色，用短虚线箭头指向公式框底边
- 标注之间等间距分布，不重叠

### 自检清单（几何图专用）

- [ ] 曲线 domain 不穿入其他区域框
- [ ] 所有标注和标签在 border 范围内（border ≥ 30pt）
- [ ] 跨区域连接线用 L 型弯折 + rounded corners，无斜向长虚线
- [ ] 高亮路径与普通连线有明显视觉层次差异（粗细+颜色）
- [ ] 兄弟节点等辅助标注不与主体连线冲突
- [ ] 公式框居中且宽度适配内容

---

## 数据流水线图专项规则

数据流水线图（Pipeline Diagram）用于展示数据从输入到输出的完整处理流程，常见于系统设计、编译器、信号处理、密码学算术化等章节。

### 适用场景

用户提及"流水线""pipeline""数据流""处理流程"，或文案描述的是 A→B→C→D 的多步骤串联处理过程，每步可能有并行分支和汇聚。

### 布局核心原则（关键教训）

**超过 6 个节点必须折行**：pipeline 图最大的坑是一字排开导致图太宽太扁。规则：
- 每行最多 5-6 个主要节点
- 超过 6 个则折成多行（2-3 行），每行对应一个逻辑阶段
- 折行用 `rounded corners=8pt` 的粗连线自然弯折到下一行
- 折行处选在阶段分界点（如"预处理→ZKP"之间），不在阶段内部折

**跨行连线必须走短路径**（反复踩坑的规则）：
- 上行的输出节点和下行的输入节点应该**纵向对齐或临近**，然后直接向下连
- **禁止**从上行右端绕远路连到下行左端——这会产生超长的 U 型连线穿越多个分区
- 如果需要跨行引用（如公共输入从第二行连到第三行），走**分区框外侧 rail**，不穿越中间分区
- 公共输入等跨层引用的虚线走 `.south` → 向下 → `-|` 弯折到目标的 `.west`，标注放在目标旁边

**折行方向**：
- 推荐"蛇形"布局：第一行左→右，折返后第二行仍然左→右（节点放在对应的 x 坐标下方）
- 不推荐"之字形"（第二行右→左），因为阅读方向不一致

### 节点形状选择

pipeline 图的核心特征是**每步用不同形状节点**区分数据类型：

| 概念类型 | 推荐形状 | TikZ style |
|---------|---------|------------|
| 处理步骤/算法 | 圆角矩形 | `proc` (各色) |
| 数据/信号 | 梯形 | `data` (trapezium) |
| 判断/过滤 | 菱形 | `decide` (diamond) |
| 存储/记录 | 圆柱 | `store` (cylinder) |
| 求和/聚合 | 圆形 | `sum_circle` |
| 代码片段 | 等宽字体矩形 | `code_block` |

### 连线类型区分

用颜色+线型区分不同类型的连线（在图例中说明）：
- **核心数据流**：橙色粗实线 `arrow_data`（`very thick, drawOrangeLine`）
- **控制流**：黑色细实线 `arrow`
- **成功路径**：绿色实线 `arrow_green`
- **失败/反馈**：红色虚线 `arrow_red`（`dashed`）

### 图例

pipeline 图因为用了多种形状和连线，**必须**在底部居中添加图例框说明各线型含义。图例用 `rectangle, rounded corners=4pt, draw=drawGreyLine, fill=drawGreyFill`，`font=\scriptsize`，水平排列各图例项。

### 分区背景

每个阶段用 `zone` style 虚线框 + 浅色背景包裹，阶段标题用 `stage` style 放在分区上方。分区框通过 `fit=(node1)(node2)...` 自动包裹内部节点。

### 自检清单（pipeline 图专用）

- [ ] 每行不超过 6 个主要节点
- [ ] 折行处在阶段分界点，用圆角粗连线弯折
- [ ] 跨行连线走短路径（纵向对齐+直接向下），不绕远路
- [ ] 跨层引用（公共输入等）走分区框外侧，不穿越中间分区
- [ ] 每种数据类型用不同节点形状
- [ ] 连线类型用颜色+线型区分，底部有图例
- [ ] 图例底部居中
- [ ] 所有分区有虚线框背景 + 阶段标题

---

## draw.io 科研展示图

### 何时使用

用户提及"技术路线图""研究框架""科研展示"，或参考图有3D透视/同心嵌套/倒金字塔/散布关键词等视觉效果。

### HTML 预览技术选型（关键教训）

**纯 CSS Flexbox/Grid 适合**：三层横向分区（模式A）、流水线链条（模式C）、三栏展开（模式E）——这些都是**规则矩形布局**。

**必须用 SVG 的场景**：3D 透视梯形/菱形嵌套（模式B）、散布关键词自由定位、放射线装饰、弧形连接线。**禁止用 CSS clip-path + preserveAspectRatio="none" 模拟梯形**——高度不可控会导致布局崩溃。

**SVG 实现规则**：
- 整张图用单个 `<svg viewBox="0 0 W H">` 包裹，所有元素（梯形、文字、标签、侧栏）都在 SVG 内用绝对坐标
- **不混用 SVG 和 CSS 布局**——要么全 SVG（模式B/D），要么全 CSS（模式A/C/E）
- 3D 透视梯形用 `<polygon>` 画4个面（前面板+顶面+左侧面+右侧面），不同透明度 fill 模拟光影
- 文字用 `<text>` + `text-anchor="middle"` 精确定位
- 竖排文字用 `writing-mode="tb"`

### 配色方案

**科研展示图默认用粉灰配色**（和小枫老师参考图一致）：
- 背景：白色或 #faf8f6（微暖灰），嵌套层 rgba 粉/灰/紫递进
- 强调文字/空心字描边：#C2185B（品红）、#E91E63（粉红）
- 深色横幅：`linear-gradient(135deg, #7B1FA2, #9C27B0)`（深紫渐变白字）
- 标题胶囊（深底白字）：`linear-gradient(135deg, #5C6BC0, #7986CB)`（蓝紫）
- 横幅：#E8EAF6/#7986CB（蓝灰）、#E0D8F0/#A090C0（紫灰）
- 棕色系（电磁/硬件模块）：#EFEBE9/#8D6E63/#BCAAA4
- 粉色强调标签：#FCE4EC/#F48FB1/#C2185B
- 编号圆：`linear-gradient(135deg, #FFD54F, #FFB300)` + border #E65100
- 普通文字：#333（深）、#555（中深）、#666（中）、#999（浅）、#bbb/#ccc（极浅散布词）
- 标签背景：#FCE4EC（粉）、#F8E0EC（浅粉）
- 流水线圆：`linear-gradient(145deg, #F0E8F5, #E8DDF0)` + border #8E6CA8
- 箭头流渐变：#F3E5F5 → #E8EAF6 → #F8BBD0 → #CE93D8

如用户要求用 TikZ 统一色板，则按 drawBlueFill/Line 等映射。

### 5 种布局模式

**模式 A：三层横向分区**（纯CSS）
- Flexbox 三栏布局，编号圆分隔

**模式 B：3D 透视倒金字塔**（纯SVG）★最复杂
- 多层梯形嵌套，从外到内收窄
- 每层梯形4面：`<polygon>` 前面板 + 顶面 + 左右侧面
- 梯形坐标计算：外层上边 `(x1,y1)-(x2,y1)` 宽，下边 `(x1+offset, y2)-(x2-offset, y2)` 窄
- 散布关键词用 `<text>` 自由定位在梯形内部/周围
- 左右侧栏在 SVG 内用 `writing-mode="tb"` 竖排

**模式 C：流水线链条**（纯CSS）
- Flexbox 圆形节点 + 加号水平排列

**模式 D：左右侧栏 + 中心嵌套**（纯SVG，配合模式B使用）
- 侧栏在 SVG 左右两侧，竖排文字+强调标签
- 弧形装饰线从中心发散到两侧：`<path d="M ... Q ..." />`

**模式 E：总论-展开-归纳**（纯CSS）
- 顶部强调框 → 三栏 → 底部箭头流程
- 左侧编号圆（一/二/三）+ 空心描边竖排分区标题
- 每层用 Flexbox 分左侧栏（side）+ 右侧内容（body）

### 视觉花样库（从真实参考图总结）

**空心描边大字**（SVG实现）——科研展示图的常见装饰手法，用于分区标题或栏目标题：
```html
<svg width="44" height="155" viewBox="0 0 44 155">
  <text x="22" y="32" text-anchor="middle" font-size="28" font-weight="900"
    fill="none" stroke="#C2185B" stroke-width="0.7"
    font-family="Microsoft YaHei,PingFang SC,sans-serif">标</text>
  <text x="22" y="68" ...>题</text>
</svg>
```
- **关键参数**：`fill="none"` + `stroke` + `stroke-width`
- **stroke-width 必须控制在 0.6-0.8**，过粗（≥1.2）会导致笔画间隙被填满，字变模糊不清
- 字号 26-30 适合分区标题，字号 22-26 适合栏目标题
- 字间距（dy）约为字号的 1.2-1.3 倍
- 空心字只用于装饰性标题，正文内容不用

**金黄渐变编号圆**：
```css
.num-circle {
  background: linear-gradient(135deg, #FFD54F, #FFB300);
  border: 3px solid #E65100;
  box-shadow: 0 2px 6px rgba(230,81,0,0.25);
}
```

**左侧粉红竖条装饰**（CSS伪元素）：
```css
.side::before {
  content: '';
  position: absolute;
  left: 6px; top: 0; bottom: 0;
  width: 5px;
  background: linear-gradient(to bottom, #E91E63, #F48FB1);
  border-radius: 3px;
}
```

**深色渐变横幅**（白字，强阴影）——用于一级标题/核心发现：
```css
.banner {
  background: linear-gradient(135deg, #7B1FA2 0%, #9C27B0 40%, #8E24AA 100%);
  color: #fff;
  box-shadow: 0 4px 14px rgba(123,31,162,0.3);
}
```

**悬浮标题胶囊**（深色底白字，浮在卡片顶部）：
```css
.col-card { padding: 30px 12px 14px; position: relative; }
.ct {
  position: absolute;
  top: -4px;  /* 不能太高（-16px会遮挡），保持在卡片顶边附近 */
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #5C6BC0, #7986CB);
  color: #fff;
  white-space: nowrap;
}
```

**带左竖条的标题框**（蓝色/棕色两种风格）：
```html
<div class="titled-box">
  <div class="bar bar-blue"></div>  <!-- 5-6px宽竖条 -->
  <div class="tb-inner tb-blue">智能表面</div>
</div>
```
- 蓝色系：`bar #5C6BC0`, `bg #E8EAF6`, `text #283593`, `border #9FA8DA`
- 棕色系：`bar #8D6E63`, `bg #EFEBE9`, `text #4E342E`, `border #BCAAA4`
- 粉色系（强调）：`bg #FCE4EC`, `text #C2185B`, `border #F48FB1`

**箭头形五边形框**（SVG polygon）——用于流程串联：
```html
<div class="af">
  <svg viewBox="0 0 100 54" preserveAspectRatio="none">
    <!-- 第一个框（无左缺口） -->
    <polygon points="0,2 88,2 99,27 88,52 0,52" fill="#f5f2ee" stroke="#ccc"/>
    <!-- 后续框（有左缺口） -->
    <polygon points="2,2 88,2 99,27 88,52 2,52 13,27" fill="#f0ede6" stroke="#ccc"/>
  </svg>
  <div class="txt">文字内容</div>
</div>
```

**渐变箭头流**（底部总结流程）——用 SVG polygon + linearGradient：
- 粉→蓝→紫渐变，每段有尖角箭头过渡
- 第一段：右侧尖角，左侧平
- 后续段：左右均有尖角/缺口

**流水线圆形节点**：
- 圆形带粉紫渐变：`background: linear-gradient(145deg, #F0E8F5, #E8DDF0)`
- 边框紫色：`border: 2.5px solid #8E6CA8`
- 背景长条：在圆形节点后面加一条渐变长条（opacity 0.25）增加连贯感

**竖排多列内容**（如"卫星遥感/航空遥感/农业遥感"）——**必须用 CSS grid 对齐**：
```css
.tag-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 4px 16px;
  text-align: center;
}
```
禁止用 flex + 自由文字排列——会导致列不对齐。

### 3D 透视梯形绘制模板（模式B核心）

```svg
<!-- 外层梯形（最大，上宽下窄） -->
<polygon points="130,155 730,155 660,650 200,650"
    fill="rgba(245,240,248,0.35)" stroke="#ccc" stroke-width="1.2"/>
<!-- 顶面（3D厚度） -->
<polygon points="130,155 730,155 750,140 150,140"
    fill="rgba(230,220,235,0.2)" stroke="#ccc" stroke-width="0.8"/>
<!-- 左侧面 -->
<polygon points="130,155 150,140 220,635 200,650"
    fill="rgba(220,210,225,0.15)" stroke="#ccc" stroke-width="0.5"/>
<!-- 右侧面 -->
<polygon points="730,155 750,140 680,635 660,650"
    fill="rgba(220,210,225,0.15)" stroke="#ccc" stroke-width="0.5"/>
```

每层内收比例约 8-12%，层间 y 间距约 50-70px。

### XML 骨架

```xml
<mxfile host="app.diagrams.net">
  <diagram name="路线图" id="roadmap">
    <mxGraphModel dx="1422" dy="900" grid="1" gridSize="10"
        guides="1" tooltips="1" connect="1" arrows="1"
        fold="1" page="1" pageScale="1"
        pageWidth="1200" pageHeight="1600" math="0" shadow="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 节点和连线 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 常用 style 速查

| 元素 | 关键 style 片段 |
|------|---------------|
| 主标题框 | `rounded=1;fillColor=#FCE4EC;strokeColor=#C2185B;strokeWidth=3;shadow=1;` |
| 深色横幅（紫底白字） | `rounded=1;fillColor=#7B1FA2;strokeColor=#9C27B0;fontColor=#FFFFFF;fontSize=18;fontStyle=1;shadow=1;` |
| 横幅（蓝灰） | `rounded=1;fillColor=#E8EAF6;strokeColor=#7986CB;strokeWidth=2;arcSize=40;` |
| 横幅（紫灰） | `rounded=1;fillColor=#E0D8F0;strokeColor=#A090C0;strokeWidth=2;arcSize=40;` |
| 标题胶囊（蓝底白字） | `rounded=1;fillColor=#5C6BC0;strokeColor=#7986CB;fontColor=#FFFFFF;fontStyle=1;shadow=1;` |
| 标题胶囊（棕色系） | `rounded=1;fillColor=#EFEBE9;strokeColor=#BCAAA4;fontColor=#4E342E;fontStyle=1;` |
| 强调标签（粉色） | `rounded=1;fillColor=#FCE4EC;strokeColor=#F48FB1;fontColor=#C2185B;fontStyle=1;arcSize=30;` |
| 内容卡片 | `rounded=1;fillColor=#FFFFFF;strokeColor=#BDBDBD;shadow=1;` |
| 编号圆（金黄） | `ellipse;fillColor=#FFD54F;strokeColor=#E65100;fontColor=#E65100;fontStyle=1;strokeWidth=3;` |
| 散布关键词（红） | `text;html=1;fontColor=#C2185B;fontStyle=3;fontSize=9;` |
| 散布关键词（灰） | `text;html=1;fontColor=#888;fontStyle=2;fontSize=9;` |
| 竖排文字 | `text;html=1;horizontal=0;fontSize=10;fontStyle=1;` |
| 入口/出口框 | `rounded=1;fillColor=#FFFFFF;strokeColor=#999;fontSize=12;` |
| 链条圆（粉紫渐变） | `ellipse;fillColor=#F0E8F5;strokeColor=#8E6CA8;fontStyle=1;fontColor=#4A148C;strokeWidth=2;` |
| 链条加号 | `text;fillColor=none;strokeColor=none;fontColor=#E65100;fontSize=20;fontStyle=1;` |
| 链条加号（强调） | `text;fillColor=none;strokeColor=none;fontColor=#C2185B;fontSize=24;fontStyle=1;` |
| 箭头形框 | 用 HTML 的 SVG polygon 实现，draw.io 中用 `shape=mxgraph.arrows2.arrow;` |

### 交付物

每次必须同时交付：
1. **`.html` 预览文件**——可在浏览器直接查看
2. **`.drawio` XML 文件**——可在 app.diagrams.net 打开编辑

### 评分与迭代（draw.io 模式）

draw.io / HTML 预览图**同样需要评分迭代**，和 TikZ 流程一致。由于 HTML 无法自动编译验证，需要更严格的人工审查。

**评分流程**：生成 HTML 后，逐项对照以下六维度打分（各 1-5 分）：

| 维度 | 检查要点 |
|------|---------|
| 完整性 | 原图/文案中的所有模块、标签、连线是否都已包含，无遗漏 |
| 准确性 | 文字内容正确无误，模块归属关系与原图一致 |
| 布局合理 | 各区域间距均匀，不拥挤不松散，层次分明 |
| 视觉花样 | 是否复刻了原图的装饰元素（空心字、竖条、渐变、阴影、箭头形框等），不能过于素淡 |
| 配色统一 | 同类元素颜色一致，不出现随意配色，整体和谐 |
| 文字可读 | 字号合适、无重叠遮挡、空心字清晰、多列文字对齐 |

**评分规则**：
- **总分 = 30 且无缺陷** → 交付给用户
- **总分 < 30** → 必须继续迭代修复，不展示给用户
- **总分 < 25** → 重大问题，回到分析阶段重新设计

**常见扣分项**（draw.io 模式特有）：
- 空心描边字模糊不清（stroke-width 过粗）→ 文字可读 -2
- 多列竖排文字错位（未用 grid）→ 布局合理 -2
- 悬浮标题遮盖卡片边框或超出容器 → 布局合理 -1
- 缺少原图中的装饰元素（竖条、渐变横幅、箭头框等）→ 视觉花样 -2
- 左侧分区标题字号过大，喧宾夺主 → 文字可读 -1
- 箭头形框尖角方向不统一 → 布局合理 -1
- HTML 在窄屏下溢出 → 布局合理 -1

**迭代要求**：
- 每次修改后说明改了什么
- 针对扣分项精确修复，最小化改动
- 如果用户提供了截图反馈，优先修复截图中指出的问题

### 自检

- HTML 预览在浏览器中布局正常，无溢出/错位
- SVG 梯形的坐标逐层内收，视觉上形成透视感
- 散布关键词不压盖核心文字
- 侧栏竖排文字与中心嵌套等高对齐
- draw.io XML 层级完整，id 唯一
- 配色一致（HTML 和 drawio 用同一套颜色值）
- **空心描边字清晰可读**：stroke-width ≤ 0.8，字号 ≥ 26，笔画间隙明显可见
- **左侧分区标题字号适中**：不能比右侧内容区主标题更大，通常 font-size 26-30
- **多列竖排内容用 grid 对齐**：禁止 flex 自由排列导致列错位
- **箭头形框的尖角方向统一**：第一个框左平右尖，后续框左凹右尖
- **视觉花样丰富度**：检查是否包含了参考图中的装饰元素（竖条、渐变、阴影、空心字等），避免输出过于素淡
