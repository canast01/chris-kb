# Packet Loss Troubleshooting

## Overview

This runbook diagnoses packet loss affecting application performance.

## Pre-Checks

- Confirm affected application
- Identify network path
- Check recent network changes

## Commands

```bash
ping -c 100 destination-host
mtr destination-host
ethtool interface
```

## Validation

1. Confirm packet loss resolved
2. Confirm latency stabilized
3. Monitor network performance metrics
