# ESXi — How It Works

```
VMkernel Internals — Resource Stack
┌────────────────────────────────────────────────────────────┐
│  VMkernel (bare-metal, no general OS underneath)           │
│                                                            │
│  CPU Scheduler                    Memory Manager           │
│  ├── NUMA-aware placement         ├── TPS (dedup pages)    │
│  ├── vCPU → pCPU assignment       ├── Balloon driver       │
│  ├── CPU Ready / Co-stop tracking ├── Compression          │
│  └── Reservations & limits        └── Host swap (.vswp)    │
│                                                            │
│  Storage Stack                    Network Stack            │
│  ├── PSA (Pluggable Storage Arch) ├── vSwitch / vDS        │
│  │   ├── NMP (multipathing)       ├── Port groups          │
│  │   │   ├── PSP (RR / MRU / FX) ├── vmkernel adapters     │
│  │   │   └── SATP (array rules)  │   vmk0 mgmt             │
│  │   └── VAAI (array offload)    │   vmk1 vMotion          │
│  └── Datastores                   │   vmk2 vSAN            │
│      VMFS6 / NFS / vSAN           │   vmk3 iSCSI/NFS       │
│                                   └── pNICs (vmnic0..n)    │
└────────────────────────────────────────────────────────────┘
  ↑ Hardware: CPUs · RAM · HBAs (FC/NVMe) · NICs · Disk
```

## Hypervisor Overview

ESXi is a Type-1 (bare-metal) hypervisor built around the **VMkernel** — a purpose-built OS that directly manages CPU, memory, storage, and network resources on the physical host. ESXi has no general-purpose OS underneath it; the VMkernel communicates directly with hardware through drivers packaged as VIBs (vSphere Installation Bundles).

Key design principles:

- **Thin footprint**: ESXi runs from a USB/SD card or M.2 boot device (< 1 GB image)
- **In-memory configuration**: most host config is held in memory and persisted to a configuration store (`/etc/vmware/` and persistent scratch partition)
- **Direct hardware access**: VMkernel drivers communicate directly with hardware via VIBs

---

## Management Interfaces

| Interface | Access Method | Purpose |
|---|---|---|
| DCUI (Direct Console UI) | Physical console or IPMI/iDRAC KVM | Emergency management, IP config, lockdown mode |
| ESXi Shell | SSH or local console | Advanced diagnostics; disable when not in use |
| vSphere Client | Via vCenter | Primary day-to-day management |
| ESXi Embedded Host Client | `https://<host>/ui` | Direct host management when vCenter unavailable |
| ESXCLI | SSH shell or remote via `esxcli -s` | Command-line host configuration and scripting |
| REST API | `https://<host>/api` | Automation and programmatic access |

---

## VMkernel Processes

The ESXi VMkernel schedules VMs and manages physical resources through a set of core internal processes:

| Process | Function |
|---|---|
| `hostd` | Host management daemon — handles vSphere API calls |
| `vpxa` | vCenter agent — maintains vCenter connection |
| `fdm` | Fault Domain Manager — vSphere HA agent |
| `vmx` | Per-VM process — manages each powered-on VM |
| `ntpd` | NTP time synchronisation |
| `sfcbd` | CIM provider — hardware monitoring via CIM/IPMI |
| `vmkctl` | VMkernel control interface — creates/destroys VMs |

```bash
# Check management agent status
/etc/init.d/hostd status
/etc/init.d/vpxa status

# Restart management agents (safe when VMs are running)
/etc/init.d/hostd restart
/etc/init.d/vpxa restart
```

---

## Networking Architecture

### Standard vSwitch (vSS)

Per-host configuration; does not synchronise across hosts. Each host has its own vSS with port groups. Suitable for simple deployments or management isolation.

### Distributed vSwitch (vDS)

Managed at vCenter cluster level; consistent configuration across all hosts in the cluster. Required for vMotion reliability, NSX, NIOC, and LACP.

### NIOC (Network I/O Control)

NIOC enforces bandwidth allocation on a shared uplink across traffic types: VM traffic, vMotion, vSAN, management, iSCSI, NFS. Prevents one traffic type from starving others.

### LACP / Link Aggregation

ESXi supports 802.3ad LACP on vDS for bonded uplinks. Requires physical switch LACP configuration. Provides both redundancy and throughput aggregation.

## VMkernel Adapters (vmk)

Standard production layout:

| Adapter | Traffic Type | MTU | Typical VLAN |
|---|---|---|---|
| vmk0 | Management | 1500 | Mgmt VLAN |
| vmk1 | vMotion | 9000 | vMotion VLAN |
| vmk2 | vSAN | 9000 | vSAN VLAN |
| vmk3 | NFS or iSCSI | 9000 | Storage VLAN |

Each vmk is associated with a port group and a TCP/IP stack:
- **Default stack**: management, NFS
- **vMotion stack**: dedicated TCP/IP stack for vMotion traffic
- **Provisioning stack**: NFC traffic for cold migration and clone
- **vSAN stack**: not used; vSAN uses a vmk tagged with the vSAN service

---

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

```bash
# View multipath policy for a device
esxcli storage nmp device list | grep -A5 <device-naa>

# Set Round Robin for a device
esxcli storage nmp psp roundrobin deviceconfig set -d <device-naa> --type=iops --iops=1
```

