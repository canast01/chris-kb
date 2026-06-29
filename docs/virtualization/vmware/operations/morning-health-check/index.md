---
tags:
  - vmware
  - vcenter
  - esxi
  - vsan
  - nsx
  - operations
  - vsphere-8
search:
  boost: 2
---
# VMware — Morning Health Check

<div class="kb-summary">
Start-of-shift health check sequence for a VMware SDDC environment. Run these checks in order — vCenter → ESXi cluster → vSAN → NSX → Aria Operations. Each section takes 2–5 minutes. The full routine should complete in under 20 minutes.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

1_vcenter: "1. vCenter" {shape: rectangle}
2_esxi_cluster: "2. ESXi Cluster" {shape: rectangle}
3_vsan: "3. vSAN" {shape: rectangle}
4_nsx: "4. NSX" {shape: rectangle}
5_aria_operations: "5. Aria Operations" {shape: rectangle}
signoff_checklist: "Sign-off Checklist" {shape: rectangle}

1_vcenter -> 2_esxi_cluster: uses
2_esxi_cluster -> 3_vsan: uses
3_vsan -> 4_nsx: uses
4_nsx -> 5_aria_operations: uses
5_aria_operations -> signoff_checklist: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## 1. vCenter

**Goal:** services healthy, no critical alarms, backup current.

```bash
# SSH to VCSA or use vCenter Shell
service-control --status --all | grep -v RUNNING   # anything not RUNNING?
```


```text title="Expected output"
vmware-vpostgres                                    STOPPED
vmware-rhttpproxy                                   RUNNING
vmware-sps                                          RUNNING
vmware-vpxd                                         RUNNING
vmware-vsan-health                                  RUNNING
vmware-cm                                           STOPPED
vmware-cis-license                                  RUNNING
vmware-netdumper                                    STOPPED
```

!!! warning "Common errors"
    **`service-control: command not found`** — Ensure you are logged into the VCSA appliance directly (SSH to the vCenter Server Appliance hostname/IP), not a Windows vCenter instance.
    **`Permission denied`** — Run the command with `sudo` or log in as root user to the VCSA appliance.
**Expected output:** No output (all services RUNNING). If any service appears, restart it:

```bash
service-control --restart <service-name>
```


```text title="Expected output"
Stopping service <service-name>...
Waiting for service <service-name> to stop...
Service <service-name> stopped successfully.
Starting service <service-name>...
Waiting for service <service-name> to start...
Service <service-name> started successfully.
```

!!! warning "Common errors"
    **`Error: Unknown service '<service-name>'`** — Replace `<service-name>` with a valid VMware service name like `vmware-vpxd`, `vmware-esx-hostd`, or `vpxa`.
    **`Error: Permission denied`** — Run the command with root privileges using `sudo service-control --restart <service-name>` or as the root user.
    **`Timeout waiting for service to start`** — Check service dependencies and logs with `service-control --status <service-name>` and review `/var/log/vmware/vpxd/vpxd.log` for startup errors.
Check alarms in vSphere Client: **Home → Alarms → All Alarms** — filter to `Critical`. Any critical alarm here blocks the rest of the routine until acknowledged or resolved.

Verify backup:

```bash
# VAMI: https://<vcenter-fqdn>:5480 → Backup → Last backup status
# CLI alternative:
grep "Backup completed" /var/log/vmware/applmgmt/backup.log | tail -1
```


```text title="Expected output"
Backup completed successfully at 2024-01-15 03:45:22 UTC. Duration: 47 minutes. Size: 23.4 GB. Destination: /mnt/backup/vcenter-prod-01.bak.
```

!!! warning "Common errors"
    **`grep: /var/log/vmware/applmgmt/backup.log: No such file or directory`** — Verify the vCenter appliance has backup logging enabled and check the correct log path with `find /var/log -name "*backup*"`.
    **`(no output returned)`** — The backup log exists but contains no successful completions; check `/var/log/vmware/applmgmt/backup.log` directly or review VAMI for backup job status and errors.
**Expected output:** Timestamp within last 24 hours.

**Escalate if:** Any service not running after restart · Last backup > 24 h ago · Critical alarms present.

