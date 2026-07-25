# 经验沉淀与基线参数

> **何时加载**：步骤②加载专项规则时，同时加载本文件。
> **本文件 = 验证过的最佳参数（表格）+ 不被全局规则覆盖的踩坑教训（清单）**
>
> （原 `evolution.md` + `experience-log.md` 已于 2026-03 合并入本文件，**不再单独存在**——不要去 Read 这两个旧路径。）
> **写入规则**：只追加经过验证的事实，不写未确认猜测。如果按经验操作失败，更新或删除该条。
> **基线只升不降**：发现更优参数才更新，被证伪的不删除而是标注适用范围。

---

## Part 1: 已验证基线参数

> **本表是连线几何/间距常量的唯一真相源（SoT）**：tikz-global-rules.md / geometry-math.md / SKILL.md 只引用本表的值，不再各自写死数字。改参数只改这里。
> 箭头样式（tip / shorten / line width）的可执行 SoT 是 `tikz-template.tex` 的预定义 style（`arrow` / `arrow short` / `residual` 等）——本文件只记录数值与理由，**代码以模板为准**。

### 通用基线（所有 TikZ 图适用）

#### 间距

| 参数 | 基线值 | 说明 |
|------|--------|------|
| 同层相邻框 x 间距 | ≥ 1.5cm | < 1.0cm 必重叠 |
| 上下相邻框 y 间距 | ≥ 1.2cm | 用 `below=1.2cm of` |
| zone 到最外层内容 padding | 0.8-1.0cm | > 1.5cm 浪费, < 0.5cm 虚线切文字 |
| zone 标题与首行内容间距 | ≥ 0.8cm | 标题框 ~0.4cm + 空白 ~0.4cm |
| 图例框与最近内容 | ≥ 0.5cm | 图例放所有 zone 外部下方居中 |

#### 箭头

> **不再调 `Stealth scale`**——2026-05-18 深度调研后已被 `tikz-template.tex` 的 canonical
> `arrow/.style` 取代。tip 形状通过 `length=⟨dim⟩ ⟨line_width_factor⟩` + `width'` + `bending`
> library 自动跟随 `line width`。**只调 line width 三档**，禁止手写 `-{Stealth[scale=X]}`。
> 详见 lessons.md Part 2 的 "[通用] 箭头/连线 — 深度调研后的 canonical 模板"。

| 参数 | 基线值 | 说明 |
|------|--------|------|
| line width 选档 — 主流程 | 1.0 pt | canonical `\draw[arrow]` 默认值 |
| line width 选档 — 强调主线 | 1.6 pt | canonical `\draw[arrow thick]` |
| line width 选档 — 辅助/dashed | 0.6 pt | canonical `\draw[arrow thin]` / `residual` |
| 弯折点到目标框距离 | ≥ 1.5cm | `rounded corners=5pt` 弧线吃掉 ~0.5cm |
| 连线弯折圆角 | `rounded corners=5pt` | 唯一值；直线段禁加（鬼影弧）|
| 树状扇出横线到目标框 | ≥ 1.5cm | 太近"刚拐过来就到了" |
| ⊕/⊗ 小汇合节点两侧间隙 | ≥ 0.4cm | 需要可见箭身 |

#### 文字

| 参数 | 基线值 | 说明 |
|------|--------|------|
| 最小可读字号 | `\scriptsize` | 300dpi 验证 |
| 框内文字 | `\footnotesize` | 有空间用 `\small` |
| 标题文字 | `\small\bfseries` | |
| 标签背景 | 默认透明 | 仅与生命线重叠时用 `fill=white, fill opacity=0.85` |

### 数据可视化混合图

#### 坐标轴标签防重叠

| 参数 | 基线值 | 说明 |
|------|--------|------|
| x 轴标题 yshift | -10pt | 防止与 x 轴刻度值重叠 |
| y 轴标题 xshift | -15pt | 防止与 y 轴刻度值重叠 |
| 刻度值到轴线距离 | ≥ 3pt | |
| 轴标题到刻度值间隙 | ≥ 0.3cm | |
| 长中文 y 轴标题（≥4 字） | 改水平显示 | 旋转后 bbox 提取不准，仍易重叠 |

#### 嵌入可视化尺寸

| 参数 | 基线值 | 说明 |
|------|--------|------|
| 柱状图容器最小宽度 | ≥ 5cm | |
| 热力图容器最小尺寸 | ≥ 4cm × 4cm | |
| 容器内 top padding | 0.5cm（标题） | |
| 容器内 bottom padding | 0.5cm（含 x 轴标签） | |
| 可视化占框面积比 | 60-75% | 太满溢出，太少浪费 |
| 面板/英雄模块标题栏高度 | ≤ 面板总高 20%（≤ 0.8cm） | 标题用 `\small\bfseries` 一行，不要大背景色块 |

### 时序交互图

| 参数 | 基线值 | 说明 |
|------|--------|------|
| 参与方间距 | 5.0-5.5cm | 4 方用 5.5cm，3 方用 5.0cm |
| 生命线线型 | `densely dashed, color!80` | !60 在浅背景上不可见 |
| 激活条宽度 | 0.45cm | 0.3cm 在 PNG 中几乎不可见 |
| 消息箭头 y 间距 | ≥ 1.0cm | 太密标签挤 |
| 消息标签颜色 | 统一 `black!80` | 不要五颜六色 |
| 阶段背景 opacity | 0.15-0.25 | 太深遮挡生命线 |

### 三栏映射图

| 参数 | 基线值 | 说明 |
|------|--------|------|
| 三栏 x 中心 | 0, 7, 14 | 栏宽 ~4cm，栏间 ~3cm |
| 跨栏 rail x 坐标（左间） | 3.0, 4.2 | 两条 rail 间距 ≥ 1.2cm |
| 跨栏 rail x 坐标（右间） | 10.2, 11.3 | |
| 栏内节点 y 间距 | 1.6cm | |
| 连线圆角 | 见通用基线（`rounded corners=5pt`）| 不再单列，避免漂移 |

### 几何/数学示意图

| 参数 | 基线值 | 说明 |
|------|--------|------|
| 坐标系范围 | ±2.5 到 ±3.0 | 给标注留空间 |
| 网格线 | `very thin, gray!20` | 不能抢主角 |
| 公式框宽度余量 | 公式宽度 + 1.0cm | 两侧各 0.5cm |
| 标注到最近数据点 | ≥ 1.0cm | 密集区不放标注 |
| 图例背景 opacity | 0.93 | 白底半透明 |

### 多实例汇聚图

| 参数 | 基线值 | 说明 |
|------|--------|------|
| 并排实例间距 | 4.5-5.0cm | 3 实例用 4.5cm |
| 汇聚树横线 y | 目标框顶 + 1.5cm | |
| 扇出树横线 y | 目标框底 - 1.5cm | |
| 监控虚线 rail x | zone 外侧 ≥ 1.0cm | 不穿越内容区域 |
| 树状分支垂直段 | 用 `let \p1` 提取精确 x | 杜绝微斜线 |

### 分层架构图

| 参数 | 基线值 | 说明 |
|------|--------|------|
| 层间 y 间距 | 3.0-4.0cm | 含 zone 标题空间 |
| 同层框最大数量 | 4-5 个 | 超过则分两行 |
| 跨层连线 rail x | zone 外侧左 -1.5cm | |
| 反馈虚线 rail | 独立于其他 rail | 不与实线共享 |

### 复刻任务基线（参考图测量）

| 维度 | 必测量 | 注意 |
|------|--------|------|
| 画布宽高比 | 参考图像素 width:height | TikZ 画布严格匹配，凭感觉会偏差 10-20% |
| zone 占比 | 各 zone 占总宽/总高的百分比 | 不要"差不多就行" |
| 框宽高比 | 参考原图（通常扁宽 2:1~3:1） | 默认不要正方形 |
| 留白率 | 元素间距占区域高度 20-30% | 元素占 zone 面积 60-70%，不要填满 |
| 嵌入可视化占框面积 | 50-60%（扣 padding 后） | 不要缩在角落 |

---

## Part 2: 不被全局规则覆盖的踩坑教训

> 已在 `tikz-global-rules.md`、本文件 Part 1 的基线表、`tikz-validator.py`/`pdf-overlap-checker.py` 中
> 显式编码的规则（锚点方向、微斜线、箭头方向反转、border 不足、padding 过大、标签未居中、zone
> 切文字、zone 未覆盖内容、⊕ 间距、消息标签颜色、轴标签防重叠等）**不重复记录在这里**。

### 编译/包/字体

#### [通用] - pgfonlayer 环境名
- **问题/发现**：背景层环境名是 `\begin{pgfonlayer}{background}`，不是 `\begin{pgfonbackgroundlayer}`。后者会编译报错但仍生成异常 PDF。
- **解决方案**：始终用 `\pgfdeclarelayer{background}` + `\pgfsetlayers{background,main}` + `\begin{pgfonlayer}{background}`。
- **发现日期**：2026-03-28

#### [三栏映射图] - zone style 在 pgfonlayer 内失效
- **问题/发现**：`\begin{pgfonlayer}{background}` 内的 `\node[zone, fit=...]` 如果 `zone` style 含 `inner sep` 等参数，可能导致 zone 框不显示。
- **解决方案**：pgfonlayer 内直接内联 style（`\fill[dashed, thick, rounded corners=8pt, inner sep=15pt, ...]`），不依赖预定义的 `zone` style。
- **发现日期**：2026-03-28

#### [通用] - 双方括号符号需 stmaryrd
- **问题/发现**：`\llbracket` / `\rrbracket`（⟦⟧）需要 `\usepackage{stmaryrd}`，否则报 "Undefined control sequence"。
- **解决方案**：密码学/形式化验证领域含 ⟦⟧ 时在 preamble 加 `\usepackage{stmaryrd}`。
- **发现日期**：2026-03-29

### 视觉层次/绘制顺序

#### [时序图] - 生命线最后绘制避免被遮挡
- **问题/发现**：TikZ 按代码顺序绘制，后画的在上层。生命线虚线被阶段背景 fill、combo 框、注释框遮挡。
- **解决方案**：所有 `\draw[lifeline=...]` 移到 `\end{tikzpicture}` 前最后位置。
- **发现日期**：2026-03-29

#### [时序图] - 消息标签默认不加白色背景
- **问题/发现**：`tag` style 用 `fill=white` 在生命线上会产生突兀的白色方块。
- **解决方案**：`tag` 默认无背景。仅当标签确实与生命线重叠且影响可读性时，才加 `fill=white, fill opacity=0.85`（半透明）。多数消息标签放在箭头上方不需要白底。
- **发现日期**：2026-03-29

#### [draw.io] - 箭头线覆盖文字（z-order 问题）
- **问题/发现**：draw.io 蓝色箭头线显示在模块文字上方，文字被遮挡。
- **解决方案**：XML 中先定义 edge，后定义 vertex——背景 < 连线 < 框体/文字。
- **发现日期**：2026-03-29

### 几何/装饰精度

#### [几何图] - 大括号方向搞反
- **问题/发现**：注意力机制图中 Q/K^T/V 的大括号开口方向不对。
- **解决方案**：`{` 开口朝右标注右侧，`}` 开口朝左。不确定时直接去掉改用文字标注——少一个有问题的装饰比多一个好。
- **发现日期**：2026-03-29

#### [几何图] - 辅助标注箭头不要死板指向正中心
- **问题/发现**：Merkle 树"兄弟节点"标签的箭头从左下方斜着插上去看起来僵硬。
- **解决方案**：辅助标注箭头可以指向 `.south west` 或 `[xshift=-3pt]node.south`，不需要精确对准正中心。像人手画一样自然。
- **发现日期**：2026-03-29

#### [通用] - 同类线条共出发点更优雅
- **问题/发现**："强制不同锚点出发"规则反而让同色同型同方向的两条线变扭曲。
- **解决方案**：同类型线可以共享出发点——看起来更像"有意分发"。只有不同类型线（实 vs 虚）才需分开。规则不是死的，美感才是最终裁判。
- **发现日期**：2026-03-29

### 连线路径

#### [分层架构图] - 反馈虚线绝不能穿过文字
- **问题/发现**：反馈虚线穿过多个层的文字标签，审查 agent 未发现。
- **解决方案**：虚线/反馈线必须逐段检查路径上有没有文字。**哪怕只穿过一个标签也必须改路径绕开**——虚线穿文字是最明显的排版问题。
- **发现日期**：2026-03-29

#### [通用] - "能直就直"——对齐节点不要加不必要弯折
- **问题/发现**：源和目标完全垂直对齐，但箭头还是画了 L 型弯折。人一看就觉得多余。
- **解决方案**：画连线前先看源/目标 x/y 是否对齐。对齐则直线，不对齐才弯折。**每次弯折必须有理由（绕障碍物）**。
- **发现日期**：2026-03-29

