---
name: thesis-figure-skill
description: |
  为学术论文生成 LaTeX/TikZ 架构图、流程图、示意图的专项 skill。
  支持两种工作模式：(1) 用户提供论文文案，自动生成画图指令再生成 TikZ 代码；
  (2) 用户提供已有图片截图，直接复刻为 TikZ 代码。
  两种模式都包含编译验证与迭代修改环节，持续优化直到用户满意。
  适用于任何学科领域的中文学术论文配图，自动识别论文所属领域并以该领域
  专家身份进行配图设计。配色统一、排版紧凑、逻辑清晰，适合直接嵌入毕业论文。
  Use when the user asks to: 画论文图、画架构图、画流程图、画示意图、
  LaTeX画图、TikZ画图、论文配图、生成画图指令、复刻图片、
  画图代码、学术论文图、画系统架构、画协议流程、论文插图、tikz diagram、
  latex figure、根据论文画图、画个图、帮我画图、生成tikz、论文tikz、
  根据文案画图、照着图片画、复刻这张图。
---

# LaTeX Academic Diagram：学术论文 TikZ 配图工具

你精通 LaTeX/TikZ 绘图，擅长将论文中的系统架构、协议流程、技术方案转化为结构清晰、配色统一、适合学术论文排版的高质量配图。

## 领域自适应（重要）

在收到用户的论文文案或图片后，**首先识别论文所属的学科领域**（如计算机科学、生物医学、电气工程、经济学、化学工程等），然后以该领域资深专家的身份进行配图设计。

具体做法：
1. 阅读用户提供的文案/图片，判断其所属领域和子方向
2. 在画图指令的开头明确声明：「本文属于 XX 领域，我将以该领域专家视角进行配图设计」
3. 使用该领域的通用术语和惯用表达，确保图中标签专业准确
4. 根据该领域的常见图表风格选择合适的布局（如计算机领域常用分层架构图，生物领域常用流程/通路图，电路领域常用模块框图等）

---

## 两种工作模式

根据用户输入自动判断进入哪种模式。

### 模式一：文案驱动

用户提供论文段落/摘要/章节内容，完整流程：

```
用户提供论文文案
       ↓
  ① 生成画图文字指令（详细描述布局、模块、连线）
       ↓
  ② 根据指令生成 LaTeX/TikZ 代码
       ↓
  ③ 编译验证
       ↓
  ④ 评估打分
       ↓
  ⑤ 迭代修改（如需要，回到③循环）
       ↓
  用户满意，结束
```

步骤①完成后直接进入步骤②，不需要等用户确认（除非有明显不确定的地方）。

### 模式二：图片驱动

用户提供一张已有图片（截图/PNG），完整流程：

```
用户提供图片
       ↓
  ① 分析图片（识别模块、标签、箭头、颜色、布局）
       ↓
  ② 生成 LaTeX/TikZ 复刻代码
       ↓
  ③ 编译验证
       ↓
  ④ 评估打分（与原图对比）
       ↓
  ⑤ 迭代修改（如需要，回到③循环）
       ↓
  用户满意，结束
```

---

## 全局约束

### 语言与表达
- 使用简体中文
- 不使用难懂抽象的词语和夸大词语
- 不使用引号
- 不在标签中用括号补充英文（除非用户明确要求）
- 图中文字标签简洁准确
- 所有文字标签和标注保持水平排列，不使用竖排文字（rotate=90），中文竖排阅读体验差

### 排版与布局
- **图不要设计得太宽**——优先采用垂直分层布局，控制横向宽度
- 适合论文单栏或双栏排版
- 模块之间留有合理间距
- 箭头连线逻辑顺畅，避免交叉
- **左右对比图的中间通道**：左右两侧之间至少留出 3cm 宽的空白通道，VS 标记或分隔线放在通道正中，确保不与任何节点重叠
- **环形/辐射布局中的外部元素**（如客户端、消息队列）：不要放在环形服务节点的同一角度上，避免位置冲突。外部元素应放在环外独立区域（如正上方/正下方）

