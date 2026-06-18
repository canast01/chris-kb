#!/usr/bin/env python3
"""
Free up disk space by pruning old backup snapshots and the MkDocs cache.

Policy:
  - Backup snapshots: keep the KEEP_MIN most recent; delete oldest until
    total backup size is under BACKUP_THRESHOLD_GB.
  - MkDocs .cache: delete entirely if over CACHE_THRESHOLD_MB.

Usage:
    python3 scripts/cleanup_space.py           # dry-run (show what would be removed)
    python3 scripts/cleanup_space.py --write   # apply deletions

Thresholds (edit below or pass as env vars):
    BACKUP_THRESHOLD_GB  default 10   — start pruning above this total size
    CACHE_THRESHOLD_MB   default 500  — wipe cache above this size
    KEEP_MIN             default 3    — always keep at least this many snapshots
"""

import os, sys, shutil, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(REPO, 'backup')
CACHE_DIR = os.path.join(REPO, '.cache')

BACKUP_THRESHOLD_GB = float(os.getenv('BACKUP_THRESHOLD_GB', '10'))
CACHE_THRESHOLD_MB = float(os.getenv('CACHE_THRESHOLD_MB', '500'))
KEEP_MIN = int(os.getenv('KEEP_MIN', '3'))

WRITE = '--write' in sys.argv
DRY = not WRITE

GB = 1024 ** 3
MB = 1024 ** 2


def dir_size_gb(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total / GB


def dir_size_mb(path):
    return dir_size_gb(path) * 1024


def fmt(gb):
    return f'{gb:.1f} GB' if gb >= 1 else f'{gb*1024:.0f} MB'


def cleanup_backups():
    if not os.path.isdir(BACKUP_DIR):
        print('No backup/ directory found.')
        return

    # Snapshots sorted oldest → newest (name is YYYY-MM-DD_HHMMSS)
    snapshots = sorted(
        d for d in os.listdir(BACKUP_DIR)
        if re.match(r'\d{4}-\d{2}-\d{2}_\d{6}$', d)
        and os.path.isdir(os.path.join(BACKUP_DIR, d))
    )

    total_gb = dir_size_gb(BACKUP_DIR)
    print(f'Backup directory: {fmt(total_gb)} across {len(snapshots)} snapshots '
          f'(threshold: {BACKUP_THRESHOLD_GB} GB, keep min: {KEEP_MIN})')

    if total_gb <= BACKUP_THRESHOLD_GB:
        print(f'  → Under threshold, nothing to prune.')
        return

    # Delete oldest snapshots until under threshold (but keep KEEP_MIN)
    deleted = 0
    for snap in snapshots:
        if len(snapshots) - deleted <= KEEP_MIN:
            print(f'  → Reached KEEP_MIN ({KEEP_MIN}), stopping.')
            break
        snap_path = os.path.join(BACKUP_DIR, snap)
        snap_gb = dir_size_gb(snap_path)
        if DRY:
            print(f'  DRY  would delete {snap} ({fmt(snap_gb)})')
        else:
            shutil.rmtree(snap_path)
            print(f'  DEL  {snap} ({fmt(snap_gb)})')
        total_gb -= snap_gb
        deleted += 1
        if total_gb <= BACKUP_THRESHOLD_GB:
            print(f'  → Now at {fmt(total_gb)}, under threshold.')
            break

    remaining = len(snapshots) - deleted
    print(f'  Snapshots remaining: {remaining}')


def cleanup_cache():
    if not os.path.isdir(CACHE_DIR):
        print('No .cache/ directory found.')
        return

    cache_mb = dir_size_mb(CACHE_DIR)
    print(f'.cache directory: {cache_mb:.0f} MB (threshold: {CACHE_THRESHOLD_MB} MB)')

    if cache_mb <= CACHE_THRESHOLD_MB:
        print(f'  → Under threshold, nothing to clear.')
        return

    if DRY:
        print(f'  DRY  would delete .cache/ ({cache_mb:.0f} MB)')
    else:
        shutil.rmtree(CACHE_DIR)
        os.makedirs(CACHE_DIR)
        print(f'  DEL  .cache/ cleared ({cache_mb:.0f} MB freed)')


def main():
    mode = 'DRY RUN' if DRY else 'WRITE'
    print(f'=== cleanup_space.py [{mode}] ===\n')

    cleanup_backups()
    print()
    cleanup_cache()

    if DRY:
        print('\nRe-run with --write to apply.')


if __name__ == '__main__':
    main()
