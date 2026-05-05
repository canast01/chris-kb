# Storage Volume Expansion Runbook

## Overview

This runbook provides a controlled process for expanding storage volumes.

## Pre-Checks

- Confirm requested size
- Validate pool capacity
- Confirm host multipathing
- Confirm filesystem expansion plan

## Commands

```bash
df -h
lsblk
multipath -ll
```

## Validation

1. Expand storage volume
2. Rescan host storage
3. Expand filesystem
4. Confirm application sees new capacity
