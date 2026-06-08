# Site Recovery Manager — Security

<div class="kb-summary">
SRM hardening — RBAC configuration, certificate management, vSphere Replication security, and audit logging.
</div>

```text
┌─────────────────────────────────────────── SRM — Security ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         vCenter SSO for SRM authentication; site pair credentials for cross-site trust        │   │
│   │      RBAC roles: admin / recovery execute / test operator / read-only for least privilege     │   │
│   │     Certificate management for SRM servers; array replication auth; audit log for all ops     │   │
│   │       Replication traffic encrypted with TLS; vSAN encryption at rest for DR datastores       │   │
│   │       Test isolation network prevents recovery test VMs from reaching production systems      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication controls SRM access · RBAC scopes recovery roles                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │       vCenter SSO auth      │  │       SRM admin: full       │  │          Replic TLS         │   │
│   │        AD integration       │  │        Recovery exec        │  │      Array replic auth      │   │
│   │        SRM admin role       │  │        Test exec only       │  │        SRM cert mgmt        │   │
│   │       Site pair creds       │  │       Read-only audit       │  │        Test isolation       │   │
│   │         Array creds         │  │         Custom roles        │  │         vSAN encr DR        │   │
│   │       Cert management       │  │         vCenter RBAC        │  │        Audit log TLS        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls who uses SRM · RBAC limits recovery execution                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   vCenter SSO    │    SRM admin     │     Replic TLS    │  Cert rotation   │  Recovery audit  │   │
│   │  AD integration  │  Recovery exec   │     Array auth    │  Site pair cert  │     Test log     │   │
│   │ Site pair creds  │    Test exec     │      SRM cert     │ Least privilege  │   Plan changes   │   │
│   │   Array creds    │    Read-only     │     vSAN encr     │  Isolation net   │ GSS audit trail  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers (SRM VMs both sites) · vSAN/SAN · WAN link · AD domain · CA infrastructure               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter SSO        = Single Sign-On; SRM authenticates all users via vCenter SSO domain              │
│  Site pair          = Trusted connection between two SRM servers across protected and recovery sites  │
│  Array-based replication = Storage array replicates LUNs/volumes; SRM integrates via SRA adapter      │
│  vSphere Replication = Host-based replication using HBCR agent; RPO minimum 5 minutes                 │
│  SRM RBAC           = Role-Based Access Control in SRM; roles: admin, recovery exec, test, read-only  │
│  Recovery admin     = SRM role with full recovery plan and protection group management                │
│  Recovery user      = SRM role that can execute recovery plans but not modify them                    │
│  Test operator      = SRM role that can run test failovers only; cannot run real failover             │
│  Certificate management = SRM server TLS cert lifecycle; must be CA-signed for site pair trust        │
│  Audit log          = SRM records all recovery, test, reprotect, and admin operations                 │
│  Test isolation network = Isolated port group used during test failover; blocks production access     │
│  Least privilege    = Principle of assigning minimum SRM role needed for each operator function       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, LDAP, local accounts, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