#### [通用] - 弯折后线段太短导致箭头断在弯角
- **问题/发现**：弯折点紧挨着箭头尖，看起来像箭头断在了弯角。
- **解决方案**：弯折点到目标框 ≥ 1.5cm（统一值，见 Part 1 基线表）。空间不够则提前弯折让最后一段够长。
- **发现日期**：2026-03-29

#### [通用] - 标签有空间却还是重叠放置
- **问题/发现**：Yes/No 标签和线重叠、hub-spoke 标签和框重叠——明明旁边有空白。
- **解决方案**：放每个标签时必须看周围——有空白就挪过去。"有空间却重叠"是不应该的错误。
- **发现日期**：2026-03-29

#### [通用] - 箭头指向空气（没"够到"目标）
- **问题/发现**：自调用弧太短，终点在激活条外。
- **解决方案**：箭头终点必须落在目标元素边框上。目标太小则**扩大目标**（加宽激活条、加长框体），不要缩短箭头。
- **发现日期**：2026-03-29

#### [英雄模块] - 宽框出箭头不要用 .east
- **问题/发现**：很宽的 hero 模块到右上/右下方目标的箭头从 `.east` 出发水平拉很远，像被强行拉过去。
- **解决方案**：从 `.north east` 或 `.south east` 出发向上/下再转。判断：从 `.east` 出发的箭头水平段 > 模块宽度 1/3 就换锚点。
- **发现日期**：2026-04-02

### 数据可视化细节

#### [数据可视化] - 中文标签自动换行字间距异常
- **问题/发现**：text width 强制换行中文 → "本 文 / 方 法" 字间距异常。
- **解决方案**：中文标签用 `\\` 手动换行或缩短为英文（`Ours`），不依赖 text width。
- **发现日期**：2026-04-02

#### [数据可视化] - 旋转文字居中需要 anchor=center
- **问题/发现**：`rotate=90` 文字用 `anchor=south` 时不居中、有偏移。
- **解决方案**：旋转文字要居中时用 `anchor=center`，不用 `south/north`。
- **发现日期**：2026-03-31

#### [数据可视化] - 旋转 y 轴标签 + 长中文，bbox 检测不准
- **问题/发现**：旋转 90° 的"准确率(%)"和刻度值重叠，pdf-overlap-checker 因旋转 bbox 提取不准未检出。
- **解决方案**：(1) 旋转标题统一 `xshift=-18pt`；(2) 长中文标题（≥4 字）改为不旋转、放轴上方水平显示。
- **发现日期**：2026-04-02

#### [数据可视化] - 迷你可视化标注不要用插值定位
- **问题/发现**：GAT 图注意力小图中数值标签放 edge 中间点（0.5-0.7 插值），刚好落在圆圈边缘上。
- **解决方案**：标注用 anchor 定位放外侧（如 `anchor=east at (node)+(-0.18,0)`），不用插值定位——插值容易落在元素边缘。
- **发现日期**：2026-03-31

### 树状/复杂拓扑

#### [通用] - 树状分叉处线段断连和"空心方块"
- **问题/发现**：树状一分多用多个独立 `\draw` 时，每段继承全局 `shorten >=2pt`，交叉点出现可见间隙。分叉点用 `\node[circle/rectangle]` 会渲染为"空心方块"。
- **解决方案**：(1) 主干+横杆用**一条连续** `\draw[thick]`（不带 arrow、不带 shorten）；(2) 只有最终分支用 `\draw[arrow]`（继承 shorten）；(3) 分叉点用 `coordinate` 而非 `\node`——coordinate 不渲染任何形状。
- **发现日期**：2026-04-03

#### [通用] - 跨层连接区域拥挤
- **问题/发现**：树状分叉区多条线（gRPC、背书、准入验证）挤同一通道交叉重叠。
- **解决方案**：(1) 同一通道最多 3 条线；(2) 多条线同方向时用不同 x 的 rail（间距 ≥ 1.0cm）；(3) 同类连接（都是 gRPC）合并为一条线 + 标签。
- **发现日期**：2026-04-03

#### [通用] - 旋转文字侵入相邻区域
- **问题/发现**：联邦学习图 "Broadcast w_global" 竖排文字碰到右侧雷达图区域。旋转文字实际宽度难预估。
- **解决方案**：放置后检查旋转文字的四角是否侵入相邻元素。宁可多留 0.5cm 间距。
- **发现日期**：2026-03-31

### 信息密度

#### [通用] - 小标注过多导致全图重叠（设计野心过度）
- **问题/发现**：为追求信息密度在每个框旁加协议标注（.sol、sDfx invoke、inter blockchain 等），导致 7 处以上重叠。
- **解决方案**：(1) 小标注只在 ≥ 0.5cm 空白区添加；(2) 一个框旁最多 1 个外挂标注；(3) 自问"删掉所有小标注读者能理解吗？"——能就说明标注是可选的；(4) **干净 > 塞满**。
- **发现日期**：2026-04-03

#### [通用] - 同类功能箭头粗细不一致
- **问题/发现**：zkSNARK 图三个功能相似的箭头（Commit、Prove、Prover→Verifier）分别用 scale=1.2/1.5/0.8。
- **解决方案**：同类功能箭头**必须**统一 scale 和 line width——全局 style 中的 scale 值要适配最短的那条箭头。
- **发现日期**：2026-03-31

### 美感守恒

#### [迭代] - 修复一处不能破坏其它对齐/平行
- **问题/发现**：迭代修改中红色虚线和蓝色实线原本平行（美观），修改后不再平行（退步）。审查 agent 未发现这种退步。
- **解决方案**：每次迭代后检查修改是否破坏了已有的好效果（对称性、平行、间距均匀度）。**不允许修复一个 bug 引入另一个审美问题**。
- **发现日期**：2026-03-29

### 连线/箭头精度（Round 11 用户实测发现）

#### [通用] - Fan-out 多线必须用 tree pattern，禁止"扫帚式"散射
- **问题/发现**：MLP 节点扇出 3 条线到 3 个 task heads，3 条线从 `(fanout)` 同一点用 `(fanout) -- ++(0.55, 0) -- (target_y) -- (target.west)` 写，结果在 junction 附近 3 条线以不同角度散开，视觉上像"扫帚"——线段相互交叉、近距离干扰，读者要费力分辨。
- **禁止模式**：`(fanout) -- ++(0.55, 0) -- (target_y) -- (target.west)` 这种单 `\draw` 隐式斜线，3 条会撞角。
- **解决方案**：tree pattern (trunk + spine + stubs)。**完整代码模板和细则见** `tikz-global-rules.md` §"一对多分叉连线（树状扇出）" 和 §"多源汇聚→多目标扇出（沙漏树）"。
- **发现日期**：2026-05-16（MMAlign Round 11 用户视觉反馈）

#### [通用] - Junction dot 不被箭头 tip 戳——所有 dot-as-connector 场景
- **问题/发现 (Round 11, fan-in 场景)**：MLP → fanout dot 段用了 `arrow_main` 自带 `-{Stealth}` tip，箭头尖戳进 dot，视觉打架。
- **问题/发现 (R3-100 Batch 3, fan-out 起点)**：fig28 Mask R-CNN Box head 的 Y-fork: FC → dot → {class, bbox}，FC 出来那段水平箭头的 tip 戳进 dot——sub-agent 把 "junction dot 不被 tip 戳" 仅理解为 fan-in，忽略了 fan-out 起点也是同一规则
- **核心规则**：dot 周围**所有相邻线**都用 `\draw[thick, color=..., line width=...]` **不带** `-{Stealth}` tip，**无论 dot 是 fan-in 汇合还是 fan-out 起点**。tip **只**画在最终到达可见 target box (有 border) 的那一段。
- **dot 本身**：`\node[circle, fill=..., minimum size=4pt]`
- **适用**：fan-in、fan-out、Y-fork、T-junction、双向分流、所有 dot-as-connector 场景
- **E2 已强化**：覆盖 fan-out 起点的 dot（见 checklist）
- **发现日期**：2026-05-16 / 2026-05-18（Y-fork case 补充）

#### [通用] - 容器标题不能用 fill 嵌在容器边框上
- **问题/发现**：Hero 框标题用 `fill=acaOrangeFill!50, inner sep=2pt` 嵌在 hero 顶部边框处，白底盖住了橙色边框圆角，视觉上像 hero 框被"咬了一口"。
- **解决方案**：容器（zone/hero）标题**完全挪到容器外的白空间**（如 `at (center_x, top_y + 0.15)` anchor=south），**不要 fill**。这样：
  - 容器边框完整闭合
  - 标题可读性更好
  - 不破坏容器视觉完整性
- **发现日期**：2026-05-16

#### [通用] - 箭头 tip 刺入目标框：shorten 数值取决于端点类型

> ⚠️ **以下表格是 2026-05-16/17 历史经验值，已被 canonical template 取代**。
> 当前 `tikz-template.tex` 的 `arrow/.style` 使用 `shorten >=2pt`（TeX Live 2024 实测，
> 配合 `bending` library + `length=⟨dim⟩ ⟨line_width_factor⟩` 自动跟随 line width，
> 不再按端点类型分挡）。**冲突时以 `tikz-template.tex` 为准**——
> 不要回到手调 shorten >=6pt 的旧路径。本表保留作为历史教训背景，不作为执行依据。

- **问题/发现 (Round 1, 2026-05-16)**：节点图里 `shorten >=2pt` 配合 `Stealth[scale=1.1]` 端点指向 `node.west` 时，tip 出现在节点框内部。
- **问题/发现 (Round 2, 2026-05-17)**：Sequence 图里 `shorten >=6pt` 又**反过来**：指 Prover 等裸生命线时 tip 在生命线左侧 6pt 处悬空，看着像断线"线不够长"。
- **历史解决方案——按端点类型分**（已被 canonical template 取代）：
  | 端点类型 | shorten >= | 端点表达 |
  |---|---|---|
  | **节点图：node.west / node.east**（节点有可见边界）| **6pt** | `(target.west)` |
  | **Sequence: 激活条边缘**（命名节点的可见边）| **2pt** | `(actvVAuth.west &#124;- 0, y)` |
  | **Sequence: 裸生命线**（dashed 线无填充）| **2pt** | `(P.south &#124;- 0, y)` |
- **关键认识**：`shorten >=` 不是万能值。**端点是否有可见边界**决定数值——有边界（节点边、激活条边）需要更大 shorten 让 tip 在边外；无边界（裸生命线）小 shorten 让 tip 紧贴线。
- **当前 canonical 行动**：用 `tikz-template.tex` 的 `arrow/.style`，不要手写 shorten 数值。Sequence 图特殊端点（裸生命线）已被 `arrow short/.style` 覆盖（tip 3pt + shorten >=1pt）。
- 模板里 01/02/04/05/06 用 6pt（节点端点）；03-sequence 用 2pt（激活+生命线混合，端点用 `actv.east/.west` 或 `lifeline.south`）。
- **发现日期**：2026-05-16 / 2026-05-17（Round 2 细化）

#### [通用] - 双向箭头（contrastive、bidirectional flow）必须两端都有 tip
- **问题/发现**：MMAlign 对比损失 L_con 用 `arrow_contrast/.style={-{Stealth[scale=0.8]}, ...}` 只在一端有 tip，但 contrastive loss 语义上是双向的。视觉上看像单向流，误导读者。
- **解决方案**：表示双向/对称关系的箭头用 `{Stealth[scale=0.8]}-{Stealth[scale=0.8]}` 两端都画 tip。或者画两条独立单向箭头形成 ↔ 形式。
- **发现日期**：2026-05-16

### 并行 100 张测试发现（R3-100 批次，2026-05-17）

> 10 轮 × 10 并行 sub-agent 测试中浮现的新教训。命名 R3-XX 对应批次内第 XX 张图。

#### [密集架构] - 密集子块禁用箭头，用视觉触底+堆叠表达"流"
- **问题/发现 (R3-1 ResNet, 5 轮收敛)**：ResNet 类密集架构图有 50+ 子块（4 stages × 多个 residual blocks）。相邻子块间用 `shorten >=6pt` 箭头表达"数据流"时，箭头几乎与边框重合或刺入框；整图被箭头噪音淹没，读者看到的是箭头海而非架构。
- **解决方案**：
  - **子块紧贴排列**（视觉触底，gap < 1pt 或无 gap），**不画箭头**。读者从空间相邻+从左到右的阅读顺序自然推断"流"。
  - 只在**阶段间**（stage1 → stage2 这种粗粒度边界）画箭头，最多 3-5 条。
  - 适用：ResNet、DenseNet、EfficientNet 等密集 backbone；不适用：Transformer encoder（block 数少，箭头清晰可读）。
