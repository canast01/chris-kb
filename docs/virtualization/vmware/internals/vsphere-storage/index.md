---
tags:
  - internals
  - vmware
---
# vSphere Storage Architecture — Datastores, Policies, and Advanced Features

vSphere supports a broad set of storage protocols and datastore types. Choosing the right combination depends on performance requirements, existing hardware, budget, and operational complexity. This page covers the full vSphere storage stack from protocols through SPBM policies, multipathing, and advanced features such as NVMe-oF and PMem — all areas covered on the VCP-DCV 8 exam.

---

## Storage Protocol Overview

vSphere can present storage to VMs through five main protocol stacks. The choice of protocol determines latency characteristics, cabling requirements, management complexity, and which datastore types are available.

### Protocol Comparison Table

| Protocol | Transport | Datastore types | Typical latency | Key use case |
|---|---|---|---|---|
| Fibre Channel (FC) | Dedicated FC fabric (HBA + switch) | VMFS | < 1 ms | Enterprise SAN, high IOPS |
| iSCSI | IP network (software or HW initiator) | VMFS | 1–3 ms | Mid-range SAN over existing Ethernet |
| NFS | IP network | NFS datastore | 1–5 ms | Shared file storage, templates |
| NVMe-oF | RDMA fabric or TCP (NVMe/TCP) | VMFS, vSAN ESA | < 0.5 ms | All-flash arrays, ultra-low latency |
| iSER | iSCSI over RDMA (InfiniBand/RoCE) | VMFS | < 0.5 ms | High-performance iSCSI alternative |

> **VCP-DCV Exam Note:** iSCSI can use either a software initiator (built into ESXi VMkernel, no HBA required) or a hardware initiator (dedicated iSCSI HBA). Software iSCSI uses more CPU but is cheaper. Hardware iSCSI offloads processing to the HBA. Both support multipathing.

### FC vs iSCSI vs NFS Decision Guide

```text
Need shared block storage?
    ├── Already have FC fabric? → Use FC (VMFS)
    ├── IP-only network? → Use iSCSI (VMFS)
    └── Need file-level sharing or templates? → Use NFS

Need HCI / converged storage?
    └── Use vSAN (local drives pooled via software)

Need per-VM policy control via array?
    └── Use vVols (requires VASA-capable array)
```

---

## Datastore Types

### VMFS 6

VMware's native clustered filesystem. Multiple ESXi hosts can mount the same VMFS6 volume simultaneously and access different files concurrently (SCSI reservations/ATS arbitrate file-level locking).

- Block sizes: up to 64 TB per datastore (VMFS6 with 512e/4K drives supported)
- Supports thin provisioning, snapshots, linked clones
- Requires block storage (FC, iSCSI, local SAS/NVMe)
- On-disk locking uses **ATS (Atomic Test and Set)** on hardware that supports it

**Datastore provisioning commands:**

```bash
# List available devices for VMFS
esxcli storage filesystem list
esxcli storage core device list

# Create VMFS6 datastore (use vSphere Client for production)
esxcli storage vmfs extent add --volume-label=DS-PROD01 --disk-name=naa.xxx
```

### NFS 4.1

NFS datastores mount a network file share directly from a NAS array. NFS 4.1 (recommended over 3.x) adds:
- Session trunking (multipath NFS via multiple VMkernel ports)
- Kerberos authentication (krb5, krb5i, krb5p)
- Improved locking (stateful, no need for external lock manager)

> **VCP-DCV Exam Note:** NFS 4.1 supports Kerberos authentication; NFS 3 does not. NFS 4.1 also supports session trunking for multipath, whereas NFS 3 requires the host to have only a single path to each NFS mount.

### vSAN

Hyperconverged storage — local drives from each ESXi host are pooled into a distributed datastore. No external storage array needed. Covered extensively in the vSAN section of this KB; key points for storage comparison:

- Minimum 3 hosts (OSA) or 4 hosts (ESA)
- Storage policies (SPBM) define resilience per VM
- All-NVMe recommended for production ESA deployments

### vVols (Virtual Volumes)

