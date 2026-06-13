---
tags:
  - security
  - veeam
---
# Veeam — Hardening


<div class="kb-summary">
Hardening reference covering Network Security, Security Hardening Checklist.

*Applies to: Veeam 12.x*
</div>

```text
┌────────────────────────────────────────── Veeam — Hardening ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Veeam — Hardening Checklist                                  │   │
│   │               [ ] Disable default/admin accounts; create named admin accounts only            │   │
│   │                   [ ] Enable MFA for all interactive logins via IdP / SAML SSO                │   │
│   │       [ ] Restrict management port (9419 (Veeam REST API)) to jump host / management VLAN     │   │
│   │               [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)            │   │
│   │                 [ ] Apply all security patches within 30 days of vendor release               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Network Hardening                                       │   │
│   │               [ ] Separate backup VLAN — no direct production host access to repo             │   │
│   │       [ ] Firewall: allow only 9419 (Veeam REST API) · 6160 (Veeam Agent) · 443 (vCenter)     │   │
│   │                  [ ] Disable unused ports and protocols on management interface               │   │
│   │              [ ] Immutable repository: enable WORM or object lock on backup target            │   │
│   │                 [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Backup Server = central Veeam component: scheduler, job engine, catalog, REST API                    │
│  Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H       │
│  CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors          │
│  VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup                 │
│  SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage        │
│  Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds                   │
│  SureBackup    = automated backup verification; test-restores VM in isolated virtual lab              │
│  Replication   = creates VM replica at DR site; enables failover without full restore time            │
│  GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points      │
│  Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec       │
│  Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery           │
│  VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required                    │
│  Health Check  = periodic backup integrity scan; verifies restore points are readable                 │
│  Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
