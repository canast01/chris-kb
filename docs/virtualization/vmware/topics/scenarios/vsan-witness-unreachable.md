---
tags:
  - scenarios
  - vmware
  - vsan
  - vsphere-8
---
# vSAN 2-Node — Witness Host Unreachable

<div class="kb-summary">
In a 2-node vSAN cluster, the witness host provides the tiebreaker vote for quorum. When the witness
loses connectivity, the cluster degrades silently — VMs continue running as long as both data nodes are
healthy, but the cluster cannot tolerate a simultaneous data-node failure. This scenario covers detecting
witness loss, restoring connectivity or the witness host, and applying a temporary workaround to prevent
unnecessary data rebuilds while the witness is being restored.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: right

D1: "D1" {shape: rectangle}
D2: "D2" {shape: rectangle}
W: "W" {shape: rectangle}
LOST: "Witness partition detected · vSAN health: red" {shape: rectangle}
RISK: "Risk window: if one data node fails · quorum lost\n— objects inaccessible" {shape: rectangle}
ACTION: "Restore witness connectivity · or restart witness\nVM/host" {shape: rectangle}
HEAL: "vSAN self-heals on reconnect · o manual rebuild needed" {shape: rectangle}

D1 -> D2
D1 -> W
D2 -> W
W -> LOST
LOST -> RISK
LOST -> ACTION
ACTION -> HEAL
```

## Symptoms

| Indicator | Detail |
|---|---|
| vSAN Health | "Witness host component health" = red under `Monitor → vSAN → Health Service` |
| vSAN Health | "Component metadata health" may show degraded or absent witness components |
| `esxcli` output | `esxcli vsan debug object list` shows witness components in ABSENT state |
| Cluster still running | VMs remain accessible if both data nodes are healthy (FTT=1 satisfied with 2 data copies) |
| Hostd log | `/var/log/hostd.log` on witness shows repeated heartbeat timeout messages |

---

## 1. Confirm Witness Is Disconnected

Run on either data node:

```bash
esxcli vsan cluster list
```


```text title="Expected output"
Cluster UUID                 Cluster Name
--------------------------  -----------
52d4a8f1-7c2e-4d9a-b1e3-   vsan-prod-01
9f2c1a8e-5b3d-4f7a-c2e1-   vsan-dev-cluster
a7f3c1d2-8e4b-5g8h-d3f2-   vsan-backup-pool
```

!!! warning "Common errors"
    **`Error: Could not connect to the host. Verify the host name, port, and credentials.`** — Verify the ESXi host is reachable and you have valid credentials configured in your vSphere client or SSH session.
    **`Error: vSAN is not enabled on this cluster.`** — Enable vSAN on the cluster through vCenter Server under Cluster Settings > vSAN > General.
    **`Error: Permission denied. User does not have required privileges.`** — Ensure your vSphere user account has the "Host.Config.Storage" privilege or equivalent vSAN administrator role.
Output shows 3 members when healthy. With witness unreachable, the witness UUID appears as disconnected
or absent from the member list:

```text
Cluster Information
   Enabled: true
   Current master UUID: <data-node-uuid>
   Local node UUID: <data-node-uuid>
   Local node type: NORMAL
   Local node state: MASTER
   Local node health state: HEALTHY
   Sub-Cluster Master UUID: <data-node-uuid>
   Sub-Cluster Backup UUID: <data-node-uuid>
   Sub-Cluster UUID: <cluster-uuid>
   Sub-Cluster Membership Entry Revision: 5
   Sub-Cluster Member Count: 2       <-- only 2 when witness is gone
   Sub-Cluster Member UUIDs: <node-a-uuid> <node-b-uuid>
```

---

## 2. Check Network Connectivity to Witness

From a data node, ping the witness TEP and management IPs:

```bash
# Ping witness management IP from data node management VMkernel
vmkping -I vmk0 <witness-mgmt-ip>

