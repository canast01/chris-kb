# Firewall Rule Validation

## Overview

This runbook verifies firewall rules allow required traffic.

## Pre-Checks

- Confirm source and destination
- Confirm port and protocol
- Identify firewall device

## Commands

```bash
nc -zv destination-host port
telnet destination-host port
ss -tulnp
```

## Validation

1. Confirm connection allowed
2. Confirm application connectivity restored
3. Document firewall change if required
