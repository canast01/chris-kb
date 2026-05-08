# CyberArk — Encryption

Session recordings are encrypted at rest using AES-256. Vault audit log integrity is protected by the Vault's internal signing mechanism. PVWA enforces TLS 1.2 minimum for all connections.

| Control | Implementation |
|---|---|
| Session recording encryption | AES-256 at rest on PSM recording storage |
| Audit log integrity | Vault internal log signing; tamper detection on export |
| PVWA TLS | TLS 1.2+ only; valid internal CA certificate |
