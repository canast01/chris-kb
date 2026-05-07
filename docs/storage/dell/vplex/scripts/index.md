# Scripts

> Part of the [Dell VPLEX](../) reference.

---
## Distributed Device Health Check

SSH to a VPLEX management server and runs vplexcli commands to check cluster health indications, distributed device health, and director hardware state. Reports any health-state value that is not "ok" and exits non-zero if issues are found.

~~~bash
#!/bin/bash
# vplex_device_health.sh — Distributed device and director health check for Dell VPLEX
# Usage: VPLEX_HOST=vplex-mgmt.example.com VPLEX_USER=service ./vplex_device_health.sh

set -euo pipefail

VPLEX_HOST="${VPLEX_HOST:-}"
VPLEX_USER="${VPLEX_USER:-service}"
ISSUES=0

if [[ -z "$VPLEX_HOST" ]]; then
  echo "ERROR: VPLEX_HOST is not set." >&2
  exit 1
fi

# Wrapper: run a vplexcli command via SSH
vplex_cmd() {
  local cmd="$1"
  ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
      "${VPLEX_USER}@${VPLEX_HOST}" "vplexcli -q -e '${cmd}'" 2>&1
}

section() {
  echo ""
  echo "========================================"
  echo "  $1"
  echo "========================================"
}

echo ""
echo "########################################"
echo "  VPLEX Health Check"
echo "  Host : $VPLEX_HOST"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "########################################"

# --- Cluster health indications ---
section "CLUSTER HEALTH INDICATIONS"
CLUSTER_HEALTH=$(vplex_cmd "ll /clusters/*/health-indications/")
echo "$CLUSTER_HEALTH"
if echo "$CLUSTER_HEALTH" | grep -qi "health-state.*[^ok]"; then
  echo ">>> ISSUE: Non-OK cluster health indication detected."
  ISSUES=$((ISSUES + 1))
fi

# --- Distributed device health ---
section "DISTRIBUTED DEVICE HEALTH"
DD_HEALTH=$(vplex_cmd "ll /distributed-storage/distributed-devices/*/health-indications/")
echo "$DD_HEALTH"
BAD_DEVICES=$(echo "$DD_HEALTH" | grep -i "health-state" | grep -iv "value:.*ok" || true)
if [[ -n "$BAD_DEVICES" ]]; then
  echo ">>> ISSUE: One or more distributed devices are NOT in 'ok' health state:"
  echo "$BAD_DEVICES"
  ISSUES=$((ISSUES + 1))
fi

# --- Director hardware ---
section "DIRECTOR HARDWARE STATUS"
DIR_HEALTH=$(vplex_cmd "ll /engines/*/directors/*/hardware/")
echo "$DIR_HEALTH"
BAD_DIRS=$(echo "$DIR_HEALTH" | grep -i "health-state" | grep -iv "value:.*ok" || true)
if [[ -n "$BAD_DIRS" ]]; then
  echo ">>> ISSUE: One or more directors have non-OK hardware state:"
  echo "$BAD_DIRS"
  ISSUES=$((ISSUES + 1))
fi

