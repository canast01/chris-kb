# Cisco MDS


## Overview

Cisco MDS switches provide Fibre Channel connectivity for SAN environments.

## Daily Checks

- Verify fabric health
- Check port errors
- Confirm zoning configuration

## Health Commands

```bash
show version
show interface brief
show zone
show fabric status
```

## Upgrade Workflow

1. Back up configuration
2. Verify firmware compatibility
3. Upgrade secondary switch first
