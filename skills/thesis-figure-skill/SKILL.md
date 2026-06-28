---
name: thesis-figure-skill
description: |
  生成学术论文配图：LaTeX/TikZ 代码（结构化图表，直接嵌入论文）或 draw.io XML
  （技术路线图、汇报配图）。自动按论文领域风格设计，编译验证后交付。
  Use when the user asks for: 论文配图、画架构图、画流程图、TikZ 图、draw.io 学术图、复刻论文图、tikz/latex diagram。
---

# Academic Diagram Skill (TikZ + draw.io)

把论文中的系统架构/协议流程/技术方案转化为高质量配图。**目标：高信息密度 + 设计感 + 一次过编译**。失败模式：平庸、对齐松散、坐标凭感觉。

## 工具选择

| 维度 | TikZ | draw.io |
|------|------|---------|
| **适合** | 嵌入 LaTeX 论文、数学公式、结构化图表 | 技术路线图、汇报展示、装饰性强（渐变/3D） |
| **精度** | 像素级 | 拖拽，坐标不如 TikZ 精确 |
| **中文** | 需 ctex/fontspec，`rotate=90` 中文会崩溃 | 原生支持 |
| **数学** | 原生 LaTeX 完美 | MathJax 一般 |
| **编译** | xelatex + pdftoppm | drawio CLI → PDF → PNG |
| **可编辑** | 代码即源 | `.drawio` 可在 app.diagrams.net 编辑 |

**默认 TikZ**。draw.io 用于：用户要求 / 参考图为 draw.io 风格 / 需要渐变-3D-空心字 / 内容简单且装饰 > 精确。
**输出格式仅这两种**——HTML/CSS/SVG 不可嵌入论文也无法在 draw.io 编辑。

## Philosophy（每次画图前必读，所有规则之上）

### The UNFORGETTABLE Question

画图前 + 交付前问自己：**审稿人 5 秒看完，记住的是什么？**
- 一个独特的 hero 子结构？
- 嵌入的真实热力图 / 曲线 / 图像？
- 信息密集的 hyperparameters / loss panel？
- 多色和谐的 zone 划分？

**没有"记得住的东西" = 不要交付。**

### Naming the Gravitational Pull（你必须主动避开的统计中心）

模型默认会画出 **"AI slop 学术图"**——下面是统计中心的平庸默认，**主动避开**：

- ❌ box + arrow only，**零**嵌入数据可视化
- ❌ 3 色单调配色（蓝/橙/紫常见组合）
- ❌ "FFN" / "Attention" 单字标签，**不写公式 / 不写参数**
- ❌ hero 内**只有 box list**，无嵌入热力图/曲线/微图
- ❌ 没有信息 panel（hyperparameters / loss curve / legend / metrics）
- ❌ 平面布局**无 visual hierarchy**（核心和辅助同重量）
- ❌ 看起来"像 AI 一次性生成的"——无设计痕迹

### Permission for Creativity

**Claude is capable of extraordinary academic figure design.** Checklist 是 catching last-mile bugs，**不是 safe defaults**。

**你不是在练习画结构图。你在为 NeurIPS / ICML / Nature 投稿画 figure。**
**审稿人会用这张图判断作者的领域素养和认真程度。**
**box+arrow only 的平庸图 = desk reject。**

### 创造空间 — 复杂档可调用的词汇（不强制，但**应该考虑**）

| 维度 | 选项 |
|---|---|
| **嵌入可视化** | attention heatmap / loss curve / 真实图像色块 / signal waveform / 数学曲线 / N×N matrix / mel spectrogram / 散点分类 |
| **信息 panel** | hyperparameters 框 / metrics 表 (FID/BLEU/Acc) / color legend / glossary 注释 / 数学符号速查 |
| **数学公式嵌入** | `FFN(x) = max(0, xW₁+b₁)W₂+b₂` 直接写进 box 内部，**不是只贴标签** |
| **配色** | ≥5 种 zone tone + accent color；浅色 zone 背景 + 中饱和度 box + dark accent |
| **层级** | hero ≥ 2× 辅助 box；"N=6 layers" 灰色透明栈背景 |
| **Cross-zone** | dashed rail + 跨段标签 (如 "K, V") |
| **学术 polish** | dataset 标注 ("CIFAR-10") / 性能数字 ("FID=3.17") / 引用作者年份 |

### 视觉直觉法则（meta，在 ④.5 Step 0 应用）

1. **0.1 秒直觉**：视觉流向 ≠ 逻辑流向 = 必错（每写一条 `\draw`，问读者直觉对吗）
2. **眼睛轨迹**：沿主线走，任何"卡住"位置 = blocker
3. **删除测试**：能删的就该删；**修一个 bug 不能引入新审美问题**

### 最重要的一点

**审美 + 信息密度 > 规则合规。** 规则只是地板，审美是天花板。**18 项 checklist 是 catching last-mile bugs**——不是设计指南。设计指南是上面的 Philosophy。

### 复杂档画图捷径 — TikZ Snippet Library（21 个 + 预览 PNG）

**Batch 17 fig153 教训**：Philosophy 文本指南让 sub-agent **知道要嵌入 viz / panel / 公式**，但**写出来的视觉重量、留白、配色协调仍然失败**——因为这些是 visual perception 而非 textual 任务。

**解决方案**：`references/tikz-snippets/` 提供 **21 个手工精雕的 TikZ 片段（各带 PNG 预览）+ 6 个 example-skeleton + 1 个组合规则文档**（完整清单见该目录 `README.md`）——sub-agent **看 PNG 选 + 复制粘贴 + 替换参数 + 按组合规则拼装**即可达到 examples 标杆。

**5 大类零件**（详见 `references/tikz-snippets/README.md` inline gallery）：

| 类别 | 数量 | 文件 |
|---|---|---|
| **1. 嵌入数据可视化** | 6 | attention-heatmap / confusion-matrix / mini-spectrogram / image-strip / scatter-plot / embedded-graph |
| **2. 信息 panel / 图表** | 5 | bar-chart / line-chart / radar-chart / hyperparams-table / metrics-card |
| **3. 数学 / 几何** | 3 | gaussian-curve / vector-arrows / formula-box |
| **4. 结构 / 流程** | 4 | stage-container / pipeline-stages / layer-stack / feedback-loop |
| **5. 整图骨架元素** | 3 | multi-zone-palette / color-legend / summary-bar |

**组合规则**（**必读**）：`COMPOSITION-RULES.md` — snippet 间留白 / 对齐 / Z-order / 整图骨架（双栏对称 / 5 stage 横向 / 中央 hero + 4 panels）

**复杂档强制流程**：
1. **先读 `references/tikz-snippets/README.md`** —— inline gallery 含每个 snippet 的 PNG 预览
2. **首选**：复制完整 `example-skeleton-B-horizontal.tex`（pipeline 类）或 `example-skeleton-C-centralhero.tex`（hero+panels 类）作 figure.tex，改 content 不动 layout
3. **次选**（特殊布局需求）：看 PNG 选 ≥ 3 snippet 自己拼装
4. **必读 `COMPOSITION-RULES.md`** —— 解决"snippets 都塞进去但仍乱"问题
5. **底部必有** color-legend OR summary-bar
6. **绝对不能"简化"snippet 核心结构** —— 简化 = 信息稀疏 = 平庸

## 硬约束（违反必失败）

