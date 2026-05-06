# Scripts

> Part of the [vCenter](../) reference.

---

## VM Health and Inventory Report (PowerShell / PowerCLI)

Connect to vCenter, enumerate all VMs, flag hygiene issues (stale snapshots, outdated Tools, missing backup tag), and export to CSV.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vcenter_vm_inventory.ps1
# Usage: pwsh -File vcenter_vm_inventory.ps1
# Env vars: VCENTER_HOST, VC_USER, VC_PASS

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS,
    [string]$CsvOutput   = "vm_inventory_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv",
    [int]$SnapAgeDays    = 7
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null

$now = Get-Date
$report = [System.Collections.Generic.List[PSObject]]::new()
$flagged = 0

foreach ($vm in (Get-VM | Sort-Object Name)) {
    $host    = $vm.VMHost.Name
    $cluster = (Get-Cluster -VMHost $vm.VMHost -ErrorAction SilentlyContinue).Name
    $ds      = ($vm | Get-Datastore | Select-Object -First 1).Name
    $snaps   = Get-Snapshot -VM $vm -ErrorAction SilentlyContinue
    $oldSnaps = @($snaps | Where-Object { ($now - $_.Created).TotalDays -gt $SnapAgeDays })
    $toolsStatus = $vm.ExtensionData.Guest.ToolsStatus
    $toolsVersion = $vm.ExtensionData.Guest.ToolsVersionStatus2
    $tags    = Get-TagAssignment -Entity $vm -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Tag | ForEach-Object { $_.Name }
    $hasBackupTag = ($tags -match 'backup') -as [bool]

    $flags = @()
    if ($toolsVersion -eq 'guestToolsNeedUpgrade') { $flags += 'ToolsOutdated' }
    if ($oldSnaps.Count -gt 0) { $flags += "OldSnaps:$($oldSnaps.Count)" }
    if (-not $hasBackupTag)    { $flags += 'NoBackupTag' }
    if ($vm.PowerState -eq 'PoweredOn' -and -not $vm.ExtensionData.Config.CpuHotAddEnabled) {
        $flags += 'CpuHotAddDisabled'
    }
    if ($flags) { $flagged++ }

    $provisionedGB = [Math]::Round($vm.ProvisionedSpaceGB, 1)
    $usedGB        = [Math]::Round($vm.UsedSpaceGB, 1)

    $row = [PSCustomObject]@{
        Name            = $vm.Name
        PowerState      = $vm.PowerState
        Host            = $host
        Cluster         = $cluster
        Datastore       = $ds
        vCPU            = $vm.NumCpu
        MemoryGB        = [Math]::Round($vm.MemoryGB, 1)
        ProvisionedGB   = $provisionedGB
        UsedGB          = $usedGB
        SnapshotCount   = $snaps.Count
        ToolsStatus     = $toolsStatus
        Flags           = $flags -join '; '
    }
    $report.Add($row)
}

$report | Export-Csv -Path $CsvOutput -NoTypeInformation
Write-Host "`nTotal VMs : $($report.Count)"
Write-Host "Flagged   : $flagged"
Write-Host "CSV saved : $CsvOutput"

Disconnect-VIServer -Confirm:$false
exit ($flagged -gt 0 ? 1 : 0)
~~~

---

## Cluster Capacity Report (PowerShell / PowerCLI)

Print a formatted table of CPU and memory utilization per cluster, including HA overhead and VM density, and warn above 80%.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vcenter_cluster_capacity.ps1
# Usage: pwsh -File vcenter_cluster_capacity.ps1

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS,
    [int]$WarnPercent    = 80
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null

$header = "{0,-30} {1,6} {2,6} {3,8} {4,8} {5,8} {6,8} {7,6} {8,6} {9}"
$divider = "-" * 95
Write-Host ($header -f "Cluster", "Hosts", "VMs", "CPU GHz", "CPU Used", "CPU%", "Mem GB", "Mem Used", "Mem%", "Status")
Write-Host $divider

$overallExit = 0

