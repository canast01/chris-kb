---
tags:
  - deployment
  - vmware
  - vsan
  - vsphere-8
search:
  boost: 2
---
# vSAN — Deploy

<div class="kb-summary">
End-to-end deployment guide from bare metal to a validated vSAN cluster. Phases 1–3 cover the physical and hypervisor foundation; Phases 4–7 cover vSAN-specific enablement, policy configuration, and end-to-end validation.

*Applies to: vSAN 7.x / 8.x*
</div>

```text
┌────────────────────────────────────── vSAN — Deployment Phases ───────────────────────────────────────┐
│                                                                                                       │
│  Seven phases from bare metal to operational vSAN cluster. Each phase has a clear exit criterion.     │
│  Do not proceed to the next phase until the current phase validates clean.                            │
│                                                                                                       │
│   ┌─────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────────────┐     │
│   │    Phase 1: Physical    │  │      Phase 2: ESXi       │  │         Phase 3: vCenter         │     │
│   │    BIOS/UEFI settings   │  │    Boot from ISO/PXE     │  │         Deploy VCSA OVA          │     │
│   │     Network cabling     │  │    First-boot config     │  │    Configure SSO + inventory     │     │
│   │     iDRAC/iLO config    │  │    vmk0 management IP    │  │     Add hosts to datacenter      │     │
│   │     HCL verification    │  │        NTP + DNS         │  │      Create cluster object       │     │
│   └─────────────────────────┘  └──────────────────────────┘  └──────────────────────────────────┘     │
│                                                                                                       │
│                ▼                            ▼                                 ▼                       │
│                                                                                                       │
│   ┌─────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────────────┐     │
│   │   Phase 4: Networking   │  │   Phase 5: vSAN Enable   │  │  Phase 6: Aria Suite (optional)  │     │
│   │    dvSwitch creation    │  │  Enable vSAN on cluster  │  │   Aria Suite Lifecycle deploy    │     │
│   │   vSAN VMkernel + tag   │  │     Disk group claim     │  │      Aria Operations config      │     │
│   │   MTU 9000 end-to-end   │  │     Storage policies     │  │    vSAN adapter + dashboards     │     │
│   │   NIOC if shared NICs   │  │    Health validation     │  │         Alert thresholds         │     │
│   └─────────────────────────┘  └──────────────────────────┘  └──────────────────────────────────┘     │
│                                                                                                       │
│                                                    ▼                                                  │
│                                                                                                       │
│                                   ┌──────────────────────────────────┐                                │
│                                   │       Phase 7: Validation        │                                │
│                                   │     Skyline Health all green     │                                │
│                                   │    Storage policy compliance     │                                │
│                                   │       Failover simulation        │                                │
│                                   │       Performance baseline       │                                │
│                                   └──────────────────────────────────┘                                │
│                                                                                                       │
│  Physical Infrastructure: All phases run on physical ESXi hosts with NVMe/SSD disks,                  │
│  ToR switches (MTU 9000), OOB management (iDRAC/iLO), and DNS/NTP infrastructure.                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  dvSwitch       = Distributed Virtual Switch; managed from vCenter across all hosts                   │
│  vmk            = VMkernel adapter; IP interface for vSAN, vMotion, management traffic                │
│  VCSA           = vCenter Server Appliance; the VM running vCenter                                    │
│  HCL            = Hardware Compatibility List; required for vSAN support                              │
│  NIOC           = Network I/O Control; traffic shaping on shared NICs                                 │
│  Disk group     = one cache device + 1-7 capacity devices per ESXi host (OSA)                         │
│  SPBM           = Storage Policy-Based Management; policies applied per VM                            │
│  Skyline Health = built-in vSAN health dashboard in vCenter                                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

!!! warning "Disk claim is destructive"
    Claiming disks for vSAN **erases all existing data** on those disks. Confirm disk selection before proceeding — this action cannot be undone.

## Phase 1 — Physical Layer

**Exit criterion:** All hosts powered on, reachable via OOB management, cabling verified, and HCL compliance confirmed.

### BIOS / UEFI Settings

Configure on every host before ESXi installation:

| Setting | Required Value | Reason |
|---|---|---|
| Boot mode | UEFI (preferred) or Legacy BIOS | UEFI required for Secure Boot and TPM 2.0 |
| Hyperthreading | Enabled | Required for ESXi CPU scheduling |
| Virtualisation extensions | Intel VT-x / AMD-V: Enabled | Required for VM execution |
| Power management | Maximum Performance (disable C-states) | Avoids latency spikes from CPU power state transitions |
| NUMA nodes | Match physical topology | Do not interleave NUMA nodes across CPU sockets |
| Turbo boost | Enabled | Improves burst throughput |
| SR-IOV | Enabled if using SR-IOV NICs | Required for direct-pass NIC features |

### Network Cabling

- Connect all hosts to ToR switches with the correct port profile (trunk/access, VLAN tags).
- Verify 25 GbE (minimum) for vSAN traffic. 10 GbE is supported but not recommended for new deployments.
- Confirm jumbo frames (MTU 9000) are configured on every switch port, trunk, and uplink the vSAN traffic traverses.
- Connect OOB management (iDRAC/iLO) to a separate management switch or VLAN.

### OOB Management Configuration (iDRAC / iLO)

Configure on each host:
1. Assign a static IP to iDRAC or iLO.
2. Create a dedicated admin user (do not use the default `root`/`admin` credentials).
3. Enable remote console (HTML5 or Java) — needed for ESXi installation.
4. Set hostname in iDRAC/iLO to match the planned ESXi hostname.

### HCL Verification

Before installation, verify every component against the [VMware Compatibility Guide](https://www.vmware.com/resources/compatibility):

- Server model and BIOS version
- NIC model and firmware
- HBA model and firmware (if used)
- Cache SSD model and firmware (must be exact match)
- Capacity disk model and firmware (must be exact match)

**HCL failures at this stage are cheaper to fix than after cluster deployment.**

---

## Phase 2 — ESXi Installation and First-Boot Config

**Exit criterion:** All hosts running ESXi with correct IP, hostname, NTP, DNS, and SSH accessible.

### Install ESXi

Install ESXi from bootable ISO (USB, iDRAC virtual media, or PXE):

1. Boot from ESXi ISO.
2. Accept EULA, select install disk (use a dedicated boot device — not a vSAN disk).
3. Set root password.
4. Complete installation and reboot.

Recommended boot device: dedicated M.2 SSD, SD card (with a 2-card redundant BOSS card), or USB (not recommended for production).

### First-Boot Configuration (DCUI)

Immediately after first boot, via the Direct Console User Interface (F2 → System Customization):

```text
Configure Management Network:
  → Network Adapters: select the correct management NIC (vmnic0 or vmnic1)
  → IP Configuration: set static IP, subnet, gateway
  → DNS Configuration: set DNS servers and hostname (FQDN)
  → Custom DNS Suffixes: add your domain

