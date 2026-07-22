# Worked example — 绝对坐标 vs 按构造

同一张 5-stage ML pipeline 图，两种写法，**渲染视觉等价**：

| 文件 | 写法 | 编辑安全 |
|---|---|---|
| `pipeline-absolute-coords-BAD.tex` | `\node at (2.25,6.8)` + 手画 `rectangle` + 箭头坐标 `{4.5/5.0,...}` | ❌ 脆 |
| `pipeline-by-construction-GOOD.tex` | `right=of` 链 + 节点 anchor 箭头 + `text width` + calc 中点 | ✅ |

## BAD 版的脆弱性

"stage 间距 5cm"和"stage-1 中心 2.25"被手抄在 **5 个互相独立的地方**：
1. `\drawstage` 的 x 边界（0/4.5, 5/9.5, …）
2. 各 stage 内容硬中心（`at (2.25,…)`, `at (7.25,…)`…）
3. inter-stage 箭头 `\foreach \a/\b in {4.5/5.0, 9.5/10.0, …}`（把 zone 边界又抄一遍）
4. summary bar `2.25 + (\i-1)*5`
5. legend `1.5 + (\i-1)*4.5`

改一个 stage 宽度 / 加一个 stage → 这 5 处必须手动同步，漏一处崩。

## 证明：同一个编辑，两版的命运

`proof-edit-safety-hero-widen.png` —— 对两版施加**同一个最自然的编辑**：加宽 hero stage（各改 1 处）。

- **BAD 版**：紫色 hero zone 压进 Stage 4，竖边框一条线切穿整个 Stage 4 的内容，两 zone 重叠。
- **GOOD 版**：Stage 4/5 自动右移腾空间、箭头跟随节点、底栏/legend/标题全部同步。完美重排。

**关键 meta 发现**：BAD 版崩成那样，`tikz-validator` + `pdf-overlap-checker` **全报 0 硬 bug**。
⇒ 静态检查不是安全网，**写法**才是。lint 过了仍必须亲眼看渲染 PNG。

## 自己验证

```bash
bash ../lint.sh pipeline-by-construction-GOOD.tex     # HARD 0, 退出码 0
# 编辑两版的 hero 宽度，各跑 lint + 看 .lint.png，对比命运
```
