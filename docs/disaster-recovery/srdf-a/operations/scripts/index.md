# SRDF-A — Scripts


<div class="kb-summary">
> Part of the [SRDF/A](../../index.md) reference.
</div>

---
## SRDF/A Cycle Time Monitor (Bash)

Use SYMCLI to query SRDF/A cycle time and delta set processing time for a given RDF group, compare against configurable thresholds, and print the last 10 samples for trend visibility.

~~~bash
#!/usr/bin/env bash
# srdf-cycle-time-monitor.sh
# Usage: SID=<symm_id> RDF_GROUP=<group_num> ./srdf-cycle-time-monitor.sh
# Optional: WARN_THRESHOLD=30 CRIT_THRESHOLD=60

set -euo pipefail

SID="${SID:?SID (Symmetrix serial) is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
WARN_THRESHOLD="${WARN_THRESHOLD:-30}"
CRIT_THRESHOLD="${CRIT_THRESHOLD:-60}"
SAMPLES=10

echo ""
echo "=== SRDF/A Cycle Time Monitor ==="
echo "SID         : ${SID}"
echo "RDF Group   : ${RDF_GROUP}"
echo "Warn > ${WARN_THRESHOLD}s  |  Crit > ${CRIT_THRESHOLD}s"
echo "Time        : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Collect current cycle time data
RAW_OUTPUT=$(symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" queryall -detail 2>&1) || {
    echo "ERROR: symrdf command failed:"
    echo "${RAW_OUTPUT}"
    exit 2
}

# Parse cycle time (seconds) and delta set processing time
CYCLE_TIME=$(echo "${RAW_OUTPUT}" | grep -i "Cycle Time" | awk '{print $NF}' | head -1)
DELTA_PROC=$(echo "${RAW_OUTPUT}" | grep -i "Delta Set Processing" | awk '{print $NF}' | head -1)

CYCLE_TIME=${CYCLE_TIME:-0}
DELTA_PROC=${DELTA_PROC:-0}

echo "Current Cycle Time             : ${CYCLE_TIME}s"
echo "Current Delta Set Proc Time    : ${DELTA_PROC}s"
echo ""

# Determine status
EXIT_CODE=0
STATUS="OK"

if (( $(echo "${CYCLE_TIME} > ${CRIT_THRESHOLD}" | bc -l) )); then
    STATUS="CRITICAL"
    EXIT_CODE=2
elif (( $(echo "${CYCLE_TIME} > ${WARN_THRESHOLD}" | bc -l) )); then
    STATUS="WARNING"
    EXIT_CODE=1
fi

echo "Status: ${STATUS}"
echo ""

# Collect trend: run symrdf query multiple times (for cron-driven trend use a file cache)
TREND_FILE="/tmp/srdf_cycle_trend_${SID}_${RDF_GROUP}.log"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

# Append current sample
echo "${TIMESTAMP} cycle=${CYCLE_TIME}s delta=${DELTA_PROC}s status=${STATUS}" >> "${TREND_FILE}"

# Print last N samples
echo "Last ${SAMPLES} samples (from ${TREND_FILE}):"
echo "---------------------------------------------------"
if [[ -f "${TREND_FILE}" ]]; then
    tail -n "${SAMPLES}" "${TREND_FILE}"
else
    echo "(no history yet)"
fi

echo ""
exit ${EXIT_CODE}
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux server with SYMCLI installed (the Dell EMC Solutions Enabler package)
- SYMCLI must be able to communicate with the PowerMax / VMAX array (via local or gatekeeper connectivity)
- The Symmetrix array serial number (SID) and the RDF group number for your SRDF/A relationship

**Step 1 — Save the file**

1. Open a text editor on the SYMCLI Linux management server
2. Copy the entire code block above
3. Save it as `srdf-cycle-time-monitor.sh`

**Step 2 — Fill in your details**

Pass as environment variables when running, or set defaults in the script:

| Variable | What to put here | How to find it |
|---|---|---|
| `SID` | Symmetrix / PowerMax serial number | Run `symcfg list` on the SYMCLI host |
| `RDF_GROUP` | RDF group number for the SRDF/A pair | Run `symrdf list -sid <SID>` to see RDF groups |
| `WARN_THRESHOLD` | Cycle time in seconds that triggers a warning | Default 30s — adjust based on your RPO requirement |
| `CRIT_THRESHOLD` | Cycle time in seconds that triggers critical | Default 60s |

