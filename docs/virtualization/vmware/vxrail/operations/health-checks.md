---
tags:
  - operations
  - vmware
  - vxrail
---
# VxRail — Health Checks

<div class="kb-summary">
Daily and weekly health check routine for VxRail clusters. Covers VxRail Plugin node status, vSAN object health and resync, iDRAC hardware alarms, capacity thresholds, and LCM bundle availability — with a single runnable sequence and alert threshold table.

*Applies to: VxRail 7.x / 8.x*
</div>

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Alert Threshold Table

![Alert Threshold Table](../../../../assets/virtualization-vmware-vxrail-hc-alert-threshold-table.svg)

| Metric | Warning | Critical | Action |
|---|---|---|---|
| vSAN datastore used % | > 70% | > 80% | Add capacity or expand cluster |
| vSAN resync bytes (sustained > 1h) | > 0 bytes | Still growing | Investigate disk or node health |
| Online node count | < expected | < quorum | Investigate offline node immediately |
| iDRAC hardware faults | Warning severity | Critical severity | Open Dell support case |
| ESXi host disconnected from vCenter | Any disconnect | Stays disconnected > 5 min | Check management network and iDRAC |
| vSAN health checks failing | 1–2 non-critical | Any critical | Run full vSAN health; check disk groups |
| vCenter CPU/memory | > 80% | > 90% | Review VM placement and vCenter sizing |
| VxRail Manager VM availability | Degraded | Unreachable | Restore from backup; check cluster |

---

## Daily Health Checks

![Daily Health Checks](../../../../assets/virtualization-vmware-vxrail-hc-daily-health-checks.svg)

### 1. VxRail Plugin — Node Status

![1. VxRail Plugin — Node Status](../../../../assets/virtualization-vmware-vxrail-hc-1-vxrail-plugin-node-status.svg)

Open vCenter and navigate to: **Menu → VxRail → Cluster → Summary**

Check:

- All nodes show status **Online** (green)
- No nodes in **Error**, **Degraded**, or **Offline** state
- No active cluster alarms on the VxRail cluster object
- SupportAssist connectivity status is **Connected**

```bash
# API check — all hosts healthy
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/hosts" | \
  python3 -c "
import sys, json
hosts = json.load(sys.stdin)
for h in hosts:
    print(h.get('esxi_hostname','?'), '-', h.get('health','?'))
"
```


```text title="Expected output"
vxrail-esx-01.lab.local - green
vxrail-esx-02.lab.local - green
vxrail-esx-03.lab.local - green
vxrail-esx-04.lab.local - green
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in example; if still failing, verify VXM IP is correct and reachable on port 443).
    **`curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused`** — Confirm VXM appliance is running and the IP address is correct; check network connectivity with `ping <vxm-ip>`.
    **`error: 401 Unauthorized`** — Verify the VXM credentials (username:password) are correct and base64-encoded properly by testing `echo -n 'mystic:password' | base64` independently.
### 2. vSAN Health

![2. vSAN Health](../../../../assets/virtualization-vmware-vxrail-hc-2-vsan-health.svg)

SSH to any ESXi node in the cluster:

```bash
# Cluster-level health (all checks pass = OK)
esxcli vsan health cluster get

# Detailed summary — look for any WARNING or ERROR
esxcli vsan health summary get

# Object resync — must be 0 Remaining Bytes for normal operation
esxcli vsan debug resync list

# Network test — all nodes should reach all nodes
esxcli vsan debug network test
```


```text title="Expected output"
Cluster Health Status: HEALTHY
Number of Hosts: 4
Number of Disk Groups: 4
Skyline Health: ENABLED

Health Check Summary
=====================
Component                          Status
---------------------------------  --------
vSAN Cluster                       HEALTHY
vSAN Object Repair Timer           HEALTHY
vSAN Disk Balance                  HEALTHY
vSAN Memory Pool                   HEALTHY
vSAN Network                       HEALTHY
vSAN Physical Disk                 HEALTHY