vVols moves storage management from the LUN/volume level to the per-VM level. The array creates a storage container; each VM's files (vmdk, config, swap) become individual objects on the array managed via VASA.

- Requires a VASA-capable storage array
- No datastore formatting on the host side — the array manages objects
- Storage policies (SPBM) drive provisioning directly on the array
- Enables per-VM snapshots and replication on the array itself

### Datastore Clusters and Storage DRS (SDRS)

A datastore cluster groups multiple datastores so that SDRS can balance space and I/O load across them, similar to how compute DRS balances hosts.

```text
Datastore Cluster: GOLD-STORAGE
  ├── Datastore: SAN-LUN-01  (10 TB, 80% full)
  ├── Datastore: SAN-LUN-02  (10 TB, 40% full)
  └── Datastore: SAN-LUN-03  (10 TB, 55% full)
        │
        SDRS migrates VMDKs via Storage vMotion
        to rebalance space and I/O
```

SDRS generates migration recommendations or acts automatically (similar to compute DRS automation levels).

---

## Storage Policies — SPBM

Storage Policy-Based Management (SPBM) is a framework that decouples storage capability requirements from specific arrays or datastores. You define a policy describing what you need; vCenter finds compliant storage and enforces the policy at provisioning time.

### How SPBM Works

### Policy Components

A storage policy consists of one or more rule sets. Each rule set specifies capabilities that the datastore must support:

| Component | Example |
|---|---|
| Capability namespace | `VSAN`, `DataServicePolicy`, array-specific |
| Rule: failures to tolerate | FTT=1 (vSAN: tolerate 1 failure) |
| Rule: RAID level | RAID-1 (mirroring) or RAID-5/6 (erasure coding) |
| Rule: IOPS limit | Maximum 5000 IOPS per VMDK |
| Rule: storage tier | All-flash required |

### Compliance States

| State | Meaning |
|---|---|
| Compliant | VMDK meets all policy requirements |
| Non-compliant | VMDK does not meet one or more rules (e.g., FTT=1 requested but only FTT=0 available) |
| Not applicable | No policy assigned to this VMDK |
| Unknown | vCenter cannot determine compliance (VASA provider unavailable) |

> **VCP-DCV Exam Note:** A VM can show "Non-compliant" immediately after a datastore goes degraded — for example, a vSAN host failure that drops below FTT requirements. vCenter flags the compliance state within 15 minutes of a capacity-affecting event. The VM keeps running; it is just unprotected per its policy.

### Applying Policies

```text
vSphere Client:
  VM → Edit Settings → VM Storage Policy → [select policy]

PowerCLI:
  $policy = Get-SpbmStoragePolicy -Name "vSAN-RAID5-FTT1"
  Set-SpbmEntityConfiguration -StoragePolicy $policy -Entity (Get-HardDisk -VM "PROD-DB01")
```

---

## VAAI and VASA

### VAAI — vStorage APIs for Array Integration

VAAI offloads specific storage operations from the ESXi host CPU to the storage array. This reduces host CPU overhead and significantly improves performance for bulk operations.

**VAAI Block (FC/iSCSI) primitives:**

| Primitive | What it does | Benefit |
|---|---|---|
| Full Copy (XCOPY) | Copies data within the array without moving it over the network | Fast cloning and migration |
| Write Same (Zero Out) | Fills a range of blocks with zeros on the array | Fast VMFS creation and eager-zeroed thick provisioning |
| ATS (Atomic Test and Set) | Hardware-accelerated VMFS locking | Replaces SCSI reservations; much lower latency |
| XCOPY Offload | Extended copy for vMotion disk transfer | Faster Storage vMotion |

**VAAI NAS primitives:**

| Primitive | What it does |
|---|---|
| Full File Clone | Array-side clone of VM files (no data over network) |
| Reserve Space | Reserve space for thick-provisioned files on NAS |
| Extended Statistics | Report space usage accurately to ESXi |

> **VCP-DCV Exam Note:** VAAI requires both ESXi support AND array firmware support. If the array does not support a primitive, ESXi falls back to the software path automatically. VAAI primitives for block storage are: Full Copy, Write Same, ATS, and XCOPY. Know these four by name.

### VASA — vStorage APIs for Storage Awareness

