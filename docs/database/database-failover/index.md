# Database Failover Procedure

## Overview

This procedure defines steps to promote a standby database during failure.

## Pre-Checks

- Confirm primary database failure
- Verify standby readiness
- Notify application teams

## Commands

```bash
systemctl stop primary-db
systemctl start standby-db
```

## Validation

1. Confirm standby promoted
2. Confirm application connectivity restored
3. Monitor system performance
