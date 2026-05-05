# Dell SRDF

## Overview

SRDF (Symmetrix Remote Data Facility) provides synchronous and asynchronous replication between Dell PowerMax or VMAX storage arrays for disaster recovery.

## Daily Checks

- Verify replication link status
- Check pair state
- Confirm synchronization health
- Review alerts and logs

## Health Commands

```bash
symrdf list
symrdf query
symcfg list
symdev show
```

## Failover Procedure

1. Confirm replication state is synchronized
2. Suspend replication if required
3. Promote target devices to read/write
4. Mount storage to recovery hosts
5. Validate application services

## Failback Procedure

1. Re-establish replication session
2. Resynchronize data
3. Validate storage state
4. Restore normal production access