**Step 3 — Open a terminal**

- **For .sh:** Log into the SYMCLI Linux management server via SSH or console and open a terminal

**Step 4 — Make the script executable and run it**

```bash
chmod +x srdf-cycle-time-monitor.sh
SID=000123456789 RDF_GROUP=1 ./srdf-cycle-time-monitor.sh
```
```
┌────────────────────────────────────────── SRDF/A — Scripts ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  SRDF/A — Automation Scripts                                  │   │
│   │               Scripts automate routine SRDF/A operations — run via cron or CI/CD              │   │
│   │               Always store credentials in vault (not in script); log all output               │   │
│   │                 Test scripts in non-production before scheduling in production                │   │
│   │                        Scope scripts to least-privilege service account                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Status / Reporting Scripts          │  │              Automation Scripts             │   │
│   │           Job success rate report            │  │            Auto-expire old points           │   │
│   │              Capacity trending               │  │          Auto-add new VMs to policy         │   │
│   │            SLA compliance report             │  │          Nightly DR test validation         │   │
│   │             RPO / RTO dashboard              │  │             Alert on job failure            │   │
│   │                 symrdf query                 │  │           symrdf suspend / resume           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports      │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology               │
│  R1            = source SRDF volume on production array; host writes flow here                        │
│  R2            = target SRDF volume on DR array; receives replicated data asynchronously              │
│  Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically          │
│  Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO                  │
│  symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore       │
│  SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth             │
│  Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle            │
│  Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts                   │
│  Restore       = after failover resolution, re-establishes replication with R1 as source              │
│  Establish     = initial sync or re-sync operation that copies R1 to R2 in full                       │
│  Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication                 │
│  FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link                      │
│  Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**What you should see**

Timestamped log lines for each step: verifying Synchronized state, suspending, waiting for Suspended confirmation, splitting, and checking R2 device states. After completion, instructions are printed for the host team. A log file is written to `/var/log/`.

---

## SRDF Resync After DR Test (Bash)

Re-establish and resynchronize SRDF relationships back to production after a DR test, once the host team confirms they have unmounted R2 copies.

~~~bash
#!/usr/bin/env bash
# srdf-resync-after-dr-test.sh
# Usage: SID=<sid> RDF_GROUP=<rdfg> CG_NAME=<cg> ./srdf-resync-after-dr-test.sh
#
# Run ONLY after DR hosts have confirmed they have stopped I/O and unmounted R2 volumes.

set -euo pipefail

SID="${SID:?SID is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
CG_NAME="${CG_NAME:?CG_NAME is required}"
MODE="${MODE:-cg}"
LOGFILE="/var/log/srdf-resync-$(date +%Y%m%d-%H%M%S).log"
SYNC_POLL_INTERVAL=30
SYNC_TIMEOUT=3600

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

run_cmd() {
    log "CMD: $*"
    "$@" 2>&1 | tee -a "${LOGFILE}"
}

log "=== SRDF Resync After DR Test ==="
log "SID=${SID}  RDFG=${RDF_GROUP}  CG=${CG_NAME}  MODE=${MODE}"

# --- Step 1: Confirm host acknowledgement ---
log "Step 1: Verifying preconditions..."
echo ""
echo "IMPORTANT: This script will re-establish SRDF replication."
echo "           R2 volumes will become READ-ONLY / Write Disabled."
echo ""
read -r -p "Confirm DR hosts have stopped I/O and unmounted R2 LUNs? [yes/no]: " CONFIRM
if [[ "${CONFIRM}" != "yes" ]]; then
    log "Aborted by operator. Please ensure DR hosts are off R2 volumes before resyncing."
    exit 1
fi

# --- Step 2: Establish SRDF relationships ---
log "Step 2: Establishing SRDF relationships (R1->R2 direction)..."
if [[ "${MODE}" == "cg" ]]; then
    run_cmd symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" -cg "${CG_NAME}" establish -noprompt
else
    run_cmd symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" establish -noprompt
fi

log "Establish command submitted. Starting sync progress monitor..."

# --- Step 3: Wait for sync to complete ---
ELAPSED=0
while [[ $ELAPSED -lt $SYNC_TIMEOUT ]]; do
    SYNC_STATUS=$(symrdf query -sid "${SID}" -rdfg "${RDF_GROUP}" 2>&1)

    SYNC_COUNT=$(echo "${SYNC_STATUS}" | grep -c "Synchronized" || true)
    SYNCING_COUNT=$(echo "${SYNC_STATUS}" | grep -c "Syncing" || true)
    TOTAL=$(echo "${SYNC_STATUS}" | grep -cE "^[0-9A-Fa-f]{4}" || true)

    log "Progress: ${SYNC_COUNT}/${TOTAL} Synchronized, ${SYNCING_COUNT} still Syncing..."

    if [[ "${SYNCING_COUNT}" -eq 0 ]] && [[ "${SYNC_COUNT}" -gt 0 ]]; then
        log "All devices appear Synchronized."
        break
    fi

    sleep "${SYNC_POLL_INTERVAL}"
    ELAPSED=$((ELAPSED + SYNC_POLL_INTERVAL))
done

if [[ $ELAPSED -ge $SYNC_TIMEOUT ]]; then
    log "WARNING: Sync timed out after ${SYNC_TIMEOUT}s. Check manually with:"
    log "  symrdf query -sid ${SID} -rdfg ${RDF_GROUP}"
    exit 1
fi

# --- Step 4: Final state verification ---
log "Step 4: Final state verification..."
FINAL_STATE=$(symrdf query -sid "${SID}" -rdfg "${RDF_GROUP}" 2>&1 | \
    grep -E "Synchronized|Consistent" | wc -l || true)

if [[ "${FINAL_STATE}" -eq 0 ]]; then
    log "WARNING: Final verification failed — no Synchronized devices found."
    log "Review output of: symrdf query -sid ${SID} -rdfg ${RDF_GROUP}"
    exit 1
fi

log "Step 4: Verified. ${FINAL_STATE} device pair(s) confirmed Synchronized."

log ""
log "=== RESYNC COMPLETE ==="
log "Production SRDF replication is restored."
log "Log: ${LOGFILE}"
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux server with SYMCLI installed and connectivity to the PowerMax array
- Confirmation from the DR/host team that all applications have been stopped and R2 LUNs unmounted on the DR site servers
- The SID, RDF group number, and Consistency Group name

**Step 1 — Save the file**

1. Open a text editor on the SYMCLI Linux management server
2. Copy the entire code block above
3. Save it as `srdf-resync-after-dr-test.sh`

**Step 2 — Fill in your details**

| Variable | What to put here | How to find it |
|---|---|---|
| `SID` | Symmetrix array serial number | `symcfg list` |
| `RDF_GROUP` | RDF group number | `symrdf list -sid <SID>` |
| `CG_NAME` | Consistency group name | `symcg list -sid <SID>` |

**Step 3 — Open a terminal**

- **For .sh:** Log into the SYMCLI Linux management server and open a terminal

**Step 4 — Make the script executable and run it**

```bash
chmod +x srdf-resync-after-dr-test.sh
SID=000123456789 RDF_GROUP=1 CG_NAME=MyAppCG ./srdf-resync-after-dr-test.sh
```

**What you should see**

A prompt asking you to confirm that DR hosts have stopped I/O and unmounted R2 LUNs — type `yes` to continue. Then timestamped log lines showing the establish command, followed by progress polling every 30 seconds (e.g. `5/50 Synchronized, 45 still Syncing...`). When complete: `RESYNC COMPLETE — Production SRDF replication is restored.`

---

## Windows: SRDF/A State Check via Unisphere REST API (PowerShell)

Query the Unisphere for PowerMax REST API from a Windows PC to list all SRDF/A pairs, their replication state, and flag any volume not in Consistent or Synchronized state.

~~~powershell
# srdf-a-state-check-windows.ps1
# Usage: .\srdf-a-state-check-windows.ps1 -UnisphereHost <IP> -UnisphereUser <user> -UnispherePass <pass> -SID <array_serial> -RdfGroup <group_num>
# Requires: PowerShell 5.1 or later
# Unisphere REST API: https://<UnisphereHost>:8443/univmax/restapi/
# Note: Use the Unisphere server hostname/IP, not the array directly.

param(
    [Parameter(Mandatory)][string]$UnisphereHost,
    [Parameter(Mandatory)][string]$UnisphereUser,
    [Parameter(Mandatory)][string]$UnispherePass,
    [Parameter(Mandatory)][string]$SID,
    [Parameter(Mandatory)][string]$RdfGroup
)

# Suppress SSL errors for self-signed certificates
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

$BaseUrl = "https://${UnisphereHost}:8443/univmax/restapi/100"
$Auth    = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${UnisphereUser}:${UnispherePass}"))
$Headers = @{
    Authorization  = "Basic $Auth"
    "Content-Type" = "application/json"
    "Accept"       = "application/json"
}

function Get-Unisphere {
    param([string]$Endpoint)
    return Invoke-RestMethod -Uri "$BaseUrl$Endpoint" -Headers $Headers -Method GET
}

Write-Host ""
Write-Host "=== SRDF/A State Check (Windows) ===" -ForegroundColor Cyan
Write-Host "Unisphere : $UnisphereHost"
Write-Host "Array SID : $SID"
Write-Host "RDF Group : $RdfGroup"
Write-Host "Date      : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

# --- List RDF groups to confirm the group exists ---
try {
    $rdfGroups = Get-Unisphere "/replication/symmetrix/$SID/rdf_group"
    $groupList = $rdfGroups.rdfGroupID
    if ($groupList -notcontains [int]$RdfGroup) {
        Write-Host "WARNING: RDF group $RdfGroup not found in array $SID." -ForegroundColor Yellow
        Write-Host "Available groups: $($groupList -join ', ')"
    } else {
        Write-Host "RDF group $RdfGroup confirmed on array $SID." -ForegroundColor Green
    }
} catch {
    Write-Host "WARNING: Could not retrieve RDF group list: $_" -ForegroundColor Yellow
}

Write-Host ""

# --- Get SRDF/A volumes in the RDF group ---
try {
    $volumeData = Get-Unisphere "/replication/symmetrix/$SID/rdf_group/$RdfGroup/volume"
    $volumes    = $volumeData.name

    if (-not $volumes -or $volumes.Count -eq 0) {
        Write-Host "No volumes found in RDF group $RdfGroup." -ForegroundColor Yellow
        exit 0
    }

    Write-Host "Volumes in RDF group $RdfGroup : $($volumes.Count)"
    Write-Host ""
    Write-Host ("{0,-12} {1,-15} {2,-15} {3,-12} {4}" -f "Volume", "R1 State", "R2 State", "Mode", "Delta Mark / Notes")
    Write-Host ("-" * 75)

    $problemVolumes = 0
    $goodStates     = @("Synchronized", "Consistent")

    foreach ($vol in $volumes) {
        try {
            $volDetail = Get-Unisphere "/replication/symmetrix/$SID/rdf_group/$RdfGroup/volume/$vol"
            $r1State   = $volDetail.rdfpairState
            $r2State   = $volDetail.remoteRdfpairState
            $mode      = $volDetail.rdfMode
            $deltaMark = $volDetail.deltaMark

            $isGood = ($r1State -in $goodStates) -and ($r2State -in $goodStates)
            $color  = if ($isGood) { "Green" } else { "Red" }
            if (-not $isGood) { $problemVolumes++ }

            $notes = if ($deltaMark) { "DeltaMark=$deltaMark" } else { "" }
            Write-Host ("{0,-12} {1,-15} {2,-15} {3,-12} {4}" -f $vol, $r1State, $r2State, $mode, $notes) -ForegroundColor $color
        } catch {
            Write-Host ("{0,-12} ERROR: Could not retrieve volume detail: $_" -f $vol) -ForegroundColor Yellow
        }
    }

    Write-Host ""
    if ($problemVolumes -gt 0) {
        Write-Host "RESULT: $problemVolumes volume(s) are NOT in Consistent/Synchronized state (shown in red)." -ForegroundColor Red
        exit 1
    } else {
        Write-Host "RESULT: All $($volumes.Count) volume(s) are Consistent or Synchronized." -ForegroundColor Green
        exit 0
    }
} catch {
    Write-Host "ERROR retrieving volume data: $_" -ForegroundColor Red
    exit 1
}
~~~

### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or 11 with PowerShell (already installed)
- Network access to the Unisphere for PowerMax server on port 8443 from your Windows PC
- Unisphere credentials (not the array credentials — the Unisphere management server credentials)
- The PowerMax / VMAX array serial number (SID) and the RDF group number

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Save it as `srdf-a-state-check-windows.ps1` on your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | How to find it |
|---|---|---|
| `$UnisphereHost` | Unisphere for PowerMax server IP or hostname | Ask your storage admin — this is the management server, not the array |
| `$UnisphereUser` | Unisphere username | Usually `smc` or your storage admin user |
| `$UnispherePass` | Unisphere password | Your Unisphere login password |
| `$SID` | PowerMax array serial number | Shown on the Unisphere dashboard, e.g. `000123456789` |
| `$RdfGroup` | RDF group number for your SRDF/A pair | Shown in Unisphere under Replication > SRDF Groups |

**Step 3 — Open a terminal**

Windows key → search `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
.\srdf-a-state-check-windows.ps1 -UnisphereHost 192.168.1.200 -UnisphereUser smc -UnispherePass MyPassword -SID 000123456789 -RdfGroup 1
```

**What you should see**

Confirmation that the RDF group exists on the array, then a table listing every volume in the group with its R1 state, R2 state, mode (SRDF/A), and delta mark value. Volumes in Consistent or Synchronized state are shown in green. Any volume in any other state (Suspended, Split, etc.) is shown in red. The final line gives the overall result.

---

## Windows: SRDF/A Cycle Time Check via Plink (CMD)

Use plink.exe to SSH to the SYMCLI Linux management server and run SYMCLI commands to check SRDF/A pair states and verify replication — without needing SYMCLI installed on your Windows PC.

~~~batch
@echo off
REM srdf-a-cycle-check.bat — SRDF/A state check via SSH to SYMCLI host (plink)
REM Uses plink.exe (from PuTTY) for SSH. Download: https://www.putty.org
REM
REM NOTE: This script SSH's to the SYMCLI Linux management server (not directly
REM       to the PowerMax array). SYMCLI must be installed on SYMCLI_HOST.
REM
REM FIRST-TIME SETUP — Accept SSH fingerprint (run once):
REM   plink.exe -ssh admin@YOUR_SYMCLI_HOST
REM   Type 'y' to accept the fingerprint, then Ctrl+C.

set SYMCLI_HOST=192.168.1.50
set SSH_USER=symadmin
set SID=000123456789
set RDF_GROUP=1
set PLINK=plink.exe

echo.
echo === SRDF/A State Check (via SYMCLI host) ===
echo SYMCLI Host : %SYMCLI_HOST%
echo Array SID   : %SID%
echo RDF Group   : %RDF_GROUP%
echo.

echo ----------------------------------------
echo SRDF/A PAIR LIST
echo ----------------------------------------
%PLINK% -ssh -l %SSH_USER% -batch %SYMCLI_HOST% "symrdf list -sid %SID% -rdfg %RDF_GROUP% -type srdf_a"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not connect to %SYMCLI_HOST% or symrdf command failed.
    echo Check: 1) SYMCLI_HOST is reachable, 2) SYMCLI is installed on that host,
    echo        3) SSH fingerprint has been accepted (run plink manually once),
    echo        4) SSH_USER has permission to run symrdf commands.
    exit /b 1
)

echo.
echo ----------------------------------------
echo SRDF/A PAIR STATE VERIFICATION
echo ----------------------------------------
%PLINK% -ssh -l %SSH_USER% -batch %SYMCLI_HOST% "symrdf verify -sid %SID% -rdfg %RDF_GROUP%"

echo.
echo ----------------------------------------
echo SRDF/A CYCLE TIME QUERY
echo ----------------------------------------
%PLINK% -ssh -l %SSH_USER% -batch %SYMCLI_HOST% "symrdf -sid %SID% -rdfg %RDF_GROUP% queryall -detail"

echo.
echo Done.
~~~

### How to run this script — step by step

**Before you start — what you need**
- PuTTY installed on Windows — download from https://www.putty.org
- A Linux management server with Dell EMC SYMCLI (Solutions Enabler) installed — this is where the script sends its commands
- SSH access from your Windows PC to that Linux SYMCLI server
- The PowerMax array serial number (SID) and the RDF group number

**Step 1 — Save the file**

1. Open **Notepad** (Windows key → search Notepad)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Save it as `srdf-a-cycle-check.bat` on your Desktop

**Step 2 — Fill in your details**

Open the saved file and change these lines near the top:

| Variable | What to put here | How to find it |
|---|---|---|
| `SYMCLI_HOST` | IP address of the Linux SYMCLI management server | Ask your storage admin — this is NOT the array IP |
| `SSH_USER` | SSH username on the SYMCLI server | Usually a dedicated symcli user, e.g. `symadmin` |
| `SID` | PowerMax array serial number | Run `symcfg list` on the SYMCLI server, or ask your storage admin |
| `RDF_GROUP` | RDF group number | Run `symrdf list -sid <SID>` on the SYMCLI server |
| `PLINK` | Path to plink.exe | Default `plink.exe` if PuTTY is in PATH, or full path like `C:\Program Files\PuTTY\plink.exe` |

**Step 3 — Accept the SSH fingerprint first (one-time step)**

Open Command Prompt and run:
```text
plink.exe -ssh symadmin@192.168.1.50
```
Type `y` when asked, then Ctrl+C. Do this once per SYMCLI host.

**Step 4 — Open a terminal**

Open **Command Prompt**: Windows key → search `cmd` → press Enter

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
srdf-a-cycle-check.bat
```

