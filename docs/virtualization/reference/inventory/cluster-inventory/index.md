# Cluster Inventory


<div class="kb-summary">
Cluster Inventory reference covering Overview, Cluster Inventory Table, Fields Reference, Cluster Configuration Checklist.
</div>

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
```text
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
> Part of the [Inventory](../index.md) reference.

---

## Overview

Use this table format to document each vSphere cluster in the environment. Maintain one row per cluster and update after any cluster configuration change or capacity event.

## Cluster Inventory Table

| Cluster Name | Datacenter | Host Count | DRS Mode | HA Enabled | vSAN Enabled | Total CPU (GHz) | Total RAM (TB) | Usable vSAN Capacity | Notes |
|---|---|---|---|---|---|---|---|---|---|
| cl-prod-compute-01 | DC-Primary | 8 | Fully Automated | Yes | Yes | 384 | 12 | 46 TB | Main production compute |
| cl-prod-edge-01 | DC-Primary | 4 | Fully Automated | Yes | No | 96 | 2 | — | NSX edge cluster |
| cl-prod-mgmt-01 | DC-Primary | 3 | Partially Automated | Yes | Yes | 72 | 3 | 14 TB | Management plane cluster |
| cl-dr-compute-01 | DC-Secondary | 4 | Fully Automated | Yes | Yes | 192 | 6 | 23 TB | DR compute cluster |

## Fields Reference

| Field | Description |
|---|---|
| Cluster Name | Follows the naming standard: `<site>-<env>-cluster-<##>` |
| Datacenter | vCenter datacenter object containing the cluster |
| Host Count | Number of ESXi hosts currently in the cluster |
| DRS Mode | Manual / Partially Automated / Fully Automated |
| HA Enabled | Whether vSphere HA is active |
| vSAN Enabled | Whether vSAN is providing storage for the cluster |
| Total CPU (GHz) | Sum of all host CPU capacity in GHz |
| Total RAM (TB) | Sum of all host physical memory |
| Usable vSAN Capacity | Available vSAN capacity accounting for FTT policy overhead |
| Notes | Purpose, owner, or any standing issues |

## Cluster Configuration Checklist

When adding a new cluster, verify:

- [ ] Cluster name follows the naming standard
- [ ] HA is enabled with appropriate admission control settings
- [ ] DRS is set to Fully Automated for production compute clusters
- [ ] EVC is enabled and set to the appropriate CPU baseline
- [ ] vSAN health is green before placing any workloads
- [ ] Cluster is tagged with environment and owner in vCenter
- [ ] Cluster is included in the monitoring platform
