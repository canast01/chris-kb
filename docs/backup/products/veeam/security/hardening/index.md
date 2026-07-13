---
tags:
  - security
  - veeam
description: "Hardening reference covering Network Security, Security Hardening Checklist."
---
# Veeam — Hardening

<div class="kb-summary">
Hardening reference covering Network Security, Security Hardening Checklist.

*Applies to: Veeam 12.x*
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
| 9392/TCP | VBR console communication | Restrict to admin management subnets |
| 2500–3300/TCP | Data transfer (proxy) | Open between proxies and repositories only |
| 443/TCP | vCenter API | VBR to vCenter |
| 6160/TCP | Veeam Installer Service | Between VBR server and managed components |

## Security Hardening Checklist

- [ ] RBAC configured with AD groups — no shared admin logins
- [ ] Encryption enabled on all jobs writing to cloud or off-site targets
- [ ] Linux hardened repository deployed for immutable local backups
- [ ] S3 Object Lock in Compliance mode for cloud capacity tier
- [ ] Encryption keys exported and stored in CyberArk/offline vault
- [ ] VBR console port (9392) restricted to admin subnets via firewall
- [ ] CyberArk integration active for infrastructure credentials
- [ ] Audit log forwarded to SIEM; alerts configured
- [ ] Veeam ONE alert for any backup job failing > 2 consecutive times

---

## See also

- [Veeam — Authentication](../authentication/)
- [Veeam — Access Control](../access-control/)
- [Veeam — Encryption](../encryption/)
