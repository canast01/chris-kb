# VMware Aria Operations

## Overview

VMware Aria Operations provides monitoring, performance analytics, and capacity management for VMware environments.

## Daily Checks

- Review active alerts
- Verify cluster health
- Check data collection status
- Confirm dashboards updating

## Health Commands

```bash
service vmware-vcops status
df -h
top
```

## Upgrade Workflow

1. Snapshot appliance before upgrade
2. Verify node health
3. Perform upgrade
4. Validate dashboards and alerts
