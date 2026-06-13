---
tags:
  - dell
  - security
---
# RecoverPoint — Authentication


<div class="kb-summary">
Authentication reference covering API Token Management.
</div>

```text
┌──────────────────────────────────── RecoverPoint — Authentication ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             RecoverPoint — Authentication Methods                             │   │
│   │         RPA admin / monitor roles; LDAP integration; certificate-based inter-RPA auth         │   │
│   │                 Management UI: HTTPS on 443 (mgmt HTTPS) — browser-based login                │   │
│   │               API: bearer token or service account; rotate credentials quarterly              │   │
│   │                 Inter-component: certificate-based mutual TLS between engines                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Human Access                 │  │                Machine Access               │   │
│   │            AD / LDAP integration             │  │               Service account               │   │
│   │              SAML SSO optional               │  │               API key / token               │   │
│   │                 MFA via IdP                  │  │               Certificate auth              │   │
│   │            Session timeout 15 min            │  │              Rotate every 90 d              │   │
│   │              Audit login events              │  │             Vault-stored secrets            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites           │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication          │
│  Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA                  │
│  Journal       = write-order-consistent storage capturing all writes for point-in-time access         │
│  Consistency Group= set of volumes protected together; writes are applied in order across all         │
│  Bookmark      = named marker in journal; enables deterministic recovery to a known state             │
│  Image Access  = mounting a journal point-in-time image to a host for testing or recovery             │
│  Failover      = activating the replica at the recovery site; breaks replication relationship         │
│  Test Copy     = non-disruptive image access for validation without breaking replication              │
│  RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero          │
│  RTO           = Recovery Time Objective; time from failover to service restored                      │
│  Reverse       = after failover, replicates from recovery site back to re-sync production             │
│  Splitter Lag  = delay between host write and journal commit; monitor for replication health          │
│  CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps          │
│  Distributed CG= consistency group spanning volumes on multiple storage arrays                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Forward to SIEM via syslog: Management Console → System Settings → Syslog Notifications. Alert on:
- Any admin account login outside business hours
- `enable_image_access` events (indicates failover test or actual DR)
- User account creation or role changes