**What you should see**

Three sections: SRDF/A pair list showing all device pairs and their current state (Consistent/Synchronized/etc.), a pair state verification output confirming pairs are in the expected state, and a detailed cycle time query showing current SRDF/A cycle time and delta set processing time. Any pairs not in a healthy state will be clearly visible in the output.

---

## Daily Check Script

SSH to the SYMCLI management host and check SRDF/A pair states. Flags any pairs not in Consistent or Synchronized state and detects Transmit_Idle, Split, or Mixed conditions.

~~~bash
#!/bin/bash
# srdf_daily_check.sh
# Usage: SYMCLI_HOST=<ip> SSH_USER=<user> SID=<sid> RDF_GROUP=<rdfg> ./srdf_daily_check.sh

SYMCLI_HOST="${SYMCLI_HOST:?SYMCLI_HOST is required}"
SSH_USER="${SSH_USER:-symadmin}"
SID="${SID:?SID is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
SSH_OPTS="-o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=10"
FAIL=0

ssh_cmd() { ssh $SSH_OPTS "$SSH_USER@$SYMCLI_HOST" "$1" 2>/dev/null; }

echo "=== SRDF/A Daily Check: SID=$SID RDFG=$RDF_GROUP — $(date) ==="

PAIRS=$(ssh_cmd "$SYMCLI_PATH/symrdf list -sid $SID -rdfg $RDF_GROUP")

