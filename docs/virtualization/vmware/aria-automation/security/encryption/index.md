# Aria Automation — Encryption

## Secrets and Encrypted Properties

- Use **Encrypted Property Groups** for sensitive values (passwords, API tokens) in blueprints — values are stored encrypted and not exposed in deployment event logs
- For enterprise-grade secrets management, integrate with **HashiCorp Vault** — Aria Automation retrieves secrets at deployment time via Vault's API
- Avoid embedding plaintext secrets in Cloud Templates — use property binding or Vault references

## TLS Certificate Management

- Aria Automation ships with self-signed certificates — replace with CA-signed certificates before production use
- Replace certificates via Aria Suite Lifecycle Manager (Locker) or via `vracli certificate import` on the appliance
- Certificate renewals should be tracked in the LCM Locker and scheduled before expiry
