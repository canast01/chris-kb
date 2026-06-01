# vSAN — Common Issues


<div class="kb-summary">
Reference for the most frequently encountered vSAN problems. Each entry includes symptoms, diagnostic steps, and resolution actions.
</div>

---

## Quick Diagnostics Checklist

Run this sequence first for any vSAN incident before diving into specific issue categories:

```bash
# 1. Cluster membership and overall status
esxcli vsan cluster get

# 2. Health check summary (all built-in checks)
esxcli vsan health cluster list

# 3. Object health — filter for non-healthy
esxcli vsan debug object list | grep -v "Healthy"

# 4. Active resync operations
esxcli vsan debug resync summary get

# 5. Disk group status
esxcli vsan storage list

# 6. Network connectivity between hosts
esxcli vsan debug network test
```
```text
┌──────────────────────────────────────── vSAN — Common Issues ─────────────────────────────────────────┐
│                                                                                                       │
│  Common vSAN issues: degraded components, resync stalls, disk failures, network                       │
│  latency causing I/O aborts, capacity alarms, and policy non-compliance.                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Degraded Components              │  │                Resync Stalls                │   │
│   │            Symptom: health UI red            │  │         Resync bytes not decreasing         │   │
│   │           Check: disk SMART errors           │  │          Check: host in maint mode          │   │
│   │           Fix: replace failed disk           │  │             Fix: exit maint mode            │   │
│   │         60-min timer before rebuild          │  │            Bandwidth limit: raise           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Degraded = policy at risk; check health UI immediately; resync removes the risk.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Network & I/O Issues             │  │           Capacity & Policy Issues          │   │
│   │        I/O abort: check MTU mismatch         │  │             Capacity >70%: alert            │   │
│   │        Latency spike: resync traffic         │  │           Non-compliant: re-apply           │   │
│   │           MTU test: vSAN health UI           │  │          Dedup savings gone: expand         │   │
│   │         NIC team fail: check uplinks         │  │           Stretched: witness down           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Most issues trace to: disk SMART failure, network MTU mismatch, host in maintenance,                 │
│  or capacity >70%; check all four before deep investigation.                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Degraded      = replica lost; policy not met; data at risk                                           │
│  Absent        = component missing <60min; vSAN waits before rebuilding                               │
│  60-min timer  = vSAN delay before treating absent as degraded                                        │
│  SMART error   = disk pre-failure indicator; replace proactively                                      │
│  MTU mismatch  = jumbo frames not configured end-to-end; causes I/O errors                            │
│  Resync BW     = configurable limit; default 128Mbps; raise for faster rebuild                        │
│  Policy non-compliant= VM does not meet FTT policy; fix = re-apply policy                             │
│  Witness down  = stretched cluster loses quorum; VMs may stall                                        │
│  NIC team fail = check uplink status on vDS; failover should be automatic                             │
│  Dedup savings = dedup ratio drops when data is incompressible                                        │
│  I/O abort     = VM I/O fails; check vSAN health for root cause                                       │
│  Capacity 70%  = alert threshold; keep 30% free for resync headroom                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

### Why VMs Slow Down During Resync

When a disk or host fails, vSAN rebuilds data across the remaining hosts. This puts extra I/O load on those hosts until the rebuild completes.

```text
Normal vSAN:
Host 1 ──── data copy 1
Host 2 ──── data copy 2  ← redundancy
Host 3 ──── data copy 3

If Host 2 goes down or a disk fails:
Host 1 ──── data copy 1
Host 2 ──── REBUILDING ← resync happening
Host 3 ──── data copy 3
              │
              └── heavy I/O on remaining hosts
                  → VM performance suffers
