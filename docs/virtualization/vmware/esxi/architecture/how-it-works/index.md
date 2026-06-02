# ESXi — How It Works


<div class="kb-summary">
How It Works reference covering Networking Architecture, VMkernel Adapters (vmk), Storage Architecture, CPU and Memory Scheduling, HA and DRS and 3 more sections.
</div>

VMkernel Internals — Resource Stack
```text
┌────────────────────────────────────────────────────────────┐
│  VMkernel (bare-metal, no general OS underneath)                                                      │
│                                                                                                       │
│  CPU Scheduler                    Memory Manager                                                      │
│  ├── NUMA-aware placement         ├── TPS (dedup pages)                                               │
│  ├── vCPU → pCPU assignment       ├── Balloon driver                                                  │
│  ├── CPU Ready / Co-stop tracking ├── Compression                                                     │
│  └── Reservations & limits        └── Host swap (.vswp)                                               │
│                                                                                                       │
│  Storage Stack                    Network Stack                                                       │
│  ├── PSA (Pluggable Storage Arch) ├── vSwitch / vDS                                                   │
│  │   ├── NMP (multipathing)       ├── Port groups                                                     │
│  │   │   ├── PSP (RR / MRU / FX) ├── vmkernel adapters                                                │
│  │   │   └── SATP (array rules)  │   vmk0 mgmt                                                        │
│  │   └── VAAI (array offload)    │   vmk1 vMotion                                                     │
│  └── Datastores                   │   vmk2 vSAN                                                       │
│      VMFS6 / NFS / vSAN           │   vmk3 iSCSI/NFS                                                  │
│                                   └── pNICs (vmnic0..n)                                               │
└────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────────── ESXi — How It Works ─────────────────────────────────────────┐
│                                                                                                       │
│  Type-1 hypervisor running directly on hardware; vmkernel mediates all I/O.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           vmkernel (Kernel Layer)            │  │             VM Execution Engine             │   │
│   │        Schedules CPUs across all VMs         │  │          VMX process per running VM         │   │
│   │         Memory balloon / swap / TPS          │  │         vCPU mapped to pCPU threads         │   │
│   │          VMkernel NIC (vmknic) mgmt          │  │          Guest OS in HW virt ring 0         │   │
│   │          Storage I/O via PSA stack           │  │            VMDK on VMFS/NFS/vSAN            │   │
│   │       Networking via vSwitch/dvSwitch        │  │            VMM, VMX, VCPU threads           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  vmkernel sends scheduled VM I/O to PSA (storage) and vSwitch (network).                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Storage I/O Stack (PSA)            │  │              Network I/O Stack              │   │
│   │            NMP → SATP → PSP path             │  │           vSwitch / dvSwitch ports          │   │
│   │          iSCSI/FC/FCoE/NFS/NVMe-oF           │  │         Uplinks to physical switches        │   │
│   │           VMFS datastores on LUNs            │  │           vmk0 mgmt / vmk1 vMotion          │   │
│   │         vSAN uses local disk groups          │  │            vmk2 vSAN / vmk3 other           │   │
│   │         APD/PDL handling per policy          │  │         NIOC bandwidth reservations         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers, NVMe/SSD/HDD, 10/25/100 GbE NICs, FC/iSCSI HBAs, ToR switches                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vmkernel  = ESXi micro-kernel; schedules CPU/mem/I/O for all VMs on host                             │
│  VMX       = user-space process managing one running VM; I/O emulation                                │
│  PSA       = Pluggable Storage Architecture; ESXi storage I/O framework                               │
│  NMP       = Native Multipathing Plugin; default path selector in PSA                                 │
│  SATP      = Storage Array Type Plugin; array-specific PSA plugin                                     │
│  PSP       = Path Selection Policy; round-robin, fixed, or MRU per LUN                                │
│  vmknic    = VMkernel NIC; carries mgmt/vMotion/vSAN/overlay traffic                                  │
│  dvSwitch  = Distributed vSwitch; managed centrally by vCenter                                        │
│  VMFS      = VMware File System; clustered FS shared across ESXi hosts                                │
│  TPS       = Transparent Page Sharing; deduplicates identical guest mem pages                         │
│  APD       = All Paths Down; storage path loss without PDL declared                                   │
│  PDL       = Permanent Device Loss; device signals storage is gone permanently                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
