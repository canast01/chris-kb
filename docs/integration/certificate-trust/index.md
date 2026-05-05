# Certificate Trust

## Overview

Certificate trust ensures secure communication between systems using trusted certificate authorities.

## Daily Checks

- Verify certificate validity
- Check trust store configuration
- Review certificate expiration alerts

## Health Commands

```bash
openssl verify certificate.pem
openssl x509 -in certificate.pem -text -noout
```

## Troubleshooting Workflow

1. Confirm certificate installed
2. Validate trust chain
3. Restart service
4. Test secure connection