### TikZ 代码规范
- 使用 `standalone` 文档类，设置合理 `border`
- 必须加载中文支持（优先 `ctex`，环境不支持时用 `ucharclasses` 方案）
- 使用统一配色方案（见下方色板）
- 使用 `drop shadow` 提升层次感
- 使用 `fit` 和 `backgrounds` 库实现分区底色
- **层标题放置**：不要使用 `fit` 节点的 `label` 选项放置层标题（容易与相邻层标题重叠）。应在分区框节点定义之后，用独立的 `\node` 配合 `anchor` 放置标题：
  ```latex
  % 先定义分区框
  \begin{pgfonlayer}{background}
      \node[zone, ...] (L1) {};
  \end{pgfonlayer}
  % 再用独立节点放标题（在框外下方）
  \node[ltitle, anchor=north east] at (L1.south east) {本地训练层};
  ```
  这样标题位置由锚点精确控制，不会被 `fit` 的自动布局挤到不可预期的位置。
- 所有节点使用 `style` 定义，便于全局调整
- 所有节点使用 `positioning` 库的相对定位，不使用绝对坐标
- 编译方式为 `xelatex`
- **标注文字防遮挡**：箭头旁的标注文字统一使用 `fill=white, inner sep=2pt` 样式，防止被交叉的线条遮挡
- **中文标注渲染陷阱（重要）**：在编译环境中，`\scriptsize` 或更小字号的中文配合 `fill=white` 可能渲染为不透明色块（特别是在 `tag` 样式下）。对于**非箭头旁的独立标注**（如回路标注、跨层标注），应使用不带 `fill` 的 `annot` 样式：
  ```
  annot/.style={font=\footnotesize, inner sep=2pt}
  ```
  只有紧贴箭头中段、可能被交叉线遮挡的标注才使用 `fill=white` 的 `tag` 样式。
- **绝对禁止 `rotate=90` 中文标注**：TikZ 中 `rotate=90` 的中文在 xelatex 编译后会渲染为不可读的色块。所有标注必须水平放置。如果空间不够，改用更短的标注文字或换行（`\\`），或使用 `annot` 样式配合 `anchor=east/west` 放在空白区域

### 跨区箭头与回路箭头规范（重要）
- **跨区箭头**：当箭头需要从一个分区指向另一个分区内的节点时，箭头应在两个分区框之间的空白区域中转，**不应直接刺穿虚线框**。具体做法：将跨区连线分为两段，在分区框之间设置中间坐标点（coordinate），从源节点画到中间点，再从中间点画到目标节点
- **回路箭头**（如全局模型下发、反馈循环等）：必须指向**所有相关目标节点**，不能只指向其中一个。

#### 回路走线方案选择（按优先级排序）

**方案一（首选）：分段绘制弧线指向分区框边界**
当回路需要从顶层指向底层多个节点时，箭头指向整个分区框的边界（`.west` 或 `.east`），而非逐个节点。

**关键：必须将回路拆分为 3 段独立 `\draw` 命令**，不能用单条 `\draw` 配合 `rounded corners`（单条 `\draw` 的 `rounded corners` 会让路径在转弯处穿入分区框）。

```latex
% === 左侧回路示例：从 source 到 target_zone 左边界 ===
% 左外侧主干 x = target_zone 左边界 - 1.5cm
\coordinate (leftRail) at ($(target_zone.west)+(-1.5,0)$);

% 第1段：源节点左出 → 到左外侧主干（水平段）
\draw[dashed, thick, color=..., rounded corners=10pt]
    (source.west) -- (leftRail |- source.west);
% 第2段：主干竖直下行（无转弯，不会穿越任何框）
\draw[dashed, thick, color=...]
    (leftRail |- source.west) -- (leftRail |- target_zone.west);
% 第3段：从主干水平右行 → 终止于分区框左边界（带箭头）
\draw[-{Stealth[scale=1.1]}, dashed, thick, color=...]
    (leftRail |- target_zone.west) -- (target_zone.west);

% 标注放在主干竖直段中点旁
\node[annot, anchor=east, align=center]
    at ($(leftRail |- middle_zone)+(-0.15,0)$) {全局模型\\[-1pt]下发};
```

这种分段画法确保每段都是纯水平或纯竖直线，不存在 `rounded corners` 导致路径偏移穿入框体的问题。

