# CyberArk — Hardening


<div class="kb-summary">
The Digital Vault server must follow the CyberArk-supplied Windows Server hardening baseline and the Vault-specific firewall policy, which permits only the exact ports required by each component; no general internet access or RDP from non-PAW hosts is permitted.
</div>

| Control | Implementation |
|---|---|
| Vault OS hardening | CyberArk-provided Windows hardening GPO; minimal services running |
| Vault firewall policy | CyberArk-defined inbound/outbound rules; deny-all default |
| PVWA TLS | TLS 1.2+ only; valid internal CA certificate |
| Master Policy review | Quarterly review of base policy and platform-specific overrides |
