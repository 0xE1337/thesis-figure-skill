---
name: tikz-figure-code
description: |
  写出高质量、一次过编译、编辑安全的 TikZ/LaTeX 配图代码的工程基础技能。
  教 agent 用「按构造布局」(positioning/fit/chains/anchor) 而非「手填绝对坐标」，
  附 8 条硬约束、canonical 箭头、before/after 范例、一个静态检查入口 (lint.sh)。
  Use when: 写/审 TikZ 或 LaTeX 图代码、修图的排版/对齐/溢出/箭头问题、
  tikz layout、latex figure code、tikz 编译报错、CJK 中文图渲染成色块。
---

# TikZ Figure Code — 写对 + 编辑安全的工程基础

这是**确定性地基**：怎么写出编译干净、不重叠、改一处不崩的 TikZ 代码。
它**不**管"画什么图才美"——那是设计/编排层（见 [thesis-figure-skill](../thesis-figure-skill/SKILL.md)）的事。
本技能管的是：无论画什么，代码本身得**写对、扛得住编辑**。

> 一句话定位：thesis-figure-skill 决定**画什么**，本技能保证**怎么写不出错**。

## 为什么需要它（问题的根）

模型写 TikZ 的默认习惯是**"坐标凭感觉"**——`\node at (5.2, 3.1)`、`\fill rectangle (x0,y0)(x1,y1)`，
一格一格手摆。这是**业余写法**，导致两类必然的痛：

1. **盲写**：你写到第 800 行时不知道渲染出来什么样，碰撞/溢出/箭头不贴框只能编译后看图才发现 → 被迫进昂贵的"渲染→审查→修"循环。
2. **编辑即崩**：同一个间距/中心被手抄在多处（zone 边界、内容中心、箭头坐标、底栏…）。改一个 stage 宽度要同步 5 处，漏一处就崩——**而静态 checker 抓不到**（实测：一个加宽 hero 的编辑把 zone 压重叠、边框切穿内容，validator + overlap-checker 全报 0 硬 bug，只有看图才发现）。

**解法不是加更多检测，是换写法。** 专家写 TikZ 是**写一张约束图**（相对定位 + fit + matrix），
让布局引擎算位置——碰撞按构造不可能发生，图**correct by construction**，不是 correct-after-review。

证据：`references/examples/` 里同一张 5-stage pipeline，绝对坐标版 (BAD) 和按构造版 (GOOD)
渲染**视觉等价**；但施加同一个最自然的编辑（加宽 hero / 加长 label），BAD 崩、GOOD 自动重排。
见 `proof-edit-safety-hero-widen.png`。

## 核心原则：LAYOUT BY CONSTRUCTION，不是 BY COORDINATE

**作用域**：按构造纪律施加在**宏观骨架层**（模块/zone 彼此怎么放、怎么连）。
**嵌入 viz 内部**（热力图一格格、柱状图）可以继续局部手画——它自包含、坐标错了不级联——
但要用 `\begin{scope}[shift={(parent.center)}]` 挂到父节点 anchor，让它随父节点移动。

## 5 条 idiom（必须照做——散文指南传不了布局技能，照抄这些代码）

### ① 布局节奏只放一处
同一个间距/行高/列宽**只定义一次**，到处引用。永不把同一个数字抄在多处。
```latex
\newlength{\stagew}\setlength{\stagew}{4.5cm}   % 改一处，全图跟着变
\def\gap{0.5cm}
\tikzset{node distance=\gap}
```

### ② 模块用相对定位摆，不用绝对 `at (x,y)`
第一个锚定，其余 `right=of` / `below=of` 前一个。间距活在 `node distance` 一处。
```latex
\node[zone] (s1) at (0,0) {};
\node[zone, right=of s1] (s2) {};      % ✅ 间距由 node distance 决定
\node[zone, right=of s2] (s3) {};      % 加宽 s2 → s3 自动右移
% ❌ \node[zone] (s2) at (5,0) {};      % 手填 5 = 改 s1 宽度就得改这里
```
网格/表格用 `\matrix of nodes`，流水线用 `chains`——别手动给 x 加 2cm。

### ③ 连线走节点 anchor，永不重抄边界坐标 ← 单点最大收益
```latex
\draw[arrow] (s1.east) -- (s2.west);   % ✅ 任何重排下都不会错位
% ❌ \draw[arrow] (4.5,5) -- (5.0,5);   % 把 zone 边界又抄了一遍 = 改布局就断
```
**箭头引用节点，就永远不可能 misalign**。这一条单独就能消灭评审环里一大半 bug。