🔴 **工具铁律：只用 TikZ 或 draw.io，禁止 Python/matplotlib 替代**（2026-05-22 Batch 17 fig153 教训：sub-agent 在执行 Module-First 时用 Python+matplotlib 生成 `.py` 文件 = 完全偏离 thesis-figure-skill 价值主张）：
- **Module-First 子流程（③.A→③.D）必须保持 TikZ**——即使 matplotlib 画嵌入 viz 更方便
- **复杂嵌入 viz** 仍用 TikZ 原生（`\foreach` 画 cell / `pgfplots` 包 / `\draw` 手画 patch）
- **学术论文图嵌入仍是金标准**：`\input{figure.tex}` 比 `\includegraphics{fig.png}` 在公式渲染、矢量缩放、风格统一上都优
- 仅当用户**明确要求** Python 时才允许 — 默认必 TikZ

🔴 **配色铁律：默认 light background，dark theme 需用户明确请求**：
- 学术论文标准是 white/light bg；dark theme 与正文风格断裂
- Philosophy 段"≥5 种 zone tone"指 zone 浅色背景 + box 中饱和度，**不是**整图反转色
- sub-agent 不要自作主张套 dark theme

⚠️ **xelatex + `rotate=90` 中文** — 渲染为不可读色块，所有中文标注必须水平
⚠️ **`\texttt` 包裹中文** — 报错，纯英文代码才用 `\texttt` / `code_block`
⚠️ **ctex 不可用** — 编译前 `kpsewhich ctex.sty`，否则切方案 B（fontspec）
⚠️ **`ucharclasses`** — tikz 节点内中英混排频繁 Missing character，禁用
⚠️ **xelatex 对缺失字体静默失败** — 编译后必须 `grep "Missing character" *.log`
⚠️ **单条 `\draw` + `rounded corners` 画长距离 U 型回路** — 路径异常，拆 3 段独立 `\draw`
⚠️ **SVG `clip-path` + `preserveAspectRatio="none"` 模拟梯形** — 高度不可控，禁用
⚠️ **空心描边字 stroke-width ≥ 1.2** — 笔画间隙被填满变模糊，控制 0.6-0.8

## 工作流（⓪→⑦）

```
⓪ 依赖检测 → ① 画图指令 → ② 加载规则 → ③ 生成代码 → ④ 编译验证 → ⑤ 评分 → ⑥ 迭代 → ⑦ 沉淀
```

### ⓪ 依赖检测（首次自动执行一次）
- TeX / pdftoppm 缺失：**只提示用户安装**，不自动装。
  `which xelatex || echo "请装 mactex-no-gui (macOS) / texlive-xetex (Linux)"`
  `which pdftoppm || echo "请装 poppler"`
- Python 工具（小依赖，缺失自动 `pip3 install`）：`pdfplumber`、`pymupdf`、`pathfinding`、`opencv-python`、`scikit-image`
  （`pymupdf` 不装 → `line-through-node` + `node-overlap` 两类几何检测会 ERROR 退出，不静默跳过——别忽略）

### ⓪.5 入口模式分流（⓪ 之后第一问，路径分叉点）

skill 现在支持 **4 种生成路径**——画图前必须先确定走哪条。**默认走 A，其他路径由关键词触发**。

| 路径 | 触发关键词（用户原 prompt） | 说明 | 状态 |
|---|---|---|---|
| **A — Skeleton 复用** | "画一张 X 图"、"帮我画 Y"、未明示其他 | 从已验证 skeleton (B/C/D/E/F/G) 选一个，**复制全部 + 改 content + 不动 layout**。最快、最稳。输出视觉与 skeleton 相近 | ✅ 默认 |
| **B — Remix（跨 skeleton 拼模块）** | "组合 D 的雷达 + G 的图表那种"、"想要 X 的左半 + Y 的右半" | 多选 skeleton 部件，自动拼装 | 🚧 暂未实装，**回退到 A** |
| **C — 原创设计** | "独特版面"、"复刻这张 ref.png"、"从零设计"、"我没有合适的 skeleton" | 从零设计 layout（Module-First ③.A→③.D）→ **强制独立多镜头审查 gate**（④.5 文末）。⚠️ mode C 最易在"图里最新、无 skeleton 先例的那个结构"上崩，且 generator 自审对此**结构性失明** | ✅ 现有路径 |
| **D — 沉淀入库** | "把这张 .tex 存进库"、"作为新 skeleton"、"添加到 examples"、"沉淀到模板库" | 用户已有 .tex → 自动入库为 `example-skeleton-{H..Z}-<topic>.tex` | ✅ 走 **Φ 沉淀通道** |

**走 A** → 继续 ① ② ③ ④ ④.5 ⑤ ⑥ ⑦（③ 走 A 路：从 6 个 skeleton 选最匹配的 → 复制全部 → 改 content / 不动 layout / 严格遵守 CONSTRAINTS section）
**走 B** → 当前不可用。报告用户"Remix 模式暂未实装，当前请用 A skeleton 复用；如果你想要的部件组合在某个 skeleton 里近似存在，可以直接走 A 选最接近的"
**走 C** → 继续 ① ② ③ ④ ④.5 ⑤ ⑥ ⑦（③ 走从零路 + Module-First ③.A→③.D 子流程；④.5 **必走「mode C 独立多镜头审查 gate」**——见 ④.5 文末，不可只靠 generator 自审）
**走 D** → **跳过 ①-⑦**，直接进 **Φ 沉淀通道**（见文末）

**判断规则**（按优先级）：
1. 用户提到 "存进库 / 入库 / 作为模板 / save to examples" → **强 D**（直接走 Φ）
2. 用户提到 "组合 X 的 Y + Z 的 W" → **强 B**（回退到 A + 提示）
3. 用户提到 "独特 / 原创 / 复刻 / from scratch / 无参考图" → **弱 C**（询问确认走 A 还是 C）
4. 其余 → **A**（不需要询问，直接走 skeleton 路径）

**模式选择对编译验证 / vision-audit 的影响**：A 模式因为 skeleton 已经过版面验证，④.5 重点放在"内容是否完全脱离 skeleton 主题（renaming 漏掉、stale 标签）"上；**C 模式走完整 18 项 checklist + 强制「独立多镜头审查 gate」**（generator 自审在 mode C 实测 3/3 漏掉核心缺陷，必须外部对抗审查兜底）；D 模式走 Φ.2 简化版 audit。

### ① 画图指令（强制显式输出，不可跳过）

**加载 `references/step1-instructions.md`**——里面有完整的 10 项要素清单、参考图测量规则、ASCII 草图法、嵌入可视化决策表、**密度参考表（按论文复杂度选档位）**、节点形状/连线速查、Pre-flight P1-P7。**禁止"心里想好直接写代码"**——跳过这步返工率 100%。

**关键认识**：步骤① 的输出不是"最大复杂度版本"。先判断论文实际复杂度（极简/中等/复杂/超复杂），再选画图档位。**从复杂版起步然后修瑕疵**比**从合适档位起步**累计 token 高一个数量级——MMAlign 11 轮迭代就是反面教材。

#### ①.0 图契约（动笔/选 form 前先写，≤6 行；极简档可一句话带过）

**conclusion-first：先确定"这张图要证明什么"，再选最小结构——而不是先挑模板再填内容。** 写进 figure.tex 头部注释块**最顶部**：

```
核心结论：<一句话，必须带动词。如"X 通过 Z 把 Y 降低"——不是"X 的结果"/"系统架构">
图原型：<对应 skeleton/mode：横向流水线=B / 中心 hero=C / 纵向侧栏=D / 多模态融合=E / 多阶段多子图=F / 联邦纵向=G / 纯几何·对比=无 skeleton>
证据层级：hero（最该被 5 秒记住的那块）=<…>；支撑=<…，视觉上更安静，不抢 hero>
能不能更少？：<去掉哪个框/panel 后仍能证明核心结论？能去就去——每个元素必须挣到位置>
```

