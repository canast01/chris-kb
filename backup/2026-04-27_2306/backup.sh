#!/usr/bin/env bash

set -e

BACKUP_ROOT="backup"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M")
DEST="$BACKUP_ROOT/$TIMESTAMP"

echo "Creating backup..."

mkdir -p "$DEST"

rsync -a \
  --exclude ".git" \
  --exclude ".venv" \
  --exclude "backup" \
  ./ "$DEST"

echo
echo "Backup created:"
echo "$DEST"
echo