- **关键认识**：箭头是表达连接的工具，不是"数据流"的唯一表达。**相邻+阅读顺序**本身就是流。
- **发现日期**：2026-05-17

#### [fanout 拓扑] - Zone 标题在垂直 fanout 时不能放 zone 顶部，必须挪左侧空白栏
- **问题/发现 (R3-35 Threshold BLS, 5 轮收敛)**：BLS threshold 签名图里，3 个签名者垂直 fanout 进 aggregator zone。zone 标题（"Aggregator"）默认放 zone 顶部 anchor=north，结果 fanout trunk + spine 从 zone 顶边进入时压在标题下方，dot 与文字垂直撞角。
- **解决方案**：fanout 主轴穿过 zone 顶/底时，zone 标题挪到 **zone 西侧外的空白栏**：
  ```latex
  \node[anchor=east, font=\small\bfseries, rotate=90]
      at ($(zone.west) + (-0.15, 0)$) {Aggregator};
  ```
  或正常水平排版在 zone 西侧（如果空间允许）。
- **判断规则**：fanout 主轴（trunk + spine）的垂直方向 ⊥ zone 哪条边，标题就不能在那条边上。
- **发现日期**：2026-05-17

#### [三栏映射图] - 跨栏箭头标签放起点一侧或紧贴线，不要默认居中
- **问题/发现 (R3-8 Pretrain→Finetune→Eval, 4 轮收敛)**：三栏映射图的跨栏箭头（如 "downstream task"、"frozen weights"）标签 `pos=0.5` 居中时，刚好落在下一栏的 zone 边框（橙色虚线 `acaOrangeLine`）上撞色重叠。3 次迭代调整 pos 才避开。
- **解决方案**：跨栏箭头标签默认放法：
  - **起点一侧同栏内部**：`node[midway, above, pos=0.2]` — 标签在起点栏的栏内白空间，远离任何 zone 边线
  - 或**紧贴箭头线上方/下方**：`above=2pt` / `below=2pt`，垂直离 zone 边线 ≥ 3mm
  - **禁止**：默认 `pos=0.5` 居中（极易撞分栏线）
- **预防**：标签放置后视觉评审必看"标签是否与任何 zone 边线/分隔线距离 < 3mm"。
- **发现日期**：2026-05-17

#### [元 / 语义核查] - 数学/几何图：Agent 应核查文案坐标是否满足方程
- **问题/发现 (R3-38 椭圆曲线点加, 2 轮，质量超预期)**：椭圆曲线点加 P+Q=R 示意图，原文案给的 P/Q/R 坐标**不在指定曲线上**（数学错误）。Agent 在第二轮绘制前发现坐标与方程 `y²=x³+ax+b` 不一致，重新计算了曲线上的真实点。
- **解决方案**：画数学/几何/密码学示意图时，agent 在绘制前**必须核查**：
  - 文案给的坐标/参数**是否满足声明的方程或约束**
  - 几何关系（"垂直"、"切线"、"中点"等）**是否成立**
  - 不一致时**先纠正再画**，并在交付时说明：例如 "原文案 P=(2,1) 不在 y²=x³+x+1 上（实际 y²=11 而非 1），已改为 P=(0,1)"
- **关键认识**：这不是"超出任务范围"，是**质量保证的一部分**。复刻一张错误的图等于扩散错误。
- **适用**：几何示意、椭圆曲线、复平面图、向量空间、相图、力学示意等"坐标/参数必须满足某方程"的场景。
- **发现日期**：2026-05-17

### R3-100 Pilot 主 agent 三遍复审发现（2026-05-17）

> 主 agent 对 10 张 sub-agent 自审通过的图做 3 遍审查后发现的盲区。这些问题 sub-agent 的 ④.5 视觉评审**全部漏过**，但用户/主 agent 一眼能看出来 — 提示视觉评审清单需要加强。

#### [通用] 自由浮动 annotation / callout 必须有 leader line 引到具体元素
- **问题/发现 (R3-100 主 agent 复审)**：
  - fig07 ASR "Masked Self-Attn + Cross-Attn + FFN" callout 浮在 decoder 右边没引线
  - fig08 ECDSA 右栏 "Shamir SSS:" / "Paillier HE:" / "ECDSA combine:" 三段说明仅靠 y 对齐隐式关联
  - fig10 突触图 1-6 步骤编号在右栏纯文字描述，没有任何 leader 连到 anatomical 特征
- **解决方案**：所有**不直接相邻**的 annotation / callout / step number 必须用 dotted 或 dashed leader line 引到具体元素：
  - Hero substructure 展开 → dotted leader 从原模块 `.south` 到展开 panel `.north`
  - 多步骤解剖图 → 每编号 leader 连到对应特征，或编号直接放特征旁（≤ 0.3cm）
  - 右栏说明文字 → dotted leader 到对应模块
- **禁止**：自由浮动文字 + "靠 y 对齐推测关联"。这是读者认知负担最大的失败模式
- **发现日期**：2026-05-17

#### [时序图 / 多方协议] 多目标广播（1-to-N）不能用单条双箭头曲线
- **问题/发现 (R3-100 主 agent 复审, fig03 PSI)**：消息 3 "MPC 协同计算" 用一条横跨 Alice-Bob 的弧线，**两端都带箭头 tip**。读者无法分辨："Verifier 广播给 Alice+Bob"还是"Alice ↔ Bob 双向交互"
- **解决方案**：1-to-N 广播必须用以下两种之一：
  - **方式 A (fork)**：源画 fork dot → N 条独立单向箭头到 N 个目标
  - **方式 B (独立)**：源直接画 N 条独立单向箭头分别到 N 个目标
- **禁止**：单条双箭头曲线表达广播 — `{Stealth}-{Stealth}` 双头曲线**专属于 ↔ 双向交互**，不可挪用
- **发现日期**：2026-05-17

#### [通用] Hero substructure 必须真正"独一无二"，不要选通用结构做 hero
- **问题/发现 (R3-100 主 agent 复审)**：
  - fig01 ViT 选 Stage 3 做 hero 展开 W-MSA — 但 4 个 stage 的 W-MSA 内部**完全一样**
  - fig07 ASR 选 "Layer 1 expanded" — 但 6 层 Transformer encoder 内部**全都一样**
- **错误模式**：从一组相同结构的多个 instance 里随机选一个标"Stage N 内部"或"Layer N expanded"
- **解决方案**：
  - 内部对所有 instance 都一样 → **不要绑定具体 instance**。标题写 **"通用展开 (Per-stage detail)" / "Layer internal (typical)"**
  - 某 instance 真有独特性（如 Stage 1 是 Patch Embed 而 Stage 2-4 是 Patch Merge；或 decoder 比 encoder 多 cross-attn）→ 选有独特性的那个，并在标题指出区别
- **触发场景**：Transformer encoder/decoder layers、Residual/Dense stages、序列里多个相同 block
- **发现日期**：2026-05-17

#### [通用] 多步骤被压缩成单一视觉元素时必须显式标注
- **问题/发现 (R3-100 主 agent 复审)**：
  - fig05 糖酵解：第 4-5 步 (aldolase 拆糖 + TPI 异构) 被压缩成一个箭头段标 "aldolase / TPI"，丢失了"两个酶两步催化"的事实
  - fig06 Diffusion CFG："apply ε̂" 箭头从 CFG 公式只指向 x_t 一个 reverse 步骤 — 实际**每个**反向步骤都要 apply
- **解决方案**（优先级降序）：
  - **不压缩**：按真实步骤数全画
  - **必须压缩**：箭头/标签上**显式标注** `{4,5}` / `(2 substeps)` / `∀t` / "(applied at every reverse step)"
  - **配图注**：图 caption 写 "step 4-5 merged for clarity"
- **关键认识**：压缩节省视觉空间但丢失语义。**显式标注是必要补偿**，不标 = 视觉撒谎
- **发现日期**：2026-05-17

#### [多分辨率金字塔 / FPN] 索引命名必须一一对应或显式标注分辨率
- **问题/发现 (R3-100 主 agent 复审, fig01)**：ViT Stage 1..4 → F_1..F_4 → P_2..P_5（**P 跳过 P_1**）。读者要心算 F_n ↔ P_{n+1} 映射。即使原 FPN paper 用 P_2..P_5 命名（对应 ResNet C_2..C_5），混用两种索引体系会增加阅读负担
- **解决方案**：
  - **统一索引**：Stage_i → F_i → P_i（全 1-based 或全 0-based）
  - **保留差异时显式分辨率**：F_n 旁边/下方写 `1/2^{n+1}` 或 `H/4, H/8, ...` 让 mapping 可推
- **触发场景**：FPN、Hourglass、U-Net skip connections、Pyramid Vision Transformer、HRNet
- **发现日期**：2026-05-17

#### [解剖图 / 机制图 / 编号图] 步骤编号必须有 leader 引到对应特征
- **问题/发现 (R3-100 主 agent 复审, fig10 突触)**：右栏 1-6 步描述完整（"AP arrives"、"Ca²⁺ flows"等），但**没有任何 leader line** 把数字连到图中对应的 AP 波形、Ca²⁺、囊泡、NT、Na+、EPSP 位置。读者必须"读文字 → 找特征 → 心算匹配"，认知负担巨大
- **解决方案**：
  - **方式 A (推荐)**：每个编号有 dotted leader 到对应特征中心
  - **方式 B**：编号直接嵌在特征旁（≤ 0.3cm 距离），无需 leader
  - **方式 C (退化)**：右栏文字描述每条加上 "(see 红圈 X)" 这类显式定位
- **禁止**：编号在右栏文字描述，靠"文字描述 + 特征外观"让读者自己映射
- **触发场景**：解剖图、信号通路图、装配/分解图、考古示意、任何"按步骤索引特征"的图
- **发现日期**：2026-05-17

### R3-100 Pilot Batch 2 主 agent 复审发现（2026-05-18）

> Batch 2（fig11-20）⭐ 5 项 (E3/E7/E8/M8/M9) **100% 被 sub-agent 主动遵守**——E7/E8 用 endpoint dots、M8 用"通用展开"标题、M9 用 fork+独立箭头，模式全部对了。但 3 遍复审又找到 2 类新盲区，需要强化已有清单项。

#### [通用] 箭头方向自评必须显式写 "tip 在哪一端"
- **问题/发现 (R3-100 Batch 2, fig18 NeRF)**：MLP 块的 input (x,d) → MLP 箭头和 MLP → output (σ,c) 箭头**两端 tip 都画反了**——tip 在 source 端而非 destination 端，视觉上像 "MLP 在往输入框送数据"。Sub-agent 自评 M3 "方向一致" 给的是 Y，但实际反了。
- **根因**：M3 原文 "源/目标方向和指令一致（不是反过来的）" 是抽象问题，自评容易脑补成 "数据流方向对吧"——但**箭头 tip 的实际几何位置**才是关键。
- **解决方案**：M3 强化为**强制 enumeration**——逐条线显式写 "input→MLP: tip at MLP.west ✓"。这种 "tip-at-which-end" 的具体语言让自评无法跳过。已更新 visual-review-checklist.md M3 语言。
- **发现日期**：2026-05-18

#### [通用] 窄 box 内的多词标签必须量字符数 vs 宽度
- **问题/发现 (R3-100 Batch 2, fig15 protein structures β-sheet 面板)**：4 个标签 "side chain (R)" / "antiparallel sheet" / "R groups alternate above/below sheet" / "twist (slight)" 在 ~2-2.5cm 宽的色块标签内**明显被切断**（PNG 渲染看得清清楚楚），但 sub-agent 自评 T4 "标签不被截断" 给的是 Y，35/35 全 Y。
- **根因**：T4 抽象问题"被截断吗"对长标签的自评不可靠——视觉上看 box，文字"看起来差不多塞进去了"。**实际溢出在 PDF 边界外，PNG 渲染时被裁掉**。自评看不到溢出部分。
- **解决方案**：T4 强化为**强制度量**——对每个 text width < 3cm 的标签盒，自评必须写 "label X (Ncm) in box (Mcm) → fit ✓/✗"。中文每字 ~0.4cm，英文每字 ~0.2cm。已更新 visual-review-checklist.md T4 语言。
- **触发场景**：右栏 annotation 标签盒、legend 项、emoji-style 色块标签
- **发现日期**：2026-05-18

