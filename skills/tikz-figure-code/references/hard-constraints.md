# 硬约束 — 违反必失败

这些不是建议，是**地雷**。25 批 157 张图踩出来的，每一条都对应一次真实的崩图。
很多是 xelatex + CJK 的**静默坑**（不报错，但渲染错）。

## CJK / 字体类（最隐蔽，因为 xelatex 不报错）

### 1. CJK 节点上 `rotate=90`（或任意 rotate）→ 不可读色块
```latex
% ❌ \node[rotate=90] {中文标签};     % 渲染成一团糊掉的色块
% ✅ 所有中文标注保持水平；竖排需求改用多行水平堆叠或换布局
```

### 2. `\texttt{…中文…}` → 报错
`\texttt` / 等宽字体只对纯英文代码有效。中文用正常 CJK 字体。
```latex
% ❌ \texttt{加密函数}      % Missing character / 报错
% ✅ \texttt{Enc()}  或  普通节点写「加密函数」
```

### 3. xelatex 对缺失字体**静默失败** → 必须 grep
xelatex 找不到字形时**不报错**，直接渲染成空白/豆腐块。编译后**强制**：
```bash
grep "Missing character" figure.log     # 必须 0 行，非 0 = 某字体没解析
```
常见诱因：`\setCJKmainfont` 指向本机没有的字体（如 Linux 上写 PingFang SC）。
编译前探测：`fc-list | grep -qi "PingFang SC" || echo "改 setCJKmainfont 为本机字体"`。

### 4. `ucharclasses` → 中英混排频繁 Missing character
tikz 节点内中英混排时 `ucharclasses` 会乱。**禁用**。用 ctex / fontspec 的常规 CJK 设置。

### 5. `ctex` 不可用时的回退
编译前 `kpsewhich ctex.sty`；不可用切方案 B：`fontspec` + `\setCJKmainfont`（需 xeCJK）。

## 路径 / 箭头几何类

### 6. 直线单段 `--` 上加 `rounded corners` → 端点鬼影弧
PGF 官方手册原话："very short line segments → rounding causes inadvertent effects"。
```latex
% ✅ 只在显式 ≥2 段折线用：
\draw[arrow, rounded corners=5pt] (A) -- (corner) -- (B);
\draw[arrow, rounded corners=5pt] (A) |- (B);          % |- 隐式含 corner
% ❌ 直线禁加：
\draw[arrow, rounded corners=5pt] (A) -- (B);          % 端点产生鬼影弧
```

### 7. 弯折路径但没 `\usetikzlibrary{bending}` → tip mis-align
任何弯路上的箭头 tip 会歪。**`bending` 必加载**。

### 8. `(A.south) |- (B.west)` 当 A.x ∈ [B.x0, B.x1] → 横线穿 B 内部（pierce）
PGF 不做 obstacle-aware routing，`|-` / `-|` 的中段会直接穿过障碍。
```latex
% ❌ (msg.south) |- (hero.west)  当 msg.x 落在 hero 的 x 范围内 → 横线画进 hero 内部
% ✅ 修法 1：named waypoint 绕开
\coordinate (wp) at (B.x0 - 0.5cm, B.center.y);
\draw[arrow] (A.south) |- (wp) -- (B.west);
% ✅ 修法 2：换 anchor 让箭头从 B 上方直接接入
\draw[arrow] (A.south) -- (B.north);
```
`pdf-overlap-checker.py` 的 `line-through-node` 检测能抓到这类（但对热力图/矩阵会误报，需 triage）。

## 短箭头 / fan-out（来自 canonical 箭头规则）

### 9. < 1.5cm 短箭头用默认 `arrow` → "只剩个头"
默认 `arrow` 的 tip = 5pt + 1.5×line_width = 6.5pt，加 shorten，一条 0.5cm 短箭头 stem 只剩 5.5pt。
**< 1.5cm 必用 `arrow short`**（3pt tip）。

### 10. fan-out 分叉 stub 用 `arrow` → spine 和 stub 间留 1pt gap（断连感）
fan-out（1 source → N targets）：spine 用普通 `\draw`，**stub 用 `fan_stub`**（`shorten <=0pt` 紧贴 spine）。

## 输出格式

### 11. 只用 TikZ 或 draw.io，禁止 Python/matplotlib 替代
学术图嵌入 `\input{figure.tex}` 在公式渲染、矢量缩放、风格统一上都优于 `\includegraphics{fig.png}`。
复杂嵌入 viz 仍用 TikZ 原生（`\foreach` 画 cell / `pgfplots` / `\draw` 手画 patch）。仅当用户明确要求 Python 才用。

### 12. 默认 light background，dark theme 需用户明确请求
学术论文标准是 white/light bg；dark theme 与正文风格断裂。
"≥5 种 zone tone"指 zone 浅色背景 + box 中饱和度，**不是**整图反转色。
