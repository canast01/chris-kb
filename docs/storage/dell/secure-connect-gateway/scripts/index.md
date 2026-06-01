# Secure Connect Gateway — Scripts


<div class="kb-summary">
> Part of the [Dell Secure Connect Gateway](../index.md) reference.
</div>
```text
┌────────────────────────────────── Dell SCG — Scripts and Automation ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           SCG scripts: automation for reporting, health monitoring, and provisioning          │   │
│   │         REST API available for all operations; PowerShell and Python modules supported        │   │
│   │          Scripts must run from dedicated service accounts with least-privilege roles          │   │
│   │        Store credentials in vault; rotate service account passwords on defined schedule       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Script → authenticate REST → execute operation → verify → log result                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Collection         │  │        Array adapters       │  │         Per product         │   │
│   │          Transport          │  │        HTTPS outbound       │  │          No inbound         │   │
│   │         CloudIQ feed        │  │       Telemetry relay       │  │        Near real-time       │   │
│   │        Support tunnel       │  │        Remote assist        │  │        On-demand only       │   │
│   │           Alerting          │  │         Email/syslog        │  │       Threshold rules       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │        Port       │       Auth       │      Notes       │   │
│   │   SCG gateway    │  Telemetry hub   │    9443 (local)   │   Certificate    │ VM or appliance  │   │
│   │  Array adapter   │ Product connect  │     Array API     │   Service acct   │ Per product typ  │   │
│   │  CloudIQ relay   │ Health/perf feed │     HTTPS 443     │   Certificate    │   Dell-hosted    │   │
│   │  Support tunnel  │    TAC remote    │     HTTPS 443     │  One-time token  │    On-demand     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SCG VM or appliance on-prem · outbound HTTPS to Dell · connected storage arrays          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SCG                = Secure Connect Gateway; replaces ESRS as Dell remote support relay platform   │
│    ESRS               = EMC Secure Remote Services; predecessor to SCG; still supported on older ar...│
│    Adapter            = SCG component connecting to a specific array type: Unity, PowerStore, PowerMax│
│    CloudIQ relay      = SCG forwards array health telemetry to CloudIQ SaaS for analytics             │
│    Support tunnel     = Dell TAC can open an encrypted on-demand remote session via SCG               │
│    Device registration = arrays registered in SCG; SCG authenticates to Dell support portal           │
│    Site               = SCG logical grouping of arrays at a physical location within the organisation │
│    Policy             = SCG alert policy; defines which events trigger email or syslog notifications  │
│    SCG bundle         = log/diagnostic collection submitted to Dell support via SCG upload            │
│    Gateway HA         = two SCG instances in active-active; both relay telemetry independently        │
│    Port 9443          = SCG local management UI port; REST API also served on port 9443               │
│    Outbound only      = SCG connections are outbound HTTPS; no inbound firewall rules required        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---
## Connectivity Health Check

Tests outbound HTTPS connectivity from the SCG host to the required Dell support endpoints, checks the SCG service status, and prints a PASS/FAIL summary for each check. Suitable for cron or a monitoring probe.

~~~bash
#!/bin/bash
# scg_connectivity_check.sh — Secure Connect Gateway connectivity health check
# Run this script ON the SCG appliance or Linux host running the SCG service.
# Usage: ./scg_connectivity_check.sh

set -uo pipefail

PASS=0
FAIL=0

DELL_ENDPOINTS=(
  "https://esrs.emc.com"
  "https://cloudiq.dell.com"
  "https://download.emc.com"
  "https://support.dell.com"
)

SCG_LOCAL_API="https://localhost:9443/scg/api/v1/system/version"

check() {
  local label="$1"
  local result="$2"
  if [[ "$result" -eq 0 ]]; then
    printf "  %-50s  PASS\n" "$label"
    PASS=$((PASS + 1))
  else
    printf "  %-50s  FAIL\n" "$label"
    FAIL=$((FAIL + 1))
  fi
}

echo ""
echo "========================================"
echo "  SCG Connectivity Health Check"
echo "  Host : $(hostname -f 2>/dev/null || hostname)"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# --- Outbound endpoint reachability ---
echo "--- Outbound Dell Endpoint Reachability ---"
for endpoint in "${DELL_ENDPOINTS[@]}"; do
  curl -so /dev/null --max-time 10 --connect-timeout 8 "$endpoint" 2>/dev/null
  check "$endpoint" $?
done

# --- SCG service ---
echo ""
echo "--- SCG Service Status ---"
if command -v systemctl &>/dev/null; then
  systemctl is-active --quiet dell-scg 2>/dev/null
  check "dell-scg systemd service active" $?
else
  service dell-scg status &>/dev/null
  check "dell-scg init.d service active" $?
fi

# --- SCG local API ---
echo ""
echo "--- SCG Local API ---"
SCG_PASS="${SCG_PASS:-admin}"
API_RESP=$(curl -sk --max-time 10 -u "admin:${SCG_PASS}" "$SCG_LOCAL_API" 2>/dev/null)
if echo "$API_RESP" | grep -q "version"; then
  check "SCG local API reachable" 0
  SCG_VER=$(echo "$API_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('version','unknown'))" 2>/dev/null || echo "unknown")
  echo "  SCG Version: $SCG_VER"
else
  check "SCG local API reachable" 1
fi

echo ""
echo "========================================"
echo "  Results: $PASS passed, $FAIL failed"
echo "========================================"

[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
~~~

### How to run this script — step by step

**Before you start — what you need**
- Run this script directly on the SCG appliance or Linux server running the SCG service
- SSH access to that server, or log in locally
- The `curl` command must be available (installed by default on most Linux systems)
- The SCG admin password (set during SCG initial configuration)

**Step 1 — Save the file**

1. Copy the entire code block above
2. Save it as `scg_connectivity_check.sh` on the SCG server

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `SCG_PASS` | SCG admin password | Set when SCG was first configured |

**Step 3 — Open a terminal**

Open a terminal or SSH into the SCG server.

**Step 4 — Run the script**

```bash
chmod +x scg_connectivity_check.sh
SCG_PASS=yourpassword ./scg_connectivity_check.sh
```

**What you should see**

Connectivity test results (PASS/FAIL) for each Dell cloud endpoint (esrs.emc.com, cloudiq.dell.com, etc.), the SCG service status, and whether the local SCG API is responding. The final line shows total passed and failed checks.

---

## Device Registration Auditor

Queries the SCG REST API to list all registered devices, checks each device's connectivity status, and flags any device that is not in a connected/active state. Useful for quarterly audits and decommission cleanup.

~~~python
#!/usr/bin/env python3
# scg_device_audit.py — Audit registered devices on Dell Secure Connect Gateway
# Run on the SCG host or any host with network access to the SCG management interface.
# Requirements: requests
# Usage: SCG_HOST=scg01.example.com SCG_PASS=admin123 ./scg_device_audit.py

import os
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCG_HOST  = os.environ.get("SCG_HOST", "localhost")
SCG_USER  = os.environ.get("SCG_USER", "admin")
SCG_PASS  = os.environ.get("SCG_PASS", "")
SCG_PORT  = os.environ.get("SCG_PORT", "9443")
BASE_URL  = f"https://{SCG_HOST}:{SCG_PORT}/scg/api/v1"

if not SCG_PASS:
    print("ERROR: SCG_PASS must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()
AUTH = (SCG_USER, SCG_PASS)


def api_get(path):
    resp = session.get(f"{BASE_URL}{path}", auth=AUTH, verify=False, timeout=15)
    resp.raise_for_status()
    return resp.json()


def main():
    print("=" * 70)
    print(f"  SCG Device Registration Audit — {SCG_HOST}")
    print("=" * 70)

    # Get SCG version
    try:
        ver_data = api_get("/system/version")
        print(f"\n  SCG Version: {ver_data.get('version', 'unknown')}")
    except Exception as e:
        print(f"  WARNING: Could not retrieve SCG version: {e}")

    # List devices
    try:
        devices_data = api_get("/devices")
        devices = devices_data.get("devices", devices_data if isinstance(devices_data, list) else [])
    except Exception as e:
        print(f"\nERROR: Could not list devices: {e}")
        sys.exit(2)

    if not devices:
        print("\n  No devices registered.")
        sys.exit(0)

    not_connected = 0
    print(f"\n{'DEVICE NAME':<35}  {'TYPE':<20}  {'IP/HOST':<20}  {'STATUS'}")
    print("-" * 90)

    for dev in devices:
        name   = dev.get("name",   dev.get("hostname",  "unknown"))
        dtype  = dev.get("type",   dev.get("deviceType","unknown"))
        ip     = dev.get("ip",     dev.get("address",   "unknown"))
        status = dev.get("status", dev.get("connectivity", dev.get("state", "unknown"))).upper()

        marker = ""
        if status not in ("CONNECTED", "ACTIVE", "OK"):
            marker = "  <<< NOT CONNECTED"
            not_connected += 1

        print(f"{name:<35}  {dtype:<20}  {ip:<20}  {status}{marker}")

    print("-" * 90)
    print(f"\nTotal: {len(devices)} devices   Not connected: {not_connected}")

    if not_connected > 0:
        print(f"\nWARNING: {not_connected} device(s) not connected. "
              "Re-register from the array side or remove stale entries.")
        sys.exit(1)
    else:
        print("\nOK: All registered devices are connected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
~~~

### How to run this script — step by step

**Before you start — what you need**
- Python 3.7 or newer installed (python.org)
- The `requests` library: run `pip install requests` in Command Prompt
- Network access to the SCG management interface on port 9443
- The SCG admin password

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `scg_device_audit.py` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `SCG_HOST` | IP address or hostname of the SCG appliance | Ask your storage admin |
| `SCG_USER` | SCG admin username | Default is `admin` |
| `SCG_PASS` | SCG admin password | Set during SCG configuration |
| `SCG_PORT` | SCG management port | Default is `9443` |

**Step 3 — Open a terminal**

- **For .py (Python):** Open Command Prompt. Install Python first from python.org if needed.

**Step 4 — Run the script**

```bash
cd C:\Users\YourName\Desktop
set SCG_HOST=192.168.10.50
set SCG_PASS=yourpassword
python scg_device_audit.py
```

**What you should see**

The SCG version, then a table of all registered devices showing name, type, IP, and connectivity status. Any device not in CONNECTED/ACTIVE state is flagged with `<<< NOT CONNECTED`. The summary shows total devices and how many are disconnected.

---

## Ansible SCG Status Playbook

Playbook targeting the SCG host. Checks the SCG service status, verifies outbound connectivity to Dell endpoints, queries the local API for registered devices, and fails if any device is disconnected or the service is not running.

~~~yaml
---
# scg_status.yml — Ansible status check playbook for Dell Secure Connect Gateway
# Inventory host: scg (the SCG appliance or Linux host running dell-scg)
# Usage: ansible-playbook -i inventory scg_status.yml

- name: Dell Secure Connect Gateway Status Check
  hosts: scg
  gather_facts: false
  vars:
    scg_user: admin
    scg_pass: "{{ vault_scg_pass }}"
    scg_port: 9443
    dell_endpoints:
      - "https://esrs.emc.com"
      - "https://cloudiq.dell.com"

  tasks:
    - name: Check SCG service is running
      ansible.builtin.shell: |
        systemctl is-active dell-scg 2>/dev/null || service dell-scg status 2>/dev/null
      register: scg_service
      changed_when: false
      failed_when: false

    - name: Show SCG service status
      ansible.builtin.debug:
        msg: "{{ scg_service.stdout_lines }}"

    - name: Fail if SCG service is not active
      ansible.builtin.fail:
        msg: "dell-scg service is not running on {{ inventory_hostname }}"
      when: "'active' not in scg_service.stdout and 'running' not in scg_service.stdout"

    - name: Test outbound connectivity to Dell endpoints
      ansible.builtin.shell: >
        curl -so /dev/null --max-time 10 --connect-timeout 8 {{ item }} && echo PASS || echo FAIL
      loop: "{{ dell_endpoints }}"
      register: connectivity_results
      changed_when: false

    - name: Show connectivity results
      ansible.builtin.debug:
        msg: "{{ item.item }}: {{ item.stdout }}"
      loop: "{{ connectivity_results.results }}"
      loop_control:
        label: "{{ item.item }}"

    - name: Fail if any Dell endpoint is unreachable
      ansible.builtin.fail:
        msg: "Connectivity to {{ item.item }} FAILED on {{ inventory_hostname }}"
      when: "'FAIL' in item.stdout"
      loop: "{{ connectivity_results.results }}"
      loop_control:
        label: "{{ item.item }}"

    - name: Query SCG registered devices
      ansible.builtin.uri:
        url: "https://{{ inventory_hostname }}:{{ scg_port }}/scg/api/v1/devices"
        method: GET
        user: "{{ scg_user }}"
        password: "{{ scg_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
      register: devices_resp

    - name: Show registered devices
      ansible.builtin.debug:
        msg: "{{ devices_resp.json }}"

    - name: All checks passed
      ansible.builtin.debug:
        msg: "SCG health check completed successfully on {{ inventory_hostname }}."
~~~

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on a Linux/macOS control node (or WSL on Windows)
- An inventory entry for the SCG appliance under the host `scg`
- Ansible Vault or environment variable for the SCG password

**Step 1 — Save the file**

1. Copy the code block above
2. Save it as `scg_status.yml` in your Ansible working directory

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `scg_pass` | SCG admin password (use vault) | Set during SCG configuration |
| `scg_port` | SCG management port | Default is `9443` |
| `dell_endpoints` | List of Dell endpoints to test | Edit to add/remove endpoints as needed |

**Step 3 — Open a terminal**

Open a terminal on your Ansible control node.

**Step 4 — Run the script**

```text
ansible-playbook -i inventory scg_status.yml --ask-vault-pass
```

**What you should see**

Ansible checks the SCG service status, tests connectivity to each Dell endpoint (PASS/FAIL), then lists all registered devices via the SCG API. The play fails if the service is not running or if any Dell endpoint is unreachable.

---

## Windows: SCG Connection Test via Plink (CMD)

Uses plink.exe to SSH into the SCG appliance from a Windows PC and run service and device listing commands.

~~~batch
@echo off
REM scg_connection_test.bat — SCG connection test from Windows CMD
REM Uses plink.exe (PuTTY) to SSH into the SCG appliance.
REM Download PuTTY (includes plink.exe) from: https://www.putty.org
REM
REM FIRST TIME SETUP: Run this once to accept the host key:
REM   plink -ssh admin@192.168.1.100
REM   Type 'y' when asked, then Ctrl+C.

set SCG_HOST=192.168.1.100
set SSH_USER=admin
set PLINK=plink.exe

echo ========================================
echo   SCG Connection Test
echo   Host: %SCG_HOST%
echo ========================================
echo.

echo --- SCG Gateway Status ---
%PLINK% -ssh -l %SSH_USER% -batch %SCG_HOST% "dsagw status"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not connect to %SCG_HOST%. Check hostname and credentials.
    exit /b 1
)

echo.
echo --- Connected Devices ---
%PLINK% -ssh -l %SSH_USER% -batch %SCG_HOST% "dsagw list-devices"

echo.
echo ========================================
echo   Connection test complete.
echo ========================================
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Windows PC with plink.exe from PuTTY (https://www.putty.org — free download)
- SSH access to the SCG appliance management IP (port 22)
- The SCG admin username and password

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `scg_connection_test.bat` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `SCG_HOST` | IP address of the SCG appliance | Ask your storage admin |
| `SSH_USER` | SSH username | Default is `admin` |
| `PLINK` | Full path to plink.exe if not in PATH | e.g. `C:\Program Files\PuTTY\plink.exe` |

**Step 3 — Accept the host key (one-time setup)**

Open Command Prompt and run:
```text
plink -ssh admin@192.168.10.50
```
Type `y` when prompted, then press Ctrl+C.

**Step 4 — Open a terminal**

- **For .bat (Command Prompt):** Open Command Prompt (Windows key → type `cmd`).

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
scg_connection_test.bat
```