#### [Hero sub-panel] 小盒子内连线穿过盒内文字（S2 盲区）
- **问题/发现 (R3-100 Batch 2 用户复审, fig11 YOLOv8 CSP Block)**：hero sub-panel 里有 "Split"、"Bottleneck"、"1×1 Conv" 等小盒子（宽 ~1.2cm），连线从 .east → 下一盒.west 时，**连线的 y 坐标和盒内 label 的 y 坐标重合**，渲染出来线段在 label 文字上压过去，视觉效果像 strikethrough（"Sp̶l̶i̶t̶"）。
- **根因**：小盒子文字 `anchor=center` 时 y = box.center.y；连线锚点 `.east` / `.west` 也在 box.center.y → 同 y 重叠。S2 自评时 sub-agent 把 S2 理解为"外部连线穿过 free-floating 文字"，没盯 hero sub-panel **盒子内部**——35/35 Y 漏检。
- **解决方案**（任选）：
  1. 加宽盒子至 ≥2cm，**或**降低 label 字号让 label 占盒高 <50%（留 padding 区让连线走 box.north 或 box.south 锚点）
  2. 连线锚点用 `.north east` / `.south west` 等**偏 y 的锚点**而非 `.east` / `.west`
  3. 连线 y 偏移：`($(box.east)+(0,0.3cm)$) -- ...`，避开盒中文字
  4. label 用 `anchor=south` 放盒顶 + label 字号缩小
- **S2 已强化**：sub-agent 自评必须显式"hero sub-panel 内每个小盒"逐一确认线不穿字
- **发现日期**：2026-05-18

#### [Legend] 多个 legend 框间距不足看起来像被分割的大框（A5 盲区）
- **问题/发现 (R3-100 Batch 2 用户复审, fig17 Merkle tree)**：图底部有两个 legend 框紧贴放置——左框"Authentication path (target → root)"，右框"Target/path node + Sibling (proof element)"。两框间距 < 0.3cm，视觉上**像一个被竖线分割的大框**而不是两个独立 legend 组。
- **解决方案**（任选）：
  1. **合并为单个 legend 框**：所有 legend 项放进一个框内，用 column 分隔
  2. **两个独立框 + 横向间距 ≥1cm**：明显分离，让读者识别为两组
- **A5 已加入 checklist**
- **发现日期**：2026-05-18

#### [Bio 图 / 化学图] 功能性标签 vs 粒子符号区分对待
- **问题/发现 (R3-100 Batch 2 用户复审, fig20 光合作用 Z-scheme)**：图中有两类视觉上类似的文字标签，但语义不同：
  - **粒子符号** ("H⁺"、"Ca²⁺"、"O₂")：表示溶液里实际存在的离子/分子，散落在 lumen/stroma 空间。**不需要 leader**——它们是图的内容，不是注释
  - **功能性标注** ("H⁺ pump"、"H⁺ flow"、"oxidation"、"electron transport")：描述某个过程或方向的注释。**必须有 leader** 到对应的箭头/通道——否则就是 fig07/fig08 那种自由浮动 callout
- **fig20 漏检**：5 个 "H⁺" 符号无 leader（正确，是离子）但 "H⁺ pump" 和 "H⁺ flow" 也无 leader（错误，是功能性标注），sub-agent 把它们和粒子符号混为一类
- **判断规则**：
  - 含名词 + 动词（pump、flow、transport、release）→ 功能标注，要 leader
  - 纯化学式（H⁺、Na⁺、ATP、NADPH）→ 粒子符号，不要 leader
- **E7 适用扩展**：自评 E7 时要分类，不能简单"散落文字都不要 leader"
- **发现日期**：2026-05-18

### R3-100 Pilot Batch 3 用户复审发现（2026-05-18）

> Batch 3 主 agent 3-pass audit 自评 0 盲区，但用户红框标出 5 张图（fig23/26/27/28/29）的同一类问题。我的 audit 看的是 "是否有 fanout/leader/hero 错误"，没逐对箭头量 "tip 离 box 边的实际像素距离"。本节是这个共同问题的沉淀。

#### [通用] 箭头/连线 — 深度调研后的 canonical 模板（替代 4 轮迭代规则）
- **背景**：Batch 3-6 用户连续复审中箭头末端问题反复出现，4 轮规则迭代（distance → size → shape → ...）治标不治本。2026-05-18 做深度调研（PGF/TikZ 官方文档 + PlotNeuralNet 实测 + arrows.meta + bending library），发现 **5 个根因** 都是我原规则没覆盖的：
  1. **`bending` library 没加载** — 不加载时 arrow tip 在曲线/弯折路径上用 `quick` 模式，几何上必然 mis-align（这是 fig58/60 箭头末端怪的根因之一）
  2. **scale 是错的调节量** — TikZ 原生设计是 `length=⟨dim⟩ ⟨line_width_factor⟩` 让 tip **跟着 line width 自动缩放**。我之前的 "scale 0.7-0.9 短箭头 / 1.0-1.3 长箭头" 跟原生设计反着来
  3. **`width'` (带 prime) 让 tip 宽 = 长的比例** — 不是固定值。`width'=0pt 0.6` 保持完美三角比例
  4. **`sep` 参数处理 tip-to-border 间距** — 比 shorten 更精确，我之前完全没用
  5. **PlotNeuralNet (业界标杆) 用粗线 + 默认 tip** — `line width=0.8mm` + default Stealth。我推荐的细线 + 缩放 tip 路线反了
- **修订**：丢弃 4 轮迭代规则，用 **canonical pattern**（见 `tikz-template.tex` `arrow/.style`）：
  ```latex
  \usetikzlibrary{arrows.meta, bending}     % bending 必加
  arrow/.style={
      -{Stealth[length=5pt 1.5, width'=0pt 0.6, sep=0pt 0.5]},
      line width=1.0pt,
      shorten >=2pt, shorten <=1pt,         % ⚠️ shorten 不支持 dual-arg，用绝对 pt（以 tikz-template.tex 为准）
      color=black!70,
  }
  arrow thick/.style={arrow, line width=1.6pt}    % 主流
  arrow thin/.style={arrow, line width=0.6pt}     % 细节
  ```
- **关键认识**：**调 line width**（0.6 / 1.0 / 1.6 pt 三档），不调 tip scale；tip 通过 `<dim> <line_width_factor>` 语法自动跟随。这跟前 4 轮规则根本路线不同
- **E9 简化**：不再要求"分类箭头长度 → 选 scale → 选形状"。改为：**所有箭头一律用 canonical pattern，自评只检查 line width 选档是否合理**
- **发现日期**：2026-05-18（深度调研产物，前 4 轮 Batch 3-6 教训汇入）

#### [递归/折叠类协议] zone 中间出现大块空白——bottom info box 锁底 + 内容指数衰减
- **问题/发现 (R3-100 Batch 3 用户复审, fig22 Bulletproofs IPA)**：IPA 有 4 轮 (n=8 → 4 → 2 → 1)，向量盒数按 2^k 衰减。Round 1 占满，Round 4 只剩 2 个小盒。但 **折叠规则 + 通信复杂度 两个 info box 被锁在 zone 底部**，结果 Round 4 和 info box 之间出现 **>3cm 高的空白带**——明显违反 S6 "大块白色空带"，sub-agent 自评 Y 漏过
- **根因**：S6 抽象问题"有空白吗"自评不可靠；递归/折叠协议**天然内容衰减**，sub-agent 默认按最高那轮锁定 zone 高度，bottom info 锁底，中间空
- **解决方案**（任选）：
  - **方式 A (推荐)**：bottom info box **紧贴最末一轮内容**（不要锁 zone 底），整个 zone 高度自动压缩
  - **方式 B**：用空白区**补充半技术内容**——具体数值示例 / 中间 commitment 值 / 一轮的 step-by-step 计算细节，填补衰减留下的空间
  - **方式 C**：把 bottom info box **挪到 zone 外**（zone 紧贴最末一轮，info 在 zone 下方独立摆放）
- **判断规则**：递归类（IPA / Merkle fold / 二叉树聚合）+ 末尾节点远小于起始 → 强制检查"末尾内容到 zone 边距"
- **S6 已强化**：sub-agent 自评必须**显式量**每片连续空白的 width × height，> 3 × 2 cm 即 N，写出"在 X-Y 坐标范围有 W × H 空白"
- **发现日期**：2026-05-18

### R3-100 Pilot Batch 4 用户复审发现（2026-05-18）

> Batch 4 用户红框找到的问题：tip 头大身子小（已合入上一节 E9 lesson 的 Batch 4 修订）+ 长虚线绕路。

#### [长虚线 routing] 不要绕图大半圈
- **问题/发现 (R3-100 Batch 4, fig36 Tacotron 2)**：residual skip 紫虚线从 Linear Projection.east 出发，**绕图大半圈**——上 → 右过 Stop Token → 上方过 PostNet → 下到 ⊕。路径长，转折 ≥3 次，与其它箭头多次交叉
- **判断信号**：同源同目标虚线**绕过 ≥3 个无关元素** 或 **转折 ≥3 次**
- **解决方案**：见 checklist **E10** — 缩短直连 / lane 归并 / coordinate 分段
- **发现日期**：2026-05-18

### R3-100 Pilot Batch 5 用户复审发现（2026-05-18）

> Batch 5: tip 精度/大小/形状 已合入上节统一 E9 lesson。本节为 Batch 5 新独立发现。

#### [E6 强化] 任何 90° 弯折用 rounded corners，多 \draw 段共享坐标避免不连续
- **问题/发现 (R3-100 Batch 5, fig48 DETR)**：折线段在弯折处 sharp 90° 转角，看起来粗糙廉价；且多个 `\draw` 拼接的段之间出现**视觉不连续**（端点坐标手写，浮点误差致段间小空隙）
- **解决方案**：
  - **任何 90° 弯折**：`\draw[arrow, rounded corners=5pt]`（默认 0pt = sharp）
  - **多 `\draw` 段共享端点**：用 named coordinate (`\coordinate (mid) at (..., ...); \draw (A) -- (mid); \draw (mid) -- (B);`)，不要手写坐标拼接
  - **更优**：单 `\draw (A) -- (mid) -- (B)` 优于拆 2 个
- **E6 强化**：从"距离 ≥1.5cm 留 rounded"升级到"**所有 90° 必须 rounded + 段间共享坐标**"
- **发现日期**：2026-05-18

#### [Hero panel] 拒绝 side-dependency — 不要把支线挂在 hero 边框外
- **问题/发现 (R3-100 Batch 5, fig41 Swin V2)**：Hero 主流（Q/K/V → cosatt → softmax → AV → W_O → post-norm → y）时，sub-agent 把 "log-spaced CPB" 作为独立 box **挂在 hero 右侧**，跨边框虚线连回 cosatt。结果：hero 视觉边界外溢，主流和支线纠缠
- **解决方案**（任选）：
  - **A (推荐)**：把支线 inline 进主流（cosatt 步骤里直接列公式，不另起 CPB box）
  - **B**：CPB 挪出 hero panel，在 hero 下方独立小框 + 引线到 cosatt，明确"展开细节"语义
  - **C**：hero 横向放，CPB 在 hero **内部**做 inset，仍在 hero 边框内
- **禁止**：主流在 hero 内 + 支线 box 在 hero 外 + 跨边框虚线 — 视觉边界破坏
- **发现日期**：2026-05-18

#### [T4 recurrence] 文字超出 box — 字符数算对了但 PNG 仍溢出
- **问题/发现 (R3-100 Batch 5, fig46 复现 Batch 2 fig15)**：T4 已强化为"对 < 3cm box 显式量字符数"，但 fig46 sub-agent 算 ✓ 后渲染仍溢出
- **应对**：T4 自评 = 算字符数 **+ 看 PNG 验证文字 visibility**。光算不够 — font 实际宽 / TeX padding / inner sep 都影响最终
- **发现日期**：2026-05-18

### R3-100 Pilot Batch 6 用户复审发现（2026-05-18）

> Batch 6: Latex tip + rounded corners + hero no side-dep 等 Batch 5 规则全部被 sub-agent 主动应用。但用户红框点出 **9/10 张图**仍有问题，主要 3 类：重叠、路径不连续、虚线非 90°。**承认**：箭头末端规则迭代 4 轮（Stealth → scale → shape → ...）仍未根治，可能需要 concrete code template 而非更多 rules。

#### [重叠] S3 自评不可靠 — 必须强制枚举每处重叠
- **问题/发现 (R3-100 Batch 6, fig55 ATP / fig58 CLIP / fig60 CRISPR)**：3 张图 sub-agent 自评 S3=Y，用户全部能看到重叠。S3 "节点框不重叠" 是抽象问题，被印象判断滑过
- **重叠类型**：(a) box vs box，(b) text vs line，(c) leader vs unrelated element，(d) annotation vs background zone
- **S3 强化**：sub-agent 自评必须**逐一扫描整图标出每处视觉重叠**，写出 "N 处重叠：位置 / 类型" 或 "0 处重叠"。禁止"看起来没重叠"印象判断
- **发现日期**：2026-05-18

