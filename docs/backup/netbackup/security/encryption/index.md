---
tags:
  - netbackup
  - security
---
# NetBackup — Encryption

<div class="kb-summary">
NetBackup encryption: KMS server configuration, backup data encryption policy settings, client-side encryption, and encryption key lifecycle management.

*Applies to: NetBackup 10.x*
</div>

| Encryption Mode | Location | CPU Impact |
|---|---|---|
| Client-side | Client host | High (on production server) |
| Media server-side | Media server | Low (off client) |
| Storage-level | Array/appliance | None (hardware) |

Mandate client-side or media-server-side encryption for all policies covering PII or regulated data.

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

- [Netbackup — Hardening](../hardening/)
- [Netbackup — Authentication](../authentication/)
- [Netbackup — Access Control](../access-control/)
