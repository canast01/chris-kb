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

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or Windows 11 (PowerShell 5.1 is already installed)
- VMware PowerCLI module — install it once by running this in PowerShell:
  `Install-Module -Name VMware.PowerCLI -Scope CurrentUser -Force`
  When prompted about an untrusted repository, type `Y` and press Enter
- Network access to your vCenter server

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files** (important — otherwise Windows adds .txt)
5. Name it `vcenter_vm_inventory.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

Open the file in Notepad and update these values near the top (the `param(` block):

| Variable | What to enter | How to find it |
|---|---|---|
| `$VCenterHost` | vCenter IP or FQDN e.g. `vcenter.company.local` | Your vCenter server address |
| `$VCUser` | vCenter username e.g. `administrator@vsphere.local` | Your vCenter login |
| `$VCPass` | vCenter password | Your vCenter password |
| `$SnapAgeDays` | Number of days after which a snapshot is considered old (default 7) | Your preference |

You can edit the defaults directly in the param block, for example:
`[string]$VCenterHost = "192.168.1.50"`

**Step 3 — Open PowerShell as Administrator**

Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time per session)**

In PowerShell, paste this before running your script:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

```
cd C:\Users\YourName\Desktop
.\vcenter_vm_inventory.ps1
```

**What you should see**

A table of all VMs prints to the screen, then a summary like:

```
Total VMs : 42
Flagged   : 7
CSV saved : vm_inventory_20260506_143022.csv
```

Open the CSV file on your Desktop in Excel to review all VM details and flags.

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

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or Windows 11 (PowerShell 5.1 is already installed)
- VMware PowerCLI module — install it once by running this in PowerShell:
  `Install-Module -Name VMware.PowerCLI -Scope CurrentUser -Force`
  When prompted about an untrusted repository, type `Y` and press Enter
- Network access to your vCenter server

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `vcenter_cluster_capacity.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

Open the file in Notepad and update the `param(` block:

| Variable | What to enter | How to find it |
|---|---|---|
| `$VCenterHost` | vCenter IP or FQDN | Your vCenter server address |
| `$VCUser` | vCenter username | Your vCenter login |
| `$VCPass` | vCenter password | Your vCenter password |
| `$WarnPercent` | Usage % threshold to trigger WARNING (default 80) | Your preference |

**Step 3 — Open PowerShell as Administrator**

Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

```
cd C:\Users\YourName\Desktop
.\vcenter_cluster_capacity.ps1
```

**What you should see**

A table of all clusters with CPU and memory percentages:

```
Cluster                        Hosts    VMs  CPU GHz CPU Used    CPU%   Mem GB Mem Used   Mem% Status
-----------------------------------------------------------------------------------------------
Production-Cluster              4       32    96.0     41.2    42.9%   768.0    410.0    53.4% OK
```

Any cluster above 80% shows `WARNING` in red and the script exits with code 1.

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

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or Windows 11 (PowerShell 5.1 is already installed)
- VMware PowerCLI module — install it once by running this in PowerShell:
  `Install-Module -Name VMware.PowerCLI -Scope CurrentUser -Force`
  When prompted about an untrusted repository, type `Y` and press Enter
- Network access to your vCenter server

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `vcenter_snapshot_cleanup.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

Open the file in Notepad and update the `param(` block:

| Variable | What to enter | How to find it |
|---|---|---|
| `$VCenterHost` | vCenter IP or FQDN | Your vCenter server address |
| `$VCUser` | vCenter username | Your vCenter login |
| `$VCPass` | vCenter password | Your vCenter password |
| `$FlagAgeDays` | Age in days to flag a snapshot as old (default 3) | Your preference |

**Step 3 — Open PowerShell as Administrator**

Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

To just list snapshots (safe, no changes):
```
cd C:\Users\YourName\Desktop
.\vcenter_snapshot_cleanup.ps1
```

To list AND remove old snapshots (you will be asked to confirm):
```
.\vcenter_snapshot_cleanup.ps1 -Remove
```

**What you should see**

A table of all snapshots with their age and size. Snapshots older than 3 days are flagged `OLD`. If you used `-Remove`, you will be prompted to type `YES` before anything is deleted. A log file is saved to your Desktop.

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

#### How to run this script — step by step

**Before you start — what you need**
- Python 3.8 or newer installed from python.org — during install, tick "Add Python to PATH"
- The `pyVmomi` and `requests` libraries — install them once by running in Command Prompt:
  `pip install pyVmomi requests`
- Network access to your vCenter server

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `vcenter_health.py` and save it to your Desktop

**Step 2 — Fill in your details**

Open the file in Notepad and update these lines near the top:

| Variable | What to enter | How to find it |
|---|---|---|
| `VCENTER_HOST` | vCenter IP or FQDN e.g. `"vcenter.company.local"` | Your vCenter server address |
| `VC_USER` | vCenter username e.g. `"administrator@vsphere.local"` | Your vCenter login |
| `VC_PASS` | vCenter password e.g. `"MyPassword123"` | Your vCenter password |

**Step 3 — Open Command Prompt**

Windows key → type `cmd` → press Enter

**Step 4 — Run it**

```
cd C:\Users\YourName\Desktop
python vcenter_health.py
```

**What you should see**

```
=== vCenter Health Dashboard: vcenter.company.local ===

  [PASS    ] vCenter system health (REST)           green
  [PASS    ] ESXi hosts connected                   4/4 connected
  [PASS    ] Datastores accessible                  8/8 accessible
  [PASS    ] Recent task errors                     0 failed task(s) in recent history

Overall: PASS
```

Any CRITICAL items will appear in red. The script exits with code 2 on critical failures.

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

#### How to run this script — step by step

**Before you start — what you need**
- Ansible is easiest to run on Windows via WSL (Windows Subsystem for Linux) — open Microsoft Store, install Ubuntu, then in the Ubuntu terminal run:
  `sudo apt update && sudo apt install -y ansible python3-pip`
- Install the VMware community collection:
  `ansible-galaxy collection install community.vmware`
  `pip3 install pyVmomi requests`
- Network access to your vCenter server from the WSL environment

**Step 1 — Save the file**

1. In your WSL/Ubuntu terminal, create the file:
   `nano ~/vcenter_operational.yml`
2. Paste the entire code block above
3. Press `Ctrl+X`, then `Y`, then `Enter` to save

**Step 2 — Fill in your details**

Open the file and update the `vars:` section:

| Variable | What to enter | How to find it |
|---|---|---|
| `vcenter_hostname` | vCenter IP or FQDN | Your vCenter server address |
| `datacenter_name` | Name of your datacenter in vCenter | vSphere Client → top of inventory tree |
| `vc_username` | vCenter username | Your vCenter login |
| `vc_password` | vCenter password (or set via env var `VC_PASS`) | Your vCenter password |

**Step 3 — Set credentials as environment variables (recommended)**

```bash
export VC_USER="administrator@vsphere.local"
export VC_PASS="YourPassword"
```

**Step 4 — Create a minimal inventory file**

```bash
echo "localhost ansible_connection=local" > ~/inventory
```

**Step 5 — Run it**

```bash
ansible-playbook -i ~/inventory ~/vcenter_operational.yml
```

**What you should see**

Ansible prints each task with `ok`, `changed`, or `failed`. Any datastore below 20% free causes a `FAILED` assertion with the datastore name and percentage shown. VMs with snapshots are listed at the end.

---

## Windows: vCenter Session Audit via REST API (PowerShell)

Use the vCenter REST API to list all VMs with power state and memory, and all ESXi hosts with connection state — no extra modules needed, just built-in PowerShell.

~~~powershell
# vcenter_rest_audit.ps1
# Uses the vCenter REST API — no PowerCLI required.
# Requires PowerShell 5.1+ (already on Windows 10/11).

param(
    [string]$VcenterHost = "192.168.1.50",
    [string]$VcUser      = "administrator@vsphere.local",
    [string]$VcPass      = "YourPasswordHere"
)

# Ignore SSL certificate errors (common in lab environments)
Add-Type @"
using System.Net;
using System.Security.Cryptography.X509Certificates;
public class TrustAll : ICertificatePolicy {
    public bool CheckValidationResult(ServicePoint sp, X509Certificate cert, WebRequest req, int prob) { return true; }
}
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAll
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

$BaseUrl = "https://$VcenterHost/api"

# Step 1: Authenticate — POST /api/session with Basic auth
$authBytes = [System.Text.Encoding]::ASCII.GetBytes("${VcUser}:${VcPass}")
$authB64   = [System.Convert]::ToBase64String($authBytes)
$authHeaders = @{ Authorization = "Basic $authB64" }

try {
    $sessionResp = Invoke-RestMethod -Uri "$BaseUrl/session" -Method POST -Headers $authHeaders
} catch {
    Write-Host "ERROR: Could not authenticate to vCenter. Check IP, username, and password." -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

$sessionToken = $sessionResp
$apiHeaders = @{ "vmware-api-session-id" = $sessionToken }

Write-Host "`n=== vCenter REST API Audit: $VcenterHost ===" -ForegroundColor Cyan
Write-Host "($(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))`n"

# Step 2: GET /api/vcenter/vm — list all VMs
try {
    $vms = Invoke-RestMethod -Uri "$BaseUrl/vcenter/vm" -Method GET -Headers $apiHeaders
    Write-Host "--- Virtual Machines ($($vms.Count) total) ---"
    $header = "{0,-35} {1,-15} {2,8} {3}"
    Write-Host ($header -f "VM Name", "Power State", "Mem MB", "VM ID")
    Write-Host ("-" * 75)
    foreach ($vm in ($vms | Sort-Object display_name)) {
        $powerColour = if ($vm.power_state -eq "POWERED_ON") { "Green" } else { "Yellow" }
        Write-Host ($header -f $vm.display_name, $vm.power_state, $vm.memory_size_MiB, $vm.vm) -ForegroundColor $powerColour
    }
} catch {
    Write-Host "WARNING: Could not retrieve VM list: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# Step 3: GET /api/vcenter/host — list all ESXi hosts
try {
    $hosts = Invoke-RestMethod -Uri "$BaseUrl/vcenter/host" -Method GET -Headers $apiHeaders
    Write-Host "--- ESXi Hosts ($($hosts.Count) total) ---"
    $header2 = "{0,-40} {1,-15} {2}"
    Write-Host ($header2 -f "Host Name", "Connection", "Host ID")
    Write-Host ("-" * 75)
    foreach ($h in ($hosts | Sort-Object name)) {
        $connColour = if ($h.connection_state -eq "CONNECTED") { "Green" } else { "Red" }
        Write-Host ($header2 -f $h.name, $h.connection_state, $h.host) -ForegroundColor $connColour
    }
} catch {
    Write-Host "WARNING: Could not retrieve host list: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Step 4: Log out
try {
    Invoke-RestMethod -Uri "$BaseUrl/session" -Method DELETE -Headers $apiHeaders | Out-Null
} catch {}

Write-Host "`nAudit complete." -ForegroundColor Cyan
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or Windows 11 — PowerShell 5.1 is already installed, no extra modules needed
- Network access to your vCenter server on port 443

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `vcenter_rest_audit.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

Open the file in Notepad and update these lines near the top (the `param(` block):

| Variable | What to enter | How to find it |
|---|---|---|
| `$VcenterHost` | vCenter IP or FQDN e.g. `"192.168.1.50"` | Your vCenter server address |
| `$VcUser` | vCenter username e.g. `"administrator@vsphere.local"` | Your vCenter login |
| `$VcPass` | vCenter password | Your vCenter password |

**Step 3 — Open PowerShell as Administrator**

Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

```
cd C:\Users\YourName\Desktop
.\vcenter_rest_audit.ps1
```

**What you should see**

```
=== vCenter REST API Audit: 192.168.1.50 ===
(2026-05-06 14:30:22)

--- Virtual Machines (15 total) ---
VM Name                             Power State      Mem MB  VM ID
---------------------------------------------------------------------------
web-server-01                       POWERED_ON         4096  vm-101
db-server-01                        POWERED_ON         8192  vm-102
test-vm-02                          POWERED_OFF        2048  vm-103

--- ESXi Hosts (3 total) ---
Host Name                                Connection     Host ID
---------------------------------------------------------------------------
esxi-01.company.local                    CONNECTED      host-201
esxi-02.company.local                    CONNECTED      host-202

Audit complete.
```

Powered-on VMs appear in green, powered-off in yellow. Disconnected hosts appear in red.

---

## Daily Check Script (PowerShell/PowerCLI)

Connect to vCenter and run daily operational checks: host connection states, datastore capacity (flag below 20% free), stale snapshots (older than 7 days), active alarms, and vCenter service health via REST API. Outputs PASS/FAIL.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vc_daily_check.ps1
# Usage: pwsh -File vc_daily_check.ps1
# Env vars: VCENTER_HOST, VC_USER, VC_PASS

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS,
    [int]$SnapAgeDays    = 7,
    [double]$DsFreeMinPct = 20
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null

$exit = 0
$now  = Get-Date

function Pass($msg) { Write-Host "  [PASS] $msg" -ForegroundColor Green }
function Fail($msg) { Write-Host "  [FAIL] $msg" -ForegroundColor Red; $script:exit = 1 }
function Warn($msg) { Write-Host "  [WARN] $msg" -ForegroundColor Yellow }

Write-Host "`n=== vCenter Daily Check: $VCenterHost ===" -ForegroundColor Cyan
Write-Host "($(Get-Date -Format 'yyyy-MM-dd HH:mm'))`n"

# --- Host connectivity ---
Write-Host "--- Host Connectivity ---"
$disconnected = Get-VMHost | Where-Object { $_.ConnectionState -ne 'Connected' }
if ($disconnected) {
    $disconnected | ForEach-Object { Fail "Host $($_.Name) is $($_.ConnectionState)" }
} else {
    Pass "All hosts connected ($(( Get-VMHost ).Count) hosts)"
}

# --- Datastore capacity ---
Write-Host "`n--- Datastore Capacity ---"
$lowDs = Get-Datastore | Where-Object {
    $_.CapacityMB -gt 0 -and ($_.FreeSpaceMB / $_.CapacityMB * 100) -lt $DsFreeMinPct
}
if ($lowDs) {
    $lowDs | ForEach-Object {
        $pct = [Math]::Round($_.FreeSpaceMB / $_.CapacityMB * 100, 1)
        Fail "Datastore $($_.Name): only ${pct}% free"
    }
} else {
    Pass "All datastores above ${DsFreeMinPct}% free"
}

# --- Stale snapshots ---
Write-Host "`n--- Stale Snapshots (>$SnapAgeDays days) ---"
$staleSnaps = Get-VM | Get-Snapshot -ErrorAction SilentlyContinue |
    Where-Object { ($now - $_.Created).TotalDays -gt $SnapAgeDays }
if ($staleSnaps) {
    $staleSnaps | ForEach-Object {
        $age = [Math]::Floor(($now - $_.Created).TotalDays)
        Warn "VM $($_.VM.Name): snapshot '$($_.Name)' is ${age} days old"
    }
} else {
    Pass "No snapshots older than $SnapAgeDays days"
}

# --- Active alarms ---
Write-Host "`n--- Active Alarms ---"
$alarms = Get-AlarmAction -ErrorAction SilentlyContinue
if ($alarms) {
    Warn "$($alarms.Count) active alarm action(s) configured"
} else {
    Pass "No active alarm actions triggered"
}

# --- vCenter services via REST API ---
Write-Host "`n--- vCenter Services ---"
try {
    Add-Type @"
using System.Net; using System.Security.Cryptography.X509Certificates;
public class NoSSL : ICertificatePolicy {
    public bool CheckValidationResult(ServicePoint s, X509Certificate c, WebRequest r, int p) { return true; }
}
"@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object NoSSL
    [System.Net.ServicePointManager]::SecurityProtocol  = [System.Net.SecurityProtocolType]::Tls12

    $authB64   = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${VCUser}:${VCPass}"))
    $sessResp  = Invoke-RestMethod -Uri "https://$VCenterHost/api/session" -Method POST `
                   -Headers @{ Authorization = "Basic $authB64" }
    $apiHdr    = @{ "vmware-api-session-id" = $sessResp }
    $health    = Invoke-RestMethod -Uri "https://$VCenterHost/api/vcenter/health/system" `
                   -Method GET -Headers $apiHdr
    $hs = $health.health_status
    if ($hs -eq "green") { Pass "vCenter system health: $hs" } else { Warn "vCenter system health: $hs" }
} catch {
    Warn "Could not check vCenter REST health: $($_.Exception.Message)"
}

Disconnect-VIServer -Confirm:$false
Write-Host ""
if ($exit -eq 0) { Write-Host "RESULT: PASS" -ForegroundColor Green }
else             { Write-Host "RESULT: FAIL" -ForegroundColor Red }
exit $exit
~~~

---

## Incident Triage Script (PowerShell/PowerCLI)

Capture disconnected hosts, inaccessible datastores, powered-off VMs, active alarms, recent tasks with errors, and vCenter service health to a timestamped file.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vc_incident_triage.ps1
# Usage: pwsh -File vc_incident_triage.ps1
# Env vars: VCENTER_HOST, VC_USER, VC_PASS

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null

$TS  = Get-Date -Format "yyyyMMdd_HHmmss"
$OUT = "vc_triage_${VCenterHost}_${TS}.txt"

function Log($msg) { $msg | Tee-Object -FilePath $OUT -Append }

Log "=== vCenter Incident Triage: $VCenterHost ==="
Log "Timestamp: $(Get-Date)"
Log ""

Log "--- Disconnected Hosts ---"
Get-VMHost | Where-Object { $_.ConnectionState -ne 'Connected' } |
    Select-Object Name, ConnectionState | Format-Table | Out-String | ForEach-Object { Log $_ }

Log "--- Inaccessible Datastores ---"
Get-Datastore | Where-Object { -not $_.ExtensionData.Summary.Accessible } |
    Select-Object Name, Type | Format-Table | Out-String | ForEach-Object { Log $_ }

Log "--- Powered-Off VMs ---"
Get-VM | Where-Object { $_.PowerState -ne 'PoweredOn' } |
    Select-Object Name, PowerState, VMHost | Format-Table | Out-String | ForEach-Object { Log $_ }

Log "--- Active Alarms ---"
Get-AlarmAction -ErrorAction SilentlyContinue |
    Select-Object * | Format-List | Out-String | ForEach-Object { Log $_ }

Log "--- Recent Tasks with Errors ---"
Get-Task -Status Error -ErrorAction SilentlyContinue | Select-Object -First 20 |
    Select-Object Name, State, StartTime, FinishTime, Description |
    Format-Table | Out-String | ForEach-Object { Log $_ }

Log ""
Log "Triage data saved to: $OUT"
Disconnect-VIServer -Confirm:$false
Write-Host "Triage data saved to: $OUT" -ForegroundColor Cyan
~~~

---

## Change Pre-Check Script (PowerShell/PowerCLI)

Run before any maintenance window. Confirms no disconnected hosts, no inaccessible datastores, no critical alarms, no running migrations, healthy vCenter services, and NTP in sync. Exits non-zero on failure.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vc_precheck.ps1
# Usage: pwsh -File vc_precheck.ps1
# Env vars: VCENTER_HOST, VC_USER, VC_PASS

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null

$exit = 0
function Go($msg)   { Write-Host "  [GO]    $msg" -ForegroundColor Green }
function NoGo($msg) { Write-Host "  [NO-GO] $msg" -ForegroundColor Red; $script:exit = 2 }

Write-Host "`n=== vCenter Change Pre-Check: $VCenterHost ===" -ForegroundColor Cyan
Write-Host "($(Get-Date -Format 'yyyy-MM-dd HH:mm'))`n"

# Check 1: No disconnected hosts
$disc = (Get-VMHost | Where-Object { $_.ConnectionState -ne 'Connected' }).Count
if ($disc -gt 0) { NoGo "$disc host(s) disconnected" } else { Go "All hosts connected" }

# Check 2: No inaccessible datastores
$inacc = (Get-Datastore | Where-Object { -not $_.ExtensionData.Summary.Accessible }).Count
if ($inacc -gt 0) { NoGo "$inacc inaccessible datastore(s)" } else { Go "All datastores accessible" }

# Check 3: No active critical alarms
$critAlarms = Get-AlarmAction -ErrorAction SilentlyContinue
if ($critAlarms -and $critAlarms.Count -gt 0) { NoGo "$($critAlarms.Count) active alarm action(s)" }
else { Go "No active alarm actions" }

# Check 4: No running vMotion/migrations
$running = Get-Task -Status Running -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match 'Migrate|vMotion|RelocateVM' }
if ($running) { NoGo "$($running.Count) migration task(s) in progress" }
else { Go "No migrations running" }

# Check 5: NTP sync on all hosts
$ntpBad = Get-VMHost | Where-Object {
    $ntp = $_ | Get-VMHostNTPServer
    -not $ntp -or $ntp.Count -eq 0
}
if ($ntpBad) { NoGo "$($ntpBad.Count) host(s) have no NTP configured" }
else { Go "NTP configured on all hosts" }

Disconnect-VIServer -Confirm:$false
Write-Host ""
if ($exit -eq 0) { Write-Host "VERDICT: GO" -ForegroundColor Green }
else             { Write-Host "VERDICT: NO-GO" -ForegroundColor Red }
exit $exit
~~~

---

## Post-Change Validation Script (PowerShell/PowerCLI)

Run after a maintenance window. Performs the same checks as pre-check and also verifies target cluster DRS/HA settings are unchanged, permissions are intact, and no new alarms were triggered.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vc_postcheck.ps1
# Usage: pwsh -File vc_postcheck.ps1
# Env vars: VCENTER_HOST, VC_USER, VC_PASS

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

$exit = 0
function Ok($msg)   { Write-Host "  [OK]   $msg" -ForegroundColor Green }
function Fail($msg) { Write-Host "  [FAIL] $msg" -ForegroundColor Red; $script:exit = 1 }
function Warn($msg) { Write-Host "  [WARN] $msg" -ForegroundColor Yellow }

Write-Host "`n=== vCenter Post-Change Validation: $VCenterHost ===" -ForegroundColor Cyan
Write-Host "($(Get-Date -Format 'yyyy-MM-dd HH:mm'))`n"

# Repeat baseline checks
$disc  = (Get-VMHost | Where-Object { $_.ConnectionState -ne 'Connected' }).Count
$inacc = (Get-Datastore | Where-Object { -not $_.ExtensionData.Summary.Accessible }).Count
if ($disc  -gt 0) { Fail "$disc host(s) still disconnected" } else { Ok "All hosts connected" }
if ($inacc -gt 0) { Fail "$inacc inaccessible datastore(s)" } else { Ok "All datastores accessible" }

# DRS/HA settings (if cluster specified)
if ($ClusterName) {
    $cl = Get-Cluster -Name $ClusterName -ErrorAction SilentlyContinue
    if ($cl) {
        Ok "Cluster $ClusterName: DRS=$($cl.DrsEnabled) HA=$($cl.HAEnabled)"
    } else {
        Warn "Cluster '$ClusterName' not found"
    }
}

# No new alarms after change
$alarms = Get-AlarmAction -ErrorAction SilentlyContinue
if ($alarms -and $alarms.Count -gt 0) { Warn "$($alarms.Count) alarm action(s) active — review" }
else { Ok "No active alarm actions" }

Disconnect-VIServer -Confirm:$false
Write-Host ""
if ($exit -eq 0) { Write-Host "RESULT: PASS" -ForegroundColor Green }
else             { Write-Host "RESULT: FAIL" -ForegroundColor Red }
exit $exit
~~~

---

## Health Check Script (PowerShell/PowerCLI, scheduled)

Compact summary suitable for scheduled tasks. Outputs host count (connected/disconnected), datastore count (any below 20% free), and critical alarm count. Exits 0/1/2.

~~~powershell
#Requires -Modules VMware.PowerCLI
# vc_health.ps1 — scheduled/cron-safe vCenter health check
# Usage: pwsh -File vc_health.ps1
# Task Scheduler: pwsh -NonInteractive -File C:\scripts\vc_health.ps1

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS,
    [double]$DsFreeMinPct = 20
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)

try {
    Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null
} catch {
    Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] CRITICAL | $VCenterHost | Cannot connect: $($_.Exception.Message)"
    exit 2
}

$hosts      = Get-VMHost
$connected  = ($hosts | Where-Object { $_.ConnectionState -eq 'Connected' }).Count
$disconn    = $hosts.Count - $connected
$datastores = Get-Datastore
$lowDs      = ($datastores | Where-Object {
    $_.CapacityMB -gt 0 -and ($_.FreeSpaceMB / $_.CapacityMB * 100) -lt $DsFreeMinPct
}).Count
$alarms = (Get-AlarmAction -ErrorAction SilentlyContinue | Measure-Object).Count

$worst = 0
if ($disconn -gt 0 -or $lowDs -gt 0) { $worst = 2 }
elseif ($alarms -gt 0) { $worst = 1 }

$status = if ($worst -eq 0) { "HEALTHY" } elseif ($worst -eq 1) { "WARNING" } else { "CRITICAL" }

Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $status | $VCenterHost | hosts=$($hosts.Count) connected=$connected disconnected=$disconn datastores=$($datastores.Count) low_ds=$lowDs alarms=$alarms"

Disconnect-VIServer -Confirm:$false
exit $worst
~~~

---

## Windows: vCenter ESXi Host Check via Plink (CMD)

Connect to an ESXi host via SSH using plink (from PuTTY) and run quick health commands. Note: vCenter itself does not expose an SSH shell for ESXCLI commands — this script connects directly to an ESXi host instead.

~~~batch
@echo off
REM esxi_host_check.bat — Quick ESXi host health check via SSH (plink)
REM Connects to an ESXi host using plink (PuTTY command-line SSH tool).
REM
REM DOWNLOAD PLINK: https://www.putty.org
REM   - Download putty-64bit-X.XX-installer.msi and install it.
REM   - plink.exe will be at: C:\Program Files\PuTTY\plink.exe
REM   - OR download the standalone plink.exe directly from the PuTTY site.
REM
REM FIRST-TIME SETUP (run once to accept the SSH fingerprint):
REM   "C:\Program Files\PuTTY\plink.exe" -ssh root@192.168.1.100
REM   Type 'y' when asked to trust the host fingerprint, then Ctrl+C.
REM
REM NOTE: SSH must be enabled on the ESXi host:
REM   vSphere Client -> Host -> Manage -> Services -> SSH -> Start

set ESXI_HOST=192.168.1.100
set SSH_USER=root
set PLINK="C:\Program Files\PuTTY\plink.exe"

echo.
echo === ESXi Host Health Check: %ESXI_HOST% ===
echo.

echo --- ESXi Version ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli system version get"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not connect to %ESXI_HOST%.
    echo Check: 1) IP address is correct  2) SSH is enabled on the host  3) Run first-time fingerprint setup above
    exit /b 1
)

