# NetApp Operations — Health Checks

<div class="kb-summary">
Health Checks reference covering Daily Health Check Workflow, AutoSupport Validation, Pre-Change Checklist, Health Summary Table.
</div>
```text
┌────────────────────────────────── NetApp Operations — Health Checks ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      NetApp Ops health checks: routine verification of operational status and performance     │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Monitoring         │  │           ActiveIQ          │  │       Risk assessment       │   │
│   │          Telemetry          │  │         AutoSupport         │  │       Call-home relay       │   │
│   │         Health check        │  │        Config Advisor       │  │        Best practice        │   │
│   │           Support           │  │     mysupport.netapp.com    │  │        SR management        │   │
│   │           Upgrade           │  │         NDO rolling         │  │        Non-disruptive       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NetApp AFF/FAS clusters · ActiveIQ SaaS · mysupport.netapp.com support portal            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ActiveIQ           = NetApp SaaS health portal; risk assessment, upgrade advisor, capacity planning│
│    AutoSupport        = ONTAP telemetry; sends daily health reports and call-home bundles to NetApp   │
│    Config Advisor     = NetApp best-practice checker; validates cabling, config, and firmware         │
│    NDO                = Non-Disruptive Operations; rolling upgrades without host I/O service disrup...│
│    Takeover           = HA failover; one node takes over partner storage on node failure event        │
│    Giveback           = return storage to original node after failover; completes HA pair recovery    │
│    Aggregate relocation = move aggregate between HA pair nodes without service disruption             │
│    LIF migration      = move logical interface to different node port during planned maintenance      │
│    System Manager     = ONTAP web GUI; unified management for cluster, SVMs, volumes, policies        │
│    ONTAP CLI          = SSH to cluster management IP; diag privilege required for low-level commands  │
│    mysupport          = mysupport.netapp.com; open SRs, download firmware, and access knowledge base  │
│    ASUP bundle        = AutoSupport bundle with logs, config, and core files for TAC case analysis    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Daily Health Check Workflow

```bash
# 1. Overall cluster health
cluster show
system health status show

# 2. HA pair status
storage failover show

# 3. Disk health
storage disk show -broken

# 4. Aggregate health
storage aggregate show -state !online
storage aggregate show -fields percent-used | awk '$2 > 80'

# 5. Volume health
volume show -state !online
volume show -fields percent-used | awk '$2 > 85'

# 6. Interface health
network interface show -status-oper down

# 7. EMS critical events (last 24 hours)
event log show -severity critical -time ">24h"
event log show -severity error -time ">24h"

# 8. SnapMirror health
snapmirror show -health false
```

## AutoSupport Validation

```bash
system node autosupport show -fields state,last-successful-destination
```

Confirm last successful delivery is recent (within 24 hours for daily AutoSupport).

## Pre-Change Checklist

- [ ] Cluster health: `system health status show` → ok
- [ ] HA connected: `storage failover show` → Connected
- [ ] No broken disks: `storage disk show -broken` → no output
- [ ] All aggregates online: `storage aggregate show -state !online` → no output
- [ ] All volumes online: `volume show -state !online` → no output
- [ ] No down LIFs: `network interface show -status-oper down` → no output
- [ ] No critical EMS events in 24h
- [ ] SnapMirror relationships healthy

## Health Summary Table

| Check | Command | Expected |
|---|---|---|
| Cluster nodes | `cluster show` | health: true |
| HA pair | `storage failover show` | Connected |
| Disks | `storage disk show -broken` | No output |
| Aggregates | `storage aggregate show -state !online` | No output |
| Capacity | `storage aggregate show` | < 80% |
| Volumes | `volume show -state !online` | No output |
| LIFs | `network interface show -status-oper down` | No output |
| EMS | `event log show -severity critical` | No output |
| SnapMirror | `snapmirror show -health false` | No output |