**方案二：底部总线分发**
当语义上需要明确箭头到达每个子节点时，使用底部总线：主干从源节点左/右外侧下行到分区框下方（至少 0.8cm），在底部铺一条横线经过各目标节点的 x 坐标，从每个 x 坐标处向上发短箭头到目标节点底部。
```
% 底部总线：主干下行到框下方，横线分叉向上
\path let \p1=(zone.south) in coordinate (bot) at (0, \y1-0.8cm);
\draw[dashed, thick, ...] (source.west) -- (Lx |- source.west) -- (Lx |- bot);
\draw[dashed, thick, ...] (Lx |- bot) -- (nodeC |- bot);
\draw[arr_dash] (nodeA |- bot) -- (nodeA_target.south);
\draw[arr_dash] (nodeB |- bot) -- (nodeB_target.south);
\draw[arr_dash] (nodeC |- bot) -- (nodeC_target.south);
```
注意两条底部总线需要不同的 y 偏移量（如 0.8cm 和 1.6cm）避免重叠。

**禁止方案A：单条 `\draw` + `rounded corners` 画长距离回路**
~~`\draw[rounded corners=10pt] (source.west) -- ++(-1,0) -- ++(0,-10) -- (target.west);`~~ —— 看起来简洁，但 `rounded corners` 会让转弯处的路径偏移，导致线条穿入分区虚线框。**长距离回路必须拆分为多段 `\draw`**。

**禁止方案B：侧面水平分叉穿越**
~~从左/右外侧竖线分叉水平箭头穿入到各节点的 .west/.east~~ —— 这种方式在分层架构图中**必然**会导致水平箭头穿过分区框并压在中间节点上。**绝对不要使用此方案**，即使竖线主干在框外也不行，因为水平分叉箭头会穿越其他节点的框体。

- **回路走线位置**：回路线必须走在**所有节点和标注之外的空白区域**。具体做法：用 `\coordinate` 基于分区框边界计算主干 x 坐标（如 `$(target_zone.west)+(-1.5,0)$`），然后用 `|-` 语法（intersection of）取交点，不要用硬编码的绝对偏移量（如 `++(0,-13.0)`），因为绝对偏移在节点数量或间距变化时容易错位
- **回路箭头标注**：回路线的标注文字应水平放置在主干线旁边的空白处（如底部横线段上方），不使用 rotate=90 竖排
- **跨层标注**：在两个分区框之间的空白处放置数据流标注文字，不要让标注与层标题重叠。标注与层标题之间至少保留 5pt 间距
- **虚线/回路不穿越节点**：所有虚线（异步连线、回路下发线等）必须绕行到节点外侧，不能穿过其他节点框或标注文字

---

## 统一配色方案

所有图表使用以下配色，保持论文全篇视觉一致：

```latex
\definecolor{drawBlueFill}{HTML}{DAE8FC}
\definecolor{drawBlueLine}{HTML}{6C8EBF}
\definecolor{drawGreenFill}{HTML}{D5E8D4}
\definecolor{drawGreenLine}{HTML}{82B366}
\definecolor{drawOrangeFill}{HTML}{FFE6CC}
\definecolor{drawOrangeLine}{HTML}{D79B00}
\definecolor{drawPurpleFill}{HTML}{E1D5E7}
\definecolor{drawPurpleLine}{HTML}{9673A6}
\definecolor{drawRedFill}{HTML}{F8CECC}
\definecolor{drawRedLine}{HTML}{B85450}
\definecolor{drawGreyFill}{HTML}{F5F5F5}
\definecolor{drawGreyLine}{HTML}{666666}
```

**配色语义建议**（根据论文领域和具体图表灵活调整）：

| 颜色 | 典型用途 |
|------|---------|
| 蓝色 | 通用模块、基础层、输入端 |
| 绿色 | 核心/创新模块、安全/可信组件、正向流程 |
| 橙色 | 数据流、传感器、传输通道、需要强调的元素 |
| 紫色 | 高层抽象、决策/验证层、外部系统 |
| 红色 | 关键操作、警告、约束条件、需要特别注意的节点 |
| 灰色 | 辅助服务、存储、外围模块、已有/不变的组件 |

以上为默认建议，实际配色应根据论文领域的语义需要灵活分配。例如生物学论文中绿色可用于细胞/有机体，化学论文中橙色可用于催化反应等。

---

## 标准 TikZ 模板骨架

所有图表基于以下骨架扩展：

### 中文字体配置策略

