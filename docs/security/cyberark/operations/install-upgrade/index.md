---
tags:
  - operations
  - security
---
# CyberArk Lifecycle

<div class="kb-summary">
CyberArk follows a structured upgrade sequence to preserve Vault integrity: the Digital Vault is upgraded first, followed by CPM, then PSM, then PVWA; upgrading out of order is unsupported and may result in component incompatibility.

*Applies to: CyberArk PAM*
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

```d2
direction: right

plan: "Plan" {shape: oval}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> verify
verify -> validate
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [CyberArk — Procedures](../procedures/)
- [CyberArk — Health Checks](../health-checks/)
- [CyberArk — CLI Reference](../cli-reference/)
- [CyberArk — Scripts](../scripts/)
- [CyberArk — Backup and Restore](../backup-restore/)
- [CyberArk — Common Issues](../../troubleshooting/common-issues/)