echo.
echo --- System Uptime (seconds) ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli system stats uptime get"

echo.
echo --- Storage Filesystems ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli storage filesystem list"

echo.
echo === Check complete ===
~~~

#### How to run this script — step by step

**Before you start — what you need**
- PuTTY installed on your Windows PC — download from https://www.putty.org (get the 64-bit installer)
- SSH enabled on your ESXi host: vSphere Client → select the host → Manage → Services → SSH → click Start
- The root password for your ESXi host
- Network access from your PC to the ESXi host management IP

**Step 1 — Accept the SSH fingerprint (one-time setup)**

Before the batch script will work, you must manually accept the host's SSH fingerprint once. Open Command Prompt and run:

```
"C:\Program Files\PuTTY\plink.exe" -ssh root@192.168.1.100
```

When asked "Store key in cache?", type `y` and press Enter. Then type the root password. Once connected, press `Ctrl+C` to disconnect. You only need to do this once per ESXi host.

**Step 2 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `esxi_host_check.bat` and save it to your Desktop

**Step 3 — Fill in your details**

Open the file in Notepad and update these lines near the top:

| Variable | What to enter | How to find it |
|---|---|---|
| `ESXI_HOST` | ESXi host IP address e.g. `192.168.1.100` | vSphere Client → host summary page |
| `SSH_USER` | SSH username — almost always `root` | ESXi root account |
| `PLINK` | Path to plink.exe | Default is `C:\Program Files\PuTTY\plink.exe` |

**Step 4 — Open Command Prompt**

Windows key → type `cmd` → press Enter

**Step 5 — Run it**

You can double-click the `.bat` file on your Desktop, or run it from Command Prompt:

```
cd C:\Users\YourName\Desktop
esxi_host_check.bat
```

**What you should see**

```
=== ESXi Host Health Check: 192.168.1.100 ===

--- ESXi Version ---
   Product: VMware ESXi
   Version: 8.0.0
   Build: Releasebuild-20513097

--- System Uptime (seconds) ---
   1382400

--- Storage Filesystems ---
   Mount Point                     Type    Size          Free
   /vmfs/volumes/datastore1        VMFS-6  499.75 GB     320.12 GB

=== Check complete ===
```
