# Public Key Infrastructure (PKI)

## Overview

PKI manages digital certificates used for encryption, authentication, and secure communication across infrastructure, applications, and services.

## Daily Checks

- Verify certificate expiration dates
- Check certificate authority services
- Review certificate revocation list status
- Validate auto-enrollment operations

## Health Commands

```powershell
certutil -viewstore My
certutil -CRL
Get-Service certsvc
```

## Upgrade Workflow

1. Backup certificate authority database
2. Verify certificate templates
3. Apply OS or certificate authority updates
4. Validate certificate issuance and renewal
