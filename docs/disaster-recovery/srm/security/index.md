# SRM — Security


```text
┌─────────────────────────────────────────── SRM — Security ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     SRM — Security Posture                                    │   │
│   │Authentication: vCenter SSO / AD integration; SRM admin role; site-pairing certificate exchange│   │
│   │      Encryption: SRM management TLS; replication encryption controlled by array/SRA layer     │   │
│   │               Network: management VLAN separated; 443 (vCenter) management port               │   │
│   │                 Audit: all admin actions logged; log retention minimum 1 year                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │          Encryption         │  │            Audit            │   │
│   │          RBAC roles         │  │       AES-256 at rest       │  │        Admin actions        │   │
│   │       Least privilege       │  │        TLS in transit       │  │         Login events        │   │
│   │         MFA optional        │  │         Key rotation        │  │        Syslog export        │   │
│   │       SVC acct rotate       │  │       WORM / immutable      │  │         SIEM forward        │   │
│   │         Just-In-Time        │  │         KMS managed         │  │       Quarterly review      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Service accounts, site pair credentials, and certificate management.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>vCenter RBAC roles and least-privilege configuration for DR operators.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Firewall ports, TLS certificates, and inter-site communication security.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Test network isolation, audit logging, and SIEM integration.</span>
</a>

</div>
