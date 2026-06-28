---
tags:
  - netbackup
  - security
---
# NetBackup — Access Control

<div class="kb-summary">
Access Control reference covering NetBackup Access Control (NBAC).

*Applies to: NetBackup 10.x*
</div>

```d2
direction: down

auth: "NetBackup\nAuthentication" {shape: rectangle}
administrator: "Administrator" {shape: rectangle}
operator: "Operator" {shape: rectangle}
auditor: "Auditor" {shape: rectangle}
readonly: "Read-Only" {shape: rectangle}
resources: Protected Resources {shape: cylinder}

auth -> administrator: grants
administrator -> resources: access
auth -> operator: grants
operator -> resources: access
auth -> auditor: grants
auditor -> resources: access
auth -> readonly: grants
readonly -> resources: access
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Netbackup — Authentication](../authentication/)
- [Netbackup — Hardening](../hardening/)
- [Netbackup — Encryption](../encryption/)
