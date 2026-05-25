# Data Domain — Scripts

## Daily Health Check

SSH to a Data Domain appliance and print a formatted health summary covering filesystem space, compression ratio, active alerts, replication state, and system uptime. Exits non-zero if any active alerts are found.

~~~bash
#!/bin/bash
# dd_health_check.sh — Daily health check for a Dell Data Domain appliance
# Usage: DD_HOST=dd01.example.com DD_USER=sysadmin ./dd_health_check.sh

set -euo pipefail

DD_HOST="${DD_HOST:-}"
DD_USER="${DD_USER:-sysadmin}"
ALERT_COUNT=0

if [[ -z "$DD_HOST" ]]; then
  echo "ERROR: DD_HOST is not set." >&2
  exit 1
fi

run_cmd() {
  local label="$1"
  local cmd="$2"
  echo "========================================"
  echo "  $label"
  echo "========================================"
  ssh -o StrictHostKeyChecking=no -o BatchMode=yes "${DD_USER}@${DD_HOST}" "$cmd"
  echo ""
}

echo ""
echo "########################################"
echo "  Data Domain Health Check"
echo "  Host : $DD_HOST"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "########################################"
echo ""

run_cmd "FILESYSTEM SPACE"         "filesys show space"
run_cmd "COMPRESSION RATIO"        "filesys show compression"
run_cmd "SYSTEM UPTIME"            "system show uptime"
run_cmd "REPLICATION STATE"        "replication show"

echo "========================================"
echo "  ACTIVE ALERTS"
echo "========================================"
ALERTS=$(ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
  "${DD_USER}@${DD_HOST}" "alerts show current")
echo "$ALERTS"
echo ""

# Count non-header, non-empty alert lines
ALERT_COUNT=$(echo "$ALERTS" | grep -cE '^\s+[0-9]+' || true)

