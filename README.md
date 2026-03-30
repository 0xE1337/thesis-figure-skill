# thesis-figure-skill

**[中文](#中文) | [English](#english)**

---

<a id="中文"></a>

## 中文

> Claude Skill：粘贴论文文案或上传图片，自动生成学术级配图（LaTeX/TikZ + draw.io）

一个用于 [Claude](https://claude.ai) 的 Skill，让 AI 自动将学术论文文案转化为高质量配图。支持两种输出格式：

- **LaTeX/TikZ**：适合系统架构图、数据流图、几何示意图等结构化图表，可直接嵌入论文
- **draw.io XML**：适合技术路线图、科研展示图、学术汇报配图等装饰性强的图表，支持渐变色、阴影、自由布局

> 输入论文文字/图片 → 自动生成代码 → 编译验证 → 高质量交付

### 效果展示

| 系统架构图 | 时序交互图 | 对比方案图 |
|:---:|:---:|:---:|
| ![system_architecture](examples/01_system_architecture.png) | ![sequence_interaction](examples/02_sequence_interaction.png) | ![comparison](examples/03_comparison.png) |

| 数据流水线图 | 技术路线图 | 几何/数学示意图 |
|:---:|:---:|:---:|
| ![data_pipeline](examples/04_data_pipeline.png) | ![research_roadmap](examples/05_research_roadmap.png) | ![math_diagram](examples/06_math_diagram.png) |

| 计算流水线图 | 分层架构图 | 研究框架图 |
|:---:|:---:|:---:|
| ![computation_pipeline](examples/07_computation_pipeline.png) | ![layered_architecture](examples/08_layered_architecture.png) | ![research_framework](examples/09_research_framework.png) |

| 分层技术路线图（draw.io） | 编译器优化流程图 | 侧栏+中心嵌套图（draw.io） |
|:---:|:---:|:---:|
| ![layered_roadmap](examples/10_layered_roadmap.png) | ![compiler_pipeline](examples/11_compiler_pipeline.png) | ![sidebar_center](examples/12_sidebar_center.png) |

> 以上示例均由本 Skill 自动生成，包含编译验证、渲染审查、自动评分全流程。

### 特性

- **双格式输出**：TikZ 嵌入论文 + draw.io 自由编辑，按需选择
- **文案驱动**：粘贴论文段落，自动分析内容生成画图指令，再转化为代码
- **图片驱动**：上传已有截图，自动复刻为可编辑代码
- **领域自适应**：自动识别论文所属学科，以该领域专家视角设计配图
- **统一配色**：TikZ 内置 6 色学术配色方案；draw.io 提供 4 套领域主题配色（学术蓝灰/粉紫渐变/翠绿自然/科技深色），根据论文领域自动选择
- **12+ 种图表类型**：分层架构图、时序图、对比图、流水线图、三栏映射图、几何数学图、多实例汇聚图、电路原理图、混合图、draw.io 路线图等
- **编译验证 + 渲染审查 + 自动评分**：生成后自动编译、转 PNG、基于渲染图视觉审查（非代码审查）、六维度评分，不满分自动迭代修改
- **设计师级审查**：三遍法审查（整体感觉→逐元素→连线路径），像人一样空间推理，发现重叠/碰撞/不自然的布局
- **中文优先**：原生支持中文标签，多平台 CJK 字体自动检测（macOS PingFang SC / Linux Noto Sans CJK SC / Windows SimHei）
- **画图哲学驱动**：四步思考循环（定义成功标准→选起点→过程校验→完成判断），对抗模型惯性
- **渐进式规则加载**：核心规则常驻，专项规则按图表类型按需加载，节省上下文 token
- **经验自动沉淀**：画图过程中的踩坑经验自动记录，后续复用越画越顺

### 安装

#### 方法一：命令行安装（推荐）

```bash
npx skills add 0xE1337/thesis-figure-skill
```

#### 方法二：上传安装

下载 [`thesis-figure-skill.skill`](thesis-figure-skill.skill) 文件，在 Claude 对话中上传，点击 **"Copy to your skills"** 即可。

#### 方法三：手动安装

将 `skills/thesis-figure-skill/SKILL.md` 文件放入 Claude 的 skills 目录。

### 使用方式

安装后，在 Claude 对话中直接说：

```
帮我根据以下论文内容画一张架构图：

本文提出一种基于联邦学习的隐私保护框架，包含三层结构：
底层为分布在各医院的本地训练节点...（粘贴论文段落）
```

或者上传一张已有的图片：

```
帮我用 TikZ 复刻这张图
（附上截图）
```

或者指定使用 draw.io 格式：

```
帮我画一张技术路线图，用 draw.io 格式
（粘贴论文内容）
```

> **提示**：首次运行时需要安装字体和 TeX 编译环境，耗时较长，请耐心等待。后续使用会直接复用已创建的环境。

Claude 会自动：
1. 识别论文领域
2. 选择合适的输出格式（TikZ / draw.io）
3. 生成详细画图指令
4. 输出完整代码
5. 编译验证（TikZ）或生成可编辑文件（draw.io）
6. 自动评分，不达标则迭代修改
7. 交付最终文件

### 输出格式对比

| 场景 | 推荐格式 | 理由 |
|------|---------|------|
| 嵌入 LaTeX 论文、含数学公式、结构化图表 | **TikZ** | 编译可控，公式精确 |
| 技术路线图、科研展示图、装饰性强（渐变/阴影） | **draw.io** | 视觉效果好，可拖拽编辑 |
| 用户明确指定 | 遵循用户要求 | — |

### 支持的图表类型

| 类型 | 布局 | 适用场景 |
|------|------|---------|
| 系统架构图 | 垂直分层 | 端→云→链、硬件→中间件→应用 |
| 时序交互图 | 多列生命线 | 多方协议交互、握手流程 |
| 对比方案图 | 左右并列 | 原有 vs 改进方案 |
| 数据流水线图 | 水平多阶段 | 数据处理流水线 |
| 中心辐射图 | 环形布局 | 微服务架构、核心模块交互 |
| 数据流转图 | 自上而下 | 输入→处理→输出 |
| 技术路线图 | 多层板块 | 研究框架、技术方案总览 |
| 分层技术路线图 | 多层板块 | 毕业论文路线图、开题报告（draw.io 模式F） |

### 配色方案

内置 draw.io 风格配色，适合学术论文：

| 颜色 | 填充色 | 边框色 | 典型用途 |
|------|--------|--------|---------|
| 蓝色 | `#DAE8FC` | `#6C8EBF` | 通用模块、基础层 |
| 绿色 | `#D5E8D4` | `#82B366` | 核心模块、安全组件 |
| 橙色 | `#FFE6CC` | `#D79B00` | 数据流、强调元素 |
| 紫色 | `#E1D5E7` | `#9673A6` | 高层抽象、决策层 |
| 红色 | `#F8CECC` | `#B85450` | 关键操作、警告 |
| 灰色 | `#F5F5F5` | `#666666` | 辅助服务、存储 |

#### draw.io 领域配色方案

根据论文所属领域自动选择：

| 方案 | 名称 | 适用领域 |
|------|------|---------|
| A | 学术蓝灰 | 计算机、工程、通用学术 |
| B | 粉紫渐变 | 生物医学、心理学 |
| C | 翠绿自然 | 环境科学、农业、生态 |
| D | 科技深色 | 网络安全、区块链、硬件 |

### 环境要求

本 Skill 在 Claude Code 中运行，自动处理编译环境。如需本地编译 TikZ 示例：

- TeX Live（含 `xelatex`）
- CJK 中文字体（macOS 自带 PingFang SC，Linux 需安装 Noto Sans CJK SC，Windows 使用 SimHei）
- ctex 宏包
- poppler-utils（用于 PDF 转 PNG）
- draw.io Desktop（可选，用于 draw.io 格式导出）

#### macOS（推荐）

```bash
# 安装 TeX Live
brew install --cask mactex-no-gui
# 安装 poppler（提供 pdftoppm）
brew install poppler
# 安装 draw.io Desktop（可选，用于 draw.io 格式导出）
brew install --cask drawio

# 编译 TikZ
xelatex -interaction=nonstopmode example.tex
# 转 PNG（300dpi）
pdftoppm -png -r 300 example.pdf preview
```

> macOS 自带 PingFang SC 字体，无需额外安装中文字体。

#### Ubuntu/Debian

```bash
sudo apt-get install texlive-xetex texlive-lang-chinese fonts-noto-cjk poppler-utils
# 编译
xelatex -interaction=nonstopmode example.tex
# 转 PNG
pdftoppm -png -r 300 example.pdf preview
```

draw.io 格式的文件可直接在 [app.diagrams.net](https://app.diagrams.net) 打开编辑，也可用 draw.io Desktop 导出 PDF/PNG。

---

<a id="english"></a>

## English

> Claude Skill: Paste thesis text or upload images, automatically generate publication-quality figures (LaTeX/TikZ + draw.io)

A Skill for [Claude](https://claude.ai) that lets AI automatically transform academic paper text into high-quality figures. Supports two output formats:

- **LaTeX/TikZ**: Ideal for system architecture diagrams, data flow diagrams, geometric illustrations, and other structured charts that can be directly embedded in papers
- **draw.io XML**: Ideal for research roadmaps, academic presentations, and decorative-rich diagrams with gradient colors, shadows, and free-form layouts

> Input thesis text/image -> Automatically generate code -> Compile and verify -> High-quality delivery

### Gallery

| System Architecture | Sequence Interaction | Comparison Diagram |
|:---:|:---:|:---:|
| ![system_architecture](examples/01_system_architecture.png) | ![sequence_interaction](examples/02_sequence_interaction.png) | ![comparison](examples/03_comparison.png) |

| Data Pipeline | Research Roadmap | Geometry/Math Diagram |
|:---:|:---:|:---:|
| ![data_pipeline](examples/04_data_pipeline.png) | ![research_roadmap](examples/05_research_roadmap.png) | ![math_diagram](examples/06_math_diagram.png) |

| Computation Pipeline | Layered Architecture | Research Framework |
|:---:|:---:|:---:|
| ![computation_pipeline](examples/07_computation_pipeline.png) | ![layered_architecture](examples/08_layered_architecture.png) | ![research_framework](examples/09_research_framework.png) |

| Layered Roadmap (draw.io) | Compiler Optimization Pipeline | Sidebar + Center Nested (draw.io) |
|:---:|:---:|:---:|
| ![layered_roadmap](examples/10_layered_roadmap.png) | ![compiler_pipeline](examples/11_compiler_pipeline.png) | ![sidebar_center](examples/12_sidebar_center.png) |

> All examples above were automatically generated by this Skill, including the full pipeline of compilation verification, rendering review, and automatic scoring.

### Features

- **Dual-Format Output**: TikZ for paper embedding + draw.io for free editing, choose as needed
- **Text-Driven**: Paste a thesis paragraph, automatically analyze the content to generate drawing instructions, then convert to code
- **Image-Driven**: Upload an existing screenshot, automatically recreate it as editable code
- **Domain-Adaptive**: Automatically identifies the paper's field and designs figures from a domain expert's perspective
- **Unified Color Schemes**: TikZ includes a built-in 6-color academic palette; draw.io provides 4 domain-themed palettes (Academic Blue-Gray / Pink-Purple Gradient / Green Nature / Tech Dark), automatically selected based on the paper's field
- **12+ Diagram Types**: Layered architecture, sequence, comparison, pipeline, three-column mapping, geometry/math, multi-instance convergence, circuit schematic, hybrid, draw.io roadmap, and more
- **Compile + Render Review + Auto-Scoring**: After generation, automatically compiles, converts to PNG, performs visual review based on rendered images (not code review), scores across six dimensions, and iterates if not perfect
- **Designer-Level Review**: Three-pass review method (overall impression -> element-by-element -> connection paths), spatial reasoning like a human, detecting overlap/collision/unnatural layouts
- **CJK Support**: Native support for Chinese labels, with automatic CJK font detection across platforms (macOS PingFang SC / Linux Noto Sans CJK SC / Windows SimHei)
- **Drawing Philosophy-Driven**: Four-step thinking cycle (define success criteria -> choose starting point -> in-process validation -> completion judgment), countering model inertia
- **Progressive Rule Loading**: Core rules stay loaded, specialized rules load on demand by diagram type, saving context tokens
- **Automatic Experience Logging**: Lessons learned during drawing are automatically recorded and reused, making each subsequent session smoother

### Installation

#### Method 1: Command Line (Recommended)

```bash
npx skills add 0xE1337/thesis-figure-skill
```

#### Method 2: Upload

Download the [`thesis-figure-skill.skill`](thesis-figure-skill.skill) file, upload it in a Claude conversation, and click **"Copy to your skills"**.

#### Method 3: Manual

Place the `skills/thesis-figure-skill/SKILL.md` file into Claude's skills directory.

### Usage

After installation, simply say in a Claude conversation:

```
Draw an architecture diagram based on the following thesis content:

This paper proposes a privacy-preserving framework based on federated learning
with a three-layer structure: the bottom layer consists of local training nodes
distributed across hospitals... (paste thesis paragraph)
```

Or upload an existing image:

```
Recreate this diagram using TikZ
(attach screenshot)
```

Or specify the draw.io format:

```
Draw a research roadmap in draw.io format
(paste thesis content)
```

> **Note**: The first run requires installing fonts and the TeX compilation environment, which takes longer. Subsequent runs will reuse the previously created environment.

Claude will automatically:
1. Identify the paper's field
2. Select the appropriate output format (TikZ / draw.io)
3. Generate detailed drawing instructions
4. Output complete code
5. Compile and verify (TikZ) or generate editable files (draw.io)
6. Auto-score, iterating if below standard
7. Deliver the final files

### Output Format Comparison

| Scenario | Recommended Format | Reason |
|----------|-------------------|--------|
| Embedding in LaTeX papers, with math formulas, structured charts | **TikZ** | Controllable compilation, precise formulas |
| Research roadmaps, academic presentations, decoration-rich (gradients/shadows) | **draw.io** | Better visual effects, drag-and-drop editing |
| User explicitly specifies | Follow user's request | -- |

### Supported Diagram Types

| Type | Layout | Use Cases |
|------|--------|-----------|
| System Architecture | Vertical layering | Device -> Cloud -> Chain, Hardware -> Middleware -> Application |
| Sequence Interaction | Multi-column lifelines | Multi-party protocol interaction, handshake flows |
| Comparison Diagram | Side-by-side | Original vs. improved approach |
| Data Pipeline | Horizontal multi-stage | Data processing pipelines |
| Hub-Spoke Diagram | Radial layout | Microservice architecture, core module interactions |
| Data Flow Diagram | Top-down | Input -> Processing -> Output |
| Research Roadmap | Multi-layer blocks | Research frameworks, technical solution overviews |
| Layered Research Roadmap | Multi-layer blocks | Thesis roadmaps, proposal reports (draw.io Mode F) |

### Color Schemes

Built-in draw.io style color scheme, suitable for academic papers:

| Color | Fill | Border | Typical Usage |
|-------|------|--------|---------------|
| Blue | `#DAE8FC` | `#6C8EBF` | General modules, base layer |
| Green | `#D5E8D4` | `#82B366` | Core modules, security components |
| Orange | `#FFE6CC` | `#D79B00` | Data flow, emphasis elements |
| Purple | `#E1D5E7` | `#9673A6` | High-level abstractions, decision layer |
| Red | `#F8CECC` | `#B85450` | Critical operations, warnings |
| Gray | `#F5F5F5` | `#666666` | Auxiliary services, storage |

#### draw.io Domain Color Schemes

Automatically selected based on the paper's field:

| Scheme | Name | Applicable Fields |
|--------|------|-------------------|
| A | Academic Blue-Gray | Computer science, engineering, general academic |
| B | Pink-Purple Gradient | Biomedical, psychology |
| C | Green Nature | Environmental science, agriculture, ecology |
| D | Tech Dark | Cybersecurity, blockchain, hardware |

### Requirements

This Skill runs within Claude Code and automatically handles the compilation environment. For local compilation of TikZ examples:

- TeX Live (with `xelatex`)
- CJK Chinese fonts (macOS includes PingFang SC, Linux requires Noto Sans CJK SC, Windows uses SimHei)
- ctex package
- poppler-utils (for PDF to PNG conversion)
- draw.io Desktop (optional, for draw.io format export)

#### macOS (Recommended)

```bash
# Install TeX Live
brew install --cask mactex-no-gui
# Install poppler (provides pdftoppm)
brew install poppler
# Install draw.io Desktop (optional, for draw.io format export)
brew install --cask drawio

# Compile TikZ
xelatex -interaction=nonstopmode example.tex
# Convert to PNG (300dpi)
pdftoppm -png -r 300 example.pdf preview
```

> macOS includes PingFang SC font by default; no additional Chinese font installation is needed.

#### Ubuntu/Debian

```bash
sudo apt-get install texlive-xetex texlive-lang-chinese fonts-noto-cjk poppler-utils
# Compile
xelatex -interaction=nonstopmode example.tex
# Convert to PNG
pdftoppm -png -r 300 example.pdf preview
```

draw.io format files can be opened and edited directly at [app.diagrams.net](https://app.diagrams.net), or exported to PDF/PNG using draw.io Desktop.

---

## License

MIT License
