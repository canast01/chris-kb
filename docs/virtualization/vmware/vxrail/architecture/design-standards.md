---
tags:
  - architecture
  - vmware
  - vxrail
---
# VxRail — Design Standards

<div class="kb-summary">
Node count requirements, cluster naming, vSAN policy standards, network design rules, and configuration baselines for VxRail HCI deployments.

*Applies to: VxRail 7.x · 8.x*
</div>
```text
┌──────────────────── Virtualization Vmware Vxrail — Architecture Design Standards ─────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Vmware design standards: network isolation, redundancy, sizing, naming conventions      │   │
│   │          Network: dedicated storage VLAN; jumbo frames for iSCSI; dual-fabric for FC          │   │
│   │          Redundancy: dual controllers, multipath I/O, and no single points of failure         │   │
│   │       Monitoring: set capacity and latency alerts; baseline performance after deployment      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Requirements → architecture design → redundancy review → size → deploy                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Vxrail infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Vxrail platform overview and core concepts              │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Cluster Sizing Standards

| Parameter | Minimum | Recommended | Maximum |
|---|---|---|---|
| Nodes per cluster | 3 | 4–8 | 64 |
| FTT=1 (RAID-1 / RAID-5) | 3 (RAID-1) or 4 (RAID-5) | 4 (RAID-5 for capacity efficiency) | — |
| FTT=2 (RAID-6) | 6 | 6+ | — |
| Dedicated management nodes | Optional | Separate cluster for vCenter/management | — |

- Use **FTT=1 RAID-5** for ≥ 4 nodes with mixed workloads (best capacity:performance balance)
- Use **FTT=1 RAID-1** for 3-node clusters and latency-sensitive workloads
- Use **FTT=2 RAID-6** for workloads requiring dual-drive failure tolerance

## Node Families

| Family | Profile | Use Case |
|---|---|---|
| P-series (NVMe AF) | All-flash NVMe | Latency-sensitive; maximum IOPS |
| V-series (Hybrid) | SSD cache + SAS capacity | Mixed workloads; cost-optimised |
| E-series (Entry AF) | All-flash SAS | Mid-range; standard enterprise workloads |
| D-series (Dense) | Large capacity | Data-intensive; backup targets |

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Cluster name | `vxrail-{site}-{seq}` | `vxrail-dc1-01` |
| Node name | `{cluster}-node-{n}` | `vxrail-dc1-01-node-1` |
| vSAN datastore | `vsds-{cluster}` | `vsds-vxrail-dc1-01` |
| vSAN storage policy | `vsp-{ftt}-{type}-{tier}` | `vsp-ftt1-raid5-gold` |

## vSAN Storage Policy Standards

| Policy Name | FTT | Method | Target Workload |
|---|---|---|---|
| `vsp-ftt1-raid5-gold` | 1 | RAID-5 | Standard VMs; balanced capacity/resilience |
| `vsp-ftt1-raid1-platinum` | 1 | RAID-1 | Latency-sensitive; databases |
| `vsp-ftt2-raid6-gold` | 2 | RAID-6 | Dual-failure tolerance; critical workloads |
| `vsp-ftt1-raid1-mgmt` | 1 | RAID-1 | Management VMs (vCenter, VxRail Manager) |

## Network Design

VxRail requires four VMkernel networks per node, separated by VLAN:

| VMkernel | Purpose | VLAN | MTU |
|---|---|---|---|
| Management (vmk0) | ESXi host management | Mgmt VLAN | 1500 |
| vSAN (vmk1) | vSAN storage traffic | vSAN VLAN | 9000 (jumbo) |
| vMotion (vmk2) | Live migration | vMotion VLAN | 9000 (jumbo) |
| VxRail Management | VxRail Manager to iDRAC | VxRail Mgmt VLAN | 1500 |

- Use 25GbE or higher for all node uplinks in production
- Bond two uplinks per node (LACP or active-standby) for redundancy

## Configuration Checklist

- [ ] LCM Composite Bundle downloaded and staged before deployment
- [ ] DNS entries created for each node management IP and vCenter VIP
- [ ] NTP configured (VxRail Manager inherits from ESXi; set ESXi NTP first)
- [ ] vSAN storage policies created and assigned to VMs by workload tier
- [ ] iDRAC access credentials stored in CyberArk
- [ ] VxRail Manager admin credentials stored in CyberArk
- [ ] Proactive HA / vSAN health checks green in vCenter
- [ ] SupportAssist registered for warranty and firmware update eligibility

## See also

- [VxRail — How It Works (VMware Platform)](how-it-works/)
- [VxRail — Deploy](../deploy/)
