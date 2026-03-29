# 时序交互图专项规则

> **何时加载**：用户提及"时序图""交互流程""多方协议""消息传递""生命线"时加载。

## 时序交互图专项规则

时序交互图（Sequence Diagram）用于展示多方协议交互流程，在区块链、密码学、分布式系统论文中极为常见。

### 适用场景

用户提及"时序图""交互流程""多方协议""消息传递""生命线"，或文案描述的是 A→B→C→D 的多方消息交换过程。

### 布局核心原则

**字号必须足够大**——时序图通常纵向很长（15cm+），如果用 `\footnotesize` 作全局默认，渲染成 PNG 后文字会非常小。规则：
- 参与方标题：`\small\bfseries`
- 消息标注（箭头上方的 tag）：`\footnotesize`
- 自调用弧旁标注：`\footnotesize`
- 注释框内容：`\footnotesize`
- 阶段标签：`\small\bfseries`
- **禁止**在时序图中使用 `\scriptsize` 或 `\tiny` 作为主要标注字号

**参与方水平间距**：用绝对坐标（`at (0,0)`, `at (5.5,0)`, `at (11,0)`, ...），间距 5–6cm。不要用 `right=3.8cm of` 等相对定位——容易导致间距过大而内容区域空旷。4 个参与方总宽度控制在 16–17cm。

**垂直间距紧凑**：
- 同一阶段内的消息/自调用弧间距 0.5–0.6cm
- 阶段之间间距 0.8–1.0cm（不超过 1.2cm）
- 整图纵向总长度控制在 17–20cm（6 个阶段以内）

**填充中间空白**——时序图最常见的问题是"阶段二三只有用户自调用，中间几列完全空着"。解决方法：
- 自调用弧加宽到 2.0cm（而非默认的 1.2cm），标注文字放在弧的右侧
- **注释框（note）放在两条生命线之间的空白区域**（如 edge 和 chain 之间），而非放在最右侧被裁切
- 注释框 `text width` 设为 3.8–4.2cm，能填满两列之间的空间

### 必备视觉元素

| 元素 | style | 说明 |
|------|-------|------|
| 参与方标题框 | `participant` | 圆角矩形，各方用不同颜色，含角色名和数学符号 |
| 生命线 | `lifeline` | 竖直虚线，颜色与参与方一致（`color=#1!60`） |
| 激活条 | `activation` | 窄矩形（宽 0.3cm），表示该方正在处理，`fill=#1!25, draw=#1!70` |
| 消息箭头 | `msg` | 实线带箭头，颜色与发送方一致；虚线表示异步/可选 |
| 自调用弧 | `selfcall` | 从激活条右侧伸出的 U 型弧，表示内部处理步骤 |
| 阶段标签 | `phase` | 左侧红色圆角框，标注"阶段N：XXX" |
| 注释框 | `note` | 黄色圆角框，放在生命线之间的空白区域，补充说明 |
| 阶段背景色 | `\fill[...Fill!15]` | 每个阶段一个浅色背景横条，增加层次感 |

### 回路/重试线规则

时序图中的回路线（如"验证失败→重新生成"）：
- **rail 竖直线必须在所有阶段标签的外侧**，距离用户生命线 2.5cm 以上
- rail 与阶段标签之间间距 ≥ 0.5cm，避免视觉混淆
- "重试"等标签用水平放置的 `tag`（不用 `rotate=90`，竖排在时序图中可读性差）
- 回路线用 `dashed, rounded corners=6pt`，颜色用 `drawRedLine!50`（半透明避免喧宾夺主）
- `border` 设为 25pt 以上，确保回路线不被裁切

### 异常分支

在正常流程之后添加"异常"阶段（灰色阶段标签），用红色虚线箭头表示失败路径。异常分支的消息方向通常是反向的（Chain→Edge→User）。

### style 定义模板

```latex
participant/.style={rectangle, rounded corners=4pt, align=center,
    minimum height=1.1cm, minimum width=2.8cm,
    drop shadow={opacity=0.15}, thick, font=\small\bfseries},
msg/.style={-{Stealth[scale=1.0]}, thick, color=#1},
tag/.style={font=\footnotesize, fill=white, inner sep=2pt, rounded corners=1pt},
phase/.style={font=\small\bfseries, text=drawRedLine, fill=drawRedFill,
    inner sep=5pt, rounded corners=3pt, draw=drawRedLine, thick},
lifeline/.style={dashed, thick, color=#1!80},  % ≥!80，!60在浅色背景上不可见
activation/.style={fill=#1!30, draw=#1!80, thick, rounded corners=1pt,
    minimum width=0.45cm},  % 宽度≥0.4cm，0.3cm在300dpi下几乎不可见
selfcall/.style={-{Stealth[scale=0.9]}, thick, rounded corners=3pt, color=#1},
note/.style={rectangle, rounded corners=3pt, draw=drawGreyLine!60, fill=drawYellowFill,
    align=left, font=\footnotesize, inner sep=6pt, text width=3.8cm},
```

### UML 组合片段（par/loop/alt/opt）

时序图中的组合片段（combo fragment）用于表示并行执行、循环、条件分支等控制逻辑。

