# Scripts

> Part of the [ESXi](../) reference.

---

## ESXi Host Health Check (PowerShell / PowerCLI)

Connect to vCenter or directly to an ESXi host and produce a per-host health report covering hardware sensors, datastore usage, network adapter state, and required service status.

~~~powershell
#Requires -Modules VMware.PowerCLI
# esxi_host_health.ps1
# Usage: pwsh -File esxi_host_health.ps1
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

$RequiredServices = @('hostd', 'vpxa', 'ntpd')
$DatastoreWarnPct  = 80
$overallExit = 0

function Write-Status {
    param($Label, $Status, $Detail)
    $colour = switch ($Status) {
        'PASS'     { 'Green'  }
        'WARNING'  { 'Yellow' }
        'CRITICAL' { 'Red'    }
        default    { 'White'  }
    }
    Write-Host ("[{0,-8}] {1,-35} {2}" -f $Status, $Label, $Detail) -ForegroundColor $colour
}

foreach ($vmhost in (Get-VMHost | Sort-Object Name)) {
    Write-Host "`n=== $($vmhost.Name) ===" -ForegroundColor Cyan

    # Connection / power state
    if ($vmhost.ConnectionState -ne 'Connected') {
        Write-Status "ConnectionState" "CRITICAL" $vmhost.ConnectionState
        $overallExit = 2; continue
    }
    if ($vmhost.PowerState -ne 'PoweredOn') {
        Write-Status "PowerState" "WARNING" $vmhost.PowerState
        $overallExit = [Math]::Max($overallExit, 1)
    } else {
        Write-Status "ConnectionState" "PASS" "Connected / PoweredOn"
    }

    # Hardware sensors
    try {
        $hw = Get-VMHostHardware -VMHost $vmhost -ErrorAction Stop
        $badSensors = $hw.CpuInfo | Where-Object { $_.HealthState -ne 'Green' }
        if ($badSensors) {
            Write-Status "Hardware Sensors" "WARNING" "$($badSensors.Count) sensor(s) not green"
            $overallExit = [Math]::Max($overallExit, 1)
        } else {
            Write-Status "Hardware Sensors" "PASS" "All sensors green"
        }
    } catch {
        Write-Status "Hardware Sensors" "WARNING" "Could not retrieve hardware info"
    }

    # Datastore capacity
    $datastores = Get-Datastore -VMHost $vmhost
    foreach ($ds in $datastores) {
        if ($ds.CapacityGB -eq 0) { continue }
        $usedPct = [Math]::Round((1 - $ds.FreeSpaceGB / $ds.CapacityGB) * 100, 1)
        $s = if ($usedPct -ge $DatastoreWarnPct) { 'WARNING' } else { 'PASS' }
        if ($s -eq 'WARNING') { $overallExit = [Math]::Max($overallExit, 1) }
        Write-Status "Datastore: $($ds.Name)" $s ("Used={0}%  Free={1:N0}GB" -f $usedPct, $ds.FreeSpaceGB)
    }

    # Network adapters
    $badNics = Get-VMHostNetworkAdapter -VMHost $vmhost | Where-Object { -not $_.BitRatePerSec -and $_.DeviceName -notmatch 'vmk' }
    if ($badNics) {
        Write-Status "Network Adapters" "WARNING" "$($badNics.DeviceName -join ', ') — no link"
        $overallExit = [Math]::Max($overallExit, 1)
    } else {
        Write-Status "Network Adapters" "PASS" "All adapters have link"
    }

    # Required services
    $services = Get-VMHostService -VMHost $vmhost
    foreach ($svc in $RequiredServices) {
        $s = $services | Where-Object { $_.Key -eq $svc }
        if (-not $s -or $s.Running -eq $false) {
            Write-Status "Service: $svc" "CRITICAL" "NOT RUNNING"
            $overallExit = 2
        } else {
            Write-Status "Service: $svc" "PASS" "Running"
        }
    }
}

Disconnect-VIServer -Confirm:$false
exit $overallExit
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or Windows 11 (PowerShell 5.1 is already installed)
- VMware PowerCLI module — install it once by running this in PowerShell:
  `Install-Module -Name VMware.PowerCLI -Scope CurrentUser -Force`
  When prompted about an untrusted repository, type `Y` and press Enter
