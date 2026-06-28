---
tags:
  - security
  - vcf
  - vmware
---
# VMware Cloud Foundation — Encryption
![VMware Cloud Foundation — Encryption](../../../../assets/virtualization-vmware-vmware-cloud-foundation-security-encry.svg)





```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "VMware Cloud Foundation Core" {shape: hexagon}

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

- [VCF — Hardening](hardening/)
- [VCF — Health Checks](../operations/health-checks/)
