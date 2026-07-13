---
tags:
  - security
  - veeam
description: "Access Control reference covering Role-Based Access Control, Audit Log."
---
# Veeam — Access Control

<div class="kb-summary">
Access Control reference covering Role-Based Access Control, Audit Log.

*Applies to: Veeam 12.x*
</div>

Forward to SIEM using a log forwarder (Filebeat, Splunk UF) on the VBR server. Alert on:
- Failed login attempts
- Job deletion or modification outside maintenance windows
- Encryption key management operations

```d2
direction: down

auth: "Veeam\nAuthentication" {shape: rectangle}
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

- [Veeam — Authentication](../authentication/)
- [Veeam — Hardening](../hardening/)
- [Veeam — Encryption](../encryption/)