**What you should see**

The SCG gateway service status from `dsagw status`, then a list of devices that SCG is currently managing from `dsagw list-devices`. If the connection fails you will see an error message.

---

## Windows: SCG Device Inventory via REST API (PowerShell)

Queries the SCG REST API from a PowerShell window to list all managed devices and any active connectivity alerts.

~~~powershell
# scg_device_inventory.ps1 — SCG device inventory via REST API (Windows PowerShell)
# Requires: PowerShell 5.1+ (built into Windows 10/11)
# Run: .\scg_device_inventory.ps1

$ScgHost = "192.168.1.100"   # IP or hostname of your SCG appliance
$ScgUser = "admin"            # SCG admin username
$ScgPass = "yourpassword"     # SCG admin password

# Trust self-signed certificates
if (-not ([System.Management.Automation.PSTypeName]'TrustAll').Type) {
    Add-Type @"
    using System.Net; using System.Security.Cryptography.X509Certificates;
    public class TrustAll : ICertificatePolicy {
        public bool CheckValidationResult(ServicePoint s, X509Certificate c, WebRequest r, int p) { return true; }
    }
"@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAll
}
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Creds   = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${ScgUser}:${ScgPass}"))
$Headers = @{ Authorization = "Basic $Creds"; Accept = "application/json" }
$BaseUrl = "https://${ScgHost}/api/v2"

