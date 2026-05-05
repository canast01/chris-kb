# VLAN

## Overview

VLANs segment network traffic into logical broadcast domains. They are commonly used to separate management, storage, server, user, backup, and replication networks.

## Daily Checks

- Confirm VLAN exists on required switches
- Verify trunk allowed VLANs
- Check access port assignments
- Validate tagging configuration

## Health Commands

```bash
show vlan brief
show interfaces trunk
show interface status
show running-config interface INTERFACE
```

## Troubleshooting Workflow

1. Confirm VLAN ID
2. Check port mode access or trunk
3. Verify VLAN allowed on trunk
4. Confirm endpoint IP configuration
5. Test connectivity
