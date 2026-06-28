---
tags:
  - dell
  - security
---
# SRDF/S — Encryption


<div class="kb-summary">
SRDF/S encryption: in-flight encryption over FCIP using GEM or Brocade encryption, IPsec tunnel configuration, and encryption key lifecycle management.

*Applies to: SRDF/S*
</div>
![SRDF/S — Encryption](../../../../assets/storage-dell-srdf-s-security-encryption.svg)




```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "SRDF/S Core" {shape: hexagon}

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

- [Srdf S — Hardening](hardening/)
- [Srdf S — Authentication](authentication/)
- [Srdf S — Access Control](access-control/)
