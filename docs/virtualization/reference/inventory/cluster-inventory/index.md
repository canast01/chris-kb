# Cluster Inventory

> Part of the [Inventory](../index.md) reference.

---

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                         Cluster Inventory Map                            │
├─────────────────────┬────────────┬──────────┬──────────┬────────────────┤
│   Cluster Name      │  Hosts     │ HA / DRS │  vSAN    │  Resources      │
├─────────────────────┼────────────┼──────────┼──────────┼────────────────┤
│ cl-prod-compute-01  │  8 hosts   │ HA ✓     │ 46 TB    │ 384 GHz / 12TB  │
│                     │            │ DRS Full │ Enabled  │                 │
├─────────────────────┼────────────┼──────────┼──────────┼────────────────┤
│ cl-prod-edge-01     │  4 hosts   │ HA ✓     │ —        │  96 GHz / 2TB   │
│                     │            │ DRS Full │ Disabled │                 │
├─────────────────────┼────────────┼──────────┼──────────┼────────────────┤
│ cl-prod-mgmt-01     │  3 hosts   │ HA ✓     │ 14 TB    │  72 GHz / 3TB   │
│                     │            │ DRS Part │ Enabled  │                 │
├─────────────────────┼────────────┼──────────┼──────────┼────────────────┤
│ cl-dr-compute-01    │  4 hosts   │ HA ✓     │ 23 TB    │ 192 GHz / 6TB   │
│                     │            │ DRS Full │ Enabled  │                 │
└─────────────────────┴────────────┴──────────┴──────────┴────────────────┘
```
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