foreach ($cluster in (Get-Cluster | Sort-Object Name)) {
    $hosts = Get-VMHost -Location $cluster
    $vms   = Get-VM -Location $cluster

    $totalCpuGHz  = [Math]::Round(($hosts | Measure-Object -Property CpuTotalMhz -Sum).Sum / 1000, 1)
    $usedCpuGHz   = [Math]::Round(($hosts | Measure-Object -Property CpuUsageMhz -Sum).Sum / 1000, 1)
    $cpuPct       = if ($totalCpuGHz -gt 0) { [Math]::Round($usedCpuGHz / $totalCpuGHz * 100, 1) } else { 0 }

    $totalMemGB   = [Math]::Round(($hosts | Measure-Object -Property MemoryTotalGB -Sum).Sum, 1)
    $usedMemGB    = [Math]::Round(($hosts | Measure-Object -Property MemoryUsageGB -Sum).Sum, 1)
    $memPct       = if ($totalMemGB -gt 0) { [Math]::Round($usedMemGB / $totalMemGB * 100, 1) } else { 0 }

    $status = "OK"
    if ($cpuPct -ge $WarnPercent -or $memPct -ge $WarnPercent) {
        $status = "WARNING"
        $overallExit = 1
    }

    Write-Host ($header -f $cluster.Name, $hosts.Count, $vms.Count,
        $totalCpuGHz, $usedCpuGHz, "${cpuPct}%",
        $totalMemGB, $usedMemGB, "${memPct}%", $status)

    # vSAN datastore (if present)
    $vsanDs = Get-Datastore -Location $cluster | Where-Object { $_.Type -eq 'vsan' }
    foreach ($ds in $vsanDs) {
        $dsPct = [Math]::Round((1 - $ds.FreeSpaceGB / $ds.CapacityGB) * 100, 1)
        $dsStat = if ($dsPct -ge $WarnPercent) { "WARNING" } else { "OK" }
        Write-Host ("  vSAN: {0}  Used={1}%  Free={2:N0}GB  [{3}]" -f $ds.Name, $dsPct, $ds.FreeSpaceGB, $dsStat)
        if ($dsStat -eq "WARNING") { $overallExit = 1 }
    }
}

Write-Host $divider
Disconnect-VIServer -Confirm:$false
exit $overallExit
~~~

---

## Snapshot Cleanup Report (PowerShell / PowerCLI)

List all VM snapshots sorted by age, flag those older than 3 days, and optionally remove them after a confirmation prompt.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vcenter_snapshot_cleanup.ps1
# Usage: pwsh -File vcenter_snapshot_cleanup.ps1 [--remove]

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS,
    [switch]$Remove,
    [int]$FlagAgeDays = 3,
    [string]$LogFile  = "snapshot_cleanup_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null

$now = Get-Date
$allSnaps = Get-VM | Get-Snapshot | Sort-Object Created

if (-not $allSnaps) {
    Write-Host "No snapshots found."
    Disconnect-VIServer -Confirm:$false
    exit 0
}

$header = "{0,-30} {1,-30} {2,-20} {3,6} {4,10} {5}"
Write-Host ($header -f "VM", "Snapshot", "Created", "Age(d)", "Size(GB)", "Flag")
Write-Host ("-" * 110)

$toRemove = [System.Collections.Generic.List[object]]::new()

foreach ($snap in $allSnaps) {
    $ageDays = [Math]::Floor(($now - $snap.Created).TotalDays)
    $sizeGB  = [Math]::Round($snap.SizeGB, 2)
    $flag    = if ($ageDays -ge $FlagAgeDays) { "OLD" } else { "" }
    Write-Host ($header -f $snap.VM.Name, $snap.Name,
        $snap.Created.ToString('yyyy-MM-dd HH:mm'), $ageDays, $sizeGB, $flag)
    if ($flag -eq "OLD") { $toRemove.Add($snap) }
}

Write-Host "`nTotal snapshots : $($allSnaps.Count)"
Write-Host "Flagged (>= $FlagAgeDays days): $($toRemove.Count)"

