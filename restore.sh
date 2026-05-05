#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"
BACKUP_ROOT="$ROOT_DIR/backup"

if [ ! -d "$BACKUP_ROOT" ]; then
  echo "No backup directory found."
  exit 1
fi

if [ "${1:-}" = "" ]; then
  echo "Available backups:"
  ls -1 "$BACKUP_ROOT" | sort -r
  echo
  echo "Usage:"
  echo "./restore.sh YYYY-MM-DD_HHMMSS"
  echo
  echo "Example:"
  latest="$(ls -1 "$BACKUP_ROOT" | sort -r | head -n 1 || true)"
  if [ "$latest" != "" ]; then
    echo "./restore.sh $latest"
  fi
  exit 0
fi

BACKUP_NAME="$1"
SRC="$BACKUP_ROOT/$BACKUP_NAME"

if [ ! -d "$SRC" ]; then
  echo "Backup not found: $SRC"
  exit 1
fi

echo
echo "Emergency restore requested."
echo "Source backup:"
echo "$SRC"
echo
echo "Project root:"
echo "$ROOT_DIR"
echo
echo "This will replace current project files with the selected backup."
echo "A pre-restore safety backup will be created first."
echo
printf "Type YES to continue: "
read -r CONFIRM

if [ "$CONFIRM" != "YES" ]; then
  echo "Restore cancelled."
  exit 0
fi

SAFETY="$BACKUP_ROOT/pre-restore_$(date +"%Y-%m-%d_%H%M%S")"
mkdir -p "$SAFETY"

rsync -a \
  --exclude "backup/" \
  --exclude ".venv/" \
  --exclude "site/" \
  --exclude "__pycache__/" \
  --exclude "*.pyc" \
  --exclude ".DS_Store" \
  "$ROOT_DIR/" "$SAFETY/"

rsync -a --delete \
  --exclude "backup/" \
  --exclude ".venv/" \
  --exclude "site/" \
  --exclude "__pycache__/" \
  --exclude "*.pyc" \
  --exclude ".DS_Store" \
  "$SRC/" "$ROOT_DIR/"

echo
echo "Restore complete."
echo "Pre-restore safety backup saved here:"
echo "$SAFETY"
echo
echo "Run this next:"
echo "mkdocs build --clean --strict"
