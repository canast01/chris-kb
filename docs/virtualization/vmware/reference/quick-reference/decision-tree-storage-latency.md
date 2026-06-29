---
tags:
  - reference
---
# Decision Tree: Storage Latency

<div class="kb-summary">
Use this when VMs are slow, I/O latency is elevated in monitoring, or vSAN latency alarms trigger.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
               Latency alert / VM storage slow
                              │
                              ▼
               ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
               │ esxtop: GAVG > 20ms?         │
               │ DAVG > 5ms?  KAVG > 2ms?     │
               └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                              │
               ┌────────────────────────────────────────────────── ┼ ──────────────────────────────────────────────────┐
               ▼              ▼              ▼
        ┌───────────────────────────────────────── ┐ ┌────────────┐ ┌ ──────────────────────────────────────────┐
        │ vSAN active│ │ Array      │ │ Network /      │
        │ resync?    │ │ health OK? │ │ HBA fabric?    │
        │ Throttle   │ │ Check ctrl │ │ vmkping vSAN   │
        │ resync     │ │ CPU/queue  │ │ FC HBA stats   │
        └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
               │
               ▼
        ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
        │ Hot-spot VM?  esxtop MBRS/MBWS  │
        │ Snapshot chain > 3 deep?        │
        │ Backup job running against VM?  │
        └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Step 1 — Confirm Latency Baseline Breach

```bash
# On ESXi host — check current device latency
esxtop -b -n 1 | grep -E "DAVG|KAVG|GAVG" | sort -k7 -n -r | head -20
# GAVG (guest average) > 20ms = elevated
# DAVG (device average) > 5ms = elevated
# KAVG (kernel average) > 2ms = kernel queue issues
```


```text title="Expected output"
DAVG   KAVG   GAVG  CMD
   4.32   0.87  18.45  vmhba0
   3.21   1.12  22.67  vmhba1
   2.98   0.65  15.33  vmhba2
   5.67   2.34  28.91  vmhba3
   1.45   0.43   9.12  vmhba4
   6.12   3.21  35.44  vmhba5
   2.87   0.91  12.56  vmhba6
   3.45   1.78  19.23  vmhba7
   4.56   2.12  26.78  vmhba8
   1.23   0.34   8.67  vmhba9
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are running this command directly on an ESXi host (not a vCenter server) with SSH access enabled.
    **`grep: (standard input) is empty`** — The esxtop batch mode may have timed out; try increasing the `-n` value or running esxtop interactively to verify the host is responsive.
Via Aria Operations: vSphere → Datastores → select datastore → Performance → I/O Latency.

## Step 2 — Is vSAN Resync Active?

```bash
esxcli vsan debug resync summary
# If bytes_remaining > 0, resync is ongoing and contributing to latency
```


```text title="Expected output"
Cluster UUID: 52d4a8f0-7c3e-4f2a-9b1e-6a2c8d5f3e1a
Resync Status: In Progress
Bytes remaining: 2147483648
Bytes synced: 8589934592
Resync rate (MB/s): 125.4
Estimated time remaining: 2h 52m
Objects pending: 1247
Disk format version: 13
```

!!! warning "Common errors"
    **`Error: Could not connect to the vSAN service`** — Ensure vSAN is enabled on the cluster and the ESXi host is properly configured with vSAN networking.
    **`Error: Unknown command or namespace`** — Verify the ESXi version supports vSAN debugging commands (vSAN 6.6+) and that vSAN is licensed on this host.
**Active resync causing latency:**
→ Throttle resync: `esxcli vsan debug resync throttle -p 25`
→ Wait for resync to complete before performing additional storage changes
→ If resync is unexpectedly large: check if a disk or host just returned from failure

## Step 3 — Check Storage Array Health

**For vSAN:**
```bash
esxcli vsan health cluster list | grep -v Green   # Disk health warnings?
esxcli vsan debug controller list                  # Controller health?
```


```text title="Expected output"
Cluster UUID                           Health State
52e1a3c4-7f2b-4a1d-9e8c-1b2c3d4e5f6a  Yellow
72f2b4d5-8g3c-5b2e-af9d-2c3d4e5f6g7b  Red

Controller                             Status      Errors
vmhba0                                 Degraded    1
vmhba1                                 Healthy     0
vmhba2                                 Offline     3
vmhba3                                 Healthy     0
```

!!! warning "Common errors"
    **`esxcli: Unknown command or namespace vsan`** — Verify VSAN is licensed and enabled on the cluster; run `esxcli vsan cluster get` to confirm VSAN is active.
    **`grep: command not found`** — Ensure you are running this command directly on an ESXi host shell, not through a remote SSH session with restricted PATH; use full path `/usr/bin/grep` if needed.
**For external storage (NFS/iSCSI/FC):**
- Log in to array management (Unisphere, ONTAP, Pure FlashArray)
- Check array-level latency, queue depth, and controller CPU utilisation
- Check backend disk response time (array-internal metric)

**For Pure FlashArray specifically:**
```bash
# Via REST API or purearray CLI
purearray get   # Throughput and latency summary
```


```text title="Expected output"
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                    PURE STORAGE ARRAY STATUS                                                          │
├─────────────────────────────────────────────────────────────────┤
│ Array Name: FA-405-1a2b3c4d                                                                           │
│ Model: FlashArray//X70-R2                                                                             │
│ Version: 6.4.2.0                                                                                      │
│ Status: Optimal                                                                                       │
├─────────────────────────────────────────────────────────────────┤
│ PERFORMANCE METRICS                                                                                   │
│ Read Throughput:  45,230 MB/s                                                                         │
│ Write Throughput: 38,950 MB/s                                                                         │
│ Read Latency:     0.42 ms                                                                             │
│ Write Latency:    0.58 ms                                                                             │
│ IOPS:             287,450                                                                             │
├─────────────────────────────────────────────────────────────────┤
│ CAPACITY METRICS                                                                                      │
│ Total Capacity:   50.0 TB                                                                             │
│ Used Capacity:    34.2 TB (68.4%)                                                                     │
│ Available:        15.8 TB                                                                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

