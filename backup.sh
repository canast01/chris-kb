#!/usr/bin/env bash

set -e

BACKUP_ROOT="backup"

# Folder-safe timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")

# Human-readable timestamp
READABLE_TIME=$(date +"%Y-%m-%d %I:%M:%S %p %Z")

DEST="$BACKUP_ROOT/$TIMESTAMP"

echo
echo "Creating full project backup..."
echo "Time: $READABLE_TIME"
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

# Write metadata file
cat > "$DEST/backup-info.txt" << INFO
Backup created: $READABLE_TIME
Source directory: $(pwd)
Hostname: $(hostname)
User: $(whoami)
INFO

echo
echo "Backup complete:"
echo "$DEST"
echo
