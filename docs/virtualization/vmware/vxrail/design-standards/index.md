---
tags:
  - vxrail
---
# VxRail Standards

<div class="kb-summary">
VxRail design standards: node count and cluster size limits, vSAN-backed storage requirements, witness node placement, dual-switch topology rules, and L2 network requirements.

*Applies to: VxRail 7.x · 8.x*
</div>

VxRail Design Requirements — Key Standards
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Network VLAN Separation (required)                                                                   │
│                                                                                                       │
│  VLAN: Management   MTU 1500   ESXi mgmt, vCenter                                                     │
│  VLAN: vMotion      MTU 9000   live VM migration (jumbo)                                              │
│  VLAN: vSAN         MTU 9000   storage traffic (jumbo)                                                │
│  VLAN: VxRail Mgmt  MTU 1500   VxRail Manager internal                                                │
│  VLAN: VM Traffic   per-app    workload connectivity                                                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                               │
```
```text
                               │
┌────────────────────────────────────────────────── ▼ ──────────────────────────────────────────────────┐
│  Firmware / Software Rule                                                                             │
│  All updates MUST go through VxRail LCM Composite Bundle                                              │
│  Never update vSphere, vSAN, or firmware independently                                                │
│  Verify HCL alignment after every LCM bundle apply                                                    │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

```d2
direction: down

naming_conventions: "Naming Conventions" {shape: rectangle}
cluster_sizing_standards: "Cluster Sizing Standards" {shape: rectangle}
vsan_storage_policy_standards: "vSAN Storage Policy Standards" {shape: rectangle}
network_vlan_standards: "Network VLAN Standards" {shape: rectangle}
firmware_and_software_standards: "Firmware and Software Standards" {shape: rectangle}
change_management_standards: "Change Management Standards" {shape: rectangle}

naming_conventions -> cluster_sizing_standards: hardens
cluster_sizing_standards -> vsan_storage_policy_standards: hardens
vsan_storage_policy_standards -> network_vlan_standards: hardens
network_vlan_standards -> firmware_and_software_standards: hardens
firmware_and_software_standards -> change_management_standards: hardens
```

## Naming Conventions

| Item | Standard | Example |
|---|---|---|
| Node hostname | `<site>-vxr-<nn>` | `lon-vxr-01` |
| Cluster name | `<site>-vxr-cluster-<nn>` | `lon-vxr-cluster-01` |
| vCenter datacenter | `<site>-dc` | `lon-dc` |
| vSAN datastore | `vsanDatastore` (default) or `<site>-vsan-ds` | `lon-vsan-ds` |
| iDRAC DNS name | `<node-hostname>-idrac` | `lon-vxr-01-idrac` |

---

## Cluster Sizing Standards

| Requirement | Standard |
|---|---|
| Minimum cluster size | 3 nodes (satisfies FTT=1 vSAN) |
| Recommended minimum (production) | 4 nodes (allows 1 node in maintenance with FTT=1 intact) |
| Recommended for FTT=2 | 6 nodes minimum |
| Node SKU selection | All nodes within a cluster must be the same SKU for supported operation |
| Mixed-node clusters | Not supported in standard VxRail; contact Dell for stretched/mixed configs |

---

## vSAN Storage Policy Standards

| Policy | Workload Type | FTT | Method |
|---|---|---|---|
| Production (capacity-optimised) | Standard VMs | FTT=1 | RAID-5 (requires 4+ nodes) |
| Production (performance-optimised) | Latency-sensitive VMs | FTT=1 | RAID-1 (mirroring) |
| Critical / high-value | Databases, critical app tiers | FTT=2 | RAID-6 (requires 6+ nodes) |
| Swap / temp objects | VM swap files | FTT=1 | RAID-1 |

Do not apply FTT=0 policies to production VMs — a single disk failure will cause data loss.

---

## Network VLAN Standards

Each traffic type must use a separate VLAN. Commingling traffic types on a single VLAN is not supported for production VxRail clusters.

| Traffic Type | VLAN Purpose | MTU |
|---|---|---|
| Management | ESXi mgmt, vCenter communication | 1500 |
| vMotion | VM live migration | 9000 (jumbo) |
| vSAN | vSAN storage traffic | 9000 (jumbo) |
| VxRail Management | VxRail Manager internal | 1500 |
| VM traffic | Guest VM workload traffic | Per application |

Jumbo frames (MTU 9000) must be configured end-to-end for vMotion and vSAN VLANs — including on the physical switch ports and uplinks.

---

## Firmware and Software Standards

- All node firmware versions **must** match the VxRail Hardware Compatibility List (HCL) for the cluster's current VxRail bundle version.
- Firmware must not be updated independently of the VxRail LCM bundle — independent firmware updates break HCL alignment.
- vSphere, vSAN, and NSX component versions must match the VxRail Composite Bundle BOM exactly.
- Do not install additional VIBs or third-party software on VxRail ESXi nodes without Dell qualification.

**Verify current bundle version:**

```text
VxRail Manager → System → Software Versions → Current Bundle
```

---

## Change Management Standards

- All VxRail lifecycle operations (LCM upgrades, node additions, node replacements) require a change ticket.
- VxRail LCM upgrades must not be started during business hours — schedule for approved maintenance windows.
- Node additions require pre-validation in VxRail Manager before physical installation.
- Post-change: verify cluster health in VxRail Manager and vSAN Skyline Health before closing the change.

---

## CMDB Standards

Each VxRail node must be registered in the CMDB with:

- Node serial number and service tag
- Cluster membership
- vSAN disk group configuration
- iDRAC IP address
- Firmware version and VxRail bundle version
- Support contract expiry date
