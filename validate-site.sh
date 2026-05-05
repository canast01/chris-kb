#!/usr/bin/env bash
set -e

echo "== Strict MkDocs validation =="
mkdocs build --clean --strict

echo
echo "== Site checks =="
python3 scripts/check-site.py

echo
echo "Validation complete."