Resync Objects
==============
Object UUID                          Remaining Bytes    Status
------------------------------------  -----------------  ----------
52e3a1c4-1a2f-4c8a-9e7b-3f5d8b2a1c9  0                  Complete
7f2b9d1e-5c3a-4b8f-2e1d-6a4c8f3b2e5  0                  Complete
3c1f7a9e-2b5d-4a8c-1f3e-5b2a7d4c6e8  0                  Complete

Network Connectivity Test Results
===================================
Source Host              Target Host              Status    Latency (ms)
------------------------  ----------------------  --------  -----------
esx-vxrail-01.lab.local  esx-vxrail-02.lab.local  PASS      0.847
esx-vxrail-01.lab.local  esx-vxrail-03.lab.local  PASS      0.923
esx-vxrail-02.lab.local  esx-vxrail-04.lab.local  PASS      1.102
esx-vxrail-03.lab.local  esx-vxrail-04.lab.local  PASS      0.756
```

!!! warning "Common errors"
    **`vSAN Cluster: UNHEALTHY — Check vSAN Object Repair Timer and Physical Disk status using esxcli vsan health cluster get, then resolve failed components before proceeding.`** — Investigate component-specific failures and remediate disk/network issues.
    **`Network test FAILED: Host esx-vxrail-02 cannot reach esx-vxrail-04 — Verify vSAN VMkernel port connectivity, check firewall rules for UDP 12345, and confirm all hosts have matching vSAN network configuration.`** — Verify vSAN VMkernel adapters are on the same subnet and multicast is enabled.
    **`Resync Objects: 2.5 TB Remaining Bytes — vSAN is actively resyncing data after a host failure or disk replacement.`** — Wait for resync to complete (monitor with watch 'esxcli vsan debug resync list') or check host/disk status if resync stalls.
In PowerCLI:

```powershell
# vSAN health summary from vCenter
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" |
  Select-Object OverallHealth, OverallHealthDescription
```

### 3. iDRAC Hardware Health

![3. iDRAC Hardware Health](../../../../assets/virtualization-vmware-vxrail-hc-3-idrac-hardware-health.svg)

Check each node's iDRAC for hardware alarms. SSH to each node's iDRAC IP:

```bash
# Get system info — look for any Status: Warning or Critical
racadm getsysinfo

# Last 20 system event log entries — look for new faults
racadm getsel | tail -20
```


```text title="Expected output"
System Information
==================
System Model: VxRail E560
System BIOS Version: 2.14.3
iDRAC Version: 5.10.20.00
Firmware Version: 4.2.1
System Status: OK
Power Status: On
Thermal Status: OK
Memory Status: OK
Storage Status: Warning
Network Status: OK

System Event Log (Last 20 entries):
2024-01-15 14:32:18 | SEL ID: 0x00F4 | Physical Drive 1.2.3 | Predictive Failure
2024-01-15 13:45:02 | SEL ID: 0x00F3 | Temperature Sensor CPU1 | Normal
2024-01-15 12:18:55 | SEL ID: 0x00F2 | Power Supply 1 | Normal
2024-01-15 11:05:33 | SEL ID: 0x00F1 | RAID Controller | Rebuild in Progress
2024-01-15 09:22:14 | SEL ID: 0x00F0 | System Boot | Completed Successfully
2024-01-15 08:10:47 | SEL ID: 0x00EF | Memory Module 3 | Correctable ECC Error
```

!!! warning "Common errors"
    **`RACADM: ERROR: iDRAC IP <IP> is not responding`** — Verify iDRAC network connectivity and ensure the management interface is configured with `racadm config -g cfgLanSecurity -o cfgIpStaticIpAddr <IP>`.
    **`RACADM: ERROR: Access Denied. Insufficient privileges`** — Confirm you are running the command as root or with sudo, or authenticate with `-u <username> -p <password>` flags.
    **`RACADM: ERROR: Unable to parse response from iDRAC`** — Restart the iDRAC service with `racadm racreset` and wait 2 minutes for it to fully initialize before retrying.
In OMIVV (vCenter plugin): **Menu → OpenManage Integration → Hardware → Alarms** — verify no red or orange alerts.

### 4. vSAN Capacity

![4. vSAN Capacity](../../../../assets/virtualization-vmware-vxrail-hc-4-vsan-capacity.svg)

```powershell
# Check vSAN datastore usage
Get-Datastore "vsanDatastore" | Select-Object Name,
    @{N="TotalGB"; E={[Math]::Round($_.CapacityGB)}},
    @{N="FreeGB"; E={[Math]::Round($_.FreeSpaceGB)}},
    @{N="UsedPct"; E={[Math]::Round((1 - $_.FreeSpaceGB/$_.CapacityGB)*100,1)}}
