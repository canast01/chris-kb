# TLS and HTTPS

## Overview

TLS secures communication between systems using encryption and certificates. HTTPS is the secure version of HTTP used for web applications and APIs.

## Daily Checks

- Verify certificate expiration dates
- Check cipher and protocol configuration
- Validate secure connections
- Review TLS errors

## Health Commands

```bash
openssl s_client -connect server:443
openssl x509 -in cert.pem -text -noout
curl -v https://example.com
```

## Upgrade Workflow

1. Replace expiring certificates
2. Disable weak protocols
3. Restart affected services
4. Validate secure connectivity
