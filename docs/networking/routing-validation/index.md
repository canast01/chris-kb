# Routing Validation

## Overview

This runbook verifies routing paths between network segments.

## Pre-Checks

- Confirm destination network
- Verify routing configuration
- Identify gateway address

## Commands

```bash
ip route show
traceroute destination-network
netstat -rn
```

## Validation

1. Confirm correct routing path
2. Confirm network reachability
3. Document routing changes
