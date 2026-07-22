# 回归 eval harness

**给 skill 维护者用，不是给生成图的 agent 用。** 解决一个具体痛点：改了 skill 之后，
"这次到底是改好了还是改坏了"无法测量 —— 所以质量在多次编辑间非单调抖动。

本 harness 把"我觉得改好了"变成**可测量的前后 pass-rate 差**：对一组冻结的 fixture 跑完整确定性
管线，与 `baselines/` 对比，任何 fixture 从 PASS 翻成 FAIL = 回归（退出码 1）。

## 工作流（每次改 SKILL.md / references 前后各跑一次）

```bash
cd references/eval
python3 runner.py            # 改之前：确认当前全绿（建立你信任的基线状态）
# … 编辑 skill …
python3 runner.py            # 改之后：若出现 FAIL，就是这次编辑引入的回归
```

- **全绿 + 退出码 0** → 这次编辑没有引入"几何/编译可检测"的回归。
- **任何 FAIL + 退出码 1** → 看回归清单，定位是哪个 fixture 的哪类指标变差了。

仅当你**人工确认当前输出确实是对的、且想把它当作新基准**时，才更新基线：

```bash
python3 runner.py --update-baselines
```

其它开关：`-k <子串>` 只跑匹配的 fixture；`--keep` 保留临时编译产物供排查。

## 管线

```
specs/*.json  --dot-to-tikz.py-->  .tex --xelatex--> .pdf
                       .tex --tikz-validator.py(几何/语法)-->  exit 0/1/2
                       .pdf --pdf-overlap-checker.py --json--> 按类别计数
library.txt 列出的库内片段、tex/*.tex   直接走 .tex --xelatex--> .pdf --> 同上
                       + grep "Missing character" 编译日志
```

## 判定逻辑（为什么不用 checker 的原始退出码）

`pdf-overlap-checker.py` 的两个**候选类**（`line-through-node` / `node-overlap`）会对正确图
误报（投影孪生框、数学下标、热力图 cell 等）。所以正常 fixture 的判定不看原始退出码，而是
按类别 vs baseline：

| 类别 | 判定 |
|---|---|
| **HARD**（text-overlap / text-overflow / off-center / top-heavy / text-line / line-crossing / node-outside-zone）| 当前数 > baseline → 回归 |
| **CANDIDATE**（line-through-node / node-overlap）| 当前数 > baseline → 回归（baseline 已把已知误报冻进去；只抓**增量**）|
| `tikz-validator` | 出现 ERROR(exit 2) 或退出码升高 → 回归 |
| 编译 | 从成功变失败、或新增 Missing character → 回归 |

## fixture 布局

```
fixtures/
├── specs/*.json              # B 路结构图：linear-pipeline / fan-out / fan-in / multi-zone / branch-reconverge
├── tex/*.tex                 # （可选）直接编译的独立 .tex
├── library.txt              # 选取库内片段当 fixture（运行时从 ../tikz-snippets/ 解析，不复制）
└── negative/
    ├── validator/*.tex       # 负向：validator 必须报 ERROR(exit 2)（证明几何门没被削弱）
    └── overlap/*.tex         # 负向：pdf-overlap 必须报 ≥1 ERROR（证明重叠门没被削弱）
baselines/*.json             # 每个正常 fixture 的冻结期望（compile / validator exit / 各类别计数）
```

**负向 fixture 不需要 baseline** —— 它们的期望是固定的"闸门必须开火"。它们防的是：将来有人
改弱了某个 checker 却没人发现。

## 覆盖边界（务必诚实）

✅ 抓得到：编译失败、缺字、微斜线/方向反转、文字重叠/溢出、节点/连线几何重叠、子框超出所属 zone（内容超容器尺寸）、布局/模板/checker 自身回归。
❌ **抓不到**：语义自相矛盾（数字对不上）、"hero 名义在但视觉平"、审美 slop、配色协调。
   这些仍依赖 ④.5 视觉回环 + mode-C 对抗闸门。**本 harness 是回归地板，不是质量天花板。**

## 可选：LLM 层（非确定性，不进 CI 门）

`fixtures/specs/*.json` 让管线**无需调用模型**即可确定性运行，适合 CI。若要测"prose 引导"层面的
回归（改了 SKILL.md 的措辞是否让生成结果变差），需要存一组自然语言 prompt、真实跑生成 agent、
再把产出喂给同样的 checker —— 那是非确定性的，建议人工触发，不作为硬门。

## 依赖

见 `requirements.txt`。**依赖/工具版本变化会让 baseline 漂移**，升级后需重建基线。