# Ping witness TEP from data node vSAN VMkernel
vmkping -I vmk1 <witness-tep-ip>
```


```text title="Expected output"
PING 192.168.100.45 (192.168.100.45): 56 data bytes
64 bytes from 192.168.100.45: icmp_seq=0 ttl=64 time=2.341 ms
64 bytes from 192.168.100.45: icmp_seq=1 ttl=64 time=2.156 ms
64 bytes from 192.168.100.45: icmp_seq=2 ttl=64 time=2.289 ms
64 bytes from 192.168.100.45: icmp_seq=3 ttl=64 time=2.204 ms
64 bytes from 192.168.100.45: icmp_seq=4 ttl=64 time=2.318 ms

PING 172.16.50.78 (172.16.50.78): 56 data bytes
64 bytes from 172.16.50.78: icmp_seq=0 ttl=64 time=1.892 ms
64 bytes from 172.16.50.78: icmp_seq=1 ttl=64 time=1.756 ms
64 bytes from 172.16.50.78: icmp_seq=2 ttl=64 time=1.834 ms
64 bytes from 172.16.50.78: icmp_seq=3 ttl=64 time=1.923 ms
64 bytes from 172.16.50.78: icmp_seq=4 ttl=64 time=1.778 ms
```

!!! warning "Common errors"
    **`PING 192.168.100.45 (192.168.100.45): 56 data bytes No answer from icmp_seq=0`** — Verify witness management IP is correct and witness appliance is powered on and reachable on the management network.
    **`Unknown interface vmk1`** — Confirm vmk1 (vSAN VMkernel interface) exists on the data node using `esxcli network ip interface list`.
If pings fail to the TEP (vmk1) but succeed to management (vmk0), the vSAN witness traffic VLAN or
routing is broken. If both fail, the witness host or VM is down.

---

## 3. Audit Affected Objects

```bash
esxcli vsan debug object list --cluster-uuid <cluster-uuid> 2>/dev/null | grep -E "ABSENT|DEGRADED"
```


```text title="Expected output"
Object UUID                          State      Policy
52a4c8f1-2b3e-4f9a-8c1d-7e9f2a3b4c5d DEGRADED   raid1 (2) - 1 component missing
63b5d9g2-3c4f-5g0b-9d2e-8f0g3b4c5d6e ABSENT     raid5 (4) - stripe offline
74c6e0h3-4d5g-6h1c-0e3f-9g1h4c5d6e7f DEGRADED   raid1 (2) - 1 replica unhealthy
85d7f1i4-5e6h-7i2d-1f4g-0h2i5d6e7f8g ABSENT     raid6 (6) - multiple components down
96e8g2j5-6f7i-8j3e-2g5h-1i3j6e7f8g9h DEGRADED   raid1 (2) - witness absent
```

!!! warning "Common errors"
    **`error: Unknown option or set of options: --cluster-uuid`** — Verify the VSAN cluster UUID format and ensure you're running this command on an ESXi host with VSAN enabled; use `esxcli vsan cluster get` to confirm VSAN is active.
    **`error: Unknown command or namespace`** — Confirm the ESXi host version supports `esxcli vsan debug object list` (requires vSAN 6.0+); check with `esxcli system version get`.
Objects with only witness components ABSENT are tolerable (VMs still running). Objects with a data
component ABSENT are at risk — a second failure causes immediate inaccessibility.

To get the cluster UUID:

```bash
esxcli vsan cluster list | grep "Sub-Cluster UUID"
```


```text title="Expected output"
Sub-Cluster UUID: 52e84d1a-c4f2-4e8b-9f3a-7b2c1d9e4f6a
Sub-Cluster UUID: 7f3a2b1c-9e4d-4f8b-3c2a-1d9e4f6a5b2c
```

!!! warning "Common errors"
    **`Unknown command or namespace vsan.cluster.list`** — Verify vSAN is licensed and enabled on the cluster by running `esxcli vsan cluster get`.
    **`grep: (standard input) has no data`** — The vsan cluster list command returned no output; confirm the host is part of an active vSAN cluster with `esxcli vsan cluster get`.
---

## 4. Review Witness Logs

SSH to the witness host (if reachable via management network):

```bash
grep -i "heartbeat" /var/log/hostd.log | tail -30
grep -i "vsan" /var/log/vmkernel.log | grep -i "partition\|disconnect\|timeout" | tail -30
```


```text title="Expected output"
2024-01-15T09:23:47.123Z [INFO] Heartbeat from host esx-prod-02.corp.local (192.168.1.42) received successfully
2024-01-15T09:24:12.456Z [WARN] Heartbeat timeout detected for host esx-prod-03.corp.local after 60 seconds
2024-01-15T09:25:03.789Z [INFO] Heartbeat restored from host esx-prod-03.corp.local
2024-01-15T09:26:45.234Z [ERROR] Heartbeat failure: network partition detected on vSAN cluster member esx-prod-04
2024-01-15T09:27:18.567Z [INFO] Heartbeat interval: 1000ms, threshold: 3 missed beats
2024-01-15T09:28:52.891Z [WARN] vSAN partition event: node esx-prod-02 isolated from quorum
2024-01-15T09:29:30.145Z [ERROR] vSAN disk disconnect: device mpx.vmhba2:C0:T1:L0 marked offline
2024-01-15T09:30:15.678Z [INFO] vSAN timeout recovery: resyncing objects on esx-prod-03
2024-01-15T09:31:42.234Z [WARN] vSAN partition healed: cluster quorum restored
2024-01-15T09:32:08.901Z [INFO] Heartbeat acknowledgment from all 4 cluster nodes confirmed
```

!!! warning "Common errors"
    **`grep: /var/log/hostd.log: No such file or directory`** — Verify the ESXi host is running and the log file exists; check with `ls -la /var/log/hostd.log`.
    **`grep: /var/log/vmkernel.log: Permission denied`** — Run the command with appropriate privileges or SSH directly to the ESXi host as root.
Look for repeated entries:

```text
WARNING: Heartbeat to cluster master lost (attempt 3 of 3)
ERROR: vSAN witness partition: unable to reach data nodes on vmk_witness
```

---

## 5. Resolution

### Network Partition — Restore L2/L3 Connectivity

If the witness host is running but isolated by a network change:

1. Identify the network segment carrying witness traffic (typically a dedicated VLAN or routed subnet).
2. Check switch port state, VLAN membership, and any firewall/ACL changes applied to the witness subnet.
3. Restore connectivity — vSAN self-heals automatically once the witness rejoins. No manual object
   rebuild is required.
4. Confirm in `esxcli vsan cluster list` that member count returns to 3.

### Witness VM or Host Down — Power On

If using the VMware vSAN Witness Appliance (OVA-deployed VM):

```bash
# Via vCenter or directly on the vSphere cluster hosting the witness VM
Get-VM -Name "vSAN-Witness-*" | Start-VM
```


```text title="Expected output"
Name                 PowerState Num CPUs MemoryGB
----                 ---------- -------- --------
vSAN-Witness-01      PoweredOn   2        4
vSAN-Witness-02      PoweredOn   2        4
vSAN-Witness-03      PoweredOn   2        4
```

!!! warning "Common errors"
    **`Get-VM : The term 'Get-VM' is not recognized as the name of a cmdlet, function, script file, or operable program.`** — Import the VMware.VimAutomation.Core module with `Import-Module VMware.VimAutomation.Core` before running the command.
    **`Get-VM : Cannot find VM with name matching pattern 'vSAN-Witness-*'.`** — Verify the witness VM naming convention matches your environment and confirm the VMs exist with `Get-VM | Where-Object {$_.Name -like "*Witness*"}`.
After power-on, allow 2–3 minutes for ESXi services and vSAN witness participation to initialise
before checking cluster membership.

### Witness Disk Full — Expand Datastore

Witness appliance needs ~10 GB minimum for component metadata. Check:

```bash
df -h   # run on witness ESXi via SSH
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       4.6G  2.1G  2.5G  46% /
/dev/sdb1       558G  312G  246G  56% /vmfs/volumes/datastore1
/dev/sdc1       1.8T  1.2T  600G  67% /vmfs/volumes/datastore2
vfat            286M  128M  158M  45% /boot
tmpfs           8.0G  512M  7.5G   6% /tmp
```

!!! warning "Common errors"
    **`Permission denied`** — Ensure your SSH user has root or equivalent privileges on the ESXi host, or prepend the command with `sudo`.
    **`Connection refused`** — Verify SSH is enabled on the ESXi host (Configuration > Security Profile > Services > SSH) and the hostname/IP is correct.
If the witness datastore is full, expand the witness VM disk via vSphere Client and extend the
filesystem inside the witness appliance:

```bash
# On witness ESXi — rescan storage
esxcli storage core adapter rescan --all
```


```text title="Expected output"
HBA vmhba0 rescan started.
HBA vmhba1 rescan started.
HBA vmhba2 rescan started.
HBA vmhba3 rescan started.
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace storage core adapter rescan`** — Verify the ESXi version supports esxcli storage commands; some older versions require `esxcfg-rescan` instead.
    **`Error: Unable to acquire lock on /var/lock/vmkiscsi.lock`** — Wait for any ongoing storage operations to complete or restart the hostd service with `services.sh restart`.
### Temporary Workaround — Defer Rebuild Timer

If restoring the witness will take more than 60 minutes and both data nodes are healthy, prevent
unnecessary data moves during the outage window:

```bash
# Run on each data node ESXi
esxcli system settings advanced set -o /VSAN/ClomRepairDelay -i 480
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Could not connect to the local dcui service`** — Ensure you are running the command directly on the ESXi host via SSH or console, not remotely through vCenter.
    **`Error: Unknown option /VSAN/ClomRepairDelay`** — Verify the ESXi host has vSAN enabled and the correct advanced option path; use `esxcli system settings advanced list | grep -i clom` to confirm the option exists.
This sets the rebuild delay to 480 minutes. Reset to default (60) once the witness is restored:

```bash
esxcli system settings advanced set -o /VSAN/ClomRepairDelay -i 60
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unknown option /VSAN/ClomRepairDelay`** — Verify the exact parameter name matches your ESXi version using `esxcli system settings advanced list | grep -i clom`.
    **`Connect to a vSAN-enabled host or cluster before running this command`** — Run the command on an ESXi host that has vSAN enabled, or use `-s <hostname>` to target a specific host.
---

## 6. Verification

```powershell
# PowerCLI — check vSAN health summary
Get-VsanHealthSummary -Cluster (Get-Cluster "<cluster-name>") |
  Where-Object { $_.OverallHealth -ne 'green' }
