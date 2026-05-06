# CyberArk Security

The Digital Vault server must follow the CyberArk-supplied Windows Server hardening baseline and the Vault-specific firewall policy, which permits only the exact ports required by each component; no general internet access or RDP from non-PAW hosts is permitted. PVWA is accessible over HTTPS only (TLS 1.2 minimum, TLS 1.3 preferred), and all production safes enforce dual-control to prevent unilateral credential access. Session recordings are encrypted at rest using AES-256, and Vault audit log integrity is protected by the Vault's internal signing mechanism.

| Control | Implementation |
|---|---|
| Vault OS hardening | CyberArk-provided Windows hardening GPO; minimal services running |
| Vault firewall policy | CyberArk-defined inbound/outbound rules; deny-all default |
| PVWA TLS | TLS 1.2+ only; valid internal CA certificate |
| Dual-control for PROD | Enforced via Master Policy; requires approver in PVWA before retrieval |
| Session recording encryption | AES-256 at rest on PSM recording storage |
| Audit log integrity | Vault internal log signing; tamper detection on export |
| Master Policy review | Quarterly review of base policy and platform-specific overrides |
| Break-glass account | Emergency Vault Admin account in sealed safe; access via dual-control + incident ticket |
| Vault DR access | DR Vault is read-only replica; promotion only during declared disaster |
