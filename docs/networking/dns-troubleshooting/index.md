# DNS Troubleshooting Runbook

## Overview

This runbook provides a structured process for diagnosing DNS resolution failures.

## Pre-Checks

- Confirm hostname being queried
- Confirm DNS server configuration
- Verify network connectivity
- Identify recent DNS changes

## Commands

```bash
nslookup hostname
dig hostname
cat /etc/resolv.conf
ping dns-server
```

## Validation

1. Confirm hostname resolves correctly
2. Confirm application connectivity restored
3. Monitor logs for repeated failures