Test Management Network → confirm all tests pass
Restart Management Network → apply changes
```

### ESXi Shell and SSH Configuration

```bash
# Enable SSH from DCUI: Troubleshooting Options → Enable SSH
# Or via vSphere Client after adding to vCenter

# Test SSH access
ssh root@esxi-01.example.com

# Set NTP (from ESXi shell)
esxcli system ntp set -s ntp1.example.com -s ntp2.example.com
esxcli system ntp set -e yes

# Verify NTP
esxcli system ntp get
esxcli system ntp stats

# Confirm hostname
esxcli system hostname get
```

### Verify Connectivity

From a management workstation:
```bash
ping esxi-01.example.com
nslookup esxi-01.example.com    # Forward DNS
nslookup <esxi-management-ip>   # Reverse DNS
ssh root@esxi-01.example.com
```

Repeat for every host. All must have working forward and reverse DNS before vCenter deployment.

---

## Phase 3 — vCenter Deployment and Initial Configuration

**Exit criterion:** vCenter running, all ESXi hosts added to a cluster object, and basic vCenter services configured.

### Deploy the VCSA

1. Mount the VCSA ISO on a workstation.
2. Run the installer: `vcsa-ui-installer/<platform>/installer`.
3. **Stage 1 — Deploy:** select deployment target (an ESXi host), provide VCSA IP and sizing, set SSO password.
4. **Stage 2 — Setup:** configure NTP, SSH, SSO domain (default: `vsphere.local`), enable CEIP (optional).
5. Wait for deployment to complete (~30 minutes).

### Post-Deployment vCenter Configuration

**From vSphere Client (browser to VCSA IP):**

1. Create a **Datacenter** object.
2. Create a **Cluster** object inside the Datacenter. Do NOT enable vSAN, DRS, or HA at this stage.
3. Add all ESXi hosts to the cluster: right-click cluster → Add Hosts.
4. Accept host thumbprints, enter root credentials for each host.

### License Assignment

```text
vSphere Client → Administration → Licenses → Add License Key
→ assign vSphere + vSAN licenses to cluster and hosts
```

### Configure vCenter NTP

vCenter and all ESXi hosts must be synchronised to the same NTP source. Drift > 500 ms causes vSAN health warnings.

```bash
# Verify vCenter NTP from VCSA shell (SSH as root)
chronyc tracking
# Reference time must match ESXi hosts
```

---

## Phase 4 — dvSwitch and vSAN Network Setup

**Exit criterion:** All hosts have a vSAN vmkernel with MTU 9000 confirmed end-to-end to all peers.

### Create the Distributed Virtual Switch

```text
vSphere Client → Datacenter → Actions → Distributed Switch → New Distributed Switch
→ Name: vDS-Prod
→ Version: match ESXi version
→ Uplinks: 2 (one per physical NIC used for vSAN/vMotion)
→ Default port group: delete (create named groups below)
```

Add all hosts to the dvSwitch and assign physical uplinks:

```text
dvSwitch → Actions → Add and Manage Hosts
→ Add hosts → assign vmnic2 to Uplink 1, vmnic3 to Uplink 2 (adjust for your hardware)
```

### Create Port Groups

| Port Group Name | VLAN | Traffic Type |
|---|---|---|
| PG-vSAN | 100 (example) | vSAN VMkernel |
| PG-vMotion | 200 (example) | vMotion VMkernel |
| PG-Management | 10 (example) | Management (if moving vmk0) |
| PG-VM-Production | 300+ | Virtual machine traffic |

### Create the vSAN VMkernel on Each Host

**From vSphere Client:**

For each host: Host → Configure → Networking → VMkernel adapters → Add Networking

```text
→ Select: Existing distributed port group → PG-vSAN
→ Enable: vSAN traffic service tag
→ IP: static, e.g. 192.168.100.1x/24 (per host)
→ MTU: 9000
```

Or via PowerCLI:

```powershell
$hosts = Get-VMHost -Location (Get-Cluster "VSAN-LON-01")
$dvs = Get-VDSwitch "vDS-Prod"
$pg = Get-VDPortgroup "PG-vSAN"

