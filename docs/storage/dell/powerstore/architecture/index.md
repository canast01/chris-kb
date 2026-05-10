# PowerStore — Architecture Overview

## Platform Summary

Dell PowerStore is a mid-range all-flash storage platform released in 2020, built on an active-active appliance architecture with an NVMe-based storage fabric. It replaces the Unity and SC (Compellent) product lines. PowerStore runs **PowerStoreOS (PSTROS)**, a purpose-built operating system derived from a microservices architecture with containerized workloads.

There are two hardware families:

| Family | Models | Primary Differentiator |
|---|---|---|
| PowerStore T (Technology) | 500T, 1000T, 3000T, 5000T, 7000T, 9000T | Scale-out capable; NVMe SSDs; standard appliance form factor |
| PowerStore X (eXtreme) | 500X, 1000X, 3000X, 5000X, 7000X, 9000X | Includes AppsOn — runs containerized VMs and apps on the array nodes directly using vSphere |

Both families support block (iSCSI, Fibre Channel, NVMe-oF), file (NFS, SMB, FTP), and vVols. All models ship with NVMe-based SSDs; there are no spinning-disk configurations.

## Appliance Architecture

Each PowerStore system consists of one or more **appliances**. Each appliance contains:

- Two storage nodes (Node A and Node B) — active-active; both serve I/O simultaneously
- An NVMe storage enclosure containing SSDs
- Front-end I/O modules (Fibre Channel, iSCSI 10/25/100GbE, NVMe-oF/RoCE)
- Back-end NVMe fabric connecting nodes to drives

Nodes communicate over a dedicated internal NVMe fabric — this is the foundation for the active-active controller design. Unlike dual-active architectures that own LUNs per controller, PowerStore volumes are served by both nodes simultaneously with distributed ownership arbitrated at the NVMe layer.

## Scale-Out (PowerStore T only)

Up to four appliances can be combined into a single PowerStore cluster, sharing a unified management plane. Cross-appliance scaling allows:

- Linear increase in capacity and performance across appliances
- Unified data management across the cluster through a single PowerStore Manager instance
- Non-disruptive data migration between appliances within the cluster
- Dynamic rebalancing of volumes across appliances (storage auto-tiering equivalent)

The X-series does not support cluster scale-out — it is designed for a single appliance deployment with the AppsOn workload co-residency model.

## Storage Services

```
PowerStoreOS Services Stack
├── Block Storage (iSCSI / FC / NVMe-oF)
│   ├── Volumes
│   ├── Host mappings (equivalent to masking views)
│   └── vVols (VMware Virtual Volumes)
├── File Storage
│   ├── NAS servers (NFS v3/v4.1, SMB 2.x/3.x)
│   ├── File systems
│   └── Quotas, access zones
├── Data Reduction (inline)
│   ├── Compression (always on)
│   └── Deduplication (pool-level)
├── Protection
│   ├── Snapshots (block and file)
│   ├── Protection policies (schedule + retention)
│   ├── Replication (async and Metro Volume sync)
│   └── Import (from Unity, SC, VNX, VNXe)
└── AppsOn (X-series only)
    └── Embedded vSphere / Kubernetes workloads
```

## Data Reduction

PowerStore applies inline data reduction to all data — there is no tiering or caching layer to manage. The reduction approach:

- **Compression**: Always enabled at write; LZ-based algorithm optimized for NVMe latency
- **Deduplication**: Pool-wide deduplication; block-level; on by default; can be disabled per volume group if the workload is known to be incompressible (e.g., pre-encrypted backup data)
- **Reported as**: Data Reduction Ratio (DRR) — shown per volume group and system-wide in PowerStore Manager

Typical effective DRR for mixed database/VM workloads: 3–5:1. Encrypted data or pre-compressed media will show DRR near 1:1.

## Metro Volume (Synchronous Replication)

Metro Volume provides zero RPO synchronous replication between two PowerStore appliances across a stretched campus or metro distance (typically up to 100 km / 5 ms RTT):

- Both sites maintain an active copy; hosts write to a primary site, which replicates synchronously to the secondary before acknowledging
- Mediator (a lightweight VM deployed at a third site or on a cloud instance) breaks split-brain on site failure
- Automatic failover: if the primary site loses connectivity, the mediator grants the secondary site authority; host I/O resumes within seconds
- Stretched host access (e.g., VMware HA clusters) can be configured to continue I/O from the surviving site without administrator intervention

Metro Volume is licensed separately from base PowerStore software.

## NAS Architecture

PowerStore NAS is delivered through **NAS servers** — logical entities that aggregate file protocols and networking for a set of file systems. Key design points:

- Each NAS server is active on one node at a time (unlike block, which is active-active)
- NAS server failover to the peer node is automatic on node failure
- NAS servers support SMB 2.x/3.x (Windows/Linux), NFS v3 and v4.1, and multi-protocol (SMB + NFS simultaneously on the same file system)
- File system quotas, access zones, and CIFS shadow copies are managed per NAS server

## AppsOn (X-series)

On PowerStore X-series appliances, storage nodes also run VMware ESXi as the host OS. This enables virtual machines and containerized applications to run on the array hardware itself:

- PowerStore X ships with a bundled vSphere instance pre-configured on the nodes
- VMs are stored on local PowerStore volumes — eliminating the need for a separate compute tier for management workloads
- Intended workloads: edge compute, branch office consolidation, secondary applications that benefit from low-latency shared storage
- Production database VMs requiring deterministic low latency should still be placed on dedicated compute hosts with external PowerStore block storage

## Management Interfaces

| Interface | Access Method | Purpose |
|---|---|---|
| PowerStore Manager | HTTPS on management IP | Primary web UI — provisioning, monitoring, protection |
| REST API | HTTPS `https://<mgmt-ip>/api/rest/` | Full API for automation and integration |
| pstcli | Binary installed on a management host | CLI wrapper for REST API; suitable for scripting |
| vSphere Plugin | vCenter extension | VM-centric provisioning of vVols and datastores |
| CloudIQ | SaaS (cloud) via SCG | Predictive analytics, health scoring, capacity forecasting |
| SupportAssist | Outbound to Dell SRS | Automated support and proactive monitoring |

## Physical Connectivity

Front-end host connectivity options (I/O modules are field-replaceable):

| Protocol | Interface | Speed |
|---|---|---|
| Fibre Channel | FC 32Gb/16Gb | 32 Gbps or 16 Gbps per port |
| iSCSI | 10GbE / 25GbE / 100GbE | 10/25/100 Gbps per port |
| NVMe-oF (RoCE) | 25GbE / 100GbE | 25/100 Gbps per port; requires RoCE-capable NICs and switches |

Back-end: NVMe PCIe fabric internal to the appliance — not customer-configurable.

## Redundancy Model

- **Power**: dual power supplies per node; dual PSUs per drive enclosure
- **Cooling**: N+1 fans per node
- **Networking**: redundant management and data paths; recommend dual-fabric SAN zoning for block hosts
- **Drive failure**: NVMe SSDs in RAID 5 (3+1) or RAID 6 (4+2) pools depending on configured protection level; PowerStore automatically chooses protection level at pool creation based on drive count
- **Node failure**: peer node assumes all I/O within seconds (block); NAS server fail-over completes within seconds

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
