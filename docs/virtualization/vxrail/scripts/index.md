# Scripts

> Part of the [VxRail](../) reference.

---
## VxRail Cluster Health Check (PowerShell / PowerCLI)

Connect to vCenter managing VxRail and query the VxRail Manager REST API to report cluster health, node states, and active faults.

~~~powershell
#!/usr/bin/env pwsh
# vxrail-cluster-health.ps1
# Usage: ./vxrail-cluster-health.ps1 -VxRailMgrHost <host> -VxRailUser <user> -VxRailPass <pass>

param(
    [Parameter(Mandatory)][string]$VxRailMgrHost = $env:VXRAIL_MGR_HOST,
    [Parameter(Mandatory)][string]$VxRailUser    = $env:VXRAIL_USER,
    [Parameter(Mandatory)][string]$VxRailPass    = $env:VXRAIL_PASS
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Suppress SSL certificate errors for self-signed certs
if (-not ([System.Management.Automation.PSTypeName]'TrustAllCertsPolicy').Type) {
    Add-Type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) { return true; }
    }
"@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
}
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

$BaseUrl = "https://$VxRailMgrHost/rest/vxm"
$Auth    = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${VxRailUser}:${VxRailPass}"))
$Headers = @{ Authorization = "Basic $Auth"; "Content-Type" = "application/json" }

function Invoke-VxRailApi {
    param([string]$Path)
    $response = Invoke-RestMethod -Uri "$BaseUrl$Path" -Headers $Headers -Method GET
    return $response
}

Write-Host "`n=== VxRail Cluster Health Check ===" -ForegroundColor Cyan
Write-Host "Host: $VxRailMgrHost  Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"

# --- Cluster overview ---
$cluster = Invoke-VxRailApi "/v1/cluster"
Write-Host "Cluster Version : $($cluster.version)"
Write-Host "Cluster Health  : $($cluster.health)"

# --- Host list ---
$hosts = Invoke-VxRailApi "/v1/hosts"
Write-Host "Node Count      : $($hosts.Count)`n"

$faultCount = 0

Write-Host ("{0,-20} {1,-12} {2,-8} {3,-8} {4,-8} {5,-8}" -f "Serial", "Health", "CPU", "Memory", "Disk", "NIC")
Write-Host ("-" * 70)