#### [E11 新增] 路径视觉连续性 — 多段 \draw 拼接出现断点
- **问题/发现 (R3-100 Batch 6, fig57 STARK)**：sub-agent 用多个 `\draw` 拼接 routing，端点坐标手写（浮点）→ 段间出现视觉断点；或路径被其它元素遮挡，没用 pgfonlayer 把路径放上层
- **解决方案**：
  - **方式 A (推荐)**：用 named coordinate (`\coordinate (mid) at (...);`)，所有段共享名字，浮点误差消失
  - **方式 B**：尽量用**单个 `\draw` 多段** `(A)--(mid)--(B)` 而不是拆 2 个 `\draw`
  - **方式 C**：路径若被其它元素遮挡 → `pgfonlayer{foreground}` 上层 OR 移动遮挡元素
- **E11 已加入 checklist**
- **发现日期**：2026-05-18

#### [E6 进一步] 虚线 routing 优先 90° 直角，禁用 Bezier 曲线
- **问题/发现 (R3-100 Batch 6, fig56 VQ-VAE)**：STE 虚线 arc 用 `to[bend left=45]` 或类似曲线 routing，本可用 90° L-bend with rounded corners. 用户："有些地方可以画 90 度，但是非要画了一个非 90 度的形状"
- **解决方案**：dashed leader / residual skip / reference 引线**首选 90° L-bend** (`\draw[dashed, rounded corners=5pt] (A) -| (mid) |- (B)` 或 `(A) -- (corner) -- (B)`)，**禁用** `to[bend left/right]` 或自由 Bezier
- **理由**：90° 直角 routing 视觉上"工整"，曲线 routing 在密集图中容易看起来"乱"
- **E6 强化**：从"90° 必须 rounded" 升级到 "**虚线 routing 默认 90° 直角，曲线只在明确语义场景用**"
- **发现日期**：2026-05-18

> Batch 6 元发现"箭头末端 4 轮迭代仍有问题，需要 concrete template" 已被 **2026-05-18 深度调研 resolved** — canonical pattern 落在 `tikz-template.tex`，详见上方 Batch 3 section 的 "[通用] 箭头/连线 — 深度调研后的 canonical 模板" lesson。

#### [Batch 9] 树状分叉 stub 和 spine 之间出现 1pt 视觉断裂
- **问题/发现 (R3-100 Batch 9, fig86 HiFi-GAN)**：MPD/MSD fan-in spine 上的 stub 用 `\draw[arrow]` 画——canonical `arrow/.style` 含 `shorten <=1pt`，导致 stub 起点离 spine **1pt** gap。300 DPI 下肉眼可见"分叉点处线断了"。用户在 PNG 一眼看出 4-5 张图都有这种断裂模式
- **根因**：`arrow/.style` 的 `shorten <=1pt` 是为节点 → 节点设计的（让线离 node 边 1pt 不贴边），但 spine → target 的 stub 起点**不是 node**而是 spine 上的精确点，shorten 把它向后挪 → 视觉 gap
- **解决方案**：`tikz-template.tex` 新加 `fan_stub/.style`：与 `arrow` 同 tip 但 **`shorten <=0pt`**（起点紧贴 spine）
  ```tex
  % spine 一条线，无 arrow 无 shorten
  \draw[line width=1.0pt, color=...] (left_x, y) -- (right_x, y);
  % 每条 stub 用 fan_stub
  \draw[fan_stub] (stub_x, y) -- (target.north);
  ```
- **避坑要点**：
  - ❌ 不要 `\draw[arrow] (x, spine_y) -- (target)` — 会有 1pt gap
  - ❌ 不要在 spine 中点放 `fill=white` 的 sum/junction 圆圈 — 圆圈截断 spine
  - ❌ 不要用多个独立 `\draw` 画主干+横杆 — 段间 shorten 制造间隙
- **E3 已加自评新增项**：每个 fan-out / fan-in 必须确认 "stub 起点和 spine **零 gap**" + "junction dot 颜色和 spine **一致** 或不放 dot"
- **发现日期**：2026-05-19

#### [Batch 8 后续] line-through-node 几何检测（pdf-overlap-checker 升级）
- **问题/发现 (R3-100 Batch 7+8, 用户复审)**：canonical 箭头模板上线后，箭头末端问题大幅改善；用户复审指出**剩余两类问题**：① 框/文字/线之间**重叠** ② **线穿过路径**（z-order + 路径绕路）。`visual-review-checklist.md` 的 S3 强枚举 + E11 共享 named coord 缓解了一部分，但**几何穿过仍要靠几何检测**——靠自评清单容易漏（fig80 apoptosis 红虚线穿过 3 个调控盒，35/35 自评 Y）
- **2026-05-19 全网调研 + 升级**：
  - 评估了 4 类技术路线：PGF graphdrawing (Lua) / libavoid (Inkscape 系) / GraphViz dot+spline-o-matic / PDF post-render bbox 检测
  - 前 3 项是 **graph-shape figure 才适用**，对我们的复合图（嵌入可视化 + sidebar + 中心 hub）无效
  - 选了 **post-render 几何检测路线**——升级 `pdf-overlap-checker.py` 加 **2 个新检测**：
    1. **line-through-node**：line segment 真穿过 filled rect 内部（不只是 bbox 相交）
       - 加 PyMuPDF 提取**真实 line endpoint**（pdfplumber 只给 bbox，丢失对角线方向）
       - 把"有 fill 的 path bbox"当作 node rect（TikZ 大量节点是 4-line + fill 而非 `re` 操作符）
       - **Liang-Barsky parametric clip** 判断 segment 是否真穿过 rect 内部
       - 4 类 false-positive 过滤：尺寸（6-140pt × 6-90pt 排除 zone）/ 自身 path / cluster suppression (≥4 segments 同 rect 视为收敛节点) / spine filter (line 在 rect 中线 ±3pt 视为 lifeline)
    2. **node-overlap**：两个 sibling node rect 几何重叠
       - 严格尺寸（10-140pt × 10-90pt 排除 glyph）
       - 跳过完全包含关系（parent-child OK）
       - **drop-shadow filter**（宽高近似 + 中心偏移 ≤5pt → TikZ drop shadow style 双绘）
       - 跳过同一 drawing path（同节点 outline + fill 复算）
  - **`--json` flag** 让 sub-agent 结构化消费 `{errors: [...], warnings: [...], summary: ...}`
- **实测命中**：
  - **line-through-node**：fig80 cell cycle 4 处全中（apoptosis 红虚线，坐标对得上）；Batch 7 fig62/63 spine filter 后 17→6；fig71/74/77/78 共 0 误报
  - **node-overlap**：drop-shadow filter 上线后 ex01-10 几乎全 0；剩下的 fig63/fig79/fig69/ex08 都是 1-4 处真问题（panel overflow / 紧密邻接节点）
- **已知边界**：
  - 矩阵密集图（heatmap cells 当作 rect）over-fire（ex10 GAT 报 121 处）—— 没办法纯几何分辨"语义 cell" vs "节点 rect"
  - 收敛节点（fan-in 多线汇聚）会被 cluster filter 误杀真问题，调高阈值又会暴出大量假阳
  - node-overlap 现在的 drop-shadow filter 假设 shadow 偏移 ≤5pt；如果 TikZ template 改了 shadow offset > 5pt 会出现假阳——记得同步更新 filter
  - **裁决依赖 sub-agent triage**：把检测结果当 **candidate report** 不是绝对 bug
- **使用方式**：
  - 编译后必跑 `python3 references/pdf-overlap-checker.py file.pdf --json > overlap.json`
  - sub-agent 在视觉自评 ④.5 时读 overlap.json：
    - `line-through-node` / `node-overlap` 类**逐条 triage**（不是绝对 bug——矩阵 cell、生物收敛节点常误报）
    - 其它 4 类（text-overlap / text-overflow / off-center / text-line）大概率是真 bug，直接修
  - 矩阵图、神经网络收敛图等**已知误报易发**的图，可在 prompt 中提醒 sub-agent "ignore line-through-node hits inside heatmap regions"
- **发现日期**：2026-05-19

---

#### [Batch 13 用户复审 #2] 步骤 ① 跳过 → 排版大块空白（fig126 Tacotron2）
- **问题/发现 (R3-100 Batch 13, fig126 Tacotron2 用户截图)**：图整体出现大块空白 — Encoder 列内容到 y≈-7 结束，WaveNet 在 y=-11.8 跨左→右整宽，Audio Waveform 在 y=-13.4。**Encoder 列下方 + WaveNet 中段 ≈ 5cm × 6cm 大块空白**。设计师一眼看到的问题，sub-agent 46 项 + Step 0 都没抓到
- **根因（步骤 ① 跳过 + 不可验证）**：
  ```
  grep 'ASCII|草图|10 项|Pre-flight|画图指令' fig126/figure.tex = 0 hits
  ```
  sub-agent 加载了 `step1-instructions.md` 但**没有按它要求实际输出 10 项 + ASCII 草图**——直接跳到编码。`step1-instructions.md` 写"必须以文字形式输出"，但 skill **没法验证** sub-agent 是否真的输出了。即使 ④.5 S6 "大块白色空带" 规则在，sub-agent 自评说 "Y, 0 处" 也漏过了
- **2026-05-21 修复（双锁 + 复杂图支持 narrative）**：
  - **锁 1：步骤 ① 产物物质化（双形式）**——SKILL.md ① 明文要求 10 项 + 草图**写进 figure.tex 头部注释块**：
    - 形式 A：ASCII 草图（极简/中等图）
    - 形式 B：**Narrative 设计文字**（复杂图 / 含 hero 子结构 / 嵌入 viz）—— 每列/每 zone 一段叙述，含 x/y 范围 + 内部子结构 + **预想"哪里可能空白"并写应对**
  - 复杂图（fig126 Tacotron2 类）**不能用 ASCII**——嵌入热力图/嵌入 mini-viz ASCII 画不出来；设计师真实思考是叙述性空间描述，不是 ASCII 字符画
  - **锁 2：Step 0 E 段验证**——sub-agent 在 ④.5 Step 0 时**必读 figure.tex 头部**确认有 form A 或 form B 注释块；若两种都没有 → critical blocker 回 ① 重做
- **设计哲学**：
  - 从"声明式纪律"（sub-agent 自报"我做了 step ①"）升级到"产物式纪律"（看 figure.tex 头部有设计文档注释 = 证据）。**可验证的纪律 > 不可验证的声明**
  - **不强制 ASCII** — ASCII 在复杂图上反而是限制（嵌入 viz / hero 子结构画不出来 → 用户反馈：会"影响画图复杂度和创新性"）。Narrative 形式允许复杂图保留设计自由度，同时保留"先想后画"的纪律
- **发现日期**：2026-05-21

#### [Batch 13 用户反思] 13 batches 加 70+ 规则但 bug 仍在 — meta 层缺失
- **问题/发现 (R3-100 Batch 13 用户反馈)**：13 batches 累积 46 项 checklist + 13 ⭐ + 7 类几何检测 + 6 canonical styles，每次用户复审仍能找出新模式 bug。**这不是"差几条规则"的问题，是反应式改进的天花板**
- **5 层根因**（深度诊断）：
  1. 规则是症状不是原理：sub-agent 不知道 "spine+stub 同色"、"tip 必落 anchor"、"label 间距 ≥0.3cm" 的共同底层是「**视觉连续性**」
  2. sub-agent 算法式写 TikZ：`spec → 选坐标 → 写 \draw → 编译`，缺"读者眼睛轨迹"视角
  3. self-eval 乐观偏差：即使写证据仍倾向 Y
  4. TikZ 自由度爆炸：每箭头 ~20 个独立选择，组合规则不可能覆盖
  5. text-only model 无 continuous visual feedback：盲写 → 编译 → 改，第一次盲写时埋的 bug 难修
- **承认现实**：原本 skill 散落 5 处类似"人类化"规则（tikz-global-rules.md 91/115/242/252/262, sequence-diagram.md 29），但**被埋在 specific rules 中没提升为 meta lens**
- **2026-05-21 修复（meta 层升级）**：
  - **SKILL.md 顶部加"视觉法则"段**（3 大法则：0.1 秒直觉 / 读者眼睛轨迹 / 删除测试），提升为所有规则之上的 lens
  - **④.5 加 Step 0：视觉直觉先行**——在 46 项 Y/N 之前必走 4 段证据（3 秒第一印象 / 主线轨迹 / 删除测试 / 审美退步测试）
  - **visual-review-checklist.md 强制流程同步**
- **为什么这有用**：把"读者视角"从可选规则提升为强制 step；从机械逐项检查变成**先视觉后机械**。设计逻辑：46 项是细节体检，Step 0 是整体心电图，缺一不可
- **发现日期**：2026-05-21

