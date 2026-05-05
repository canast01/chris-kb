# Database Health Check

## Overview

This runbook verifies database availability, performance, and connectivity.

## Pre-Checks

- Confirm database instance name
- Identify application dependencies
- Check recent alerts

## Commands

```bash
systemctl status mysqld
ps aux | grep postgres
netstat -tulnp | grep 5432
```

## Validation

1. Confirm database service running
2. Confirm client connectivity
3. Review database logs
