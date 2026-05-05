#!/usr/bin/env bash
set -e

OUT="site-audit-report.txt"

{
  echo "== Chris KB Site Audit =="
  echo "Generated: $(date '+%Y-%m-%d %I:%M:%S %p %Z')"
  echo

  echo "== Page count =="
  find docs -name "*.md" | wc -l | tr -d ' '
  echo
  echo

  echo "== Pages by section =="
  for d in docs/*; do
    if [ -d "$d" ] && [ "$(basename "$d")" != "assets" ]; then
      count="$(find "$d" -name "*.md" | wc -l | tr -d ' ')"
      echo "$(basename "$d"): $count"
    fi
  done
  echo

  echo "== Site checks =="
  python3 scripts/check-site.py
  echo

  echo "== Strict build =="
  mkdocs build --clean --strict

} > "$OUT" 2>&1

cat "$OUT"
