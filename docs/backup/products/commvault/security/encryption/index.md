---
tags:
  - commvault
  - security
description: "Encryption reference covering Backup Encryption, Linux Hardened Repository (Immutable Backups)."
---
# Commvault — Encryption

<div class="kb-summary">
Encryption reference covering Backup Encryption, Linux Hardened Repository (Immutable Backups).

*Applies to: Commvault 2024.x*
</div>

Configure via VBR Repository settings: enable "Immutable" with retention period matching recovery requirements.

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Commvault — Hardening](../hardening/)
- [Commvault — Authentication](../authentication/)
- [Commvault — Access Control](../access-control/)