if ($Remove -and $toRemove.Count -gt 0) {
    Write-Host "`nWARNING: About to remove $($toRemove.Count) snapshot(s)." -ForegroundColor Yellow
    $confirm = Read-Host "Type 'YES' to proceed"
    if ($confirm -eq 'YES') {
        foreach ($snap in $toRemove) {
            Write-Host "Removing: $($snap.VM.Name) / $($snap.Name)"
            $logEntry = "$(Get-Date -Format 'o')  REMOVE  VM=$($snap.VM.Name)  Snap=$($snap.Name)  Age=$([Math]::Floor(($now - $snap.Created).TotalDays))d"
            $logEntry | Out-File -FilePath $LogFile -Append
            Remove-Snapshot -Snapshot $snap -Confirm:$false -ErrorAction Continue
        }
        Write-Host "Done. Log: $LogFile"
    } else {
        Write-Host "Aborted."
    }
}

Disconnect-VIServer -Confirm:$false
exit ($toRemove.Count -gt 0 ? 1 : 0)
~~~

---

## vCenter Health Check (Python / pyVmomi)

Connect to vCenter via pyVmomi and the REST API, check service health, host connectivity, datastore status, and recent task errors.

~~~python
#!/usr/bin/env python3
"""
vcenter_health.py
Usage: python3 vcenter_health.py
Deps: pip install pyVmomi requests
"""

import os, ssl, sys, requests
from urllib3.exceptions import InsecureRequestWarning
from pyVim.connect  import SmartConnect, Disconnect
from pyVmomi        import vim

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VCENTER_HOST = os.environ.get("VCENTER_HOST", "vcenter.local")
VC_USER      = os.environ.get("VC_USER",      "administrator@vsphere.local")
VC_PASS      = os.environ.get("VC_PASS",      "")

overall = 0

def check(label, status, detail=""):
    global overall
    colours = {"PASS": "\033[32m", "WARNING": "\033[33m", "CRITICAL": "\033[31m"}
    reset = "\033[0m"
    c = colours.get(status, "")
    print(f"  {c}[{status:<8}]{reset} {label:<40} {detail}")
    if status == "CRITICAL": overall = max(overall, 2)
    if status == "WARNING":  overall = max(overall, 1)


print(f"\n=== vCenter Health Dashboard: {VCENTER_HOST} ===\n")

# --- REST API: system health ---
try:
    session = requests.Session()
    session.verify = False
    auth_url  = f"https://{VCENTER_HOST}/api/session"
    token_resp = session.post(auth_url, auth=(VC_USER, VC_PASS))
    token_resp.raise_for_status()
    token = token_resp.json()
    session.headers.update({"vmware-api-session-id": token})

    health_resp = session.get(f"https://{VCENTER_HOST}/api/vcenter/health/system")
    if health_resp.ok:
        h = health_resp.json()
        status = "PASS" if h.get("health_status") == "green" else "WARNING"
        check("vCenter system health (REST)", status, h.get("health_status", "unknown"))
    else:
        check("vCenter system health (REST)", "WARNING", f"HTTP {health_resp.status_code}")
except Exception as e:
    check("vCenter system health (REST)", "WARNING", str(e)[:80])

# --- pyVmomi: host connectivity ---
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode    = ssl.CERT_NONE
si = SmartConnect(host=VCENTER_HOST, user=VC_USER, pwd=VC_PASS, sslContext=context)
content = si.RetrieveContent()

container = content.viewManager.CreateContainerView(
    content.rootFolder, [vim.HostSystem], True
)
hosts = container.view
container.Destroy()

connected    = [h for h in hosts if h.runtime.connectionState == "connected"]
disconnected = [h for h in hosts if h.runtime.connectionState != "connected"]

check("ESXi hosts connected",    "PASS"     if not disconnected else "CRITICAL",
      f"{len(connected)}/{len(hosts)} connected")
for h in disconnected:
    check(f"  Host: {h.name}", "CRITICAL", h.runtime.connectionState)

