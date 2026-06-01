# vSAN — Integrations


<div class="kb-summary">
Integrations reference covering NSX Integration, Stretched Cluster Witness, File Services, Aria Operations.
</div>

```text
vSAN INTEGRATION MAP

  ┌────────────────────────────────────────────────────────┐
  │                    vCenter Server                      │
  │  (management plane — all vSAN config flows through VC) │
  └──────┬──────────┬──────────────┬──────────┬───────────┘
         │          │              │          │
         ▼          ▼              ▼          ▼
  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌───────────┐
  │  vSAN    │ │  NSX    │ │  vSphere │ │   Aria    │
  │ Cluster  │ │         │ │Replication│ │Operations │
  │(data     │ │TEP vmk  │ │          │ │(vROps)    │
  │ plane)   │ │on hosts │ │RPO-based │ │           │
  └────┬─────┘ └────┬────┘ │ VM rep.  │ └─────┬─────┘
       │            │      └──────────┘        │
       ▼            ▼                          │
  ┌────────────────────────────┐               │
  │     ESXi Hosts (shared)    │               │
  │  vmk0 — Management         │◄──────────────┘
  │  vmk1 — vMotion            │   (metrics, health,
  │  vmk2 — vSAN (dedicated)   │    capacity alerts)
  │  vmk3 — NSX TEP            │
  │                            │
  │  Disk Group                │
  │  ├── Cache SSD/NVMe        │
  │  └── Capacity disks        │
  └────────────────────────────┘
         │
         ▼
  ┌───────────────────────┐   ┌──────────────────────┐
  │  vSAN File Services   │   │  Backup Tools        │
  │  (NFS v3/v4.1, SMB)  │   │  (Veeam / Commvault  │
  │  File Agent VMs per   │   │   via VADP + CBT)    │
  │  host, IP pool req.   │   │                      │
  └───────────────────────┘   └──────────────────────┘
```
┌───────────────────────────────────────── vSAN — Integrations ─────────────────────────────────────────┐
│                                                                                                       │
│  vSAN integrates with vCenter for management, NSX for micro-segmentation,                             │
│  external KMS for encryption, and backup tools via VADP.                                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             vCenter Integration              │  │              Backup Integration             │   │
│   │         Managed via Hosts & Clusters         │  │             VADP: CBT snapshots             │   │
│   │           Storage policies from VC           │  │          Veeam / Commvault / Avamar         │   │
│   │             Health in vCenter UI             │  │            NFS target: not needed           │   │
│   │          Alarms: disk/host failures          │  │           SRM: vSAN datastores OK           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  vCenter is the single management plane; policies defined here flow to all vSAN hosts.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Security Integrations             │  │           Monitoring Integrations           │   │
│   │          KMS: external KMIP server           │  │             vROps: vSAN capacity            │   │
│   │           Data-at-rest encryption            │  │             vSAN Skyline health             │   │
│   │         NSX: microsegment VM traffic         │  │          SNMP: disk failure alerts          │   │
│   │         vSAN ESA: inline encryption          │  │             Syslog: host events             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  KMS must be reachable from each ESXi host on KMIP port 5696; monitoring tools                        │
│  use vCenter APIs to pull vSAN health and capacity data.                                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VADP     = vStorage APIs for Data Protection; backup quiescing                                       │
│  CBT      = Changed Block Tracking; incremental backup efficiency                                     │
│  KMIP     = Key Management Interoperability Protocol; port 5696                                       │
│  KMS      = Key Management Server; holds KEKs for vSAN encryption                                     │
│  SRM      = Site Recovery Manager; supports vSAN datastores directly                                  │
│  vROps    = Aria Operations; capacity planning for vSAN                                               │
│  Skyline  = VMware proactive support; vSAN health telemetry                                           │
│  NSX      = network virtualisation; micro-segments guest VMs                                          │
│  Storage policy= VC-defined rules: FTT, RAID, IOPs limit per VM                                       │
│  Avamar   = Dell backup tool; VADP integration for vSAN VMs                                           │
│  Commvault = backup tool; VADP snapshot integration                                                   │
│  Inline enc= ESA encrypts data as it enters the storage layer                                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Key vCenter-managed vSAN functions:

- Cluster creation and disk group claim
- Storage policy creation and assignment
- vSAN health service (Skyline Health)
- Stretched cluster configuration
- File Services configuration
- vSAN upgrade via vLCM

If vCenter is unavailable, existing VMs continue running (vSAN data plane is independent of vCenter), but no configuration changes can be made and health monitoring is unavailable.

## NSX Integration

vSAN and NSX coexist on the same ESXi hosts and share the vSphere Distributed Switch (vDS). Careful NIC planning is required to avoid contention.

**NIC allocation considerations:**

| Traffic Type | Recommended NIC Allocation |
|---|---|
| vSAN vmkernel | Dedicated NIC pair (25 GbE or higher) |
| NSX TEP vmkernel | Separate NIC pair or shared with vMotion on lower-bandwidth environments |
| Management vmkernel | Shared with a management NIC pair |

If NICs are shared between vSAN and NSX TEP traffic, use NIOC (Network I/O Control) on the vDS to set bandwidth reservations:

- vSAN: minimum 50% reservation.
- NSX TEP: minimum 25% reservation.
- vMotion: minimum 25% reservation.

Verify that NSX TEP and vSAN vmkernel adapters are on separate VLANs and separate port groups, even if they share the same physical NICs.

## Stretched Cluster Witness

The vSAN Stretched Cluster requires a witness host at a third site to provide split-brain arbitration.

**Witness options:**

| Option | Description |
|---|---|
| vSAN Witness Appliance | Lightweight OVA deployed on an existing vSphere host at the witness site |
| Physical ESXi host | Full ESXi host with minimal resources; holds only metadata |

The witness host does not run production VMs and requires only minimal resources (the Witness Appliance is a small VM).

**Licensing:** The witness host requires a separate vCenter instance or a free vSphere Hypervisor licence. It cannot be managed by the same vCenter as the production cluster without an additional licence.

**Configuration:** The stretched cluster and witness are configured from vCenter via Cluster > Configure > vSAN > Fault Domains. vCenter creates the fault domains (Site A, Site B, Witness) and manages witness communication automatically.

## File Services

vSAN File Services extends the vSAN datastore to provide NFS and SMB file shares, enabling file-level access for containerised workloads, legacy applications, and multi-writer scenarios.

**Supported protocols:** NFS v3, NFS v4.1, SMB 2.x/3.x

**Requirements:**

- Minimum 3-node vSAN cluster.
- File Service Agent VMs are automatically deployed by vCenter (one per host hosting a file share).
- A dedicated IP pool for File Service Agent VMs.
- DNS entry for the file service VDI endpoint.

**Enabling File Services:**

vSphere Client > Cluster > Configure > vSAN > File Service > Enable

Specify the IP pool, subnet, gateway, and DNS. vCenter deploys the File Service Agent VMs automatically.

File Services is suited for:

- Kubernetes persistent volumes (ReadWriteMany) using NFS.
- Legacy applications requiring SMB file shares without a separate NAS.
- Multi-VM shared storage scenarios.

## Aria Operations

The vSAN management pack in Aria Operations (vROps) provides detailed visibility into vSAN performance, capacity, and health.

**Metrics available:**

| Category | Metrics |
|---|---|
| Cluster | Read/write IOPS, throughput, latency, resync throughput |
| Host | Per-host IOPS, latency, disk group utilisation |
| Disk Group | Cache hit ratio, write buffer utilisation, capacity per disk group |
| Capacity | Used/free/reserved capacity with forecast |
| Health | Health score from Skyline Health, degraded object count |

**Alerting:** Configure alerts in Aria Operations for:

- Resync throughput above threshold (indicates recovery in progress).
- Health score below 80%.
- Object non-compliance count > 0 for more than 1 hour.
- Capacity utilisation above 70%.

The vSAN management pack connects through the vCenter adapter; no separate vSAN credentials are required.
