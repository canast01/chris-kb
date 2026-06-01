# PowerPath — Scripts


<div class="kb-summary">
Scripts reference covering Path Health Check, Path Count Validator, Policy Audit, Windows: PowerPath Device Status via Plink (CMD), Windows: PowerPath Check on Local Windows Host (CMD) and 5 more sections.
</div>
```text
┌─────────────────────────────── Dell PowerPath — Scripts and Automation ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerPath scripts: automation for reporting, health monitoring, and provisioning       │   │
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
│   │            Driver           │  │        powermt daemon       │  │           OS-level          │   │
│   │            Paths            │  │        Active-active        │  │         ≥4 paths/LUN        │   │
│   │            Policy           │  │        Adaptive/ALUA        │  │        Array-specific       │   │
│   │           Failover          │  │         Auto reroute        │  │          <5 sec RTO         │   │
│   │          Management         │  │           pp_mgmt           │  │         Centralised         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Command      │      Notes       │    Frequency     │   │
│   │ powermt display  │ Show path state  │  powermt display  │   Active/dead    │   Daily check    │   │
│   │  powermt check   │  Refresh paths   │   powermt check   │  After changes   │   Post-zoning    │   │
│   │  powermt config  │  Apply license   │  powermt config l │     Per host     │   Install time   │   │
│   │     pp_mgmt      │ Central monitor  │       Web UI      │     Optional     │    Multi-host    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Host OS (Windows/Linux) · HBA or iSCSI NIC ports · FC/IP switches · Dell arrays          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerPath          = Dell multipath driver; manages multiple I/O paths to storage for HA/perform...│
│    powermt            = CLI utility; powermt display, powermt check, powermt save are core commands   │
│    Pseudo device      = virtual block device created by PowerPath aggregating physical I/O paths      │
│    Path health        = alive or dead status per path; dead paths trigger automatic I/O failover      │
│    Adaptive policy    = load-balancing that distributes I/O across all active paths evenly            │
│    CLARiiON policy    = active/passive policy for older VNX/CLARiiON arrays (one active path)         │
│    ALUA               = Asymmetric Logical Unit Access; array signals preferred vs. non-preferred p...│
│    Trespass           = LUN ownership movement between SP-A and SP-B on Unity or VNX arrays           │
│    Ghost path         = stale path entry in PowerPath no longer backed by a physical device           │
│    powermt check      = validates all paths and refreshes device table; run after fabric changes      │
│    pp_mgmt            = PowerPath Management Appliance; central monitoring for all PowerPath hosts    │
│    License key        = host-based license required per server; applied via powermt config license    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Path Health Check

Runs `powermt display dev=all`, counts total devices, dead paths, and devices with fewer paths than the expected minimum. Prints a summary table of each device with its path counts. Exits non-zero if any dead paths are found. Suitable for cron or a monitoring agent.

~~~bash
#!/bin/bash
# powerpath_health_check.sh — PowerPath path health check
# Usage: EXPECTED_PATHS=4 ./powerpath_health_check.sh

set -euo pipefail

EXPECTED_PATHS="${EXPECTED_PATHS:-4}"
TOTAL_DEVICES=0
DEAD_PATH_DEVICES=0
LOW_PATH_DEVICES=0
OVERALL_DEAD=0

# Capture powermt output
POWERMT_OUT=$(powermt display dev=all 2>&1)
if [[ $? -ne 0 ]]; then
  echo "ERROR: powermt display dev=all failed." >&2
  exit 1
fi

echo ""
echo "========================================"
echo "  PowerPath Path Health Check"
echo "  Expected paths per device : $EXPECTED_PATHS"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""
printf "%-20s  %12s  %10s  %10s  %s\n" \
  "PSEUDO-DEV" "TOTAL-PATHS" "DEAD-PATHS" "ALIVE" "STATUS"
printf "%s\n" "------------------------------------------------------------------------"

# Parse powermt output:
# Pseudo name=emcpowera  dev=sdb,sdc  ... 4 paths, 0 dead
# We detect lines like: Pseudo name=<dev> and "X paths, Y dead"
current_dev=""
while IFS= read -r line; do
  # Match device header line
  if [[ "$line" =~ ^Pseudo\ name=([a-zA-Z0-9_/-]+) ]]; then
    current_dev="${BASH_REMATCH[1]}"
    TOTAL_DEVICES=$((TOTAL_DEVICES + 1))
    continue
  fi

  # Match path count summary line, e.g. "     4 paths, 0 dead"
  if [[ -n "$current_dev" && "$line" =~ ([0-9]+)\ paths,\ ([0-9]+)\ dead ]]; then
    total="${BASH_REMATCH[1]}"
    dead="${BASH_REMATCH[2]}"
    alive=$((total - dead))
    OVERALL_DEAD=$((OVERALL_DEAD + dead))

    status="OK"
    if [[ "$dead" -gt 0 ]]; then
      status="DEAD PATHS"
      DEAD_PATH_DEVICES=$((DEAD_PATH_DEVICES + 1))
    elif [[ "$total" -lt "$EXPECTED_PATHS" ]]; then
      status="LOW PATHS"
      LOW_PATH_DEVICES=$((LOW_PATH_DEVICES + 1))
    fi

    printf "%-20s  %12s  %10s  %10s  %s\n" \
      "$current_dev" "$total" "$dead" "$alive" "$status"
    current_dev=""
  fi
done <<< "$POWERMT_OUT"

echo ""
echo "========================================"
echo "  SUMMARY"
echo "  Total devices    : $TOTAL_DEVICES"
echo "  Devices w/ dead  : $DEAD_PATH_DEVICES"
echo "  Devices low path : $LOW_PATH_DEVICES"
echo "  Total dead paths : $OVERALL_DEAD"
echo "========================================"

if [[ "$OVERALL_DEAD" -gt 0 ]]; then
  echo "STATUS: DEGRADED — Dead paths found. Run 'powermt restore' after fixing the underlying issue."
  exit 1
elif [[ "$LOW_PATH_DEVICES" -gt 0 ]]; then
  echo "STATUS: WARNING — Some devices have fewer than $EXPECTED_PATHS paths."
  exit 1
else
  echo "STATUS: OK — All paths healthy."
  exit 0
fi
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux server with PowerPath installed and licensed
- The `powermt` command must be available — run `which powermt` to confirm
- Run the script as root or with sudo (PowerPath requires elevated privileges)

**Step 1 — Save the file**

1. Copy the entire code block above
2. Save it as `powerpath_health_check.sh` on the server where PowerPath is installed

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `EXPECTED_PATHS` | Number of paths you expect per device | Depends on your SAN design — ask your storage admin (typically 4 or 8) |

**Step 3 — Open a terminal**

Open a terminal on the Linux server with PowerPath installed.

**Step 4 — Run the script**

```bash
chmod +x powerpath_health_check.sh
sudo EXPECTED_PATHS=4 ./powerpath_health_check.sh
```

**What you should see**

A table with one row per PowerPath pseudo device showing total paths, dead paths, alive paths, and status. The summary shows total devices, how many have dead paths, and how many have fewer paths than expected. If all paths are healthy the final status is `STATUS: OK — All paths healthy.`

---

## Path Count Validator

Parses `powermt display dev=all` output and validates that every pseudo device has exactly the expected number of paths. Prints PASS/FAIL per device and a final summary. Exits 0 if all pass, 1 if any fail.

~~~perl
#!/usr/bin/env perl
# powerpath_path_validator.pl — Validate path counts for all PowerPath pseudo devices
# Usage: EXPECTED_PATHS=4 ./powerpath_path_validator.pl

use strict;
use warnings;

my $expected = $ENV{EXPECTED_PATHS} // 4;

# Run powermt display dev=all
my @output = qx{powermt display dev=all 2>&1};
if ($? != 0) {
    die "ERROR: powermt display dev=all failed.\n@output\n";
}

my ($current_dev, %results);

for my $line (@output) {
    chomp $line;

    # Match pseudo device header: "Pseudo name=emcpowera"
    if ($line =~ /^Pseudo\s+name=(\S+)/) {
        $current_dev = $1;
        next;
    }

    # Match path count line: "     4 paths, 0 dead"
    if (defined $current_dev && $line =~ /(\d+)\s+paths?,\s*(\d+)\s+dead/) {
        my ($total, $dead) = ($1, $2);
        $results{$current_dev} = {
            total    => $total,
            dead     => $dead,
            alive    => $total - $dead,
        };
        $current_dev = undef;
    }
}

if (!%results) {
    print "ERROR: No pseudo devices parsed from powermt output.\n";
    exit 1;
}

my ($pass, $fail) = (0, 0);
printf "%-20s  %12s  %10s  %10s  %s\n",
    'DEVICE', 'TOTAL PATHS', 'DEAD', 'ALIVE', 'RESULT';
printf "%s\n", '-' x 68;

for my $dev (sort keys %results) {
    my $r = $results{$dev};
    my $result;
    if ($r->{dead} > 0) {
        $result = "FAIL (dead paths)";
        $fail++;
    } elsif ($r->{total} != $expected) {
        $result = sprintf "FAIL (got %d, want %d)", $r->{total}, $expected;
        $fail++;
    } else {
        $result = "PASS";
        $pass++;
    }
    printf "%-20s  %12d  %10d  %10d  %s\n",
        $dev, $r->{total}, $r->{dead}, $r->{alive}, $result;
}

printf "%s\n", '-' x 68;
printf "Total: %d devices — %d PASS, %d FAIL\n", $pass + $fail, $pass, $fail;

exit($fail > 0 ? 1 : 0);
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux server with PowerPath installed
- Perl must be available — run `perl --version` to check (it is installed by default on most Linux systems)
- Run as root or with sudo

**Step 1 — Save the file**

1. Copy the entire code block above
2. Save it as `powerpath_path_validator.pl` on the server

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `EXPECTED_PATHS` | Number of paths per device you expect | Ask your storage admin — commonly 4 or 8 |

**Step 3 — Open a terminal**

Open a terminal on the Linux server with PowerPath installed.

**Step 4 — Run the script**

```bash
chmod +x powerpath_path_validator.pl
sudo EXPECTED_PATHS=4 perl powerpath_path_validator.pl
```

**What you should see**

A table listing each pseudo device with total paths, dead paths, alive paths, and PASS or FAIL. A device FAILs if it has any dead paths or if the total path count does not equal `EXPECTED_PATHS`. The final line shows total devices, passes, and failures.

---

## Policy Audit

Runs `powermt display options` and `powermt display dev=all`, checks that all pseudo devices are using the CLAROpt (`co`) load balancing policy, and reports any exceptions. If the `--fix` flag is passed, automatically applies CLAROpt to all devices and persists the change with `powermt save`.

~~~bash
#!/bin/bash
# powerpath_policy_audit.sh — Audit and optionally fix PowerPath load balancing policy
# Usage: ./powerpath_policy_audit.sh [--fix]
#
# Without --fix: report devices NOT using CLAROpt and exit non-zero if any found.
# With    --fix: apply CLAROpt to all devices and run powermt save.

set -euo pipefail

FIX_MODE=0
if [[ "${1:-}" == "--fix" ]]; then
  FIX_MODE=1
fi

EXPECTED_POLICY="co"   # CLAROpt abbreviation used in powermt output
WRONG_POLICY_DEVICES=0

echo ""
echo "========================================"
echo "  PowerPath Policy Audit"
echo "  Expected policy : CLAROpt (co)"
echo "  Fix mode        : $([ "$FIX_MODE" -eq 1 ] && echo YES || echo NO)"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Show current global options
echo ""
echo "--- Current Global Options ---"
powermt display options
echo ""

# Parse powermt display dev=all for policy per device
POWERMT_OUT=$(powermt display dev=all 2>&1)
current_dev=""
current_policy=""

echo "--- Policy per Device ---"
printf "%-20s  %-15s  %s\n" "DEVICE" "POLICY" "STATUS"
printf "%s\n" "-------------------------------------------"

while IFS= read -r line; do
  if [[ "$line" =~ ^Pseudo\ name=([a-zA-Z0-9_/-]+) ]]; then
    current_dev="${BASH_REMATCH[1]}"
    current_policy=""
    continue
  fi

  # Policy line looks like: "Logical device ID=xxx  Policy=CLAROpt(co)  ..."
  if [[ -n "$current_dev" && "$line" =~ Policy=([A-Za-z]+)\(([a-z]+)\) ]]; then
    policy_name="${BASH_REMATCH[1]}"
    policy_code="${BASH_REMATCH[2]}"

    if [[ "$policy_code" == "$EXPECTED_POLICY" ]]; then
      printf "%-20s  %-15s  PASS\n" "$current_dev" "$policy_name"
    else
      printf "%-20s  %-15s  FAIL — not CLAROpt\n" "$current_dev" "$policy_name"
      WRONG_POLICY_DEVICES=$((WRONG_POLICY_DEVICES + 1))
    fi
    current_dev=""
  fi
done <<< "$POWERMT_OUT"

echo ""
echo "  Devices with non-CLAROpt policy: $WRONG_POLICY_DEVICES"
echo ""

if [[ "$FIX_MODE" -eq 1 && "$WRONG_POLICY_DEVICES" -gt 0 ]]; then
  echo "--- Applying CLAROpt to all devices ---"
  powermt set policy=CLAROpt class=all
  powermt save
  echo "  CLAROpt applied and configuration saved."
  exit 0
fi

if [[ "$WRONG_POLICY_DEVICES" -gt 0 ]]; then
  echo "STATUS: FAIL — $WRONG_POLICY_DEVICES device(s) not using CLAROpt."
  echo "  Run with --fix to correct automatically."
  exit 1
else
  echo "STATUS: PASS — All devices using CLAROpt policy."
  exit 0
fi
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux server with PowerPath installed and licensed
- Run as root or with sudo
- Know what load balancing policy your environment should use (CLAROpt is the Dell recommended default)

**Step 1 — Save the file**

1. Copy the entire code block above
2. Save it as `powerpath_policy_audit.sh` on the server

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `EXPECTED_POLICY` | The load balancing policy code to expect | `co` for CLAROpt (Dell recommended default) |

**Step 3 — Open a terminal**

Open a terminal on the Linux server with PowerPath installed.

**Step 4 — Run the script**

To check only (no changes made):
```bash
chmod +x powerpath_policy_audit.sh
sudo ./powerpath_policy_audit.sh
```

To check and automatically fix any non-CLAROpt devices:
```bash
sudo ./powerpath_policy_audit.sh --fix
```

**What you should see**

The current global PowerPath options, then a per-device table showing the policy in use and PASS or FAIL. The summary shows how many devices are not using CLAROpt. With `--fix`, CLAROpt is applied to all devices and `powermt save` is run to make it permanent.

---

## Windows: PowerPath Device Status via Plink (CMD)

Uses plink.exe to SSH into a Linux host that has PowerPath installed and runs path health checks remotely from a Windows CMD window.

~~~batch
@echo off
REM powerpath_remote_check.bat — PowerPath device check on a remote Linux host via plink
REM Uses plink.exe (PuTTY) to SSH into the Linux server running PowerPath.
REM Download PuTTY (includes plink.exe) from: https://www.putty.org
REM
REM NOTE: PowerPath must be installed on the REMOTE Linux server you are connecting to.
REM This .bat runs on your Windows PC but checks a Linux SAN host.
REM
REM FIRST TIME SETUP: Run this once to accept the host key:
REM   plink -ssh admin@192.168.1.100
REM   Type 'y' when asked, then Ctrl+C.

set HOST_IP=192.168.1.100
set SSH_USER=root
set PLINK=plink.exe

echo ========================================
echo   PowerPath Remote Check
echo   Host: %HOST_IP%
echo ========================================
echo.

echo --- PowerPath Device Status ---
%PLINK% -ssh -l %SSH_USER% -batch %HOST_IP% "powermt display dev=all"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not connect to %HOST_IP%. Check hostname and credentials.
    exit /b 1
)

echo.
echo --- PowerPath Path Check ---
%PLINK% -ssh -l %SSH_USER% -batch %HOST_IP% "powermt check"

echo.
echo ========================================
echo   Remote check complete.
echo ========================================
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Windows PC with plink.exe from PuTTY (https://www.putty.org — free)
- SSH access to the Linux server that has PowerPath installed (usually as root)
- PowerPath must already be installed and licensed on the remote Linux host

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `powerpath_remote_check.bat` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `HOST_IP` | IP address of the Linux server with PowerPath | Ask your storage admin |
| `SSH_USER` | SSH username | Typically `root` for PowerPath servers |
| `PLINK` | Full path to plink.exe if not in PATH | e.g. `C:\Program Files\PuTTY\plink.exe` |

**Step 3 — Accept the host key (one-time setup)**

Open Command Prompt and run:
```text
plink -ssh root@192.168.10.50
```
Type `y` when prompted, then press Ctrl+C.

**Step 4 — Run the script**

```bash
cd C:\Users\YourName\Desktop
powerpath_remote_check.bat
```

---

## Windows: PowerPath Check on Local Windows Host (CMD)

If PowerPath for Windows is installed directly on your Windows server, you can run `powermt` commands locally without SSH. This .bat file runs a health check and saves a report.

~~~batch
@echo off
REM powerpath_local_check.bat — PowerPath health check on a LOCAL Windows server
REM Run this ON the Windows server that has PowerPath for Windows installed.
REM PowerPath must be installed: https://www.dell.com/en-us/dt/data-protection/powerpath.htm
REM Run this script as Administrator (right-click → Run as administrator).

set REPORT_FILE=%USERPROFILE%\Desktop\powerpath_report.txt

echo ========================================
echo   PowerPath Local Health Check
echo   Report will be saved to: %REPORT_FILE%
echo ========================================
echo.

REM Check that powermt is available
where powermt >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: powermt.exe not found. Is PowerPath for Windows installed?
    echo Install it from the Dell support portal and try again.
    exit /b 1
)

echo Running powermt display dev=all ...
echo ===== PowerPath Device Report ===== > "%REPORT_FILE%"
echo Generated: %DATE% %TIME% >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

powermt display dev=all >> "%REPORT_FILE%" 2>&1

echo. >> "%REPORT_FILE%"
echo ===== PowerPath Check Output ===== >> "%REPORT_FILE%"
powermt check >> "%REPORT_FILE%" 2>&1

echo. >> "%REPORT_FILE%"
echo ===== PowerPath Migration Check ===== >> "%REPORT_FILE%"
powermig -chkpath >> "%REPORT_FILE%" 2>&1

echo.
echo Health check complete. Opening report ...
echo.

REM Open the report in Notepad automatically
notepad "%REPORT_FILE%"
~~~

---

## Daily Check Script

SSHes to each Linux host running PowerPath, runs `powermt display dev=all`, counts paths per device, flags any device with fewer than 2 active paths, and flags any path in a dead or failed state.

~~~bash
#!/bin/bash
# powerpath_daily_check.sh — Daily PowerPath path health check on Linux hosts
# Usage: HOST_IP=192.168.1.50 SSH_USER=root EXPECTED_PATHS=4 ./powerpath_daily_check.sh

set -euo pipefail

HOST_IP="${HOST_IP:?Set HOST_IP}"
SSH_USER="${SSH_USER:-root}"
EXPECTED_PATHS="${EXPECTED_PATHS:-4}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"
FAIL=0

echo "========================================"
echo "  PowerPath Daily Check"
echo "  Host : ${SSH_USER}@${HOST_IP}"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

POWERMT_OUT=$(ssh $SSH_OPTS "${SSH_USER}@${HOST_IP}" "powermt display dev=all" 2>&1) || \
  { echo "ERROR: Cannot connect to $HOST_IP or powermt not available"; exit 2; }

echo "$POWERMT_OUT" | python3 -c "
import sys, re

lines = sys.stdin.read().splitlines()
current_dev = None
devices = {}

for line in lines:
    m = re.match(r'^Pseudo\s+name=(\S+)', line)
    if m:
        current_dev = m.group(1)
        continue
    if current_dev:
        m2 = re.search(r'(\d+)\s+paths?,\s*(\d+)\s+dead', line)
        if m2:
            total = int(m2.group(1))
            dead  = int(m2.group(2))
            devices[current_dev] = {'total': total, 'dead': dead}
            current_dev = None

expected = int('${EXPECTED_PATHS}')
min_paths = 2
fail = False

print(f\"{'DEVICE':<22} {'TOTAL':>8} {'DEAD':>6} {'ALIVE':>6}  STATUS\")
print('-' * 60)

for dev, d in sorted(devices.items()):
    alive = d['total'] - d['dead']
    if d['dead'] > 0:
        status = 'DEAD PATHS  <<<'
        fail = True
    elif alive < min_paths:
        status = f'LOW PATHS (only {alive} alive)  <<<'
        fail = True
    else:
        status = 'OK'
    print(f\"{dev:<22} {d['total']:>8} {d['dead']:>6} {alive:>6}  {status}\")

print()
print(f'Total devices: {len(devices)}')
sys.exit(1 if fail else 0)
" || FAIL=1

echo ""
echo "========================================"
[[ "$FAIL" -eq 0 ]] && echo "  Result: PASS — all paths healthy on $HOST_IP" || \
  echo "  Result: FAIL — dead or low-path devices found on $HOST_IP"
exit $FAIL
~~~

---

## Incident Triage Script

Captures `powermt display dev=all`, `powermt check`, `powermt display options=all`, and kernel messages related to SCSI/multipath to a timestamped file.

~~~bash
#!/bin/bash
# powerpath_triage.sh — Capture PowerPath state to timestamped file
# Usage: HOST_IP=192.168.1.50 SSH_USER=root ./powerpath_triage.sh

set -euo pipefail

HOST_IP="${HOST_IP:?Set HOST_IP}"
SSH_USER="${SSH_USER:-root}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"

TS=$(date '+%Y%m%d_%H%M%S')
OUTFILE="/tmp/powerpath_triage_${HOST_IP//./_}_${TS}.txt"

pp_ssh() { ssh $SSH_OPTS "${SSH_USER}@${HOST_IP}" "$@" 2>&1 || echo "Command failed: $*"; }

{
  echo "========================================"
  echo "  PowerPath Incident Triage"
  echo "  Host : $HOST_IP"
  echo "  Time : $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================"

  echo ""
  echo "--- powermt display dev=all ---"
  pp_ssh "powermt display dev=all"

  echo ""
  echo "--- powermt check ---"
  pp_ssh "powermt check"

  echo ""
  echo "--- powermt display options=all ---"
  pp_ssh "powermt display options=all" 2>/dev/null || pp_ssh "powermt display options"

  echo ""
  echo "--- Kernel SCSI/multipath messages (last 100 lines) ---"
  pp_ssh "dmesg | grep -iE 'scsi|multipath|emcpower|powerpath' | tail -100" 2>/dev/null || echo "dmesg not available"

  echo ""
  echo "--- /var/log/messages (SCSI related, last 50 lines) ---"
  pp_ssh "grep -iE 'scsi|powerpath|emcpower' /var/log/messages 2>/dev/null | tail -50" 2>/dev/null || echo "Not available"

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

Before HBA maintenance or replacement: confirms each volume has more than 2 active paths, no paths are currently recovering, and `powermt check` returns clean. Exits 2 if any path count equals 1.

~~~bash
#!/bin/bash
# powerpath_precheck.sh — Pre-check before HBA maintenance on a Linux host
# Usage: HOST_IP=192.168.1.50 SSH_USER=root MIN_PATHS=2 ./powerpath_precheck.sh

set -euo pipefail

HOST_IP="${HOST_IP:?Set HOST_IP}"
SSH_USER="${SSH_USER:-root}"
MIN_PATHS="${MIN_PATHS:-2}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

echo "========================================"
echo "  PowerPath Pre-Change Check"
echo "  Host     : $HOST_IP"
echo "  Min paths: $MIN_PATHS"
echo "  Date     : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

pp_ssh() { ssh $SSH_OPTS "${SSH_USER}@${HOST_IP}" "$@" 2>&1; }

# Check 1: powermt check returns clean
echo "--- powermt check ---"
CHECK_OUT=$(pp_ssh "powermt check" 2>&1) || { check_fail "Cannot connect to $HOST_IP"; exit 2; }
echo "$CHECK_OUT"
if echo "$CHECK_OUT" | grep -qi "error\|dead\|failed\|topology change"; then
  check_fail "powermt check reports issues — resolve before HBA maintenance"
else
  check_pass "powermt check returned clean"
fi

# Check 2: All devices have > MIN_PATHS active paths (and no paths = 1)
echo ""
echo "--- Path count per device ---"
POWERMT_OUT=$(pp_ssh "powermt display dev=all" 2>&1)
echo "$POWERMT_OUT" | python3 -c "
import sys, re

lines = sys.stdin.read().splitlines()
current_dev = None
fail = False
min_paths = int('${MIN_PATHS}')

for line in lines:
    m = re.match(r'^Pseudo\s+name=(\S+)', line)
    if m:
        current_dev = m.group(1)
        continue
    if current_dev:
        m2 = re.search(r'(\d+)\s+paths?,\s*(\d+)\s+dead', line)
        if m2:
            total = int(m2.group(1))
            dead  = int(m2.group(2))
            alive = total - dead
            if alive <= 1:
                print(f'  [FAIL] {current_dev}: only {alive} alive path(s) — UNSAFE for HBA removal')
                fail = True
            elif alive <= min_paths:
                print(f'  [WARN] {current_dev}: {alive} alive paths (min {min_paths}) — proceed with caution')
                fail = True
            else:
                print(f'  [PASS] {current_dev}: {alive} alive paths, {dead} dead')
            current_dev = None

sys.exit(1 if fail else 0)
" || FAIL=1

# Check 3: No recovering paths
RECOVERING=$(echo "$POWERMT_OUT" | grep -ic "recovering" || true)
if [[ "$RECOVERING" -eq 0 ]]; then
  check_pass "No paths currently in recovering state"
else
  check_fail "$RECOVERING path(s) in recovering state — wait for recovery to complete"
fi

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: READY — safe to proceed with HBA maintenance"
  exit 0
else
  echo "  Result: NOT READY — resolve failures above (exit 2)"
  exit 2
fi
~~~

---

## Post-Change Validation Script

After HBA maintenance: runs `powermt display dev=all`, confirms all expected paths per device are restored, and compares path count to the pre-change baseline.

~~~bash
#!/bin/bash
# powerpath_postcheck.sh — Post-HBA maintenance path validation
# Usage: HOST_IP=x SSH_USER=root EXPECTED_PATHS=4 ./powerpath_postcheck.sh

set -euo pipefail

HOST_IP="${HOST_IP:?Set HOST_IP}"
SSH_USER="${SSH_USER:-root}"
EXPECTED_PATHS="${EXPECTED_PATHS:-4}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

echo "========================================"
echo "  PowerPath Post-Change Validation"
echo "  Host            : $HOST_IP"
echo "  Expected paths  : $EXPECTED_PATHS"
echo "  Date            : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

pp_ssh() { ssh $SSH_OPTS "${SSH_USER}@${HOST_IP}" "$@" 2>&1; }

POWERMT_OUT=$(pp_ssh "powermt display dev=all" 2>&1) || \
  { echo "ERROR: Cannot connect to $HOST_IP"; exit 1; }

echo "$POWERMT_OUT" | python3 -c "
import sys, re

lines = sys.stdin.read().splitlines()
current_dev = None
expected = int('${EXPECTED_PATHS}')
fail = False

print(f\"{'DEVICE':<22} {'TOTAL':>8} {'DEAD':>6} {'ALIVE':>6}  STATUS\")
print('-' * 65)

for line in lines:
    m = re.match(r'^Pseudo\s+name=(\S+)', line)
    if m:
        current_dev = m.group(1)
        continue
    if current_dev:
        m2 = re.search(r'(\d+)\s+paths?,\s*(\d+)\s+dead', line)
        if m2:
            total = int(m2.group(1))
            dead  = int(m2.group(2))
            alive = total - dead
            if dead > 0:
                status = 'DEAD PATHS  <<<'
                fail = True
            elif total < expected:
                status = f'LOW — expected {expected}, got {total}  <<<'
                fail = True
            elif total == expected:
                status = 'RESTORED OK'
            else:
                status = f'OK ({total} paths)'
            print(f'{current_dev:<22} {total:>8} {dead:>6} {alive:>6}  {status}')
            current_dev = None

sys.exit(1 if fail else 0)
" || FAIL=1

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: PASS — all paths restored to expected count ($EXPECTED_PATHS) on $HOST_IP"
  exit 0
else
  echo "  Result: FAIL — some devices have not fully restored expected paths"
  exit 1
fi
~~~

---

## Health Check Script

Cron-safe script reporting total devices, total paths, dead paths count, and devices with fewer than 2 active paths. Exits 0 (OK), 1 (warning), or 2 (critical/dead paths found).

~~~bash
#!/bin/bash
# powerpath_health.sh — Cron-safe PowerPath health check
# Usage: HOST_IP=x SSH_USER=root ./powerpath_health.sh
# Exit: 0=OK  1=WARNING(low paths)  2=CRITICAL(dead paths)

HOST_IP="${HOST_IP:?Set HOST_IP}"
SSH_USER="${SSH_USER:-root}"
MIN_ALIVE="${MIN_ALIVE:-2}"
SSH_OPTS="-o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=15"

POWERMT_OUT=$(ssh $SSH_OPTS "${SSH_USER}@${HOST_IP}" "powermt display dev=all" 2>/dev/null) || \
  { echo "PP_HEALTH host=${HOST_IP} status=CRITICAL reason=connection_failed"; exit 2; }

python3 -c "
import sys, re

lines = '''${POWERMT_OUT}'''.splitlines()
current_dev = None
total_devices = 0
total_paths   = 0
dead_paths    = 0
low_path_devs = 0
min_alive = int('${MIN_ALIVE}')
worst = 0

for line in lines:
    m = re.match(r'^Pseudo\s+name=(\S+)', line)
    if m:
        current_dev = m.group(1)
        total_devices += 1
        continue
    if current_dev:
        m2 = re.search(r'(\d+)\s+paths?,\s*(\d+)\s+dead', line)
        if m2:
            total = int(m2.group(1))
            dead  = int(m2.group(2))
            alive = total - dead
            total_paths += total
            dead_paths  += dead
            if dead > 0:
                worst = max(worst, 2)
            elif alive < min_alive:
                low_path_devs += 1
                worst = max(worst, 1)
            current_dev = None

if dead_paths > 0:
    worst = 2
elif low_path_devs > 0:
    worst = 1

status_map = {0: 'OK', 1: 'WARNING', 2: 'CRITICAL'}
print(f'PP_HEALTH host=${HOST_IP} total_devices={total_devices} total_paths={total_paths} dead_paths={dead_paths} low_path_devices={low_path_devs} status={status_map[worst]}')
sys.exit(worst)
"
~~~