# --- Datastores ---
ds_container = content.viewManager.CreateContainerView(
    content.rootFolder, [vim.Datastore], True
)
datastores = ds_container.view
ds_container.Destroy()

inaccessible = [ds for ds in datastores if not ds.summary.accessible]
check("Datastores accessible",
      "PASS" if not inaccessible else "CRITICAL",
      f"{len(datastores) - len(inaccessible)}/{len(datastores)} accessible")
for ds in inaccessible:
    check(f"  Datastore: {ds.name}", "CRITICAL", "not accessible")

# --- Recent tasks with errors ---
tm = content.taskManager
recent_tasks = tm.recentTask
task_errors = [t for t in recent_tasks if t.info.state == "error"]
check("Recent task errors", "PASS" if not task_errors else "WARNING",
      f"{len(task_errors)} failed task(s) in recent history")

Disconnect(si)

print(f"\nOverall: {'PASS' if overall == 0 else 'WARNING' if overall == 1 else 'CRITICAL'}")
sys.exit(overall)
~~~

---

## Ansible vCenter Operational Playbook

Use the `community.vmware` collection to check cluster capacity, vSAN health, snapshot counts, and datastore free space — asserting no datastores are below 20% free.

~~~yaml
---
# vcenter_operational.yml
# Usage: ansible-playbook -i inventory vcenter_operational.yml
# Deps: ansible-galaxy collection install community.vmware
# Vars: vcenter_hostname, datacenter_name, vc_username, vc_password

- name: vCenter Operational Health Check
  hosts: localhost
  gather_facts: false
  vars:
    vcenter_hostname: vcenter.local
    datacenter_name:  Production
    vc_username:      "{{ lookup('env','VC_USER') }}"
    vc_password:      "{{ lookup('env','VC_PASS') }}"
    ds_free_min_pct:  20

  tasks:

    - name: Gather cluster facts
      community.vmware.vmware_cluster_info:
        hostname:       "{{ vcenter_hostname }}"
        username:       "{{ vc_username }}"
        password:       "{{ vc_password }}"
        datacenter:     "{{ datacenter_name }}"
        validate_certs: false
      register: cluster_facts

    - name: Show cluster summary
      ansible.builtin.debug:
        msg: "Clusters found: {{ cluster_facts.clusters | list }}"

    - name: Check vSAN cluster health
      community.vmware.vmware_vsan_health_info:
        hostname:       "{{ vcenter_hostname }}"
        username:       "{{ vc_username }}"
        password:       "{{ vc_password }}"
        cluster_name:   "{{ item }}"
        validate_certs: false
      loop: "{{ cluster_facts.clusters | list }}"
      register: vsan_health
      failed_when: false

    - name: Gather datastore facts
      community.vmware.vmware_datastore_info:
        hostname:       "{{ vcenter_hostname }}"
        username:       "{{ vc_username }}"
        password:       "{{ vc_password }}"
        datacenter:     "{{ datacenter_name }}"
        validate_certs: false
      register: datastore_facts

    - name: Assert no datastores below minimum free space
      ansible.builtin.assert:
        that: >
          ((item.freeSpace | float) / (item.capacity | float) * 100) >= {{ ds_free_min_pct }}
        fail_msg: >
          Datastore {{ item.name }} is below {{ ds_free_min_pct }}% free
          ({{ ((item.freeSpace | float) / (item.capacity | float) * 100) | round(1) }}% free)
        success_msg: "{{ item.name }} OK"
      loop: "{{ datastore_facts.datastores }}"
      when: item.capacity | int > 0

    - name: Gather snapshot info across all VMs
      community.vmware.vmware_vm_info:
        hostname:       "{{ vcenter_hostname }}"
        username:       "{{ vc_username }}"
        password:       "{{ vc_password }}"
        validate_certs: false
        vm_type:        vm
      register: vm_info

    - name: Report VMs with snapshots
      ansible.builtin.debug:
        msg: "VM with snapshots: {{ item.guest_name }}"
      loop: "{{ vm_info.virtual_machines }}"
      when: item.snapshots is defined and item.snapshots | length > 0
~~~
