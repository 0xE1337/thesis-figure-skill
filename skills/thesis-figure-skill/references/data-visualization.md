# 数据可视化模板（TikZ 原生绘制）

当图表中需要嵌入信号波形、频谱柱状图、热力图矩阵等数据可视化元素时，使用以下 TikZ 原生模板。不需要 pgfplots——纯 TikZ 的 `\draw plot` 和 `\fill` 足够绘制学术级可视化。

## 字体最小尺寸（关键规则）

数据可视化混合图信息密度高，容易把字缩得太小。**强制最小字号**：

| 元素 | 最小字号 | 禁止使用 |
|------|---------|---------|
| 框标题/模块名 | `\small\bfseries` | `\scriptsize` |
| 坐标轴标签 | `\footnotesize` | `\tiny` |
| 数据标注（百分比、数值） | `\footnotesize` | `\tiny` |
| 公式 | `\footnotesize` | `\scriptsize` |
| 图例文字 | `\footnotesize` | `\tiny` |

**绝对禁止 `\tiny`**——在 300dpi PNG 中 `\tiny` 文字几乎不可读。如果空间不够放 `\footnotesize`，说明框太小了——加大框尺寸，不要缩小字。

## 坐标轴标签防重叠（最高频问题）

嵌入图表的坐标轴有**三种文字重叠**，每次都会出现，必须在生成代码时主动预防：

| 重叠类型 | 表现 | 修复方法 |
|---------|------|---------|
| x 轴标题 vs x 轴刻度值 | "Iterations (×10³)" 和 "400" 挤在一起 | 标题加 `yshift=-6pt` 或 `-8pt` |
| y 轴旋转标题 vs y 轴刻度值 | "Loss" 和 "0.5" 重叠 | 标题加 `xshift=-15pt` |
| 迷你图表 x 轴标签 vs 框外文字 | 框内 "Epoch" 和框外 "Local SGD" 重叠 | scope 整体上移 0.3cm，或框高度加大 |

**生成代码时的强制动作**：每画一个坐标轴，立刻给轴标题加 shift——不要等渲染后才发现重叠。默认值：x 轴标题 `node[below, yshift=-5pt]`，y 轴标题 `node[left, xshift=-12pt, rotate=90]`。

## 嵌入可视化尺寸（关键规则）

嵌入在框内的迷你可视化（热力图、柱状图、波形等）必须**居中并占满框面积的 60% 以上**。不要把一个 1cm×1cm 的热力图塞在 5cm×4cm 的框角落——要么放大热力图填满框，要么缩小框。空白区域不能超过可视化区域。

## 容器边界强制检查（最容易犯的错）

框内嵌入的所有内容（可视化 + 坐标轴 + 标签文字）**必须完全在框边界内**，且四周留 ≥ 0.3cm padding。

**代码层面验证公式**（生成代码后必须检查）：
```
框 y 范围: [center_y - height/2, center_y + height/2]
标题占用: 顶部 ~0.5cm（标题 + padding）
可用区域: [center_y - height/2 + 0.3, center_y + height/2 - 0.8]
内容底部: scope_shift_y - rows * row_height - label_height
→ 检查: 内容底部 > 可用区域下界
```

最常见的溢出有两种：
1. 热力图/矩阵下方的标签（如"Attention Map"）跑到框线外面——忘了加标签的 ~0.3cm
2. **柱状图/条形图底部的 x 轴文字标签**（如"本系统""BLEU-4""满意度"）——这些标签在 scope 内通常位于 y≈-0.25，是最容易被忽略的溢出源

**生成代码时的强制计算流程**（每个含可视化的框都必须执行）：
```
步骤1: 列出内容高度
  标题行:     0.5cm
  上方padding: 0.3cm
  可视化本体:  (根据内容计算)
  x轴标签:    0.4cm  ← 最容易遗漏！
  下方padding: 0.5cm  ← 要留够！
  ──────────────
  总计:       框最小高度

步骤2: 设框高度 = 总计（向上取整到 0.5cm）
步骤3: 写注释验证
  % 框: [y_bottom, y_top], 标签底: y_label, padding: y_label - y_bottom = Xcm ✓
```

**标签和 padding 必须算在内容高度内，不是"可选的额外空间"。**

## 嵌入可视化水平居中（常见偏移问题）

嵌入可视化在框内**必须水平居中**。最常见的错误：scope shift 的 x 坐标没有对准框中心，导致可视化整体偏左或偏右。

**居中计算公式**：
```
框中心 x: box_center_x
可视化总宽度: viz_width（含 y 轴标签和右侧数值标签）
scope shift x = box_center_x - viz_width / 2
```

**最容易偏移的情况**：
- 横条图（如 SHAP 贡献度）：左侧有类别名称标签，右侧有数值——总宽度 = 标签宽 + 条形宽 + 数值宽，scope x 要基于这个总宽度居中
- 柱状图：左侧有 y 轴标签，scope x 不能从框左边开始，要算上 y 轴占的宽度后居中
- 分段条形图：总宽度包含两端的阈值标注