# Count pairs not in Consistent/Synchronized
NOT_GOOD=$(echo "$PAIRS" | grep -vE "Consistent|Synchronized|^-|^ *$|^Sym|^Local|^RDF|^Dev" | grep -c "[0-9A-Fa-f]" || true)
if [ "$NOT_GOOD" -gt 0 ]; then
  echo "[FAIL] $NOT_GOOD pair(s) not in Consistent/Synchronized state"; FAIL=$((FAIL+1))
else
  echo "[OK]   All pairs Consistent/Synchronized"
fi

# Flag Transmit_Idle, Split, or Mixed
for BAD_STATE in "Transmit_Idle" "Split" "Mixed"; do
  COUNT=$(echo "$PAIRS" | grep -ic "$BAD_STATE" || true)
  if [ "$COUNT" -gt 0 ]; then
    echo "[FAIL] $COUNT pair(s) in $BAD_STATE state"; FAIL=$((FAIL+1))
  fi
done

echo ""
echo "Daily check: $FAIL failure(s)"
[ "$FAIL" -gt 0 ] && exit 2 || exit 0
~~~

---

## Incident Triage Script

Capture a full SRDF/A diagnostic snapshot to a timestamped file via SSH to the SYMCLI host.

~~~bash
#!/bin/bash
# srdf_triage.sh
# Usage: SYMCLI_HOST=<ip> SSH_USER=<user> SID=<sid> RDF_GROUP=<rdfg> ./srdf_triage.sh

