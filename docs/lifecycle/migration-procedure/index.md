# System Migration Procedure

## Overview

This procedure defines steps to migrate systems or workloads between platforms, sites, or environments.

## Migration Steps

1. Confirm source system health
2. Prepare destination environment
3. Perform data synchronization
4. Execute cutover
5. Validate services

## Validation Commands

```bash
rsync -av source destination
ping destination-host
systemctl status
```

## Completion Criteria

- Data synchronized
- Services running
- Users confirmed functionality