foreach ($h in $hosts) {
    $hostNum = [int]($h.Name -replace ".*-0*","")
    New-VMHostNetworkAdapter -VMHost $h -VirtualSwitch $dvs `
        -PortGroup $pg -IP "192.168.100.$hostNum" -SubnetMask "255.255.255.0" `
        -Mtu 9000 -VsanTrafficEnabled $true
}
```

### Verify MTU End-to-End

```bash
# From each host — test to every other vSAN vmk IP in the cluster
# Replace IPs with your vSAN VMkernel addresses
vmkping -I vmk2 -d -s 8972 192.168.100.12
vmkping -I vmk2 -d -s 8972 192.168.100.13
vmkping -I vmk2 -d -s 8972 192.168.100.14
# 0% packet loss on all tests = MTU correct end-to-end
```

Any packet loss means MTU 9000 is not configured somewhere in the path (switch port, trunk, uplink). Fix before enabling vSAN.

### Configure NIOC (If Sharing NICs)

If vSAN, vMotion, and VM traffic share the same uplinks, configure Network I/O Control:

```text
dvSwitch → Configure → Network I/O Control → Enable
→ System Traffic → vSAN: set reservation to 50% (minimum)
→ System Traffic → vMotion: set reservation to 25%
```

---

## Phase 5 — vSAN Cluster Enablement

**Exit criterion:** vSAN enabled, disk groups claimed on all hosts, storage policies created, and Skyline Health showing all green.

### Enable vSAN on the Cluster

**From vSphere Client:**

```text
Cluster → Configure → vSAN → Services → Configure
→ Select: Single site cluster (or 2-node / Stretched)
→ Deduplication and Compression: disable for now (enable after validation)
→ Encryption: disable for now (enable after validation)
→ Allow reduced redundancy: leave unchecked
→ Next → claim disks
```

### Claim Disks (OSA)

On the Disk Claim screen, vSAN presents eligible disks per host:

- **Cache tier:** assign the fastest device (NVMe SSD, or SATA SSD for cache). One per disk group.
- **Capacity tier:** assign remaining eligible devices. Up to 7 per disk group.

Best practice: one disk group per host with all eligible disks. Multiple disk groups per host are supported but add management complexity.

```bash
# Verify disk groups created on each host
esxcli vsan storage list | grep -E "Disk Group UUID|Is SSD|Health"
```

### Verify vSAN Cluster Formation

```bash
# Confirm all hosts are cluster members
esxcli vsan cluster get
# All hosts should appear in the member list; one is Master

