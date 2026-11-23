#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"
BACKUP_ROOT="$ROOT_DIR/backup"
STAMP="$(date +"%Y-%m-%d_%H%M%S")"
READABLE_TIME="$(date +"%Y-%m-%d %I:%M:%S %p %Z")"
DEST="$BACKUP_ROOT/$STAMP"

# Incremental snapshots: unchanged files are hard-linked to the previous
# backup instead of copied, so each backup is a full browsable tree but
# takes seconds and ~no extra disk (was ~8 min / 2.4 GB per commit).
PREV="$(ls -1d "$BACKUP_ROOT"/????-??-??_* 2>/dev/null | sort | tail -n 1 || true)"
LINK_DEST=()
if [ -n "$PREV" ] && [ -d "$PREV" ]; then
  LINK_DEST=(--link-dest "$PREV")
fi

mkdir -p "$DEST"

rsync -a ${LINK_DEST[@]+"${LINK_DEST[@]}"} \
  --exclude "/backup/" \
  --exclude ".venv/" \
  --exclude "site/" \
  --exclude "__pycache__/" \
  --exclude "*.pyc" \
  --exclude ".DS_Store" \
  --exclude "/.git/sg-inflight-*" \
  "$ROOT_DIR/" "$DEST/"

cat > "$DEST/backup-info.txt" <<INFO
Backup created: $READABLE_TIME
Source: $ROOT_DIR
Destination: $DEST
Mode: Full project snapshot (incremental, hard-linked to previous)
Included: project files, hidden files, .git, docs, scripts, configs, assets
Excluded: backup, .venv, site, __pycache__, *.pyc, .DS_Store
INFO

echo "Backup created: $DEST"

# Keep only the 5 most recent backups; delete the rest
KEEP=5
BACKUP_COUNT=$(ls -1d "$BACKUP_ROOT"/????-??-??_* 2>/dev/null | wc -l | tr -d ' ')
if [ "$BACKUP_COUNT" -gt "$KEEP" ]; then
  DELETE_COUNT=$((BACKUP_COUNT - KEEP))
  ls -1d "$BACKUP_ROOT"/????-??-??_* 2>/dev/null | sort | head -n "$DELETE_COUNT" | while IFS= read -r old; do
    rm -rf "$old"
  done
fi
