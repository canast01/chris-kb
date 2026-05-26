# ESXi — Architecture

<div class="kb-summary">
ESXi is VMware's Type-1 hypervisor. It is deployed in standalone, standard cluster, vSAN cluster, or stretched cluster configurations depending on resilience, storage, and scale requirements.
</div>

```
┌───────────────────────────────────────── ESXi — Architecture ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    VMware ESXi — Type-1 bare-metal hypervisor; VMkernel OS runs directly on server hardware   │   │
│   │ Deployed standalone, in vSphere cluster, vSAN cluster (HCI), or stretched cluster across sites│   │
│   │ VMkernel ports isolate traffic: management, vMotion, vSAN, NFC, replication — one VMk per role│   │
│   │  Storage: VMFS on SAN (FC/iSCSI/NVMe-oF), NFS datastores, or vSAN — accessed via HBAs + PSPs  │   │
│   │   Networking: vSS per host or vDS cluster-wide; port groups per workload; NIC teaming for HA  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines VMkernel internals · integrations connect vCenter and storage                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │   VMkernel: CPU/RAM sched   │  │    vCenter: mgmt + HA/DRS   │  │       Host naming std       │   │
│   │   vSwitch/vDS port groups   │  │     SAN/NAS/vSAN storage    │  │      BIOS/UEFI baseline     │   │
│   │     HBAs: FC/iSCSI/NVMe     │  │     Backup: VADP via NBD    │  │      VMkernel IP layout     │   │
│   │   NIC teaming: active/stby  │  │     Monitoring: Aria Ops    │  │   NTP: 2 sources required   │   │
│   │     Cluster: HA/DRS/vSAN    │  │    Identity: vCenter SSO    │  │    VIB acceptance policy    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    How-it-works covers VMkernel · integrations connect storage and monitoring                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   How It Works   │   Integrations   │    Design Stds    │    Deployment    │     Key Stds     │   │
│   │  VMkernel sched  │  vCenter plugin  │  Standalone host  │   Single ESXi    │    Naming std    │   │
│   │   vSwitch/vDS    │   SAN/NAS/vSAN   │  vSphere cluster  │   3+ hosts HA    │  BIOS baseline   │   │
│   │  HBA multipath   │   VADP backup    │    vSAN cluster   │   3+ HCI hosts   │   VMk IP plan    │   │
│   │   HA/DRS model   │  Aria Ops intg   │  Stretched clstr  │  4+ 2-per-site   │    VIB policy    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server · CPUs (Intel/AMD) · RAM DIMMs · PCIe HBAs/NICs · SAS/NVMe disks · Power & Cooling        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VMkernel      = ESXi micro-kernel OS; schedules CPU/memory and handles I/O for all VMs on the host   │
│  vSS           = vSphere Standard Switch; per-host virtual switch; port groups define VM networks     │
│  vDS           = vSphere Distributed Switch; cluster-wide switch managed centrally by vCenter         │
│  VMkernel port = VMk NIC for host services: management, vMotion, vSAN, NFC, or replication            │
│  VMFS          = VM File System; cluster-aware filesystem on shared block storage for VMDK files      │
│  HBA           = Host Bus Adapter; PCIe card connecting ESXi to FC SAN or iSCSI/NVMe storage          │
│  PSP           = Path Selection Policy; multipathing algorithm: MRU, Fixed, or Round Robin per LUN    │
│  HA            = vSphere High Availability; restarts VMs on surviving hosts after a host failure      │
│  DRS           = Distributed Resource Scheduler; load-balances VMs across cluster hosts via vMotion   │
│  vSAN          = Virtual SAN; pools local flash/HDD from ESXi hosts into a shared HCI datastore       │
│  VADP          = vStorage APIs for Data Protection; backup vendor interface for consistent VM backup  │
│  VIB           = vSphere Installation Bundle; ESXi software package; acceptance level governs install │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| Cluster Type | Min Hosts | Storage | HA / DRS |
|---|---|---|---|
| Standalone | 1 | Local / external | No |
| Standard Cluster | 3+ | Shared SAN or NAS | Yes |
| vSAN Cluster | 3+ | Pooled from hosts (HCI) | Yes |
| Stretched Cluster | 4+ (2 per site) | vSAN stretched | Yes (site-level) |

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>VMkernel, networking, storage paths, CPU/memory scheduling, HA/DRS, and boot architecture.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>vCenter, storage, network, backup, and monitoring integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Host naming, BIOS baseline, vmkernel layout, NTP, VIB policy, and cluster sizing.</span></a>
</div>

## ESXi Cluster Deployment Models

![ESXi Cluster Deployment Models](../../../../assets/esxi-architecture-overview.svg)