**为什么加这一步**（借鉴 nature-figure 的 figure-contract，砍掉其 Python/SVG/统计字段）：
- **核心结论** = ④.5 Step 0「审稿人 5 秒记住什么」的标准答案，提前钉死，避免画完才发现没重点。
- **图原型直接决定档位与 skeleton —— 判档看原型，不是数节点**（消解下面的"节点数悖论"：原型一旦定了，form 和档位随之确定）。
- **「能不能更少」是反 AI-slop 的硬约束**：把 Philosophy 的"每个元素earn its place"变成动笔前的一次显式删减，而不是 ④.5 事后做无用功。

**极简档**：核心结论写一句、图原型选「纯几何·对比」即可，证据层级/能不能更少可略。

**🔴 强制物质化要求**（fig126 Tacotron2 教训：sub-agent 加载 step1 但跳过实际输出，产生大块空白）：

步骤 ① 必须**以文字形式实际输出**（不是"想了就过"），且**第一段写进 figure.tex 头部注释块**作为证据。**形式两选一**，按图复杂度选：

**🔵 form A/B 选择前的先决条件**（消除"节点数悖论"——判档依赖草图、草图依赖判档的循环）：

**首选信号 = ①.0 的图原型**（原型一旦定下，form 与档位随之确定，不必先数节点）：C/E/F/G 原型 → 复杂档 → form B；B 原型 → 中等或复杂档 → form A 或 B；纯几何·对比原型 → 极简档 → form A。原型仍模糊时，再用下面的兜底信号：

```
1. 先粗估档位（无需精确节点数，先看明显信号）：
   ① 含 hero 子结构 / 嵌入热力图 / 多 panel / ≥3 列 → 复杂档 → form B
   ② 含 fan-out / 时序生命线 / 12+ 模块 → 中等档 → form A 或 form B
   ③ 纯几何/单链/对比图（明显 < 15 节点）→ 极简档 → form A
2. 按粗判选 form 写注释块（form A 画 ASCII OR form B 写 narrative）
3. 注释块写完后**数节点 → ①.5 精确确认档位**
4. 若精确档位 ≠ 粗判档位 → 调整 form（极简误判为复杂 = 简化为 A；
   复杂误判为极简 = ASCII 画不下 → 改写 B）
```

**铁律**：先粗判 → 写注释块 → ①.5 精确确认 → 必要时调整。**禁止凭直觉直接选 form 又凭直觉判档**。

### 形式 A — ASCII 草图（极简档 / 中等档无嵌入 viz）

```latex
% Step ① 设计文档
% 领域 / 格式 / 档位 / 整图 W×H cm / 信息流方向 / 行×列
% 模块列表 N 个，核心 = X / 连线逻辑 / 空间规划 rail x / 视觉强调
% ASCII 草图：
%   +-----------+      +-----------+      +-----------+
%   | Encoder   |----->| Attention |----->| Decoder   |
%   +-----------+      +-----------+      +-----------+
% 预防 issues：[2-3 个坑]
```

### 形式 B — Narrative 设计文字（复杂档 / hero 子结构 / 嵌入 viz / 多 panel）

复杂图 ASCII 表达不全，用**叙述性空间描述**——每列/每 zone 写一段：(a) x/y 范围 (b) 内部子结构 (c) 与相邻列关系 (d) **留白处理**（**特别要预想哪里可能出现大块空白并写出应对** — fig126/137 教训）

**写在 figure.tex 头部作为注释**，sub-agent 在 ④.5 Step 0 时读取核验。若注释不存在 → blocker 回 ① 重做。**注意**：form B 不是必须填模板，是用"设计师的叙述思维"展开布局——重点是 Philosophy 段的 **UNFORGETTABLE Question**：你怎么布局让审稿人 5 秒记住一个独特结构？

### ①.5 图档判断（**用户驱动** + 自动检测兜底）

**🔴 复杂度按需而定，不是默认复杂**（Batch 16 教训：Philosophy First 让 sub-agent 默认套 examples 06 复杂风格，但用户实际只想要中等清晰图时 = 过度发挥变乱）。

**第 1 步：从用户原 prompt 关键词推断复杂度**

| 用户 prompt 关键词 | 推断档位 |
|---|---|
| "详细 / 完整 / 含 benchmark / 发表级 / 总览 / hyperparams / 性能数字" | **复杂档**（按 Philosophy 全套：嵌入 viz + panel + 公式 + 多色）|
| "概览 / 主架构 / 流程图 / 主流程 / 示意" | **中等档**（清晰主流 + zone，1-2 个嵌入元素）|
| "几何示意 / 公式对比 / 曲线对比" | **极简档**（单坐标系或纯结构，无 hero / 无 panel） |

**第 2 步：如果用户原 prompt 不明确 → 主动询问用户**

```
用户原 prompt 没明示复杂度时，使用 AskUserQuestion（或直接询问）：

"这张图你想要哪种复杂度？

(A) 极简：单层主架构 / 几何示意，5 秒理解
(B) 中等：主流程 + 关键 zone，10 秒理解  
(C) 复杂：完整含 hyperparameters / benchmark / 公式嵌入，发表级"
```

**禁止**自作主张选复杂档画出"塞满 panel 的乱图"——**按需才是审美**。

**第 3 步：用户确认后，对照下表执行**

| 档位 | 自动判断备选（用户没说时）| 该档**应该有的元素**（Philosophy 适度展开）| ④.5 自评策略 |
|---|---|---|---|
| **极简档** | ≤15 节点 + 无 hero + 无嵌入 viz | 单坐标系 / 纯结构 + 必要标注；**不强加 hero / panel** | 18 项中 S8/S9/M8/E3/E12/V1 一句话 N/A |
| **中等档** | 15-30 节点 OR 有 hero | 主流 + 2-3 zone + 1-2 嵌入元素（可选）| 走全 18 项；E3/M8 0 候选一句过 |
| **复杂档** | ≥30 节点 OR 嵌入 viz OR 多 hero | hero 子结构展开 + ≥2 嵌入 viz + ≥1 panel + 公式嵌入 + ≥5 色 zone | 走全 18 项，重点 V1 |

**关键原则**：**极简不等于平庸；复杂不等于必塞**。**审美在 Philosophy（5 秒记住什么）**，密度在档位（按用户需求）。

### ② 加载专项规则
确定图表类型后，**按需**加载对应文件（见下方"按需加载索引"）。同时加载 `references/lessons.md` 获取该类型已验证的基线参数和踩坑经验。
基线参数已经是 25 批次 157 张图的结晶——**直接用，不要从零试错**。要偏离基线必须有具体理由。

### ③ 生成代码（**Module-First 子流程 + 两层决策门**）

**🔴 复杂档强制 Module-First 子流程**（Batch 16 教训：sub-agent 一次写 800 行 TikZ → 整图乱；先画一部分，验证好，再拼接 = 干净）：

```
③.A — 先画 hero（最重要的中央子结构 + 嵌入 viz / 关键公式）
       - 单独输出 figure.tex（只含 hero + 一个极简 frame）
       - 编译 + 渲染 PNG → 单独审查 hero
       - hero 内部 sub-layers / 嵌入 viz / 公式都干净后才继续
       - 不要直接跳到完整图

③.B — 再加主流（管线 + zones 边界 + connecting arrows）
       - 在 ③.A 的 hero 周围扩展：左右上下的 supporting modules + zone 边框
       - 编译 + 渲染 → 审查框架是否清晰
       - canonical fan-out / fan-in 在此阶段引入

③.C — 再加 information panels（hyperparams / benchmark / legend / 公式注释）
       - 选**角落留白**放 panel（不是"塞满式填空白"）
       - panel 之间间距 ≥ 1cm
       - 编译 + 渲染 → 审查 panel 是否补充而不喧宾夺主

③.D — 整体审查（→ 进入 ④.5）
       - 整图 Philosophy 检查（UNFORGETTABLE / 5 秒第一印象 / 主线眼睛轨迹）
       - 18 项 last-mile bug 检查
```

