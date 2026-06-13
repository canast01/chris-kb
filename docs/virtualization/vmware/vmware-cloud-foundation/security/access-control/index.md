---
tags:
  - security
  - vcf
  - vmware
---
# VMware Cloud Foundation — Access Control

```text
┌────────────────────────────── VMware Cloud Foundation — Access Control ───────────────────────────────┐
│                                                                                                       │
│  VCF access control spans SDDC Manager (admin/operator/viewer roles), vCenter RBAC                    │
│  per domain, NSX RBAC, and credential management for all service accounts.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              SDDC Manager Roles              │  │               Per-Domain RBAC               │   │
│   │             Admin: full control              │  │           Each domain: own vCenter          │   │
│   │       Operator: manage but not config        │  │             AD groups per domain            │   │
│   │         Viewer: read-only dashboard          │  │            NSX: per-domain roles            │   │
│   │           SSO: AD-integrated login           │  │            No cross-domain access           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager roles control VCF platform ops; domain RBAC controls workload access.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Credential Management             │  │              Audit & Compliance             │   │
│   │          SDDC Mgr: rotate passwords          │  │           Log: all SDDC Mgr events          │   │
│   │          Service accounts: managed           │  │           Review admin list qtrly           │   │
│   │         Break-glass: local SSO admin         │  │           Alert: failed login SIEM          │   │
│   │         Vault integration: optional          │  │           SDDC Mgr audit log: API           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SDDC Manager runs on management domain; AD must be reachable on management network                   │
│  for identity-based login; all SDDC Mgr operations are logged.                                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager Admin= full platform control; assign to minimal staff                                   │
│  Operator role= manage domains/clusters; cannot change VCF config                                     │
│  Viewer role   = read-only; safe for monitoring teams                                                 │
│  AD integration= SDDC Mgr authenticates against AD via LDAP                                           │
│  Break-glass   = local admin account; used when AD is unreachable                                     │
│  Credential rotation= SDDC Mgr rotates service account passwords automatically                        │
│  Vault integration= optional HashiCorp Vault for credential storage                                   │
│  SIEM          = receives SDDC Mgr syslog and vCenter events                                          │
│  Audit API     = SDDC Mgr REST API /v1/audit-events endpoint                                          │
│  Quarterly review= verify admin role assignments across all domains                                   │
│  No cross-domain= workload domain RBAC is isolated per domain                                         │
│  Service accounts= SDDC Mgr manages all component service credentials                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  SDDC Manager → Security → Credentials → Rotate                                                       │
│  ESXi root · vCenter SSO admin · NSX admin                                                            │
│  SDDC Manager admin · vSAN iSCSI accounts                                                             │
│  Schedule: every 90 days (or per policy)                                                              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