**验证方法**：scope shift x + viz_width/2 ≈ box_center_x（误差 ≤ 0.2cm）。如果差距 > 0.3cm 就明显偏了。

## 波形图（Waveform / Time-Domain Signal）

多条叠加正弦波，模拟时序信号：

```latex
% 坐标轴
\draw[-{Stealth[scale=0.7]}, thick] (0.6,0.5) -- (0.6,4.0)
  node[left, font=\scriptsize, pos=0.5, rotate=90, anchor=south] {Amplitude};
\draw[-{Stealth[scale=0.7]}, thick] (0.6,0.5) -- (5.2,0.5)
  node[below, font=\scriptsize, pos=0.5] {Time};

% 多色叠加波形（每条用不同颜色和频率参数）
\draw[waveBlue, thick, smooth, samples=80, domain=0.8:5.0]
  plot (\x, {2.2 + 0.85*sin((\x-0.8)*200) + 0.3*sin((\x-0.8)*500)});
\draw[wavePurple, thick, smooth, samples=80, domain=0.8:5.0]
  plot (\x, {2.2 + 0.65*sin((\x-0.8)*280+40) + 0.35*sin((\x-0.8)*150)});
```

**要点**：
- `samples=80` 确保曲线平滑；复杂波形可提高到 `samples=120`
- `smooth` 关键字让 TikZ 使用贝塞尔插值
- 基线 y 值（如 `2.2`）决定波形的中心位置
- 叠加多个 `sin` 项产生复杂波形；高噪声 → 多项+高频，低噪声 → 少项+低频
- **"处理前"用多项高频（嘈杂），"处理后"用少项低频（平滑）**——对比效果直观

## 频谱柱状图（Bar Chart / Frequency Spectrum）

```latex
% 坐标轴
\draw[-{Stealth[scale=0.7]}, thick] (0.6,0.5) -- (0.6,4.0)
  node[left, font=\scriptsize, pos=0.5, rotate=90, anchor=south] {Magnitude};
\draw[-{Stealth[scale=0.7]}, thick] (0.6,0.5) -- (5.2,0.5)
  node[below, font=\scriptsize, pos=0.5] {Frequency};

% 柱状图（每根柱子一个 \fill 矩形）
\fill[barBlue]   (0.90,0.5) rectangle (1.35,1.7);   % 低频
\fill[barPurple] (1.50,0.5) rectangle (1.95,2.5);   % 中频
\fill[barDeep]   (2.10,0.5) rectangle (2.55,3.6);   % 主频（最高）
\fill[barBlue!60](2.70,0.5) rectangle (3.15,2.0);   % 中频
% ... 逐渐递减

% 标注最高峰
\draw[-{Stealth[scale=0.7]}, thick, wavePurple]
  (3.3,3.9) -- (2.4,3.65);
\node[font=\scriptsize, text=wavePurple] at (3.5,4.05) {Peak};
```

**要点**：
- 柱子宽度统一（如 0.45cm），间隔统一（如 0.15cm）
- 高度从高到低排列呈现"频谱衰减"效果
- 主频柱子用最深的颜色，其余逐渐变浅
- 半透明滤波器叠加层用 `\fill[color, opacity=0.2] ... .. controls ... -- cycle;`

## 热力图矩阵（Heatmap / Attention Weights）

```latex
% N×N 热力图（对角线强调模式，模拟注意力权重）
\foreach \row in {0,...,7} {
  \foreach \col in {0,...,7} {
    \pgfmathsetmacro{\dist}{abs(\row-\col)}
    \pgfmathsetmacro{\noise}{int(mod(\row*5+\col*3+\row*\col,4))}
    \pgfmathtruncatemacro{\score}{min(4, int(\dist + \noise/2))}
    \ifnum\score=0 \def\cellcol{heatDeep}\fi    % 对角线：最深
    \ifnum\score=1 \def\cellcol{heatDark}\fi
    \ifnum\score=2 \def\cellcol{heatMid}\fi
    \ifnum\score=3 \def\cellcol{heatLight}\fi
    \ifnum\score=4 \def\cellcol{heatBg}\fi       % 远离对角线：最浅
    \fill[\cellcol] ({x0+\col*0.38},{y0+\row*0.35})
      rectangle ({x0+\col*0.38+0.36},{y0+\row*0.35+0.33});
    \draw[white, very thin] ({x0+\col*0.38},{y0+\row*0.35})
      rectangle ({x0+\col*0.38+0.36},{y0+\row*0.35+0.33});
  }
}
```

**要点**：
- 格子大小 0.36×0.33cm，间距由白色细线（`very thin`）产生
- `\score` 计算基于到对角线的距离+伪随机噪声，模拟真实注意力分布
- 5 级色阶：heatDeep（最深紫）→ heatDark → heatMid → heatLight → heatBg
- 矩阵大小建议 6×6 到 10×10，太大会挤在一起
- 非对角线模式（如块状注意力）：修改 `\dist` 计算公式