**优先使用方案 A（ctex）**。如果环境中没有 ctex，先尝试安装（`apt-get install texlive-lang-chinese`），安装失败再退回方案 B。

**方案 A（首选）：ctex + Noto Sans CJK SC**
```latex
\usepackage[fontset=none]{ctex}
\setCJKmainfont{Noto Sans CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
```

**方案 B（回退）：无法安装 ctex 时，用 ucharclasses + Noto Sans CJK SC**
```latex
\usepackage{fontspec}
\setmainfont{DejaVu Sans}
\setsansfont{DejaVu Sans}
\newfontfamily\cjkfont{Noto Sans CJK SC}
\usepackage{ucharclasses}
\setTransitionsForCJK{\cjkfont}{\rmfamily}{\rmfamily}
```

两种方案都支持 `\bfseries` 和 `\textbf`，无需做粗体替代处理。

**用户交付版**：无论本地用哪种方案，交付给用户的 `.tex` 文件顶部都用注释说明：如需在 Overleaf 编译，将字体配置替换为 `\usepackage{ctex}`。

以下模板骨架展示方案 A 的写法（方案 B 只需替换字体配置部分）：

```latex
\documentclass[tikz,border=25pt]{standalone}
\usepackage{tikz}
% ===== 中文支持 =====
% 当前为服务器编译版，确保中文正确渲染
% 如在 Overleaf 编译，可将字体配置替换为 \usepackage{ctex}
\usepackage[fontset=none]{ctex}
\setCJKmainfont{Noto Sans CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
\usetikzlibrary{shapes, arrows.meta, positioning, fit, backgrounds, calc, shadows}

% ===== 统一色板 =====
\definecolor{drawBlueFill}{HTML}{DAE8FC}
\definecolor{drawBlueLine}{HTML}{6C8EBF}
\definecolor{drawGreenFill}{HTML}{D5E8D4}
\definecolor{drawGreenLine}{HTML}{82B366}
\definecolor{drawOrangeFill}{HTML}{FFE6CC}
\definecolor{drawOrangeLine}{HTML}{D79B00}
\definecolor{drawPurpleFill}{HTML}{E1D5E7}
\definecolor{drawPurpleLine}{HTML}{9673A6}
\definecolor{drawRedFill}{HTML}{F8CECC}
\definecolor{drawRedLine}{HTML}{B85450}
\definecolor{drawGreyFill}{HTML}{F5F5F5}
\definecolor{drawGreyLine}{HTML}{666666}

\pgfdeclarelayer{background}
\pgfsetlayers{background,main}

\begin{document}
\begin{tikzpicture}[
    node distance=1.2cm and 2cm,
    every node/.style={font=\footnotesize},
    base_box/.style={
        rectangle, rounded corners=3pt, align=center,
        minimum height=0.9cm, minimum width=2.8cm,
        drop shadow={opacity=0.15}, thick
    },
    blue_node/.style={base_box, fill=drawBlueFill, draw=drawBlueLine},
    green_node/.style={base_box, fill=drawGreenFill, draw=drawGreenLine},
    orange_node/.style={base_box, fill=drawOrangeFill, draw=drawOrangeLine},
    purple_node/.style={base_box, fill=drawPurpleFill, draw=drawPurpleLine},
    red_node/.style={base_box, fill=drawRedFill, draw=drawRedLine,
        font=\footnotesize\bfseries},
    grey_node/.style={base_box, fill=drawGreyFill, draw=drawGreyLine},
    sensor/.style={
        circle, draw=drawOrangeLine, fill=drawOrangeFill,
        inner sep=0pt, minimum size=1.3cm,
        align=center, thick, font=\footnotesize
    },
    database/.style={
        cylinder, cylinder uses custom fill,
        cylinder body fill=drawGreyFill, cylinder end fill=black!10,
        shape border rotate=90, draw=drawGreyLine,
        aspect=0.25, minimum height=1.2cm, minimum width=1.8cm,
        align=center, thick
    },
    arrow/.style={-{Stealth[scale=1.2]}, thick, color=black!70},
    arrow_data/.style={-{Stealth[scale=1.2]}, very thick, color=drawOrangeLine},
    arrow_dash/.style={-{Stealth[scale=1.2]}, dashed, thick, color=black!70},
    tag/.style={font=\scriptsize, fill=white, inner sep=2pt, rounded corners=1pt},
    annot/.style={font=\footnotesize, inner sep=2pt},
    zone/.style={dashed, thick, inner sep=15pt, rounded corners=8pt},
    layer_title/.style={font=\bfseries\small, inner sep=5pt}
    % 注意：层标题不要用 zone 的 label 选项，
    % 应在分区框定义后用独立 \node[layer_title, anchor=...] 放置
]

% ===== 节点、连线、分区 =====

\end{tikzpicture}
\end{document}
```