### ④ 容器用 `fit`，标签用 `text width`（换行）不用 `minimum width`（撑大）
```latex
\node[fit=(a)(b)(c), draw, rounded corners] {};         % zone 自动包住内容
\node[box, text width=3.2cm, align=center] {长标签会换行不会溢出};
% ❌ minimum width=3.2cm → 长标签把框横向撑大、顶破 zone
```
`text width` 让超长内容**换行**（保持框宽），`minimum width` 让框**长出去**（溢出邻居）。
前者把"碰撞 bug"（硬，必修）降级成"挤一点"（软，审美）。

### ⑤ 整体居中用 calc 中点，不手算
```latex
\coordinate (c) at ($(first.north west)!0.5!(last.north east)$);
\node[anchor=south] at ($(c)+(0,0.5)$) {标题};   % 行变宽，标题自动跟着居中
```

## 8 条硬约束（违反必失败——加载 `references/hard-constraints.md` 看全）

最高频的几条（很多是 CJK / xelatex 静默坑）：
- ⚠️ **CJK 节点上 `rotate=90`** → 渲成不可读色块。所有中文标注必须水平。
- ⚠️ **`\texttt{…中文…}`** → 报错。`\texttt` 只包纯英文代码。
- ⚠️ **xelatex 对缺失字体静默失败** → 编译后必须 `grep "Missing character" *.log`，非 0 = 字体没解析（常是 CJK）。
- ⚠️ **直线单段 `--` 上加 `rounded corners`** → 端点鬼影弧。只在 ≥2 段折线 / `|-` 用。
- ⚠️ **路径有弯折但没 `\usetikzlibrary{bending}`** → 弯路上箭头 tip 必然 mis-align。
- ⚠️ **`(A.south) |- (B.west)` 当 A.x 落在 B 的 x 范围内** → 横线穿过 B 内部 (pierce)。用 waypoint 绕开或换 anchor。

## Canonical 箭头（别手写 `-{Stealth[scale=X]}`）

用预定义 style，只调 `line width`（0.6/1.0/1.6pt 三档），tip 自动跟随。详见
`../thesis-figure-skill/references/tikz-template.tex` 的 6 个 canonical styles。铁律：
- **< 1.5cm 短箭头**必用 `arrow short`（tip 3pt），否则默认 6.5pt tip 把 stem 吃光 = "只剩个头"。
- **fan-out 分叉的 stub** 用 `fan_stub`（`shorten <=0pt`，紧贴 spine 无 gap），不用 `arrow`。
- **`\usetikzlibrary{bending}` 必加载**。

## 工作流：写 → lint → 看图

```bash
bash references/lint.sh figure.tex
```
一个入口跑完：① tikz-validator（编译前静态：微斜线/溢出/碰撞）→ ② xelatex 编译 →
③ missing-char 闸门 → ④ pdf-overlap-checker（硬 bug vs 候选分开报）→ ⑤ design-linter（advisory）。
退出码 0 = 无硬 bug，1 = 有硬 bug。

**checker 是地板不是天花板。** 它消灭便宜的 20%（编译错、重叠、已知坑），抓不到贵的 80%
（图记不记得住、跨面板数字自洽、新几何对不对）。**lint 过了仍必须亲眼看渲染 PNG**——
很多崩坏（zone 重叠、边框切穿内容）static 全盲，只有看图才发现。

## 何时用本技能 vs thesis-figure-skill

| 你要做的 | 用 |
|---|---|
| 写/审任何 TikZ 图代码、修排版/对齐/溢出/箭头 bug、CJK 渲染问题 | **本技能** |
| 把论文文案/参考图变成成品配图（设计 + 编排 + 视觉迭代 + skeleton 复用） | thesis-figure-skill（它在代码正确性层 compose 本技能） |

thesis-figure-skill 的 6 个 `example-skeleton-*.tex` 已全部按这 5 条 idiom 重写，是本技能最好的 worked examples。

## 按需加载

| 触发 | 文件 |
|---|---|
| 要看 5 idiom 的完整代码模式 | `references/by-construction.md` |
| 要看全部 8 条硬约束 + 修法 | `references/hard-constraints.md` |
| 要对照 before/after | `references/examples/`（BAD vs GOOD + 编辑安全证明图） |
| 要跑静态检查 | `references/lint.sh`（执行即可，不用 Read） |
