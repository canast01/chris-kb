# Database Backup Validation

## Overview

This runbook confirms database backups are successful and recoverable.

## Pre-Checks

- Confirm backup job schedule
- Identify backup location
- Verify storage capacity

## Commands

```bash
ls -lh /backup/database
grep backup /var/log/messages
df -h
```

## Validation

1. Confirm backup file exists
2. Perform test restore if required
3. Verify database integrity