## 前后对比小图（Before/After Mini-plots）

```latex
% 外框
\fill[bgColor, rounded corners=6pt, draw=borderColor, thick]
  (x0, y0) rectangle (x1, y1);
\node[font=\small\bfseries] at (center) {SAB Effect Comparison};

% Before（嘈杂波形）
\fill[white, rounded corners=3pt, draw=border!50] (bx0,by0) rectangle (bx1,by1);
\node[font=\scriptsize\bfseries] at (bcenter) {Before SAB};
\draw[waveBlue, thick, smooth, samples=70, domain=a:b]
  plot (\x, {y + 0.4*sin((\x)*380) + 0.2*sin((\x)*850) + 0.12*sin((\x)*1400)});

% After（平滑波形）
\fill[white, rounded corners=3pt, draw=border!50] (ax0,ay0) rectangle (ax1,ay1);
\node[font=\scriptsize\bfseries] at (acenter) {After SAB};
\draw[wavePurple, thick, smooth, samples=70, domain=a:b]
  plot (\x, {y + 0.4*sin((\x)*380)});  % 只保留基频，去掉高频噪声
```

**要点**：
- Before 波形：3+ 个 sin 项叠加，包含高频噪声
- After 波形：仅保留 1 个 sin 基频项，视觉上明显更平滑
- 两个小图并排，宽度相同，波形振幅相同，仅复杂度不同

## 半透明滤波器叠加（Filter Overlay）

```latex
\fill[filterColor, opacity=0.2]
  (x_start,y_base) -- (x_start,y_peak)
  .. controls (x_mid1,y_ctrl1) and (x_mid2,y_ctrl2) ..
  (x_end,y_low) -- (x_end,y_base) -- cycle;
```

用贝塞尔控制点画出钟形/衰减形状的半透明覆盖层，叠在柱状图上方表示"滤波器频率响应"。

## 推荐配色

数据可视化图建议使用蓝紫学术配色（cool palette），和常规框图的暖色系区分开：

| 变量名 | 色值 | 用途 |
|--------|------|------|
| waveBlue | `#3B82F6` | 主波形线 |
| wavePurple | `#8B5CF6` | 副波形线 |
| waveCyan | `#06B6D4` | 第三波形 |
| wavePink | `#EC4899` | 第四波形 |
| barBlue | `#3B82F6` | 柱状图主色 |
| barPurple | `#8B5CF6` | 柱状图重点 |
| heatDeep | `#6D28D9` | 热力图最深 |
| heatDark | `#3B82F6` | 热力图深 |
| heatMid | `#93C5FD` | 热力图中 |
| heatLight | `#DBEAFE` | 热力图浅 |
| boxBg | `#D6E4F0` | 可视化框背景 |
| boxTitleBg | `#B8CCE4` | 可视化框标题栏 |

## 与常规框图混合使用（混合图生成策略）

混合图 = 架构流程框图 + 嵌入式数据可视化。不是所有框都要嵌入可视化——**只在有具体数值或可量化信息的模块中嵌入**。

### 代码结构

```
\begin{tikzpicture}
  % 1. 先画外层框图骨架（所有 \node 定义）
  \node[big_box] (moduleA) at (...) {};    % 有可视化的大框
  \node[small_box] (moduleB) at (...) {};  % 纯文字的普通框

  % 2. 在大框内用 scope 画嵌入可视化
  \begin{scope}[shift={(moduleA 的内部坐标)}]
    % 坐标轴、柱状图、热力图等
  \end{scope}

  % 3. 最后画框之间的连线
  \draw[arrow] (moduleA) -- (moduleB);
\end{tikzpicture}
```

### 两种框的尺寸差异

| 框类型 | 最小宽度 | 最小高度 | 内容 |
|--------|---------|---------|------|
| 普通框（纯文字） | 3.0cm | 1.1cm | 标题 + 1-2行描述 |
| 可视化框（嵌入图） | 5.0cm | 4.0cm | 标题 + 迷你可视化 + 标签 |

可视化框是普通框的 **1.5-2 倍大**——这种大小差异本身就形成了视觉层次：大框=重要/有数据，小框=过渡/逻辑。

### 混合比例

一张图中 **30-50%** 的模块嵌入可视化最佳：
- 太少（<20%）：回到纯框图，不够生动
- 太多（>60%）：信息过密，每个可视化都挤在一起看不清
- 适中（30-50%）：重点模块有丰富细节，过渡模块简洁干净，节奏感好

### 配色协调

混合图中两套配色并存——框图用暖色系（draw.io 6 色），嵌入可视化用冷色系（蓝紫 palette）。两套颜色在视觉上自然区分"结构"和"数据"，不会混淆。
