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

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="dr-design/">
  <strong>DR Design</strong>
  <span>RTO/RPO tier matrix, replication strategies, site topology, network design, and recovery objective governance.</span>
</a>

<a class="kb-card" href="runbooks/">
  <strong>Runbooks</strong>
  <span>Step-by-step DR procedures — failover, failback, and full DR activation runbook.</span>
</a>

<a class="kb-card" href="recovery-testing/">
  <strong>Recovery Testing</strong>
  <span>Tabletop exercises, functional tests, full DR failover tests, and ransomware recovery validation.</span>
</a>

<a class="kb-card" href="ire/">
  <strong>Isolated Recovery Environment</strong>
  <span>Air-gapped clean-room for ransomware recovery — isolation, clean-room restore, and CyberSense validation.</span>
</a>

<a class="kb-card" href="backup-validation/">
  <strong>Backup Validation</strong>
  <span>Automated and manual verification that backups are intact and recoverable within defined objectives.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Pre-change, post-change, and DR-readiness health checks across platform layers.</span>
</a>

<a class="kb-card" href="failure-testing/">
  <strong>Failure Testing</strong>
  <span>Planned failure injection, chaos testing, and resilience validation procedures.</span>
</a>

<a class="kb-card" href="reliability-engineering/">
  <strong>Reliability Engineering</strong>
  <span>SRE principles for infrastructure — error budgets, toil reduction, and chaos engineering.</span>
</a>

<a class="kb-card" href="service-level-objectives/">
  <strong>Service Level Objectives</strong>
  <span>Defining SLOs and SLIs for infrastructure services — availability, latency, and error rate targets.</span>
</a>

<a class="kb-card" href="service-availability/">
  <strong>Service Availability</strong>
  <span>Measuring and reporting service availability — uptime tracking, incident impact, and reporting cadence.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common DR and backup failures — backup job errors, replication lag, failover issues, and IRE connectivity.</span>
</a>

</div>