---

## 2. ESXi Cluster

**Goal:** all hosts connected, cluster features active, NTP in sync.

Open **vSphere Client → Hosts and Clusters → \<cluster\>**. Confirm:

- All hosts show status **Connected** (green)
- No hosts in **Maintenance Mode** unexpectedly
- **HA Status** — green, admission control satisfied
- **DRS Status** — Fully Automated, no migration recommendations pending > 1 hour

Check NTP across hosts (PowerCLI):

```powershell
Get-VMHost | Select Name, @{N='NTP';E={($_ | Get-VMHostNtpServer) -join ', '}}, `
  @{N='TimeDrift';E={(Get-View $_.Id).Config.DateTimeInfo.SystemClockResolution}}
```

**Expected output:** All hosts show NTP servers configured, no host drift > 5 seconds.

Check for host hardware warnings:

```powershell
Get-VMHost | Get-View | Select Name, @{N='HWStatus';E={$_.OverallStatus}} |
  Where-Object HWStatus -ne 'green'
```

**Expected output:** No output (all green).

**Escalate if:** Any host disconnected · HA admission control breached · NTP drift > 30 s on any host · Hardware status yellow/red.

---

## 3. vSAN

**Goal:** health green, no degraded objects, capacity safe, no stuck resync.

```bash
# SSH to any ESXi host in the vSAN cluster
esxcli vsan health cluster get | grep -v "Green\|green" | grep -v "^$"
```


```text title="Expected output"
Cluster Status: yellow
Memory Usage: yellow
Network Latency: yellow
Disk Capacity: yellow
```

!!! warning "Common errors"
    **`Connect timed out`** — Verify the ESXi host is reachable and SSH is enabled via `esxcli system ssh set --enabled=true` on the target host.
    **`Unknown command or namespace`** — Ensure you're connected to an ESXi host with vSAN enabled; run `esxcli vsan cluster list` first to confirm vSAN is active on the cluster.
    **`Permission denied`** — Confirm your SSH user has root or equivalent privileges; use an account with administrative rights to the ESXi host.
**Expected output:** No output (all checks green). Any non-green line needs investigation.

Check object health:

```bash
esxcli vsan debug object list | grep -v "state:healthy" | head -20
```


```text title="Expected output"
Object UUID                          State          Space Used
52a4c8f1-2b3e-4a9c-8d1f-7e6c5b4a3d2c state:degraded 2.1 GB
7f9e8d7c-6b5a-4938-2c1b-0a9f8e7d6c5b state:absent    0 B
3c2b1a0f-9e8d-7c6b-5a4938-2c1b0a9f8e state:congested 5.8 GB
9d8c7b6a-5f4e-3d2c-1b0a-9f8e7d6c5b4a state:degraded 1.2 GB
1a0f9e8d-7c6b5a49-38-2c1b0a9f8e7d6c state:inaccessible 0 B
6b5a4938-2c1b-0a9f-8e7d-6c5b4a3d2c1b state:degraded 3.4 GB
```

!!! warning "Common errors"
    **`esxcli: command not found`** — Ensure you are running this command directly on an ESXi host (SSH session), not from vCenter; if on vCenter, use SSH to connect to the ESXi host first.
    **`VSAN is not enabled on this cluster`** — Verify VSAN is licensed and enabled on the cluster by checking vSphere Client > Cluster > Configure > vSAN > General.
**Expected output:** No output, or only objects in `state:resyncing` (acceptable if resync is making progress).

Check capacity:

```bash
esxcli vsan storage list | grep -E "Used Capacity|Total Capacity"
```


```text title="Expected output"
Used Capacity: 2.34 TB
Total Capacity: 5.12 TB
Used Capacity: 1.87 TB
Total Capacity: 5.12 TB
Used Capacity: 3.21 TB
Total Capacity: 5.12 TB
```

!!! warning "Common errors"
    **`Connect to localhost failed. Error: Unable to connect to the vSAN Health Service`** — Ensure vSAN is enabled on the cluster and the vSAN Health Service is running; restart the service with `systemctl restart vsanvpd` if needed.
    **`Unknown command or namespace vsan`** — Verify the ESXi host has vSAN licensed and enabled; check with `esxcli vsan cluster get` to confirm vSAN is active on the cluster.
**Expected output:** Used capacity < 70% of total. At 70% set a ticket; at 80% escalate immediately.

Check resync throughput (if objects are resyncing):

```powershell
# vSphere Client: Cluster → Monitor → vSAN → Resyncing Objects
# Must show progress (bytes remaining decreasing over 5 min intervals)
```

**Escalate if:** Any object in ABSENT or DEGRADED state · Capacity ≥ 80% · Resync stuck (no progress > 30 min) · Health check not green after 2 attempts.

---

## 4. NSX

**Goal:** managers reachable, edges up, BGP established, DFW baseline unchanged.

Check Manager cluster health (NSX UI: **System → Overview**):

- All three NSX Manager nodes: **Active** (green)
- Management cluster status: **Stable**

Check Edge nodes:

```bash
# NSX Manager → Fabric → Nodes → Edge Transport Nodes
# Each Edge: Status = Up, BFD = Up, Tunnel = Up
```

Check BGP sessions (NSX UI or API):

```bash
# NSX Manager → Networking → Tier-0 Gateways → <T0> → BGP → Neighbors
# All BGP neighbors: State = Established
```

Spot-check DFW rule count (should not have changed overnight):

```bash
curl -sk -u admin:<password> https://<nsx-mgr>/api/v1/firewall/sections \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'DFW sections: {d[\"result_count\"]}')"
```


```text title="Expected output"
DFW sections: 47
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl to skip SSL verification (already present in the example, so verify the flag wasn't removed).
    **`curl: (7) Failed to connect to <nsx-mgr>: Name or service not known`** — Verify the NSX Manager hostname or IP address is correct and resolvable from your network.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Check that the NSX Manager API is responding and the credentials are valid; a 401/403 response will produce invalid JSON.
**Expected output:** DFW section count matches previous day. An unexpected increase may indicate a runaway automation job.

**Escalate if:** Any NSX Manager node not active · Any Edge node down · BGP session not Established · DFW count changed unexpectedly by > 5.

---

## 5. Aria Operations

**Goal:** alert count normal, no new capacity breaches, log ingestion healthy.

Open **Aria Operations → Alerts → Active Alerts**. Confirm:

- Active alert count is within normal range (establish a baseline for your environment; flag if > 20% above 7-day average)
- No **Capacity Remaining** alerts on vSAN, hosts, or datastores
- No **Certificate Expiry** alerts within 30 days

Check Aria Operations for Logs:

- **Aria Logs → Overview** — ingestion rate normal (within ±30% of 7-day average)
- No agents showing as disconnected

Check Aria Operations adapters:

```text
Aria Ops → Administration → Solutions → Collection State
```

**Expected output:** All adapters show **Data Receiving** in last 5 minutes.

**Escalate if:** Alert storm (sudden spike > 50 alerts in 1 hour) · Capacity alert on any cluster · Log ingestion dropped to zero · Any adapter not collecting for > 15 min.

---

## Sign-off Checklist

Copy this block into your shift log after completing the check:

```text
Date/Time : _______________
Completed by : _______________

1. vCenter    ☐ Clean  ☐ Issues: _______________________
2. ESXi       ☐ Clean  ☐ Issues: _______________________
3. vSAN       ☐ Clean  ☐ Issues: _______________________
4. NSX        ☐ Clean  ☐ Issues: _______________________
5. Aria Ops   ☐ Clean  ☐ Issues: _______________________

Overall status : ☐ All clear  ☐ Monitoring  ☐ Incident open (ticket: ______)
```

---

## See also

- [vCenter — Operations](../../vcenter/operations/) — detailed vCenter CLI and service reference
- [vSAN Cluster Health Internals](../../internals/vsan-cluster-health/) — object state machine and resync mechanics
- [NSX Data Plane Internals](../../internals/nsx-data-plane/) — TEP, BFD, DFW fast path
- [Runbooks](../runbooks/) — step-by-step procedures for specific operational tasks
- [Scenarios — Issues](../../topics/scenarios/) — cross-product troubleshooting playbooks

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
