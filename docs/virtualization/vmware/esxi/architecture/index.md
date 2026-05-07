# ESXi Architecture
## Hypervisor Overview

ESXi is a Type-1 (bare-metal) hypervisor built around the **VMkernel** — a purpose-built OS that directly manages CPU, memory, storage, and network resources on the physical host. ESXi has no general-purpose OS underneath it.

Key design principles:
- **Thin footprint**: ESXi runs from a USB/SD card or M.2 boot device (< 1 GB)
- **In-memory configuration**: most host config is held in memory and persisted to a config store
- **Direct hardware access**: VMkernel drivers communicate directly with hardware via VIBs (vSphere Installation Bundles)

## Management Interfaces

| Interface | Access | Purpose |
|---|---|---|
| DCUI | Physical console (or IPMI/iDRAC KVM) | Emergency management, IP config, lockdown mode |
| ESXi Shell | SSH or local console | Advanced diagnostics; disable when not in use |
| vSphere Client | Via vCenter | Primary day-to-day management |
| ESXi Embedded Host Client | `https://<host>/ui` | Direct host management when vCenter unavailable |
| REST API | `https://<host>/api` | Automation and programmatic access |

## Networking Architecture

### Standard vSwitch (vSS)

Per-host configuration; does not synchronise across hosts. Each host has its own vSS with port groups. Suitable for simple deployments or management isolation.

### Distributed vSwitch (vDS)

Managed at vCenter cluster level; consistent configuration across all hosts in the cluster. Required for vMotion reliability, NSX-T, NIOC, and LACP.

```
Physical NICs (pNICs/vmnic0, vmnic1, ...)
        │
    vDS Uplink Port Group
        │
    ┌───┴──────────────────────┐
    │   vSphere Distributed    │
    │         Switch           │
    │  ┌──────────────────┐   │
    │  │ Port Group A     │   │  ← VM Network
    │  │ Port Group B     │   │  ← vMotion
    │  │ Port Group C     │   │  ← vSAN
    │  └──────────────────┘   │
    └──────────────────────────┘
```

### NIOC (Network I/O Control)

NIOC enforces bandwidth allocation on a shared uplink across traffic types: VM traffic, vMotion, vSAN, management, iSCSI, NFS. Prevents one traffic type from starving others.

### LACP / Link Aggregation

ESXi supports 802.3ad LACP on vDS for bonded uplinks. Requires physical switch LACP configuration. Provides both redundancy and throughput aggregation.

## VMkernel Adapters (vmk)

VMkernel adapters are the host's own network endpoints. Standard production layout:

| Adapter | Traffic Type | Typical VLAN |
|---|---|---|
| vmk0 | Management | Mgmt VLAN |
| vmk1 | vMotion | vMotion VLAN |
| vmk2 | vSAN | vSAN VLAN |
| vmk3 | NFS or iSCSI | Storage VLAN |

Each vmk is associated with a port group and has a TCP/IP stack:
- **Default stack**: management, vMotion (can be moved), NFS
- **vMotion stack**: dedicated TCP/IP stack for vMotion
- **Provisioning stack**: NFC traffic for cold migration/clone
- **vSAN stack**: not used; vSAN uses vmk tagged with vSAN service

## Storage Architecture

| Type | Protocol | Notes |
|---|---|---|
| VMFS6 | FC, iSCSI, FCoE, SAS | Block; supports 64 TB LUNs, cluster locking |
| NFS 3 | NFS over TCP | Simple; no VAAI NAS for thin block |
| NFS 4.1 | NFS over TCP | Kerberos auth, session trunking |
| iSCSI (SW) | iSCSI over TCP | Software initiator built into VMkernel |
| FC / FCoE | FC fabric | Hardware HBA or CNA required |
| NVMe/FC | FC fabric | NVMe over FC; low-latency block |
| NVMe/TCP | TCP/IP | NVMe over TCP; supported vSphere 7.0 U3+ |
| vSAN | Internal (vSAN network) | HCI; managed from within vCenter |

### Multipathing (PSP)

ESXi multipathing is managed by NMP (Native Multipathing Plugin):

| Policy | Description | When to Use |
|---|---|---|
| Most Recently Used (MRU) | Uses last active path; fails over on failure | Active/Passive arrays |
| Fixed | Always uses preferred path; returns after failover | Active/Active arrays where path pinning is needed |
| Round Robin (RR) | Distributes I/O across active paths | Active/Active arrays (Pure, NetApp AFF, etc.) |

Verify PSP for a device:
```bash
esxcli storage nmp device list | grep -A5 <device>
```

## High Availability at Host Level

ESXi hosts do not provide HA themselves — HA is orchestrated by vCenter through the **HA cluster**. When a host fails:

1. vCenter HA master detects host failure (network isolation or host failure)
2. HA master elects which surviving host will restart failed VMs
3. VMs are restarted based on restart priority and available capacity (admission control)

**Host Profiles** enforce consistent configuration across cluster hosts. Applied from vCenter; any host that drifts from profile is flagged as non-compliant.
