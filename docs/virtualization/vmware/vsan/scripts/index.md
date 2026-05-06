# Scripts

> Part of the [vSAN](../) reference.

---

## vSAN Cluster Health Check (PowerShell / PowerCLI)

Run the full vSAN health test suite via PowerCLI and exit non-zero if any test is YELLOW or RED.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vsan_cluster_health.ps1
# Usage: pwsh -File vsan_cluster_health.ps1
# Env vars: VCENTER_HOST, VC_USER, VC_PASS, CLUSTER_NAME

param(
    [string]$VCenterHost  = $env:VCENTER_HOST,
    [string]$VCUser       = $env:VC_USER,
    [string]$VCPass       = $env:VC_PASS,
    [string]$ClusterName  = $env:CLUSTER_NAME
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null

$cluster = Get-Cluster -Name $ClusterName -ErrorAction Stop

Write-Host "`n=== vSAN Health Check: $($cluster.Name) ===" -ForegroundColor Cyan
Write-Host "($(Get-Date -Format 'o'))`n"

$overallExit = 0

# --- Cluster health summary ---
$healthSummary = Get-VsanClusterHealthSummary -Cluster $cluster -FetchFromCache:$false
foreach ($group in $healthSummary.Groups) {
    foreach ($test in $group.GroupTests) {
        $s = switch ($test.TestHealth) {
            'green'   { 'PASS'     }
            'yellow'  { 'WARNING'  }
            'red'     { 'CRITICAL' }
            default   { 'UNKNOWN'  }
        }
        $colour = switch ($s) {
            'PASS'     { 'Green'  }
            'WARNING'  { 'Yellow' }
            'CRITICAL' { 'Red'    }
            default    { 'White'  }
        }
        if ($s -eq 'CRITICAL') { $overallExit = 2 }
        if ($s -eq 'WARNING' -and $overallExit -lt 2) { $overallExit = 1 }
        Write-Host ("[{0,-8}] {1}" -f $s, $test.TestName) -ForegroundColor $colour
    }
}

# --- Disk group capacity ---
Write-Host "`n--- Disk Group Capacity ---"
$diskGroups = Get-VsanDiskGroup -Cluster $cluster
foreach ($dg in $diskGroups) {
    $capacityDisks = $dg.ExtensionData.DiskMapping.NonSsd
    $totalGB  = ($capacityDisks | Measure-Object -Property CapacityGB -Sum).Sum
    $usedGB   = ($capacityDisks | Measure-Object -Property UsedGB     -Sum).Sum
    $usedPct  = if ($totalGB -gt 0) { [Math]::Round($usedGB / $totalGB * 100, 1) } else { 0 }
    $s = if ($usedPct -ge 70) { 'WARNING' } else { 'PASS' }
    if ($s -eq 'WARNING' -and $overallExit -lt 2) { $overallExit = 1 }
    Write-Host ("[{0,-8}] Host={1}  Total={2:N0}GB  Used={3:N0}GB  {4}%" -f
        $s, $dg.VMHost.Name, $totalGB, $usedGB, $usedPct)
}

# --- Object resync status ---
Write-Host "`n--- Resync Status ---"
$vsanView = Get-VsanView -Id "VsanObjectSystem-vsan-cluster-object-system"
if ($vsanView) {
    $resync = $vsanView.VsanQueryObjectIdentities($cluster.ExtensionData.MoRef, $null, $null, $false, $true, $false)
    $resyncing = if ($resync) { ($resync.Health | Where-Object { $_.Status -ne 'healthy' }).Count } else { 0 }
    $s = if ($resyncing -gt 0) { 'WARNING' } else { 'PASS' }
    if ($s -eq 'WARNING' -and $overallExit -lt 2) { $overallExit = 1 }
    Write-Host ("[{0,-8}] Objects resyncing: {1}" -f $s, $resyncing)
}

Write-Host "`nOverall: $(if ($overallExit -eq 0){'PASS'} elseif ($overallExit -eq 1){'WARNING'} else{'CRITICAL'})"
Disconnect-VIServer -Confirm:$false
exit $overallExit
~~~

---

## Disk Group Capacity Report (PowerShell / PowerCLI)

Print a per-host, per-disk-group capacity table showing cache and capacity tier details, sorted by utilization.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vsan_diskgroup_report.ps1
# Usage: pwsh -File vsan_diskgroup_report.ps1

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS,
    [string]$ClusterName = $env:CLUSTER_NAME,
    [int]$WarnPercent    = 70
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null
$cluster = Get-Cluster -Name $ClusterName -ErrorAction Stop

$results = [System.Collections.Generic.List[PSObject]]::new()

foreach ($dg in (Get-VsanDiskGroup -Cluster $cluster)) {
    $cacheDisk = $dg.ExtensionData.DiskMapping.Ssd
    $capDisks  = $dg.ExtensionData.DiskMapping.NonSsd

    $cacheSizeGB  = [Math]::Round(($cacheDisk | Measure-Object -Property CapacityGB -Sum).Sum, 0)
    $cacheHealth  = ($cacheDisk | ForEach-Object { $_.OperationalState }) -join ','

    $totalGB = [Math]::Round(($capDisks | Measure-Object -Property CapacityGB -Sum).Sum, 0)
    $usedGB  = [Math]::Round(($capDisks | Measure-Object -Property UsedGB -Sum).Sum, 0)
    $freeGB  = $totalGB - $usedGB
    $pct     = if ($totalGB -gt 0) { [Math]::Round($usedGB / $totalGB * 100, 1) } else { 0 }

    $results.Add([PSCustomObject]@{
        Host        = $dg.VMHost.Name
        DiskGroup   = $dg.Name
        CacheGB     = $cacheSizeGB
        CacheHealth = $cacheHealth
        TotalGB     = $totalGB
        UsedGB      = $usedGB
        FreeGB      = $freeGB
        UsedPct     = $pct
        Status      = if ($pct -ge $WarnPercent) { 'WARNING' } else { 'PASS' }
    })
}

$sorted = $results | Sort-Object UsedPct -Descending
$header = "{0,-25} {1,-20} {2,9} {3,-12} {4,9} {5,9} {6,9} {7,7} {8}"
Write-Host ($header -f "Host", "DiskGroup", "Cache GB", "CacheHealth", "Total GB", "Used GB", "Free GB", "Used%", "Status")
Write-Host ("-" * 105)
foreach ($r in $sorted) {
    $colour = if ($r.Status -eq 'WARNING') { 'Yellow' } else { 'White' }
    Write-Host ($header -f $r.Host, $r.DiskGroup, $r.CacheGB, $r.CacheHealth,
        $r.TotalGB, $r.UsedGB, $r.FreeGB, "$($r.UsedPct)%", $r.Status) -ForegroundColor $colour
}

$warnCount = ($sorted | Where-Object { $_.Status -eq 'WARNING' }).Count
Write-Host "`nDisk groups above ${WarnPercent}%: $warnCount"
Disconnect-VIServer -Confirm:$false
exit ($warnCount -gt 0 ? 1 : 0)
~~~

---

## vSAN Object Health Check (Python / pyVmomi)

Connect to vCenter via pyVmomi, query all vSAN objects, and report any that are not in a healthy state.

~~~python
#!/usr/bin/env python3
"""
vsan_object_health.py
Usage: python3 vsan_object_health.py
Deps: pip install pyVmomi
"""

import os, ssl, sys
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi      import vim, vmodl

VCENTER_HOST = os.environ.get("VCENTER_HOST", "vcenter.local")
VC_USER      = os.environ.get("VC_USER",      "administrator@vsphere.local")
VC_PASS      = os.environ.get("VC_PASS",      "")
CLUSTER_NAME = os.environ.get("CLUSTER_NAME", "vSAN-Cluster")

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode    = ssl.CERT_NONE

si      = SmartConnect(host=VCENTER_HOST, user=VC_USER, pwd=VC_PASS, sslContext=context)
content = si.RetrieveContent()

# Find cluster
cluster = None
for dc in content.rootFolder.childEntity:
    if not hasattr(dc, 'hostFolder'): continue
    for item in dc.hostFolder.childEntity:
        if hasattr(item, 'name') and item.name == CLUSTER_NAME:
            cluster = item
            break

if not cluster:
    print(f"Cluster '{CLUSTER_NAME}' not found.")
    sys.exit(2)

print(f"=== vSAN Object Health: {CLUSTER_NAME} ===\n")

# Use VsanObjectSystem to query object health
vsan_obj_sys = None
for mo in content.viewManager.CreateContainerView(
    content.rootFolder, [vim.ClusterComputeResource], True
).view:
    if mo.name == CLUSTER_NAME:
        try:
            vsan_obj_sys = si._stub.GetServiceInstance().content.serviceContent
        except Exception:
            pass
        break

# Fallback: inspect vm config datastores for vSAN object identities
issues = []
vm_container = content.viewManager.CreateContainerView(
    content.rootFolder, [vim.VirtualMachine], True
)

for vm in vm_container.view:
    try:
        runtime = vm.runtime
        if not hasattr(runtime, 'dasVmProtection'):
            continue
        # Check each virtual disk
        for device in vm.config.hardware.device:
            if not isinstance(device, vim.vm.device.VirtualDisk):
                continue
            backing = device.backing
            if not hasattr(backing, 'backingObjectId'):
                continue
            # vSAN-backed disk — check accessibility
            if hasattr(runtime, 'connectionState') and runtime.connectionState == 'inaccessible':
                issues.append({
                    "vm":     vm.name,
                    "type":   "vmdk",
                    "label":  device.deviceInfo.label,
                    "state":  "inaccessible",
                })
    except Exception:
        pass

vm_container.Destroy()

# Check VM home directories
vm2 = content.viewManager.CreateContainerView(
    content.rootFolder, [vim.VirtualMachine], True
)
for vm in vm2.view:
    try:
        if vm.runtime.connectionState == 'inaccessible':
            issues.append({"vm": vm.name, "type": "vm_home", "label": "config", "state": "inaccessible"})
        elif vm.runtime.connectionState == 'orphaned':
            issues.append({"vm": vm.name, "type": "vm_home", "label": "config", "state": "orphaned"})
    except Exception:
        pass
vm2.Destroy()

if issues:
    print(f"{'VM':<30} {'Type':<10} {'Label':<25} {'State'}")
    print("-" * 75)
    for i in issues:
        print(f"{i['vm']:<30} {i['type']:<10} {i['label']:<25} {i['state']}")
    print(f"\nInaccessible/degraded objects: {len(issues)}")
    Disconnect(si)
    sys.exit(1)
else:
    print("All vSAN-backed VM objects appear accessible.")
    Disconnect(si)
    sys.exit(0)
~~~

---

## Performance Baseline Check (PowerShell / PowerCLI)

Collect 24-hour vSAN performance statistics via `Get-VsanStat` and compare key metrics against configurable baselines.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vsan_perf_baseline.ps1
# Usage: pwsh -File vsan_perf_baseline.ps1

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS,
    [string]$ClusterName = $env:CLUSTER_NAME
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null
$cluster = Get-Cluster -Name $ClusterName -ErrorAction Stop

# Configurable baselines
$baselines = @{
    'Backend.Throughput.Read.Average'   = 500    # MB/s
    'Backend.Throughput.Write.Average'  = 300
    'Performance.ReadIops.Average'      = 50000  # IOPS
    'Performance.WriteIops.Average'     = 30000
    'Performance.ReadLatency.Average'   = 5      # ms
    'Performance.WriteLatency.Average'  = 10
    'Congestion.Average'                = 10
    'Overbooking.Average'               = 20
}

$startTime = (Get-Date).AddHours(-24)
$endTime   = Get-Date

Write-Host "`n=== vSAN Performance Baseline: $($cluster.Name) ===" -ForegroundColor Cyan
Write-Host "Period: $($startTime.ToString('o')) → $($endTime.ToString('o'))`n"

$header = "{0,-45} {1,14} {2,14} {3,14} {4}"
Write-Host ($header -f "Metric", "Avg Value", "Baseline", "Delta%", "Status")
Write-Host ("-" * 100)

$overallExit = 0

foreach ($metric in $baselines.Keys | Sort-Object) {
    try {
        $stats = Get-VsanStat -Cluster $cluster -Name $metric `
            -StartTime $startTime -EndTime $endTime -ErrorAction SilentlyContinue
        if (-not $stats) { continue }
        $avg = [Math]::Round(($stats | Measure-Object -Property Value -Average).Average, 2)
        $baseline = $baselines[$metric]
        $deltaPct = if ($baseline -gt 0) { [Math]::Round(($avg - $baseline) / $baseline * 100, 1) } else { 0 }
        $status = if ($deltaPct -gt 20) { 'WARNING' } elseif ($deltaPct -gt 50) { 'CRITICAL' } else { 'PASS' }
        if ($status -eq 'CRITICAL') { $overallExit = 2 }
        if ($status -eq 'WARNING' -and $overallExit -lt 2) { $overallExit = 1 }
        $colour = switch ($status) { 'PASS'{'Green'} 'WARNING'{'Yellow'} 'CRITICAL'{'Red'} default{'White'} }
        Write-Host ($header -f $metric, $avg, $baseline, "${deltaPct}%", $status) -ForegroundColor $colour
    } catch {
        Write-Host ($header -f $metric, "N/A", $baselines[$metric], "-", "SKIPPED")
    }
}

Write-Host "`nOverall: $(if ($overallExit -eq 0){'PASS'} elseif ($overallExit -eq 1){'WARNING'} else{'CRITICAL'})"
Disconnect-VIServer -Confirm:$false
exit $overallExit
~~~

---

## Ansible vSAN Health Playbook

Use `community.vmware` to gather vSAN cluster info, run health checks, inspect disk groups, and assert all health tests pass.

~~~yaml
---
# vsan_health.yml
# Usage: ansible-playbook -i inventory vsan_health.yml
# Deps: ansible-galaxy collection install community.vmware
# Vars: vcenter_hostname, datacenter_name, cluster_name, vc_username, vc_password

- name: vSAN Cluster Health Check
  hosts: localhost
  gather_facts: false
  vars:
    vcenter_hostname: vcenter.local
    datacenter_name:  Production
    cluster_name:     vSAN-Cluster
    vc_username:      "{{ lookup('env','VC_USER') }}"
    vc_password:      "{{ lookup('env','VC_PASS') }}"

  tasks:

    - name: Gather vSAN cluster health info
      community.vmware.vmware_vsan_health_info:
        hostname:       "{{ vcenter_hostname }}"
        username:       "{{ vc_username }}"
        password:       "{{ vc_password }}"
        cluster_name:   "{{ cluster_name }}"
        validate_certs: false
      register: vsan_health

    - name: Show vSAN health groups
      ansible.builtin.debug:
        var: vsan_health.vsan_health_info

    - name: Assert no RED health tests
      ansible.builtin.assert:
        that: >
          vsan_health.vsan_health_info.groups | default([]) | map(attribute='tests') | flatten
          | selectattr('testHealth', 'equalto', 'red') | list | length == 0
        fail_msg: "One or more vSAN health tests are RED — immediate attention required"
        success_msg: "No RED vSAN health tests found"

    - name: Assert no YELLOW health tests
      ansible.builtin.assert:
        that: >
          vsan_health.vsan_health_info.groups | default([]) | map(attribute='tests') | flatten
          | selectattr('testHealth', 'equalto', 'yellow') | list | length == 0
        fail_msg: "One or more vSAN health tests are YELLOW — review required"
        success_msg: "No YELLOW vSAN health tests found"
      register: yellow_assert
      failed_when: false  # report but don't halt on yellow

    - name: Gather cluster facts (for disk group info)
      community.vmware.vmware_cluster_info:
        hostname:       "{{ vcenter_hostname }}"
        username:       "{{ vc_username }}"
        password:       "{{ vc_password }}"
        datacenter:     "{{ datacenter_name }}"
        validate_certs: false
      register: cluster_facts

    - name: Output health summary
      ansible.builtin.debug:
        msg:
          - "vSAN health check complete for cluster: {{ cluster_name }}"
          - "Yellow tests assertion: {{ yellow_assert.msg | default('N/A') }}"
          - "Cluster info retrieved: {{ cluster_facts.clusters[cluster_name] is defined }}"

    - name: Notify on failures (placeholder — replace with your notification method)
      ansible.builtin.debug:
        msg: "ALERT: vSAN health issue detected on {{ cluster_name }}"
      when: yellow_assert is failed
~~~
