# 画图经验沉淀

> 本文件由 Agent 在画图过程中自动维护。每次遇到编译错误、布局缺陷、或发现有效技巧时，按格式追加记录。
> 下次画同类型图时，先读取本文件获取先验知识。

## 使用规则

### 何时读取
确定图表类型后，先读取本文件中该类型的已有经验。经验标注了发现日期，当作「可能有效的提示」而非「保证正确的事实」——工具版本会更新，之前的 workaround 可能已不需要。

### 何时写入
以下情况自动追加经验记录：
- 编译错误经过 2 次以上尝试才解决
- 发现了某种图表类型的有效布局技巧
- 渲染结果与预期差异大，需要调整方案
- 用户反馈指出了某个反复出现的问题

### 记录格式

每条经验包含：

    ### [图表类型] - [简述]
    - **问题/发现**：具体描述
    - **解决方案**：怎么做的
    - **发现日期**：YYYY-MM-DD

只写经过验证的事实，不写未确认的猜测。如果按经验操作失败，更新或删除该条经验。

---

## 经验记录

### [通用] - pgfonlayer 环境名
- **问题/发现**：背景层环境名是 `\begin{pgfonlayer}{background}`，不是 `\begin{pgfonbackgroundlayer}`。后者会导致编译报错但仍生成异常 PDF。
- **解决方案**：始终使用 `\pgfdeclarelayer{background}` + `\pgfsetlayers{background,main}` + `\begin{pgfonlayer}{background}`
- **发现日期**：2026-03-28

### [三栏映射图] - zone style 不能在 pgfonlayer 中使用
- **问题/发现**：在 `\begin{pgfonlayer}{background}` 中用 `\node[zone, fit=...]` 时，如果 `zone` style 包含 `inner sep` 等参数，可能导致 zone 框不显示。
- **解决方案**：在 `pgfonlayer` 中直接内联 style（`\fill[dashed, thick, rounded corners=8pt, inner sep=15pt, ...]`），不依赖预定义的 `zone` style。
- **发现日期**：2026-03-28

### [通用] - amsmath 包缺失导致 \boldsymbol 未定义
- **问题/发现**：对比方案图中使用 `\boldsymbol` 但未加载 `amsmath` 包，导致编译报错。
- **解决方案**：在 preamble 中加 `\usepackage{amsmath, amssymb}`，尤其是含数学公式的图。
- **发现日期**：2026-03-29

### [多实例汇聚图] - rotate=90 中文侧栏标签
- **问题/发现**：尝试用 `rotate=90` 放置中文侧栏标签，触发了 xelatex 不可读色块问题。
- **解决方案**：所有中文标注必须水平放置，侧栏标签用多行 `\shortstack` 替代旋转。
- **发现日期**：2026-03-29

### [通用] - stmaryrd 包提供双方括号符号
- **问题/发现**：`\llbracket` / `\rrbracket`（语义双方括号⟦⟧）需要 `stmaryrd` 包，否则编译报错 "Undefined control sequence"。
- **解决方案**：在 preamble 加 `\usepackage{stmaryrd}`。常见于密码学/形式化验证领域的图。
- **发现日期**：2026-03-29