# Step 1: List managed devices
Write-Host "Fetching device inventory from SCG at $ScgHost ..."
try {
    $DevResp = Invoke-RestMethod -Uri "$BaseUrl/devices" -Headers $Headers
    $Devices = $DevResp.devices
    if (-not $Devices) { $Devices = $DevResp }
} catch {
    Write-Host "ERROR: Could not connect to SCG API - $($_.Exception.Message)"
    exit 1
}

Write-Host ""
Write-Host "========================================"
Write-Host "  SCG Managed Devices"
Write-Host "========================================"

$NotConnected = 0
if (-not $Devices -or $Devices.Count -eq 0) {
    Write-Host "  No devices found."
} else {
    foreach ($Dev in $Devices) {
        $Name   = $Dev.name
        $Type   = $Dev.type
        $IP     = $Dev.ip
        $Status = ($Dev.status).ToUpper()
        $Flag   = ""
        if ($Status -notin @("CONNECTED","ACTIVE","OK")) {
            $Flag = "  <<< NOT CONNECTED"
            $NotConnected++
        }
        Write-Host "  $Name  ($Type)  $IP  $Status$Flag"
    }
    Write-Host ""
    Write-Host "  Total: $($Devices.Count) devices   Not connected: $NotConnected"
}

# Step 2: Get active connectivity alerts
Write-Host ""
Write-Host "========================================"
Write-Host "  Active Connectivity Alerts"
Write-Host "========================================"
try {
    $AlertResp = Invoke-RestMethod -Uri "$BaseUrl/alerts" -Headers $Headers
    $Alerts = $AlertResp.alerts
    if (-not $Alerts) { $Alerts = $AlertResp }
    if (-not $Alerts -or $Alerts.Count -eq 0) {
        Write-Host "  No active alerts."
    } else {
        foreach ($Alert in $Alerts) {
            Write-Host "  [$($Alert.severity)] $($Alert.device_name): $($Alert.description)"
        }
    }
} catch {
    Write-Host "  WARNING: Could not retrieve alerts - $($_.Exception.Message)"
}

