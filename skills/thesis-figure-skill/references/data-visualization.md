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

最常见的溢出：嵌入可视化下方的标签文字（如"Attention Map"）跑到了框线外面。原因是计算内容高度时忘了加标签的 ~0.3cm。**标签必须算在内容高度内。**

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

## 与常规框图混合使用

数据可视化元素通常嵌入在架构图内部（如信号处理流程的每个阶段包含一个迷你图），使用 `\begin{scope}[shift={(x,y)}]` 定位每个嵌入图的局部坐标系。

混合图的结构通常是：
1. 外层：常规框图布局（大框+箭头+标签）
2. 内层：每个大框内用 scope 绘制迷你可视化
3. 框之间的箭头和框内的坐标轴/数据完全独立，互不影响
