# vSAN — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering ESA Migration, Driver and Firmware.
</div>

```text
VSAN UPGRADE SEQUENCE (host-by-host rolling)

  Pre-checks
  ├── Health: all green
  ├── No degraded objects
  └── Resync queue empty
         │
         ▼
  Step 1 — Upgrade vCenter Server (always first)
         │
         ▼
  Step 2 — Update vLCM Cluster Image
           (target ESXi build + certified driver versions)
         │
         ▼
  ┌──────────────────────────────────────────────────┐
  │  Per-Host Remediation Loop (one host at a time)  │
  │                                                  │
  │  ESXi-01 → Maintenance Mode (Full Data Mig.)     │
  │          → vLCM upgrades ESXi + drivers          │
  │          → Host exits maintenance mode           │
  │          → Verify vSAN health (must be green)    │
  │          → Verify resync complete (0 bytes)       │
  │                                                  │
  │  ESXi-02 → same sequence                         │
  │  ESXi-03 → same sequence                         │
  │  ... (all hosts)                                 │
  └──────────────────────────────────────────────────┘
         │
         ▼
  Post-upgrade validation
  ├── All hosts on new ESXi build
  ├── vSAN health all green
  ├── Disk format version current
  └── Object compliance 100%
```
```
┌────────────────────────────────────── vSAN — Install & Upgrade ───────────────────────────────────────┐
│                                                                                                       │
│  vSAN is enabled per cluster in vCenter; hardware must be on the HCL; upgrades                        │
│  use vSphere Lifecycle Manager (vLCM) with host remediation.                                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Enable vSAN Checklist             │  │             Disk Group Creation             │   │
│   │            HCL: verify all disks             │  │              Claim disks in UI              │   │
│   │           10GbE+ VMkernel per host           │  │           Cache: 1 disk per group           │   │
│   │           Jumbo frames on switches           │  │           Capacity: 1–7 per group           │   │
│   │          Cluster > Configure > vSAN          │  │           ESA: all NVMe auto-claim          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  HCL compliance is mandatory; non-HCL disks cause unsupported configuration warning.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Upgrade with vLCM               │  │              Post-Upgrade Steps             │   │
│   │            Create baseline image             │  │              Run health checks              │   │
│   │              Attach to cluster               │  │          Verify disk format version         │   │
│   │           Remediate: rolling hosts           │  │          Upgrade disk format (OSA)          │   │
│   │          Hosts: maintenance → patch          │  │           Monitor resync complete           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Each host must enter maintenance mode before remediation; vSAN evacuates data                        │
│  during maintenance; requires 30% free space for safe data migration.                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vLCM          = vSphere Lifecycle Manager; baseline images + remediation                             │
│  Remediate     = apply baseline to host; put in maintenance, patch, reboot                            │
│  HCL           = Hardware Compatibility List; required for support                                    │
│  Disk format   = vSAN on-disk format version; upgrade after host upgrade                              │
│  OSA           = Original Storage Architecture; needs explicit format upgrade                         │
│  ESA           = Express Storage Architecture; vSAN 8+; all-NVMe                                      │
│  VMkernel      = vSAN network adapter; must be enabled with vSAN tag                                  │
│  Maintenance mode= evacuates VMs; ensures FTT=1 redundancy before host offline                        │
│  Jumbo frames  = MTU 9000; configure on TOR switches and VMkernel                                     │
│  Resync        = post-upgrade, data rebalances across now-updated hosts                               │
│  Claim disks   = select disks in VC UI for cache/capacity role                                        │
│  Disk group    = logical container of cache + capacity disks per host                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Upgrade Procedure

All health checks must pass before beginning an upgrade. Resolve any degraded objects or active resyncs before proceeding.

**Upgrade sequence:**

1. Upgrade vCenter Server first (never upgrade ESXi before vCenter on a vSAN cluster).
2. Update vLCM cluster image baseline to the target ESXi version.
3. Remediate one host at a time via vLCM. vLCM will:
   - Place the host in maintenance mode with the "Ensure Accessibility" or "Full Data Migration" option.
   - Validate vSAN health before and after each host.
   - Upgrade ESXi and NVMe/disk controller drivers in a single reboot.
4. Verify vSAN health after each host remediation before proceeding to the next.

**FTT requirement during upgrade:**

vSAN must maintain policy compliance throughout the upgrade. With FTT=1, one host is in maintenance at a time — the cluster needs at least 3 remaining healthy hosts. With FTT=2, at least 5 hosts must remain healthy while one is in maintenance.

If the cluster does not have sufficient hosts to maintain FTT during the upgrade, either:
- Temporarily change the storage policy to a lower FTT (accept reduced protection).
- Add hosts before upgrading.

**Post-upgrade validation:**

```bash
# Verify all hosts on new build
esxcli system version get

# Verify vSAN health
esxcli vsan health cluster list

# Check object compliance
esxcli vsan debug object list | grep -i noncompliant
```

## ESA Migration

The Express Storage Architecture (ESA) introduced in vSAN 8.0 is not an in-place upgrade from OSA. Migration requires a new cluster build.

**Migration options:**

1. **Build a new ESA cluster** in the same vCenter and Storage vMotion VMs from the OSA cluster to the ESA cluster. This is the recommended approach for minimal downtime.
2. **Site-level failover** (for stretched clusters): fail over to one site, rebuild the other as ESA, then fail back and rebuild the original site.
3. **Backup and restore** via Veeam or another backup tool: restore VMs to the new ESA cluster.

ESA requires:
- vSphere 8.0 or later.
- NVMe devices on the ESA-specific HCL (different from OSA HCL).
- Minimum 4 hosts.
- All hosts in the cluster must use ESA; mixed OSA/ESA is not supported.

## Driver and Firmware

vSAN is highly sensitive to disk controller driver versions. Use only hardware on the VMware HCL and only the driver versions certified for the specific controller and vSAN version.

```bash
# Check disk controller driver version
esxcli software vib list | grep -i <controller-name>

# Check device/firmware info
esxcli storage core device list
```

**vLCM with hardware support manager:** If the server vendor (Dell, HPE, Lenovo) provides a vSphere Lifecycle Manager Hardware Support Manager plugin, use it to manage firmware and driver updates alongside ESXi updates in a single vLCM image. This ensures certified driver/firmware combinations are applied together.

**Key rule:** Never apply an ESXi patch without also verifying that the disk controller driver version in the vLCM image is HCL-certified for vSAN. Mismatched drivers are a leading cause of disk group failures post-upgrade.