# Run initial health check
esxcli vsan health cluster get
# All tests should PASS
```

**From vSphere Client:**
Cluster → Monitor → vSAN → Skyline Health — resolve any warnings before proceeding.

### Create Storage Policies

Create the standard policy set before provisioning any VMs:

```powershell
Connect-VIServer <vcenter>

# FTT=1 RAID-5 (4+ nodes) — general workloads
New-SpbmStoragePolicy -Name "VSAN-T2-FTT1-RAID5" `
    -AnyOfRuleSets @(
        New-SpbmRuleSet -AllOfRules @(
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.hostFailuresToTolerate" -Value 1),
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.replicaPreference" -Value "RAID-5")
        )
    )

# FTT=2 RAID-6 (6+ nodes) — Tier-1 databases
New-SpbmStoragePolicy -Name "VSAN-T1-FTT2-RAID6" `
    -AnyOfRuleSets @(
        New-SpbmRuleSet -AllOfRules @(
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.hostFailuresToTolerate" -Value 2),
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.replicaPreference" -Value "RAID-6")
        )
    )

# FTT=1 RAID-1 (3 nodes minimum) — dev/test
New-SpbmStoragePolicy -Name "VSAN-DEV-FTT1-RAID1" `
    -AnyOfRuleSets @(
        New-SpbmRuleSet -AllOfRules @(
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.hostFailuresToTolerate" -Value 1),
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.replicaPreference" -Value "RAID-1")
        )
    )
```

### Enable vSAN Performance Service

```text
Cluster → Configure → vSAN → Services → Performance Service → Enable
```

Without this, performance metrics are not collected and the Performance view in Monitor is empty.

---

## Phase 6 — Aria Suite Lifecycle and Monitoring (Optional)

**Exit criterion:** If Aria Operations is in scope, vSAN adapter configured and dashboards showing cluster data.

This phase is optional — skip if not deploying Aria Operations.

### Deploy Aria Suite Lifecycle Manager

Aria Suite Lifecycle (previously vRealize Suite Lifecycle Manager) is the deployment orchestrator for Aria Operations, Aria Log Insight, and Aria Automation.

1. Deploy Aria Suite Lifecycle OVA to the vSAN datastore.
2. Configure with vCenter credentials.
3. Use Lifecycle Manager to deploy Aria Operations with the appropriate T-shirt size.

### Configure vSAN Adapter in Aria Operations

1. Aria Operations → Administration → Solutions → VMware vSAN → Configure.
2. Add vCenter as a data source — the vSAN adapter pulls metrics automatically.
3. Import the vSAN management pack if not bundled.

### Configure Alert Thresholds

