#!/usr/bin/env bash

set -e

echo
echo "Validating Chris KB..."
echo

echo "1) Checking backup folder..."
if [ -d "backup" ]; then
  echo "OK: backup folder exists"
else
  echo "WARNING: backup folder does not exist"
fi

echo
echo "2) Checking key files..."
for f in mkdocs.yml docs/index.md backup.sh; do
  if [ -f "$f" ]; then
    echo "OK: $f"
  else
    echo "MISSING: $f"
  fi
done

echo
echo "3) Building site..."
mkdocs build --clean --strict

echo
echo "4) Current docs structure:"
find docs -maxdepth 3 -type f -name "index.md" | sort

echo
echo "Validation complete."
echo