Write-Host ""
Write-Host "========================================"
Write-Host "  Inventory complete."
Write-Host "========================================"
~~~

### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or 11 (PowerShell 5.1 is already installed)
- Network access to the SCG appliance management interface (HTTPS, typically port 443)
- The SCG admin username and password

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `scg_device_inventory.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `$ScgHost` | IP address or hostname of the SCG appliance | Ask your storage admin |
| `$ScgUser` | SCG admin username | Default is `admin` |
| `$ScgPass` | SCG admin password | Set during SCG initial configuration |

**Step 3 — Open a terminal**

- **For .ps1 (PowerShell):** Press Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time)**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
.\scg_device_inventory.ps1
```

**What you should see**

A list of all devices registered in SCG with their name, type, IP, and connection status. Disconnected devices are flagged. Then a list of active connectivity alerts. If everything is healthy you will see "No devices" flagged and "No active alerts."

---

## Daily Check Script

SSHes to the SCG host, runs `dsagw status` and `dsagw list-devices`, counts devices in error state, and checks the last telemetry upload time. Prints PASS/FAIL output.

~~~bash
#!/bin/bash
# scg_daily_check.sh — Daily SCG status check via SSH
# Usage: SCG_HOST=scg01.example.com SSH_USER=admin ./scg_daily_check.sh

