---
tags:
  - san
  - security
---
# Cisco DCNM — Access Control


<div class="kb-summary">
Access Control reference covering Overview, Built-In Roles, Fabric-Level Scoping, LDAP Group to Role Mapping, Service Account Configuration and 2 more sections.

*Applies to: Cisco MDS · Nexus*
</div>
![Cisco DCNM — Access Control](../../../../assets/san-cisco-cisco-dcnm-security-access-control.svg)




```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "Cisco DCNM Core" {shape: hexagon}

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

- [Cisco Dcnm — Authentication](authentication/)
- [Cisco Dcnm — Hardening](hardening/)
- [Cisco Dcnm — Encryption](encryption/)