---

## 各步骤详细说明

### 步骤①-A：生成画图文字指令（模式一）

首先阅读用户提供的论文段落，**识别论文所属领域**，然后以该领域专家身份输出一份详细的画图文字指令。目标是：**任何人仅凭此文字就能画出完整的图**。

必须包含：

0. **领域识别**：明确声明论文所属领域和子方向，后续所有术语和布局选择基于此

1. **整体布局策略**：选用垂直分层 / 左右对比 / 环形流程等，说明理由
2. **每一层/区域包含的模块**：
   - 模块名称
   - 一句话功能说明
   - 使用哪种颜色样式
   - 标注是原有模块还是新增模块（如适用）
3. **连线逻辑**（图的灵魂）：
   - 每条连线的起点、终点
   - 线型：实线 / 虚线 / 粗实线
   - 箭头方向
   - 标注文字
4. **视觉强调点**：如加密标记、销毁标记、对比色块等

输出格式：

```
### 图名：XXX示意图

#### 一、整体布局
- 采用XXX布局，理由是...

#### 二、各层模块
##### 底层：XXX层
- 模块A（蓝色）：...
- 模块B（绿色，新增）：...

##### 中层：XXX层
- ...

##### 顶层：XXX层
- ...

#### 三、连线与数据流
1. 模块A → 模块B：实线箭头，标注"加密数据"
2. 模块C → 模块D：虚线箭头，标注"反馈结果"
3. ...

#### 四、视觉强调
- 在XX处使用红色突出
- 在XX处添加销毁标记
```

完成后直接进入步骤②。

### 步骤①-B：分析图片（模式二）

仔细观察用户提供的截图，识别并记录：
- 所有模块的形状、大小、相对位置
- 所有文字标签的内容
- 颜色和填充（映射到统一色板）
- 箭头方向、线型、标注文字
- 分区边界和底色
- 层次标题文字

如有不清晰的文字，合理推测并在代码注释中标注。
如果原图布局过宽或不合理，可以适当优化，但要告知用户做了哪些调整。

### 步骤②：生成 LaTeX/TikZ 代码

基于步骤①的结果，生成完整可编译的 `.tex` 文件。

**生成后执行自检清单**：
- [ ] `\documentclass` 在第一行
- [ ] `border` 设置为 25pt 或更大（有外部回路标注时需要 35pt，确保标注不被裁切）
- [ ] 加载了中文支持（ctex 或 ucharclasses 方案）
- [ ] 所有 `\definecolor` 在 `\begin{document}` 之前
- [ ] 没有未闭合的花括号或 `\begin/\end` 不配对
- [ ] 所有引用的节点名称都已定义
- [ ] `positioning` 引用的锚点节点在引用之前定义
- [ ] 没有使用未加载的 TikZ 库
- [ ] 中文文字没有放在不支持中文的命令中（如 `\texttt`）
- [ ] **没有使用 `rotate=90` 竖排中文**，所有标注水平放置
- [ ] 回路箭头指向了所有相关目标节点，而非只指向其中一个
- [ ] **回路使用了分段绘制方案（3段独立 `\draw`）或底部总线方案**，没有使用单条 `\draw` + `rounded corners` 画长距离回路，也没有使用侧面水平分叉穿越方案
- [ ] **回路终止段的箭头精确终止于分区框边界**（如 `target_zone.west` 或 `target_zone.east`），没有穿入框内
- [ ] 跨区箭头没有直接刺穿虚线框，而是在分区之间的空白区域中转
- [ ] 跨层标注文字与层标题之间有足够间距，不会重叠
- [ ] **虚线/回路线没有穿过任何节点框**，走在节点外侧空白区域
- [ ] **回路主干线与节点边缘至少 0.7cm 间距**
- [ ] **箭头旁标注使用 `tag` 样式**（`fill=white`），**独立标注使用 `annot` 样式**（不带 `fill`），避免中文色块
- [ ] **左右对比图中间通道 >= 3cm**，VS 标记不与任何节点重叠
- [ ] **所有标注文字在画布 border 范围内**，不会被裁切