VASA is the mechanism by which storage arrays advertise their capabilities to vCenter. Without VASA, vCenter cannot know what features (replication, dedup, tiers) a datastore supports, and SPBM cannot match policies to arrays.

For vVols, VASA is mandatory — the VASA provider on the array handles all object creation and management for vVol-based VMs.

---

## Multipathing

ESXi uses the Native Multipathing Plugin (NMP) framework to manage multiple physical paths to a storage device.

### NMP Architecture

```text
VM I/O Request
      │
      ▼
  NMP (Native Multipathing Plugin)
      │
      ├── SATP (Storage Array Type Plugin)
      │     Identifies array vendor, manages path health
      │     Examples: VMW_SATP_ALUA, VMW_SATP_SVC, VMW_SATP_LOCAL
      │
      └── PSP (Path Selection Plugin)
            Selects which physical path to use for each I/O
            Examples: VMW_PSP_RR, VMW_PSP_MRU, VMW_PSP_FIXED
```

### Path Selection Plugins (PSP)

| PSP | Behavior | Best for |
|---|---|---|
| Round Robin (RR) | Distributes I/O across all active paths | Active-Active arrays, all-flash |
| Most Recently Used (MRU) | Uses last active path; switches only on failure | Active-Passive arrays |
| Fixed | Uses a preferred path; falls back on failure | Arrays with dedicated preferred path |

> **VCP-DCV Exam Note:** Round Robin is the recommended PSP for Active-Active arrays (most modern arrays). MRU is used for Active-Passive arrays where only one path is active at a time and sending I/O to the passive path would fail. The default PSP for ALUA (Asymmetric Logical Unit Access) arrays is typically MRU or RR depending on the SATP.

### iSCSI Multipath Setup

Software iSCSI multipath requires multiple VMkernel ports bound to the software iSCSI initiator:

```bash
# List iSCSI adapters
esxcli iscsi adapter list

# Bind VMkernel ports to iSCSI adapter
esxcli iscsi networkportal add --adapter vmhba65 --nic vmk1
esxcli iscsi networkportal add --adapter vmhba65 --nic vmk2

# Verify paths
esxcli storage nmp path list | grep vmhba65
```

ALUA (Asymmetric Logical Unit Access) arrays expose preferred/non-preferred path states. ESXi selects paths accordingly via the SATP.

---

## SIOC — Storage I/O Control

SIOC prevents storage "noisy neighbor" problems by enforcing per-VM disk I/O shares when the datastore is congested.

### How SIOC Works

```text
Normal operation (no congestion):
  All VMs get full I/O they request — shares ignored

Datastore congestion detected:
  (Latency > congestion threshold, default 30 ms for SSD, 30 ms HDD)
        │
        ▼
  SIOC activates per-VM I/O throttling
  VM shares determine allocation:
    High shares VM  → gets more IOPS
    Low shares VM   → throttled
```

**SIOC configuration per VM:**

| Shares | Relative IOPS allocation when congested |
|---|---|
| Low (500) | Lowest priority |
| Normal (1000) | Default |
| High (2000) | Double normal |
| Custom | Specify exact share count |

**IOPS limit** — you can also set a hard IOPS limit per VM disk, independent of congestion. Useful for ensuring a single VM cannot saturate the datastore.

> **VCP-DCV Exam Note:** SIOC congestion threshold is 30 ms by default (configurable). SIOC only activates when the datastore is congested — it has no effect during normal operation. SIOC requires the datastore to be enabled for SIOC in the datastore settings. It works with VMFS and NFS datastores, but NOT with vVols (vVols use array-side QoS via SPBM).

### Enabling SIOC

```text
vSphere Client:
  Datastore → Configure → General → Storage I/O Control → Enabled
  Set congestion threshold (default: 30 ms, or % of peak throughput)
```

---

## Raw Device Mapping (RDM)

An RDM is a special VMFS file that acts as a proxy, pointing to a raw LUN on the storage array. The VM accesses the LUN directly rather than through a VMDK file.

### RDM Compatibility Modes

