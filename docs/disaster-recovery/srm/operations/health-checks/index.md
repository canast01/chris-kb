# SRM Operations — Health Checks


<div class="kb-summary">
Health Checks reference covering Weekly Checks, Quarterly.
</div>

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

## Run This Routine

1. **SRM service status** — On both protected and recovery SRM servers, open Services or run `Get-Service -Name vmware-dr | Select Status`; confirm the SRM service is `Running` on both sites.
2. **Site pair connection** — In the SRM UI, navigate to **Site Recovery → Sites** and verify the site pair shows `Connected`; a `Disconnected` status indicates a network or certificate issue between vCenter instances.
3. **Protection group health** — Navigate to **SRM UI → Protection Groups**; all groups must show status `OK`; any group in `Not Ready` or `Error` state must be investigated before end of business day.
4. **Recovery plan readiness** — Navigate to **SRM UI → Recovery Plans**; confirm every plan shows `Ready`; a plan in `Not Ready` indicates a missing placeholder VM, failed network mapping, or an unresolved dependency.
5. **Replication health** — In the vSphere Replication UI, go to **Monitor → Replication**; confirm no VMs show RPO violations (red or amber); compare current lag against the agreed RPO target and escalate if exceeded.
6. **Placeholder VM presence** — At the recovery site vCenter, browse the DR cluster inventory and confirm placeholder VMs exist for each protected VM; missing placeholders indicate a broken protection group configuration.
7. **Network mappings** — In **SRM UI → Network Mappings**, confirm all mappings show a green status with valid source and target networks; any unmapped entry will cause a recovery plan to fail at the network configuration step.
8. **Last test date** — In **SRM UI → Recovery Plans**, check the **Last Test** column for each plan; if any plan has not been tested in more than 90 days, raise a change request to schedule a test failover within the next two weeks.

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
