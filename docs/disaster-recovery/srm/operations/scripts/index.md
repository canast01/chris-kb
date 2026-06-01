# SRM Operations — Scripts


<div class="kb-summary">
SRM Operations — Scripts reference.
</div>

```
┌──────────────────────────────────────────── SRM — Scripts ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    SRM — Automation Scripts                                   │   │
│   │                Scripts automate routine SRM operations — run via cron or CI/CD                │   │
│   │               Always store credentials in vault (not in script); log all output               │   │
│   │                 Test scripts in non-production before scheduling in production                │   │
│   │                        Scope scripts to least-privilege service account                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Status / Reporting Scripts          │  │              Automation Scripts             │   │
│   │           Job success rate report            │  │            Auto-expire old points           │   │
│   │              Capacity trending               │  │          Auto-add new VMs to policy         │   │
│   │            SLA compliance report             │  │          Nightly DR test validation         │   │
│   │             RPO / RTO dashboard              │  │             Alert on job failure            │   │
│   │              srm-cli plan test               │  │               srm-cli pg list               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
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
