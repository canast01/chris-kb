# Upgrade Readiness Checklist

## Overview

This checklist validates that infrastructure is ready for a safe upgrade before changes begin.

## Pre-Upgrade Checks

- Confirm maintenance window approval
- Verify backups completed successfully
- Confirm rollback plan documented
- Validate monitoring coverage
- Confirm vendor compatibility matrix

## Validation Commands

```bash
df -h
uptime
ping gateway
systemctl --failed
```

## Go / No-Go Criteria

- All health checks passing
- Backup verified
- Support contacts available
- Change approved