set -euo pipefail

SCG_HOST="${SCG_HOST:?Set SCG_HOST}"
SSH_USER="${SSH_USER:-admin}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"

FAIL=0
check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

echo "========================================"
echo "  SCG Daily Check"
echo "  Host : $SCG_HOST"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Check 1: SCG gateway running
echo "--- SCG Service Status ---"
STATUS_OUT=$(ssh $SSH_OPTS "${SSH_USER}@${SCG_HOST}" "dsagw status" 2>&1) || \
  { check_fail "SSH connection to $SCG_HOST failed"; exit 1; }
echo "$STATUS_OUT"
if echo "$STATUS_OUT" | grep -qi "running\|active\|started"; then
  check_pass "SCG gateway is running"
else
  check_fail "SCG gateway does not appear to be running"
fi

echo ""
# Check 2: All devices connected
echo "--- Device List ---"
DEVICES_OUT=$(ssh $SSH_OPTS "${SSH_USER}@${SCG_HOST}" "dsagw list-devices" 2>&1)
echo "$DEVICES_OUT"
ERROR_COUNT=$(echo "$DEVICES_OUT" | grep -ic "error\|disconnected\|failed" || true)
if [[ "$ERROR_COUNT" -eq 0 ]]; then
  check_pass "No devices in error state"