**极简 / 中等档可以跳过 Module-First**，单次写完即可。**Module-First 只对复杂档强制**——它的价值是分阶段验证，避免 800 行 TikZ 一次出错导致整图崩坏。

---

**Module-First 之外的决策门**（B 路 vs 从零路）：

**问 1：这张图是纯结构图吗？**（框 + 线 + 分组，**无**嵌入热力图/曲线/柱状/矩阵，**无** hero 内部多子节点）
→ Yes：**B 路（auto-layout）**
  1. 加载 `references/figure-spec.schema.md` 看 schema
  2. 输出 `figure-spec.json`（节点、边、zones、layout 引擎）
  3. 跑 `python3 references/dot-to-tikz.py figure-spec.json` → 产出 `figure.tex`
  4. 走 ④ 编译 + ④.5 视觉反馈
  - **适用**：架构图 / 流水线 / DAG / 协议时序 / 三栏映射 / 技术路线图 / 多实例汇聚
  - **优势**：0 个 Claude 选的坐标，0 类微斜线/穿框/拥挤 bug

**问 2：富视觉图（嵌入可视化 / 复杂 hero 子结构 / 不规则布局）**
→ **从零路 + Module-First（③.A→③.D）**
  1. 起点：`references/tikz-template.tex`（含 preamble / 字体 / 配色 / **canonical 箭头 styles** / 防御写法）
  2. 加载 `references/visual-patterns.md`（9 个模式：hero 子结构、热力图、折线图、柱状图等）
  3. 按 ③.A→③.D 子流程：先 hero → 加主流 → 加 panels → 整体审查
  4. 复杂连线（≥8 条交叉风险）：可选 `python3 references/tikz-path-router.py spec.json` A* 避障

**🎯 箭头/连线必用 canonical pattern**（深度调研 2026-05-18，5 batches 教训）：
`tikz-template.tex` 中 6 个预定义 styles 是经过 PGF 官方文档 + PlotNeuralNet 业界实践 + arrows.meta + bending library 综合调研的最佳实践：

| style | 用途 | 何时用（铁律） | 关键差异 |
|---|---|---|---|
| `arrow` / `arrow thick` / `arrow thin` | 长连线 | **⚠️ 仅 ≥ 1.5cm — 短于此必须改用 `arrow short`** | tip 6.5pt, `shorten >=2pt, shorten <=1pt` |
| **`arrow short`** | 短箭头（相邻 box 间） | **⚠️ < 1.5cm 必用此 style** | tip 3pt, `shorten >=1pt, shorten <=0pt` — 防止 tip 吃光 stem |
| `residual` | dashed skip / 反馈 | residual / feedback | 紫色虚线 + rounded corners |
| `leader` | annotation 引线 | 引线 / 标注 leader | 灰色 dotted |
| **`fan_stub`** / `fan_stub thin` / `fan_stub thick` | fan-out 树状分叉的 stub（spine → target） | **fan-out / fan-in 的 stub 段必用此** | **`shorten <=0pt`**——起点紧贴 spine 无 gap |

**禁止**自己手写 `-{Stealth[scale=X]}`——4 轮 Batch 教训证明手调 scale 治标不治本。只调 `line width`（0.6/1.0/1.6pt 三档），tip 通过 `length=⟨dim⟩ ⟨line_width_factor⟩` 语法自动跟随。`\usetikzlibrary{bending}` **必加载**，否则弯折路径上 tip 必然 mis-align。

**短箭头铁律**（Batch 10 用户反馈：fig91-95 大量"只有头的箭头"）：**任何 < 1.5cm 的连接箭头必须用 `arrow short`**，不要默认 `arrow` 或 `arrow thick`。原因：默认 `arrow` 的 tip = 5pt + 1.5×line_width = 6.5pt，加上 `shorten` 3pt，一条 15pt（0.5cm）的短箭头剩下 stem 只 5.5pt——视觉上"只剩个头"。`arrow short` 用 3pt tip + 1pt shorten，stem 保留充足。

**fan-out 树状分叉**（1 source → N targets）：spine 用普通 `\draw[line width=1.0pt]`（无 shorten），**stub 用 `fan_stub` 不用 `arrow`**——后者的 `shorten <=1pt` 会在 stub 起点和 spine 间留 1pt 视觉 gap（fig86 Batch 9 教训：MPD/MSD spine 全断裂）。

