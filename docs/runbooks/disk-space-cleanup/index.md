# Disk Space Cleanup Runbook

## Overview

This runbook helps identify and clean up disk space issues safely.

## Pre-Checks

- Confirm affected filesystem
- Identify largest directories
- Avoid deleting application data without approval

## Commands

```bash
df -h
du -sh /* 2>/dev/null | sort -h
find /var/log -type f -name '*.gz' -mtime +30
journalctl --disk-usage
```

## Validation

1. Confirm free space improved
2. Confirm application still running
3. Document files removed