else
  check_fail "$ERROR_COUNT device(s) in error/disconnected state"
fi

echo ""
# Check 3: Last telemetry upload
echo "--- Last Telemetry Upload ---"
LOG_OUT=$(ssh $SSH_OPTS "${SSH_USER}@${SCG_HOST}" "dsagw log show --last 20" 2>&1) || LOG_OUT="unavailable"
LAST_UPLOAD=$(echo "$LOG_OUT" | grep -i "upload\|telemetry" | tail -1 || echo "not found")
echo "  Last upload entry: $LAST_UPLOAD"
if [[ "$LAST_UPLOAD" != "not found" ]]; then
  check_pass "Telemetry upload event found in recent logs"
else
  check_fail "No telemetry upload event found in last 20 log entries"
fi

echo ""
echo "========================================"
[[ "$FAIL" -eq 0 ]] && echo "  Result: PASS" || echo "  Result: FAIL"
exit $FAIL
~~~

---

## Incident Triage Script

Captures SCG status, device list with states, recent log entries, connectivity test to Dell backend, and certificate expiry to a timestamped file.

~~~bash
#!/bin/bash
# scg_triage.sh — Capture SCG state to timestamped file for incident triage
# Usage: SCG_HOST=scg01.example.com SSH_USER=admin ./scg_triage.sh

set -euo pipefail

SCG_HOST="${SCG_HOST:?Set SCG_HOST}"
SSH_USER="${SSH_USER:-admin}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"

TS=$(date '+%Y%m%d_%H%M%S')
OUTFILE="/tmp/scg_triage_${SCG_HOST}_${TS}.txt"

scg_ssh() { ssh $SSH_OPTS "${SSH_USER}@${SCG_HOST}" "$@" 2>&1 || echo "Command failed: $*"; }

{
  echo "========================================"
  echo "  SCG Incident Triage Capture"
  echo "  Host : $SCG_HOST"
  echo "  Time : $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================"

  echo ""
  echo "--- dsagw status ---"
  scg_ssh "dsagw status"

  echo ""
  echo "--- dsagw list-devices ---"
  scg_ssh "dsagw list-devices"

  echo ""
  echo "--- dsagw log show --last 50 ---"
  scg_ssh "dsagw log show --last 50"

  echo ""
  echo "--- Dell backend connectivity test ---"
  scg_ssh "curl -sk --max-time 10 -o /dev/null -w 'HTTP %{http_code}' https://esrs.emc.com && echo ' OK' || echo ' FAIL'"
  scg_ssh "curl -sk --max-time 10 -o /dev/null -w 'HTTP %{http_code}' https://cloudiq.dell.com && echo ' OK' || echo ' FAIL'"

  echo ""
  echo "--- Certificate expiry check ---"
  scg_ssh "openssl s_client -connect localhost:9443 -servername localhost </dev/null 2>/dev/null | openssl x509 -noout -dates" || echo "  Certificate check unavailable"

  echo ""
  echo "========================================"
  echo "  Triage capture complete: $OUTFILE"
  echo "========================================"
} | tee "$OUTFILE"

echo ""
echo "Output saved to: $OUTFILE"
~~~

---

## Change Pre-Check Script

