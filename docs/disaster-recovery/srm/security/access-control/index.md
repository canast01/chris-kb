```yaml
Privileges to include:
  Site Recovery Manager:
    - Site Recovery.Manage
    - Site Recovery.Test
    - Site Recovery.Recovery
  Datastore:
    - Datastore.AllocateSpace
  Network:
    - Network.Assign (for network customisation)
  Virtual Machine:
    - Virtual Machine.Provisioning.* (for recovery)
```

```text
┌──────────────────────────────────────── SRM — Access Control ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 SRM — RBAC and Access Control                                 │   │
│   │     Auth: vCenter SSO / AD integration; SRM admin role; site-pairing certificate exchange     │   │
│   │             Principle of least privilege: each role gets only required permissions            │   │
│   │              Service accounts: dedicated, non-interactive; rotation every 90 days             │   │
│   │               Emergency break-glass: documented, monitored, time-limited access               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Role       │   Access Level   │    Typical User   │   Review Freq    │    Granted By    │   │
│   │      Admin       │ Full config/ops  │   Sr Backup Eng   │    Quarterly     │  Security team   │   │
│   │     Operator     │ Start/stop jobs  │     Backup Eng    │    Quarterly     │    Team lead     │   │
│   │     Monitor      │  Read-only view  │      NOC / L1     │    Quarterly     │    Team lead     │   │
│   │   Service Acct   │  API / headless  │     Automation    │   Per rotation   │  Security team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
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