#### [Batch 12 用户复审 #3] T7 label 间距太小（fig116 WaveGlow）
- **问题/发现 (R3-100 Batch 12, fig116 用户截图)**：z_a / z_b bypass labels 与 bypass lines 间距仅 0.02-0.04cm — 视觉上 label "骑在线上"
  ```latex
  % bypass line at y = -2.0
  \coordinate (zb1_l) at (10.5, -2.0);
  \draw[arrow, ...] (split1.south) -- (zb1_l) -- ... ;
  % z_b label
  \node[font=\scriptsize, anchor=south] at (14.0, -1.98) {z_b (unchanged)};
  %                                              ↑↑↑↑
  %                                        只比 line 高 0.02cm
  ```
- **根因**：之前 T7 只规定 label 必须 `above`/`below`（方向对），**没规定最小间距 ≥ 0.3cm**。sub-agent 写 `anchor=south at (14.0, -1.98)` 自认为 above，技术上对，但 0.02cm 间距 = 视觉上压在线上
- **2026-05-20 修复**：T7 加最小间距铁律 — label 到 line ≥ 0.3cm（或等效 `yshift=8pt`）。**自评必须报具体数值，禁止印象判断**
- **正确写法**：
  ```latex
  \node[font=\scriptsize, anchor=south, yshift=8pt] at (14.0, -2.0) {z_b (unchanged)};
  % 或显式
  \node[font=\scriptsize, anchor=south] at (14.0, -1.7) {z_b (unchanged)};   % line at -2.0, label south at -1.7 → 0.3cm gap
  ```
- **发现日期**：2026-05-20

#### [Batch 12 用户复审 #2] tip 撞裸坐标 = "撞墙"视觉（fig118）
- **问题/发现 (R3-100 Batch 12, fig118 YOLOv8 用户截图)**：3 条 head feed arrows `\draw[arrow] (bu_p3.east) -- (14.5, 0.0);` —— tip 落在裸坐标 `(14.5, 0.0)`（spine 线上的点），不是任何 node。视觉上"箭头指向空气" / "撞 dashed zone border"。fig118 这是 "3 平行 pass-through with shared vertical spine" 模式，不是 fan-in/fan-out — sub-agent 画 spine 当"shared rail" 但 incoming 误用 `\draw[arrow]`
- **vs fig120 fan-in 不同点**：fig120 是真 N→1 汇合；fig118 是 3→3 平行流共享 visual rail。两者 sub-agent 都犯"incoming 带 tip"错，但触发模式不同
- **根因（E2 措辞漏洞）**：之前 E2 写"junction 不被 tip 戳"，sub-agent 不把 `(14.5, 0.0)` 当 "junction"（因为只有 1 incoming + 1 outgoing per row，不像"汇合"）
- **2026-05-20 修复（E2 重写）**：明文铁律 "**`\draw[arrow*]` 的 tip 终点必须是 node.anchor，禁止是裸坐标 / `\coordinate`**" — 不管是不是 junction，只要 tip 撞坐标就 ERROR。三类违规：(a) fan-out junction dot 被戳 / (b) fan-in 汇合点 / (c) spine 中间点
- **fig118 正确写法**（写进本 lesson 备查）：
  ```latex
  % 方案 A（推荐，无 spine）：3 条直接横向箭头
  \draw[arrow] (bu_p3.east) -- (det_head.west);
  \draw[arrow] (bu_p4.east) -- (seg_head.west);
  \draw[arrow] (bu_p5.east) -- (pose_head.west);

  % 方案 B（要保留 shared spine 的视觉象征）：
  \draw[line width=1pt, color=black!70] (14.5, 0.0) -- (14.5, -9.0);          % spine 仍画
  \draw[line width=1pt, color=black!70] (bu_p3.east) -- (14.5, 0.0);          % incoming NO tip
  \draw[line width=1pt, color=black!70] (bu_p4.east) -- (14.5, -4.5);
  \draw[line width=1pt, color=black!70] (bu_p5.east) -- (14.5, -9.0);
  \draw[fan_stub] (14.5, 0.0) -- (det_head.west);                             % outgoing 带 tip
  \draw[fan_stub] (14.5, -4.5) -- (seg_head.west);
  \draw[fan_stub] (14.5, -9.0) -- (pose_head.west);
  ```
- **发现日期**：2026-05-20

#### [Batch 12 用户复审] Fan-in canonical 缺失 + 颜色不一致 + 孤立 legend 点
- **问题/发现 (R3-100 Batch 12, fig120 CRISPR-Cas9 用户截图)**：
  1. **Y-junction "><绿尖"** (crRNA + tracrRNA → sgRNA)：两条 incoming 用 `\draw[arrow]` 都带 tip 在汇合点（"><"），且 incoming 蓝色 / outgoing 青色 — 颜色不一致 + 双 tip 对撞
  2. **fan-out spine 黑 + stub 彩** (DSB → NHEJ/HDR)：spine `color=black!70` 1.4pt vs stub `color=acaPurpleLine/acaGreenLine` 1.2pt → 折角处看上去断 + 颜色突变
  3. **4 个孤立彩色圆点漂浮**（蓝/橙/灰/红）无 label 无 leader — sub-agent 大概想画 legend 标记但忘了 label
- **根因（skill 5 处漏洞）**：
  - **E3 只有 fan-out canonical，没有 fan-in canonical** — sub-agent 不知道 N→1 怎么画，模仿 fan-out 反过来 → 错
  - **E2 没明文 "incoming 全部 no tip + 同色"** — sub-agent 给 incoming 加 tip
  - **没规则规定 spine + stub 颜色一致** — sub-agent 选 spine 黑 / stub 彩
  - **E7 没强制 legend dot 必有 label** — 孤立彩点放任
  - rounded corners 在 fan-in 折角处也漏（fig120 incoming 用 `++(0,-0.4) -- (combine)` sharp 90°）
- **2026-05-20 修复（5 处规则）**：
  - **E2 强化**：incoming 全部 no tip + 与 outgoing 同色（铁律）
  - **E3 重写**：(a) fan-out canonical + (b) **新增 fan-in canonical** + (c) 颜色铁律全同色 + (d) fan_stub style + (e) spine 中点禁放 white fill + (f) rounded corners 必加
  - **E7 强化**：legend dot 必紧贴 label < 0.3cm；禁止孤立彩色圆点
  - **lessons sample code**：fan-out / fan-in 两段 canonical TikZ 代码示例（本 lesson 上方 E3 中）
- **fan-in canonical 代码（写进 checklist E3 + 此 lesson 备查）**：
  ```latex
  % N sources → 1 target，所有 SAME COLOR
  \draw[line width=1pt, color=C, rounded corners=5pt] (src1.south) -- (src1.south |- Y);
  \draw[line width=1pt, color=C, rounded corners=5pt] (src2.south) -- (src2.south |- Y);
  \draw[line width=1pt, color=C] (src1.south |- Y) -- (src2.south |- Y);  % spine
  \draw[arrow, color=C] (midpoint, Y) -- (target.north);                   % 唯一带 tip
  ```
- **发现日期**：2026-05-20

#### [Batch 11 用户复审] residual / 标签位置 / 时序 annotation 三连击
- **问题/发现 (R3-100 Batch 11, fig101/107/108/110 用户截图)**：
  1. fig110 末端短箭头（~0.5cm）用 `\draw[arrow, shorten >=6pt]` 而非 `arrow short`，stem 被吃光剩 tip
  2. fig110 5'/3' label 用 `anchor=left/right` 在 y=0.5 → 与同 y 箭头压字
  3. fig108 ViT residual rail 离 addnorm1.east 仅 0.4cm → U-bend 形状回路怪
  4. fig107 MuSig2 B-N compute box 距 P1.x 仅 0.35cm，与 activation bar ±0.225cm 半宽几乎重合
  5. fig101 ConvNeXt residual 用了 `residual` style 自带 `rounded corners` → U-bend 视觉怪
- **根因**：
  - E13 短箭头规则 sub-agent 漏看 — 短距离箭头偶发回退 `arrow` 默认
  - skill 没规则规定水平箭头 label 必用 `above/below`
  - E14 只约束 `|-` pierce，没规则约束 residual rail 与 box 的最小间距
  - skill 没规则规定时序图 annotation box 与 lifeline 间距
- **2026-05-20 修复（4 处规则）**：
  - **T7 标签放置规范**：水平箭头 label 必用 `above`/`below` 不用 `left`/`right`
  - **S10 时序图 annotation 间距**：compute box 距 lifeline ≥ 0.5cm
  - **E14 扩充 residual rail 间距**：rail 距最近 box 边界 ≥ 0.5cm
  - **residual aesthetic 指南**（本 lesson 沉淀）：垂直 tap < 1.0cm（避免线下潜过深）；多 residual 共用 rail y（保持平行带）；residual `rounded corners` 默认值不变（5pt 软化），但 tap 长度小时**自动失效不显弧**——不必特意 `sharp corners`
- **发现日期**：2026-05-20