---

## CPU and Memory Scheduling

### CPU Scheduling

The ESXi CPU scheduler assigns physical CPU time to VM vCPUs:

| Concept | Description |
|---|---|
| CPU Ready (`%RDY`) | Time a vCPU spent waiting for a physical CPU — high values indicate overcommitment |
| CPU Co-stop (`%CSTP`) | vCPUs in an SMP VM waiting for each other — reduce vCPU count |
| NUMA | VMs perform best when all vCPUs and memory fit in one NUMA node |
| CPU Limit | Maximum CPU allocation; set to -1 (unlimited) unless explicitly required |
| CPU Reservation | Guaranteed minimum CPU; use for latency-sensitive workloads |

### Memory Management

ESXi manages memory through a hierarchy of techniques (from least to most impactful on performance):

1. **Transparent Page Sharing (TPS)**: Deduplicates identical memory pages across VMs
2. **Balloon driver**: Inflates inside the guest, causing the guest OS to swap
3. **Memory Compression**: Compresses 4KB pages before swapping — faster than full swap
4. **Host Swap**: ESXi swaps VM memory to the `.vswp` file on a datastore — high latency

```bash
# Check memory stats on a host
esxtop
# Press 'm' for memory view
# Key columns: MCTLSZ (balloon), SWCUR (host swap), GRANT (memory given to VMs)
```

---

## HA and DRS

### vSphere HA

When a host fails, vCenter HA restarts VMs on surviving hosts. Key features:

| Feature | Function |
|---|---|
| VM Restart | Restarts VMs on surviving hosts after a host failure |
| VM Monitoring | Restarts individual VMs if VMware Tools heartbeat fails |
| Proactive HA | Pre-emptively migrates VMs from hosts with degrading hardware |
| Admission Control | Reserves capacity to absorb failure of N hosts (default: 1) |

**Host Isolation Response**: If a host loses management network connectivity, the isolation response determines VM behaviour: `Leave Powered On`, `Power Off`, or `Shut Down`.

### DRS (Distributed Resource Scheduler)

DRS balances VM load across the cluster using vMotion:

| Mode | Behaviour |
|---|---|
| Manual | DRS provides recommendations; admin applies them |
| Partially Automated | Auto-places on power-on; manual for ongoing balancing |
| Fully Automated | Auto-places and auto-migrates based on imbalance threshold (1–5) |

```powershell
# Check DRS recommendations
Get-Cluster "CL-PROD" | Get-DrsRecommendation

# Apply all pending recommendations
Get-Cluster "CL-PROD" | Get-DrsRecommendation | Apply-DrsRecommendation
```

---

## Boot Architecture

ESXi boots from one of:

| Boot Device | Notes |
|---|---|
| M.2 NVMe | Preferred for vSphere 7/8; allows persistent logging without SAN |
| M.2 SD card (older) | Factory default on many Dell/HP servers pre-2020; no local VMFS |
| USB (legacy) | Not recommended for production — high failure rate |
| SAN LUN (Boot from SAN) | FC or iSCSI; ESXi boot from a dedicated LUN on the storage array |

### Boot from SAN

Requirements:
- Dedicated boot LUN per host (do not share boot LUNs)
- HBA must be configured as boot initiator in BIOS
- SAN zoning: each HBA initiator sees only its own boot LUN
- LUN minimum 8 GB; 32 GB recommended

```bash
# Verify boot device
esxcli system boot device get

# View HBA boot configuration
esxcli storage san fc list
esxcli iscsi adapter get -A vmhba64
```

---

## Host Profiles

Host Profiles capture the entire ESXi host configuration and enforce it consistently across all cluster hosts. Deviations are flagged as non-compliant.

Key captured settings:
- VMkernel adapter configuration (IPs, services, MTU)
- NTP and DNS servers
- Firewall ruleset state
- VIB acceptance level
- PSP/SATP storage rules
- SSH and ESXi Shell state
- Syslog server
- Advanced settings (security timeouts, etc.)

```powershell
# Extract a host profile from a reference host
New-VMHostProfile -Name "HP-Cluster-Profile" `
    -ReferenceHost (Get-VMHost "esxi-01.example.local") `
    -Description "Cluster hardened baseline"

# Check compliance for all hosts
Get-VMHost | ForEach-Object {
    Test-VMHostProfileCompliance -VMHost $_ |
        Select-Object VMHost, ComplianceStatus, IncomplianceDescription
}
```

---

## Ports and Logs

| Use | Protocol | Port |
|---|---|---|
| vSphere Client / API | HTTPS | 443 |
| ESXi Host Client | HTTPS | 443 |
| vCenter to ESXi (vpxa) | HTTPS | 902 |
| NFC (migration / backup) | TCP | 902 |
| vSAN transport | TCP/UDP | 2233 |
| CIM (hardware monitoring) | HTTP/HTTPS | 5988 / 5989 |

**Key log files (ESXi host):**

- `/var/log/vmkernel.log` — kernel events, storage, network
- `/var/log/hostd.log` — host management agent
- `/var/log/vpxa.log` — vCenter agent
- `/var/log/fdm.log` — HA Fault Domain Manager
- `/var/log/vobd.log` — VM observer daemon (HA events)
- `/var/log/syslog.log` — general system log