Confirms SCG is running, all devices are connected, backend connectivity test passes, and certificate is valid for more than 30 days. Exits 2 on any failure.

~~~bash
#!/bin/bash
# scg_precheck.sh — Pre-check before SCG update or restart
# Usage: SCG_HOST=scg01.example.com SSH_USER=admin ./scg_precheck.sh

set -euo pipefail

SCG_HOST="${SCG_HOST:?Set SCG_HOST}"
SSH_USER="${SSH_USER:-admin}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"
CERT_WARN_DAYS=30
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

scg_ssh() { ssh $SSH_OPTS "${SSH_USER}@${SCG_HOST}" "$@" 2>&1; }

echo "========================================"
echo "  SCG Pre-Change Check"
echo "  Host : $SCG_HOST"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Check 1: SCG service running
STATUS=$(scg_ssh "dsagw status" 2>&1) || { check_fail "Cannot connect to $SCG_HOST via SSH"; exit 2; }
echo "$STATUS" | grep -qi "running\|active\|started" && \
  check_pass "SCG gateway running" || check_fail "SCG gateway not running"

# Check 2: All devices connected
DEVICES=$(scg_ssh "dsagw list-devices" 2>&1)
ERROR_COUNT=$(echo "$DEVICES" | grep -ic "error\|disconnected\|failed" || true)
[[ "$ERROR_COUNT" -eq 0 ]] && \
  check_pass "All devices connected (0 error states)" || \
  check_fail "$ERROR_COUNT device(s) in error/disconnected state"

# Check 3: Dell backend connectivity
for ENDPOINT in "https://esrs.emc.com" "https://cloudiq.dell.com"; do
  HTTP=$(scg_ssh "curl -sk --max-time 10 -o /dev/null -w '%{http_code}' ${ENDPOINT}" 2>/dev/null || echo "000")
  [[ "$HTTP" =~ ^(200|301|302|403) ]] && \
    check_pass "Backend reachable: $ENDPOINT (HTTP $HTTP)" || \
    check_fail "Backend unreachable: $ENDPOINT (HTTP $HTTP)"
done

# Check 4: Certificate valid for >30 days
EXPIRY=$(scg_ssh "openssl s_client -connect localhost:9443 -servername localhost </dev/null 2>/dev/null | openssl x509 -noout -enddate" 2>/dev/null | grep "notAfter" | cut -d= -f2 || echo "")
if [[ -n "$EXPIRY" ]]; then
  EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$EXPIRY" +%s 2>/dev/null || echo "0")
  NOW_EPOCH=$(date +%s)
  DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
  [[ "$DAYS_LEFT" -gt "$CERT_WARN_DAYS" ]] && \
    check_pass "Certificate valid for ${DAYS_LEFT} more days (expires: $EXPIRY)" || \
    check_fail "Certificate expires in ${DAYS_LEFT} days — renew before change (expires: $EXPIRY)"
else
  echo "  [SKIP] Certificate expiry check unavailable"
fi

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: READY — proceed with SCG change"
  exit 0
else
  echo "  Result: NOT READY — resolve failures before proceeding"
  exit 2
fi
~~~

---

## Post-Change Validation Script

After an SCG update or restart: re-runs the same checks, confirms all devices have reconnected, and verifies that telemetry has resumed. Compares device count to a pre-change baseline.

~~~bash
#!/bin/bash
# scg_postcheck.sh — Post-change validation after SCG update or restart
# Usage: SCG_HOST=x SSH_USER=admin EXPECTED_DEVICE_COUNT=5 ./scg_postcheck.sh

set -euo pipefail

SCG_HOST="${SCG_HOST:?Set SCG_HOST}"
SSH_USER="${SSH_USER:-admin}"
EXPECTED_DEVICE_COUNT="${EXPECTED_DEVICE_COUNT:-0}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

scg_ssh() { ssh $SSH_OPTS "${SSH_USER}@${SCG_HOST}" "$@" 2>&1; }

echo "========================================"
echo "  SCG Post-Change Validation"
echo "  Host                   : $SCG_HOST"
echo "  Expected device count  : $EXPECTED_DEVICE_COUNT"
echo "  Date                   : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Check 1: SCG running
STATUS=$(scg_ssh "dsagw status" 2>&1) || { check_fail "Cannot connect to $SCG_HOST"; exit 1; }
echo "$STATUS" | grep -qi "running\|active\|started" && \
  check_pass "SCG gateway running post-change" || check_fail "SCG gateway not running post-change"

