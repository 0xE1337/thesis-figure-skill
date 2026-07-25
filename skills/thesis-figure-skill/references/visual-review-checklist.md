# 视觉审查清单（19 项 — last-mile bug 检查）

> **本文件是审查条目与数量的唯一真相源（SoT）**：SKILL.md 只引用本清单、不另行规定条目数或 ID 范围。新增/删除条目只改这里，改完同步本行标题的计数。
> **何时加载**：步骤 ④.5 视觉反馈循环中每一轮加载本文件。
> **加载后必须做的事**：Read PNG + Read overlap.json 后**逐项**回答 19 个 Y/N。
> **核心理解**：本清单是 catching last-mile bugs，**不是设计指南**。设计指南在 SKILL.md 顶部 Philosophy 段。
> 19 项全部 Y 仅说明"没有明显 bug"，**不说明"审美达标"**——审美由 Philosophy 段的 UNFORGETTABLE Question 主导。

## 强制流程

```
0. Read PNG + Philosophy 检查（不是机械 19 项之前的前置）
   ↓
   问 3 个 UNFORGETTABLE 问题：
   (a) 审稿人 5 秒看完，记住什么？(若说不出 → blocker)
   (b) 是否避开了 7 个统计中心默认？(box+arrow only / 3 色单调 / 无嵌入 viz / ...)
   (c) 沿主线眼睛走一遍有无"卡住"？
   ↓
1. Read overlap.json（7 类几何检测）
2. 逐项回答下面 19 项 Y/N
3. 任一 N → blocker → patch → recompile → 回 0
4. Philosophy 段 + 19 项全过 → 给用户看
5. 用户也 OK → 交付
```

**两层标准**：Philosophy（审美天花板，主观判断）+ 19 项（地板，机械验证）。**两者都必须过**。

---

## 维度 1：编译保障（4 项 — 编译必过）

- [ ] **T1** 所有数学公式字符（`\mathbf`、`\frac`、下标、希腊字母）渲染正常（无小点、无 sigil、无问号、无空白方块）？
- [ ] **T3** 编译日志无 `Missing character` 警告？
- [ ] **T4** 任一标签都不被截断——对每个 text width < 3cm 的标签盒，显式量字符数 vs box width（中文每字 ~0.4cm，英文每字 ~0.2cm）
- [ ] ⭐ **T5** **字号上限与文字/容器比例**（T4 只管下限方向，本项管上限——缺了它字号规则就是单向棘轮）：
  - **(a) 撑框检测**：任一标签渲染宽度 ≤ 所在框内宽的 **80%**、渲染高度 ≤ 框内高的 **60%**。超出即 N；修法优先级：缩短文案 > 改两行 > 加宽框；**画布已定时禁止放大字号**
  - **(b) 字号回归检测**（round ≥ 2 且本轮动过 `\documentclass` 基准 / `every node` 字号 / 任一 `font=` 档位时**强制**）：并列报出上一轮与本轮的 CJK 字号分布，任一档位涨幅 > 15% 即 N，除非同时按比例缩小了画布
    ```bash
    python3 -c "
    import fitz,sys;from collections import Counter
    p=fitz.open(sys.argv[1])[0];c=Counter()
    for b in p.get_text('dict')['blocks']:
      for l in b.get('lines',[]):
        for s in l.get('spans',[]):
          if any('一'<=ch<='鿿' for ch in s['text']):
            c[round(s['size'],1)]+=len([ch for ch in s['text'] if '一'<=ch<='鿿'])
    print(f'{p.rect.width/28.3465:.2f}cm', dict(sorted(c.items(),reverse=True)))" out.pdf
    ```
  - **(c) 印刷字号复核**：`最小 CJK 字号 × (目标印刷宽度 ÷ PDF 宽度)` ≥ ①.3a 定的目标值。不达标 → **回 ① 重定画布或删内容**，不是原地放大字号

## 维度 2：空间布局（4 项 — 防灾难）

- [ ] **S1** 任意两个文字标签都不重叠（包括轻微 1-2px 触碰）？
- [ ] **S6** 没有可避免的大块白色空带——**强制扫描整图，逐片量连续无内容区域**。任何 > 3cm × 2cm 的空白 → 写 "在 X-Y 范围有 W × H 空白" 并标 N。**注**：细线（rail/leader/dashed/arrow）不算填充内容，必须有 box/text/嵌入 viz 才算
- [ ] ⭐ **S8** **节点几何重叠检测**——读 `pdf-overlap-checker.py --json` 的 `node-overlap` category。每条都是两个 sibling node rect 的真实几何相交（drop shadow / 包含关系已过滤）。逐条对照 PNG triage
- [ ] ⭐ **S9** **最小邻接间距**——逐对相邻元素测量：同行 sibling box ≥ 0.8cm / 跨行 ≥ 0.6cm / text 与 box 边距 ≥ 0.3cm / 连线与无关 box 边距 ≥ 0.4cm

