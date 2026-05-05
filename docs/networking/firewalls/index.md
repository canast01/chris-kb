# Firewalls

## Overview

Firewalls control traffic between networks using rules, policies, zones, objects, and inspection profiles.

## Daily Checks

- Review blocked traffic logs
- Validate rule hit counts
- Check VPN tunnel health
- Confirm policy changes
- Review expired objects

## Health Commands

```bash
show session all
show running security-policy
show log traffic
show system info
```

## Troubleshooting Workflow

1. Confirm source, destination, port, and protocol
2. Check policy match
3. Review NAT rules
4. Validate route path
5. Review deny logs
