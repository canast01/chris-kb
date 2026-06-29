---
tags:
  - troubleshooting
  - vmware
  - vsan
  - vsphere-8
search:
  boost: 2
---
# vSAN — Common Issues
![vSAN — Common Issues](../../../../assets/virtualization-vmware-vsan-troubleshooting-common-issues.svg)

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
```bash
esxcli vsan debug resync summary get
# Wait until bytesToSync = 0
```
```d2
direction: right

alert: "Object degraded or absent\n(vSAN health alarm" {shape: rectangle}
checkHost: "checkHost" {shape: rectangle}
restoreHost: "Restore host connectivity\nor power on host" {shape: rectangle}
waitResync: "Wait for vSAN resync\n(clomRepairDelay = 60 min default" {shape: rectangle}
checkDisk: "checkDisk" {shape: rectangle}
diskReplace: "Proceed to disk replacement\n(Procedures → Disk Groups" {shape: rectangle}
checkNet: "checkNet" {shape: rectangle}
fixNet: "Fix network:\nMTU, VLAN, NIC, switch port" {shape: rectangle}
monResync: "Monitor:\nesxcli vsan debug resync summary get" {shape: rectangle}
checkResync: "checkResync" {shape: rectangle}
resolved: "Objects healthy" {shape: rectangle}
checkCap: "checkCap" {shape: rectangle}
freeCap: "Free capacity:\nremove snapshots,\nlower FTT temporarily" {shape: rectangle}
escalate: "Escalate to VMware Support\nwith state capture bundle" {shape: rectangle}

alert -> checkHost
checkHost -> restoreHost
restoreHost -> waitResync
checkHost -> checkDisk
checkDisk -> diskReplace
diskReplace -> waitResync
checkDisk -> checkNet
checkNet -> fixNet
fixNet -> waitResync
checkNet -> waitResync
waitResync -> monResync
monResync -> checkResync
checkResync -> resolved
checkResync -> checkCap
checkCap -> freeCap
freeCap -> monResync
checkCap -> escalate
```
```bash
# Find degraded/absent objects
esxcli vsan debug object list | grep -v "Healthy"

# Get detail on a specific object UUID
esxcli vsan debug object get -u <object-uuid>

# Check which host/disk the absent components are on
esxcli vsan debug component list | grep -i absent
```
```bash
esxcli vsan debug network test
# Loss % > 0 indicates network issues — check switch, NIC, or vDS configuration
```
```bash
# Check object state
esxcli vsan debug object list | grep -i "inaccessible"

# Check host count in cluster
esxcli vsan cluster get | grep -i "member"

# Network partition test
esxcli vsan debug network test
```
```bash
# Check and remove throttle (if set too low)
esxcli vsan debug resync throttle get
esxcli vsan debug resync throttle set --throttle 0  # unlimited

# Check capacity
esxcli vsan storage list

# Identify blocked components
esxcli vsan debug object list | grep -i "stale\|absent"
```
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
```d2
direction: right

highLat: "High vSAN latency detected\n(> 10 ms read / > 20 ms write" {shape: rectangle}
checkNet: "checkNet" {shape: rectangle}
fixMTU: "Fix MTU end-to-end\n(switch, vDS, vmk adapter = 9000" {shape: rectangle}
resolved: "Latency normal" {shape: rectangle}
checkResync: "checkResync" {shape: rectangle}
throttle: "Throttle resync during\nbusiness hours:\nesxcli vsan debug resync\nthrottle set --throttle 500" {shape: rectangle}
checkCap: "checkCap" {shape: rectangle}
freeCap: "Free capacity:\ndelete snapshots,\nexpand cluster" {shape: rectangle}
checkDisk: "checkDisk" {shape: rectangle}
replaceDisk: "Replace failed\nhardware" {shape: rectangle}
checkCPU: "checkCPU" {shape: rectangle}
vMotion: "vMotion high-IOPS\nVMs to less-loaded hosts" {shape: rectangle}
openCase: "Escalate to VMware\nSupport" {shape: rectangle}

highLat -> checkNet
checkNet -> fixMTU
fixMTU -> resolved
checkNet -> checkResync
checkResync -> throttle
throttle -> resolved
checkResync -> checkCap
checkCap -> freeCap
freeCap -> resolved
checkCap -> checkDisk
checkDisk -> replaceDisk
replaceDisk -> resolved
checkDisk -> checkCPU
checkCPU -> vMotion
vMotion -> resolved
checkCPU -> openCase
```
```bash
# Per-disk I/O stats (IOPS, latency)
esxcli vsan storage stats get

# vSAN congestion indicator — should be 0
esxcli vsan debug vmdk list

# Check vSAN network latency
vmkping -I vmk2 -d -s 8972 <peer_vmk_ip>
```
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
```bash
esxcli vsan debug network test
# Packet loss to one or more hosts
```
```bash
esxcli vsan storage list | grep "Format Version"
```
```bash
# Check clock on each host
esxcli system time get

# NTP status
esxcli system ntp get
ntpq -p
```
```powershell
# List non-compliant VMs
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" } |
    Select Entity, StoragePolicy, ComplianceStatus
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What triggered the alert?" {shape: rectangle}
A: "Object DEGRADED\nor ABSENT" {shape: rectangle}
B: "Capacity alarm\n≥ 70 / 80%" {shape: rectangle}
C: "Skyline Health\ncheck failing" {shape: rectangle}
D: "Resync stuck\nor very slow" {shape: rectangle}
E: "VM storage\npolicy non-compliant" {shape: rectangle}
A1: "A1" {shape: rectangle}
A2: "Restore host first\n— wait for rebuild\n→ Object Health section" {shape: rectangle}
A3: "A3" {shape: rectangle}
A4: "Replace disk\n→ Disk Group Failure section" {shape: rectangle}
A5: "Check network\npartition / witness" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "Clean snapshots\ncheck dedup savings\n→ Capacity section" {shape: rectangle}
B3: "Escalate immediately\nStorage vMotion or\nadd capacity" {shape: rectangle}
C1: "Identify specific\nfailing check\n→ Health Checks section" {shape: rectangle}
D1: "Check resync throttle\nand available bandwidth\n→ Resync section" {shape: rectangle}
E1: "Run policy compliance\ncheck + remediate\n→ Policy Compliance section" {shape: rectangle}

S -> A
S -> B
S -> C
S -> D
S -> E
A1 -> A2
A3 -> A4
A3 -> A5
B1 -> B2
B1 -> B3
C -> C1
D -> D1
E -> E1
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## See also

- [vSAN Cluster Health — Internals](../../../internals/vsan-cluster-health/)
- [vSAN — Operations](../../operations/)
- [Scenarios — vSAN Disk Failure](../../../topics/scenarios/vsan-disk-component-failure/)

---

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
