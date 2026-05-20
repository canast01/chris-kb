# Cluster Inventory

```
┌───────────────────────────────────── vSphere — Cluster Inventory ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Per-cluster record capturing identity, feature enablement, and capacity state         │   │
│   │       One row per cluster; reviewed during capacity planning, audits, and change control      │   │
│   │       Fields: name, vCenter, environment, host count, HA, DRS, vSAN, NSX, resource pools      │   │
│   │        Capacity fields: overcommit ratio, datastore count, free memory headroom, notes        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identity fields anchor the record · Feature flags drive operational decisions                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Identity          │  │        Feature Flags        │  │           Capacity          │   │
│   │         Cluster name        │  │       HA enabled (Y/N)      │  │          Host count         │   │
│   │         vCenter FQDN        │  │        DRS automation       │  │       Datastore count       │   │
│   │       Environment tag       │  │         vSAN enabled        │  │       vCPU overcommit       │   │
│   │      Datacenter / site      │  │         NSX enabled         │  │        RAM headroom %       │   │
│   │         Owner / team        │  │         EVC baseline        │  │      Free datastore GB      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Identity + flags determine operational posture and expansion eligibility                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Name       │     vCenter      │       HA/DRS      │     vSAN/NSX     │     Capacity     │   │
│   │ cl-prod-compute  │   vcsa-prod-01   │      Y / Auto     │      Y / Y       │    >25% free     │   │
│   │   cl-prod-edge   │   vcsa-prod-01   │    Y / Partial    │      N / Y       │    NFS backed    │   │
│   │  cl-dev-compute  │   vcsa-dev-01    │      Y / Auto     │      Y / N       │     Dev only     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell PowerEdge nodes · vCenter appliance · vSAN disk groups · NSX transport nodes        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cluster       = vSphere grouping of ESXi hosts sharing HA, DRS, and vSAN resources                 │
│    HA            = High Availability; restarts VMs on surviving hosts after a host failure            │
│    DRS           = Distributed Resource Scheduler; balances VM workloads across cluster hosts         │
│    vSAN          = Virtual SAN; pooled storage from host-local NVMe/SSD disks per cluster             │
│    NSX           = Network virtualisation; software-defined networking overlay for the cluster        │
│    EVC           = Enhanced vMotion Compatibility; CPU baseline for cross-host live migration         │
│    DRS Auto      = DRS migrates VMs automatically to balance load without operator approval           │
│    Overcommit    = vCPU or vRAM assigned to VMs vs physical cores/RAM on the cluster                  │
│    HA headroom   = Free memory reserved by admission control for VM restart on host failure           │
│    Resource pool = vSphere object limiting and reserving CPU/memory for a group of VMs                │
│    Environment   = Production / Non-Production / DR tag applied for policy and access scoping         │
│    Datacenter    = vSphere logical container grouping clusters, hosts, and datastores                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
| Field | Example |
|---|---|
| Cluster Name | cl-prod-compute-01 |
| vCenter | vcsa-prod-01 |
| Environment | Production |
| Host Count | 8 |
| HA Enabled | Yes |
| DRS Enabled | Fully Automated |
| vSAN Enabled | Yes |
| NSX Enabled | Yes |
| Notes | Main production compute cluster |
