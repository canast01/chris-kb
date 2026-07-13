---
tags:
  - dell
  - security
description: "SRDF/A encryption: in-flight data encryption over FCIP using GigE Encryption Module (GEM), certificate management, and encryption status verification..."
---
# SRDF/A — Encryption

<div class="kb-summary">
SRDF/A encryption: in-flight data encryption over FCIP using GigE Encryption Module (GEM), certificate management, and encryption status verification commands.

*Applies to: SRDF/A*
</div>
![SRDF/A — Encryption](../../../../../assets/storage-dell-srdf-a-security-encryption.svg)

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Notes

- SRDF/E applies to data transmitted over FCIP links; dark fibre (native FC) does not traverse the WAN and does not require SRDF/E, though physical security of the fibre path should be assured.
- Enabling encryption on a live SRDF group requires no downtime but may briefly increase CPU overhead on the SRDF directors.
- Verify encryption status after any firmware upgrade or RDF group reconfiguration.

---

## See also

- [Srdf A — Hardening](../hardening/)
- [Srdf A — Authentication](../authentication/)
- [Srdf A — Access Control](../access-control/)
