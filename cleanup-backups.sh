#!/usr/bin/env bash
set -euo pipefail

KEEP="${1:-10}"
BACKUP_DIR="backup"

echo
echo "=== BACKUP CLEANUP ==="
echo "Keeping latest $KEEP backups."

if [ ! -d "$BACKUP_DIR" ]; then
  echo "No backup directory found."
  exit 0
fi

mapfile -t backups < <(find "$BACKUP_DIR" -maxdepth 1 -mindepth 1 -type d | sort)

count="${#backups[@]}"

if [ "$count" -le "$KEEP" ]; then
  echo "Backup count is $count. Nothing to remove."
  exit 0
fi

remove_count=$((count - KEEP))

echo "Found $count backups."
echo "Removing oldest $remove_count backups..."

for old_backup in "${backups[@]:0:$remove_count}"; do
  echo "Removing: $old_backup"
  rm -rf "$old_backup"
done

echo
echo "Backup cleanup complete."
echo "Remaining backups:"
find "$BACKUP_DIR" -maxdepth 1 -mindepth 1 -type d | sort