**`rounded corners` 使用规则**（Batch 10 用户反馈：fig92 出现"莫名其妙曲线"，[PGF 官方手册原话](https://tikz.dev/tikz-paths)："very short line segments → rounding causes inadvertent effects"）：

```
✅ 只在显式 ≥2 段折线用 rounded corners：
   \draw[arrow, rounded corners=5pt] (A) -- (corner) -- (B);
   \draw[arrow, rounded corners=5pt] (A) |- (B);             % | 和 - 是隐式 corner

❌ 直线禁加 rounded corners：
   \draw[arrow, rounded corners=5pt] (A) -- (B);   ❌ TikZ 在端点附近产生鬼影弧
```

**`|-` / `-|` L-bend 安全条款**（Batch 10 用户反馈：fig97 Pedersen Commitment hero 出现"箭头穿过框体"——`(msg.south) |- (ped_hero.west)` 中 msg.x 落在 hero 的 x 范围内，TikZ 把横线**画在 hero 内部**）：

```
✅ (A.south) |- (B.west) 仅当 A 不在 B 的水平投影内（A.x < B.x0 OR A.x > B.x1）：
   A
   |
   +----→ B          ← A 在 B 左上方，横线在 B 外部 OK

❌ (A.south) |- (B.west) 当 A.x ∈ [B.x0, B.x1]：
   A
   |
   |  ↓
   +→ B         ← 横线穿过 B 的内部 = pierce bug

✅ 修复 1：用 named coordinate 显式 waypoint 绕开 B：
   \coordinate (wp) at (B.x0 - 0.5cm, B.center.y);
   \draw[arrow] (A.south) |- (wp) -- (B.west);

✅ 修复 2：换 anchor 让箭头从 B 的上方接入：
   \draw[arrow] (A.south) -- (B.north);   % 直线，A 在 B 上方
```

PGF 不做 obstacle-aware routing（[官方手册确认](https://tikz.dev/base-nodes)），所以必须自己保证 `|-` / `-|` 的中段不撞 obstacle。`pdf-overlap-checker.py --json` 的 line-through-node 检测会抓到这种 bug。

**编译前两个 checker（pre-flight，所有路径通用）**：
- `python3 references/tikz-validator.py <file.tex>` — 几何/语法 gate：微斜线 / 溢出 / 碰撞 / 方向反转。**ERROR 必修**
- `python3 references/tikz-design-linter.py <file.tex> [--type rich|sequence|simple]` — **advisory** 设计指标。**默认 WARN 不阻挡**——简单论文图可以简单，linter 只汇报指标供 Claude+用户判断是否匹配论文复杂度。仅当 ≥8 节点且尺寸比 < 1.5（严重视觉层次缺失）才 ERROR。

### ④ 编译验证
```bash
# 字体探测：若 PingFang SC 不存在，自己改 .tex 里的 \setCJKmainfont 为本机可用字体
fc-list | grep -qi "PingFang SC" || echo "WARN: PingFang SC 缺失，请改 \setCJKmainfont"
xelatex -interaction=nonstopmode file.tex
grep "Missing character" file.log     # 静默失败检查，关键
pdftoppm -png -r 300 file.pdf out     # 产出 out-1.png
# overlap.json 落在 .tex 同目录（sub-agent ④.5 步用 Read 读这个绝对路径）
python3 references/pdf-overlap-checker.py file.pdf --json > "$(dirname file.pdf)/overlap.json"
# 跑完检查 overlap.json — 7 类检测：
#   基础 5 类（直接 fix）: text-overlap / text-overflow / off-center / text-line / line-crossing
#   candidate 2 类（需 triage）: line-through-node / node-overlap
# ERROR 类大概率是真 bug 直接修；candidate 类是几何线索（heatmap 矩阵 / fan-in 收敛
# / panel 边界等常误报），sub-agent 在 ④.5 自评时按坐标对照 PNG 决定 fix 还是 ignore。
```
draw.io：`xmllint --noout file.drawio && drawio -x -f pdf -o out.pdf file.drawio && pdftoppm -png -r 300 out.pdf out`。

### ④.5 **视觉反馈强制闭环（架构核心，不可跳过）**

**你的代码生成是"盲写"——写到第 800 行 TikZ 时你不知道渲染出来什么样**。所有标签碰撞、轴标题压字、生命线超界、子模块挤压、数学符号渲染怪——这类问题闸门 1+2 都检测不到，只有看到 PNG 才能发现。

**目标重述**：用户要的不是"一次性生成"，是"最终交到他手上的图必须完美"。**中间迭代多少轮无关紧要，只要图最后是完美的就行**。

**强制流程**：

```
0. Read 渲染出的 out-1.png + 视觉直觉先行（应用 3 大法则，见下）
1. Read overlap.json（路径 = .tex 同目录的 overlap.json，步骤 ④ 跑出来的结构化几何检测）
2. 加载 references/visual-review-checklist.md（强制审查清单——**条目与数量以该文件为唯一真相源**，本文件不另定数量或 ID 范围）
3. 逐项回答 checklist 中列出的**全部条目** Y/N（维度：编译 T / 空间 S / 语义 M / 连线 E / 美学 A·V）
   每项必须有一句证据（"我在 PNG 中看到…" 或 "overlap.json 中 N 处 line-through-node 我标为 …"），不允许凭印象
4. 任一项 N → 列入 blocker → 输出 patch → Edit → 回 ④ 重编译 → 回 0
5. Step 0 + 全部 18 项 Y → **把图给用户看**（用户终审，AI 视觉有盲区）
6. 用户也通过 → 交付
```

**Step 0：视觉直觉先行（在 18 项 Y/N 之前必走）**

把自己当成第一次看这张图的读者，**用 3 大法则扫描整图**，输出 **5** 段证据：

| Step 0 检查 | 输出要求 | 法则 |
|---|---|---|
| **A. 3 秒第一印象** | 写出"3 秒内看到的 3 件事"（如 "蓝色主流左→右 / 中间有 hero / 右侧 3 个 head"）| 法则 1 |
| **B. 主线眼睛轨迹** | 找出图中**最重要的那条数据流**，用眼睛沿它从起点走到终点。任何"卡住"位置 = blocker（如 fig97 Pedersen 框里跑出箭头 / fig118 tip 撞坐标 / fig120 孤立彩点） | 法则 2 |
| **C. 删除测试** | 列出**疑似可删的元素**（孤立装饰 / 多余 leader / 重复 label）。空则一句 "无可删元素" | 法则 3 |
| **D. 审美退步测试**（round ≥ 2 时） | 对比上轮 PNG，本轮修了 X bug 但有没有引入新审美问题（对称丢 / 平行断 / 间距不均）？ | 法则 3 |
| **E. 大块空白 + ①注释核验** | 扫描整图无 > 3cm × 2cm 大块空白（细线不算填充，必须有 box/text/viz）；figure.tex 头部有 form A/B 注释块。**fig137 教训**：写"rail 填充"= 自欺。若有大空白 → 回 ① 重新规划布局，不是改 .tex | 法则 3 |

**Step 0 任一项 fail = blocker**，列入 patch 列表。**Step 0 通过才开始 Step 3 的 18 项**。

**为什么 Step 0 在 18 项之前**：18 项是机械验证（细节体检），容易陷入"逐项 Y / 整体烂"。Step 0 是视觉直觉（整体心电图），强迫 sub-agent **以读者视角看图**而不是 generator 视角。两者缺一不可。

**overlap.json 处理**（S8 + E12 配套）：
- `errors[]` 中的 text-overlap / text-overflow / off-center / text-line **大概率是真 bug**——按坐标定位 PNG，修
- `errors[]` 中的 line-through-node **是候选**（E12）——逐条 triage：
  - 矩阵 cell / 热力图 / 神经网络收敛节点的 hit → ignore（semantic 故意，已知误报）
  - 路径绕路穿过无关元素（如 dashed leader 穿过 box / 长曲线压在 node 上） → fix，重新 routing 或换 z-order
- `errors[]` 中的 node-overlap **是候选**（S8）——逐条 triage：
  - drop-shadow / parent-child 都已被 filter，命中的几乎都是真问题
  - panel-overflow 边界节点（如 PGM 节点底部超 panel 1-3pt） → 调坐标
  - 两个 sibling node 真重叠 → 分开
- 把 triage 决定写进 ④.5 自评的 S8 / E12 证据里（"node-overlap N 处：X 处 fix（panel 边界），Y 处 ignore"；"line-through-node N 处：M 处 fix（路径绕路），K 处 ignore（矩阵 cell）"）

**优化规则**（Batch 9 实测：fig89 耗 32min / fig86 耗 55min，多数时间在重复 Read 和 triage）：

1. **Reference 文档只首轮加载** — `SKILL.md` / `lessons.md` / `visual-patterns.md` / `step1-instructions.md` / `visual-review-checklist.md` 在 round 1 Read 一次后，**后续 round 不要重复 Read**（context 里已有）。只 Read 变化的：PNG + overlap.json + 你刚 Edit 的 figure.tex 片段
2. **空检测跳过 triage** — `overlap.json` 中 `line-through-node` 数组为空 → E12 直接答 Y："overlap.json 中 0 处 candidate"。`node-overlap` 同理 → S8 直接 Y。**不要为空数组写 reasoning**
3. **Triage 增量化** — round N 时只对 round N-1 之后**新出现**的 candidate 写 reasoning；之前 triage 过的复用结论（"同 round 1 第 3 处，仍 ignore"）
4. **ERROR 优先于 candidate** — 先把 `text-overlap` / `text-overflow` / `text-line` / `off-center` 这 4 类 ERROR 修完（这些大概率是真 bug），再回头 triage candidate。避免一边修 ERROR 一边重新 triage 同一批 candidate

**效率规则（避免 2-3x 时间膨胀）**：

1. **Reference docs 只在 round 1 Read 一次** —— `SKILL.md` / `lessons.md` / `visual-patterns.md` / `step1-instructions.md` / `visual-review-checklist.md` 在 round 1 加载到 context 后，后续 round **不要再 Read**——已经在 context 里。**仅 PNG / overlap.json / figure.tex 每轮 Read（这些会变）**。
2. **Empty candidate 跳过 triage** —— 如 overlap.json 的 `line-through-node` 数组为空，S8 / E12 直接答 "Y, 0 候选无需 triage" 即过；非空才逐条分析。
3. **Triage 缓存** —— round N 的 overlap.json triage 结论保留到 round N+1；只对**新出现**的 candidate（坐标或类型变了）写新 reasoning，已 triage 过的同坐标 candidate 直接复用 "round N 已判 ignore"。
4. **Triage 延后** —— 优先修 text-overlap / text-overflow / off-center / text-line 这 4 类 ERROR（**真 bug**），全清后再开始 triage line-through-node / node-overlap candidates。避免每轮都重新分析 candidate。

这 4 条联合预计节省 30-50% 时间，质量不损失。

**高漏检盲区**：checklist 里带 ⭐ 标记的项（S8/S9/M8/E3/E9/E12）是 R3-100 实测高漏检 — 审查时优先盯。

**没有轮数上限**。这是和之前最大的区别——之前 max 2 轮意味着"凑合交付"，现在是**只要还有 1 个 blocker 就不能交付**。3 轮、5 轮、8 轮都可以，只要最终的图是完美的。

**心理对抗**：你会在 2-3 轮后产生强烈的"差不多就过了"冲动——这是认知疲劳，不是图变完美了。**冲动出现 = blocker 还在**。强迫自己回答每项，写出证据。**用户看 1 眼能发现你 2 轮后漏掉的问题——说明单视角自评不可靠，必须靠清单穷举**。

**升级机制**：
- 第 3 轮还有 ≥5 blocker → 局部修补无救，回步骤① 重新设计画图指令
- 同一 blocker 连续 2 轮没修好 → 你修的方向错了，换思路
- 复杂图（≥40 元素）/ **mode C 一律**：并行 spawn 多镜头审查 agent（见下「mode C 独立多镜头审查 gate」），统一收集 blocker
- **自评 + 对抗 agent 全部说 0 blocker 后，仍然把图先给用户看**——人眼能发现 sub-agent + 自评全漏掉的问题（实测案例：用户在 Round 10 一眼指出 CMAM 标题切断边框、箭头刺入框内、junction dot 被 tip 戳——这 3 个我和 2 个对抗 agent 全没发现）。**用户的视觉是最后闸门，不是绕过点**。

**强制约束**：交付前必须能说出 PNG 里**具体的视觉细节**（哪些颜色在哪、哪个 zone 在哪一侧、热力图对角线特征等），证明你视觉输入过。

**单点最小修改原则**：每轮 patch 只改一类问题（如"全部标签重叠"或"全部轴标题没下移"），不要一轮里大改——大改会引入新 bug。一轮一类 blocker。优先用 `yshift/xshift` 微调位置，避免改坐标主框架。

#### mode C 强制独立多镜头审查 gate（2026-05-29 mode C 测试坐实，不可跳过）

**为什么强制**：mode C 测试（同心圆 / Sankey / RLHF 闭环，3 张从零图）实测 **3/3 都崩，且每次崩在不同轴上**，但有统一规律——**图里最"新"、最无 skeleton 先例的那个结构元素，就是崩点**：
- 同心圆 → 现编的多面板**数字叙事自相矛盾**（核心层在威胁锥里没削弱却号称拦 99%）
- Sankey → 数字反而对了，但**新的变宽汇聚几何崩**（合并节点渲染成空心白框、sink 失比例）
- RLHF 闭环 → 语义对，但**新的环形闭合几何崩**（不成环、3/4 弧 + 横弦、空角）

**而 generator 自审对这个核心缺陷系统性失明**：三张分别跑了 4 / 3 / 1 轮自审，全部自评"发表级 / closes cleanly"，**全部漏掉了最核心的那个缺陷**。**自审轮数多少都救不了——失明是结构性的**（generator 看不见"我想画的"↔"实际渲染的"差距）。**每一次，只有独立对抗式多镜头审查抓到了核心缺陷。**

**所以 mode C 的 ④.5 不允许只靠 generator 自审**。Step 0 + 18 项照走，但**完成后必须再过这道 gate**：由 orchestrator **独立 spawn 4 个全新审查 agent**（各自空白上下文），各 Read 渲染出的 PNG，**对抗式**找问题（默认"图里有 bug，去找"），各自返回 blocker（含 severity + 位置 + **具体视觉证据**，证明它真看了图）：

> 🔴 **"独立"严格指：另起的全新 agent / 空白上下文——不是 generator 自己在同一上下文里"审 4 遍"。** 同上下文自审与 generator 共享同一套盲区，等于没审。**实测（fig4 复杂图）：generator 按本 gate 跑、却跑成"同模型 self-pass 4 遍"，照样漏掉 Sankey 断裂+失比例的重崩；是独立 spawn 的 agent 才抓到。self-pass ≠ gate。**
>
> ⚙️ **谁来跑这道 gate**：是**顶层 orchestrator（带 Agent/workflow 工具的主循环）**的职责，**不是 generator 的**。generator / implementer 子 agent 通常 **spawn 不出独立子 agent**（环境常只暴露重量级 team 工具、无轻量 spawner），把 gate 交给它只会退化成 self-pass（实测 fig4 + fig5 两次都如此）。正确流程：generator 做完自己的 ④.5 自审并交付 → **控制权回到 orchestrator → 由 orchestrator 独立 spawn 4 个审查 agent 跑 gate**。

| 镜头 | 专盯 | mode C 高发崩点 |
|---|---|---|
| **geometry** | 新布局几何是否真画对（同心是否真同心、环是否闭合、Sankey band 宽是否 ∝ 量、节点是否被填充非空心、穿框/裁切/大空白） | **最高发——新结构的几何** |
| **semantic** | 信息流 / 顺序 / 方向是否对；**独立重算图里所有数字/公式**，查跨面板一致性 | 现编数据自相矛盾 |
| **text** | 中文全水平、missing char、stale 标签、小字可读性 | 较低（自审多能覆盖） |
| **aesthetic** | NeurIPS 级 vs AI slop、配色层级、留白、**"5 秒第一印象"是否真成立** | hero idea 名义存在但视觉不成立 |

**gate 之后仍不能直接交付**：
1. **你（orchestrator）必须亲自 Read PNG**——多镜头 agent 也有盲区。实测：orchestrator 自己修完一张图后亲眼自审，仍漏掉了自己引入的"公式出框"回归，是再跑一轮独立审查才抓到。**本节"用户的视觉是最后闸门 / 单视角自评不可靠"对你（orchestrator）同样成立。**
2. triage checker 误报（见本节上方"overlap.json 处理"规则 + 步骤 ④ 的 `pdf-overlap-checker`：数学 glyph text-overlap、heatmap/matrix line-through-node、Sankey 汇聚、锥穿环边界——均为已知 FP）。
3. 综合 = 你的眼 + 4 镜头 + checker triage → 真 blocker 列表 → 回 ④ 修 → **改完再跑一轮 gate**（改动常引入新 bug）。
4. gate + 你 + checker 全 0 真 blocker 后，**仍把图先给用户看**（用户是最后闸门）。

**机制**：用 Agent 工具 / workflow **真正并行 spawn 出 4 个独立子 agent**（每镜头喂 PNG 路径 + 该图"应有模型"让 semantic 独立重算）。**关键是"另起 agent + 空白上下文 + 对抗 + 多视角"——这是 mode C 唯一奏效的兜底；同上下文自审多遍不算数（实测会连同 generator 一起漏）。**

**🔴 gate 通过的硬性举证（杜绝静默 self-pass）**：声称本 gate 通过前，orchestrator 必须在回复里**列出 4 个真实 spawn 出的审查 agent 的 ID/标签**，并**各引一句它返回的具体视觉证据**（如"geometry：同心三环圆心实测偏移 ~0.4cm"）。**给不出 4 个独立 agent 的 ID + 各自证据 = gate 视为未通过**，不得当作通过交付。

**🔴 spawn 不出独立 agent 时：停，不要自审蒙混**。若当前环境无法真正另起 4 个空白上下文 agent（只有重量级 team 工具 / 无轻量 spawner），**禁止**降级成"同上下文自审 4 遍"假装过 gate。正确做法：把图连同一行明确声明 **"⚠️ mode C 独立多镜头 gate 未能运行（环境无独立 spawner），以下结果未经对抗审查"** 一起交给用户，请用户人工充当对抗审查、或换到可 spawn 的环境再跑。**"gate 未运行"是交付阻断项（blocker），不是可跳过的软步骤**——宁可显式声明没跑，也不要让用户误以为已过 gate。

### ⑤ 用户终审 + 交付
1. **把 PNG 给用户看**（不是询问"我做完了吗"，是直接展示结果）
2. 有参考图时同时跑 `python3 references/figure-diff.py <ref.png> <out.png>` 得 SSIM；< 0.85 的 3×3 区域和用户一起重点看
3. 用户指出问题 → 回 ④.5，把问题作为新一轮 blocker；用户没问题 → 交付

**步骤⑤ 不再独立做"自审三遍法"**——所有自审已经在 ④.5 对 checklist 全部条目的穷举里做过。把同一组审查做两次只是认知疲劳的来源，不是质量提升。

### ⑥ 迭代到完美（无上限）

**没有轮数表，没有"3 轮够了"**。规则极简：
- **还有 blocker → 继续修**（不管这是第 2 轮还是第 8 轮）
- **同一 blocker 连续 2 轮没修好 → 修复方向错了，换思路**
- **第 3 轮还有 ≥5 blocker → 局部修补救不了，回步骤① 重新设计画图指令**

用户的目标重述："中间迭代多少轮无关紧要，只要图最后是完美的就行"。**绝不允许"凑合交付"**——"改了 3 轮差不多了吧"是认知疲劳的产物，不是质量信号。

### ⑦ 经验沉淀
- 2 次以上才解决的问题 → 追加到 `references/lessons.md` 的 Part 2
- 发现更优参数 → 更新 `lessons.md` 的 Part 1 基线表（**只升不降**）
- 已被全局规则/Python checker 覆盖的内容**不要重复写入**

## Φ 沉淀通道（D 模式 — 用户已有 .tex 入库为新 skeleton）

**触发**：⓪.5 用户选 D 路径。

**前置条件**：
- 用户提供已编译通过的 `.tex` 文件路径
- 文件能 xelatex 编译成功
- 渲染后视觉无明显 bug

**流程**：

```
Φ.1 — 接收 + 编译验证
   - 读取用户提供的 .tex 文件
   - 跑 xelatex -interaction=nonstopmode + pdftoppm -r 150 渲染 PNG
   - 编译失败 → 报告错误，停止入库

Φ.2 — Vision-audit 把关（简化版 ④.5）
   - Read 渲染出的 PNG
   - 走 Step 0（3 大法则）+ checklist 中的关键 6 项（S1 标签不重叠 / S9 元素间距 /
     T1 文字渲染 / M3 信息流方向 / E1 箭头清晰止于框外 / V1 整体审美）
   - 任何 blocker → 报告给用户，要求修复后再入库

Φ.3 — 分析 layout pattern + 决策入库方式（**关键 gate**）
   - 扫描 .tex 提取结构指纹：zone 数量 / zone 坐标范围 / hero 子结构 /
     嵌入 viz 类型 / 配色（line/fill 色对集合）/ 箭头模式
   - **若 .tex 头部注释明示 "Adapted from Skeleton X"** → 直接判定为 X 变体，
     跳过结构相似度计算
   - 否则与现有 6 skeleton 比对相似度，按 zone 数 + 关键结构（hero 位置/
     side panel/底部图表对）匹配，**三档判定**：
     * **>90% 匹配（结构等同，仅内容/主题不同）** → 默认 skip 入库，
       提示用户"这就是 skeleton X 的 <主题> 应用，直接用 X 即可"。
       若用户坚持入库 → Φ.3 verdict = "变体入库"，记录 parent letter
     * **50-90% 匹配（明显借鉴 X 但有结构修改）** → 询问用户
       (a) 合并到 X 作内部变体注释  (b) 作 hybrid 新 skeleton 入库
       后者 → Φ.3 verdict = "结构创新"
     * **<50% 匹配（结构创新）** → Φ.3 verdict = "结构创新"
   - **输出**：verdict + parent letter（若变体）/ 主题 keyword

Φ.4 — 命名 + 字母分配（**按 Φ.3 verdict 分支**）
   - **若 verdict = "变体入库"**：
     - 文件名 = `example-skeleton-{parent}-variant-{domain}.tex`
       例：D 的 MoE 变体 → `example-skeleton-D-variant-moe.tex`
     - **不占用新字母槽**，留给真正的结构创新
   - **若 verdict = "结构创新"**：
     - `ls references/tikz-snippets/example-skeleton-*.tex` 取下一个可用字母
       （当前 B-G 已用，下一个 = H）
     - 询问用户 kebab-case 主题（如 "sankey-flow" / "matrix-grid" / "timeline"）
     - 文件名 = `example-skeleton-{letter}-{topic}.tex`

Φ.5 — 自动生成 USAGE header（**含具体生成算法**）
   - 顶部模板字段及生成方法：
     * **标题行**：
       - 创新："Skeleton {letter} — <layout 一句话描述>"
       - 变体："Skeleton {parent}-variant — {domain} ({parent}-layout domain variant)"
     * **USAGE**：固定模板 "Sub-agent: copy ENTIRE file as figure.tex,
       change ONLY content (text/labels/numbers). DO NOT touch layout."
     * **LAYOUT MODEL** ASCII 生成步骤：
       a) 扫所有 `\fill[...] rectangle (x0,y0) (x1,y1)` 和 `\draw[...] rectangle`
          提 zone bounding box
       b) 按 y 范围归 row（top/mid/bottom），x 范围归 col（left/center/right）
       c) 画 ASCII box：每个 zone 一个 □，按相对位置布局
       d) **若是变体，直接继承 parent 的 LAYOUT MODEL，加注 "(same as Skeleton X)"**
     * **WHEN TO USE**：从用户提供主题 + 域关键词推断
       （如 "MoE" → "Mixture-of-Experts papers, sparse gating/routing"）
       若变体：加一行 "For non-{domain} structurally similar cases, prefer skeleton X directly"
     * **CONTAINS**：自动列清单
       a) 数 `\node[*_node]` count by color (e.g., "4 blue_node + 3 purple_node")
       b) 扫嵌入 viz：heatmap (`\fill` matrix) / bar (`\fill` rect series) /
          curve (`\draw ... smooth`) / radar (`\draw` polar) / formula box (`$...$` in node)
       c) 列 bullet
     * **CONSTRAINTS — DO NOT VIOLATE**：留空 + TODO 注释
       - 若变体：加 "see example-skeleton-{parent}.tex CONSTRAINTS for inherited rules"
       - 加 4-5 个领域专属的 TODO 起跑提示

Φ.6 — 写入库 + 更新索引（**含明确路径与格式**）
   - 写文件：`references/tikz-snippets/example-skeleton-{X}.tex`（X = 完整文件名前缀）
   - 渲染：`xelatex -interaction=nonstopmode` + `pdftoppm -r 100 -png`
     **PNG 输出到 `references/tikz-snippets/previews/example-skeleton-{X}.png`**
     （注意是 `previews/` 子目录，不是 `tikz-snippets/` 根，与现有 example-skeleton 预览放在一起）
   - 更新 `references/tikz-snippets/README.md` inline gallery：
     a) 定位 gallery 表（anchor 行：含 `example-skeleton-B-horizontal.tex` 的 markdown 表格）
     b) 插入位置：
        - 创新：最后一行 example-skeleton-G 之后
        - 变体：parent skeleton 行下面，行最后加 "({parent} 领域变体)" 标注
     c) 行格式：
        ```
        | `example-skeleton-X.tex` | **X: <一句话布局描述>** | <主要应用场景> | ![example-X](previews/example-skeleton-X.png) |
        ```

Φ.7 — 提醒用户后续补 CONSTRAINTS（关键防回归提示）
   - "⚠️ 新 skeleton 已入库，但 CONSTRAINTS 段当前是 TODO 占位。
      如果你在画这张图时踩过坑（标签长度上限 / 锚点选择 / 路径形状 /
      box 宽度依赖等），请手动补充到这一段。
      这是防止未来 sub-agent 复用时重新引入 bug 的关键——参考
      D/E/F/G 的 CONSTRAINTS section 写法。"
```

**Φ 与 ⑦ 经验沉淀 的区别**：
- ⑦ 沉淀**抽象 lessons 与基线参数**（写入 `references/lessons.md`）
- Φ 沉淀**完整可复用的 figure 模板**（写入 `tikz-snippets/example-skeleton-X-*.tex`）
- 两者独立工作，可在同一会话各做各的

**Φ 的杠杆价值**：每入一个 skeleton，未来 N 个 user/session 都能复用。**库是 self-growing 的**——这是 thesis-figure-skill 长期复利的核心机制。

## 设计原则（对抗模型惯性）

容易陷入的刻板印象（必须警惕）：
- "心里有数，直接写代码" → **禁止跳过步骤①**，"想了"≠"想清楚了"
- "我能估比例" → **不行**。复刻必须像素级测量，凭感觉偏差 15-20%
- "框的大小差不多就行" → 不行。参考图通常扁宽 2:1~3:1，**默认不要正方形**
- "改了 3 轮差不多了吧" → 标准不会因为努力降低。还有 blocker 就继续修
- "这个小重叠用户看不出来" → 看得出来。300dpi 下清清楚楚
- "坐标差 0.2cm 没关系" → 0.2cm 在渲染图上是 24 像素
- "信息密度不够就硬塞东西" → **反例**。简单论文图就该简单——贝叶斯网络/几何/对比图天然元素少，强加 hero 和嵌入可视化是污染。`tikz-design-linter` 现在是 advisory，按论文实际复杂度决定密度

**信息密度匹配论文复杂度**：复杂模型架构图允许 30+ 元素 + hero 子结构 + 嵌入可视化；简单流程图 5-10 元素 + 清晰布局就够了。**不要把所有图都画到最大复杂度**。详见 `step1-instructions.md` 的"信息密度判断"。

## 常见图表类型

| 类型 | 布局 | 场景 |
|------|------|------|
| 系统架构图 | 自下而上分层 | 端→云→链、硬件→中间件→应用 |
| 协议/流程图 | 左→右或上→下 | 时序步骤、信号处理 |
| 数据流水线 | 左→右水平串联 | 输入→处理→输出，每步不同形状 |
| 电路/约束原理 | 左→右 | ZK 电路、信号管线、编译器 |
| 数据映射/转换 | 左-中-右三栏 | 格式转换、API 适配 |
| 时序交互 | 多列生命线+水平消息 | 多方协议 |
| 对比方案 | 左右并列 | 方案 A vs B，中间 ≥3cm |
| 几何/数学 | 坐标系+几何元素 | 算法原理、向量关系 |
| 技术路线图 | 三层分区（draw.io 模式 A） | 科研展示 |
| 同心嵌套 | 多层嵌套椭圆（draw.io 模式 B） | 宏观→微观 |
| 流水线链条 | 圆形节点+加号（draw.io 模式 C） | 技术叠加 |
| 侧栏+中心 | 左右侧栏+中心嵌套（draw.io 模式 D） | 技术突破+路径 |
| 总论-展开-归纳 | 顶部→三栏→底部（draw.io 模式 E） | 创新+应用+方案 |
| 分层技术路线图 | 背景→问题→框架→路线→结论（draw.io 模式 F） | 毕业论文路线图 |
| 多实例汇聚 | 横排三列→汇聚 | 联邦学习、分布式 |
| 数据可视化混合 | 框图内嵌波形/柱状/热力图 | 信号处理、深度学习注意力 |

## 按需加载索引

确定图表类型/工作流阶段后**才**加载对应文件：

| 触发条件 | 文件 |
|---------|------|
| 进入步骤① | `references/step1-instructions.md` |
| 步骤②（任何 TikZ 图，**必加载**） | `references/lessons.md` + `references/visual-patterns.md` |
| 步骤③ 决策门 | `references/figure-spec.schema.md`（B 路 spec） |
| 步骤③ 走 B 路 → 跑 `dot-to-tikz.py` | （脚本，不需 Read） |
| 步骤③ 走模板/从零 → 用 TikZ | `references/tikz-global-rules.md` + `references/tikz-template.tex` |
| **步骤③ 复杂档需嵌入 viz / panel / 公式** | **`references/tikz-snippets/` ⭐ 优先用 snippet 拼装而不是从零写**（含 21 个手工精雕片段 + 6 个 example-skeleton，**完整清单见 `references/tikz-snippets/README.md`**；下列只是常用几个，勿局限：attention-heatmap / bar-chart / hyperparams-table / multi-zone-palette / pipeline-stages / formula-box …） |
| 步骤④.5 视觉反馈每一轮 | `references/visual-review-checklist.md`（18 项强制清单） |
| 配色需求 | `references/tikz-colors.md` |
| 分层架构图 | `references/layered-architecture.md` |
| 时序交互图 | `references/sequence-diagram.md` |
| 数据流水线图 | `references/data-pipeline.md` |
| 三栏映射图 | `references/three-column-mapping.md` |
| 几何/数学示意图 | `references/geometry-math.md` |
| 含数据可视化的图 | `references/data-visualization.md` |
| draw.io 科研展示图 | `references/drawio-modes.md` |
| 步骤⑤ 有参考图 | `references/figure-diff.py`（脚本） |

**未列出的文件不要加载**——节省 token。

## Python 助手脚本（执行即可，不要 Read）

| 脚本 | 用途 | 何时跑 |
|------|------|--------|
| `dot-to-tikz.py <spec.json>` | B 路：spec → graphviz 自动布局 → TikZ | 结构化图 step ③ |
| `tikz-validator.py <file.tex>` | 微斜线/溢出/碰撞/方向反转（几何/语法 gate） | 编译前必跑 |
| `tikz-design-linter.py <file.tex> [--type ...]` | 元素数/尺寸比/线型/hero/嵌入viz（设计野心 gate） | 编译前必跑 |
| `pdf-overlap-checker.py <file.pdf> [--json]` | PDF 坐标级重叠 + 线穿节点 + 节点重叠几何检测（**7 类**：text-overlap / text-overflow / off-center / text-line / line-crossing / line-through-node / node-overlap） | 编译后必跑 |
| `figure-diff.py <ref.png> <out.png>` | SSIM + 3×3 区域差异 | 复刻任务必跑 |
| `tikz-path-router.py <spec.json>` | A* 自动避障路径 | 连线 ≥8 条可选 |

这些脚本**作为黑盒调用**——不要把源码读进上下文，跑 `--help` 看参数即可。

## 领域自适应

收到输入后**先识别论文领域**（计算机/密码学/生物/物理/化学/AI/网络/系统/区块链等），以该领域专家身份选术语和布局风格。

---

## 维护者回归自检（⚠️ 不在画图流程内 —— 生成图时不要跑）

**仅当你在修改本 skill（SKILL.md / references / 脚本）时使用。** 改动前后各跑一次，确认这次编辑没有
引入"几何/编译可检测"的回归：

```bash
cd references/eval && python3 runner.py      # 改前确认全绿；改后若有 FAIL 即本次回归
```

它对一组冻结 fixture 跑 `dot-to-tikz → xelatex → tikz-validator → pdf-overlap-checker`，与 baseline 比对，
退出码 1 = 有回归。**只是回归地板**：抓编译/缺字/微斜线/重叠等几何问题，**抓不到**语义/审美 slop（那些靠 ④.5）。
详见 `references/eval/README.md`。新增检查项或确认新基准后再 `python3 runner.py --update-baselines`。
