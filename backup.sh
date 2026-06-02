#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"
BACKUP_ROOT="$ROOT_DIR/backup"
STAMP="$(date +"%Y-%m-%d_%H%M%S")"
READABLE_TIME="$(date +"%Y-%m-%d %I:%M:%S %p %Z")"
DEST="$BACKUP_ROOT/$STAMP"

mkdir -p "$DEST"

rsync -a \
  --exclude "backup/" \
  --exclude ".venv/" \
  --exclude "site/" \
  --exclude "__pycache__/" \
  --exclude "*.pyc" \
  --exclude ".DS_Store" \
  "$ROOT_DIR/" "$DEST/"

cat > "$DEST/backup-info.txt" <<INFO
Backup created: $READABLE_TIME
Source: $ROOT_DIR
Destination: $DEST
Mode: Full project backup
Included: project files, hidden files, .git, docs, scripts, configs, assets
Excluded: backup, .venv, site, __pycache__, *.pyc, .DS_Store
INFO

echo "Backup created: $DEST"

# Remove backups older than 10 days
find "$BACKUP_ROOT" -maxdepth 1 -type d -name "????-??-??_*" -mtime +10 -exec rm -rf {} +
