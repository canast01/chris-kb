# Database Replication Check

## Overview

This runbook verifies replication status between primary and secondary database nodes.

## Pre-Checks

- Identify replication topology
- Confirm network connectivity
- Review replication configuration

## Commands

```bash
mysql -e 'SHOW SLAVE STATUS\G'
psql -c 'SELECT * FROM pg_stat_replication;'
```

## Validation

1. Confirm replication active
2. Confirm replication lag within limits
3. Verify data consistency
