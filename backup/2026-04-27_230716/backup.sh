#!/usr/bin/env bash

set -e

BACKUP_ROOT="backup"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
DEST="$BACKUP_ROOT/$TIMESTAMP"

echo
echo "Creating full project backup..."
echo

mkdir -p "$DEST"

rsync -av \
  --exclude ".git" \
  --exclude ".venv" \
  --exclude "backup" \
  --exclude "__pycache__" \
  --exclude "*.pyc" \
  --exclude ".DS_Store" \
  --exclude "site" \
  ./ "$DEST"

echo
echo "Backup complete:"
echo "$DEST"
echo