```

Alert if `UsedPct` exceeds **70%**. vSAN performance degrades above 70% as rebalancing becomes more frequent and slack capacity for rebuilds shrinks.

### 5. LCM Bundle Status

![5. LCM Bundle Status](../../../../assets/virtualization-vmware-vxrail-hc-5-lcm-bundle-status.svg)

In vCenter: **VxRail Plugin → Lifecycle Management → Available Upgrades**

Or via API:

```bash
# Check if an upgrade bundle is available
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/lcm/upgrade" | python3 -m json.tool
```


```text title="Expected output"
{
  "id": "upgrade-bundle-20240115",
  "version": "7.0.500",
  "releaseDate": "2024-01-15T00:00:00Z",
  "bundleSize": 8589934592,
  "bundleSizeGB": 8.0,
  "status": "available",
  "releaseNotes": "https://docs.vmware.com/vxrail/7.0.500/release-notes",
  "components": [
    {
      "name": "ESXi",
      "currentVersion": "7.0.480",
      "targetVersion": "7.0.500"
    },
    {
      "name": "vCenter",
      "currentVersion": "7.0.480",
      "targetVersion": "7.0.500"
    },
    {
      "name": "vSAN",
      "currentVersion": "7.0.480",
      "targetVersion": "7.0.500"
    }
  ],
  "prerequisites": [
    "Minimum 50GB free space on VXM",
    "All hosts in healthy state",
    "No active LCM operations"
  ],
  "estimatedDowntimeMinutes": 45
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag (already present) or import the VXM certificate into your system's CA bundle; if still failing, verify the VXM hostname matches the certificate CN.
    **`jq: parse error: Invalid JSON`** — Ensure python3 is installed and the API response is valid JSON; check that the VXM service is running with `curl -sk https://<vxm-ip>/rest/vxm/v1/system/status`.
    **`curl: (401) Unauthorized`** — Verify the VXM credentials are correct and base64-encoded properly with `echo -n 'mystic:password' | base64`, then confirm the user has LCM API permissions in VXM.
If a bundle is available, record it and plan an upgrade in the next maintenance window.

---

## Weekly Health Checks

![Weekly Health Checks](../../../../assets/virtualization-vmware-vxrail-hc-weekly-health-checks.svg)

### ESXi Version Consistency

![ESXi Version Consistency](../../../../assets/virtualization-vmware-vxrail-hc-esxi-version-consistency.svg)

All nodes in a VxRail cluster must run the same ESXi version and build. After any LCM upgrade, confirm consistency:

```powershell
# All hosts should show identical Version and Build
Get-VMHost | Select-Object Name,
    @{N="Version"; E={$_.Version}},
    @{N="Build"; E={$_.Build}} |
  Sort-Object Name | Format-Table -AutoSize
```

A mismatch means a node was skipped during LCM or a node was manually patched (not supported). Open a Dell support case if mismatch is unexplained.

### vSAN Storage Policy Compliance

![vSAN Storage Policy Compliance](../../../../assets/virtualization-vmware-vxrail-hc-vsan-storage-policy-compliance.svg)

```powershell
# Check all VMs for policy compliance — flag any non-compliant
Get-VM | Get-SpbmEntityConfiguration |
  Select-Object Entity, StoragePolicy, ComplianceStatus |
  Where-Object {$_.ComplianceStatus -ne "compliant"} |
  Format-Table -AutoSize
```

### Node Hardware Summary

![Node Hardware Summary](../../../../assets/virtualization-vmware-vxrail-hc-node-hardware-summary.svg)

```bash
# Run on each node — check BIOS and iDRAC firmware versions
racadm getversion -f bios
racadm getversion -f idrac

# Temperature and fan health
esxcli hardware sensor list --type Temperature | grep -i critical
esxcli hardware sensor list --type Fan | grep -i critical
```


```text title="Expected output"
BIOS Version=2.14.2
iDRAC Version=6.10.40.00

(no output — command completes silently)

(no output — command completes silently)
```

!!! warning "Common errors"
    **`racadm: command not found`** — Install Dell iDRAC tools or run this command directly on the iDRAC IP via SSH instead of the ESXi host.
    **`Unable to parse objname _NIC.Embedded.1-1-1`** — Restart the iDRAC service with `racadm racreset soft` and retry after 2 minutes.
---

## Run This Routine

Paste this sequence into a PowerCLI session connected to vCenter. It runs all critical daily checks in order and outputs a pass/fail summary.

```powershell
# === VxRail Daily Health Check Routine ===
# Prerequisites: Connect-VIServer first
# Also requires: curl access to VxRail Manager IP

$ClusterName  = "VxRail-Cluster"
$VxmIp        = "<vxm-ip>"
$VxmPassword  = "<mystic-password>"
$VsanDS       = "vsanDatastore"
$CapacityAlert = 70   # percent

$Auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("mystic:$VxmPassword"))
$Headers = @{ Authorization = "Basic $Auth" }

Write-Host "`n=== VxRail Health Check: $(Get-Date -Format 'yyyy-MM-dd HH:mm') ===" -ForegroundColor Cyan

# 1. VxRail Plugin node status via API
Write-Host "`n[1] VxRail Node Status" -ForegroundColor Yellow
try {
    $hosts = Invoke-RestMethod -Uri "https://$VxmIp/rest/vxm/v1/hosts" `
        -Headers $Headers -SkipCertificateCheck
    foreach ($h in $hosts) {
        $status = $h.health
        $color  = if ($status -eq "NORMAL") { "Green" } else { "Red" }
        Write-Host "  $($h.esxi_hostname) — $status" -ForegroundColor $color
    }
} catch {
    Write-Host "  ERROR: Cannot reach VxRail Manager at $VxmIp" -ForegroundColor Red
}

# 2. vSAN cluster health
Write-Host "`n[2] vSAN Cluster Health" -ForegroundColor Yellow
$vsan = Get-VsanClusterHealthSummary -Cluster $ClusterName -ErrorAction SilentlyContinue
if ($vsan) {
    $color = if ($vsan.OverallHealth -eq "green") { "Green" } else { "Red" }
    Write-Host "  Overall Health: $($vsan.OverallHealth)" -ForegroundColor $color
} else {
    Write-Host "  ERROR: Cannot get vSAN health" -ForegroundColor Red
}

# 3. vSAN capacity
Write-Host "`n[3] vSAN Capacity" -ForegroundColor Yellow
$ds = Get-Datastore $VsanDS -ErrorAction SilentlyContinue
if ($ds) {
    $usedPct = [Math]::Round((1 - $ds.FreeSpaceGB / $ds.CapacityGB) * 100, 1)
    $color   = if ($usedPct -ge $CapacityAlert) { "Red" } else { "Green" }
    Write-Host "  $VsanDS — Used: $usedPct% (Total: $([Math]::Round($ds.CapacityGB)) GB, Free: $([Math]::Round($ds.FreeSpaceGB)) GB)" -ForegroundColor $color
} else {
    Write-Host "  ERROR: Datastore '$VsanDS' not found" -ForegroundColor Red
}

# 4. Host version consistency
Write-Host "`n[4] ESXi Version Consistency" -ForegroundColor Yellow
$hosts = Get-VMHost | Sort-Object Name
$versions = $hosts | Select-Object -ExpandProperty Version | Sort-Object -Unique
$builds   = $hosts | Select-Object -ExpandProperty Build   | Sort-Object -Unique
if ($versions.Count -eq 1 -and $builds.Count -eq 1) {
    Write-Host "  All nodes: ESXi $($versions[0]) build $($builds[0])" -ForegroundColor Green
} else {
    Write-Host "  VERSION MISMATCH DETECTED:" -ForegroundColor Red
    $hosts | Select-Object Name, Version, Build | Format-Table -AutoSize
}

# 5. vCenter alarms
Write-Host "`n[5] Active vCenter Alarms on Cluster" -ForegroundColor Yellow
$cluster = Get-Cluster $ClusterName
$alarms  = $cluster.ExtensionData.TriggeredAlarmState
if ($alarms.Count -eq 0) {
    Write-Host "  No active alarms" -ForegroundColor Green
} else {
    Write-Host "  $($alarms.Count) alarm(s) active — check vCenter alarms panel" -ForegroundColor Red
}

# 6. LCM upgrade availability
Write-Host "`n[6] LCM Upgrade Availability" -ForegroundColor Yellow
try {
    $lcm = Invoke-RestMethod -Uri "https://$VxmIp/rest/vxm/v1/lcm/upgrade" `
        -Headers $Headers -SkipCertificateCheck
    if ($lcm.state -and $lcm.state -ne "NONE") {
        Write-Host "  LCM job in state: $($lcm.state)" -ForegroundColor Yellow
    } else {
        Write-Host "  No active LCM job" -ForegroundColor Green
    }
} catch {
    Write-Host "  INFO: LCM endpoint returned no active job (expected when idle)" -ForegroundColor Gray
}

Write-Host "`n=== Health Check Complete ===" -ForegroundColor Cyan
```

### Companion Bash Snippet (run on any ESXi node)

![Companion Bash Snippet (run on any ESXi node)](../../../../assets/virtualization-vmware-vxrail-hc-companion-bash-snippet-run-on-any-esxi-node.svg)

```bash
#!/bin/bash
# Run on any VxRail ESXi node over SSH
# Checks vSAN health, resync, and network

echo "=== vSAN Health ==="
esxcli vsan health cluster get 2>&1 | grep -E "Health|Status|Error"

echo ""
echo "=== vSAN Resync ==="
esxcli vsan debug resync list 2>&1 | grep -E "Total|Remaining|Object"

echo ""
echo "=== vSAN Network Test ==="
esxcli vsan debug network test 2>&1 | tail -5

echo ""
echo "=== Hardware Sensors (Critical only) ==="
esxcli hardware sensor list 2>&1 | grep -i "critical" || echo "No critical sensors"
```


```text title="Expected output"
=== vSAN Health ===
Health Status: Healthy
Cluster Status: Healthy
Error Count: 0

=== vSAN Resync ===
Total Objects: 1247
Remaining Objects: 0
Resync Status: Complete

=== vSAN Network Test ===
vmnic0: PASS (latency: 0.42ms)
vmnic1: PASS (latency: 0.38ms)
vmnic2: PASS (latency: 0.41ms)
vmnic3: PASS (latency: 0.39ms)
Network Status: All links operational

=== Hardware Sensors (Critical only) ===
No critical sensors
```

!!! warning "Common errors"
    **`vsan health cluster get: Unknown command or namespace`** — Verify the ESXi host is vSAN-enabled by running `esxcli vsan cluster get` instead (older ESXi versions use different command syntax).
    **`Permission denied`** — Ensure you are connected via SSH as root or a user with vSAN admin privileges; use `sudo` or authenticate with elevated credentials.
    **`Network test: No such file or directory`** — The vSAN debug network test command may not exist on this ESXi version; use `esxcli vsan debug network list` to verify network participation instead.
---

## See also

- [VxRail — Common Issues](../../troubleshooting/common-issues/)
- [VxRail — Procedures](../procedures/)
- [VxRail — CLI Reference](../cli-reference/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
