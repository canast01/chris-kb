---
tags:
  - security
  - srm
  - vmware
---
# SRM — Encryption


<div class="kb-summary">
Encryption reference covering Encryption at Recovery Site, Certificate Management for SRM Server, SRA Credential Storage Encryption, FIPS Mode.

*Applies to: SRM 8.x / 9.x*
</div>
![SRM — Encryption](../../../../assets/virtualization-vmware-srm-security-encryption.svg)


  TLS Encryption Coverage


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

- [SRM — Hardening](hardening/)
- [SRM — Health Checks](../operations/health-checks/)