```

Monitor resync progress:
```bash
esxcli vsan debug resync summary get
# Wait until bytesToSync = 0
```

---

## Degraded Object Recovery Flow

```mermaid
graph TD
    alert(["Object degraded or absent\n(vSAN health alarm)"])
    checkHost{"Is a host\noffline?"}
    restoreHost["Restore host connectivity\nor power on host"]
    checkDisk{"Is a disk group\noffline / failed?"}
    checkNet{"Does network test\nshow packet loss?"}
    fixNet["Fix network:\nMTU, VLAN, NIC, switch port"]
    diskReplace["Proceed to disk replacement\n(Procedures → Disk Groups)"]
    waitResync["Wait for vSAN resync\n(clomRepairDelay = 60 min default)"]
    monResync["Monitor:\nesxcli vsan debug resync summary get"]
    checkResync{"Resync completing\nwithin 24 hours?"}
    checkCap{"Cluster capacity\n> 70%?"}
    freeCap["Free capacity:\nremove snapshots,\nlower FTT temporarily"]
    escalate["Escalate to VMware Support\nwith state capture bundle"]
    resolved(["Objects healthy"])

    alert --> checkHost
    checkHost -->|"Yes"| restoreHost --> waitResync
    checkHost -->|"No"| checkDisk
    checkDisk -->|"Yes"| diskReplace --> waitResync
    checkDisk -->|"No"| checkNet
    checkNet -->|"Yes"| fixNet --> waitResync
    checkNet -->|"No"| waitResync
    waitResync --> monResync --> checkResync
    checkResync -->|"Yes"| resolved
    checkResync -->|"Stalled"| checkCap
    checkCap -->|"Yes"| freeCap --> monResync
    checkCap -->|"No"| escalate

    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff

    class checkHost,checkDisk,checkNet,checkResync,checkCap decision
    class restoreHost,fixNet,diskReplace,waitResync,monResync,freeCap,escalate action
    class alert,resolved terminal
```

## Object Degraded or Absent

**Symptoms:**
- vSAN health shows "Object health issues"
- VMs running slowly or with I/O errors
- vCenter alerts: "vSAN object health alarm"

**Cause:** One or more object components (portions of a VMDK or VM namespace) are on a host or disk that is offline, removed, or failed.

**Diagnosis:**

```bash
# Find degraded/absent objects
esxcli vsan debug object list | grep -v "Healthy"

# Get detail on a specific object UUID
esxcli vsan debug object get -u <object-uuid>

# Check which host/disk the absent components are on
esxcli vsan debug component list | grep -i absent
```

**Resolution steps:**

1. Check if a host is offline or disconnected in vCenter. If so, restore host connectivity.
2. If host is online, check disk group health: `esxcli vsan storage list | grep -E "Health|State"`.
3. If a disk has failed, proceed to disk replacement (see Procedures → Disk Groups).
4. After hardware is restored, vSAN will automatically rebuild absent components. Monitor resync:
   ```bash
   esxcli vsan debug resync summary get
   ```
5. If resync does not start within 60 minutes (default `clomRepairDelay`), check if capacity is available:
   ```powershell
   Get-VsanSpaceUsage -Cluster (Get-Cluster "VSAN-LON-01")
   ```

**If no hardware failure — check for network partition:**

```bash
esxcli vsan debug network test
# Loss % > 0 indicates network issues — check switch, NIC, or vDS configuration
```

---

## Inaccessible VM Objects

**Symptoms:**
- VM is in an "Invalid" or "Inaccessible" state in vCenter
- Attempts to power on the VM fail with "Cannot open the disk"
- All VMDK files appear inaccessible

**This is a critical condition.** An inaccessible object means no component is readable — the VM cannot function.

**Causes:**
- Multiple simultaneous host or disk failures exceeding the FTT policy
- Complete network partition isolating all components of an object
- vSAN cluster without quorum (fewer hosts than FTT+1 are reachable)

**Diagnosis:**

```bash
# Check object state
esxcli vsan debug object list | grep -i "inaccessible"

# Check host count in cluster
esxcli vsan cluster get | grep -i "member"

# Network partition test
esxcli vsan debug network test
```

**Resolution:**

1. Restore all hosts to the cluster. If a host is down, bring it back online.
2. If hosts are online but the object is still inaccessible, check CMMDS partition:
   ```bash
   esxcli vsan debug object list --all | grep -i "CMMDS"
   ```
3. If the cluster has split-brain (two groups of hosts cannot see each other), restore network connectivity between the partitioned groups.
4. If no hardware or network fault is found, open a VMware support case — do not attempt to force-open inaccessible objects without VMware guidance.

---

## Resync Not Completing

**Symptoms:**
- Resync has been running for > 24 hours without visible progress
- `esxcli vsan debug resync summary get` shows bytes remaining unchanged across multiple checks

**Causes:**

| Cause | Check |
|---|---|
| Insufficient capacity for rebuild | `Get-VsanSpaceUsage` — is cluster > 70% full? |
| Throttle too low | `esxcli vsan debug resync throttle get` — is throttle set to a very low value? |
| Another host in maintenance | More than one host offline during rebuild — not enough capacity |
| Degraded disk group on target host | Target host has a failed disk group — cannot receive data |
| Network issues | `esxcli vsan debug network test` — packet loss on vSAN network? |

**Resolution:**

```bash
# Check and remove throttle (if set too low)
esxcli vsan debug resync throttle get
esxcli vsan debug resync throttle set --throttle 0  # unlimited

# Check capacity
esxcli vsan storage list

