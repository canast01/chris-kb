# ESXi — Architecture Overview

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
| ESXCLI | SSH shell or remote via esxcli `-s` | Command-line host configuration and scripting |
| REST API | `https://<host>/api` | Automation and programmatic access |

---

## VMkernel Processes

The ESXi VMkernel schedules VMs and manages physical resources through a set of core internal processes:

| Process | Function |
|---|---|
| `vmkctl` | VMkernel control interface — creates/destroys VMs |
| `hostd` | Host management daemon — handles vSphere API calls |
| `vpxa` | vCenter agent — maintains vCenter connection |
| `ntpd` | NTP time synchronisation |
| `sfcbd` | CIM provider — hardware monitoring via CIM/IPMI |
| `fdm` | Fault Domain Manager — vSphere HA agent |
| `vmx` | Per-VM process — manages each powered-on VM |

```bash
# Check all running processes
ps | grep -v grep | head -30

# Check management agent status
/etc/init.d/hostd status
/etc/init.d/vpxa status

# Restart management agents (safe when VMs are running)
/etc/init.d/hostd restart
/etc/init.d/vpxa restart
```

---

## High Availability at Host Level

ESXi hosts do not provide HA themselves — HA is orchestrated by vCenter through the **HA cluster**. When a host fails:

1. vCenter HA master detects host failure via heartbeat network and datastore heartbeat
2. HA master elects which surviving hosts will restart failed VMs
3. VMs are restarted based on restart priority and available capacity (admission control)

**HA Admission Control** ensures the cluster always retains enough capacity to absorb the failure of N hosts (configurable — default is 1). If admission control would be violated, vCenter blocks VM power-on operations.

**Host Isolation Response**: If a host loses management network connectivity but VMs are still running, the host's isolation response determines whether to leave VMs running or power them off (configurable per cluster: `Leave Powered On`, `Power Off`, or `Shut Down`).

---

## CPU and Memory Scheduling

### CPU Scheduling

The ESXi CPU scheduler assigns physical CPU time to VM vCPUs. Key concepts:

| Concept | Description |
|---|---|
| CPU Ready (`%RDY`) | Time a vCPU spent waiting for a physical CPU — high values indicate overcommitment |
| CPU Co-stop (`%CSTP`) | vCPUs in an SMP VM waiting for each other to be co-scheduled — reduce vCPU count |
| NUMA | Non-Uniform Memory Access — VMs perform best when all vCPUs and memory fit in one NUMA node |
| CPU Limit | Maximum CPU allocation; set to -1 (unlimited) unless required |
| CPU Reservation | Guaranteed minimum CPU; use for latency-sensitive workloads |

### Memory Management

ESXi manages memory through a hierarchy of techniques (from least to most impactful on performance):

1. **Transparent Page Sharing (TPS)**: Deduplicates identical memory pages across VMs
2. **Balloon driver**: Inflates inside the guest, causing the guest OS to swap — less impactful than host swap
3. **Host Swap**: ESXi swaps VM memory to the `.vswp` file on a datastore — high latency
4. **Memory Compression**: Compresses 4KB pages before swapping — faster than full swap

```bash
# Check memory stats on a host
esxtop
# Press 'm' for memory view
# Key columns: MCTLSZ (balloon), SWCUR (host swap), GRANT (memory given to VMs)
```

---

## vSphere HA and DRS Integration

### vSphere HA

| Feature | Function |
|---|---|
| VM Restart | Restarts VMs on surviving hosts after a host failure |
| VM Monitoring | Restarts individual VMs if VMware Tools heartbeat fails |
| Proactive HA | Pre-emptively migrates VMs from hosts with degrading hardware |
| Application Monitoring | Guest-level health checking (requires VMware Tools) |

### DRS (Distributed Resource Scheduler)

DRS balances VM load across the cluster using vMotion. Operation modes:

| Mode | Behaviour |
|---|---|
| Manual | DRS provides recommendations; admin applies them |
| Partially Automated | DRS auto-places on power-on; manual for ongoing balancing |
| Fully Automated | DRS auto-places and auto-migrates based on imbalance threshold |

DRS imbalance threshold (1–5): lower = more aggressive migrations.

```powershell
# Check DRS recommendations (PowerCLI)
Get-Cluster "CL-PROD" | Get-DrsRecommendation

# Apply all pending recommendations
Get-Cluster "CL-PROD" | Get-DrsRecommendation | Apply-DrsRecommendation
```

---

## Boot Architecture

### ESXi Boot Device

ESXi boots from one of:

| Boot Device | Notes |
|---|---|
| M.2 SD card (older) | Factory default on many Dell/HP servers pre-2020; no local VMFS |
| M.2 NVMe (newer) | Preferred for vSphere 7/8; allows persistent logging without SAN |
| USB (legacy) | Not recommended for production — high failure rate |
| SAN LUN (Boot from SAN) | FC or iSCSI; ESXi boot from a dedicated LUN on the storage array |

### Boot from SAN

Boot from SAN allows the ESXi image to reside on a shared SAN LUN. All hosts boot from individual LUNs on the same array.

Requirements:
- Dedicated boot LUN per host (do not share boot LUNs)
- HBA must be configured as boot initiator in BIOS
- SAN zoning: each HBA initiator sees only its boot LUN (not cluster LUNs)
- LUN must be at least 8 GB (minimum); 32 GB recommended

```bash
# Verify boot device
esxcli system boot device get

# View HBA boot configuration
esxcli storage san fc list
esxcli iscsi adapter get -A vmhba64
```

### Host Profiles

Host Profiles capture the entire ESXi host configuration and enforce it consistently across all cluster hosts. Deviations are flagged as non-compliant.

Key captured settings:
- VMkernel adapter configuration (IPs, services, MTU)
- NTP servers
- DNS servers
- Firewall ruleset state
- VIB acceptance level
- PSP/SATP storage rules
- SSH and ESXi Shell state
- Syslog server
- Advanced settings (security timeouts, etc.)

```powershell
# Extract a host profile from a reference host
New-VMHostProfile -Name "HP-Cluster-Profile" \
    -ReferenceHost (Get-VMHost "esxi-01.corp.local") \
    -Description "Cluster hardened baseline"

# Check compliance for all hosts
Get-VMHost | ForEach-Object {
    Test-VMHostProfileCompliance -VMHost $_ |
        Select-Object VMHost, ComplianceStatus, IncomplianceDescription
}
```

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
