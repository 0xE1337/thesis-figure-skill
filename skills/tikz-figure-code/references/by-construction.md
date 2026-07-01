# 按构造布局 — 5 idiom 完整代码模式

核心命题：**写一张约束图，让布局引擎算位置**，而不是手填坐标然后靠编译看图修。
布局正确**correct by construction**，碰撞按构造不可能发生。

作用域提醒：这 5 条用在**宏观骨架**（模块/zone 彼此怎么放、怎么连）。嵌入 viz 内部
（热力图格子、柱状图）局部手画 OK，但要用 `\begin{scope}[shift={(parent.center)}]`
挂到父节点 anchor，让它随父节点移动（见 idiom ②ʹ）。

---

## ① 布局节奏只放一处（single source of truth）

**反模式**：同一个数字（stage 间距 5cm、stage-1 中心 2.25）被手抄在 zone 边界、内容中心、
箭头坐标、底栏、legend ——5 个互相独立的地方。改一处要同步 5 处，漏一处崩。

```latex
% ✅ 节奏集中定义
\newlength{\colw}\setlength{\colw}{4.5cm}
\newlength{\rowgap}\setlength{\rowgap}{1.2cm}
\def\gap{0.5cm}
\tikzset{node distance=\gap}
% 之后所有引用 \colw / \rowgap / node distance —— 改一处全图跟随
```

## ② 模块相对定位，不用绝对 `at (x,y)`

```latex
% ✅ 链式：第一个锚定，其余相对前一个
\node[zone] (s1) at (0,0) {};
\node[zone, right=of s1] (s2) {};
\node[zone, right=of s2] (s3) {};
% 加宽 s2（minimum width=6cm）→ s3/s4 自动右移，无需改任何坐标

% ❌ 绝对：
\node[zone] (s2) at (5,0) {};      % "5" = 改 s1 宽度就得手改这里
```

**网格用 matrix**（别写 N 个 `\node at`）：
```latex
\matrix[matrix of nodes, row sep=4mm, column sep=6mm,
        nodes={draw, minimum width=2cm}] {
  A & B & C \\
  D & E & F \\
};
```

**流水线用 chains**：
```latex
\begin{scope}[start chain=going right, node distance=5mm]
  \node[on chain] {输入}; \node[on chain] {处理}; \node[on chain] {输出};
\end{scope}
```

### ②ʹ 嵌入 viz 挂到父节点 anchor（让内部画法随 zone 移动）

```latex
\node[zone] (s1) at (0,0) {};
% 热力图用 LOCAL 坐标，整体 shift 到 s1 中心 → s1 移动它就跟着移动
\begin{scope}[shift={(s1.center)}]
  \def\cs{0.4}
  \foreach \i in {1,...,5}\foreach \j in {1,...,5}{
    \fill[...] ({(\j-3)*\cs},{(3-\i)*\cs}) rectangle ++(\cs,\cs);
  }
\end{scope}
```

## ③ 连线走节点 anchor，永不重抄边界坐标 ← 单点最大收益

```latex
% ✅ 引用节点 anchor —— 任何重排下都不会错位
\draw[arrow] (s1.east) -- (s2.west);
\foreach \a/\b in {s1/s2, s2/s3, s3/s4} \draw[arrow] (\a.east) -- (\b.west);

% ❌ 重抄坐标 —— 改布局就断
\draw[arrow] (4.5,5) -- (5.0,5);     % 把 zone 边界又抄了一遍
```

L 型连线（`|-` / `-|`）也用 anchor，但注意硬约束 #8（中段别穿障碍）。

## ④ 容器 fit，标签 text width

```latex
% ✅ zone 边框自动包住一组节点 —— 节点动，框跟着动
\node[draw, rounded corners, fit=(a)(b)(c), inner sep=4pt] {};

% ✅ 长标签换行（保持框宽）
\node[box, text width=3.2cm, align=center] (lbl) {很长的标签会自动换行不溢出};

% ❌ minimum width —— 长标签把框横向撑大、顶破 zone、压到邻居
\node[box, minimum width=3.2cm] {很长的标签把这个框撑出去};
```

**关键性质**：`text width` 把"碰撞 bug"（硬，必修）降级成"挤一点/多一行"（软，审美）。
即使 xelatex 文字度量有残余不可预测性，超长 label 也只是**换行**，不会**碰撞**。

## ⑤ 整体居中用 calc 中点

```latex
\usetikzlibrary{calc}
% 行的中点 = 第一个的左上 与 最后一个的右上 的中点
\coordinate (c) at ($(s1.north west)!0.5!(s5.north east)$);
\node[font=\Large\bfseries, anchor=south] at ($(c)+(0,0.6)$) {图标题};
% 行变宽（加 stage / 加宽 hero）→ 标题自动重新居中
```

---

## 编辑安全是怎么来的（把 5 条连起来）

施加同一个最自然的编辑——**加宽 hero stage**：
- 绝对坐标版：改 hero 的 x1 → 但 stage 4/5 的 x、inter-stage 箭头坐标、底栏 pitch、legend
  **都不会跟**，要手动同步 5 处，漏一处 → zone 重叠、箭头错位、边框切穿内容。**且 checker 全盲。**
- 按构造版：改 hero 一处 `minimum width` → stage 4/5 经 `right=of` 自动右移、箭头经 anchor 自动跟随、
  底栏经 `below=of` 自动跟过去、标题经 calc 中点自动重新居中。**一处编辑，全图重排，保持干净。**

对照 `examples/pipeline-absolute-coords-BAD.tex` vs `examples/pipeline-by-construction-GOOD.tex`
和 `examples/proof-edit-safety-hero-widen.png`。
