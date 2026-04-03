# thesis-figure-skill

**中文 | [English](README.en.md)**

> Claude Skill：粘贴论文文案或上传图片，自动生成学术级配图（LaTeX/TikZ + draw.io）

一个用于 [Claude](https://claude.ai) 的 Skill，让 AI 自动将学术论文文案转化为高质量配图。支持两种输出格式：

- **LaTeX/TikZ**：适合系统架构图、数据流图、几何示意图等结构化图表，可直接嵌入论文
- **draw.io XML**：适合技术路线图、科研展示图、学术汇报配图等装饰性强的图表，支持渐变色、阴影、自由布局

> 输入论文文字/图片 → 自动生成代码 → 编译验证 → 高质量交付

## 效果展示

### 数据可视化混合图（NEW）

| Transformer 架构 + 注意力热力图 | zkSNARK 密码学流水线 + 椭圆曲线 | 扩散模型 U-Net + 损失曲线 |
|:---:|:---:|:---:|
| ![transformer](examples/06_transformer.png) | ![zksnark](examples/07_zksnark.png) | ![diffusion](examples/08_diffusion.png) |

| 联邦学习 + 雷达图 + 收敛曲线 | 图注意力网络 GAT + 散点图 |
|:---:|:---:|
| ![fl_crypto](examples/09_fl_crypto.png) | ![gat](examples/10_gat.png) |

### 经典图表类型

| 编译器优化流程图 | 时序交互图 | 对比方案图 |
|:---:|:---:|:---:|
| ![compiler_pipeline](examples/05_compiler_pipeline.png) | ![sequence_interaction](examples/01_sequence_interaction.png) | ![comparison](examples/02_comparison.png) |

| 分层路线图（draw.io） | 侧栏+中心嵌套图（draw.io） |
|:---:|:---:|
| ![layered_roadmap](examples/03_layered_roadmap.png) | ![sidebar_center](examples/04_sidebar_center.png) |

> 以上示例均由本 Skill 自动生成，包含编译验证、44 项视觉审查、六维度评分全流程。

> 完整版本更新历史见 [Releases](https://github.com/0xE1337/thesis-figure-skill/releases)

## 特性

- **双格式输出**：TikZ 嵌入论文 + draw.io 自由编辑，按需选择
- **数据可视化嵌入**：在框图内嵌入热力图、柱状图、波形、雷达图、散点图——架构流程 + 数据展示一张图搞定
- **文案驱动**：粘贴论文段落，自动分析内容生成画图指令，再转化为代码
- **图片驱动**：上传已有截图，自动复刻为可编辑代码
- **领域自适应**：自动识别论文所属学科，以该领域专家视角设计配图
- **统一配色**：TikZ 内置 6 色暖色架构配色 + 蓝紫冷色数据可视化配色；draw.io 提供 4 套领域主题配色
- **14 种图表类型**：分层架构图、时序图、对比图、流水线图、三栏映射图、几何数学图、多实例汇聚图、电路原理图、数据可视化混合图、draw.io 路线图等
- **44 项审查规则 + 六维度评分**：生成后自动编译、转 PNG、基于渲染图视觉审查，不满分自动迭代修改
- **三阶段自动化质检**：编译前坐标验证 → 编译后 PDF 重叠检测（pdfplumber, 0.1pt 精度）→ 可选 A* 路径规划
- **设计野心体系**：最低设计门槛 + ASCII 布局草图 + 三轮自审（找 bug→找平庸→找排版问题）
- **防御性 TikZ 模板**：箭头防刺入（shorten）、连线防贴框（-|/|-）、分叉防断连（coordinate）、装饰防遮挡（background 层）
- **A* 路径规划器**：密集连线场景自动计算避障正交路径，告别手动路由
- **中文优先**：原生支持中文标签，多平台 CJK 字体自动检测
- **渐进式规则加载**：核心规则常驻，审查清单和专项规则按需加载，节省上下文 token
- **进化基线**：已验证最佳参数自动复用，标准只升不降
- **经验自动沉淀**：55+ 条踩坑经验自动记录，后续复用越画越顺

## 安装

### 方法一：命令行安装（推荐）

```bash
npx skills add 0xE1337/thesis-figure-skill
```

### 方法二：上传安装

下载 [`thesis-figure-skill.skill`](thesis-figure-skill.skill) 文件，在 Claude 对话中上传，点击 **"Copy to your skills"** 即可。

### 方法三：手动安装

将 `skills/thesis-figure-skill/` 整个目录（包含 `SKILL.md` 和 `references/` 子目录）复制到 Claude 的 skills 目录下。

## 使用方式

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

## 输出格式对比

| 场景 | 推荐格式 | 理由 |
|------|---------|------|
| 嵌入 LaTeX 论文、含数学公式、结构化图表 | **TikZ** | 编译可控，公式精确 |
| 技术路线图、科研展示图、装饰性强（渐变/阴影） | **draw.io** | 视觉效果好，可拖拽编辑 |
| 用户明确指定 | 遵循用户要求 | — |

## 支持的图表类型

| 类型 | 布局 | 适用场景 |
|------|------|---------|
| 系统架构图 | 垂直分层 | 端→云→链、硬件→中间件→应用 |
| 时序交互图 | 多列生命线 | 多方协议交互、握手流程 |
| 对比方案图 | 左右并列 | 原有 vs 改进方案 |
| 数据流水线图 | 水平多阶段 | 数据处理流水线 |
| 电路/约束原理图 | 左→右 | ZK 电路、信号处理、编译器 pipeline |
| 三栏映射图 | 左-中-右 | 格式转换、API 适配、编码映射 |
| 几何/数学示意图 | 坐标系 | 算法原理、向量关系、椭圆曲线 |
| 多实例汇聚图 | 横排→汇聚 | 联邦学习、分布式系统 |
| **数据可视化混合图** | **框图+嵌入图表** | **深度学习架构+热力图/柱状图/曲线** |
| 技术路线图 | 多层板块 | 研究框架、技术方案总览（draw.io） |
| 同心嵌套图 | 多层嵌套 | 从宏观到微观（draw.io） |
| 侧栏+中心图 | 左右侧栏 | 技术突破+路径+核心（draw.io） |
| 总论-展开-归纳图 | 顶→三栏→底 | 核心创新+应用场景（draw.io） |
| 分层技术路线图 | 多层板块 | 毕业论文路线图、开题报告（draw.io） |

## 配色方案

内置 draw.io 风格配色，适合学术论文：

| 颜色 | 填充色 | 边框色 | 典型用途 |
|------|--------|--------|---------|
| 蓝色 | `#DAE8FC` | `#6C8EBF` | 通用模块、基础层 |
| 绿色 | `#D5E8D4` | `#82B366` | 核心模块、安全组件 |
| 橙色 | `#FFE6CC` | `#D79B00` | 数据流、强调元素 |
| 紫色 | `#E1D5E7` | `#9673A6` | 高层抽象、决策层 |
| 红色 | `#F8CECC` | `#B85450` | 关键操作、警告 |
| 灰色 | `#F5F5F5` | `#666666` | 辅助服务、存储 |

### 数据可视化配色（嵌入图表专用）

| 颜色 | 色值 | 用途 |
|------|------|------|
| waveBlue | `#3B82F6` | 主波形线、柱状图 |
| wavePurple | `#8B5CF6` | 副波形线 |
| heatDeep | `#6D28D9` | 热力图最深 |
| heatMid | `#93C5FD` | 热力图中 |
| heatLight | `#DBEAFE` | 热力图浅 |

> 架构框图用暖色（蓝绿橙紫红灰），嵌入可视化用冷色（蓝紫），两套配色自然区分"结构"和"数据"。

### draw.io 领域配色方案

根据论文所属领域自动选择：

| 方案 | 名称 | 适用领域 |
|------|------|---------|
| A | 学术蓝灰 | 计算机、工程、通用学术 |
| B | 粉紫渐变 | 生物医学、心理学 |
| C | 翠绿自然 | 环境科学、农业、生态 |
| D | 科技深色 | 网络安全、区块链、硬件 |

## 环境要求

本 Skill 在 Claude Code 中运行，自动处理编译环境。如需本地编译 TikZ 示例：

- TeX Live（含 `xelatex`）
- CJK 中文字体（macOS 自带 PingFang SC，Linux 需安装 Noto Sans CJK SC，Windows 使用 SimHei）
- ctex 宏包
- poppler-utils（用于 PDF 转 PNG）
- draw.io Desktop（可选，用于 draw.io 格式导出）

### macOS（推荐）

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

### Ubuntu/Debian

```bash
sudo apt-get install texlive-xetex texlive-lang-chinese fonts-noto-cjk poppler-utils
# 编译
xelatex -interaction=nonstopmode example.tex
# 转 PNG
pdftoppm -png -r 300 example.pdf preview
```

draw.io 格式的文件可直接在 [app.diagrams.net](https://app.diagrams.net) 打开编辑，也可用 draw.io Desktop 导出 PDF/PNG。

## 许可证

MIT License
