---
tags:
  - dell
  - security
---
# SRDF/A — Authentication


<div class="kb-summary">
Authentication reference covering Credential Rotation, Service Account Policy.

*Applies to: SRDF/A*
</div>
![SRDF/A — Authentication](../../../../assets/storage-dell-srdf-a-security-authentication.svg)




Each automation system (monitoring, SRM, runbook scripts) should use a dedicated account scoped to the minimum required RDF groups and roles.

```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "SRDF/A Core" {shape: hexagon}

external -> perimeter_controls: traffic in
perimeter_controls -> identity_access
identity_access -> audit_logging
audit_logging -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Srdf A — Access Control](access-control/)
- [Srdf A — Hardening](hardening/)
- [Srdf A — Encryption](encryption/)
