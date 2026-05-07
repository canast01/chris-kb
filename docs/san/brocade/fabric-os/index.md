# Brocade Fabric OS


## Overview

Brocade Fabric OS is the operating system for Brocade Fibre Channel SAN switches.

## Daily Checks

- Review switch health
- Check port errors
- Validate zoning configuration
- Confirm fabric membership

## Health Commands

```bash
switchshow
fabricshow
porterrshow
zoneshow
```

## Upgrade Workflow

1. Backup switch configuration
2. Verify upgrade path
3. Upgrade redundant fabric first
4. Validate fabric health