| Mode | Description | Supports snapshots | Use case |
|---|---|---|---|
| Virtual (vRDM) | ESXi manages the SCSI layer; VM sees a virtual disk | Yes | Migration, snapshots, while keeping raw LUN |
| Physical (pRDM) | VM sees raw SCSI commands; no ESXi virtualization layer | No | Physical clustering (WSFC with SCSI reservations, Oracle RAC) |

> **VCP-DCV Exam Note:** Physical RDM (pRDM) passes SCSI commands directly to the LUN, which is required for guest clustering solutions (like Windows Server Failover Clustering with SCSI persistent reservations). Virtual RDM (vRDM) supports snapshots and vMotion. Physical RDM does NOT support snapshots or vMotion across hosts (only Storage vMotion of the pointer file).

### RDM Requirements

- Storage must be FC or iSCSI (not NFS or vSAN)
- LUN must not be formatted with a filesystem — it is raw
- The .vmdk file in VMFS is just a mapping descriptor; the actual data is on the raw LUN
- Physical RDMs cannot be used with FT-protected VMs

```bash
# List RDMs attached to a VM
vim-cmd vmsvc/get.summary <vmid> | grep rdm

# ESXi — list available LUNs for RDM
esxcli storage core device list | grep -i naa
```

---

## Advanced Storage: PMem, NVMe, and NVMe-oF

### Persistent Memory (PMem) as Datastore

NVDIMMs (Persistent Memory DIMMs) installed in ESXi hosts can be used as an ultra-low-latency storage tier:

- **vPMem** — exposes PMem as a fast virtual disk to the VM (byte-addressable via SCSI emulation)
- **vPMemDisk** — presents PMem as a raw disk in the VM for use by PMem-aware applications
- PMem datastore appears as a local datastore per host; not shared across hosts

Use cases: in-memory databases (Redis, SAP HANA), latency-critical transaction logs.

### NVMe Local Storage

ESXi supports NVMe drives directly (no SCSI emulation layer):
- NVMe namespaces appear as storage devices in ESXi
- VMFS6 can be created on NVMe devices
- Lower I/O overhead vs SCSI-attached SSDs
- vSAN ESA is designed around NVMe-only storage (no HDD or SATA SSD)

```bash
# List NVMe adapters
esxcli nvme adapter list

# List NVMe namespaces
esxcli nvme namespace list --adapter vmhba1
```

### NVMe-oF — NVMe over Fabrics

NVMe-oF extends NVMe semantics over a network fabric, enabling shared NVMe storage with near-local latency:

| Transport | Notes |
|---|---|
| NVMe/FC | NVMe commands over Fibre Channel; requires Gen 6+ FC HBAs |
| NVMe/RDMA | NVMe over InfiniBand or RoCE; lowest latency |
| NVMe/TCP | NVMe over standard TCP/IP; no special fabric required; higher latency than RDMA |

ESXi 7.0+ supports NVMe/FC and NVMe/TCP. NVMe/TCP requires no special hardware beyond 25 GbE or better NICs.

> **VCP-DCV Exam Note:** NVMe/TCP is the easiest NVMe-oF deployment path because it uses standard IP infrastructure. It has higher latency than NVMe/RDMA but significantly lower than traditional iSCSI at equivalent hardware due to the NVMe queue model (65535 queues vs SCSI's single queue).

---

## Storage Architecture Decision Reference

---

## Quick Reference — Key Facts for VCP-DCV

| Topic | Key fact |
|---|---|
| VMFS maximum datastore size | 64 TB |
| VAAI block primitives | Full Copy, Write Same (Zero Out), ATS, XCOPY |
| SIOC congestion threshold default | 30 ms |
| SPBM compliance check interval | ~15 minutes after capacity event |
| NFS version supporting Kerberos | NFS 4.1 only |
| Physical RDM — snapshots | Not supported |
| Virtual RDM — snapshots | Supported |
| vVols requirement | VASA-capable storage array |
| PSP for Active-Active arrays | Round Robin (VMW_PSP_RR) |
| PSP for Active-Passive arrays | Most Recently Used (VMW_PSP_MRU) |
| NVMe/TCP transport | Standard TCP/IP — no special fabric needed |
| PMem datastore scope | Per-host local only (not shared) |