将代码保存为 `.tex` 文件供用户下载。

### 步骤③：编译验证

**首次编译前必须确保 ctex 可用**（后续迭代可跳过）：

```bash
# 1. 检测 ctex 是否已安装
if kpsewhich ctex.sty > /dev/null 2>&1; then
    echo "ctex: YES"
else
    echo "ctex: NO，尝试安装..."
    apt-get update -qq && apt-get install -y -qq texlive-lang-chinese 2>&1 | tail -3
    # 安装后再次检测
    kpsewhich ctex.sty && echo "ctex 安装成功" || echo "ctex 安装失败，将使用方案 B"
fi
# 2. 确认 CJK 字体
fc-list :lang=zh family | grep -i "Noto Sans CJK SC" | head -3
```

- **ctex 可用**（安装成功或已有）：使用方案 A（`\usepackage[fontset=none]{ctex}`），这是首选方案
- **ctex 不可用**（安装失败）：切换到方案 B（`ucharclasses`），修改 `.tex` 文件头部后编译

确认字体配置正确后编译：

```bash
xelatex -interaction=nonstopmode diagram.tex
```

四种情况的处理：
- **编译成功**：用 `pdftoppm` 将 PDF 转为 PNG 预览图，查看 PNG 进入步骤④评估
- **字体/宏包缺失错误**：检查是方案 A 还是方案 B 的问题，切换方案或安装依赖后重试
- **其他编译失败**：分析 `.log` 文件中的错误，修复代码后重新编译
- **无 LaTeX 环境**：将 `.tex` 文件提供给用户，请用户在 Overleaf 等平台编译后将结果截图发回

**最终输出规则（重要）**：
- 同时输出 **`.tex` 源文件** 和 **高清 PNG 预览图**（或 PDF）给用户
- 编译时使用服务器编译版字体配置（`fontset=none` + Noto Sans CJK SC），确保输出的 PDF/PNG 中文正确
- 编译成功后用 `pdftoppm -png -r 300` 将 PDF 转为高清 PNG
- 用 `present_files` 将 `.tex` 和 `.png`（或 `.pdf`）一起交付给用户
- 在 `.tex` 文件顶部用注释说明：如需在 Overleaf 编译，将字体配置替换为 `\usepackage{ctex}`

### 步骤④：评估打分

**评估前必须执行的缺陷扫描清单**（逐项检查 PNG 预览图，发现任何一项即扣分）：

- [ ] **文字重叠**：任意两段文字（标签、标注、层标题）是否有重叠或紧贴？特别注意跨层箭头标注与层标题之间
- [ ] **箭头落点**：每条箭头是否精确指向目标节点的边界？是否有箭头指向空白区域或框外？
- [ ] **回路箭头**：下行/反馈箭头是否对称合理？是否只指向部分节点而遗漏其他？
- [ ] **层标题归属**：每个层标题是否明确位于对应分区框的边缘？是否会被误认为属于相邻层？
- [ ] **标题被箭头遮挡**：层标题是否位于箭头的路径上？如果箭头从两层之间穿过，标题不应放在箭头正下方/正上方，应偏移到框的左下角或右下角
- [ ] **标注位置**：箭头旁的标注文字是否紧贴箭头中段？是否偏移到无关区域？
- [ ] **分区框边界**：虚线框是否完整包裹住所属模块？是否有模块半露在框外？
- [ ] **箭头穿越分区框**：是否有箭头从分区框外部直接穿过虚线框边界指向框内节点？外部回路线应在框边界处终止或从框的开口处进入，不应刺穿虚线框
- [ ] **间距均匀**：相邻层之间的间距是否一致？同层内的模块间距是否均匀？
- [ ] **文字紧贴**：即使没有重叠，两段不同文字之间是否间距过小（视觉上快要粘连）？特别注意层标题与跨层箭头标注之间
- [ ] **竖排文字**：是否有使用 rotate=90 的竖排中文？
- [ ] **虚线穿越节点**：是否有虚线（异步连线、回路线等）从其他节点框上方穿过？虚线应绕行到节点外侧
- [ ] **标注被线遮挡**：标注文字是否被经过的线条遮挡？如果可能有交叉，标注应使用 `fill=white` 白底
- [ ] **标注渲染为色块**：是否有中文标注显示为不透明的矩形色块而非可读文字？如有，改用 `annot` 样式（不带 `fill`）或增大字号为 `\footnotesize`
- [ ] **标注被裁切**：是否有标注文字超出画布边界被截断？如有，增大 `border` 值或调整标注位置