# Identify blocked components
esxcli vsan debug object list | grep -i "stale\|absent"
```

If resync is blocked due to capacity, consider:
- Deleting stale snapshots to free space.
- Temporarily changing some VMs to a lower FTT policy.
- Adding capacity disks or hosts.

---

## Disk Group Fails to Come Online

**Symptoms:**
- ESXi host shows a disk group as "Degraded" or offline
- VMs on that host show degraded objects
- vSAN health shows disk-related failures

**Causes:**
- Cache SSD has failed
- All-flash capacity disk has failed and the group is below minimum disk count
- Disk controller firmware/driver issue
- Disk was removed without evacuation

**Diagnosis:**

```bash
# Check disk group and disk status
esxcli vsan storage list

# Check for hardware errors on the disk
esxcli storage core device list | grep <naa>

# Check disk controller driver version
esxcli software vib list | grep -i <controller-vendor>

# VMkernel log — disk errors
grep -i "scsi\|disk\|naa" /var/log/vmkernel.log | grep -i "error\|fail" | tail -30
```

**Resolution:**

1. If cache SSD failed: replace the SSD and recreate the disk group.
2. If capacity disk failed: remove the failed disk, replace it, and add it back.
3. If driver version mismatch: check HCL and update to certified driver via vLCM.
4. If disk was removed without evacuation: add it back physically — if data is still intact, vSAN will recognise it and rebuild. If the disk is gone, proceed with adding a new disk and allow rebuild.

---

## High vSAN Latency

**Symptoms:**
- VM I/O latency above normal baseline
- Application timeouts or slowness
- vCenter performance charts show high vSAN read or write latency

```mermaid
graph TD
    highLat(["High vSAN latency detected\n(> 10 ms read / > 20 ms write)"])
    checkNet{"vmkping -d -s 8972\npeer succeeds?"}
    fixMTU["Fix MTU end-to-end\n(switch, vDS, vmk adapter = 9000)"]
    checkResync{"Active resync\nin progress?"}
    throttle["Throttle resync during\nbusiness hours:\nesxcli vsan debug resync\nthrottle set --throttle 500"]
    checkCap{"Cluster capacity\n> 80%?"}
    freeCap["Free capacity:\ndelete snapshots,\nexpand cluster"]
    checkDisk{"Disk group\nhealthy?"}
    replaceDisk["Replace failed\nhardware"]
    checkCPU{"Host CPU\ncongestion?"}
    vMotion["vMotion high-IOPS\nVMs to less-loaded hosts"]
    openCase["Escalate to VMware\nSupport"]
    resolved(["Latency normal"])

    highLat --> checkNet
    checkNet -->|"No / packet loss"| fixMTU --> resolved
    checkNet -->|"Yes"| checkResync
    checkResync -->|"Yes"| throttle --> resolved
    checkResync -->|"No"| checkCap
    checkCap -->|"Yes"| freeCap --> resolved
    checkCap -->|"No"| checkDisk
    checkDisk -->|"Degraded"| replaceDisk --> resolved
    checkDisk -->|"Healthy"| checkCPU
    checkCPU -->|"Yes"| vMotion --> resolved
    checkCPU -->|"No"| openCase

    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff

    class checkNet,checkResync,checkCap,checkDisk,checkCPU decision
    class fixMTU,throttle,freeCap,replaceDisk,vMotion,openCase action
    class highLat,resolved terminal
```

**Diagnosis:**

```bash
# Per-disk I/O stats (IOPS, latency)
esxcli vsan storage stats get

# vSAN congestion indicator — should be 0
esxcli vsan debug vmdk list

# Check vSAN network latency
vmkping -I vmk2 -d -s 8972 <peer_vmk_ip>
```

**Common causes and resolution:**

| Cause | Check | Fix |
|---|---|---|
| Cache tier full (OSA) | Cache SSD usage | Add more cache SSDs or reduce write-heavy workloads |
| Capacity near full (> 80%) | `Get-VsanSpaceUsage` | Expand capacity or delete data |
| Snapshots consuming capacity | `Get-Snapshot` | Consolidate snapshots |
| Network MTU mismatch | `vmkping -d -s 8972` fails | Fix switch MTU end-to-end |
| Active resync consuming bandwidth | `esxcli vsan debug resync summary get` | Throttle resync |
| CPU congestion on host | vCenter host performance charts | Check VM density — consider vMotion |
| Disk group degraded | `esxcli vsan storage list` | Replace failed hardware |

---

## vSAN Network Issues

**Symptoms:**
- vSAN health check: "vSAN cluster partition" — warning or critical
- Hosts showing as disconnected from the vSAN cluster
- High back-end latency despite healthy disks

**Diagnosis:**

```bash
# Test network connectivity to all peers
esxcli vsan debug network test

