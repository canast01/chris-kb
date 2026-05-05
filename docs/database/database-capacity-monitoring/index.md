# Database Capacity Monitoring

## Overview

This runbook monitors database storage growth and prevents capacity exhaustion.

## Pre-Checks

- Confirm database size
- Identify storage thresholds
- Review growth trends

## Commands

```bash
du -sh /var/lib/mysql
df -h
```

## Validation

1. Confirm storage capacity sufficient
2. Identify growth patterns
3. Plan storage expansion if required
