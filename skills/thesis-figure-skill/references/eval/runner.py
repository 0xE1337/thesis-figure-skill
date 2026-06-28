#!/usr/bin/env python3
"""
回归 eval harness — thesis-figure-skill 的"安全网"

目的：把"我觉得这次改好了"变成**可测量的前后 pass-rate 差**。
对一组冻结的 fixture 跑完整确定性管线，与 baselines/ 对比；
任何 fixture 从 PASS 翻成 FAIL = 回归（退出码 1）。改 skill 前后各跑一次即可。

管线（每个 fixture）：
  spec.json --dot-to-tikz--> .tex --xelatex--> .pdf
        .tex --tikz-validator(几何/语法)-->  exit 0/1/2
        .pdf --pdf-overlap-checker --json--> 按类别计数
  + grep "Missing character" 编译日志

覆盖边界（务必诚实）：
  ✅ 抓得到：编译失败、缺字、微斜线/方向反转(validator ERROR)、文字重叠/溢出、节点/连线几何重叠
  ❌ 抓不到：语义自相矛盾(数字对不上)、"hero 名义在但视觉平"、审美 slop
     —— 这些仍靠 ④.5 视觉回环 + mode-C 对抗闸门。**本 harness 是回归地板，不是质量天花板。**

pdf-overlap-checker 的两个候选类(line-through-node / node-overlap)会对正确图误报，
所以这里**不**用它的原始退出码判定；而是按类别计数 vs baseline：
  - HARD 类(真 bug)：当前数 > baseline 即回归
  - CANDIDATE 类(含已知误报)：当前数 > baseline 才回归（baseline 已把已知 FP 冻进去）

用法：
  python3 runner.py                    跑全部，与 baseline 比对，回归则 exit 1
  python3 runner.py --update-baselines  把当前结果冻结为 baseline（**先人工确认当前状态是对的**）
  python3 runner.py -k fan              只跑名字含 'fan' 的 fixture
  python3 runner.py --keep             保留临时编译产物供排查
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
REFS_DIR = EVAL_DIR.parent                     # references/
FIXTURES = EVAL_DIR / "fixtures"
BASELINES = EVAL_DIR / "baselines"
SNIPPETS = REFS_DIR / "tikz-snippets"

DOT_TO_TIKZ = REFS_DIR / "dot-to-tikz.py"
VALIDATOR = REFS_DIR / "tikz-validator.py"
OVERLAP = REFS_DIR / "pdf-overlap-checker.py"

# 几何重叠类别分级（见 pdf-overlap-checker.py 的 category 字段）
HARD_CATEGORIES = {
    "text-overlap", "text-overflow", "off-center", "top-heavy",
    "text-line", "line-crossing",
}
CANDIDATE_CATEGORIES = {"line-through-node", "node-overlap"}

COMPILE_TIMEOUT = 180
TOOL_TIMEOUT = 120


# ── 管线步骤 ──────────────────────────────────────────────────────────────

def _run(cmd, cwd=None, timeout=TOOL_TIMEOUT):
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
    )


def spec_to_tex(spec_path: Path, out_tex: Path) -> tuple[bool, str]:
    r = _run([sys.executable, str(DOT_TO_TIKZ), str(spec_path), "-o", str(out_tex)])
    out = (r.stderr or r.stdout).strip().splitlines()
    return r.returncode == 0, (out[-1] if out else "")


def validate_tex(tex_path: Path) -> int:
    r = _run([sys.executable, str(VALIDATOR), str(tex_path)])
    return r.returncode


def compile_tex(tex_path: Path, workdir: Path) -> tuple[bool, bool]:
    """返回 (compile_ok, missing_char)。"""
    _run(
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=workdir, timeout=COMPILE_TIMEOUT,
    )
    pdf = workdir / (tex_path.stem + ".pdf")
    log = workdir / (tex_path.stem + ".log")
    compile_ok = pdf.exists() and pdf.stat().st_size > 0
    missing_char = False
    if log.exists():
        missing_char = "Missing character" in log.read_text(errors="ignore")
    return compile_ok, missing_char


def check_overlap(pdf_path: Path) -> tuple[dict, int, int]:
    """返回 (per-category counts, error_count, warn_count)。"""
    r = _run([sys.executable, str(OVERLAP), str(pdf_path), "--json"])
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"__parse_error__": 1}, -1, -1
    cats = Counter()
    for item in data.get("errors", []) + data.get("warnings", []):
        cats[item["category"]] += 1
    summ = data.get("summary", {})
    return dict(cats), summ.get("error_count", -1), summ.get("warning_count", -1)


# ── 单 fixture 执行 ───────────────────────────────────────────────────────

def run_fixture(name: str, kind: str, src: Path, workdir: Path, keep: bool) -> dict:
    """kind ∈ {spec, tex, neg-validator, neg-overlap}。返回观测结果 dict。"""
    work = workdir / name
    work.mkdir(parents=True, exist_ok=True)
    tex = work / (name + ".tex")
    res: dict = {"kind": kind}

    if kind == "spec":
        ok, msg = spec_to_tex(src, tex)
        res["dot_ok"] = ok
        if not ok:
            res["dot_msg"] = msg
            return res
    else:
        shutil.copyfile(src, tex)

    res["validator_exit"] = validate_tex(tex)

    if kind == "neg-validator":
        return res  # 只需 validator

    compile_ok, missing_char = compile_tex(tex, work)
    res["compile_ok"] = compile_ok
    res["missing_char"] = missing_char
    if compile_ok:
        cats, ec, wc = check_overlap(work / (name + ".pdf"))
        res["overlap_categories"] = cats
        res["overlap_error_count"] = ec
        res["overlap_warn_count"] = wc
    return res


# ── 比对 ─────────────────────────────────────────────────────────────────

def compare_normal(res: dict, base: dict) -> list[str]:
    regs = []
    if res.get("kind") == "spec" and not res.get("dot_ok", True):
        return [f"dot-to-tikz 失败：{res.get('dot_msg','')}"]
    if base.get("compile_ok") and not res.get("compile_ok"):
        regs.append("编译从成功变失败")
    if res.get("missing_char") and not base.get("missing_char"):
        regs.append("出现 Missing character（之前没有）")
    bve, rve = base.get("validator_exit", 0), res.get("validator_exit", 0)
    if rve == 2 and bve != 2:
        regs.append(f"tikz-validator 报 ERROR(exit2)，baseline 是 exit{bve}")
    elif rve > bve:
        regs.append(f"tikz-validator 退出码升高 {bve}→{rve}（新增 WARN）")
    base_cats = base.get("overlap_categories", {})
    res_cats = res.get("overlap_categories", {})
    for cat in sorted(set(base_cats) | set(res_cats)):
        b, c = base_cats.get(cat, 0), res_cats.get(cat, 0)
        if c > b and (cat in HARD_CATEGORIES or cat in CANDIDATE_CATEGORIES):
            tag = "真 bug 类" if cat in HARD_CATEGORIES else "候选类(可能误报)"
            regs.append(f"overlap [{cat}] {tag} 从 {b} 增到 {c}")
        if cat == "__parse_error__":
            regs.append("pdf-overlap-checker 输出无法解析")
    return regs


def check_negative(name: str, kind: str, res: dict) -> tuple[bool, str]:
    """负向 fixture：闸门必须开火。返回 (ok, detail)。"""
    if kind == "neg-validator":
        ok = res.get("validator_exit") == 2
        return ok, (f"validator exit={res.get('validator_exit')} "
                    f"({'✓ 捕获' if ok else '✗ 漏检！闸门被削弱'})")
    if kind == "neg-overlap":
        ec = res.get("overlap_error_count", 0)
        ok = bool(res.get("compile_ok")) and ec >= 1
        return ok, (f"compile_ok={res.get('compile_ok')} overlap_errors={ec} "
                    f"({'✓ 捕获' if ok else '✗ 漏检！闸门被削弱'})")
    return False, "未知负向类型"


# ── fixture 发现 ──────────────────────────────────────────────────────────

def discover() -> list[tuple[str, str, Path]]:
    items: list[tuple[str, str, Path]] = []
    for p in sorted((FIXTURES / "specs").glob("*.json")):
        items.append((p.stem, "spec", p))
    for p in sorted((FIXTURES / "tex").glob("*.tex")):
        items.append((p.stem, "tex", p))
    manifest = FIXTURES / "library.txt"
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            sp = SNIPPETS / line
            if sp.exists():
                items.append(("library__" + sp.stem, "tex", sp))
            else:
                print(f"  ⚠ library.txt 引用了不存在的片段：{line}", file=sys.stderr)
    for p in sorted((FIXTURES / "negative" / "validator").glob("*.tex")):
        items.append(("neg_val__" + p.stem, "neg-validator", p))
    for p in sorted((FIXTURES / "negative" / "overlap").glob("*.tex")):
        items.append(("neg_ovl__" + p.stem, "neg-overlap", p))
    return items


# ── 主流程 ───────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="thesis-figure-skill 回归 eval harness")
    ap.add_argument("--update-baselines", action="store_true",
                    help="把当前结果冻结为 baseline（先人工确认当前状态正确）")
    ap.add_argument("-k", "--filter", default="", help="只跑名字含该子串的 fixture")
    ap.add_argument("--keep", action="store_true", help="保留临时编译产物")
    args = ap.parse_args()

    for tool in (DOT_TO_TIKZ, VALIDATOR, OVERLAP):
        if not tool.exists():
            print(f"FATAL: 找不到 {tool}", file=sys.stderr)
            return 2
    BASELINES.mkdir(exist_ok=True)

    items = [it for it in discover() if args.filter in it[0]]
    if not items:
        print("没有匹配的 fixture", file=sys.stderr)
        return 2

    tmp = Path(tempfile.mkdtemp(prefix="figeval-"))
    passed = failed = 0
    failures: list[str] = []
    try:
        for name, kind, src in items:
            res = run_fixture(name, kind, src, tmp, args.keep)

            if kind.startswith("neg-"):
                ok, detail = check_negative(name, kind, res)
                print(f"[{'PASS' if ok else 'FAIL'}] {name:32s} (负向) {detail}")
                if ok:
                    passed += 1
                else:
                    failed += 1
                    failures.append(f"{name}: 负向闸门漏检 — {detail}")
                continue

            base_path = BASELINES / (name + ".json")
            if args.update_baselines:
                base_path.write_text(json.dumps(res, ensure_ascii=False, indent=2))
                print(f"[BASE] {name:32s} 已写入 baseline")
                passed += 1
                continue

            if not base_path.exists():
                print(f"[MISS] {name:32s} 无 baseline（先跑 --update-baselines）")
                failed += 1
                failures.append(f"{name}: 缺 baseline")
                continue

            base = json.loads(base_path.read_text())
            regs = compare_normal(res, base)
            if regs:
                failed += 1
                print(f"[FAIL] {name:32s}")
                for r in regs:
                    print(f"         ↳ {r}")
                failures.append(f"{name}: " + "; ".join(regs))
            else:
                passed += 1
                ov = res.get("overlap_error_count", "-")
                print(f"[PASS] {name:32s} compile={res.get('compile_ok')} "
                      f"validator=exit{res.get('validator_exit')} overlap_err={ov}")
    finally:
        if args.keep:
            print(f"\n临时产物保留在 {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    total = passed + failed
    print(f"\n{'='*54}\n结果：{passed}/{total} PASS"
          + (f"  ({failed} 回归/失败)" if failed else "  —— 无回归")
          + f"\n{'='*54}")
    if failures and not args.update_baselines:
        print("回归清单：")
        for f in failures:
            print(f"  ✗ {f}")
    return 1 if (failed and not args.update_baselines) else 0


if __name__ == "__main__":
    raise SystemExit(main())