foreach ($node in $hosts) {
    $cpu    = $node.component_health | Where-Object { $_.component -eq "CPU" }    | Select-Object -ExpandProperty health
    $mem    = $node.component_health | Where-Object { $_.component -eq "MEMORY" } | Select-Object -ExpandProperty health
    $disk   = $node.component_health | Where-Object { $_.component -eq "DISK" }   | Select-Object -ExpandProperty health
    $nic    = $node.component_health | Where-Object { $_.component -eq "NIC" }    | Select-Object -ExpandProperty health

    $rowColor = if ($node.health -ne "Healthy") { "Red" } else { "Green" }
    Write-Host ("{0,-20} {1,-12} {2,-8} {3,-8} {4,-8} {5,-8}" -f `
        $node.serial_number, $node.health, $cpu, $mem, $disk, $nic) -ForegroundColor $rowColor

    if ($node.health -ne "Healthy") { $faultCount++ }
}

# --- System health / active faults ---
Write-Host ""
$sysHealth = Invoke-VxRailApi "/v1/system/health"

if ($sysHealth.faults -and $sysHealth.faults.Count -gt 0) {
    Write-Host "Active Faults ($($sysHealth.faults.Count)):" -ForegroundColor Red
    foreach ($fault in $sysHealth.faults) {
        Write-Host "  [$(($fault.severity).ToUpper())] $($fault.description)" -ForegroundColor Yellow
        $faultCount++
    }
} else {
    Write-Host "Active Faults   : None" -ForegroundColor Green
}

Write-Host ""
if ($faultCount -gt 0) {
    Write-Host "RESULT: UNHEALTHY — $faultCount issue(s) found." -ForegroundColor Red
    exit 1
} else {
    Write-Host "RESULT: HEALTHY" -ForegroundColor Green
    exit 0
}
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or 11 with PowerShell 5.1 or PowerShell 7 (already installed)
- Network access to the VxRail Manager IP from your Windows PC
- VxRail Manager credentials (vCenter SSO admin or local admin account)

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files** (so Windows doesn't add .txt)
5. Save it as `vxrail-cluster-health.ps1` on your Desktop

**Step 2 — Fill in your details**

Open the saved file and change these values in the `param(...)` block, or pass them on the command line:

| Variable | What to put here | How to find it |
|---|---|---|
| `$VxRailMgrHost` | IP address or hostname of VxRail Manager | VxRail Manager appliance IP — ask your admin |
| `$VxRailUser` | Username for VxRail Manager | Usually `administrator@vsphere.local` or `admin` |
| `$VxRailPass` | Password for the above account | Your VxRail / vCenter admin password |

**Step 3 — Open a terminal**

Windows key → search `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
cd C:\Users\YourName\Desktop
.\vxrail-cluster-health.ps1 -VxRailMgrHost 192.168.1.50 -VxRailUser admin -VxRailPass MyPassword
```

**What you should see**

A table listing each VxRail node (by serial number) with colour-coded health status for CPU, Memory, Disk, and NIC. Any active faults are listed below the table. The final line says either `RESULT: HEALTHY` (green) or `RESULT: UNHEALTHY` (red) with a count of issues found.

---

## LCM Upgrade Readiness Check (Bash)

Query the VxRail Manager REST API to determine the current version, available updates, and whether all nodes are healthy before an LCM upgrade.

~~~bash
#!/usr/bin/env bash
# vxrail-lcm-readiness.sh
# Usage: VXRAIL_MGR_HOST=<host> VXRAIL_USER=<user> VXRAIL_PASS=<pass> ./vxrail-lcm-readiness.sh

set -euo pipefail

VXRAIL_MGR_HOST="${VXRAIL_MGR_HOST:?VXRAIL_MGR_HOST is required}"
VXRAIL_USER="${VXRAIL_USER:?VXRAIL_USER is required}"
VXRAIL_PASS="${VXRAIL_PASS:?VXRAIL_PASS is required}"

BASE_URL="https://${VXRAIL_MGR_HOST}/rest/vxm"
CURL_OPTS=(-sk -u "${VXRAIL_USER}:${VXRAIL_PASS}" -H "Content-Type: application/json")

rc=0

vxm_get() {
    curl "${CURL_OPTS[@]}" "${BASE_URL}${1}"
}

echo ""
echo "=== VxRail LCM Upgrade Readiness Check ==="
echo "Host : ${VXRAIL_MGR_HOST}"
echo "Time : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# --- Current version ---
CURRENT_VERSION=$(vxm_get "/v1/system/version" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('version','unknown'))")
echo "Current Version  : ${CURRENT_VERSION}"

# --- Available updates ---
ADVISORY=$(vxm_get "/v2/lcm/upgrade/advisory")
AVAILABLE_VERSION=$(echo "${ADVISORY}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
releases = d.get('advisory', {}).get('upgrade_advisories', [])
if releases:
    print(releases[0].get('target_version', 'none'))
else:
    print('none')
")
echo "Available Version: ${AVAILABLE_VERSION}"

if [[ "${AVAILABLE_VERSION}" == "none" ]]; then
    echo "No upgrade available. Cluster is at latest."
fi

# --- Node health ---
echo ""
echo "Node Health:"
echo "-------------------------------------------------------------"
printf "%-20s %-12s %-10s\n" "Serial" "Health" "PSNT"

HOSTS_JSON=$(vxm_get "/v1/hosts")
ALL_HEALTHY=true

python3 - <<EOF
import json, sys
hosts = json.loads('''${HOSTS_JSON}''')
all_ok = True
for h in hosts:
    health = h.get('health', 'unknown')
    serial = h.get('serial_number', 'unknown')
    psnt   = h.get('psnt', 'unknown')
    status = "OK" if health == "Healthy" else "FAULT"
    if health != "Healthy":
        all_ok = False
    print(f"{serial:<20} {health:<12} {psnt:<10}  {status}")
print()
if all_ok:
    print("All nodes: HEALTHY")
    sys.exit(0)
else:
    print("ERROR: One or more nodes are NOT healthy. Upgrade not recommended.")
    sys.exit(1)
EOF
node_rc=$?

# --- vSAN health (via vCenter API placeholder) ---
echo ""
echo "vSAN Health      : (verify manually via vCenter or vSAN Health Check plugin)"

# --- Summary ---
echo ""
if [[ $node_rc -ne 0 ]]; then
    echo "PRE-CHECK RESULT : FAIL — Unhealthy nodes detected. Do not proceed with LCM."
    exit 1
elif [[ "${AVAILABLE_VERSION}" == "none" ]]; then
    echo "PRE-CHECK RESULT : INFO — No upgrade available."
    exit 0
else
    echo "PRE-CHECK RESULT : PASS — Ready to upgrade from ${CURRENT_VERSION} to ${AVAILABLE_VERSION}."
    exit 0
fi
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Linux or macOS machine (or WSL on Windows — see Step 3)
- `curl` installed (already present on most Linux/Mac systems)
- `python3` installed (`sudo apt install python3` or `brew install python3`)
- Network access to the VxRail Manager IP

**Step 1 — Save the file**

1. Open a text editor (gedit, nano, VS Code, etc.)
2. Copy the entire code block above
3. Save it as `vxrail-lcm-readiness.sh` in your home directory or `/opt/scripts/`

**Step 2 — Fill in your details**

Set these environment variables before running (replace the example values):

| Variable | What to put here | How to find it |
|---|---|---|
| `VXRAIL_MGR_HOST` | IP or hostname of VxRail Manager | VxRail Manager appliance IP |
| `VXRAIL_USER` | Username | `administrator@vsphere.local` or `admin` |
| `VXRAIL_PASS` | Password | Your VxRail admin password |

**Step 3 — Open a terminal**

- **Linux/Mac:** Open Terminal normally
- **Windows:** Install Git for Windows (gitforwindows.org) and use Git Bash, or enable WSL (Windows Subsystem for Linux)

**Step 4 — Make the script executable and run it**

```
chmod +x vxrail-lcm-readiness.sh
VXRAIL_MGR_HOST=192.168.1.50 VXRAIL_USER=admin VXRAIL_PASS=MyPassword ./vxrail-lcm-readiness.sh
```

**What you should see**

Current VxRail version, available upgrade version (or "none" if already up to date), and a table showing each node's health. Final line reads `PRE-CHECK RESULT : PASS`, `FAIL`, or `INFO`.

---

## Node Hardware Status (Bash)

Retrieve per-node hardware health from the VxRail Manager REST API and flag any component not in a Healthy state.

~~~bash
#!/usr/bin/env bash
# vxrail-node-hardware.sh
# Usage: VXRAIL_MGR_HOST=<host> VXRAIL_USER=<user> VXRAIL_PASS=<pass> ./vxrail-node-hardware.sh

set -euo pipefail

VXRAIL_MGR_HOST="${VXRAIL_MGR_HOST:?VXRAIL_MGR_HOST is required}"
VXRAIL_USER="${VXRAIL_USER:?VXRAIL_USER is required}"
VXRAIL_PASS="${VXRAIL_PASS:?VXRAIL_PASS is required}"

BASE_URL="https://${VXRAIL_MGR_HOST}/rest/vxm"
CURL_OPTS=(-sk -u "${VXRAIL_USER}:${VXRAIL_PASS}" -H "Content-Type: application/json")

FAULT_COUNT=0

vxm_get() {
    curl "${CURL_OPTS[@]}" "${BASE_URL}${1}"
}

echo ""
echo "=== VxRail Node Hardware Status ==="
echo "Host : ${VXRAIL_MGR_HOST}"
echo "Time : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Get all host serial numbers
HOST_SERIALS=$(vxm_get "/v1/hosts" | python3 -c "
import sys, json
hosts = json.load(sys.stdin)
for h in hosts:
    print(h['serial_number'])
")

for SERIAL in ${HOST_SERIALS}; do
    echo "Node: ${SERIAL}"
    echo "  $(printf '%-8s %-20s %-10s %s' 'Type' 'Component' 'Health' 'Details')"
    echo "  $(printf '%0.s-' {1..65})"

    HW_JSON=$(vxm_get "/v1/hosts/${SERIAL}/hardware")

    python3 - <<EOF
import json, sys

hw = json.loads('''${HW_JSON}''')

sections = {
    'PSU':  hw.get('psu', []),
    'Fan':  hw.get('fan', []),
    'Disk': hw.get('disk', []),
    'NIC':  hw.get('nic', []),
}

fault_count = 0
for section, items in sections.items():
    for item in items:
        name   = item.get('name', item.get('slot', 'unknown'))
        health = item.get('health', 'unknown')
        detail = item.get('description', '')
        flag   = '' if health == 'Healthy' else '  <-- FAULT'
        if health != 'Healthy':
            fault_count += 1
        print(f"  {section:<8} {name:<20} {health:<10} {detail}{flag}")

if fault_count:
    print(f"\n  FAULTS DETECTED: {fault_count} component(s) not Healthy")
    sys.exit(1)
else:
    print(f"\n  All components Healthy")
    sys.exit(0)
EOF
    hw_rc=$?
    if [[ $hw_rc -ne 0 ]]; then
        FAULT_COUNT=$((FAULT_COUNT + 1))
    fi
    echo ""
done

if [[ $FAULT_COUNT -gt 0 ]]; then
    echo "OVERALL: ${FAULT_COUNT} node(s) with hardware faults."
    exit 1
else
    echo "OVERALL: All nodes hardware Healthy."
    exit 0
fi
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Linux, macOS, or WSL terminal
- `curl` and `python3` installed
- Network access to the VxRail Manager IP and valid credentials

**Step 1 — Save the file**

1. Open a text editor
2. Copy the entire code block above
3. Save it as `vxrail-node-hardware.sh`

**Step 2 — Fill in your details**

| Variable | What to put here | How to find it |
|---|---|---|
| `VXRAIL_MGR_HOST` | VxRail Manager IP or hostname | VxRail Manager appliance IP |
| `VXRAIL_USER` | Admin username | `administrator@vsphere.local` or local admin |
| `VXRAIL_PASS` | Admin password | Your VxRail admin password |

**Step 3 — Open a terminal**

- **For .sh:** Open Terminal on Linux/Mac, or use Git Bash / WSL on Windows

**Step 4 — Make the script executable and run it**

```
chmod +x vxrail-node-hardware.sh
VXRAIL_MGR_HOST=192.168.1.50 VXRAIL_USER=admin VXRAIL_PASS=MyPassword ./vxrail-node-hardware.sh
```

**What you should see**

A section for each VxRail node showing PSU, Fan, Disk, and NIC health status. Any component not in a `Healthy` state is marked with `<-- FAULT`. The final line shows `OVERALL: All nodes hardware Healthy` or a count of nodes with faults.

---

## Ansible VxRail Health Playbook

Use the Ansible `uri` module to authenticate against VxRail Manager, collect cluster and host health, retrieve system faults, assert no critical faults, and print a structured summary.

~~~yaml
---
# vxrail-health.yml
# Usage: ansible-playbook vxrail-health.yml -e "vxrail_mgr=192.0.2.10 vxrail_user=admin vxrail_pass=secret"

- name: VxRail Health Check
  hosts: localhost
  gather_facts: false

  vars:
    vxrail_mgr:  "{{ lookup('env', 'VXRAIL_MGR_HOST') }}"
    vxrail_user: "{{ lookup('env', 'VXRAIL_USER') }}"
    vxrail_pass: "{{ lookup('env', 'VXRAIL_PASS') }}"
    base_url:    "https://{{ vxrail_mgr }}/rest/vxm"
    auth_header: "{{ ('Basic ' + (vxrail_user + ':' + vxrail_pass) | b64encode) }}"

  tasks:

    # --- 1. Get cluster health ---
    - name: Get cluster health
      uri:
        url: "{{ base_url }}/v1/cluster"
        method: GET
        headers:
          Authorization: "{{ auth_header }}"
          Content-Type: "application/json"
        validate_certs: false
        return_content: true
      register: cluster_result

    - name: Set cluster facts
      set_fact:
        cluster_version: "{{ cluster_result.json.version }}"
        cluster_health:  "{{ cluster_result.json.health }}"

    # --- 2. Get host health ---
    - name: Get host health
      uri:
        url: "{{ base_url }}/v1/hosts"
        method: GET
        headers:
          Authorization: "{{ auth_header }}"
          Content-Type: "application/json"
        validate_certs: false
        return_content: true
      register: hosts_result

    - name: Set host facts
      set_fact:
        vxrail_hosts: "{{ hosts_result.json }}"

    # --- 3. Get system faults ---
    - name: Get system faults
      uri:
        url: "{{ base_url }}/v1/system/faults"
        method: GET
        headers:
          Authorization: "{{ auth_header }}"
          Content-Type: "application/json"
        validate_certs: false
        return_content: true
      register: faults_result

    - name: Set faults fact
      set_fact:
        system_faults: "{{ faults_result.json }}"

    # --- 4. Assert no critical faults ---
    - name: Assert no critical faults
      assert:
        that:
          - "system_faults | selectattr('severity', 'equalto', 'CRITICAL') | list | length == 0"
        fail_msg: >
          CRITICAL faults detected:
          {{ system_faults | selectattr('severity', 'equalto', 'CRITICAL') | map(attribute='description') | list | join(', ') }}
        success_msg: "No critical faults found."

    # --- 5. Print health summary ---
    - name: Print cluster summary
      debug:
        msg:
          - "Cluster Version : {{ cluster_version }}"
          - "Cluster Health  : {{ cluster_health }}"
          - "Node Count      : {{ vxrail_hosts | length }}"

    - name: Print per-node health
      debug:
        msg: >
          Node {{ item.serial_number }}: health={{ item.health }}
          {% for comp in item.component_health | default([]) %}
          {{ comp.component }}={{ comp.health }}
          {% endfor %}
      loop: "{{ vxrail_hosts }}"
      loop_control:
        label: "{{ item.serial_number }}"

    - name: Print fault list
      debug:
        msg: "[{{ item.severity }}] {{ item.description }}"
      loop: "{{ system_faults }}"
      loop_control:
        label: "{{ item.severity }}"
      when: system_faults | length > 0
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Linux or WSL machine with Python 3 installed
- Ansible installed: `pip install ansible` or `sudo apt install ansible`
- Network access to the VxRail Manager IP
- Valid VxRail Manager credentials

**Step 1 — Save the file**

1. Open a text editor
2. Copy the entire code block above
3. Save it as `vxrail-health.yml`

**Step 2 — Fill in your details**

You can pass variables on the command line with `-e`, or set environment variables `VXRAIL_MGR_HOST`, `VXRAIL_USER`, and `VXRAIL_PASS` before running.

| Variable | What to put here | How to find it |
|---|---|---|
| `vxrail_mgr` | VxRail Manager IP or hostname | VxRail Manager appliance IP |
| `vxrail_user` | Admin username | `administrator@vsphere.local` or local admin |
| `vxrail_pass` | Admin password | Your VxRail admin password |

**Step 3 — Open a terminal**

- **For .yml (Ansible):** Requires Linux/WSL. Open a Linux or WSL terminal.

**Step 4 — Run the playbook**

```
cd /path/to/your/file
ansible-playbook vxrail-health.yml -e "vxrail_mgr=192.168.1.50 vxrail_user=admin vxrail_pass=MyPassword"
```

**What you should see**

Ansible will print task-by-task output. The `debug` tasks will display cluster version, health state, node count, and per-node component health. If any CRITICAL faults exist the playbook will fail at the `assert` task and display the fault descriptions.

---

## Windows: VxRail Cluster Health via REST API (PowerShell)

Query the VxRail Manager REST API from a Windows machine to report cluster version, number of nodes, any unhealthy nodes, and alert count.

~~~powershell
# vxrail-health-windows.ps1
# Usage: .\vxrail-health-windows.ps1 -VxrailMgr <IP> -VxUser <user> -VxPass <pass>
# Requires: PowerShell 5.1 or later (built into Windows 10/11)

param(
    [Parameter(Mandatory)][string]$VxrailMgr,
    [Parameter(Mandatory)][string]$VxUser,
    [Parameter(Mandatory)][string]$VxPass
)

# Suppress SSL errors for self-signed certificates (common on VxRail)
if (-not ([System.Management.Automation.PSTypeName]'TrustAllCertsPolicy').Type) {
    Add-Type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) { return true; }
    }
"@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
}
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

$BaseUrl = "https://$VxrailMgr/rest/vxm/v1"
$Auth    = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${VxUser}:${VxPass}"))
$Headers = @{ Authorization = "Basic $Auth"; "Content-Type" = "application/json" }

function Get-VxRail {
    param([string]$Endpoint)
    return Invoke-RestMethod -Uri "$BaseUrl$Endpoint" -Headers $Headers -Method GET
}

Write-Host ""
Write-Host "=== VxRail Cluster Health (Windows) ===" -ForegroundColor Cyan
Write-Host "Manager : $VxrailMgr"
Write-Host "Date    : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

# --- Cluster overview ---
try {
    $cluster = Get-VxRail "/cluster"
    Write-Host "Cluster Version : $($cluster.version)"
    $healthColor = if ($cluster.health -eq "Healthy") { "Green" } else { "Red" }
    Write-Host "Cluster Health  : $($cluster.health)" -ForegroundColor $healthColor
} catch {
    Write-Host "ERROR retrieving cluster info: $_" -ForegroundColor Red
    exit 1
}

# --- Host list ---
try {
    $hosts = Get-VxRail "/hosts"
    Write-Host "Number of Nodes : $($hosts.Count)"
    Write-Host ""

    $unhealthyNodes = 0
    Write-Host ("{0,-20} {1,-12}" -f "Serial Number", "Health Status")
    Write-Host ("-" * 35)
    foreach ($node in $hosts) {
        $color = if ($node.health -ne "Healthy") { "Red"; $unhealthyNodes++ } else { "Green" }
        Write-Host ("{0,-20} {1,-12}" -f $node.serial_number, $node.health) -ForegroundColor $color
    }

    if ($unhealthyNodes -gt 0) {
        Write-Host ""
        Write-Host "WARNING: $unhealthyNodes node(s) are not Healthy!" -ForegroundColor Red
    }
} catch {
    Write-Host "ERROR retrieving host list: $_" -ForegroundColor Red
}

# --- Active alerts ---
Write-Host ""
try {
    $alerts = Get-VxRail "/system/alerts"
    $alertCount = if ($alerts) { $alerts.Count } else { 0 }
    if ($alertCount -gt 0) {
        Write-Host "Active Alerts : $alertCount" -ForegroundColor Yellow
        foreach ($alert in $alerts) {
            Write-Host "  [$($alert.severity)] $($alert.message_id) — $($alert.description)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Active Alerts : None" -ForegroundColor Green
    }
} catch {
    Write-Host "Active Alerts : (could not retrieve — endpoint may vary by VxRail version)" -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "Done." -ForegroundColor Cyan
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or Windows 11 (PowerShell is already installed)
- Network access to the VxRail Manager IP from your Windows PC
- VxRail Manager username and password (vCenter SSO admin works)

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files** (so Windows doesn't add .txt)
5. Save it as `vxrail-health-windows.ps1` on your Desktop

**Step 2 — Fill in your details**

You pass all values on the command line — no editing needed. But note what each value means:

| Variable | What to put here | How to find it |
|---|---|---|
| `$VxrailMgr` | VxRail Manager IP address or hostname | Ask your VMware admin or check the vCenter VxRail plugin |
| `$VxUser` | Admin username | Typically `administrator@vsphere.local` or `admin` |
| `$VxPass` | Password for the above user | Your VxRail / vCenter admin password |

**Step 3 — Open a terminal**

Windows key → search `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
cd C:\Users\YourName\Desktop
.\vxrail-health-windows.ps1 -VxrailMgr 192.168.1.50 -VxUser admin -VxPass MyPassword
```

**What you should see**

Cluster version and health state, number of nodes, a table showing each node's health (green = healthy, red = fault), and a list of any active alerts. If all is well the final output shows "Active Alerts : None" in green.

---

## Windows: VxRail Node Status via Plink (CMD)

Use plink.exe (PuTTY's command-line SSH tool) to connect to the VxRail Manager appliance and run CLI commands to check system version and cluster health.

~~~batch
@echo off
REM vxrail-node-status.bat — VxRail node status via SSH (plink)
REM Uses plink.exe (from PuTTY) for SSH. Download: https://www.putty.org
REM
REM FIRST-TIME SETUP — Accept SSH fingerprint (run once):
REM   plink.exe -ssh mystic@YOUR_VXM_IP
REM   Type 'y' to accept the fingerprint, then Ctrl+C.

set VXM_HOST=192.168.1.50
set SSH_USER=mystic
set PLINK=plink.exe

echo.
echo === VxRail Manager Node Status ===
echo Host: %VXM_HOST%
echo.

echo --- System Version ---
%PLINK% -ssh -l %SSH_USER% -batch %VXM_HOST% "mystic vxm-cli system version"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not connect to %VXM_HOST%.
    echo Check: 1) hostname is correct, 2) SSH is enabled on VxRail Manager,
    echo        3) you have run plink manually once to accept the fingerprint.
    exit /b 1
)

echo.
echo --- Cluster Health ---
%PLINK% -ssh -l %SSH_USER% -batch %VXM_HOST% "mystic vxm-cli cluster health"

echo.
echo --- Node List ---
%PLINK% -ssh -l %SSH_USER% -batch %VXM_HOST% "mystic vxm-cli node list"

echo.
echo Done.
~~~

#### How to run this script — step by step

**Before you start — what you need**
- PuTTY installed on Windows — download from https://www.putty.org (get the installer)
- After installing PuTTY, `plink.exe` will be in `C:\Program Files\PuTTY\`
- SSH access enabled on the VxRail Manager appliance
- The `mystic` SSH user account credentials for VxRail Manager

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Save it as `vxrail-node-status.bat` on your Desktop

**Step 2 — Fill in your details**

Open the saved file and change these lines near the top:

| Variable | What to put here | How to find it |
|---|---|---|
| `VXM_HOST` | IP address of VxRail Manager | Ask your VMware admin |
| `SSH_USER` | SSH username | Usually `mystic` for VxRail Manager CLI |
| `PLINK` | Full path to plink.exe | Default: `C:\Program Files\PuTTY\plink.exe` |

If plink is not in your system PATH, change `set PLINK=plink.exe` to `set PLINK=C:\Program Files\PuTTY\plink.exe`

**Step 3 — Accept the SSH fingerprint first (one-time step)**

Open Command Prompt and run:
```
plink.exe -ssh mystic@192.168.1.50
```
Type `y` when asked to accept the fingerprint, then press Ctrl+C to disconnect. You only need to do this once per host.

**Step 4 — Open a terminal**

Open **Command Prompt**: Windows key → search `cmd` → press Enter

**Step 5 — Run the script**

```
cd C:\Users\YourName\Desktop
vxrail-node-status.bat
```

You can also double-click the `.bat` file in File Explorer.

**What you should see**

Three sections of output: the VxRail software version, cluster health status (Healthy/Degraded), and a list of nodes in the cluster. If the connection fails you will see an ERROR message with troubleshooting hints.
