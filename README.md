# thesis-figure-skill

> Claude Skill：粘贴论文文案或上传图片，自动生成学术级配图（LaTeX/TikZ + draw.io）

一个用于 [Claude](https://claude.ai) 的 Skill，让 AI 自动将学术论文文案转化为高质量配图。支持两种输出格式：

- **LaTeX/TikZ**：适合系统架构图、数据流图、几何示意图等结构化图表，可直接嵌入论文
- **draw.io XML**：适合技术路线图、科研展示图、学术汇报配图等装饰性强的图表，支持渐变色、阴影、自由布局

> 输入论文文字/图片 → 自动生成代码 → 编译验证 → 高质量交付

## 效果展示

| 系统架构图 | 时序交互图 | 对比方案图 |
|:---:|:---:|:---:|
| ![system_architecture](examples/01_system_architecture.png) | ![sequence_interaction](examples/02_sequence_interaction.png) | ![comparison](examples/03_comparison.png) |

| 数据流水线图 | 技术路线图 | 几何/数学示意图 |
|:---:|:---:|:---:|
| ![data_pipeline](examples/04_data_pipeline.png) | ![research_roadmap](examples/05_research_roadmap.png) | ![math_diagram](examples/06_math_diagram.png) |

| 计算流水线图 | 分层架构图 | 分层技术路线图（draw.io） |
|:---:|:---:|:---:|
| ![computation_pipeline](examples/07_computation_pipeline.png) | ![layered_architecture](examples/08_layered_architecture.png) | ![layered_roadmap](examples/10_layered_roadmap.png) |

## 特性

- **双格式输出**：TikZ 嵌入论文 + draw.io 自由编辑，按需选择
- **文案驱动**：粘贴论文段落，自动分析内容生成画图指令，再转化为代码
- **图片驱动**：上传已有截图，自动复刻为可编辑代码
- **领域自适应**：自动识别论文所属学科，以该领域专家视角设计配图
- **统一配色**：内置 6 色学术配色方案（蓝/绿/橙/紫/红/灰），全篇视觉一致
- **多种图表类型**：支持分层架构图、时序图、对比图、流水线图、中心辐射图、数据流转图、技术路线图等
- **编译验证 + 自动评分**：生成后自动编译验证、缺陷扫描、多维度评分，不满分自动迭代修改
- **中文优先**：原生支持中文标签，自动处理字体配置

## 安装

### 方法一：命令行安装（推荐）

```bash
npx skills add yijingguo/thesis-figure-skill
```

### 方法二：上传安装

下载 [`thesis-figure-skill.skill`](thesis-figure-skill.skill) 文件，在 Claude 对话中上传，点击 **"Copy to your skills"** 即可。

### 方法三：手动安装

将 `skills/thesis-figure-skill/SKILL.md` 文件放入 Claude 的 skills 目录。

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
| 中心辐射图 | 环形布局 | 微服务架构、核心模块交互 |
| 数据流转图 | 自上而下 | 输入→处理→输出 |
| 技术路线图 | 多层板块 | 研究框架、技术方案总览 |
| 分层技术路线图 | CSS+SVG 混合分层 | 毕业论文路线图、开题报告（draw.io 模式F） |

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

## 示例文件

`examples/` 目录包含 10 个示例，覆盖多种学术图表类型：

1. **系统架构图** — 区块链/云端/边缘/感知四层架构，联邦学习 + 微服务网关
2. **时序交互图** — 多方 ZKP 协议交互，感知用户→边缘节点→区块链→任务发布方
3. **对比方案图** — 传统群智感知 vs 基于 ZKP 的隐私保护方案，左右并列 + 评估指标
4. **数据流水线图** — 多模态免疫原性预测，序列/结构/生化三通道→融合→预测
5. **技术路线图** — 超大规模 MIMO 信道建模技术路线图，多层板块布局
6. **几何/数学示意图** — 椭圆曲线、Merkle 树、Groth16 验证方程
7. **计算流水线图** — 源代码→算术电路→R1CS→QAP 多项式，算术化流程
8. **分层架构图** — IoT 联邦学习系统，感知终端→边缘计算→云端服务→区块链可信层
9. **研究框架图** — 源-网-荷-储多层协同优化，漏斗形四层研究架构
10. **分层技术路线图（draw.io 模式F）** — 研究背景→问题提出→研究框架→研究内容→结论展望，含 3D 圆柱体网络节点与树状连线，CSS+SVG 混合布局

## 环境要求

本 Skill 在 Claude.ai 中运行，自动处理编译环境。如需本地编译 TikZ 示例：

- TeX Live（含 `xelatex`）
- Noto Sans CJK SC 字体
- ctex 宏包（`texlive-lang-chinese`）

```bash
# Ubuntu/Debian
sudo apt-get install texlive-xetex texlive-lang-chinese fonts-noto-cjk poppler-utils
# 编译
xelatex -interaction=nonstopmode example.tex
# 转 PNG
pdftoppm -png -r 300 example.pdf preview
```

draw.io 格式的文件可直接在 [app.diagrams.net](https://app.diagrams.net) 打开编辑。

## 许可证

MIT License
