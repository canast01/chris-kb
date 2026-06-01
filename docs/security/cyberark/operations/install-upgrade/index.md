# CyberArk Lifecycle


<div class="kb-summary">
CyberArk follows a structured upgrade sequence to preserve Vault integrity: the Digital Vault is upgraded first, followed by CPM, then PSM, then PVWA; upgrading out of order is unsupported and may result in component incompatibility.
</div>

 The DR Vault must also be upgraded and its replication link verified after each major upgrade. CyberArk supports a rolling EOL model where each major version receives 5 years of support, with extended support available under a separate agreement.

| Version (example) | GA Date | End of Support | Notes |
|---|---|---|---|
| CyberArk PAM 14.x | 2024 | ~2029 | Current major release |
| CyberArk PAM 13.x | 2023 | ~2028 | Still supported |
| CyberArk PAM 12.x | 2022 | ~2027 | Extended support tier |
| Legacy CPM/PSM v10 | 2018 | EOL | Upgrade required |

**Upgrade sequence:** Vault → DR Vault → CPM → PSM → PVWA → PSMP

**Pre-upgrade checklist:**
- Full Vault backup (via Vault backup utility) and DR sync confirmation
- Snapshot all Windows VMs hosting PAM components
- Review CyberArk release notes for breaking changes
- Verify licence count covers current account inventory