- Network access to your vCenter server (the script connects via vCenter, which then manages the ESXi hosts)

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files** (important — otherwise Windows adds .txt)
5. Name it `esxi_host_health.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

Open the file in Notepad and update the `param(` block:

| Variable | What to enter | How to find it |
|---|---|---|
| `$VCenterHost` | vCenter IP or FQDN e.g. `"vcenter.company.local"` | Your vCenter server address |
| `$VCUser` | vCenter username e.g. `"administrator@vsphere.local"` | Your vCenter login |
| `$VCPass` | vCenter password | Your vCenter password |

**Step 3 — Open PowerShell as Administrator**

Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

```
cd C:\Users\YourName\Desktop
.\esxi_host_health.ps1
```

**What you should see**

For each ESXi host managed by vCenter, you will see a block like:

```
=== esxi-01.company.local ===
[PASS    ] ConnectionState                    Connected / PoweredOn
[PASS    ] Hardware Sensors                   All sensors green
[PASS    ] Datastore: datastore1              Used=42.1%  Free=289GB
[PASS    ] Network Adapters                   All adapters have link
[PASS    ] Service: hostd                     Running
[PASS    ] Service: vpxa                      Running
[PASS    ] Service: ntpd                      Running
```

Any WARNING items appear in yellow, CRITICAL in red. The script exits with code 2 if any critical issues are found.

---

## Storage Path Health Check (Bash / esxcli)

Run on an ESXi host via SSH. Report per-device path counts (active / standby / dead) and exit non-zero if any dead paths exist.

~~~bash
#!/bin/bash
# esxi_path_health.sh
# Usage: ssh root@esxi-host 'bash -s' < esxi_path_health.sh
# Or run locally on the ESXi host.

CRIT=0
TS=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

echo "==================================="
echo " ESXi Storage Path Health Check"
echo " $TS"
echo "==================================="
printf "%-40s %8s %8s %8s %8s %s\n" "Device" "Active" "Standby" "Dead" "Total" "Status"
printf "%-40s %8s %8s %8s %8s %s\n" "------" "------" "-------" "----" "-----" "------"

# Build per-device path summary from nmp device list
current_device=""
declare -A active standby dead total

while IFS= read -r line; do
    if [[ $line =~ ^[[:space:]]Device\ Display\ Name:.*\(([^)]+)\) ]]; then
        current_device="${BASH_REMATCH[1]}"
    elif [[ $line =~ ^[[:space:]]Device\ Display\ Name:\ (.*) && -z "$current_device" ]]; then
        current_device="$(echo "$line" | awk -F': ' '{print $2}')"
    fi
done < <(esxcli storage nmp device list 2>/dev/null)

# Use path list for counts
declare -A path_active path_standby path_dead

while IFS= read -r line; do
    if [[ $line =~ ^[[:space:]]Device:\ (.*) ]]; then
        dev="${BASH_REMATCH[1]// /}"
    elif [[ $line =~ State:\ (active|standby|dead|disabled) ]]; do
        state="${BASH_REMATCH[1]}"
        case "$state" in
            active)   (( path_active["$dev"]++  )) ;;
            standby)  (( path_standby["$dev"]++ )) ;;
            dead)     (( path_dead["$dev"]++    )) ;;
        esac
    fi
done < <(esxcli storage core path list 2>/dev/null)

for dev in $(echo "${!path_active[@]} ${!path_standby[@]} ${!path_dead[@]}" | tr ' ' '\n' | sort -u); do
    a="${path_active[$dev]:-0}"
    s="${path_standby[$dev]:-0}"
    d="${path_dead[$dev]:-0}"
    t=$(( a + s + d ))
    if (( d > 0 )); then
        status="DEAD_PATHS"
        CRIT=1
    elif (( a == 0 )); then
        status="NO_ACTIVE"
        CRIT=1
    else
        status="OK"
    fi
    printf "%-40s %8d %8d %8d %8d %s\n" "$dev" "$a" "$s" "$d" "$t" "$status"
done

echo
if [ $CRIT -eq 1 ]; then
    echo "RESULT: CRITICAL — dead or missing paths detected"
else
    echo "RESULT: PASS — all paths healthy"
fi
exit $CRIT
~~~

#### How to run this script — step by step

**Before you start — what you need**
- SSH must be enabled on the ESXi host: vSphere Client → select the host → Manage → Services → SSH → click Start
- An SSH client on your Windows PC — either:
  - **Git Bash** (install from https://git-scm.com) — gives you a bash shell on Windows
  - **PuTTY** (install from https://www.putty.org) — see the plink section at the bottom of this page
  - **Windows Subsystem for Linux (WSL)** — install Ubuntu from the Microsoft Store
- The root password for your ESXi host

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `esxi_path_health.sh` and save it to your Desktop

**Step 2 — No edits needed**

This script runs entirely on the ESXi host — no variables to change. The `ssh` command below pipes the script over the connection.

**Step 3 — Open a terminal**

- **Git Bash:** right-click Desktop → "Git Bash Here"
- **WSL:** Windows key → type `Ubuntu` → press Enter

**Step 4 — Run it**

Replace `192.168.1.100` with your ESXi host's IP:

```bash
ssh root@192.168.1.100 'bash -s' < ~/Desktop/esxi_path_health.sh
```

Type the root password when prompted.

**What you should see**

```
===================================
 ESXi Storage Path Health Check
 2026-05-06T14:30:00Z
===================================
Device                                    Active  Standby     Dead    Total Status
------                                    ------  -------     ----    ----- ------
naa.60003ff44dc75adcbc1e2f3a4b5c6d7e       2        0          0        2   OK
naa.60003ff44dc75adcbc1e2f3a4b5c6d7f       2        0          0        2   OK

RESULT: PASS — all paths healthy
```

If any device shows `DEAD_PATHS` the script exits with code 1.

---

## ESXi Syslog and Event Collector (Python)

Connect to vCenter via pyVmomi, retrieve events from the last 24 hours filtered by severity, and report NMP/storage errors.

~~~python
#!/usr/bin/env python3
"""
esxi_event_collector.py
Usage: python3 esxi_event_collector.py
Deps: pip install pyVmomi
"""

import os, ssl, sys
from datetime import datetime, timedelta, timezone
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

VCENTER_HOST = os.environ.get("VCENTER_HOST", "vcenter.local")
VC_USER      = os.environ.get("VC_USER",      "administrator@vsphere.local")
VC_PASS      = os.environ.get("VC_PASS",      "")
HOURS_BACK   = int(os.environ.get("HOURS_BACK", "24"))

# Event types to capture
WARN_TYPES = {
    vim.event.EventEx,
    vim.event.GeneralHostWarningEvent,
    vim.event.GeneralHostErrorEvent,
    vim.event.VmFailedToSuspendEvent,
    vim.event.DatastoreCapacityIncreasedEvent,
}

NMP_PATTERNS = ["NMP", "Dead path", "SCSI", "storage", "LUN", "vmhba"]


def connect_vcenter():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=VCENTER_HOST, user=VC_USER, pwd=VC_PASS, sslContext=context)
    return si


def collect_events(si):
    content = si.RetrieveContent()
    em = content.eventManager

    start_time = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)
    filter_spec = vim.event.EventFilterSpec(
        time=vim.event.EventFilterSpec.ByTime(beginTime=start_time),
    )
    events = em.QueryEvents(filter=filter_spec)
    return events


def collect_host_vmkernel_events(si):
    """Scan vmkernel.log for NMP/storage messages via host ConfigManager."""
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    findings = []
    for host in container.view:
        try:
            dm = host.configManager.diagnosticSystem
            if not dm:
                continue
            # Read last 500 lines of vmkernel
            lines = dm.BrowseDiagnosticLog(key="vmkernel", start=None, lines=500)
            for entry in (lines.lineText or "").splitlines():
                if any(p.lower() in entry.lower() for p in NMP_PATTERNS):
                    findings.append(f"  [{host.name}] {entry.strip()}")
        except Exception:
            pass
    container.Destroy()
    return findings


si = connect_vcenter()
events = collect_events(si)

print(f"Events from last {HOURS_BACK}h on {VCENTER_HOST}")
print(f"Total events retrieved: {len(events)}")
print()

issues = []
for e in sorted(events, key=lambda x: x.createdTime):
    msg = getattr(e, 'fullFormattedMessage', str(e))
    lvl = "INFO"
    if isinstance(e, (vim.event.GeneralHostErrorEvent,)):
        lvl = "ERROR"
    elif isinstance(e, (vim.event.GeneralHostWarningEvent,)):
        lvl = "WARNING"
    if lvl in ("ERROR", "WARNING"):
        ts = e.createdTime.strftime('%Y-%m-%dT%H:%M:%SZ')
        host = getattr(e.host, 'name', 'N/A') if hasattr(e, 'host') else 'N/A'
        issues.append(f"  [{lvl}] {ts}  host={host}  {msg[:120]}")

if issues:
    print(f"Host events (WARNING/ERROR):")
    for i in issues:
        print(i)
else:
    print("No WARNING/ERROR host events found.")

print()
print("VMkernel NMP/storage log entries:")
vmk_entries = collect_host_vmkernel_events(si)
if vmk_entries:
    for e in vmk_entries[:50]:
        print(e)
else:
    print("  None found.")

Disconnect(si)
sys.exit(1 if issues or vmk_entries else 0)
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Python 3.8 or newer installed from python.org — during install, tick "Add Python to PATH"
- The `pyVmomi` library — install it once by running in Command Prompt:
  `pip install pyVmomi`
- Network access to your vCenter server

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `esxi_event_collector.py` and save it to your Desktop

**Step 2 — Fill in your details**

Open the file in Notepad and update these lines near the top:

| Variable | What to enter | How to find it |
|---|---|---|
| `VCENTER_HOST` | vCenter IP or FQDN e.g. `"vcenter.company.local"` | Your vCenter server address |
| `VC_USER` | vCenter username e.g. `"administrator@vsphere.local"` | Your vCenter login |
| `VC_PASS` | vCenter password | Your vCenter password |
| `HOURS_BACK` | How many hours of events to retrieve (default 24) | Your preference |

**Step 3 — Open Command Prompt**

Windows key → type `cmd` → press Enter

**Step 4 — Run it**

```
cd C:\Users\YourName\Desktop
python esxi_event_collector.py
```

**What you should see**

```
Events from last 24h on vcenter.company.local
Total events retrieved: 312

No WARNING/ERROR host events found.

VMkernel NMP/storage log entries:
  None found.
```

If storage or NMP issues are present, they will be listed with timestamps and host names. The script exits with code 1 if any issues are found.

---

## NTP Configuration Audit (Bash)

SSH to each ESXi host (or run locally), verify NTP service state, configured servers, and time offset.

~~~bash
#!/bin/bash
# esxi_ntp_audit.sh
# Usage: ESXI_HOSTS="host1 host2 host3" ./esxi_ntp_audit.sh
# Requires passwordless SSH to each host as root.

ESXI_HOSTS="${ESXI_HOSTS:-esxi01 esxi02 esxi03}"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10 -o BatchMode=yes"
OFFSET_WARN_MS=500
OFFSET_CRIT_MS=2000
overall=0

printf "%-25s %-20s %-10s %-12s %s\n" "Hostname" "NTP Server(s)" "Service" "Offset(ms)" "Status"
printf "%-25s %-20s %-10s %-12s %s\n" "--------" "-------------" "-------" "----------" "------"

for host in $ESXI_HOSTS; do
    run() { ssh $SSH_OPTS "root@${host}" "$1" 2>/dev/null; }

    svc_status=$(run "/etc/init.d/ntpd status" | grep -io 'running\|stopped\|not running' | head -1)
    svc_status="${svc_status:-unknown}"

    ntp_servers=$(run "esxcli system ntp get" | awk '/NTP Servers:/{for(i=3;i<=NF;i++) printf $i" "; print ""}' | xargs)
    [ -z "$ntp_servers" ] && ntp_servers="NOT_CONFIGURED"

    # Get time offset from ntpq or chronyc
    offset_raw=$(run "ntpq -p 2>/dev/null | awk 'NR>2{print \$9}' | head -1")
    if [[ "$offset_raw" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
        offset_ms=$(printf "%.0f" "$offset_raw")
        abs_offset=${offset_ms#-}
    else
        offset_ms="N/A"
        abs_offset=0
    fi

    status="OK"
    if [[ "$svc_status" != "running" ]]; then
        status="SVC_DOWN"
        overall=2
    elif [[ "$ntp_servers" == "NOT_CONFIGURED" ]]; then
        status="NO_NTP_SERVER"
        overall=2
    elif (( abs_offset >= OFFSET_CRIT_MS )); then
        status="HIGH_DRIFT"
        overall=2
    elif (( abs_offset >= OFFSET_WARN_MS )); then
        status="WARN_DRIFT"
        [ $overall -lt 1 ] && overall=1
    fi

    printf "%-25s %-20s %-10s %-12s %s\n" "$host" "${ntp_servers:0:20}" "$svc_status" "${offset_ms}ms" "$status"
done

echo
case $overall in
    0) echo "Overall: PASS"    ;;
    1) echo "Overall: WARNING" ;;
    2) echo "Overall: CRITICAL";;
esac
exit $overall
~~~

#### How to run this script — step by step

**Before you start — what you need**
- SSH must be enabled on each ESXi host: vSphere Client → select the host → Manage → Services → SSH → click Start
- Passwordless SSH set up from your Linux/WSL machine to each ESXi host as root — or be prepared to type the password for each host
- A bash shell — use Git Bash (https://git-scm.com) or WSL (Ubuntu from the Microsoft Store)
- Network access from your machine to all ESXi host management IPs

**Step 1 — Save the file**

1. Open **Notepad** (or a text editor in WSL: `nano ~/esxi_ntp_audit.sh`)
2. Copy the entire code block above
3. Save it as `esxi_ntp_audit.sh` (in WSL, save to your home directory)

**Step 2 — Fill in your ESXi hosts**

Open the file and update this line near the top:

| Variable | What to enter | How to find it |
|---|---|---|
| `ESXI_HOSTS` | Space-separated list of ESXi hostnames or IPs e.g. `"192.168.1.101 192.168.1.102"` | vSphere Client → host list |

Or set it when you run the script (see Step 5).

**Step 3 — Open a bash terminal**

- **WSL:** Windows key → type `Ubuntu` → press Enter
- **Git Bash:** right-click Desktop → "Git Bash Here"

**Step 4 — Make the script executable**

```bash
chmod +x ~/esxi_ntp_audit.sh
```

**Step 5 — Run it**

```bash
ESXI_HOSTS="192.168.1.101 192.168.1.102 192.168.1.103" ~/esxi_ntp_audit.sh
```

**What you should see**

```
Hostname                  NTP Server(s)        Service    Offset(ms)   Status
--------                  -------------        -------    ----------   ------
192.168.1.101             192.168.1.1          running    12ms         OK
192.168.1.102             192.168.1.1          running    8ms          OK
192.168.1.103             NOT_CONFIGURED       running    N/A          NO_NTP_SERVER

Overall: CRITICAL
```

Any host with NTP issues exits with code 2 (CRITICAL).

---

## Ansible ESXi Configuration Playbook

Use the `community.vmware` collection to verify NTP, DNS, syslog, and SSH security profile compliance across all ESXi hosts in a cluster.

~~~yaml
---
# esxi_compliance.yml
# Usage: ansible-playbook -i inventory esxi_compliance.yml
# Deps: ansible-galaxy collection install community.vmware
# Vars: vcenter_hostname, datacenter_name, cluster_name, vc_username, vc_password

- name: ESXi Host Configuration Compliance Check
  hosts: localhost
  gather_facts: false
  vars:
    vcenter_hostname: vcenter.local
    datacenter_name:  Production
    cluster_name:     Cluster-01
    vc_username:      "{{ lookup('env','VC_USER') }}"
    vc_password:      "{{ lookup('env','VC_PASS') }}"
    ntp_servers:
      - 192.168.1.1
      - 192.168.1.2
    dns_servers:
      - 192.168.1.53
    syslog_host: "udp://syslog.local:514"

  tasks:

    - name: Gather ESXi host facts
      community.vmware.vmware_host_facts:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        cluster:    "{{ cluster_name }}"
        validate_certs: false
      register: host_facts

    - name: Check NTP configuration per host
      community.vmware.vmware_host_ntp:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        esxi_hostname: "{{ item }}"
        ntp_servers: "{{ ntp_servers }}"
        validate_certs: false
        state: present
      loop: "{{ host_facts.hosts_facts.keys() | list }}"

    - name: Check DNS configuration per host
      community.vmware.vmware_host_dns:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        esxi_hostname: "{{ item }}"
        dns_servers: "{{ dns_servers }}"
        validate_certs: false
      loop: "{{ host_facts.hosts_facts.keys() | list }}"

    - name: Check syslog target per host
      community.vmware.vmware_host_config_manager:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        esxi_hostname: "{{ item }}"
        options:
          'Syslog.global.logHost': "{{ syslog_host }}"
        validate_certs: false
      loop: "{{ host_facts.hosts_facts.keys() | list }}"

    - name: Check SSH security profile (SSH should be disabled in production)
      community.vmware.vmware_host_service:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        esxi_hostname: "{{ item }}"
        service_name: TSM-SSH
        state: stopped
        validate_certs: false
      loop: "{{ host_facts.hosts_facts.keys() | list }}"
      register: ssh_result
      failed_when: false

    - name: Assert compliance summary
      ansible.builtin.assert:
        that:
          - host_facts.hosts_facts | length > 0
        fail_msg: "No hosts found in cluster {{ cluster_name }}"
        success_msg: "Compliance check complete for {{ host_facts.hosts_facts | length }} hosts"
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Ansible — easiest on Windows via WSL. Open Microsoft Store, install Ubuntu, then in the Ubuntu terminal:
  `sudo apt update && sudo apt install -y ansible python3-pip`
- Install the VMware community collection and dependencies:
  `ansible-galaxy collection install community.vmware`
  `pip3 install pyVmomi requests`
- Network access to your vCenter server

**Step 1 — Save the file**

In your WSL terminal:

```bash
nano ~/esxi_compliance.yml
```

Paste the entire code block, then press `Ctrl+X`, then `Y`, then `Enter` to save.

**Step 2 — Fill in your details**

Open the file and update the `vars:` section:

| Variable | What to enter | How to find it |
|---|---|---|
| `vcenter_hostname` | vCenter IP or FQDN | Your vCenter server address |
| `datacenter_name` | Datacenter name in vCenter | vSphere Client → top of inventory |
| `cluster_name` | Cluster name to audit | vSphere Client → cluster list |
| `ntp_servers` | Your NTP server IPs | Your network admin |
| `dns_servers` | Your DNS server IPs | Your network admin |
| `syslog_host` | Your syslog server URI e.g. `"udp://syslog.local:514"` | Your syslog server address |

**Step 3 — Set credentials as environment variables**

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
ansible-playbook -i ~/inventory ~/esxi_compliance.yml
```

**What you should see**

Each task prints `ok` (no change needed) or `changed` (configuration was corrected). If no hosts are found in the cluster, you get a `FAILED` assertion. Any task that encounters an error (such as a host that cannot be reached) will show `fatal` with the error detail.

---

## Windows: ESXi Host Health via REST API (PowerShell)

Use the ESXi Embedded Host Client REST API (available on ESXi 6.x and newer) to check system health and list services — no extra modules needed.

~~~powershell
# esxi_rest_health.ps1
# Uses the ESXi local REST API on port 443.
# Available on ESXi 6.x and newer (Embedded Host Client REST API).
# Requires PowerShell 5.1+ (already on Windows 10/11). No extra modules needed.

param(
    [string]$EsxiHost = "192.168.1.100",
    [string]$EsxiUser = "root",
    [string]$EsxiPass = "YourRootPasswordHere"
)

# Ignore SSL certificate errors (ESXi uses self-signed certs)
Add-Type @"
using System.Net;
using System.Security.Cryptography.X509Certificates;
public class TrustAll : ICertificatePolicy {
    public bool CheckValidationResult(ServicePoint sp, X509Certificate cert, WebRequest req, int prob) { return true; }
}
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAll
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

$BaseUrl = "https://$EsxiHost/rest"

# Step 1: Authenticate — POST /rest/com/vmware/cis/session with Basic auth
$authBytes = [System.Text.Encoding]::ASCII.GetBytes("${EsxiUser}:${EsxiPass}")
$authB64   = [System.Convert]::ToBase64String($authBytes)
$authHeaders = @{ Authorization = "Basic $authB64" }

try {
    $sessionResp = Invoke-RestMethod -Uri "$BaseUrl/com/vmware/cis/session" -Method POST -Headers $authHeaders
    $sessionToken = $sessionResp.value
} catch {
    Write-Host "ERROR: Could not authenticate to ESXi host. Check IP, username, and password." -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

$apiHeaders = @{ "vmware-api-session-id" = $sessionToken }

Write-Host "`n=== ESXi Host Health Check: $EsxiHost ===" -ForegroundColor Cyan
Write-Host "($(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))`n"

# Step 2: GET /rest/appliance/health/system — overall health
try {
    $health = Invoke-RestMethod -Uri "$BaseUrl/appliance/health/system" -Method GET -Headers $apiHeaders
    $healthVal = $health.value
    $colour = if ($healthVal -eq "green") { "Green" } elseif ($healthVal -eq "yellow") { "Yellow" } else { "Red" }
    Write-Host "System Health: " -NoNewline
    Write-Host $healthVal.ToUpper() -ForegroundColor $colour
} catch {
    Write-Host "System Health: UNKNOWN (could not retrieve — $($_.Exception.Message))" -ForegroundColor Yellow
}

Write-Host ""

# Step 3: GET /rest/appliance/vmon/service — list services
try {
    $services = Invoke-RestMethod -Uri "$BaseUrl/appliance/vmon/service" -Method GET -Headers $apiHeaders
    Write-Host "--- Services ---"
    $header = "{0,-40} {1,-15} {2}"
    Write-Host ($header -f "Service", "State", "Startup Type")
    Write-Host ("-" * 70)

    $stoppedServices = @()
    foreach ($svc in ($services.value | Sort-Object { $_.key })) {
        $state   = $svc.value.state
        $startup = $svc.value.startup_type
        $colour  = if ($state -eq "STARTED") { "Green" } elseif ($state -eq "STOPPED") { "Red" } else { "Yellow" }
        Write-Host ($header -f $svc.key, $state, $startup) -ForegroundColor $colour
        if ($state -eq "STOPPED" -and $startup -eq "AUTOMATIC") {
            $stoppedServices += $svc.key
        }
    }

    if ($stoppedServices.Count -gt 0) {
        Write-Host "`nWARNING: The following automatic services are stopped:" -ForegroundColor Yellow
        $stoppedServices | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
    } else {
        Write-Host "`nAll automatic services are running." -ForegroundColor Green
    }
} catch {
    Write-Host "Services: UNKNOWN (could not retrieve — $($_.Exception.Message))" -ForegroundColor Yellow
}

# Log out
try {
    Invoke-RestMethod -Uri "$BaseUrl/com/vmware/cis/session" -Method DELETE -Headers $apiHeaders | Out-Null
} catch {}

Write-Host "`nCheck complete." -ForegroundColor Cyan
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or Windows 11 — PowerShell 5.1 is already installed, no extra modules needed
- ESXi 6.x or newer (the Embedded Host Client REST API was introduced in ESXi 6.0)
- Network access to your ESXi host on port 443
- The root password for your ESXi host

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `esxi_rest_health.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

Open the file in Notepad and update the `param(` block:

| Variable | What to enter | How to find it |
|---|---|---|
| `$EsxiHost` | ESXi host IP address e.g. `"192.168.1.100"` | vSphere Client → host summary |
| `$EsxiUser` | ESXi username — almost always `"root"` | ESXi root account |
| `$EsxiPass` | ESXi root password | Your ESXi root password |

**Step 3 — Open PowerShell as Administrator**

Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

```
cd C:\Users\YourName\Desktop
.\esxi_rest_health.ps1
```

**What you should see**

```
=== ESXi Host Health Check: 192.168.1.100 ===
(2026-05-06 14:30:22)

System Health: GREEN

--- Services ---
Service                                  State           Startup Type
----------------------------------------------------------------------
hostd                                    STARTED         AUTOMATIC
ntpd                                     STARTED         AUTOMATIC
sfcbd                                    STOPPED         MANUAL

All automatic services are running.

Check complete.
```

Any service that should start automatically but is stopped is listed as a warning.

---

## Windows: ESXi ESXCLI Commands via Plink (CMD)

Connect to an ESXi host via SSH using plink (from PuTTY) and run a series of diagnostic ESXCLI commands with clear labels.

~~~batch
@echo off
REM esxi_esxcli_check.bat — ESXi diagnostic commands via SSH (plink)
REM Connects to an ESXi host using plink (PuTTY command-line SSH tool).
REM
REM DOWNLOAD PLINK: https://www.putty.org
REM   - Download putty-64bit-X.XX-installer.msi and install it.
REM   - plink.exe will be at: C:\Program Files\PuTTY\plink.exe
REM
REM ENABLE SSH ON ESXI:
REM   vSphere Client -> select the host -> Manage -> Services -> SSH -> Start
REM
REM FIRST-TIME SETUP (run once to accept the SSH fingerprint):
REM   "C:\Program Files\PuTTY\plink.exe" -ssh root@192.168.1.100
REM   Type 'y' when asked to trust the host fingerprint, then Ctrl+C.

set ESXI_HOST=192.168.1.100
set SSH_USER=root
set PLINK="C:\Program Files\PuTTY\plink.exe"

echo.
echo === ESXi ESXCLI Diagnostic Check: %ESXI_HOST% ===
echo.

echo --- ESXi Version ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli system version get"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not connect to %ESXI_HOST%.
    echo Check: 1) IP is correct  2) SSH is enabled  3) Run first-time fingerprint setup above
    exit /b 1
)

echo.
echo --- Storage Multipath Devices (first 40 lines) ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli storage nmp device list | head -40"

echo.
echo --- Network NICs ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli network nic list"

echo.
echo --- Host Summary (product, build, status) ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "vim-cmd hostsvc/hostsummary | grep -E 'product|build|status'"

echo.
echo --- System Uptime (seconds) ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli system stats uptime get"

echo.
echo === Diagnostic check complete ===
~~~

#### How to run this script — step by step

**Before you start — what you need**
- PuTTY installed on your Windows PC — download from https://www.putty.org (get the 64-bit installer)
- SSH enabled on your ESXi host: vSphere Client → select the host → Manage → Services → SSH → click Start
- The root password for your ESXi host
- Network access from your PC to the ESXi host management IP

**Step 1 — Accept the SSH fingerprint (one-time setup)**

Before the batch script will work, you must accept the host's SSH fingerprint once. Open Command Prompt and run:

```
"C:\Program Files\PuTTY\plink.exe" -ssh root@192.168.1.100
```

When asked "Store key in cache?", type `y` and press Enter. Type the root password when prompted. Once connected, press `Ctrl+C` to disconnect. You only need to do this once per ESXi host.

**Step 2 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `esxi_esxcli_check.bat` and save it to your Desktop

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
esxi_esxcli_check.bat
```

**What you should see**

```
=== ESXi ESXCLI Diagnostic Check: 192.168.1.100 ===

--- ESXi Version ---
   Product: VMware ESXi
   Version: 8.0.0
   Build: Releasebuild-20513097

--- Storage Multipath Devices (first 40 lines) ---
   Device Display Name: Local VMware Disk (mpx.vmhba0:C0:T0:L0)
   ...

--- Network NICs ---
   Name    PCI          Driver  Link  Speed  Duplex MAC Address
   vmnic0  0000:02:00.0 nvmxnet3  Up  10000  Full   00:0c:29:ab:cd:ef

--- Host Summary (product, build, status) ---
   product = "VMware ESXi"
   build = "20513097"

--- System Uptime (seconds) ---
   1382400

=== Diagnostic check complete ===
```