**style 定义**：
```latex
% 组合片段框 — 线宽≥1.2pt，颜色≥!90，确保在浅色阶段背景上清晰可见
combo/.style={rectangle, draw=drawGreyLine!90, fill=none, dashed,
    inner sep=0pt, rounded corners=2pt, line width=1.2pt},
% 组合片段类型标签（如 "par"、"loop"、"alt"）— 字号用\small加粗，不能太小
combo_label/.style={rectangle, fill=drawGreyFill, draw=drawGreyLine!90,
    font=\small\bfseries, inner sep=4pt, rounded corners=2pt},
% 条件分隔线（alt 框内的虚线）— 颜色≥!80
combo_divider/.style={dashed, drawGreyLine!80, line width=1.0pt},
% 条件标签（如 "[验证通过]"、"[验证失败]"）
combo_guard/.style={font=\footnotesize\itshape, text=drawGreyLine},
```

**绘制规则**：
1. **combo 框坐标**：左边界 = 最左参与方 x - 1.0cm，右边界 = 最右参与方 x + 2.5cm，上边界 = 第一条消息 y - 0.3cm，下边界 = 最后一条消息 y + 0.3cm
2. **类型标签位置**：combo 框左上角内侧（`combo_label` at 框.north west + (0.3, -0.15)）
3. **alt 分隔线**：水平虚线从框左边界到右边界，y = 两个分支之间的中点
4. **条件守卫标签**：`[条件]` 放在分隔线下方 0.2cm，左对齐（x = 框左边界 + 1.0cm）
5. **par 框**：左右边界紧贴相关参与方（不要延伸到无关参与方），分隔线表示并行分支
6. **loop 框**：类型标签写 `loop [条件]`，注意中英文混排时数学模式的空格：用 `loop [$k$ 轮]` 而非 `loop $[k$~轮$]$`
7. **嵌套**：combo 框可以嵌套，内层框缩进 0.3cm，使用更浅的虚线颜色

### 激活条坐标计算（关键规则）

激活条的 y 坐标必须**使用与消息相同的绝对 y 值**，不要用相对偏移手动估算。

**计算公式**：
- 激活条起始 y = 该参与方**收到第一条消息**的 y - 0.2cm
- 激活条结束 y = 该参与方**发出最后一条消息**的 y + 0.2cm
- 激活条宽度 = 0.45cm（⚠️ 0.3cm 在 300dpi 渲染后几乎不可见），中心 x = 参与方 x

**绘制方式**：
```latex
% 推荐：使用绝对 y 坐标，与消息行精确对齐
\fill[activation=blue] ([xshift=-0.15cm]P.south |- 0,-3.0)
    rectangle ([xshift=0.15cm]P.south |- 0,-8.5);
% 其中 -3.0 和 -8.5 是该参与方首尾消息的 y 坐标 ± 0.2cm
```

**禁止**：用 `++(0, -offset) rectangle ++(0.3, -height)` 的相对偏移方式——数值是手动估算的，极易导致激活条与消息行不对齐。

### 自调用弧方向选择

- **最右侧参与方**的自调用弧**必须向左伸出**（而非向右），否则弧和标签会超出画布右边界
- 具体做法：从激活条左侧边缘出发，向左伸出 1.5cm 形成 U 型弧，标签放在弧的左侧
- 其他参与方默认向右伸出
- 自调用弧标签的 `text width` 控制在 3.0cm 以内，避免超出 border

### 自检清单（时序图专用）

- [ ] 全局字号 ≥ `\small`，标注字号 ≥ `\footnotesize`
- [ ] 参与方间距 5–6cm，总宽度 ≤ 17cm
- [ ] 每个阶段内垂直间距 ≤ 0.6cm，阶段间 ≤ 1.0cm
- [ ] 无大面积空白区域（注释框已填充到生命线之间）
- [ ] 自调用弧宽度 ≥ 2.0cm
- [ ] **最右侧参与方的自调用弧向左伸出**，标签不超出 border
- [ ] 回路线 rail 在阶段标签外侧，标签水平放置
- [ ] border ≥ 25pt，回路线不被裁切
- [ ] 阶段背景色覆盖完整，无间隙无重叠
- [ ] **激活条 y 坐标使用绝对值**，与首尾消息行精确对齐
- [ ] **combo 框左右边界紧贴相关参与方**，不过度延伸
- [ ] combo 标签中的数学公式排版正确（无多余空格）
- [ ] `\shortstack` 多行文字行距充足（用 `\\[3pt]` 增加行距）
- [ ] **编译后 grep "Missing character" 检查字体是否缺失**
- [ ] **渲染后视觉审查**（必须打开 PNG 查看，不可仅凭代码判断）：
  - [ ] 所有 5 条生命线在阶段背景色上清晰可见（颜色 ≥ !80）
  - [ ] 激活条在 300dpi 下肉眼可辨（宽度 ≥ 0.45cm）
  - [ ] combo 框虚线在阶段背景上清晰可见（线宽 ≥ 1.2pt，颜色 ≥ !90）
  - [ ] combo 类型标签（par/loop/alt）字号足够大（≥ \small）
  - [ ] 每个参与方列都有足够的交互内容，无大面积空列
  - [ ] 自调用弧清晰可见，标签可读
  - [ ] 整图纵横比 ≤ 1:1.5（过长则压缩阶段间距或增加横向宽度）