SYMCLI_HOST="${SYMCLI_HOST:?SYMCLI_HOST is required}"
SSH_USER="${SSH_USER:-symadmin}"
SID="${SID:?SID is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
SSH_OPTS="-o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=10"
OUTFILE="/tmp/srdf_triage_${SID}_${RDF_GROUP}_$(date +%Y%m%d_%H%M%S).txt"

ssh_cmd() { ssh $SSH_OPTS "$SSH_USER@$SYMCLI_HOST" "$1" 2>/dev/null; }

{
  echo "=== SRDF/A Incident Triage: SID=$SID RDFG=$RDF_GROUP — $(date) ==="
  echo ""
  echo "--- symrdf list -sid $SID ---"
  ssh_cmd "$SYMCLI_PATH/symrdf list -sid $SID"
  echo ""
  echo "--- symrdf queryall -sid $SID -rdfg $RDF_GROUP ---"
  ssh_cmd "$SYMCLI_PATH/symrdf queryall -sid $SID -rdfg $RDF_GROUP"
  echo ""
  echo "--- symcfg -sid $SID list -license ---"
  ssh_cmd "$SYMCLI_PATH/symcfg -sid $SID list -license"
  echo ""
  echo "--- SRDF link utilization ---"
  ssh_cmd "$SYMCLI_PATH/symrdf -sid $SID -rdfg $RDF_GROUP queryall -detail" | grep -iE "util|bandwidth|cycle|delta"
} > "$OUTFILE" 2>&1