# Check 2: Device count matches baseline
DEVICES=$(scg_ssh "dsagw list-devices" 2>&1)
echo "--- Device list ---"
echo "$DEVICES"
CONNECTED_COUNT=$(echo "$DEVICES" | grep -ic "connected\|active\|ok" || true)
ERROR_COUNT=$(echo "$DEVICES" | grep -ic "error\|disconnected\|failed" || true)

if [[ "$ERROR_COUNT" -eq 0 ]]; then
  check_pass "No devices in error state"
else
  check_fail "$ERROR_COUNT device(s) in error state after change"
fi

if [[ "$EXPECTED_DEVICE_COUNT" -gt 0 ]]; then
  if [[ "$CONNECTED_COUNT" -ge "$EXPECTED_DEVICE_COUNT" ]]; then
    check_pass "Connected device count ($CONNECTED_COUNT) meets baseline ($EXPECTED_DEVICE_COUNT)"
  else
    check_fail "Connected device count ($CONNECTED_COUNT) is below baseline ($EXPECTED_DEVICE_COUNT)"
  fi
fi

# Check 3: Telemetry resumed
LOGS=$(scg_ssh "dsagw log show --last 30" 2>&1)
TELEMETRY=$(echo "$LOGS" | grep -i "upload\|telemetry" | tail -1 || echo "")
[[ -n "$TELEMETRY" ]] && \
  check_pass "Telemetry upload event found in post-change logs" || \
  check_fail "No telemetry upload event in last 30 log entries — may still be reconnecting"

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: PASS — SCG post-change validation successful"
  exit 0
else
  echo "  Result: FAIL — investigate issues above"
  exit 1
fi
~~~

---

## Health Check Script

Cron-safe script checking SCG service status, device count, devices in error, and Dell backend reachability. Exits 0 (OK), 1 (warning), or 2 (critical).

~~~bash
#!/bin/bash
# scg_health.sh — Cron-safe SCG health check
# Usage: SCG_HOST=x SSH_USER=admin ./scg_health.sh
# Exit: 0=OK  1=WARNING  2=CRITICAL

SCG_HOST="${SCG_HOST:?Set SCG_HOST}"
SSH_USER="${SSH_USER:-admin}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"

scg_ssh() { ssh $SSH_OPTS "${SSH_USER}@${SCG_HOST}" "$@" 2>/dev/null; }

# SCG service status
STATUS=$(scg_ssh "dsagw status" 2>&1) || { echo "SCG_HEALTH host=${SCG_HOST} status=CRITICAL reason=ssh_failed"; exit 2; }
RUNNING=$(echo "$STATUS" | grep -ci "running\|active\|started" || true)

# Device counts
DEVICES=$(scg_ssh "dsagw list-devices" 2>&1)
TOTAL=$(echo "$DEVICES" | grep -c "." || true)
ERROR_COUNT=$(echo "$DEVICES" | grep -ic "error\|disconnected\|failed" || true)

# Backend reachability
BACKEND_OK=1
HTTP=$(scg_ssh "curl -sk --max-time 10 -o /dev/null -w '%{http_code}' https://esrs.emc.com" 2>/dev/null || echo "000")
[[ "$HTTP" =~ ^(200|301|302|403) ]] || BACKEND_OK=0

if [[ "$RUNNING" -eq 0 ]]; then
  echo "SCG_HEALTH host=${SCG_HOST} service=DOWN devices_total=${TOTAL} devices_error=${ERROR_COUNT} backend_reachable=${BACKEND_OK} status=CRITICAL"
  exit 2
elif [[ "$ERROR_COUNT" -gt 0 || "$BACKEND_OK" -eq 0 ]]; then
  echo "SCG_HEALTH host=${SCG_HOST} service=UP devices_total=${TOTAL} devices_error=${ERROR_COUNT} backend_reachable=${BACKEND_OK} status=WARNING"
  exit 1
else
  echo "SCG_HEALTH host=${SCG_HOST} service=UP devices_total=${TOTAL} devices_error=${ERROR_COUNT} backend_reachable=${BACKEND_OK} status=OK"
  exit 0
fi
~~~