## 维度 3：语义正确（4 项 — 防错画）

- [ ] **M1** 画图指令里列出的**每个模块**在 PNG 中都能找到？
- [ ] **M2** 画图指令里规定的**每条连线**都画出来了？
- [ ] **M3** 每条连线的源/目标方向和指令一致——tip 必须在 destination 端（信息流入处），不是 source 端
- [ ] ⭐ **M8** **Hero substructure 真正"独一无二"**——如果展开内容对所有 instance 都一样（Transformer Layer 1 = Layer 2 = ... = Layer N），**不要绑定具体 instance**。改标题为"通用展开 (Per-stage detail)"

## 维度 4：连线精度（5 项 — canonical 防 bug）

- [ ] **E1** 箭头 tip 真正止于目标框**外侧**（不刺入框内）？默认 `shorten >=2pt`
- [ ] **E2** **`\draw[arrow*]` 的 tip 终点必须是 `node.anchor`，禁止裸坐标 / `\coordinate`**——tip 指向空气 = bug。incoming/spine 段全部用 `\draw[line width=...]`，**禁用 `\draw[arrow]`**
- [ ] ⭐ **E3** **Fan-out / Fan-in canonical**——3+ 条线从同一区域散出或 2+ 条线汇入同一目标的场合：**trunk + spine + N stubs**（不是 N 条独立 \draw）；spine + stubs + outgoing **全 SAME COLOR**（颜色铁律）；折角用 `rounded corners=5pt`
- [ ] ⭐ **E9** **箭头/连线必须用 canonical 模板**——所有 `\draw[arrow]` / `\draw[arrow short]` / `\draw[residual]` 用 `tikz-template.tex` 预定义 styles，**禁止**手写 `-{Stealth[scale=X]}`。短箭头 < 1.5cm 必用 `arrow short`
- [ ] ⭐ **E12** **线穿过节点几何检测**——编译完后**必读** `pdf-overlap-checker.py --json` 的 `line-through-node` category。Triage 规则：① **batch ignore 模式**：≥5 处同类已知误报（heatmap/DNA/收敛节点），写一句批量声明；② **fix 类**：路径绕路穿过无关元素 → blocker，逐处修

## 维度 5：审美底线（2 项 — 美学地板）

- [ ] **A1** 整图视觉平衡（左右两半权重相当，不头重脚轻）？
- [ ] **V1** 复杂档（≥30 节点 / 嵌入 viz / 多 hero）**应该有 ≥1 个嵌入数据可视化** OR **≥1 个信息 panel**（hyperparameters / loss curve / legend / metrics）——若全是 box+arrow 无嵌入 = 视觉失败（Philosophy "FAIL Mode"）。*极简/中等档此项 N/A 一句过*

---

## 审查输出格式

```
=== Visual review round N ===
Philosophy:
  - UNFORGETTABLE: 审稿人会记住 [...]
  - 统计中心默认避开：[box+arrow only / 3 色单调 / 无 viz / ...] 各 Y/N
  - 主线眼睛轨迹：从 [起点] 到 [终点] 无卡住 ✓
19 项：
  [T1] Y/N — 证据
  [T3] Y/N — 证据
  ...
  [V1] Y/N — 证据

Blockers (N items): [...]
Patch plan (单类，最小改动)：[...]
```

**任一 Philosophy 项 fail OR 任一 19 项 N = blocker**。

---

## 升级机制

- **第 3 轮还有 ≥5 blocker** → 局部修补救不了，回 ① 重新设计画图指令
- **同一 blocker 连续 2 轮没修好** → 修复方向错了，换思路
- **自评 + 对抗 agent 全部 0 blocker 后**：**仍把图给用户看**。AI 视觉有结构性盲区（实测案例：fig137 v1 用户看出 11×5cm 空白；v2 用户看出 5 处 bug；v3 用户看出 fan-out 飞角）

---

## 历次用户终审教训（仍生效但不强制写入清单）

老的细则规则（E15 同 anchor、T7 0.5cm、E3 g1-g4 几何、Step 0 E 细线判定、hero sub-layer 间距预算）在 fig137 v1-v3 三代演化中加过，但事后发现 47 项 checklist 把 sub-agent 推到"统计中心防御"——**审美反而退化**。

2026-05-21 重构：精简 47 → 18 项，**释放 sub-agent 创造空间**。具体老教训保留在 `lessons.md`（背景知识），但**不进 checklist 强制执行**。

新教训：
- **fig137 全部 bug** 都因为 sub-agent **机械填规则**而非**整体设计** → philosophy 加 UNFORGETTABLE / Permission 后，期望 sub-agent 在写代码前先想"读者记住什么"
