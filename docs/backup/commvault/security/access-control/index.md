---
tags:
  - commvault
  - security
---
# Commvault — Access Control


<div class="kb-summary">
Commvault access control: RBAC role assignment, user group scoping, audit trail configuration, and MFA enforcement for CommCell Console and Web Console.

*Applies to: Commvault 2024.x*
</div>
![Commvault — Access Control](../../../../assets/backup-commvault-security-access-control-index.svg)




Forward audit logs to SIEM via syslog:
- Command Center: Manage → Alerts → configure syslog destination
- Alert on: admin account creation, policy modifications, job deletion, encryption key access

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Commvault — Authentication](../authentication/)
- [Commvault — Hardening](../hardening/)
- [Commvault — Encryption](../encryption/)
