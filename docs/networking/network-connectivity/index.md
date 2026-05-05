# Network Connectivity Troubleshooting

## Overview

This runbook identifies and resolves network connectivity issues between systems.

## Pre-Checks

- Confirm source and destination systems
- Verify IP addresses
- Confirm routing configuration
- Check firewall policies

## Commands

```bash
ping destination-host
traceroute destination-host
ip route
netstat -rn
```

## Validation

1. Confirm connectivity restored
2. Confirm application communication functioning
3. Document root cause
