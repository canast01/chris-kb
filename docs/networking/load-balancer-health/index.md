# Load Balancer Health Check

## Overview

This runbook validates load balancer health and backend availability.

## Pre-Checks

- Confirm load balancer IP or hostname
- Identify backend servers
- Confirm service port

## Commands

```bash
curl -I http://load-balancer
curl http://backend-server
netstat -tulnp
```

## Validation

1. Confirm backend servers responding
2. Confirm load balancer distributing traffic
3. Monitor application response time