#### [Batch 10 用户复审 #2] `|-` / `-|` L-bend 穿 hero body + checker MAX_AREA 漏报
- **问题/发现 (R3-100 Batch 10, fig97 Pedersen Commitment 用户截图)**：`\draw[arrow] (msg.south) |- (ped_hero.west)` 中 msg 的 x 落在 hero box 的 x 范围内，TikZ 把横线**画在 hero 内部**——产生"箭头从 hero 内部出来"的视觉怪象。这种 bug 在 Batch 8/9/10 多次出现但未被 checker 抓到
- **根因双层**：
  1. **设计层**：PGF 不做 obstacle-aware routing（[官方手册](https://tikz.dev/base-nodes)），`|-` 只机械地"先垂直再水平"，**不考虑路径上有没有 obstacle**
  2. **checker 层**：`pdf-overlap-checker.py` 有 3 个 bug：
     - `MAX_AREA = 7500` 排除了 4.4cm × 2.2cm (=7750pt²) 的 Pedersen hero，hero-sized 节点被跳过
     - "endpoint inside rect → skip" 误判：`|-` 横线两端**都在 rect 内部**时也被 skip
     - "endpoint on boundary → skip" 把 stroke path 的 rect 边（top/bottom/left/right line）也算作"穿过"，cluster filter (≥4) 把真 bug 一起 drop
- **2026-05-19 修复（4 处）**：
  1. **`pdf-overlap-checker.py`**：(a) `MAX_AREA = 12500` 允许全 140×90 节点；(b) "both endpoints inside" 不再 skip 而是 flag；(c) "both endpoints on boundary" 仅当 seg 不沿 rect 4 条边时 flag
  2. **`SKILL.md` ③ 加 `|-` L-bend 安全条款**：✅/❌ 代码示例 + 用 named coordinate waypoint 绕开 obstacle
  3. **`visual-review-checklist.md` 加 E14**：自评每条 `|-`/`-|` source/target 投影是否重叠 + waypoint 数量
  4. **本 lesson 沉淀**
- **fig97 验证**：fix 后 checker 正确报 2 处 line-through-node — (62,165)→(39,165) 和 (130,165)→(152,165)，对应 msg/rand 进入 Pedersen 内部的两条横线
- **发现日期**：2026-05-19

#### [Batch 18 架构重思考] TikZ Snippet Library — 用乐高积木解决文本范式天花板

- **问题/发现 (R3-100 Batch 17, fig153 v2 TikZ)**：Philosophy First 重构后 sub-agent 把"嵌入 viz / panel / 公式 / 多色"4 个要素都做对了，但用户复审仍说"排版乱 / 大量空白 / 配色有问题"。
- **核心洞察**：Figure design 本质是 **multi-modal 任务**（visual perception + 结构组合 + 工程实现），当前 skill 是**纯 textual prompt engineering**：
  - ✅ 文本能做到 "嵌入 ≥ 1 个 viz" / "≥ 5 种 zone 颜色" / "无大空白"
  - ❌ 文本做不到 "嵌入 viz 看起来要有视觉重量" / "颜色要协调" / "留白要均匀"
  - **Batch 13-17 实质上在用文本逼近一个本质上需要 visual reference 的任务 = dead-end**
- **6 个候选方向**（A/B/C/D/E/F），选定 **A: TikZ Snippet Library**——给 sub-agent 高质量乐高积木拼装而不是从零写
- **解决方案（2026-05-22 Batch 18）**：创建 `references/tikz-snippets/` 含 6 个手工精雕的 TikZ 片段：
  - `attention-heatmap.tex`（N×N 热力图 + colorbar，硬编码 diagonal-dominant pattern + 紫色渐变）
  - `bar-chart.tex`（benchmark 柱状图 + grid + 数字标注）
  - `hyperparams-table.tex`（参数表 + 交替行 fill + bold value）
  - `multi-zone-palette.tex`（6 色 zone tone 标准模板 + 用色规则）
  - `pipeline-stages.tex`（N-stage 水平管线 + 自动 arrow 连接）
  - `formula-box.tex`（公式 box 3 variant：simple / with annotation / multi-line）
  - 每个 30-80 行 TikZ，独立可编译验证（6/6 PASS）
- **SKILL.md 改动**：Philosophy 段加"复杂档画图捷径"子段 + 加载索引加 `tikz-snippets/` 路径 + 明令禁简化 snippet 核心结构
- **预期效果**：sub-agent 在复杂档时**拼装 ≥ 3 个 snippet**（如 pipeline + heatmap + bar chart）—— 视觉重量自动达到 examples 标杆。N×M 组合让多样性保持。
- **元教训**：当文本范式触天花板，**不要再加规则，而是给 high-quality artifacts (snippets)**。这是 React 组件库思想应用到 TikZ。
- **发现日期**：2026-05-22

#### [Batch 17 元教训 — TikZ 硬约束 + dark theme 禁忌] sub-agent 用 Python 替代 TikZ

- **问题/发现 (R3-100 Batch 17, fig153 LLaMA-2)**：sub-agent 在执行 Module-First 子流程时**完全用 Python + matplotlib 生成 `.py` 文件**，没有 `figure.tex`。同时用了 **dark theme background**。
- **sub-agent 的动机推断**：
  - matplotlib 对复杂嵌入 viz (RoPE 旋转圆图 / GQA 头组示意 / benchmark bar chart) 比 TikZ 原生 API 方便
  - dark theme `plt.style.use('dark_background')` 一句话搞定，TikZ 反转全色工程量大
  - Module-First 多次编译时 Python (1-3s) 比 xelatex (5-30s) 快
- **核心问题**：Python 是**画起来更方便，不是画得更好**——
  - ❌ 不能 `\input{figure.tex}` 嵌入 LaTeX 论文（必须 `\includegraphics{.png}`，破坏 thesis-figure-skill 价值主张）
  - ❌ dark theme 与学术论文 light bg 风格断裂
  - ❌ 公式渲染：matplotlib mathtext 不如 LaTeX 原生
  - ❌ 风格不一致：fig153 (Python dark) 和 fig151/152/154 (TikZ light) 不能共存于同一 paper
- **解决方案（2026-05-22）**：
  1. **SKILL.md 硬约束**新加 🔴 工具铁律：**Module-First 子流程必须保持 TikZ**，禁 Python 替代；复杂嵌入 viz 用 TikZ 原生（`\foreach` / `pgfplots` / 手画 `\draw`）
  2. **SKILL.md 硬约束**新加 🔴 配色铁律：默认 light bg，dark theme 需用户明确请求
  3. **重画 fig153 v2 用 TikZ** 作为 case study，验证 TikZ 能否达到同质量
- **发现日期**：2026-05-22

#### [Batch 16 元教训 — 按需复杂度 + Module-First] Philosophy First 重构后剩余两个短板

- **问题/发现 (R3-100 Batch 16 用户反馈)**：Philosophy First 重构后，4 张复杂图（BERT/ResNet50/PPO/GAT）都达到了 examples 06-10 风格的方向（嵌入 viz + 信息 panel + 公式 + 多色），但用户反馈两个问题：
  1. **"都是画的很复杂的 但是也有些乱"**——sub-agent 默认套复杂档 examples 06 风格，用户实际可能只想要中等档清晰图 → 过度发挥 = 乱
  2. **"是不是应该先画一部分 一部分 然后每部分都画好了 再拼接"**——一次性写 800 行 TikZ 模块太多 → 整图局部混乱
- **核心洞察**：Philosophy First 解决了"审美方向"，但没解决：
  - **复杂度按需而定**（不是默认复杂 examples 06）
  - **Module-First 分块设计**（不是一次性整图）
- **解决方案（2026-05-22 加 2 条流程规则）**：
  1. **SKILL.md ①.5 改为"用户驱动 + 自动检测兜底"**：
     - 第 1 步：从用户原 prompt 关键词推断复杂度（"详细/含 benchmark" → 复杂；"概览/主架构" → 中等；"示意/几何" → 极简）
     - 第 2 步：如果不明确**主动询问用户**（A 极简 / B 中等 / C 复杂）
     - 第 3 步：用户确认后再画——禁止自作主张套复杂档
  2. **SKILL.md ③ 加 Module-First 子流程**（仅复杂档强制）：
     - ③.A 先画 hero（嵌入 viz + 公式）→ 单独编译验证
     - ③.B 再加主流（zones + connecting arrows）→ 拼接验证
     - ③.C 再加 panels（hyperparams / benchmark / legend）→ 拼接验证
     - ③.D 整体审查（→ 进入 ④.5）
- **关键原则**：**Prescriptive 流程规则 ≠ Defensive checklist 规则**。这 2 条是"应该 X"（流程），不是"不要 X"（防御）——加 2 条不算回到 47 项老路。
- **Batch 17 验证预期**：sub-agent 应该
  - 看到不明确 prompt 时**主动询问复杂度**
  - 复杂档时**分块画 + 单独验证**，整图更干净
- **发现日期**：2026-05-22

#### [Batch 15 元教训 — Philosophy First 重构] 47 项防御规则反而抑制了创造力

- **问题/发现 (R3-100 Batch 14/15 用户反馈)**：fig137 经历 v1 (大空白) → v2 (5 bug) → v3 (修 5 bug 但 fan-out 仍丑) 三代迭代，每轮都加新规则补漏洞，但**整体审美和 examples 06-10 的距离越来越远**。用户反馈："新的毛病还是会有"，"现在很少能画出 examples 06-10 那种风格"。
- **根因（最深层）**：13-15 批演化方向**完全错了**：
  - 47 项 checklist 是 **defensive 规则**（"不要 X"）—— 没有任何 **prescriptive 设计指导**（"应该 X"）
  - canonical 模板 + g1-g4 几何 + E15 anchor 等细则把 sub-agent 推向**统计中心的安全默认**（box+arrow only / 3 色单调 / 无嵌入 viz）
  - 全部规则可通过 = box+arrow figure，**审美天花板被规则地板压低**
- **全网调研发现**（2026-05-21）：
  - **Anthropic frontend-design** (277k installs)：42 行打败 800 行；Philosophy first；Naming gravitational pull；Permission for creativity；UNFORGETTABLE question
  - **PUA skill** (GitHub tanweai/pua)：corporate framing + L1-L4 pressure escalation + ownership mindset
- **解决方案（2026-05-21 Philosophy First 重构）**：
  1. **SKILL.md 顶部**新增 Philosophy 段（替代之前的"视觉法则"）：
     - The UNFORGETTABLE Question（审稿人 5 秒记住什么）
     - Naming Gravitational Pull（7 个统计中心默认明确列禁）
     - Permission for Creativity（NeurIPS/ICML investor framing + "Don't hold back"）
     - 创造空间词汇菜单（嵌入 viz / panel / 公式 / 配色 / 层级 / cross-zone / 学术 polish）
  2. **visual-review-checklist 精简 47 → 18 项**：保留编译保障 (T1/T3/T4) + 空间灾难 (S1/S6/S8/S9) + 语义 (M1/M2/M3/M8) + 连线 (E1/E2/E3/E9/E12) + 美学 (A1) + **新增 V1** (复杂档应有 ≥1 嵌入 viz/panel)
  3. **删除最近 5 个 commit 的防御细则**：E3 g1-g4 几何 / E15 同 anchor / T7 0.5cm 强化 / Step 0 E (1a)/(1b) / hero sub-layer 间距预算公式
  4. **Philosophy + 18 项双重门**：18 项过仅说明无明显 bug，Philosophy 通过才说明审美达标
- **Batch 16+ 验证预期**：sub-agent 应能在 Philosophy 引导下**主动考虑嵌入 viz/panel/公式嵌入**，不再 box+arrow only
- **反思**：13-15 批教训的最大价值不是规则本身，而是认识到"defensive 规则越多 → 创造力越少"。**少而精的 Philosophy 比繁多防御更释放潜力**。
- **发现日期**：2026-05-21

#### [Batch 14 用户反馈] fig137 v2 修一个 bug 引入 5 个 — 白盒规则被黑盒绕过

- **问题/发现 (R3-100 Batch 14, fig137 v2 用户复审)**：
  v2 修复 v1 的 11×5cm 大空白后，用户在新 PNG 中标出 5 处新问题：
  1. K/V 入口的"fork dot"：sub-agent 用 **2 条独立 `\draw[arrow]`**（不是 fan-out canonical spine + stubs）从 enc_an2.east 到 ca_k / ca_v；`line width=1.2pt + rounded corners=5pt` 在 90° 折角处渲染成可见 bulge，视觉像 fork dot
  2. Q 旁紫色方块：`\node[fill=white, inner sep=1pt, font=\scriptsize\bfseries, color=acaPurpleLine] {Q}` 在白背景 PDF 上，fill=white 不可见，紫色粗体单字符把 1pt inner sep 填满 → 视觉是紫色方块（fig120 孤立 dot 教训的变体）
  3. 紫橙撞车：紫色 `(dec_ca.west) -- (ca_q.east)` 和橙色 `... -- (dec_ca.west)` 两条 incoming arrow tip **都终止在 dec_ca.west 同一 anchor** → 同一像素点不同颜色重叠
  4. "Multitask Output" 标题离 spine 仅 0.3cm = T7 边界值视觉太紧
  5. v2 sub-agent 自评 0 blocker 仍漏检全部 5 处
- **元根因（最深层）**：规则用"if X then must Y"形式，sub-agent **可以"不用 X"绕开 Y**——白盒规则被黑盒绕过：
  - E3 自评只问"有没有 fan-out canonical 实施"，sub-agent 用 2 条独立 \draw 替代 spine + stub → E3 自评条件未触发
  - "多 tip 同 anchor 撞车" SKILL 没明文规则 → 规则空白
  - T7 报"0.3cm ✓"过 → 边界值通过 = 实质失败
- **解决方案（2026-05-21 fig137 v2 后三处修复）**：
  1. **`visual-review-checklist.md` E3 加"反绕过铁律"**：grep figure.tex，同一 node.anchor 出现 ≥2 次作为 `\draw[arrow]` 起点 → 必须重写为 canonical（即使是独立写法）
  2. **`visual-review-checklist.md` 新增 E15** ⭐：同一 anchor 不能被多条 incoming arrow 同时 tip；修复用换 anchor / anchor offset / routing 改道
  3. **`visual-review-checklist.md` T7 强化**：(a) 视觉默认从 0.3cm 提升到 0.5cm（0.3 是 compile fail 阈值不是视觉安全值）；(b) `fill=white` + 单字符 + bfseries label 警告（inner sep ≥ 3pt OR 不用 bfseries OR 加长 label）
  4. 总项数 46 → 47；⭐ 13 → 14
- **fig137 v3 验证预期**：sub-agent 应该写"E15 dec_ca anchor 检查：3 条 incoming（dec_an1.south + Q + Attn out），用了 .west / .north / [yshift=+3pt]dec_ca.west 三个不同 anchor offset 分开" 才能通过
- **发现日期**：2026-05-21

#### [Batch 14 用户反馈] Step 0 E 段"细线填充"自欺漏检 — fig126 教训再现

- **问题/发现 (R3-100 Batch 14, fig137 Whisper 用户复审)**：
  Encoder zone 右沿 x≈7cm，Decoder zone 左沿 x≈18cm，中间 ~11cm × 5cm 是大空白
  ——只有一条 orange cross-attention rail + "K, V" 标签穿过。
  sub-agent 在 ④.5 Step 0 E 段写"无 > 3×2cm 大块空白，Encoder 和 Decoder 之间由
  cross-attention rail 填充"——**自欺漏检**。
- **根因**：Step 0 E 段原条款只说"扫描大块空白"，没说**怎么算"已填充"**。
  sub-agent 把"有一条线穿过" = "已填充" 的 rationalization 顺利过了 self-check。
  fig126 是赤裸裸空白，fig137 是**伪装填充**——更狡猾，self-check 形式化通过。
- **解决方案（2026-05-21 三处修复）**：
  1. **`SKILL.md` Step 0 E 段加 (1a) 客观度量铁律 + (1b) 填充判定**：
     - (1a) 必须**写出怀疑区 x/y 范围 + 宽×高**（如"x=7-18 = 11cm × 5cm"），
       禁止抽象判断"无空白"
     - (1b) "已填充"定义：区域内有 ≥1 个 **box/text/嵌入 viz/标注块**；
       **细线（rail/leader/dashed/arrow）不算填充**，线占面积可忽略
     - 修复方向改为：**回 ① 重新规划布局**（拉近 hero / 中间加内容 / 改垂直）——
       **不是改 .tex**
  2. **`visual-review-checklist.md` Step 0 E 段同步 (1a)/(1b)**：阻止 sub-agent
     读 checklist 时漏新条款
  3. **本 lesson 沉淀**：未来 audit 关注"E 段判定标准是否客观可机械验证"
- **预期 Batch 15 验证点**：fig137 类布局（两个 hero 远距离 + 单条 rail）应该被
  Step 0 E blocker 并要求重新规划——不允许"rail 填充"过关
- **发现日期**：2026-05-21

#### [Batch 10 用户反馈] 短箭头 + rounded corners + 最小间距三连击
- **问题/发现 (R3-100 Batch 10, fig91-95 用户复审)**：canonical `arrow.style` 让短箭头出现"只有头的箭头"（tip 6.5pt + shorten 3pt 吃光 stem）；`rounded corners=5pt` 被 sub-agent 滥用在直线上产生"莫名其妙曲线"；重叠问题仍频繁（layout 时邻接间距没硬约束）
- **全网调研定位**：
  - [PGF/TikZ Arrows 官方手册](https://tikz.dev/tikz-arrows)：Stealth tip natural size 按 line width 0.4pt 时匹配 11pt x-height — 我们 1.0pt 线已是 natural 2.5x
  - [PGF Path Specifications](https://tikz.dev/tikz-paths)：「very short line segments → rounding may cause inadvertent effects」「lines suddenly extend over the other end」直接命中
  - [Node Overlap Removal (arxiv 2016)](https://arxiv.org/pdf/1608.02653)：业界 best practice 是 layout 时预防而非 detect-then-fix
- **解决方案（2026-05-19 三处修复）**：
  1. **`tikz-template.tex` 新加 `arrow short/.style`**：tip 3pt（`length=3pt 1.0`）+ line width 0.8pt + `shorten >=1pt, shorten <=0pt`。专用于 < 1.5cm 的短连接箭头
  2. **`SKILL.md` ③ canonical 表新增 `arrow short` 行 + "短箭头铁律"段 + "`rounded corners` 使用规则"代码示例**（✅ 多段折线 OK / ❌ 直线禁用）
  3. **`visual-review-checklist.md` 加 E13**（短箭头形状 + rounded corners 规范）和 **S9**（最小邻接间距强制扫描：同行 ≥ 0.8cm / 跨行 ≥ 0.6cm / text-box ≥ 0.3cm / 线-box ≥ 0.4cm）。计数 41 → 43
- **发现日期**：2026-05-19

---

#### [通用 · 元规则] 字号单向棘轮 —— 只给下限的规则会把版面挤爆

- **问题/发现（AST-GCN 图，用户复审）**：独立审查提出两条压力——「印刷字号不够」与「全图除标题外只有一个字号 = 模板感」。
  据此把 `\documentclass` 基准 10pt→11pt 并上调标题档位，**画布一动没动**。结果正文 CJK 6.5→8.0pt（+23%）、
  区标题 6.5→9.0pt（+38%）。每个框单看都更清楚，合起来全部顶满边框，用户直接判"最终版字太大，还是早期版好看"。
- **根因（四条，都在 skill 自身）**：
  1. **单向棘轮**：`data-visualization.md` 的最小字号表五行全是下限，且明写「加大框尺寸，不要缩小字」。
     checklist T4 只查截断（也是下限方向）。**TikZ 流程没有任何字号上限规则**——唯一那条
     「字号过大→扣分」躺在 `drawio-modes.md`，draw.io 专属，TikZ 图永远加载不到。
     于是"放大字号"在规则体系里是纯收益、零成本动作。
  2. **缺「目标印刷宽度」一级约束**：`textwidth`/`印刷`/`正文宽` 在 SKILL.md、step1、lessons、checklist
     命中数全为 0。step1 第 3 项只要求匹配"宽高比"，没有绝对尺寸。画布（cm）与字号（pt）两个绝对量
     的耦合完全缺席 → 画布定死后才发现印刷字号不够，此时**唯一还能动的就是字号**，动它必然破坏比例。
  3. **Philosophy 把层级绑死在 scale**：「Clear hierarchy through scale contrast」+「hero ≥ 2× 辅助 box」，
     从没提层级也可由字重/颜色/描边/留白构造。被批"只有一个字号"时，第一反应必然是放大。
  4. **Step 0 D 审美退步测试的三个例子全是几何**（对称丢/平行断/间距不均），
     "每处单看更清楚、合起来更挤"这种整体性退步不在视野内，18 项逐条自审全过。
- **解决方案（2026-07）**：
  - `data-visualization.md` 最小字号表 → **双向区间表**，并把「加大框尺寸」限定为"画布未定时"；
    画布已定时的正确动作是 缩短文案 > 改两行 > 重排，**禁止放大字号或框**
  - `step1-instructions.md` 新增 **3a 目标印刷宽度**（必填，不可跳过）+ 印刷字号基线表
  - `SKILL.md` 层级词条扩为 **尺寸/字重/颜色/留白/描边 五选二**，并注明画布已定时优先非字号手段
  - `visual-review-checklist.md` 新增 **T5**（撑框比例 ≤80% / 字号回归对比 / 印刷字号复核），18→19 项
  - `SKILL.md` Step 0 D 补「字号整体放大 / 文字撑框」，并要求动过字号时并列报两轮字号分布
- **元教训（比本条本身更重要）**：**只给下限、不给上限的规则 = 单向棘轮**。
  写任何"不得小于 / 至少 / 必须加大"的规则时，都要问一句「反方向失控会怎样」，并把上限一起写出来。
  同类嫌疑：「hero ≥ 2× 辅助 box」（没有上限）、「嵌入 viz 占框 60% 以上」（没有上限）。
- **发现日期**：2026-07-25

## 写入指引

新发现满足以下任一条件时追加到本文件：
- 编译错误经过 2 次以上尝试才解决
- 发现某类图的有效布局技巧
- 渲染结果与预期差异大需要调整方案
- 用户反馈指出反复出现的问题
- 验证出比当前基线更优的参数（更新 Part 1 表格，**只升不降**）

不要写入：
- 已被 `tikz-global-rules.md` / Python checker **完全覆盖且无新 narrative** 的内容（checklist 项的 narrative 上下文允许在 lessons.md 留存——但不要复述 checklist 的具体 Y/N 语言）
- 一次性的 latex 语法错误（应改文档而非积累故事）
- 未确认的猜测
- **测试协议 / 落盘格式 / 状态追踪 / 主题选择策略**——这些是 test harness 而非 TikZ 知识，不写入

**lessons.md 范围**：TikZ/draw.io 渲染技巧、图层选择、布局规则、参数基线、踩坑教训。专注图本身的视觉/几何质量。

#### [复杂图] - 残差 skip 线必须走 zone 之间的间隙，不能走 zone 内部

- **问题/发现**：Batch 17 fig153 v2：residual skip 连线设定 x=4.25（在 attention subzone 内，zone 左边=4.15），导致竖线穿过 Q/K/V 节点 → `line-through-node` 8 处。
- **解决方案**：残差 skip 竖线的 x 坐标必须落在 **hero 外框与 subzone 之间的间隙**（如 hero.left=3.8, subzone.left=4.15，则 skip x=3.97，落在间隙 [3.8, 4.15] 中）。同理右侧 skip x 落在 subzone.right 和 hero.right 之间。
- **发现日期**：2026-05-22

#### [嵌入 viz] - `dashed` zone 边框在 `pdf-overlap-checker` 中会误报 line-through-node

- **问题/发现**：`\draw[dashed] (x0,y0) rectangle (x1,y1)` 的水平边段会穿过 zone 内所有节点，触发 line-through-node。
- **处理方式**：这是已知语义误报。批量 ignore：`"N 处 line-through-node 全部来自 dashed 子区背景框与其包含节点的几何相交，属于 zone 边界设计而非路由错误"`。
- **发现日期**：2026-05-22

#### [嵌入 viz] - RoPE / GQA embedded viz 放置坐标需精确预算防 node-overlap

- **问题/发现**：RoPE viz 中心=(4.75,5.2), width=2.8cm → x范围[3.35,6.15]；GQA viz 中心=(7.65,5.2), width=3.0cm → x范围[6.15,9.15]。两个 viz 的 x 范围在 6.15 重合 → node-overlap。
- **解决方案**：放置 embedded viz 前先算出 (center_x ± half_width) 范围，确保两个 viz 之间间隙 ≥ 0.3cm。
- **发现日期**：2026-05-22

#### [数据可视化] - 热力图格子在 background layer 被可视化框填充色覆盖

- **问题/发现**：在 `\begin{pgfonlayer}{background}` 中绘制热力图格子（`\fill[heatDeep] ... rectangle`），同时用 `\node[viz_box, fill=zoneBlueBg]` 定义可视化框，框的背景填充覆盖了热力图格子（TikZ background layer 按代码顺序绘制）。渲染结果：heatmap 区域一片空白。
- **解决方案**：不用 `\node[viz_box, fill=...]` 定义可视化框，改用 `\draw[fill=..., draw=...]` 手动绘制框轮廓（置于 main layer），然后热力图格子用普通代码（main layer）绘制在框轮廓之后。这样格子永远在框背景色上方。核心规则：**热力图/柱状图等嵌入可视化必须在 main layer 绘制，不要放入 background layer**。
- **发现日期**：2026-05-22

#### [数据流水线图] - 柱状图 y 轴 scale 需所有面板统一

- **问题/发现**：RLHF 图中 3 个 benchmark 面板用了不同的 y 轴 scale（0-60% 对应不同 bar 高度），数值标签出现在轴线上方甚至溢出到图外，导致 text-overlap 和 text-overflow 错误。
- **解决方案**：多个并排柱状图面板必须用**统一的 y 轴 scale**（如 0-80%，统一换算公式 `height = value/max_val * axis_height`）。这不仅消除溢出错误，也让面板之间的比较更直观。
- **发现日期**：2026-05-22

#### [嵌入 viz] - hero 框内嵌入迷你 bar chart 位置需避开 sub-node

- **问题/发现**：RM hero 框内放了嵌入迷你 bar chart，初始 y 坐标与 sub-node (rmScore, rmEnc) 重叠，导致 text-overlap 错误（bar 标签与 sub-node 文字撞在一起）。
- **解决方案**：hero 框内有多个 sub-node 时，嵌入可视化应放在 sub-node **之间的空白区域**（x 和 y 都错开）。提前规划 hero 框内各元素的 x/y 坐标，留出迷你图的位置。
- **发现日期**：2026-05-22

#### [通用] - `\foreach` 内使用 xcolor 颜色名变量必定失败

- **问题/发现**：AlphaFold 图中氨基酸序列条用 `\foreach \col in {barBlue,...}` 循环，xcolor 无法在 `\foreach` 展开中解析多 token 颜色名（如 `barGreen`、`acaBlueLine`），触发 `! Package xcolor Error: Undefined color 'barGreen '`（注意末尾有空格）。同样问题出现在分子图原子颜色循环中。
- **解决方案**：凡是需要逐元素使用不同颜色的场合，**放弃 `\foreach` 循环，改为每个元素单独写 `\fill[barBlue!70,...] ... \node[...] {M};`**。代码量增加但编译稳定。共用颜色的循环（所有元素同色）不受影响。
- **发现日期**：2026-05-22

#### [数据流水线图] - 节点名包含小数点导致 "No shape named" 错误

- **问题/发现**：流水线底部摘要条用 `\foreach \xp in {0.6,4.1,16.0,...}` 生成节点，TikZ 把 `\xp` 值（如 `16.0`）直接用作节点名，创建名为 `pipe16.0` 的形状，之后引用时报 `! Package pgf Error: No shape named 'pipe16' is known`。
- **解决方案**：流水线节点名必须是合法标识符（字母/数字/下划线，无小数点、空格）。将循环改为逐个命名节点：`pipeA`、`pipeB`、`pipeC`、`pipeD`、`pipeE`、`pipeF`，用绝对坐标定位。或用 `\def\pipename{...}` 为每个位置单独定义名称。
- **发现日期**：2026-05-22

#### [复杂图] - hero 模块内部连线应绕边而非穿心

- **问题/发现**：AlphaFold Evoformer hero 框内 6 个 sub-node 堆叠（MSA Row Attention、MSA Col Attention、FFN、Triangular Attention、Triangular Mult Update、Pair FFN），连接 MSA 侧和 Pair 侧的内部反馈箭头直接垂直画，路径穿过中间 sub-node 的文字标签，pdf-overlap-checker 报 overlap WARNING。
- **解决方案**：hero 框内 sub-node 密集堆叠时，跨越多个 sub-node 的连线必须**从 sub-node 侧边绕行**（L 型路由）：先从起点 `.east` 或 `.west` 水平伸出 0.5-0.6cm（离开 sub-node 文字区），再垂直走到目标 y，再 `-|` 接回目标 `.east`/`.west`。不要直接 `.south` → `.north` 穿心连线。
- **发现日期**：2026-05-22