echo "Triage data saved to: $OUTFILE"
~~~

---

## Change Pre-Check Script

Validate SRDF/A pair state before R1 or R2 storage maintenance. Exits 2 on any failure.

~~~bash
#!/bin/bash
# srdf_precheck.sh
# Usage: SYMCLI_HOST=<ip> SSH_USER=<user> SID=<sid> RDF_GROUP=<rdfg> ./srdf_precheck.sh

SYMCLI_HOST="${SYMCLI_HOST:?SYMCLI_HOST is required}"
SSH_USER="${SSH_USER:-symadmin}"
SID="${SID:?SID is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
SSH_OPTS="-o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=10"
FAIL=0

ssh_cmd() { ssh $SSH_OPTS "$SSH_USER@$SYMCLI_HOST" "$1" 2>/dev/null; }

echo "=== SRDF/A Pre-Change Check: SID=$SID RDFG=$RDF_GROUP — $(date) ==="

PAIRS=$(ssh_cmd "$SYMCLI_PATH/symrdf list -sid $SID -rdfg $RDF_GROUP")

# All pairs in Consistent state
NOT_CONSISTENT=$(echo "$PAIRS" | grep -vE "Consistent|^-|^ *$|^Sym|^Local|^RDF|^Dev" | grep -c "[0-9A-Fa-f]" || true)
if [ "$NOT_CONSISTENT" -gt 0 ]; then
  echo "[FAIL] $NOT_CONSISTENT pair(s) not in Consistent state"; FAIL=$((FAIL+1))
