# NetBackup

## Overview

NetBackup provides enterprise backup and recovery for servers, databases, virtual machines, and large-scale production environments.

## Daily Checks

- Review failed jobs
- Check storage unit capacity
- Confirm catalog backup status
- Validate media server health
- Review policy schedules

## Health Commands

```bash
bpdbjobs
bppllist
bpstulist
nbemmcmd -listhosts
bperror -backstat -hoursago 24
```

## Upgrade Workflow

1. Confirm master and media server compatibility
2. Back up catalog
3. Upgrade master server first
4. Upgrade media servers and clients
5. Validate backup and restore jobs
