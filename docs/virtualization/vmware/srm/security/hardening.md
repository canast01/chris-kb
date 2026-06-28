---
tags:
  - security
  - srm
  - vmware
---
# SRM — Hardening


<div class="kb-summary">
Hardening reference covering Least-Privilege SRA Service Accounts, Rotate SRA Credentials, Test Recovery Plans Regularly, Restrict Who Can Execute Recovery, Secure Recovery Site Network Design and 3 more sections.

*Applies to: SRM 8.x / 9.x*
</div>
![SRM — Hardening](../../../../assets/virtualization-vmware-srm-security-hardening.svg)


  SRM Hardening Controls


```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "Site Recovery Manager Core" {shape: hexagon}

external -> perimeter_controls: traffic in
perimeter_controls -> identity_access
identity_access -> audit_logging
audit_logging -> core: secured path
```

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## See also

- [SRM — Access Control](access-control/)
- [SRM — Authentication](authentication/)
- [SRM — Health Checks](../operations/health-checks/)
