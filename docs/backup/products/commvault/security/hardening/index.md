---
tags:
  - commvault
  - security
---
# Commvault — Hardening

<div class="kb-summary">
Hardening reference covering Network Security, Security Hardening Checklist.

*Applies to: Commvault 2024.x*
</div>

```d2
direction: down

network_security: "Network Security" {shape: rectangle}
security_hardening_checklist: "Security Hardening Checklist" {shape: rectangle}

network_security -> security_hardening_checklist: hardens
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Network Security

| Port | Purpose | Restriction |
|---|---|---|
| 8400/TCP | CommServe communication | Restrict to admin management subnets |
| 8403/TCP | MediaAgent data movement | Allow from client subnets to MediaAgent IPs only |
| 443/HTTPS | Command Center web UI | Restrict to admin subnets |

## Security Hardening Checklist

- [ ] RBAC configured — all users assigned to roles via AD groups
- [ ] No shared admin credentials
- [ ] Encryption enabled for all regulated data policies
- [ ] DDB encryption enabled
- [ ] 2FA enabled for Command Center
- [ ] CommServe management ports (8400, 8403) firewall-restricted
- [ ] CyberArk integration active for service account passwords
- [ ] Audit log forwarded to SIEM; alerts configured
- [ ] CommServe OS and SQL Server on supported, patched versions

---

## See also

- [Commvault — Authentication](../authentication/)
- [Commvault — Access Control](../access-control/)
- [Commvault — Encryption](../encryption/)