**在上述清单中，每发现一个问题，对应维度至少扣1分。文字重叠和虚线穿越节点是严重问题，发现即该维度不超过2分。**

然后从六个维度评估，每项 1-5 分：

| 维度 | 5分标准 | 3分标准 | 1分标准 |
|------|--------|--------|--------|
| **完整性** | 所有模块和连线齐全 | 缺少1-2个次要元素 | 大量缺失 |
| **准确性** | 标签、箭头与原文完全一致 | 1-2处小偏差 | 多处错误 |
| **布局合理** | 紧凑不过宽，层次分明，层标题归属清晰 | 局部拥挤或层级归属有歧义 | 过宽或严重混乱 |
| **连线清晰** | 无交叉、无重叠，回路箭头对称完整 | 1处交叉或回路不完整 | 大量交叉或箭头指向错误 |
| **配色统一** | 使用统一色板，语义对应 | 基本统一但1-2处语义不当 | 颜色随意 |
| **文字可读** | 无任何文字重叠，标注位置精确，间距合理 | 1处轻微紧贴 | 多处重叠难以辨认 |

评分输出：

```
### 缺陷扫描
- [x/✗] 文字重叠：...
- [x/✗] 箭头落点：...
- [x/✗] 回路箭头：...
- [x/✗] 层标题归属：...
- [x/✗] 标注位置：...
- [x/✗] 分区框边界：...
- [x/✗] 间距均匀：...
- [x/✗] 竖排文字：...
- [x/✗] 虚线穿越节点：...
- [x/✗] 标注被线遮挡：...

### 评分

| 维度     | 得分 | 说明 |
|----------|------|------|
| 完整性   | ?/5  | ... |
| 准确性   | ?/5  | ... |
| 布局合理 | ?/5  | ... |
| 连线清晰 | ?/5  | ... |
| 配色统一 | ?/5  | ... |
| 文字可读 | ?/5  | ... |
| **总分** | ?/30 | ... |
```

决策逻辑：
- **总分 ≥ 25 且缺陷扫描全部通过**：告知用户质量良好，询问是否满意或需要微调
- **总分 ≥ 25 但缺陷扫描有未通过项**：仍需进入步骤⑤修复缺陷
- **总分 < 25**：列出需要修改的具体问题，主动进入步骤⑤

### 步骤⑤：迭代修改

根据步骤④的评估结果或用户提出的修改意见，修改 TikZ 代码。

修改原则：
- 精确定位问题，最小化改动范围
- 每次修改后说明改了什么、为什么改
- 修改后回到步骤③重新编译验证
- 持续循环直到用户满意

---

## 常见图表类型与布局建议

| 图表类型 | 推荐布局 | 适用场景 |
|---------|---------|---------|
| 系统架构图 | 自下而上垂直分层 | 层次递进关系，如端→云→链、硬件→中间件→应用 |
| 协议/流程图 | 从左到右或从上到下 | 时序步骤、实验流程、信号处理流水线 |
| 时序交互图 | 多列生命线+水平消息 | 多方协议交互、握手流程，参与方作纵向生命线，消息按时间从上到下排列 |
| 对比方案图 | 左右并列 | 原有 vs 改进、方案A vs 方案B，中间留 3cm+ 通道放 VS 标记 |
| 数据流水线图 | 水平四阶段 | 从左到右的多阶段处理流水线，每阶段顶部放图标，内部放子模块 |
| 模块交互图 | 中心辐射 | 核心模块居中（如 API 网关）、周围子系统环绕，可配合数据库/消息队列 |
| 数据流转图 | 自上而下线性 | 输入→处理→输出，强调数据/信号变换 |
| 网络/拓扑图 | 网络状/树状 | 物理节点连接、组织结构、分类层级 |
