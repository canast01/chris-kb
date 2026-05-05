# Time Synchronization

## Overview

Time synchronization ensures consistent timestamps across infrastructure systems.

## Daily Checks

- Verify NTP service status
- Check time drift
- Confirm time source availability

## Health Commands

```bash
timedatectl status
ntpq -p
chronyc tracking
```

## Troubleshooting Workflow

1. Confirm NTP server reachable
2. Validate time configuration
3. Restart time service
4. Verify synchronization
