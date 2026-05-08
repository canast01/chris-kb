# Aria Operations — Encryption

## TLS Certificate Replacement

Aria Operations ships with a self-signed certificate. Replace with a CA-signed certificate for production.

**Via UI:**

```
Administration > Certificates > Replace Certificate
```

Upload:
- Certificate (PEM)
- Private key (PEM, no passphrase)
- CA chain / intermediate (PEM)