| Metric | Warning | Critical |
|---|---|---|
| vSAN capacity used | 65% | 75% |
| Resync queue (bytes) | > 0 for 2h | > 0 for 8h |
| Object health (non-healthy) | > 0 | > 0 for 30 min |
| Read latency | > 5 ms | > 10 ms |
| Write latency | > 10 ms | > 20 ms |
| Disk SMART errors | Any | Any |

---

## Phase 7 — End-to-End Validation

**Exit criterion:** All checks in this phase pass. Sign off on the deployment and hand to operations.

### Skyline Health — All Green

```text
Cluster → Monitor → vSAN → Skyline Health
→ All categories must show green
→ Resolve every warning before sign-off
```

```bash
# CLI equivalent
esxcli vsan health cluster get | grep -v PASS
# Expected: no output (all tests pass)
```

### Storage Policy Compliance

```powershell
# No VMs should be non-compliant
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" }
# Expected: no output
```

### Disk Group Verification

```bash
# All disk groups healthy, all hosts member of cluster
esxcli vsan cluster get
esxcli vsan storage list | grep -E "Disk Group|Health|State"
```

### MTU Verification (Final Check)

```bash
# From every host to every other host
vmkping -I vmk2 -d -s 8972 <all-other-vsan-vmk-ips>
# 0% loss on all tests
```

### Deploy a Test VM

Provision a test VM on the vSAN datastore using the standard storage policy:

1. Deploy from template or create new VM.
2. Select storage policy `VSAN-T2-FTT1-RAID5`.
3. Power on the VM.
4. Verify storage policy compliance: VM → Monitor → Policies.

### Simulate a Host Failure (Confidence Test)

> **Warning:** Only run on a cluster with no production workloads.

1. Confirm cluster health is green and all objects compliant.
2. Put one host into maintenance mode with **Ensure Accessibility** (simulates an unplanned failure).
3. Verify VMs on that host migrate or remain accessible.
4. Confirm objects show ABSENT but NOT inaccessible.
5. Exit maintenance mode.
6. Confirm resync completes and all objects return to Healthy.

```bash
# Monitor during simulated failure
watch -n 10 "esxcli vsan debug object list | grep -v Healthy | wc -l"
# Count should return to 0 after host exits maintenance
```

### Performance Baseline

Run a baseline I/O test to capture initial performance figures:

```powershell
# Enable performance service (if not already)
# Run from vCenter → Cluster → Monitor → vSAN → Performance
# Record: read latency, write latency, IOPS at idle

# Optional: run HCIBench for a full load test
# Deploy HCIBench OVA → configure test profile → run → export report
```

Store the baseline numbers in a runbook. They become the reference for future troubleshooting.

### Final Sign-Off Checklist

- [ ] All Skyline Health checks green
- [ ] All objects compliant with storage policy
- [ ] MTU 9000 confirmed end-to-end on all hosts
- [ ] NTP synchronised on all hosts and vCenter (< 500 ms drift)
- [ ] DNS forward and reverse resolution working for all hosts
- [ ] Storage policies created: T1-FTT2-RAID6, T2-FTT1-RAID5, DEV-FTT1-RAID1
- [ ] Performance service enabled and collecting metrics
- [ ] Test VM deployed and policy-compliant
- [ ] Simulated failure test passed
- [ ] Performance baseline recorded
- [ ] vSAN HCL compliance confirmed for all disks
- [ ] Capacity headroom > 30% confirmed
- [ ] Monitoring alerts configured (if Aria Operations deployed)
- [ ] Runbook updated with cluster-specific IPs, VLANs, and disk NAAs

---

## See also

- [vSAN — How It Works](../architecture/how-it-works/)
- [vSAN — Health Checks](../operations/health-checks/)
- [vSAN — Common Issues](../troubleshooting/common-issues/)

## Verify

- **Skyline Health:** Cluster → Monitor → vSAN → Skyline Health — all checks green
- **Disk groups:** Cluster → Configure → vSAN → Disk Management — all disk groups Healthy
- **Object compliance:** Cluster → Monitor → vSAN → Virtual Objects — all Compliant
- **Performance service:** Cluster → Monitor → vSAN → Performance — graphs populating within 5 min
