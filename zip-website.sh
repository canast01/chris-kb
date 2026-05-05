#!/usr/bin/env bash

set -euo pipefail

# ------------------------------------------------------------
# Chris KB — Full Website Zip Export
# Safe, deterministic, repeatable
# ------------------------------------------------------------

echo "=== RUNNING BACKUP ==="
./backup.sh

echo
echo "=== VALIDATING BUILD ==="
mkdocs build --clean --strict

echo
echo "=== CREATING ZIP EXPORT ==="

TS="$(date +"%Y-%m-%d_%H%M%S")"
OUT="website-export-${TS}.zip"

zip -r "$OUT" . \
  -x "*.git*" \
  -x "*.venv*" \
  -x "backup/*" \
  -x "__pycache__/*" \
  -x "*.pyc" \
  -x ".DS_Store" \
  -x "site/*"

echo
echo "=== EXPORT COMPLETE ==="
echo "Created: $OUT"
echo "Upload this ZIP file here."