# List vSAN VMkernel adapters
esxcli vsan network list

# Verify MTU
vmkping -I vmk2 -d -s 8972 <peer_vmk_ip>
# Failure = MTU mismatch along the path

# Check unicast agent list
esxcli vsan network ipconfig list
# All cluster host vSAN vmk IPs should appear as unicast agents
```

**Resolution:**

| Issue | Fix |
|---|---|
| MTU mismatch | Set vDS port group MTU to 9000; set physical switch port MTU to 9000; set vmkernel adapter MTU to 9000 |
| Missing vSAN tag on vmkernel | `esxcli network ip interface tag add -i vmk2 -t VSAN` |
| Unicast agents missing | vCenter will repopulate automatically — verify vSAN vmkernel is on the correct VLAN |
| Packet loss | Check physical NIC health, switch errors, duplex/speed mismatch |
| Wrong VLAN on vSAN port group | Correct port group VLAN — all hosts must be on the same vSAN VLAN |

---

## Capacity Spike — Unexpected Utilisation

**Symptoms:**
- Capacity utilisation increases rapidly without new VMs being deployed
- vSAN health shows "Disk space low" warning
- vCenter capacity chart shows large gap between provisioned and physical capacity

**Common causes:**

```powershell
# 1. Find VMs with large snapshots
Get-VM | Get-Snapshot | Select VM, Name, SizeGB, Created |
    Sort-Object SizeGB -Descending | Format-Table -AutoSize

# 2. Find VMs with large swap files (memory overhead)
# vSAN swap files equal the VM's configured RAM size
Get-VM | Select Name, MemoryGB | Sort-Object MemoryGB -Descending | Select -First 20

# 3. Find VMs with thick-provisioned disks in thin-by-default policies
Get-HardDisk -VM * | Where-Object { $_.StorageFormat -eq "Thick" } |
    Select Parent, Name, CapacityGB, StorageFormat
```

**Resolution:**

1. Consolidate stale snapshots:
   ```powershell
   Get-VM | Where-Object { (Get-Snapshot -VM $_).Count -gt 0 } |
       ForEach-Object { Remove-Snapshot -VM $_ -RemoveChildren -Confirm:$false }
   ```
2. Review oversized VM memory allocations — unnecessary RAM results in large vSAN swap objects.
3. If thin VMs are ballooning (guest OS writing large files), investigate application activity.

---

## vSAN Health Check Failures

### Cluster Partition

Indicates one or more hosts are in a different partition (cannot see other hosts via the vSAN network).

```bash
esxcli vsan debug network test
# Packet loss to one or more hosts
```

Fix: Restore vSAN network connectivity between affected hosts.

### Disk Format Version Mismatch

```bash
esxcli vsan storage list | grep "Format Version"
```

All hosts must be on the same vSAN disk format version. After cluster upgrade, trigger format upgrade:
vSphere Client → Cluster → Configure → vSAN → Advanced Options → Upgrade Disk Format

### Time Drift

```bash
# Check clock on each host
esxcli system time get

# NTP status
esxcli system ntp get
ntpq -p
```

Fix: Ensure NTP is configured and syncing. Clock drift > 500 ms causes CMMDS partitioning.

### vSAN Build Recommendation Engine (HCL Check)

HCL check fails when disk controller, SSD, or driver is not on the vSAN HCL.

Fix: Check [Broadcom vSAN HCL](https://www.vmware.com/resources/compatibility/search.php?deviceCategory=vsansd) and align hardware/drivers. Update drivers via vLCM.

---

## Storage Policy Non-Compliance

**Symptoms:**
- vCenter vSAN Virtual Objects shows VMs as "Non-compliant"
- vSAN health: "vSAN object health — non-compliant"

**Diagnosis:**

```powershell
# List non-compliant VMs
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" } |
    Select Entity, StoragePolicy, ComplianceStatus
```

**Common causes:**

| Cause | Resolution |
|---|---|
| FTT policy requires more hosts than available | Reduce FTT or add hosts |
| RAID-5/6 requires 4+ or 6+ hosts | Ensure cluster meets minimum host count |
| Disk group failure reduces available fault domains | Repair disk group first |
| Capacity insufficient for current policy | Free capacity or expand cluster |
| Policy changed but resync not yet complete | Allow resync to complete — non-compliance is temporary |

After resolving the root cause, vSAN automatically re-evaluates compliance and starts resync to meet the policy. Monitor in vCenter → Cluster → Monitor → vSAN → Resyncing Objects.