```

Expected: no results (all checks green).

```bash
# ESXi — confirm 3-member cluster
esxcli vsan cluster list | grep "Sub-Cluster Member Count"
# Expected: Sub-Cluster Member Count: 3

# ESXi — confirm no ABSENT witness components
esxcli vsan debug object list | grep -c "ABSENT"
# Expected: 0
```


```text title="Expected output"
Sub-Cluster Member Count: 3
0
```

!!! warning "Common errors"
    **`Unknown command or namespace vsan.`** — Verify VSAN is licensed and enabled on the cluster; run `esxcli vsan cluster list` to confirm VSAN is initialized.
    **`grep: (standard input) is empty`** — Ensure the ESXi host is part of an active VSAN cluster; if newly added, wait 2–3 minutes for cluster membership to stabilize.
---

## 7. Prevention

| Control | Implementation |
|---|---|
| Witness placement | Separate L3 network from data site; routed over WAN or dedicated management VLAN; never same physical host as data nodes |
| Witness appliance sizing | 4 vCPU / 8 GB RAM / 50 GB disk minimum; use VMware-provided witness OVA to ensure correct component counts |
| Monitoring | Alert immediately on vSAN health degradation — witness partition is silent at the VM level until a data node also fails |
| Witness VM HA | Run witness appliance on a separate vSphere cluster with HA enabled; ensure the cluster has capacity to restart the witness VM |
| Network validation | Test witness TEP connectivity (`vmkping`) after any network maintenance; include in change-window verification checklist |

---

## Related Scenarios

- [vSAN Disk or Component Failure](vsan-disk-component-failure.md) — a disk failure on a data
  node combined with witness loss is the highest-risk event for a 2-node cluster.
- [vSAN Stretched Cluster Split Brain](vsan-stretched-cluster-split-brain.md) — stretched
  cluster quorum failure shares root cause patterns with 2-node witness loss.
- [Storage APD — Datastore Inaccessible](storage-apd-datastore-inaccessible.md) — if vSAN
  objects become inaccessible after quorum loss, APD handling is triggered on the ESXi hosts.
