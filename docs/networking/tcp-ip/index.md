# TCP/IP

## Overview

TCP/IP is the core communication model used by servers, storage, cloud services, applications, and infrastructure platforms.

## Daily Checks

- Verify host IP configuration
- Confirm gateway reachability
- Check DNS resolution
- Validate service port connectivity

## Health Commands

```bash
ip addr
ip route
ping 8.8.8.8
traceroute 8.8.8.8
nc -vz server 443
```

## Troubleshooting Workflow

1. Confirm source and destination IPs
2. Verify subnet and gateway
3. Test DNS resolution
4. Test port connectivity
5. Check firewall rules
