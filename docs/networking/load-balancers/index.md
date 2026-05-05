# Load Balancers

## Overview

Load balancers distribute traffic across multiple backend systems. They improve availability, scalability, and maintenance flexibility.

## Daily Checks

- Review pool member health
- Check virtual server status
- Validate certificates
- Confirm persistence settings
- Review error rates

## Health Commands

```bash
curl -vk https://vip.example.com
openssl s_client -connect vip.example.com:443
dig vip.example.com
```

## Troubleshooting Workflow

1. Confirm VIP is reachable
2. Check pool member health
3. Validate backend service ports
4. Review SSL certificate state
5. Check firewall path
