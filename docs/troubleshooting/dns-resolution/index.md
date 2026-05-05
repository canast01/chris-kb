# DNS Resolution Failures

## Overview

DNS failures prevent applications, servers, and services from locating required resources.

## Symptoms

- Unable to resolve hostname
- Application connection errors
- Service startup failures

## Health Commands

```bash
nslookup hostname
dig hostname
ipconfig /flushdns
```

## Troubleshooting Workflow

1. Confirm DNS server configuration
2. Validate network connectivity
3. Check DNS records
4. Restart DNS service if required
5. Test resolution again