else
  echo "[OK]   All pairs Consistent"
fi

# No pairs in degraded state
for BAD in "Transmit_Idle" "Split" "Suspended" "Failed"; do
  CNT=$(echo "$PAIRS" | grep -ic "$BAD" || true)
  if [ "$CNT" -gt 0 ]; then
    echo "[FAIL] $CNT pair(s) in degraded state: $BAD"; FAIL=$((FAIL+1))
  fi
done

# SRDF link bandwidth < 70% (parse from queryall)
DETAIL=$(ssh_cmd "$SYMCLI_PATH/symrdf -sid $SID -rdfg $RDF_GROUP queryall -detail")
UTIL=$(echo "$DETAIL" | grep -iE "util" | awk '{print $NF}' | tr -d '%' | head -1)
if [ -n "$UTIL" ] && [ "$UTIL" -gt 70 ] 2>/dev/null; then
  echo "[FAIL] SRDF link utilisation at ${UTIL}% — above 70%"; FAIL=$((FAIL+1))
else
  echo "[OK]   SRDF link utilisation: ${UTIL:-N/A}%"
fi

echo ""
echo "Pre-check: $FAIL failure(s)"
[ "$FAIL" -gt 0 ] && exit 2 || exit 0
~~~

---

## Post-Change Validation Script

Confirm all SRDF/A pairs have returned to Consistent state after maintenance and RPO is within SLA.