echo "========================================"
echo "  SUMMARY"
echo "========================================"
if [[ "$ALERT_COUNT" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $ALERT_COUNT active alert(s) found."
  exit 1
else
  echo "STATUS: OK — No active alerts."
  exit 0
fi
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux/macOS computer or Windows with Git Bash installed
- SSH access to your Data Domain appliance (ask your storage admin for the IP and a username)
- The Data Domain user account must have at least read-only (sysadmin) permissions

**Step 1 — Save the file**

1. Open **Notepad** (search for it in the Start menu) or any text editor
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `dd_health_check.sh` and save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file and change these values near the top:

| Variable | What to put | How to find it |
|---|---|---|
| `DD_HOST` | IP address or hostname of your Data Domain | Ask your storage admin, e.g. `192.168.10.50` |
| `DD_USER` | SSH username on the Data Domain | Default is `sysadmin` |

**Step 3 — Open a terminal**

- **For .sh (Bash):** Install Git for Windows (gitforwindows.org) and open Git Bash.

**Step 4 — Run the script**

```bash
cd ~/Desktop
chmod +x dd_health_check.sh
DD_HOST=192.168.10.50 DD_USER=sysadmin ./dd_health_check.sh
```

**What you should see**

A series of sections separated by `========` lines: filesystem space usage, compression ratio, system uptime, replication state, and active alerts. The final line reads either `STATUS: OK — No active alerts.` or `STATUS: DEGRADED — X active alert(s) found.` If degraded, the script exits with a non-zero code.

---

## Replication Lag Monitor

SSH to a Data Domain appliance and parse `replication show` output. Extracts lag time per replication context and emits Nagios-compatible WARNING or CRITICAL output. Designed to be called directly by Icinga, Nagios, or a monitoring relay.

~~~perl
#!/usr/bin/env perl
# dd_repl_monitor.pl — Data Domain replication lag monitor
# Usage: DD_HOST=dd01 DD_USER=sysadmin WARN_MIN=30 CRIT_MIN=60 ./dd_repl_monitor.pl

use strict;
use warnings;

my $dd_host  = $ENV{DD_HOST}  or die "ERROR: DD_HOST not set\n";
my $dd_user  = $ENV{DD_USER}  || 'sysadmin';
my $warn_min = $ENV{WARN_MIN} // 30;
my $crit_min = $ENV{CRIT_MIN} // 60;

# Fetch replication show output via SSH
my $output = qx{ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${dd_user}\@${dd_host} "replication show" 2>&1};
if ($? != 0) {
    print "UNKNOWN: SSH to $dd_host failed\n";
    exit 3;
}

my @contexts;
my $worst_state = 0;  # 0=OK 1=WARN 2=CRIT

# Parse replication show output
# Example line: ctx:1  source:mtree://dd01/data/col1/veeam  dest:mtree://dd02/...  state:Normal  lag:00:15:23
for my $line (split /\n/, $output) {
    next unless $line =~ /\bctx:/;

    my ($ctx)   = $line =~ /ctx:(\S+)/;
    my ($state) = $line =~ /state:(\S+)/;
    my ($lag)   = $line =~ /lag:(\d+:\d+:\d+)/;

    $ctx   //= 'unknown';
    $state //= 'unknown';
    $lag   //= '00:00:00';

    # Convert lag HH:MM:SS to minutes
    my ($hh, $mm, $ss) = split /:/, $lag;
    my $lag_minutes = ($hh // 0) * 60 + ($mm // 0) + int(($ss // 0) / 60);

    my $status = 'OK';
    if ($lag_minutes >= $crit_min) {
        $status      = 'CRITICAL';
        $worst_state = 2 if $worst_state < 2;
    } elsif ($lag_minutes >= $warn_min) {
        $status      = 'WARNING';
        $worst_state = 1 if $worst_state < 1;
    }

    push @contexts, {
        ctx        => $ctx,
        state      => $state,
        lag        => $lag,
        lag_min    => $lag_minutes,
        status     => $status,
    };
}

if (!@contexts) {
    print "UNKNOWN: No replication contexts found in output\n";
    exit 3;
}

# Print results table
printf "%-6s  %-14s  %-10s  %8s  %s\n",
    'CTX', 'STATE', 'LAG', 'LAG(min)', 'STATUS';
printf "%s\n", '-' x 60;
for my $c (@contexts) {
    printf "%-6s  %-14s  %-10s  %8d  %s\n",
        $c->{ctx}, $c->{state}, $c->{lag}, $c->{lag_min}, $c->{status};
}

# Exit with worst state
if ($worst_state == 2) {
    print "\nCRITICAL: One or more replication contexts exceed ${crit_min}-minute lag threshold.\n";
    exit 2;
} elsif ($worst_state == 1) {
    print "\nWARNING: One or more replication contexts exceed ${warn_min}-minute lag threshold.\n";
    exit 1;
} else {
    print "\nOK: All replication contexts within lag thresholds.\n";
    exit 0;
}
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux/macOS computer or Windows with Git Bash and Strawberry Perl installed
- SSH access to your Data Domain appliance
- Strawberry Perl (Windows): download from strawberryperl.com — it is free and installs in a few clicks

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `dd_repl_monitor.pl` and save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file and change these values (or pass them as environment variables):

| Variable | What to put | How to find it |
|---|---|---|
| `DD_HOST` | IP or hostname of your Data Domain | Ask your storage admin |
| `DD_USER` | SSH username | Default is `sysadmin` |
| `WARN_MIN` | Minutes of lag before WARNING | Default is `30` |
| `CRIT_MIN` | Minutes of lag before CRITICAL | Default is `60` |

**Step 3 — Open a terminal**

- **For .pl (Perl):** Open Command Prompt. Install Strawberry Perl from strawberryperl.com if needed.

**Step 4 — Run the script**

```bash
cd C:\Users\YourName\Desktop
set DD_HOST=192.168.10.50
set DD_USER=sysadmin
perl dd_repl_monitor.pl
```

**What you should see**

A table with columns CTX, STATE, LAG, LAG(min), and STATUS for each replication context. The final line says `OK`, `WARNING`, or `CRITICAL`. If any context is lagging beyond your thresholds the script exits non-zero — useful for plugging into a monitoring system like Nagios.

---

## Ansible Daily Check Playbook

Playbook targeting the `data_domain` host group. Runs filesystem space, alert, and replication checks via SSH and prints each result using the `debug` module.

~~~yaml
---
# dd_daily_check.yml — Ansible daily health check playbook for Data Domain
# Inventory group: data_domain
# Required vars: dd_user (default: sysadmin)
# Usage: ansible-playbook -i inventory dd_daily_check.yml

- name: Dell Data Domain Daily Health Check
  hosts: data_domain
  gather_facts: false
  vars:
    dd_user: sysadmin

  tasks:
    - name: Check filesystem space
      ansible.builtin.raw: "filesys show space"
      register: filesys_space
      changed_when: false

    - name: Show filesystem space output
      ansible.builtin.debug:
        msg: "{{ filesys_space.stdout_lines }}"

    - name: Check active alerts
      ansible.builtin.raw: "alerts show current"
      register: alerts_output
      changed_when: false

    - name: Show active alerts output
      ansible.builtin.debug:
        msg: "{{ alerts_output.stdout_lines }}"

    - name: Check replication state
      ansible.builtin.raw: "replication show"
      register: repl_output
      changed_when: false

    - name: Show replication state output
      ansible.builtin.debug:
        msg: "{{ repl_output.stdout_lines }}"

    - name: Fail if active alerts detected
      ansible.builtin.fail:
        msg: "Active alerts found on {{ inventory_hostname }}. Review output above."
      when: >
        alerts_output.stdout is defined and
        alerts_output.stdout | regex_search('[0-9]+\\s+\\w+\\s+\\w+')
~~~

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on a Linux/macOS control node (or WSL on Windows)
- An inventory file listing your Data Domain appliances under the group `data_domain`
- SSH access from the Ansible control node to the Data Domain appliances

**Step 1 — Save the file**

1. Open a text editor
2. Copy the entire code block above
3. Save it as `dd_daily_check.yml` in your Ansible working directory

**Step 2 — Fill in your details**

Open the saved file and change these values near the top:

| Variable | What to put | How to find it |
|---|---|---|
| `dd_user` | SSH username on Data Domain | Default is `sysadmin` |

Also ensure your inventory file has a `[data_domain]` group with the correct IP addresses or hostnames.

**Step 3 — Open a terminal**

Open a terminal on your Ansible control node (Linux, macOS, or WSL).

**Step 4 — Run the script**

```bash
cd /path/to/your/playbooks
ansible-playbook -i inventory dd_daily_check.yml
```

**What you should see**

Ansible runs three tasks on each Data Domain host and prints the raw output of `filesys show space`, `alerts show current`, and `replication show`. If any alerts are detected the play fails with a message telling you to review the output above.

---

## DDBoost Client Check

Runs `ddboost show clients` and `ddboost status`, parses for disconnected clients, and prints a formatted table. Exits non-zero if any client is found in a disconnected or unknown state.

~~~bash
#!/bin/bash
# dd_ddboost_check.sh — Check DDBoost client connectivity on a Data Domain appliance
# Usage: DD_HOST=dd01.example.com DD_USER=sysadmin ./dd_ddboost_check.sh

set -euo pipefail

DD_HOST="${DD_HOST:-}"
DD_USER="${DD_USER:-sysadmin}"

if [[ -z "$DD_HOST" ]]; then
  echo "ERROR: DD_HOST is not set." >&2
  exit 1
fi

echo "========================================"
echo "  DDBoost Client Check — $DD_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Fetch DDBoost clients list
CLIENTS=$(ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
  "${DD_USER}@${DD_HOST}" "ddboost show clients")

# Fetch DDBoost overall status
STATUS=$(ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
  "${DD_USER}@${DD_HOST}" "ddboost status")

echo "--- DDBoost Status ---"
echo "$STATUS"
echo ""
echo "--- Client Table ---"
printf "%-30s  %-15s  %-10s\n" "CLIENT" "IP/HOSTNAME" "STATE"
printf "%s\n" "--------------------------------------------------------------"

DISCONNECTED=0
# Parse client lines — format: <name>  <ip>  <state>  ...
while IFS= read -r line; do
  # Skip header and blank lines
  [[ "$line" =~ ^(Client|---|$) ]] && continue
  [[ -z "$line" ]] && continue

  client=$(echo "$line" | awk '{print $1}')
  ip=$(echo "$line"     | awk '{print $2}')
  state=$(echo "$line"  | awk '{print $3}')

  [[ -z "$client" ]] && continue

  if [[ "${state,,}" != "connected" ]]; then
    DISCONNECTED=$((DISCONNECTED + 1))
    printf "%-30s  %-15s  %-10s  <<< DISCONNECTED\n" "$client" "$ip" "$state"
  else
    printf "%-30s  %-15s  %-10s\n" "$client" "$ip" "$state"
  fi
done <<< "$CLIENTS"

echo ""
echo "========================================"
if [[ "$DISCONNECTED" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $DISCONNECTED disconnected DDBoost client(s)."
  exit 1
else
  echo "STATUS: OK — All DDBoost clients connected."
  exit 0
fi
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux/macOS computer or Windows with Git Bash installed
- SSH access to your Data Domain appliance
- DDBoost must be licensed and enabled on the Data Domain

**Step 1 — Save the file**

1. Open **Notepad** or any text editor
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `dd_ddboost_check.sh` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `DD_HOST` | IP address or hostname of your Data Domain | Ask your storage admin |
| `DD_USER` | SSH username | Default is `sysadmin` |

**Step 3 — Open a terminal**

- **For .sh (Bash):** Install Git for Windows (gitforwindows.org) and open Git Bash.

**Step 4 — Run the script**

```bash
cd ~/Desktop
chmod +x dd_ddboost_check.sh
DD_HOST=192.168.10.50 DD_USER=sysadmin ./dd_ddboost_check.sh
```

**What you should see**

The DDBoost overall status followed by a table showing each backup client, its IP, and its connection state. Any disconnected client is flagged with `<<< DISCONNECTED`. The final line shows `STATUS: OK` or `STATUS: DEGRADED` with a count of disconnected clients.

---

## Windows: Data Domain Health Check via Plink (CMD)

Uses plink.exe (part of the free PuTTY package) to SSH into the Data Domain from a Windows machine and run the three most important health commands: system stats, active alerts, and filesystem space.

~~~batch
@echo off
REM dd_health_check.bat — Data Domain health check from Windows CMD
REM Uses plink.exe (PuTTY) to SSH into the Data Domain appliance.
REM Download PuTTY (includes plink.exe) from: https://www.putty.org
REM
REM FIRST TIME SETUP: Run this once to accept the host key:
REM   plink -ssh admin@192.168.1.100
REM   Type 'y' when asked to trust the fingerprint, then Ctrl+C.

set DD_HOST=192.168.1.100
set SSH_USER=sysadmin
set PLINK=plink.exe

echo ========================================
echo   Data Domain Health Check
echo   Host: %DD_HOST%
echo ========================================
echo.

echo --- System Stats ---
%PLINK% -ssh -l %SSH_USER% -batch %DD_HOST% "ddsh -c ""system show stats"""
if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not connect to %DD_HOST%. Check hostname and credentials.
    exit /b 1
)

echo.
echo --- Active Alerts ---
%PLINK% -ssh -l %SSH_USER% -batch %DD_HOST% "ddsh -c ""alerts show current"""

echo.
echo --- Filesystem Space ---
%PLINK% -ssh -l %SSH_USER% -batch %DD_HOST% "ddsh -c ""filesys show space"""

echo.
echo ========================================
echo   Health check complete.
echo ========================================
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Windows PC (Windows 10 or 11)
- plink.exe from PuTTY — download the installer from https://www.putty.org (it is free)
- SSH access to your Data Domain appliance (IP address and a username/password)

**Step 1 — Save the file**

1. Open **Notepad** (search for it in the Start menu)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `dd_health_check.bat` and save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file and change these values near the top:

| Variable | What to put | How to find it |
|---|---|---|
| `DD_HOST` | IP address of your Data Domain | Ask your storage admin, e.g. `192.168.10.50` |
| `SSH_USER` | SSH username | Default is `sysadmin` |
| `PLINK` | Full path to plink.exe if not in PATH | e.g. `C:\Program Files\PuTTY\plink.exe` |

**Step 3 — Accept the host key (one-time setup)**

The very first time you connect, plink needs you to trust the server's fingerprint. Open Command Prompt and run:
```text
plink -ssh sysadmin@192.168.10.50
```
Type `y` when asked, then press Ctrl+C to exit. You only need to do this once.

**Step 4 — Open a terminal**

- **For .bat (Command Prompt):** Open Command Prompt (Windows key → type `cmd`).

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
dd_health_check.bat
```

**What you should see**

Three sections of output: system performance counters, a list of any active alerts (or "No active alerts"), and a breakdown of how much space the filesystem is using and how much is free.

---

## Windows: Data Domain Health via REST API (PowerShell)

Uses the Data Domain REST API to authenticate, pull system information, and check active alerts — all from a PowerShell window on your Windows PC. No SSH required.

~~~powershell
# dd_health_rest.ps1 — Data Domain health check via REST API (Windows PowerShell)
# Requires: PowerShell 5.1+ (built into Windows 10/11)
# Run: .\dd_health_rest.ps1

$DdHost = "192.168.1.100"   # Your Data Domain IP or hostname
$DdUser = "sysadmin"         # API username
$DdPass = "yourpassword"     # API password

# Trust self-signed certificates (Data Domain uses self-signed certs by default)
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

$BaseUrl = "https://${DdHost}:3009/rest/v1.0"

# Step 1: Authenticate and get auth token
Write-Host "Authenticating to $DdHost ..."
$AuthBody = @{ username = $DdUser; password = $DdPass } | ConvertTo-Json
try {
    $AuthResp = Invoke-RestMethod -Uri "$BaseUrl/auth" `
        -Method POST `
        -Body $AuthBody `
        -ContentType "application/json"
} catch {
    Write-Host "ERROR: Authentication failed - $($_.Exception.Message)"
    exit 1
}

$Token = $AuthResp.token
if (-not $Token) {
    Write-Host "ERROR: No token returned. Check credentials."
    exit 1
}
Write-Host "Authentication successful."
$Headers = @{ "X-DD-AUTH-TOKEN" = $Token; "Accept" = "application/json" }

# Step 2: Get system information
Write-Host ""
Write-Host "========================================"
Write-Host "  System Information"
Write-Host "========================================"
try {
    $SysInfo = Invoke-RestMethod -Uri "$BaseUrl/system" -Headers $Headers
    Write-Host "  Hostname   : $($SysInfo.hostname)"
    Write-Host "  Model      : $($SysInfo.model)"
    Write-Host "  Serial     : $($SysInfo.serial_no)"
    Write-Host "  SW Version : $($SysInfo.version)"
    Write-Host "  Uptime     : $($SysInfo.uptime)"
} catch {
    Write-Host "  WARNING: Could not retrieve system info - $($_.Exception.Message)"
}

# Step 3: Get active alerts
Write-Host ""
Write-Host "========================================"
Write-Host "  Active Alerts"
Write-Host "========================================"
try {
    $AlertsResp = Invoke-RestMethod -Uri "$BaseUrl/system/alerts" -Headers $Headers
    $Alerts = $AlertsResp.alerts
    if (-not $Alerts -or $Alerts.Count -eq 0) {
        Write-Host "  No active alerts."
    } else {
        foreach ($Alert in $Alerts) {
            Write-Host "  [$($Alert.severity)] $($Alert.description)"
        }
        Write-Host ""
        Write-Host "  Total active alerts: $($Alerts.Count)"
    }
} catch {
    Write-Host "  WARNING: Could not retrieve alerts - $($_.Exception.Message)"
}

Write-Host ""
Write-Host "========================================"
Write-Host "  Health check complete."
Write-Host "========================================"
~~~

### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or 11 (PowerShell 5.1 is already installed — no downloads needed)
- Network access to your Data Domain management interface (port 3009)
- A Data Domain username and password with at least read access

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `dd_health_rest.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file and change these three lines near the top:

| Variable | What to put | How to find it |
|---|---|---|
| `$DdHost` | IP address or hostname of your Data Domain | Ask your storage admin |
| `$DdUser` | API username | Default is `sysadmin` |
| `$DdPass` | Password for that user | Ask your storage admin |

**Step 3 — Open a terminal**

- **For .ps1 (PowerShell):** Press Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time)**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
.\dd_health_rest.ps1
```

**What you should see**

First a confirmation that authentication succeeded, then a System Information block showing the Data Domain hostname, model, serial number, software version, and uptime. Then an Active Alerts block — either "No active alerts" or a list of alerts with their severity levels.

---

## Daily Check Script

SSHes to the Data Domain appliance and checks alerts, disk health, filesystem space (flagging above 80%), replication state, and compression ratio — printing PASS/FAIL for each check.

```bash
#!/bin/bash
# dd_daily_check.sh — Daily operations check for Dell Data Domain
# Usage: SSH_USER=sysadmin DD_HOST=dd01.example.com ./dd_daily_check.sh

set -uo pipefail

SSH_USER="${SSH_USER:-sysadmin}"
DD_HOST="${DD_HOST:-}"

if [[ -z "$DD_HOST" ]]; then
  echo "ERROR: DD_HOST is not set." >&2
  exit 1
fi

PASS=0
FAIL=0
SPACE_WARN_PCT=80

ddcmd() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$DD_HOST" "ddsh -c \"$1\""
}

check() {
  local label="$1"
  local rc="$2"
  if [[ "$rc" -eq 0 ]]; then
    printf "  %-50s  PASS\n" "$label"
    PASS=$((PASS + 1))
  else
    printf "  %-50s  FAIL\n" "$label"
    FAIL=$((FAIL + 1))
  fi
}

echo "========================================"
echo "  Data Domain Daily Check — $DD_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 1. Alerts — no current alerts
ALERTS=$(ddcmd "alerts show current" 2>&1)
echo "$ALERTS"
echo "$ALERTS" | grep -qiE "emergency|alert|critical|error" \
  && check "alerts (none expected)" 1 || check "alerts (clean)" 0

# 2. Disk health
DISKS=$(ddcmd "disk show state" 2>&1)
echo "$DISKS"
echo "$DISKS" | grep -qi "failed\|absent\|reconstructing\|unknown" \
  && check "disk health" 1 || check "disk health (all OK)" 0

# 3. Filesystem space (<80%)
SPACE=$(ddcmd "filesys show space" 2>&1)
echo "$SPACE"
HIGH=$(echo "$SPACE" | grep -oE '[0-9]+(\.[0-9]+)?%' | tr -d '%' | awk -v t="$SPACE_WARN_PCT" '$1 > t' | wc -l | tr -d ' ')
[[ "$HIGH" -gt 0 ]] \
  && check "filesystem space (<${SPACE_WARN_PCT}%)" 1 \
  || check "filesystem space (<${SPACE_WARN_PCT}%)" 0

# 4. Replication state
REPL=$(ddcmd "replication show all" 2>&1)
echo "$REPL"
echo "$REPL" | grep -qi "error\|disabled\|idle-error\|in-error" \
  && check "replication state" 1 || check "replication state (OK)" 0

# 5. Compression ratio — report only
COMP=$(ddcmd "filesys show compression" 2>&1)
echo "$COMP"
echo "  [INFO] compression output above"
check "compression stats retrieved" $?

echo "========================================"
echo "  PASS: $PASS   FAIL: $FAIL"
[[ "$FAIL" -eq 0 ]] && echo "  STATUS: OK" && exit 0 || echo "  STATUS: DEGRADED" && exit 1
```

---

## Incident Triage Script

Captures DD OS version, system stats, current alerts, disk state, filesystem space, compression ratios, and replication status to a timestamped file for support handoff.

```bash
#!/bin/bash
# dd_triage.sh — Incident triage data capture for Dell Data Domain
# Usage: SSH_USER=sysadmin DD_HOST=dd01.example.com ./dd_triage.sh

SSH_USER="${SSH_USER:-sysadmin}"
DD_HOST="${DD_HOST:-}"

if [[ -z "$DD_HOST" ]]; then
  echo "ERROR: DD_HOST is not set." >&2
  exit 1
fi

OUTFILE="dd_triage_$(date '+%Y%m%d_%H%M%S').txt"

ddcmd() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$DD_HOST" "ddsh -c \"$1\""
}

section() {
  echo "" >> "$OUTFILE"
  echo "========================================" >> "$OUTFILE"
  echo "  $1" >> "$OUTFILE"
  echo "========================================" >> "$OUTFILE"
}

{
  echo "Data Domain Triage Capture"
  echo "Host : $DD_HOST"
  echo "Date : $(date '+%Y-%m-%d %H:%M:%S')"
} > "$OUTFILE"

section "VERSION";          ddcmd "system show version"      >> "$OUTFILE" 2>&1
section "HOSTNAME";         ddcmd "net show hostname"         >> "$OUTFILE" 2>&1
section "SYSTEM STATS";     ddcmd "system show stats"         >> "$OUTFILE" 2>&1
section "ALERTS";           ddcmd "alerts show current"       >> "$OUTFILE" 2>&1
section "DISK STATE";       ddcmd "disk show state"           >> "$OUTFILE" 2>&1
section "FILESYSTEM SPACE"; ddcmd "filesys show space"        >> "$OUTFILE" 2>&1
section "COMPRESSION";      ddcmd "filesys show compression"  >> "$OUTFILE" 2>&1
section "REPLICATION";      ddcmd "replication show all"      >> "$OUTFILE" 2>&1

echo "Triage data written to: $OUTFILE"
```

---

## Change Pre-Check Script

Confirms no critical alerts are present, all disks are healthy, the filesystem is under 85% full, and all replication sessions are active — exits 2 on any failure.

```bash
#!/bin/bash
# dd_precheck.sh — Pre-change validation for Dell Data Domain
# Usage: SSH_USER=sysadmin DD_HOST=dd01.example.com ./dd_precheck.sh

set -uo pipefail

SSH_USER="${SSH_USER:-sysadmin}"
DD_HOST="${DD_HOST:-}"
SPACE_LIMIT=85

if [[ -z "$DD_HOST" ]]; then
  echo "ERROR: DD_HOST is not set." >&2
  exit 1
fi

ISSUES=0

ddcmd() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$DD_HOST" "ddsh -c \"$1\""
}

fail() { echo "  FAIL: $1"; ISSUES=$((ISSUES + 1)); }
pass() { echo "  PASS: $1"; }

echo "========================================"
echo "  Data Domain Pre-Change Check — $DD_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 1. No critical alerts
ALERTS=$(ddcmd "alerts show current" 2>&1)
echo "$ALERTS" | grep -qiE "emergency|alert|critical|error" \
  && fail "critical alert(s) present" || pass "no critical alerts"

# 2. All disks healthy
DISKS=$(ddcmd "disk show state" 2>&1)
echo "$DISKS" | grep -qi "failed\|absent\|reconstructing\|unknown" \
  && fail "unhealthy disk(s) found" || pass "all disks healthy"

# 3. Filesystem below 85%
SPACE=$(ddcmd "filesys show space" 2>&1)
HIGH=$(echo "$SPACE" | grep -oE '[0-9]+(\.[0-9]+)?%' | tr -d '%' | awk -v t="$SPACE_LIMIT" '$1 >= t' | wc -l | tr -d ' ')
[[ "$HIGH" -gt 0 ]] \
  && fail "filesystem at or above ${SPACE_LIMIT}% full" \
  || pass "filesystem below ${SPACE_LIMIT}%"

# 4. Replication sessions active
REPL=$(ddcmd "replication show all" 2>&1)
echo "$REPL" | grep -qi "error\|disabled\|idle-error\|in-error" \
  && fail "replication session(s) not active" || pass "replication sessions active"

echo "========================================"
if [[ "$ISSUES" -gt 0 ]]; then
  echo "  PRE-CHECK FAILED — $ISSUES issue(s). Do not proceed."
  exit 2
fi
echo "  PRE-CHECK PASSED — Safe to proceed."
exit 0
```

---

## Post-Change Validation Script

Runs the same checks as the pre-check after maintenance and additionally confirms the DD OS version matches an expected value and that replication has resumed.

```bash
#!/bin/bash
# dd_postcheck.sh — Post-change validation for Dell Data Domain
# Usage: SSH_USER=sysadmin DD_HOST=dd01.example.com \
#        EXPECTED_VERSION="7.13.0.0" ./dd_postcheck.sh

set -uo pipefail

SSH_USER="${SSH_USER:-sysadmin}"
DD_HOST="${DD_HOST:-}"
EXPECTED_VERSION="${EXPECTED_VERSION:-}"
SPACE_LIMIT=85

if [[ -z "$DD_HOST" ]]; then
  echo "ERROR: DD_HOST is not set." >&2
  exit 1
fi

ISSUES=0

ddcmd() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$DD_HOST" "ddsh -c \"$1\""
}

fail() { echo "  FAIL: $1"; ISSUES=$((ISSUES + 1)); }
pass() { echo "  PASS: $1"; }

echo "========================================"
echo "  Data Domain Post-Change Validation — $DD_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 1. No critical alerts
ALERTS=$(ddcmd "alerts show current" 2>&1)
echo "$ALERTS" | grep -qiE "emergency|alert|critical|error" \
  && fail "critical alert(s) present" || pass "no critical alerts"

# 2. All disks healthy
DISKS=$(ddcmd "disk show state" 2>&1)
echo "$DISKS" | grep -qi "failed\|absent\|reconstructing\|unknown" \
  && fail "unhealthy disk(s) found" || pass "all disks healthy"

# 3. Filesystem below 85%
SPACE=$(ddcmd "filesys show space" 2>&1)
HIGH=$(echo "$SPACE" | grep -oE '[0-9]+(\.[0-9]+)?%' | tr -d '%' | awk -v t="$SPACE_LIMIT" '$1 >= t' | wc -l | tr -d ' ')
[[ "$HIGH" -gt 0 ]] \
  && fail "filesystem at or above ${SPACE_LIMIT}%" \
  || pass "filesystem below ${SPACE_LIMIT}%"

# 4. Replication resumed
REPL=$(ddcmd "replication show all" 2>&1)
echo "$REPL" | grep -qi "error\|disabled\|idle-error\|in-error" \
  && fail "replication not active after change" || pass "replication active"

# 5. DD OS version check (if EXPECTED_VERSION set)
if [[ -n "$EXPECTED_VERSION" ]]; then
  VER=$(ddcmd "system show version" 2>&1)
  echo "$VER" | grep -q "$EXPECTED_VERSION" \
    && pass "DD OS version matches $EXPECTED_VERSION" \
    || fail "DD OS version does not match expected $EXPECTED_VERSION"
else
  echo "  INFO: EXPECTED_VERSION not set — skipping version check"
fi

echo "========================================"
if [[ "$ISSUES" -gt 0 ]]; then
  echo "  POST-CHECK FAILED — $ISSUES issue(s). Investigate before closing change."
  exit 2
fi
echo "  POST-CHECK PASSED — All checks healthy."
exit 0
```

---

## Health Check Script

Cron-safe single script reporting system uptime, disk health, free space percentage, dedup ratio, and replication status — exits 0 for OK, 1 for WARN, 2 for CRIT.

```bash
#!/bin/bash
# dd_health.sh — Cron-safe health check for Dell Data Domain
# Usage: SSH_USER=sysadmin DD_HOST=dd01.example.com ./dd_health.sh
# Exit codes: 0=OK  1=WARN  2=CRIT

SSH_USER="${SSH_USER:-sysadmin}"
DD_HOST="${DD_HOST:-}"

if [[ -z "$DD_HOST" ]]; then
  echo "CRIT: DD_HOST not set" >&2
  exit 2
fi

ddcmd() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$DD_HOST" "ddsh -c \"$1\""
}

STATE=0

flag() {
  local level="$1"; shift
  echo "  [$level] $*"
  case "$level" in
    CRIT) [[ "$STATE" -lt 2 ]] && STATE=2 ;;
    WARN) [[ "$STATE" -lt 1 ]] && STATE=1 ;;
  esac
}

echo "Data Domain Health — $DD_HOST — $(date '+%Y-%m-%d %H:%M:%S')"

# Uptime
UPTIME=$(ddcmd "system show stats" 2>&1 | grep -i "uptime" | head -1)
echo "  [INFO] ${UPTIME:-uptime not parsed}"

# Disk health
DISKS=$(ddcmd "disk show state" 2>&1)
echo "$DISKS" | grep -qi "failed\|absent\|reconstructing\|unknown" \
  && flag CRIT "unhealthy disk(s) detected" \
  || echo "  [OK] all disks healthy"

# Filesystem space
SPACE=$(ddcmd "filesys show space" 2>&1)
HIGH=$(echo "$SPACE" | grep -oE '[0-9]+(\.[0-9]+)?%' | tr -d '%' | awk '$1 >= 85' | wc -l | tr -d ' ')
WARN_HIGH=$(echo "$SPACE" | grep -oE '[0-9]+(\.[0-9]+)?%' | tr -d '%' | awk '$1 >= 80 && $1 < 85' | wc -l | tr -d ' ')
[[ "$HIGH" -gt 0 ]]      && flag CRIT "filesystem >= 85% full"
[[ "$WARN_HIGH" -gt 0 ]] && flag WARN "filesystem >= 80% full"
[[ "$HIGH" -eq 0 && "$WARN_HIGH" -eq 0 ]] && echo "  [OK] filesystem space OK"

# Dedup ratio
COMP=$(ddcmd "filesys show compression" 2>&1)
RATIO=$(echo "$COMP" | grep -i "cumulative compression factor\|total compression" | grep -oE '[0-9]+\.[0-9]+x' | head -1)
echo "  [INFO] dedup/compression ratio: ${RATIO:-not parsed}"

# Replication
REPL=$(ddcmd "replication show all" 2>&1)
echo "$REPL" | grep -qi "error\|disabled\|idle-error\|in-error" \
  && flag CRIT "replication session error" \
  || echo "  [OK] replication active"

LABELS=( OK WARN CRIT )
echo "OVERALL: ${LABELS[$STATE]}"
exit "$STATE"
```
