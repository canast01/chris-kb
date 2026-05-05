# VPN

## Overview

VPNs provide encrypted connectivity between users, sites, cloud environments, and partner networks.

## Daily Checks

- Confirm tunnel status
- Review authentication failures
- Check encryption settings
- Validate route advertisements
- Review certificate expiration

## Health Commands

```bash
show vpn-sessiondb
show crypto ikev2 sa
show crypto ipsec sa
ping remote-subnet-ip
```

## Troubleshooting Workflow

1. Confirm peer IP reachability
2. Validate Phase 1 settings
3. Validate Phase 2 settings
4. Check routes and ACLs
5. Review tunnel logs
