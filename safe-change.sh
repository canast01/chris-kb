#!/usr/bin/env bash

set -e

echo
echo "Step 1 — Backup"
echo

if [ -f "./backup.sh" ]; then
  ./backup.sh
else
  echo "ERROR: backup.sh not found."
  exit 1
fi

echo
echo "Step 2 — Validate site"
echo

if [ -f "./validate-site.sh" ]; then
  ./validate-site.sh
else
  echo "WARNING: validate-site.sh not found — skipping validation"
fi

echo
echo "Step 3 — Commit changes"
echo

git add .

git commit -m "Auto commit after backup and validation" || true

echo
echo "Done."
echo
