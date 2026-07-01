#!/bin/bash
# =============================================================================
# tikz-figure-code: ONE static-check entry point for a TikZ figure .tex
# =============================================================================
# Pipeline:  pre-compile lint  ->  xelatex  ->  missing-char gate  ->  overlap
#
#   1. tikz-validator.py      (static) micro-slope / overflow / collision / dir
#   2. xelatex                 must compile
#   3. grep "Missing character" must be 0  (xelatex fails SILENTLY on bad fonts)
#   4. pdf-overlap-checker.py  (post-compile) text-overlap/overflow/off-center/
#                              line-through-node/node-overlap (HARD vs candidate)
#   5. tikz-design-linter.py   (advisory) density metrics — never blocks
#
# Exit code:  0 = clean (no HARD issues)   1 = HARD issues found   2 = setup err
#
# Checkers live in the thesis-figure-skill bundle (single source of truth).
# Override the location with:  TFS_REFS=/path/to/thesis-figure-skill/references
# =============================================================================
set -uo pipefail

f="${1:-}"
[ -z "$f" ] && { echo "usage: lint.sh <figure.tex>"; exit 2; }
[ -f "$f" ] || { echo "no such file: $f"; exit 2; }

# --- locate the checkers (sibling thesis-figure-skill by default) ------------
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFS="${TFS_REFS:-$here/../../thesis-figure-skill/references}"
if [ ! -f "$REFS/tikz-validator.py" ]; then
  echo "!! checkers not found under: $REFS"
  echo "   set TFS_REFS to the thesis-figure-skill/references dir"
  exit 2
fi

dir="$(cd "$(dirname "$f")" && pwd)"; base="$(basename "${f%.tex}")"
cd "$dir" || exit 2
hard=0

echo "── 1. pre-compile static lint (tikz-validator) ──────────────────────"
python3 "$REFS/tikz-validator.py" "$base.tex"; vrc=$?
[ $vrc -eq 2 ] && { echo "   ↑ ERROR class — fix before compiling"; hard=1; }

echo "── 2. compile (xelatex) ─────────────────────────────────────────────"
if xelatex -interaction=nonstopmode -halt-on-error "$base.tex" >"$base.lint.log" 2>&1; then
  echo "   compile OK"
else
  echo "   !! COMPILE FAILED:"; grep -m3 -E "^! " "$base.lint.log" | sed 's/^/     /'
  exit 1
fi

echo "── 3. missing-character gate (silent-font-failure) ──────────────────"
mc=$(grep -c "Missing character" "$base.log" 2>/dev/null || true)
if [ "${mc:-0}" -gt 0 ]; then
  echo "   !! $mc Missing-character lines — a font (often CJK) is not resolving"
  grep -m3 "Missing character" "$base.log" | sed 's/^/     /'
  hard=1
else
  echo "   0 missing characters"
fi

echo "── 4. post-compile geometry (pdf-overlap-checker) ───────────────────"
pdftoppm -png -r 150 -singlefile "$base.pdf" "$base.lint" >/dev/null 2>&1
python3 "$REFS/pdf-overlap-checker.py" "$base.pdf" --json >"$base.overlap.json" 2>/dev/null
ovh=$(python3 - "$base.overlap.json" <<'PY'
import json,sys
from collections import Counter
HARD={'text-overlap','text-overflow','off-center','text-line','node-overlap','line-crossing'}
d=json.load(open(sys.argv[1])); errs=d.get('errors',[])
c=Counter(e.get('category') for e in errs)
h={k:v for k,v in c.items() if k in HARD}
cand={k:v for k,v in c.items() if k not in HARD}
print("HARD",sum(h.values()),"|",dict(h) if h else "{}")
print("CAND",sum(cand.values()),"|",dict(cand) if cand else "{}",
      "(line-through-node/node-overlap are often FP on heatmaps/matrices/fan-in — triage against the PNG)")
PY
)
echo "$ovh" | sed 's/^/   /'
echo "$ovh" | grep -q "^HARD [1-9]" && hard=1

echo "── 5. design density (advisory — never blocks) ──────────────────────"
python3 "$REFS/tikz-design-linter.py" "$base.tex" 2>/dev/null | tail -6 | sed 's/^/   /'

echo "─────────────────────────────────────────────────────────────────────"
if [ "$hard" -eq 0 ]; then
  echo "✅ CLEAN — no HARD issues. (Still EYEBALL $base.lint.png — checkers are a floor, not a ceiling.)"
  exit 0
else
  echo "❌ HARD issues above — fix, then re-run. Open $base.lint.png to locate them."
  exit 1
fi
