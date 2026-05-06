# Scripts

> Part of the [Dell PowerPath](../) reference.

---

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

#### How to run this script — step by step

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

```
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

#### How to run this script — step by step

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

```
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

#### How to run this script — step by step

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
```
chmod +x powerpath_policy_audit.sh
sudo ./powerpath_policy_audit.sh
```

To check and automatically fix any non-CLAROpt devices:
```
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

#### How to run this script — step by step

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
```
plink -ssh root@192.168.10.50
```
Type `y` when prompted, then press Ctrl+C.

**Step 4 — Open a terminal**

- **For .bat (Command Prompt):** Open Command Prompt (Windows key → type `cmd`).

**Step 5 — Run the script**

```
cd C:\Users\YourName\Desktop
powerpath_remote_check.bat
```

**What you should see**

The full output of `powermt display dev=all` showing every pseudo device with its paths, followed by `powermt check` output which reports any path failures or topology changes detected since the last check.

---

## Windows: PowerPath Check on Local Windows Host (CMD)

If PowerPath for Windows is installed directly on your Windows server (common in Windows SAN environments), you can run `powermt` commands locally without SSH. This .bat file runs a health check and saves a report.

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

#### How to run this script — step by step

**Before you start — what you need**
- PowerPath for Windows installed on this Windows server (it must be the server connected to the SAN, not just any Windows PC)
- Administrator rights on the server
- PowerPath is a licensed product — confirm with your storage admin that it is installed

**Step 1 — Save the file**

1. Open **Notepad** on the Windows server
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `powerpath_local_check.bat` and save it to your Desktop

**Step 2 — Fill in your details**

No variables need to be changed for a basic run. The report will be saved to your Desktop automatically. To change the report location, edit the `REPORT_FILE` line near the top.

**Step 3 — Open a terminal**

Right-click the `powerpath_local_check.bat` file on your Desktop and choose **Run as administrator**. PowerPath commands require admin rights to run.

**Step 4 — Run the script**

Double-click the .bat file (as administrator), or from an elevated Command Prompt:
```
cd C:\Users\YourName\Desktop
powerpath_local_check.bat
```

**What you should see**

The script runs three PowerPath commands and saves their output to a text file on your Desktop called `powerpath_report.txt`. When it finishes, Notepad opens automatically showing the report. Look for lines containing `dead` (dead paths) or any devices with fewer paths than expected. The `powermt check` section reports any path topology changes.
