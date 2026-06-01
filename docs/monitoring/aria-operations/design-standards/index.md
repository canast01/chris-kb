# Aria Operations Standards


<div class="kb-summary">
Aria Operations Standards reference covering Alert Naming Convention, Alert Policy Hierarchy, Super Metric Standards, Dashboard Naming Convention, Custom Group Naming and 2 more sections.
</div>

```
┌───────────────────────────────── Aria Operations — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Sizing & Topology      │  │        Data Retention       │  │      High Availability      │   │
│   │      XS: 1 node ≤1k obj     │  │      Metrics: 6 months      │  │        2-node minimum       │   │
│   │      S: 1 node ≤5k obj      │  │       Events: 6 months      │  │       Witness optional      │   │
│   │       M: 2 nodes ≤20k       │  │      Snapshots: 30 days     │  │      vSphere HA enabled     │   │
│   │       L: 4 nodes ≤50k       │  │      Purge via vROps UI     │  │      DRS anti-affinity      │   │
│   │      XL: 8 nodes ≤150k      │  │       Backup: nightly       │  │       Shared datastore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Naming, tagging, and alert policy standards drive consistent operation across all environments     │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Naming Standards      │  │     Alert Policy Design     │  │      Adapter Standards      │   │
│   │       Groups: env-team      │  │        Symptom first        │  │      1 adapter/instance     │   │
│   │     Dashboards: func-obj    │  │     Threshold reviewed Q    │  │       Credential vault      │   │
│   │     Reports: sched-scope    │  │     No duplicate alerts     │  │       PAK from VMware       │   │
│   │    Alerts: sev-component    │  │     Notify via outbound     │  │       Test before prod      │   │
│   │       Tags: env+owner       │  │      Escalation defined     │  │        Version locked       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Master node: 4 vCPU 16 GB min · Data node: 8 vCPU 32 GB · NFS/vSAN for VMDK storage                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Object = Monitored entity in Aria Ops (VM, host, datastore, application component)                   │
│  Super metric = Formula combining raw metrics into a single derived KPI                               │
│  Policy = Named ruleset controlling collection intervals, thresholds, and alert actions               │
│  Group = Dynamic or static collection of objects; policies and alerts applied at group level          │
│  PAK = Plugin/adapter package installed via Administration > Solutions                                │
│  Symptom = Condition evaluated against metric; true/false trigger for alert                           │
│  Recommendation = Action suggested when alert fires (KB link, runbook, automated action)              │
│  Outbound plugin = Webhook or SMTP/SNMP connector for alert notification                              │
│  Anti-affinity = DRS rule keeping Aria Ops nodes on separate ESXi hosts                               │
│  Retention = Days Aria Ops stores raw metrics before rollup and eventual purge                        │
│  Witness node = Tie-breaking node used in 2-node HA cluster to avoid split-brain                      │
│  NFS datastore = Shared storage enabling vSphere HA restart of Aria Ops VMs                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────── Aria Operations — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Sizing & Topology      │  │        Data Retention       │  │      High Availability      │   │
│   │      XS: 1 node ≤1k obj     │  │      Metrics: 6 months      │  │        2-node minimum       │   │
│   │      S: 1 node ≤5k obj      │  │       Events: 6 months      │  │       Witness optional      │   │
│   │       M: 2 nodes ≤20k       │  │      Snapshots: 30 days     │  │      vSphere HA enabled     │   │
│   │       L: 4 nodes ≤50k       │  │      Purge via vROps UI     │  │      DRS anti-affinity      │   │
│   │      XL: 8 nodes ≤150k      │  │       Backup: nightly       │  │       Shared datastore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Naming, tagging, and alert policy standards drive consistent operation across all environments     │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Naming Standards      │  │     Alert Policy Design     │  │      Adapter Standards      │   │
│   │       Groups: env-team      │  │        Symptom first        │  │      1 adapter/instance     │   │
│   │     Dashboards: func-obj    │  │     Threshold reviewed Q    │  │       Credential vault      │   │
│   │     Reports: sched-scope    │  │     No duplicate alerts     │  │       PAK from VMware       │   │
│   │    Alerts: sev-component    │  │     Notify via outbound     │  │       Test before prod      │   │
│   │       Tags: env+owner       │  │      Escalation defined     │  │        Version locked       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Master node: 4 vCPU 16 GB min · Data node: 8 vCPU 32 GB · NFS/vSAN for VMDK storage                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Object = Monitored entity in Aria Ops (VM, host, datastore, application component)                   │
│  Super metric = Formula combining raw metrics into a single derived KPI                               │
│  Policy = Named ruleset controlling collection intervals, thresholds, and alert actions               │
│  Group = Dynamic or static collection of objects; policies and alerts applied at group level          │
│  PAK = Plugin/adapter package installed via Administration > Solutions                                │
│  Symptom = Condition evaluated against metric; true/false trigger for alert                           │
│  Recommendation = Action suggested when alert fires (KB link, runbook, automated action)              │
│  Outbound plugin = Webhook or SMTP/SNMP connector for alert notification                              │
│  Anti-affinity = DRS rule keeping Aria Ops nodes on separate ESXi hosts                               │
│  Retention = Days Aria Ops stores raw metrics before rollup and eventual purge                        │
│  Witness node = Tie-breaking node used in 2-node HA cluster to avoid split-brain                      │
│  NFS datastore = Shared storage enabling vSphere HA restart of Aria Ops VMs                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Alert Naming Convention

Alerts follow the pattern `ENV-OBJECT_TYPE-CONDITION` to ensure consistent filtering and automated routing.

Examples:
- `PROD-VM-CPU_CONTENTION`
- `PROD-HOST-MEMORY_BALLOON`
- `NONPROD-DATASTORE-CAPACITY_WARN`

Alert names must be unique across all alert definitions. Use ALL_CAPS for the condition segment.

## Alert Policy Hierarchy

Policies are applied from broadest to most specific; the most specific policy wins.

| Policy Level | Scope | Example |
|---|---|---|
| Global Default | All objects, all environments | Base CPU/memory thresholds |
| Environment Policy | Prod or non-prod object groups | Tighter thresholds for PROD |
| Cluster Policy | Specific cluster or workload group | DB cluster, VDI cluster |

Always document the rationale for any threshold that deviates from the Global Default policy.

## Super Metric Standards

- Prefix: `SM_` followed by a descriptive camelCase name
- Examples: `SM_AvgClusterCpuUsage`, `SM_VMStorageLatencyP95`
- Super metrics must include a description field explaining the formula
- Review super metric accuracy after any vCenter or adapter upgrade

## Dashboard Naming Convention

Dashboards use the format `TEAM-Topic-Scope`.

| Segment | Rule | Example |
|---|---|---|
| TEAM | Owning team prefix | `INFRA`, `DBA`, `NETWORK` |
| Topic | Functional area | `Capacity`, `Performance`, `Alerts` |
| Scope | Breadth of data | `Overview`, `Cluster`, `VM` |

Examples:
- `INFRA-Capacity-Overview`
- `DBA-Performance-SQLCluster`
- `NETWORK-Alerts-NSXEdge`

Shared dashboards visible to all users should be placed in the **Shared** folder. Team-specific dashboards go in the relevant team folder.

## Custom Group Naming

Custom groups follow `ENV-ObjectType`.

- `PROD-ComputeCluster`
- `NONPROD-VM`
- `PROD-Datastore`

Dynamic groups should use membership criteria that automatically includes new objects (e.g., objects in a named vCenter folder or cluster).

## Report Schedules

| Report | Schedule | Audience |
|---|---|---|
| Capacity Overview | Weekly, Monday 07:00 | Infra team |
| Top-N VMs by Contention | Weekly, Monday 07:00 | Infra + App teams |
| Monthly Executive Capacity Summary | Monthly, 1st working day | Management |
| Alert Trend Report | Weekly | Ops team |

Reports are distributed via email and archived in the shared drive capacity folder.

## Threshold Reference

| Metric | Warning | Critical |
|---|---|---|
| VM CPU Usage | 80% | 95% |
| VM Memory Usage | 85% | 95% |
| Host CPU Contention | 5% | 10% |
| Host Memory Balloon | 1% | 5% |
| Datastore Capacity Used | 75% | 85% |
| Datastore Latency (ms) | 10 | 20 |