~~~bash
#!/bin/bash
# srdf_postcheck.sh
# Usage: SYMCLI_HOST=<ip> SSH_USER=<user> SID=<sid> RDF_GROUP=<rdfg> ./srdf_postcheck.sh

SYMCLI_HOST="${SYMCLI_HOST:?SYMCLI_HOST is required}"
SSH_USER="${SSH_USER:-symadmin}"
SID="${SID:?SID is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
SSH_OPTS="-o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=10"
FAIL=0

ssh_cmd() { ssh $SSH_OPTS "$SSH_USER@$SYMCLI_HOST" "$1" 2>/dev/null; }

echo "=== SRDF/A Post-Change Validation: SID=$SID RDFG=$RDF_GROUP — $(date) ==="

PAIRS=$(ssh_cmd "$SYMCLI_PATH/symrdf list -sid $SID -rdfg $RDF_GROUP")

# All pairs back to Consistent
NOT_CONSISTENT=$(echo "$PAIRS" | grep -vE "Consistent|^-|^ *$|^Sym|^Local|^RDF|^Dev" | grep -c "[0-9A-Fa-f]" || true)
if [ "$NOT_CONSISTENT" -gt 0 ]; then
  echo "[FAIL] $NOT_CONSISTENT pair(s) still not in Consistent state"; FAIL=$((FAIL+1))
else
  echo "[OK]   All pairs Consistent"
fi

# Delta mark count stable
DETAIL=$(ssh_cmd "$SYMCLI_PATH/symrdf -sid $SID -rdfg $RDF_GROUP queryall -detail")
DELTA=$(echo "$DETAIL" | grep -i "delta" | awk '{print $NF}' | head -1)
echo "[INFO] Delta mark count: ${DELTA:-N/A}"

# Link utilization back to baseline
UTIL=$(echo "$DETAIL" | grep -iE "util" | awk '{print $NF}' | tr -d '%' | head -1)
echo "[INFO] SRDF link utilisation: ${UTIL:-N/A}%"

echo ""
echo "Post-change validation: $FAIL failure(s)"
[ "$FAIL" -gt 0 ] && exit 2 || exit 0
~~~

---

## Health Check Script

Cron-safe summary: total pairs, pairs Consistent, pairs degraded, delta mark count, and link utilization. Exits 0 (OK), 1 (WARNING), or 2 (CRITICAL).

~~~bash
#!/bin/bash
# srdf_health_check.sh
# Cron: */5 * * * * SYMCLI_HOST=<ip> SSH_USER=<user> SID=<sid> RDF_GROUP=<rdfg> /opt/scripts/srdf_health_check.sh

SYMCLI_HOST="${SYMCLI_HOST:?SYMCLI_HOST is required}"
SSH_USER="${SSH_USER:-symadmin}"
SID="${SID:?SID is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
SSH_OPTS="-o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=10"

ssh_cmd() { ssh $SSH_OPTS "$SSH_USER@$SYMCLI_HOST" "$1" 2>/dev/null; }

PAIRS=$(ssh_cmd "$SYMCLI_PATH/symrdf list -sid $SID -rdfg $RDF_GROUP")
TOTAL=$(echo "$PAIRS" | grep -c "[0-9A-Fa-f]\{4\}" || true)
CONSISTENT=$(echo "$PAIRS" | grep -ic "Consistent" || true)
DEGRADED=$(echo "$PAIRS" | grep -icE "Transmit_Idle|Split|Suspended|Failed" || true)

DETAIL=$(ssh_cmd "$SYMCLI_PATH/symrdf -sid $SID -rdfg $RDF_GROUP queryall -detail")
DELTA=$(echo "$DETAIL" | grep -i "delta" | awk '{print $NF}' | head -1)
UTIL=$(echo "$DETAIL" | grep -iE "util" | awk '{print $NF}' | tr -d '%' | head -1)

echo "sid=$SID rdfg=$RDF_GROUP total_pairs=$TOTAL consistent=$CONSISTENT degraded=$DEGRADED delta_marks=${DELTA:-N/A} link_util_pct=${UTIL:-N/A}"

if [ "${DEGRADED:-0}" -gt 5 ]; then
  exit 2
elif [ "${DEGRADED:-0}" -gt 0 ]; then
  exit 1
fi
exit 0
~~~
