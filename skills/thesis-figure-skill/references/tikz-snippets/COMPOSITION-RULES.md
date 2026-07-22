# Snippet 组合规则

> **何时读**：复杂档准备拼装 ≥ 3 个 snippet 时必读。
> **核心**：snippet 解决"局部质量"，组合规则解决"全局组合"。Batch 17 fig153 v3 教训：sub-agent 把 snippets 都塞进去了，但 snippets 之间的留白、对齐、Z-order 没规划 = 整图仍乱。

## 1. 三种推荐整图骨架（选一个）

### A. 双栏对称（Encoder/Decoder 类）
参考：examples 06 Transformer
```
+----- TITLE + AUTHOR -----+
|                          |
|  Hyperparams Box (LU)    |
|                          |
|  [Stage A]    [Stage B]  |
|  Encoder      Decoder    |
|  (mirror)     (mirror)   |
|                          |
|  [Input]      [Output]   |
|                          |
+--- Color Legend (bottom) -+
```

### B. 5 Stage 横向（Pipeline 类）
参考：examples 08 Diffusion / test-gat
```
+---- TITLE ----+
[S1] [S2] [S3] [S4] [S5]
 每 stage 含 viz + box + 标签
+---- Summary Bar (bottom) -----+
A → B → C → D → E
```

### C. 中央 hero + 4 panels（含 benchmark 的 paper-style）
参考：examples 06 Transformer 风格
```
+---- TITLE ----+
| [Hyperp]      [Benchmark]|
| (LU)          (RU)       |
|                          |
|   Central Hero (BIG)     |
|                          |
| [Pipeline] [Color Legend]|
| (LD)       (RD)          |
+--------------------------+
```

**v3 失败原因**: 用 C 骨架但 4 panels 与 hero 间距不足，且 hero 内部太挤。

## 2. snippet 间留白铁律

| 元素间关系 | 最小间距 |
|---|---|
| Stage container 之间（横向）| 0.8cm |
| Snippet 容器（如 heatmap）与 zone 边框 | 0.4cm |
| 公式 box 之间 | 1.0cm |
| Panel 与 main flow | 1.2cm |
| Color Legend 与最近 zone | 0.8cm |
| Title 与下方第一行内容 | 0.6cm |

**fig153 v3 违规**: 中下 4 个公式 box（GQA Attn Matrix / RMSNorm / SwiGLU / RoPE）间距 < 0.3cm → 视觉重叠。

## 3. 对齐铁律

| 多个 snippet 在同一 row | 必须 |
|---|---|
| 同一行所有 stage container | **同 y top + 同 height** |
| 同一列所有 panel | **同 x left + 同 width** |
| 公式 box 在 hero 下方 | 多个公式同 y baseline |

## 4. Z-order 铁律

层次（从下到上）：
1. **底层**：zone background fills（acaXxxBg, opacity 0.3-0.5）
2. **中层**：connector arrows (canonical fan-out / pipe arrow)
3. **上层**：box + text + labels
4. **最上**：标题 + Color Legend + annotations

**v3 违规**: 左下"孤立黄色 bar"是个未被任何 zone 包含的元素 — 应该在某个 stage 内部 OR 删掉。

## 5. 整图配色策略（必选 ≤ 6 色）

参考 `multi-zone-palette.tex`。选色规则：
- **1 个 accent 色**：hero / 最重要元素（紫 OR 橙）
- **2-3 个主色**：主流 stage（蓝 / 绿）
- **1-2 个辅色**：辅助 panel（青 / 金）
- **灰色**：annotation / leader / 次要 box border

**不要做**：
- ❌ 一个 stage 自带橙色但其他 stage 都是冷色 → 突兀
- ❌ 用了 5+ 鲜艳色 → 喧闹
- ❌ 全冷色 / 全暖色 → 缺 accent

**选色原则**（同一实体全图同色、灰度打印仍可分、红绿留给有向语义）见 `references/tikz-colors.md` 顶部"配色原则"。

## 6. 必备元素（复杂档）

| 元素 | 用 snippet | 位置 |
|---|---|---|
| 标题 + author + year | （自己写）| 顶部 |
| ≥1 嵌入 viz | attention-heatmap / embedded-graph / scatter-plot | 在某 stage 内 |
| ≥1 信息 panel | hyperparams-table / bar-chart | 角落 |
| ≥2 公式 box | formula-box | 与对应模块同 zone |
| Color Legend | color-legend | **底部** |
| Pipeline Summary Bar（可选 stage 类）| summary-bar | 底部（在 legend 上方） |

## 6.5 反冗余：每个 panel / 嵌入图回答唯一问题（借鉴 nature-figure）

复杂档常见失败：snippet 都塞进去了，但**两个 panel 在用不同图形重复同一份信息** = 信息密度的假象，审稿人一眼看穿。

**铁律**：盖住任意一个 panel，整图必须**丢掉一条无法从其它 panel 推回的信息**。盖住后没损失 = 那个 panel 冗余 → 合并或删掉。

**结构图里的高频冗余陷阱**：

| 陷阱 | 例子 | 修复 |
|---|---|---|
| 同数据两种画法 | 上方 pipeline 已画 5 stage，下方 summary-bar 又把同样 5 stage 平铺一遍 | summary-bar 改为承载**新信息**（每 stage 耗时/参数量），只重复就删 |
| 父集的子集 | hero 内部已展开 Attention，旁边又单画一张 attention-heatmap 重复同一矩阵 | 旁边换成**补充维度**（不同 head 对比 / 消融），否则删 |
| 装饰性重复 | 每个 stage 都配一个长得一样、不传递差异的小图标 | 图标只在**区分语义**时保留，纯装饰删 |
| 两张同类信息 panel | 两个 bar-chart 比的是相关指标 | 合并成分组柱状，或一张换成关系图（scatter）|

**与 ①.0 图契约呼应**：契约里的"能不能更少？"在这里落到 panel 粒度——每个 panel 都要能在契约的**证据层级**里找到唯一位置（hero 一处、各支撑各一处）。

## 7. 检查清单（拼装完成后）

- [ ] 整图有标题 + author + year
- [ ] 选了 A/B/C 三种骨架之一
- [ ] 同 row 模块同 height
- [ ] 所有 snippet 之间 ≥ 0.4cm padding（公式 box 之间 ≥ 1.0cm）
- [ ] 配色 ≤ 6 色，有 1 accent
- [ ] 底部有 Color Legend OR Summary Bar
- [ ] 没有孤立悬空元素（每个元素都属于某 zone）
- [ ] Hero 是视觉中心（最大 + accent 色）
- [ ] 嵌入 viz 真的在 stage 内（不是浮在边缘）
- [ ] 没有两个 panel 用不同图形重复同一信息（盖住任一 panel 都会丢失独有信息，见 §6.5）
