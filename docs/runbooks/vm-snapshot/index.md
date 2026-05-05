# VM Snapshot Runbook

## Overview

This runbook defines safe use of VM snapshots before changes.

## Pre-Checks

- Confirm VM owner approval
- Check existing snapshots
- Confirm datastore capacity
- Define snapshot removal time

## Commands

```bash
vim-cmd vmsvc/getallvms
vim-cmd vmsvc/snapshot.get VMID
vim-cmd vmsvc/snapshot.create VMID pre-change '' 0 0
```

## Validation

1. Confirm snapshot created
2. Complete change
3. Remove snapshot after validation
4. Confirm snapshot consolidation is clean