!!! warning "Common errors"
    **`Error: Connection refused (Connection refused)`** — Verify the array management IP is reachable and the REST API service is running with `purearray list --controllers`.
    **`Error: Invalid credentials (401 Unauthorized)`** — Ensure your API token is valid and not expired; regenerate credentials in the Pure Storage management console.
    **`Error: Command not found: purearray`** — Install the Pure Storage CLI tools or add the installation directory to your system PATH environment variable.
## Step 4 — Check Network / Fabric

For vSAN: high network latency on the vSAN VMkernel can cause I/O latency:
```bash
# Test vSAN network latency between hosts
vmkping -I vmk1 <other-host-vsan-vmk-ip>   # <1ms expected on 10GbE
```


```text title="Expected output"
PING 192.168.100.42 (192.168.100.42): 56 data bytes
64 bytes from 192.168.100.42: icmp_seq=0 time=0.234 ms
64 bytes from 192.168.100.42: icmp_seq=1 time=0.218 ms
64 bytes from 192.168.100.42: icmp_seq=2 time=0.241 ms
64 bytes from 192.168.100.42: icmp_seq=3 time=0.227 ms
64 bytes from 192.168.100.42: icmp_seq=4 time=0.235 ms

--- 192.168.100.42 statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 0.218/0.231/0.241 ms
```

!!! warning "Common errors"
    **`Unknown interface vmk1`** — Verify the vmkernel interface name with `esxcli network ip interface list` and use the correct interface (e.g., vmk0, vmk2).
    **`No route to host`** — Ensure the vSAN network is properly configured and the target host's vSAN vmkernel IP is reachable; check vSAN cluster membership with `esxcli vsan cluster get`.
    **`100% packet loss`** — Confirm the vSAN vmkernel interface is enabled and the network switch/VLAN is properly configured for vSAN traffic.
For FC (iSCSI/FC block storage): check HBA port statistics:
```bash
esxcli storage san fc stats get
# Look for: Link failures, Tx/Rx errors, queue_depth exhaustion
```


```text title="Expected output"
HBA Name: vmhba0
  Link Failures: 0
  Tx Frames: 1247856
  Rx Frames: 1248923
  Tx Bytes: 2156789012
  Rx Bytes: 2158934567
  Tx Errors: 0
  Rx Errors: 0
  Queue Depth: 32
  Queue Depth Exhaustion Events: 0
  Link Speed: 16 Gbps
  Port State: Online

HBA Name: vmhba1
  Link Failures: 2
  Tx Frames: 892341
  Rx Frames: 891256
  Tx Bytes: 1567234891
  Rx Bytes: 1565123456
  Tx Errors: 1
  Rx Errors: 3
  Queue Depth: 32
  Queue Depth Exhaustion Events: 47
  Link Speed: 8 Gbps
  Port State: Online
```

!!! warning "Common errors"
    **`Error: Could not get HBA statistics`** — Verify the HBA is properly detected with `esxcli storage san fc list` and check that FC drivers are loaded.
    **`Permission denied`** — Run the command with root privileges or as a user with administrator role on the ESXi host.
## Step 5 — Check for Hot-Spot VMs

High I/O from a single VM can saturate a datastore or disk group:

```bash
# Identify top I/O consumers
esxtop -b -n 1 | grep -E "Virtual Machine|MBRS|MBWS" | head -20

# Sort by GAVG in esxtop interactive mode: press 'u' → sort by GAVG
```


```text title="Expected output"
GID NAME NWLD %ACTV %BCPU %CCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %PCPU %
```
If a single VM is driving all the I/O:
- Check if the VM has a stuck snapshot (common cause of write amplification)
- Check if a backup job is running hot-backup against this VM right now

## Step 6 — Snapshot Chain

Long snapshot chains dramatically increase latency on writes:

```powershell
Get-VM | Where-Object {$_.ExtensionData.Snapshot} | Get-Snapshot |
    Where-Object {$_.SizeMB -gt 10240} |
    Select-Object VM, Name, Created, SizeMB
```

VMs with snapshot chains > 3 deep or snapshots older than 24 hours during normal operation should be investigated immediately.

## Escalation

If storage latency persists > 30 minutes with no obvious cause:
1. Generate vSAN support bundle: vCenter → Cluster → Monitor → vSAN → Support → Generate Bundle
2. Capture esxtop output: `esxtop -b -n 30 > /tmp/esxtop_$(date +%Y%m%d_%H%M).txt`
3. Open SR with VMware or storage vendor as appropriate
