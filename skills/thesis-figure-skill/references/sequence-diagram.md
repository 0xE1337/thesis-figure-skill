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
lifeline/.style={dashed, thick, color=#1!60},
activation/.style={fill=#1!25, draw=#1!70, thick, rounded corners=1pt},
selfcall/.style={-{Stealth[scale=0.9]}, thick, rounded corners=3pt, color=#1},
note/.style={rectangle, rounded corners=3pt, draw=drawGreyLine!60, fill=drawYellowFill,
    align=left, font=\footnotesize, inner sep=6pt, text width=3.8cm},
```

### 自检清单（时序图专用）

- [ ] 全局字号 ≥ `\small`，标注字号 ≥ `\footnotesize`
- [ ] 参与方间距 5–6cm，总宽度 ≤ 17cm
- [ ] 每个阶段内垂直间距 ≤ 0.6cm，阶段间 ≤ 1.0cm
- [ ] 无大面积空白区域（注释框已填充到生命线之间）
- [ ] 自调用弧宽度 ≥ 2.0cm
- [ ] 回路线 rail 在阶段标签外侧，标签水平放置
- [ ] border ≥ 25pt，回路线不被裁切
- [ ] 阶段背景色覆盖完整，无间隙无重叠
