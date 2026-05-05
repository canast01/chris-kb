# Certificate Renewal Runbook

## Overview

This runbook covers renewing and validating certificates used by applications and infrastructure services.

## Pre-Checks

- Confirm certificate expiration date
- Identify certificate owner
- Confirm issuing CA
- Confirm services using the certificate

## Commands

```bash
openssl x509 -in cert.pem -text -noout
openssl s_client -connect server:443
curl -vk https://server
```

## Validation

1. Install renewed certificate
2. Restart affected service
3. Validate TLS connection
4. Confirm monitoring alert cleared
