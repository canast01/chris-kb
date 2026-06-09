# Backup & DR

<div class="kb-summary">
Enterprise backup and disaster recovery — Veeam, Commvault, and NetBackup backup products, plus DR design, runbooks, recovery testing, Isolated Recovery Environment (IRE), backup validation, and health checks.
</div>

```text
┌──────────────────────────── Backup & Disaster Recovery Platform ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    Backup & DR — Scope and Objectives                                         │   │
│   │   Backup = protecting data and enabling point-in-time recovery                                │   │
│   │   DR = restoring service availability after a site-level or major disruptive event            │   │
│   │   RPO drives backup frequency · RTO drives recovery infrastructure sizing                     │   │
│   │   Untested DR is a hypothesis — validated DR requires scheduled tests and runbooks            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Backup Products         │  │        DR Runbooks          │  │     Recovery Testing        │   │
│   │   Veeam · Commvault         │  │   Failover · failback       │  │   Tabletop · functional     │   │
│   │   NetBackup                 │  │   Step-by-step procedures   │  │   Full DR test · ransomware │   │
│   │   Jobs · repos · proxies    │  │   Escalation contacts       │  │   Evidence and sign-off     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │    Isolated Recovery Env    │  │       DR Design             │  │   Backup Validation         │   │
│   │   Air-gap vault · IRE       │  │   RTO/RPO tiers · strategy  │  │   Verify restorability      │   │
│   │   Clean-room restore        │  │   Site topology · network   │  │   SureBackup · bpverify     │   │
│   │   CyberSense integrity      │  │   Replication technology    │  │   Test restore cadence      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Backup servers · proxy servers · dedup appliances · tape libraries · object storage targets          │
│  Production site · DR site · replication link · management network · vault network                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│  RPO         = Recovery Point Objective; max acceptable data loss window                              │
│  RTO         = Recovery Time Objective; max acceptable downtime before restore                        │
│  Failover    = activating the DR site; redirecting hosts to replica resources                         │
│  Failback    = returning operations to production site after DR event is resolved                     │
│  IRE         = Isolated Recovery Environment; air-gapped clean-room for ransomware recovery           │
│  Immutability= backup data that cannot be modified or deleted for a defined retention period          │
│  Cyber vault = air-gapped isolated copy with integrity verification for ransomware scenarios          │
│  Dedup       = deduplication; eliminates redundant data blocks across backup jobs                     │
│  Proxy       = Veeam/Commvault component that moves data from source to repository                    │
│  Repository  = backup storage target — disk, dedup appliance, object store, or tape                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Backup Products

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="veeam/">
  <strong>Veeam</strong>
  <span>VM and physical backup, replication, instant recovery, and Veeam ONE monitoring.</span>
</a>

<a class="kb-card" href="commvault/">
  <strong>Commvault</strong>
  <span>Enterprise data platform — backup, archive, compliance, and cloud integration.</span>
</a>

<a class="kb-card" href="netbackup/">
  <strong>NetBackup</strong>
  <span>Enterprise backup for VMs, physical servers, databases, and tape infrastructure.</span>
</a>

</div>

## Disaster Recovery

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="dr-operations/">
  <strong>DR Operations</strong>
  <span>DR design, runbooks, recovery testing, IRE, backup validation, health checks, failure testing, SLOs, service availability, and troubleshooting.</span>
</a>

</div>