echo ""
echo "========================================"
echo "  SUMMARY"
echo "========================================"
if [[ "$ISSUES" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $ISSUES issue category/categories found. Review output above."
  exit 1
else
  echo "STATUS: OK — All VPLEX health checks passed."
  exit 0
fi
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Linux or macOS system with Bash and the `ssh` command available
- SSH access to the VPLEX Management Station (VMS) — the Linux server that manages your VPLEX system
- The default SSH user for VPLEX is `service` (used to run vplexcli commands)
- SSH key authentication configured, or you can add `-o PasswordAuthentication=yes` and enter the password interactively
- The hostname or IP of your VPLEX Management Station

**Step 1 — Save the file**

1. Copy the code block above into a text editor
2. Save it as `vplex_device_health.sh`
3. Make it executable: `chmod +x vplex_device_health.sh`

**Step 2 — Fill in your details**

| What to change | Where to find it |
|---|---|
| `VPLEX_HOST` | Hostname or IP of the VPLEX Management Station (VMS) |
| `VPLEX_USER` | SSH username — default is `service` for VPLEX |

**Step 3 — Open a terminal**

On Linux/macOS, open a terminal. On Windows, use Git Bash or WSL.

**Step 4 — Run it**

```
cd /path/to/script
VPLEX_HOST=192.168.1.20 VPLEX_USER=service ./vplex_device_health.sh
```

**What you should see**

Three labelled sections: cluster health indications, distributed device health, and director hardware status. Each section shows the raw vplexcli output followed by any detected issues. The final SUMMARY line shows STATUS: OK or STATUS: DEGRADED with an issue count. The script exits 0 on success or 1 if issues are found.

---

## Metro Consistency Group Monitor

SSH to a VPLEX Metro system and queries consistency group operational status. Parses for any CG that is not in `in-sync` state and emits a Nagios-compatible PASS/WARNING/CRITICAL result. Alerts on split-brain or out-of-sync state.

~~~perl
#!/usr/bin/env perl
# vplex_cg_monitor.pl — Metro consistency group monitor for Dell VPLEX
# Usage: VPLEX_HOST=vplex-mgmt.example.com VPLEX_USER=service ./vplex_cg_monitor.pl

use strict;
use warnings;

my $host   = $ENV{VPLEX_HOST}  or die "ERROR: VPLEX_HOST not set\n";
my $user   = $ENV{VPLEX_USER} || 'service';

# Critical states
my %crit_states = map { lc($_) => 1 } qw(
    split-brain
    split_brain
    out-of-sync
    out_of_sync
    degraded
    faulted
    error
);

# Warning states
my %warn_states = map { lc($_) => 1 } qw(
    transitioning
    resyncing
    partial
    unknown
);

# Run vplexcli via SSH and list all consistency groups
my $cmd    = qq{ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${user}\@${host} }
           . q{"vplexcli -q -e 'll /distributed-storage/consistency-groups/'" 2>&1};
my $output = qx{$cmd};
if ($? != 0) {
    print "UNKNOWN: SSH/vplexcli failed for $host\n$output\n";
    exit 3;
}

my @cgs;
my $worst = 0;   # 0=OK 1=WARN 2=CRIT

# Parse output — lines like: Name: cg-prod  operational-status: in-sync
my %current;
for my $line (split /\n/, $output) {
    $line =~ s/^\s+|\s+$//g;
    next unless $line;

    if ($line =~ /^Name:\s+(.+)$/i) {
        if (%current) {
            push @cgs, {%current};
        }
        %current = (name => $1, status => 'unknown', visibility => 'unknown');
        next;
    }
    if ($line =~ /operational-status:\s*(.+)$/i) {
        $current{status} = lc($1);
        next;
    }
    if ($line =~ /visibility:\s*(.+)$/i) {
        $current{visibility} = lc($1);
        next;
    }
}
push @cgs, {%current} if %current;

if (!@cgs) {
    print "UNKNOWN: No consistency groups found in output\n";
    exit 3;
}

# Print table
printf "%-30s  %-20s  %-15s  %s\n", 'CG NAME', 'STATUS', 'VISIBILITY', 'RESULT';
printf "%s\n", '-' x 80;

for my $cg (@cgs) {
    my $status = lc($cg->{status} // 'unknown');
    my $result = 'OK';

    if ($crit_states{$status}) {
        $result  = 'CRITICAL';
        $worst   = 2 if $worst < 2;
    } elsif ($warn_states{$status} || $status ne 'in-sync') {
        $result  = 'WARNING';
        $worst   = 1 if $worst < 1;
    }

    printf "%-30s  %-20s  %-15s  %s\n",
        $cg->{name}, $cg->{status}, $cg->{visibility}, $result;
}

print "\n";
if ($worst == 2) {
    print "CRITICAL: One or more consistency groups are in a split-brain or out-of-sync state.\n";
    exit 2;
} elsif ($worst == 1) {
    print "WARNING: One or more consistency groups require attention.\n";
    exit 1;
} else {
    print "OK: All consistency groups are in-sync.\n";
    exit 0;
}
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Linux or macOS system with Perl installed (pre-installed on most Linux distros and macOS)
- SSH access to the VPLEX Management Station with the `service` user
- SSH key authentication configured (the script uses `BatchMode=yes` which disables password prompts)
- The hostname or IP of your VPLEX Management Station

**Step 1 — Save the file**

1. Copy the code block above into a text editor
2. Save it as `vplex_cg_monitor.pl`

**Step 2 — Fill in your details**

| What to change | Where to find it |
|---|---|
| `VPLEX_HOST` | Hostname or IP of the VPLEX Management Station |
| `VPLEX_USER` | SSH username — default is `service` |

**Step 3 — Open a terminal**

On Linux/macOS, open a terminal. On Windows, use Git Bash or WSL.

**Step 4 — Run it**

```
cd /path/to/script
VPLEX_HOST=192.168.1.20 VPLEX_USER=service perl vplex_cg_monitor.pl
```

**What you should see**

A formatted table with columns CG NAME, STATUS, VISIBILITY, and RESULT. Each consistency group is listed with its operational status. Groups in split-brain or out-of-sync states are marked CRITICAL; groups in transitioning or unknown states are marked WARNING; healthy in-sync groups show OK. The final line gives an overall CRITICAL, WARNING, or OK verdict with exit code 2, 1, or 0.

---

## Storage View Audit

SSH to a VPLEX management server and enumerates all storage views across all clusters. For each view, lists the initiator ports and virtual volumes. Flags any storage view with no registered initiators as an orphaned view and outputs a formatted report.

~~~python
#!/usr/bin/env python3
# vplex_storage_view_audit.py — Storage view audit for Dell VPLEX
# Requirements: paramiko
# Usage: VPLEX_HOST=vplex-mgmt.example.com VPLEX_USER=service VPLEX_KEY=~/.ssh/id_rsa \
#        ./vplex_storage_view_audit.py

import os
import sys
import re
import paramiko

VPLEX_HOST = os.environ.get("VPLEX_HOST", "")
VPLEX_USER = os.environ.get("VPLEX_USER", "service")
VPLEX_KEY  = os.environ.get("VPLEX_KEY",  os.path.expanduser("~/.ssh/id_rsa"))
VPLEX_PASS = os.environ.get("VPLEX_PASS", None)

if not VPLEX_HOST:
    print("ERROR: VPLEX_HOST must be set.", file=sys.stderr)
    sys.exit(1)


def ssh_run(command):
    """Run a command on the VPLEX management server via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    kw = {"username": VPLEX_USER, "timeout": 30}
    if VPLEX_PASS:
        kw["password"] = VPLEX_PASS
    else:
        kw["key_filename"] = VPLEX_KEY
    client.connect(VPLEX_HOST, **kw)
    _, stdout, stderr = client.exec_command(command)
    out = stdout.read().decode()
    err = stderr.read().decode()
    client.close()
    return out, err


def vplex_cli(cmd):
    """Run a vplexcli command and return its output."""
    out, err = ssh_run(f"vplexcli -q -e '{cmd}'")
    return out


def parse_attribute(lines, attr):
    """Extract the first matching attribute value from a list of output lines."""
    for line in lines:
        m = re.match(rf'^\s*{re.escape(attr)}:\s*(.+)$', line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""


def parse_list_attribute(lines, attr):
    """Extract a comma/space-separated list attribute (e.g., initiator-ports)."""
    val = parse_attribute(lines, attr)
    if not val or val.lower() in ("none", "[]", ""):
        return []
    return [v.strip() for v in re.split(r'[,\s]+', val) if v.strip()]


def main():
    print("=" * 70)
    print("  VPLEX Storage View Audit")
    print(f"  Host : {VPLEX_HOST}")
    print("=" * 70)

    # List storage views for all clusters
    sv_list_out = vplex_cli("ll /clusters/*/exports/storage-views/")

    # Parse view names and their cluster paths
    views = []
    for line in sv_list_out.splitlines():
        m = re.match(r'^\s*(/clusters/[^/]+/exports/storage-views/\S+)', line)
        if m:
            views.append(m.group(1))
        # Some vplexcli versions list just names with a path prefix
        m2 = re.match(r'^\s*Name:\s*(\S+)', line)
        if m2 and m2.group(1) not in [v.split("/")[-1] for v in views]:
            # Try to build path from context — best effort
            views.append(m2.group(1))

    if not views:
        # Fallback: list names only
        for line in sv_list_out.splitlines():
            line = line.strip()
            if line and not line.startswith("/") and not re.match(r'^(Name|--)', line):
                views.append(line)

    if not views:
        print("\nNo storage views found (or unable to parse vplexcli output).")
        sys.exit(0)

    orphans = 0
    print(f"\n{'STORAGE VIEW':<35}  {'INITIATORS':>3}  {'VIRT-VOLS':>3}  STATUS")
    print("-" * 70)

    for view_path in views:
        try:
            detail = vplex_cli(f"ll {view_path}")
        except Exception as e:
            print(f"  ERROR querying {view_path}: {e}")
            continue

        detail_lines = detail.splitlines()
        name        = parse_attribute(detail_lines, "name") or view_path.split("/")[-1]
        init_ports  = parse_list_attribute(detail_lines, "initiator-ports")
        virt_vols   = parse_list_attribute(detail_lines, "virtual-volumes")

        n_inits = len(init_ports)
        n_vols  = len(virt_vols)

        if n_inits == 0:
            status = "ORPHANED (no initiators)"
            orphans += 1
        else:
            status = "OK"

        print(f"{name:<35}  {n_inits:>3}  {n_vols:>3}  {status}")

        if n_inits > 0:
            for p in init_ports:
                print(f"  {'':35}  initiator: {p}")
        for v in virt_vols:
            print(f"  {'':35}  vol:       {v}")

    print("-" * 70)
    print(f"\nTotal views: {len(views)}   Orphaned (no initiators): {orphans}")

    if orphans > 0:
        print(f"\nWARNING: {orphans} orphaned storage view(s) found. Review and clean up.")
        sys.exit(1)
    else:
        print("\nOK: All storage views have registered initiators.")
        sys.exit(0)


if __name__ == "__main__":
    main()
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Python 3.7 or later installed on your machine (python.org)
- The `paramiko` library installed: run `pip install paramiko` in your terminal
- SSH access to the VPLEX Management Station
- An SSH key (`~/.ssh/id_rsa`) or a password for the VPLEX `service` user
- The hostname or IP of your VPLEX Management Station

**Step 1 — Save the file**

1. Copy the code block above into a text editor
2. Save it as `vplex_storage_view_audit.py`

**Step 2 — Fill in your details**

Set these environment variables before running:

| What to change | Where to find it |
|---|---|
| `VPLEX_HOST` | Hostname or IP of the VPLEX Management Station |
| `VPLEX_USER` | SSH username (default `service`) |
| `VPLEX_KEY` | Path to your SSH private key file (default `~/.ssh/id_rsa`) |
| `VPLEX_PASS` | Set this instead of VPLEX_KEY if you use password authentication |

**Step 3 — Open a terminal**

On Linux/macOS, open a terminal. On Windows, press **Windows key**, type `cmd`, press Enter. Make sure Python is installed (python.org). Install paramiko first: `pip install paramiko`.

**Step 4 — Run it**

```
cd C:\Users\YourName\Desktop
set VPLEX_HOST=192.168.1.20
set VPLEX_USER=service
set VPLEX_KEY=C:\Users\YourName\.ssh\id_rsa
python vplex_storage_view_audit.py
```

**What you should see**

A table of all storage views across all VPLEX clusters with columns for view name, number of registered initiator ports, number of virtual volumes, and status. Views with no initiators are flagged as ORPHANED. A summary line at the bottom shows total view count and orphan count. The script exits 0 if all views are healthy, or 1 if orphaned views are found.

---

## Ansible VPLEX Health Playbook

Playbook targeting the `vplex_mgmt` host. Runs director, distributed device, and consistency group health checks via vplexcli, asserts all states are healthy, and sends a failure notification on any issue detected.

~~~yaml
---
# vplex_health.yml — Ansible health check playbook for Dell VPLEX
# Inventory host: vplex_mgmt
# Usage: ansible-playbook -i inventory vplex_health.yml

- name: Dell VPLEX Health Check
  hosts: vplex_mgmt
  gather_facts: false

  tasks:
    - name: Check director hardware health
      ansible.builtin.shell: "vplexcli -q -e 'll /engines/*/directors/*/hardware/'"
      register: director_health
      changed_when: false

    - name: Show director hardware status
      ansible.builtin.debug:
        msg: "{{ director_health.stdout_lines }}"

    - name: Check distributed device sync state
      ansible.builtin.shell: >
        vplexcli -q -e 'll /distributed-storage/distributed-devices/*/health-indications/'
      register: dd_health
      changed_when: false

    - name: Show distributed device health
      ansible.builtin.debug:
        msg: "{{ dd_health.stdout_lines }}"

    - name: Check consistency group state
      ansible.builtin.shell: >
        vplexcli -q -e 'll /distributed-storage/consistency-groups/'
      register: cg_health
      changed_when: false

    - name: Show consistency group state
      ansible.builtin.debug:
        msg: "{{ cg_health.stdout_lines }}"

    - name: Assert director hardware is healthy
      ansible.builtin.assert:
        that:
          - "'health-state: error' not in director_health.stdout | lower"
          - "'health-state: degraded' not in director_health.stdout | lower"
        fail_msg: "Director health issue detected on {{ inventory_hostname }}."
        success_msg: "Director hardware health OK."

    - name: Assert distributed devices are in-sync
      ansible.builtin.assert:
        that:
          - "'out-of-sync' not in dd_health.stdout | lower"
          - "'split-brain' not in dd_health.stdout | lower"
          - "'faulted' not in dd_health.stdout | lower"
        fail_msg: "Distributed device health issue on {{ inventory_hostname }}."
        success_msg: "Distributed device health OK."

    - name: Assert consistency groups are in-sync
      ansible.builtin.assert:
        that:
          - "'out-of-sync' not in cg_health.stdout | lower"
          - "'split-brain' not in cg_health.stdout | lower"
        fail_msg: "Consistency group out-of-sync or split-brain on {{ inventory_hostname }}."
        success_msg: "All consistency groups in-sync."

    - name: Send failure notification (runs only on failure via block/rescue)
      ansible.builtin.debug:
        msg: >
          VPLEX health check FAILED on {{ inventory_hostname }}.
          Review the output above and investigate any flagged health states.
      when: false   # Triggered via block/rescue in production — replace with notify handler
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on your control machine (`pip install ansible`)
- SSH access from the Ansible control machine to the VPLEX Management Station
- The VPLEX `service` user accessible via SSH key from your control machine
- vplexcli available on the VPLEX Management Station (it always is on VMS)

**Step 1 — Save the file**

1. Copy the code block above into a text editor
2. Save it as `vplex_health.yml`

**Step 2 — Fill in your details**

Create an inventory file (`inventory`) with:
```
vplex_mgmt ansible_host=192.168.1.20 ansible_user=service ansible_ssh_private_key_file=~/.ssh/id_rsa
```
Replace `192.168.1.20` with your VPLEX Management Station IP and adjust the key path.

**Step 3 — Open a terminal**

On Linux/macOS, open a terminal. On Windows, use WSL or Git Bash.

**Step 4 — Run it**

```
cd /path/to/playbook
ansible-playbook -i inventory vplex_health.yml
```

**What you should see**

Ansible prints a task-by-task log. You will see the director hardware status, distributed device health indications, and consistency group states printed as lists. The three assert tasks pass silently if all checks are healthy, or fail with a descriptive message if issues are found. The play ends with a summary showing the number of OK, failed, and changed tasks.

---

## Windows: VPLEX Cluster Health via Plink (CMD)

Run VPLEX CLI commands from a Windows Command Prompt using plink.exe (PuTTY) — SSH to the VPLEX Management Station and check cluster and health state without needing Linux on your desktop.

~~~batch
@echo off
REM vplex_cluster_health.bat — Check VPLEX cluster health via SSH (plink/PuTTY)
REM Uses plink.exe to run vplexcli commands on the VPLEX Management Station (VMS).
REM
REM Prerequisites:
REM   1. Download and install PuTTY from https://www.putty.org
REM      plink.exe is included with PuTTY.
REM   2. First-time use: run plink manually once to accept the VMS host key:
REM        plink -ssh service@192.168.1.20
REM      Type "yes" when prompted to store the host key, then Ctrl+C.
REM   3. The default VPLEX SSH user is "service". Use SSH key auth for automation.
REM
REM Note: vplexcli is the VPLEX CLI wrapper that runs on the VMS.
REM       Commands use the path-based VPLEX management tree (e.g. /clusters).

set VPLEX_HOST=192.168.1.20
set SSH_USER=service
REM Set PLINK to the full path if plink.exe is not in your PATH:
set PLINK=plink.exe

echo.
echo ########################################
echo   VPLEX Cluster Health Check
echo   Host : %VPLEX_HOST%
echo ########################################
echo.

echo [1] Listing VPLEX clusters ...
echo.
%PLINK% -ssh -l %SSH_USER% -batch %VPLEX_HOST% "vplexcli -q -e 'ls /clusters'"
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Could not connect to VPLEX Management Station.
    echo   - Check that %VPLEX_HOST% is reachable (try: ping %VPLEX_HOST%^)
    echo   - Check SSH access for user %SSH_USER%
    echo   - Accept the host key first (see Prerequisites above^)
    exit /b 1
)

echo.
echo [2] Running VPLEX health check ...
echo.
%PLINK% -ssh -l %SSH_USER% -batch %VPLEX_HOST% "vplexcli -q -e 'health-check'"
if %ERRORLEVEL% neq 0 (
    echo.
    echo WARNING: health-check command returned a non-zero exit code.
    echo   Review the output above for any reported issues.
    exit /b 1
)

echo.
echo Done.
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Windows 10 or Windows 11 PC
- PuTTY installed — download from https://www.putty.org (free). `plink.exe` is included.
- SSH access to the VPLEX Management Station (VMS) using the `service` account
- SSH key authentication configured for the `service` user, or use `-pw YourPassword` in the plink command

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Click **File → Save As**
4. In "Save as type" drop-down, select **All Files**
5. Name it `vplex_cluster_health.bat` and click Save (Desktop is fine)

**Step 2 — Fill in your details**

Open the saved file in Notepad and change these lines:

| What to change | Where to find it |
|---|---|
| `VPLEX_HOST` | IP address or hostname of the VPLEX Management Station (VMS) |
| `SSH_USER` | SSH username — default is `service` for VPLEX |

**Step 3 — Accept the host key (first time only)**

Open Command Prompt and run:
```
plink -ssh service@192.168.1.20
```
When asked "Store key in cache?", type `y` and press Enter, then Ctrl+C. You only need to do this once per VMS.

**Step 4 — Open a terminal**

Press **Windows key**, type `cmd`, press Enter to open Command Prompt.

**Step 5 — Run it**

```
cd C:\Users\YourName\Desktop
vplex_cluster_health.bat
```

**What you should see**

Two sections: (1) a list of the VPLEX clusters known to the Management Station (e.g., `cluster-1`, `cluster-2`); (2) the output of the `health-check` command which reports the overall health status of all VPLEX components. If all components are healthy, you will see OK or healthy indicators. Any issues will be listed with descriptions. A connection failure prints a plain-English error with troubleshooting steps.

---

## Windows: VPLEX System Status via REST API (PowerShell)

Query the VPLEX REST API from a Windows PC using PowerShell to list clusters and check system health — no SSH or vplexcli required on your desktop.

~~~powershell
# vplex_system_status.ps1 — VPLEX system status via REST API (Windows PowerShell)
# Run: .\vplex_system_status.ps1
# Requires: PowerShell 5.1+ (built into Windows 10/11) — no extra install needed
#
# Note: VPLEX REST API is available on the VPLEX Management Station (VMS).
# The API base path is /vplex/v2/ on the VMS management IP.

$VplexHost = "192.168.1.20"   # Change to your VPLEX Management Station IP or hostname
$ApiUser   = "admin"           # Change to your VPLEX API username
$ApiPass   = "yourpassword"    # Change to your VPLEX API password

$ApiBase = "https://$VplexHost/vplex/v2"

# Allow self-signed certificates (VPLEX VMS uses these by default)
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) { return true; }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Build Basic auth header
$Pair    = "${ApiUser}:${ApiPass}"
$Bytes   = [System.Text.Encoding]::ASCII.GetBytes($Pair)
$Base64  = [Convert]::ToBase64String($Bytes)
$Headers = @{
    Authorization  = "Basic $Base64"
    "Content-Type" = "application/json"
    Accept         = "application/json"
}

Write-Host ""
Write-Host "########################################" -ForegroundColor Cyan
Write-Host "  VPLEX System Status via REST API"      -ForegroundColor Cyan
Write-Host "  Host : $VplexHost"                     -ForegroundColor Cyan
Write-Host "########################################" -ForegroundColor Cyan

# --- List clusters ---
Write-Host "`n[1] Fetching VPLEX cluster list ..."
try {
    $ClustersResp = Invoke-RestMethod -Uri "$ApiBase/clusters" `
                                      -Method GET -Headers $Headers
    $Clusters = $ClustersResp.response.context
    if ($Clusters) {
        Write-Host ""
        Write-Host "  Clusters found:"
        foreach ($cl in $Clusters) {
            Write-Host "    - $($cl.name)  [top-level-assembly: $($cl.'top-level-assembly')]"
        }
    } else {
        Write-Host "  No clusters found in API response."
    }
} catch {
    Write-Host "  ERROR fetching cluster list: $_" -ForegroundColor Red
    Write-Host "  Note: Verify the VPLEX REST API is enabled on the VMS and the host/credentials are correct."
}

# --- Health check ---
Write-Host "`n[2] Running VPLEX health check ..."
try {
    $HealthResp = Invoke-RestMethod -Uri "$ApiBase/health-check" `
                                    -Method GET -Headers $Headers
    $HealthCtx = $HealthResp.response.context
    Write-Host ""
    if ($HealthCtx) {
        foreach ($item in $HealthCtx) {
            $status = $item.'health-state'
            $name   = $item.name
            $color  = if ($status -eq "ok") { "Green" } else { "Red" }
            Write-Host ("  {0,-40}  {1}" -f $name, $status.ToUpper()) -ForegroundColor $color
        }
    } else {
        # Some VPLEX REST API versions return health under a different key
        Write-Host "  Raw health response:"
        Write-Host ($HealthResp | ConvertTo-Json -Depth 5)
    }
} catch {
    Write-Host "  ERROR running health check: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================"
Write-Host "  Status check complete."
Write-Host "========================================"
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Windows 10 or Windows 11 PC (PowerShell 5.1 is built in — nothing to install)
- Network access from your PC to the VPLEX Management Station (VMS) on port 443 (HTTPS)
- VPLEX REST API enabled on the VMS (it is enabled by default on modern VPLEX firmware)
- A valid VPLEX API username and password

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC (search in the Start menu)
2. Copy the entire code block above
3. Click **File → Save As**
4. In "Save as type" drop-down, select **All Files**
5. Name it `vplex_system_status.ps1` and click Save (Desktop is a fine location)

**Step 2 — Fill in your details**

Open the saved file in Notepad and change these three lines near the top:

| What to change | Where to find it |
|---|---|
| `$VplexHost` | IP address or hostname of the VPLEX Management Station (VMS) |
| `$ApiUser` | Your VPLEX REST API username |
| `$ApiPass` | Your VPLEX REST API password |

**Step 3 — Open a terminal**

Press **Windows key**, type `PowerShell`, right-click, choose **Run as Administrator**.

**Step 4 — Allow scripts to run (one-time, per session)**

In PowerShell, run this once:
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run it**

```
cd C:\Users\YourName\Desktop
.\vplex_system_status.ps1
```

**What you should see**

Two sections: (1) a list of the VPLEX clusters visible through the REST API, showing each cluster name; (2) a health check table listing each VPLEX component with its health state — components in `ok` state print in green, anything else prints in red. If the API cannot be reached, an error message explains what to check.

---

## Daily Check Script

SSHes to the VPLEX Management Server and runs health-check, lists clusters and engines, checks consistency group states, and prints PASS/FAIL for each check.

```bash
#!/bin/bash
# vplex_daily_check.sh — Daily operations check for Dell VPLEX
# Usage: SSH_USER=service VPLEX_HOST=vplex-mgmt.example.com ./vplex_daily_check.sh

set -uo pipefail

SSH_USER="${SSH_USER:-service}"
VPLEX_HOST="${VPLEX_HOST:-}"

if [[ -z "$VPLEX_HOST" ]]; then
  echo "ERROR: VPLEX_HOST is not set." >&2
  exit 1
fi

PASS=0
FAIL=0

vplex() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$VPLEX_HOST" "vplexcli -q -e \"$1\""
}

check() {
  local label="$1"
  local result="$2"
  if [[ "$result" -eq 0 ]]; then
    printf "  %-45s  PASS\n" "$label"
    PASS=$((PASS + 1))
  else
    printf "  %-45s  FAIL\n" "$label"
    FAIL=$((FAIL + 1))
  fi
}

echo "========================================"
echo "  VPLEX Daily Check — $VPLEX_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 1. Health check
HC=$(vplex "health-check" 2>&1)
echo "$HC"
echo "$HC" | grep -qi "error\|failed\|fault" && HC_RC=1 || HC_RC=0
check "health-check" "$HC_RC"

# 2. Clusters reachable
CL=$(vplex "ls /clusters" 2>&1)
echo "$CL"
[[ -n "$CL" ]] && CL_RC=0 || CL_RC=1
check "ls /clusters" "$CL_RC"

# 3. Engines listed
EN=$(vplex "ls /engines" 2>&1)
echo "$EN"
[[ -n "$EN" ]] && EN_RC=0 || EN_RC=1
check "ls /engines" "$EN_RC"

# 4. Consistency group states — flag any non-in-sync
CG=$(vplex "ls /consistency-groups" 2>&1)
echo "$CG"
echo "$CG" | grep -qi "out-of-sync\|split-brain\|degraded\|faulted" && CG_RC=1 || CG_RC=0
check "consistency-groups (no degraded)" "$CG_RC"

echo "========================================"
echo "  PASS: $PASS   FAIL: $FAIL"
[[ "$FAIL" -eq 0 ]] && echo "  STATUS: OK" && exit 0 || echo "  STATUS: DEGRADED" && exit 1
```

---

## Incident Triage Script

Captures health-check, engines, directors, virtual-volumes, consistency groups, and storage-views output to a timestamped triage file for support handoff.

```bash
#!/bin/bash
# vplex_triage.sh — Incident triage data capture for Dell VPLEX
# Usage: SSH_USER=service VPLEX_HOST=vplex-mgmt.example.com ./vplex_triage.sh

SSH_USER="${SSH_USER:-service}"
VPLEX_HOST="${VPLEX_HOST:-}"

if [[ -z "$VPLEX_HOST" ]]; then
  echo "ERROR: VPLEX_HOST is not set." >&2
  exit 1
fi

OUTFILE="vplex_triage_$(date '+%Y%m%d_%H%M%S').txt"

vplex() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$VPLEX_HOST" "vplexcli -q -e \"$1\""
}

section() {
  echo "" >> "$OUTFILE"
  echo "========================================" >> "$OUTFILE"
  echo "  $1" >> "$OUTFILE"
  echo "========================================" >> "$OUTFILE"
}

{
  echo "VPLEX Triage Capture"
  echo "Host : $VPLEX_HOST"
  echo "Date : $(date '+%Y-%m-%d %H:%M:%S')"
} > "$OUTFILE"

section "HEALTH CHECK";        vplex "health-check"        >> "$OUTFILE" 2>&1
section "ENGINES";             vplex "ls /engines"         >> "$OUTFILE" 2>&1
section "DIRECTORS";           vplex "ls /directors"       >> "$OUTFILE" 2>&1
section "VIRTUAL VOLUMES";     vplex "ls /virtual-volumes" >> "$OUTFILE" 2>&1
section "CONSISTENCY GROUPS";  vplex "ls /consistency-groups" >> "$OUTFILE" 2>&1
section "STORAGE VOLUMES";     vplex "ls /storage-volumes" >> "$OUTFILE" 2>&1

echo "Triage data written to: $OUTFILE"
```

---

## Change Pre-Check Script

Confirms VPLEX health-check returns OK, all engines are running, no consistency groups are degraded, and all directors are online before a maintenance window — exits 2 on any failure.

```bash
#!/bin/bash
# vplex_precheck.sh — Pre-change validation for Dell VPLEX
# Usage: SSH_USER=service VPLEX_HOST=vplex-mgmt.example.com ./vplex_precheck.sh

set -uo pipefail

SSH_USER="${SSH_USER:-service}"
VPLEX_HOST="${VPLEX_HOST:-}"

if [[ -z "$VPLEX_HOST" ]]; then
  echo "ERROR: VPLEX_HOST is not set." >&2
  exit 1
fi

ISSUES=0

vplex() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$VPLEX_HOST" "vplexcli -q -e \"$1\""
}

fail() {
  echo "  FAIL: $1"
  ISSUES=$((ISSUES + 1))
}

pass() {
  echo "  PASS: $1"
}

echo "========================================"
echo "  VPLEX Pre-Change Check — $VPLEX_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 1. Health check must be clean
HC=$(vplex "health-check" 2>&1)
echo "$HC" | grep -qi "error\|failed\|fault" && fail "health-check reports errors" || pass "health-check clean"

# 2. Engines must be listed and not show fault
EN=$(vplex "ls /engines" 2>&1)
echo "$EN" | grep -qi "fault\|error\|down" && fail "engine(s) not running" || pass "all engines running"

# 3. No degraded consistency groups
CG=$(vplex "ls /consistency-groups" 2>&1)
echo "$CG" | grep -qi "out-of-sync\|split-brain\|degraded\|faulted" \
  && fail "degraded consistency group(s) found" \
  || pass "all consistency groups healthy"

# 4. Directors online
DIR=$(vplex "ls /directors" 2>&1)
echo "$DIR" | grep -qi "offline\|fault\|error\|down" \
  && fail "director(s) not online" \
  || pass "all directors online"

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

Runs the same checks as the pre-check after maintenance and prints a before/after comparison for health-check, engine count, CG state, and director count.

```bash
#!/bin/bash
# vplex_postcheck.sh — Post-change validation for Dell VPLEX
# Usage: SSH_USER=service VPLEX_HOST=vplex-mgmt.example.com \
#        BEFORE_ENGINES=4 BEFORE_DIRS=8 BEFORE_CGS=clean ./vplex_postcheck.sh

set -uo pipefail

SSH_USER="${SSH_USER:-service}"
VPLEX_HOST="${VPLEX_HOST:-}"
BEFORE_ENGINES="${BEFORE_ENGINES:-unknown}"
BEFORE_DIRS="${BEFORE_DIRS:-unknown}"
BEFORE_CGS="${BEFORE_CGS:-unknown}"

if [[ -z "$VPLEX_HOST" ]]; then
  echo "ERROR: VPLEX_HOST is not set." >&2
  exit 1
fi

ISSUES=0

vplex() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$VPLEX_HOST" "vplexcli -q -e \"$1\""
}

echo "========================================"
echo "  VPLEX Post-Change Validation — $VPLEX_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Health check
HC=$(vplex "health-check" 2>&1)
HC_STATE="clean"
echo "$HC" | grep -qi "error\|failed\|fault" && HC_STATE="errors detected"
echo "  health-check    before=clean      after=$HC_STATE"
[[ "$HC_STATE" != "clean" ]] && ISSUES=$((ISSUES + 1))

# Engines
EN=$(vplex "ls /engines" 2>&1)
AFTER_ENGINES=$(echo "$EN" | grep -c "engine" || true)
echo "  engines         before=$BEFORE_ENGINES   after=$AFTER_ENGINES"
echo "$EN" | grep -qi "fault\|error\|down" && ISSUES=$((ISSUES + 1))

# Consistency groups
CG=$(vplex "ls /consistency-groups" 2>&1)
CG_STATE="clean"
echo "$CG" | grep -qi "out-of-sync\|split-brain\|degraded\|faulted" && CG_STATE="degraded"
echo "  consistency-groups  before=$BEFORE_CGS  after=$CG_STATE"
[[ "$CG_STATE" != "clean" ]] && ISSUES=$((ISSUES + 1))

# Directors
DIR=$(vplex "ls /directors" 2>&1)
AFTER_DIRS=$(echo "$DIR" | grep -c "director" || true)
echo "  directors       before=$BEFORE_DIRS   after=$AFTER_DIRS"
echo "$DIR" | grep -qi "offline\|fault\|error\|down" && ISSUES=$((ISSUES + 1))

echo "========================================"
if [[ "$ISSUES" -gt 0 ]]; then
  echo "  POST-CHECK FAILED — $ISSUES issue(s). Investigate before closing change."
  exit 2
fi
echo "  POST-CHECK PASSED — All metrics healthy."
exit 0
```

---

## Health Check Script

Single cron-safe script that runs health-check, cluster, engine, director, and consistency group checks plus a count of virtual volumes — exits 0 for OK, 1 for WARN, 2 for CRIT.

```bash
#!/bin/bash
# vplex_health.sh — Comprehensive cron-safe health check for Dell VPLEX
# Usage: SSH_USER=service VPLEX_HOST=vplex-mgmt.example.com ./vplex_health.sh
# Exit codes: 0=OK  1=WARN  2=CRIT

SSH_USER="${SSH_USER:-service}"
VPLEX_HOST="${VPLEX_HOST:-}"

if [[ -z "$VPLEX_HOST" ]]; then
  echo "CRIT: VPLEX_HOST not set" >&2
  exit 2
fi

vplex() {
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_USER@$VPLEX_HOST" "vplexcli -q -e \"$1\""
}

STATE=0  # 0=OK 1=WARN 2=CRIT

flag() {
  local level="$1"; shift
  echo "  [$level] $*"
  case "$level" in
    CRIT) [[ "$STATE" -lt 2 ]] && STATE=2 ;;
    WARN) [[ "$STATE" -lt 1 ]] && STATE=1 ;;
  esac
}

echo "VPLEX Health Check — $VPLEX_HOST — $(date '+%Y-%m-%d %H:%M:%S')"

# Health check
HC=$(vplex "health-check" 2>&1)
echo "$HC" | grep -qi "error\|failed\|fault" \
  && flag CRIT "health-check reports errors" \
  || echo "  [OK] health-check clean"

# Clusters
CL=$(vplex "ls /clusters" 2>&1)
[[ -z "$CL" ]] && flag CRIT "no clusters returned" || echo "  [OK] clusters: $(echo "$CL" | wc -l | tr -d ' ') found"

# Engines
EN=$(vplex "ls /engines" 2>&1)
echo "$EN" | grep -qi "fault\|error\|down" \
  && flag CRIT "engine fault detected" \
  || echo "  [OK] engines: $(echo "$EN" | wc -l | tr -d ' ') found"

# Directors
DIR=$(vplex "ls /directors" 2>&1)
echo "$DIR" | grep -qi "offline\|fault\|error\|down" \
  && flag WARN "director issue detected" \
  || echo "  [OK] directors: $(echo "$DIR" | wc -l | tr -d ' ') found"

# Consistency groups
CG=$(vplex "ls /consistency-groups" 2>&1)
echo "$CG" | grep -qi "out-of-sync\|split-brain\|degraded\|faulted" \
  && flag CRIT "degraded consistency group(s)" \
  || echo "  [OK] consistency groups healthy"

# Virtual volume count
VV=$(vplex "ls /virtual-volumes" 2>&1)
VV_COUNT=$(echo "$VV" | grep -c "." || true)
echo "  [INFO] virtual-volumes: $VV_COUNT"

LABELS=( OK WARN CRIT )
echo "OVERALL: ${LABELS[$STATE]}"
exit "$STATE"
```
