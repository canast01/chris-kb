#!/usr/bin/env bash
set -euo pipefail

MSG="${1:-Site update}"

echo
echo "=== SAFE CHANGE START ==="

echo
echo "Running backup..."
./backup.sh

echo
echo "Running validation and health check..."
./validate-site.sh

echo
echo "Checking git status..."
git status --short

echo
echo "Staging changes..."
git add .

echo
echo "Committing changes..."
git commit -m "$MSG"

echo
echo "=== SAFE CHANGE COMPLETE ==="
echo "Committed with message: $MSG"
