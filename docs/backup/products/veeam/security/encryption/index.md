---
tags:
  - security
  - veeam
description: "Veeam encryption: backup job-level encryption, encryption key management in the Veeam console, tape encryption, and password rotation procedures."
---
# Veeam — Encryption

<div class="kb-summary">
Veeam encryption: backup job-level encryption, encryption key management in the Veeam console, tape encryption, and password rotation procedures.

*Applies to: Veeam 12.x*
</div>

```d2
direction: down

immutable_repository_configuration: "Immutable Repository Configuration" {shape: rectangle}

```

## Immutable Repository Configuration

### S3 Object Lock (SOBR Capacity Tier)

Configure Object Lock in `Compliance` mode:
- VBR console → SOBR → Capacity Tier → Enable immutability
- Set immutability period = retention period + 10 days buffer
- Compliance mode: even bucket owner cannot delete during immutability period

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Veeam — Hardening](../hardening/)
- [Veeam — Authentication](../authentication/)
- [Veeam — Access Control](../access-control/)
