---
tags:
  - vmware
  - vcenter
  - esxi
  - vsan
  - nsx
  - operations
  - vsphere-8
---
# VMware — Morning Health Check

<div class="kb-summary">
Start-of-shift health check sequence for a VMware SDDC environment. Run these checks in order — vCenter → ESXi cluster → vSAN → NSX → Aria Operations. Each section takes 2–5 minutes. The full routine should complete in under 20 minutes.
</div>

```text
┌────────────────────────────────── VMware Morning Health Check ────────────────────────────────────────┐
│                                                                                                       │
│  Run order (each check feeds the next):                                                               │
│                                                                                                       │
│  1. vCenter ──► 2. ESXi Cluster ──► 3. vSAN ──► 4. NSX ──► 5. Aria Ops ──► Done / Escalate            │
│                                                                                                       │
│  vCenter: services running, no critical alarms, recent backup successful                              │
│  ESXi: all hosts connected, no warnings, HA/DRS active, NTP in sync                                   │
│  vSAN: health green, no degraded objects, capacity < 70%, no resync stuck                             │
│  NSX: managers healthy, edges up, BGP established, DFW rules unchanged                                │
│  Aria: alert count normal, no capacity threshold breaches, no log spikes                              │
│                                                                                                       │
│  Escalate immediately if:                                                                             │
│  ■ Any vSAN object in ABSENT/DEGRADED state          ■ NSX Edge BGP session down                      │
│  ■ ESXi host disconnected or in error state          ■ vCenter backup missed >24 h                    │
│  ■ vSAN capacity > 80%                               ■ Aria alert storm (>50 new in 1 h)              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

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

**Expected output:** No output (all services RUNNING). If any service appears, restart it:

```bash
service-control --restart <service-name>
```

Check alarms in vSphere Client: **Home → Alarms → All Alarms** — filter to `Critical`. Any critical alarm here blocks the rest of the routine until acknowledged or resolved.

Verify backup:

```bash
# VAMI: https://<vcenter-fqdn>:5480 → Backup → Last backup status
# CLI alternative:
grep "Backup completed" /var/log/vmware/applmgmt/backup.log | tail -1
```

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

**Expected output:** No output (all checks green). Any non-green line needs investigation.

Check object health:

```bash
esxcli vsan debug object list | grep -v "state:healthy" | head -20
```

**Expected output:** No output, or only objects in `state:resyncing` (acceptable if resync is making progress).

Check capacity:

```bash
esxcli vsan storage list | grep -E "Used Capacity|Total Capacity"
```

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
