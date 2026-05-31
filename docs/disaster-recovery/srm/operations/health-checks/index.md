# SRM Operations — Health Checks

```text
┌───────────────────────────────────────── SRM — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 SRM — Health Check Procedures                                 │   │
│   │                 Run these checks daily/weekly to confirm protection is working                │   │
│   │                                        srm-cli plan test                                      │   │
│   │                  Review job completion rate — target 100%; investigate failures               │   │
│   │                         Check replication/backup lag against RPO target                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Check       │  What to verify  │      Expected     │    Frequency     │  Action if bad   │   │
│   │    Job status    │All jobs complete │    100% success   │      Daily       │ Triage failures  │   │
│   │    Lag / RPO     │ Replication lag  │    < RPO target   │      Daily       │  Tune bandwidth  │   │
│   │     Capacity     │ Repo space used  │     < 80% full    │      Weekly      │ Expand or expire │   │
│   │   Restore test   │  Random restore  │    Data intact    │     Monthly      │ Fix backup chain │   │
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
Weekly SRM operations focus on validating protection group health, confirming SRA connectivity, and ensuring recovery plans remain executable. All protection groups must show `OK` status; any group in `Not Ready` or `Error` state must be investigated and resolved before the end of the business day. Quarterly test failovers validate the full recovery plan workflow and must be completed in isolated network segments to avoid impacting production.

## Weekly Checks

| Check | Location / Command | Expected State |
|---|---|---|
| Protection group status | SRM UI → Protection Groups | All groups `OK` |
| SRA connectivity | SRM UI → Array Managers | Connection `Connected` |
| vSphere Replication health | vSphere Replication UI → Monitor | No replication errors |
| Recovery plan status | SRM UI → Recovery Plans | All plans `Ready` |
| Failed protection jobs | SRM UI → Tasks & Events | No failed jobs in last 7 days |

## Quarterly

- Execute test failover on at least one non-critical recovery plan.
- Document results and resolve any script or network mapping failures.
- Confirm SRA version compatibility with current array firmware.
