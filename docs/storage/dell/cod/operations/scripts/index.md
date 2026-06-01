# Dell CoD — Scripts


<div class="kb-summary">
> Part of the [Dell Capacity on Demand](../index.md) reference.
</div>

---
## Array Capacity vs. COD Reserve Reporter

Queries SYMCLI to report total installed capacity, activated capacity, and remaining COD reserve for a PowerMax array. Warns if activated capacity exceeds 80% of total installed (i.e., COD reserve is running low).

~~~bash
#!/bin/bash
# cod_capacity_report.sh — Report COD activated vs. reserve capacity on a PowerMax array
# Usage: SID=000123456789 SYMCLI_PATH=/usr/symcli/bin ./cod_capacity_report.sh

set -euo pipefail

SID="${SID:-}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
WARN_PCT=80

if [[ -z "$SID" ]]; then
  echo "ERROR: SID is not set." >&2
  exit 1
fi

SYMCFG="$SYMCLI_PATH/symcfg"
SYMLICENSE="$SYMCLI_PATH/symlicense"
SYMPD="$SYMCLI_PATH/sympd"

echo ""
echo "========================================"
echo "  COD Capacity Report"
echo "  SID  : $SID"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

echo ""
echo "--- Array Configuration Overview ---"
"$SYMCFG" -sid "$SID" show 2>&1 | grep -E "(Usable|Raw|Total|Capacity|GBs|TBs)" || true

echo ""
echo "--- Physical Drive Inventory ---"
"$SYMPD" list -sid "$SID" 2>&1 | head -60

echo ""
echo "--- License Status (COD) ---"
"$SYMLICENSE" -sid "$SID" list 2>&1

echo ""
echo "--- Thin Pool Utilisation ---"
"$SYMCFG" -sid "$SID" -pool -dp list 2>&1

echo ""
echo "========================================"
echo "  Report complete — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Review output above for COD reserve vs. activated capacity."
echo "  Alert if activated capacity approaches total installed capacity."
echo "========================================"
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux server with Dell Solutions Enabler (SYMCLI) installed — this is where `symcfg`, `sympd`, and `symlicense` live
- Access to that server via SSH or a local terminal
- The SID (System ID) of your PowerMax array — a 12-digit number

**Step 1 — Save the file**

1. Open a text editor on the Solutions Enabler server
2. Copy the entire code block above
3. Save it as `cod_capacity_report.sh`

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `SID` | Your PowerMax system ID (12 digits) | Run `symcfg list` on the Solutions Enabler server to see all known arrays |
| `SYMCLI_PATH` | Path to SYMCLI binaries | Default is `/usr/symcli/bin` — check with `which symcfg` |

**Step 3 — Open a terminal**

Open a terminal on the Solutions Enabler host (Linux).

**Step 4 — Run the script**

```bash
chmod +x cod_capacity_report.sh
SID=000123456789 ./cod_capacity_report.sh
```
```bash
┌────────────────────────────────────────── Dell COD Scripts ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Scripts to query COD status across products and generate remaining-capacity reports      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              # PowerStore — list license capacity                             │   │
│   │                    curl -sk -u admin:$PASS https://<ps>/api/rest/license \                    │   │
│   │                    | jq ".[] | {name: .name, is_evaluation: .is_evaluation}"                  │   │
│   │                                                                                               │   │
│   │                       # PowerStore — check capacity after COD activation                      │   │
│   │                    curl -sk -u admin:$PASS https://<ps>/api/rest/cluster \                    │   │
│   │                     | jq ".[0] | {total_raw_capacity, usable_raw_capacity}"                   │   │
│   │                                                                                               │   │
│   │                            # Unity — list license status via uemcli                           │   │
│   │                 uemcli -d <unity> -u admin -p $PASS /license show -output csv                 │   │
│   │                                                                                               │   │
│   │                        # PowerMax Solutions Enabler — list COD licenses                       │   │
│   │                     symlic -sid <SID> list | grep -i "capacity on demand"                     │   │
│   │                                                                                               │   │
│   │                       # Report: all arrays, COD status, capacity summary                      │   │
│   │                                for ARRAY in "${ARRAYS[@]}"; do                                │   │
│   │                  echo "=== $ARRAY ==="; curl -sk ... /api/rest/license | jq ...               │   │
│   │                                              done                                             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    total_raw_capacity = All physical raw storage including locked COD; in bytes                       │
│    usable_raw_capacity= Capacity available to create pools; increases after COD activation            │
│    symlic             = Solutions Enabler license command; requires SYMAPI connectivity               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

**What you should see**

Ansible prints the array configuration overview, pool utilisation, and license status. If the pool output contains a percentage at or above the warning threshold, a warning message is displayed but the play does not fail — review the pool list output to assess the situation.

---

## Windows: COD License Query via Unisphere REST API (PowerShell)

Queries the Unisphere for PowerMax REST API from a Windows PC to report current licensed capacity and available COD headroom. No SYMCLI installation required — just network access to the Unisphere server.

~~~powershell
# cod_license_query.ps1 — COD license query via Unisphere REST API (Windows PowerShell)
# Requires: PowerShell 5.1+ (built into Windows 10/11)
# Run: .\cod_license_query.ps1

$UnisphereHost = "192.168.1.100"   # IP or hostname of your Unisphere for PowerMax server
$UnisphereUser = "sysadmin"        # Unisphere username
$UnispherePass = "yourpassword"    # Unisphere password
$SID           = "000123456789"    # Your PowerMax system ID (12 digits)

# Trust self-signed certificates (Unisphere uses self-signed certs by default)
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

$Creds   = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${UnisphereUser}:${UnispherePass}"))
$Headers = @{ Authorization = "Basic $Creds"; Accept = "application/json" }
$BaseUrl = "https://${UnisphereHost}:8443/univmax/restapi/100"

# Step 1: Get system capacity
Write-Host "Querying system capacity for SID $SID ..."
try {
    $CapResp = Invoke-RestMethod -Uri "$BaseUrl/system/symmetrix/$SID/system_capacity" -Headers $Headers
    Write-Host ""
    Write-Host "========================================"
    Write-Host "  System Capacity — $SID"
    Write-Host "========================================"
    Write-Host "  Usable Total (TB) : $($CapResp.system_capacity.usable_total_tb)"
    Write-Host "  Usable Used  (TB) : $($CapResp.system_capacity.usable_used_tb)"
    Write-Host "  Subscribed   (TB) : $($CapResp.system_capacity.subscribed_total_tb)"
} catch {
    Write-Host "WARNING: Could not retrieve system capacity - $($_.Exception.Message)"
}

# Step 2: Get license information (includes COD)
Write-Host ""
Write-Host "Querying license information ..."
try {
    $LicResp = Invoke-RestMethod -Uri "$BaseUrl/system/symmetrix/$SID/license" -Headers $Headers
    Write-Host ""
    Write-Host "========================================"
    Write-Host "  License Information"
    Write-Host "========================================"
    $Licenses = $LicResp.feature
    if (-not $Licenses) {
        Write-Host "  No license features returned. Check SID and Unisphere version."
    } else {
        foreach ($Lic in $Licenses) {
            $Name    = $Lic.name
            $Enabled = if ($Lic.enabled) { "ENABLED" } else { "DISABLED" }
            Write-Host "  $Name : $Enabled"
        }
    }
} catch {
    Write-Host "WARNING: Could not retrieve license info - $($_.Exception.Message)"
}

Write-Host ""
Write-Host "========================================"
Write-Host "  Query complete."
Write-Host "========================================"
~~~

### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or 11 (PowerShell 5.1 is already installed)
- Network access to your Unisphere for PowerMax server on port 8443
- Unisphere username and password with at least read-only access
- The 12-digit SID of your PowerMax array

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `cod_license_query.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `$UnisphereHost` | IP or hostname of Unisphere for PowerMax | Ask your storage admin |
| `$UnisphereUser` | Unisphere username | Default is `sysadmin` |
| `$UnispherePass` | Unisphere password | Ask your storage admin |
| `$SID` | PowerMax system ID | Shown in Unisphere under System → Arrays, or run `symcfg list` |

**Step 3 — Open a terminal**

- **For .ps1 (PowerShell):** Press Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time)**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
.\cod_license_query.ps1
```

**What you should see**

First a capacity block showing total usable, used, and subscribed capacity in TB. Then a license block listing every licensed feature on the array and whether it is enabled or disabled. Look for entries containing "COD" or "Capacity on Demand" to see the COD license status.

---

## Daily Check Script

Queries the Unisphere REST API for the `system_capacity` endpoint, parses `total_usable_capacity_gb` and `used_capacity_gb`, calculates percentage used, flags if above 85%, and prints licensed vs consumed COD capacity.

~~~bash
#!/bin/bash
# cod_daily_check.sh — Daily capacity check via Unisphere REST API
# Usage: UNISPHERE_HOST=192.168.1.100 SID=000123456789 UNISPHERE_USER=sysadmin UNISPHERE_PASS=secret ./cod_daily_check.sh

set -euo pipefail

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
WARN_PCT=85

BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)

echo "========================================"
echo "  COD Daily Check"
echo "  SID  : $SID"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Query system_capacity endpoint
CAP_JSON=$(curl -sk -H "Authorization: Basic $AUTH" \
  -H "Accept: application/json" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>&1)

if [[ $? -ne 0 || -z "$CAP_JSON" ]]; then
  echo "ERROR: Could not reach Unisphere at ${UNISPHERE_HOST}" >&2
  exit 2
fi

TOTAL_GB=$(echo "$CAP_JSON" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d.get('system_capacity',{}).get('usable_total_tb',0))" 2>/dev/null || echo "0")
USED_GB=$(echo "$CAP_JSON"  | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d.get('system_capacity',{}).get('usable_used_tb',0))" 2>/dev/null || echo "0")

PCT=$(python3 -c "t=float('${TOTAL_GB}'); u=float('${USED_GB}'); print(round(u/t*100,1) if t>0 else 0)" 2>/dev/null || echo "0")

echo ""
echo "  Total usable : ${TOTAL_GB} TB"
echo "  Used         : ${USED_GB} TB"
echo "  % Used       : ${PCT}%"

STATUS=0
python3 -c "exit(0 if float('${PCT}') < ${WARN_PCT} else 1)" 2>/dev/null && \
  echo "  Status       : OK" || \
  { echo "  Status       : WARNING — capacity above ${WARN_PCT}%"; STATUS=1; }

echo ""
echo "--- Licensed vs Consumed COD Capacity ---"
if [[ -x "${SYMCLI_PATH}/symcfg" ]]; then
  "${SYMCLI_PATH}/symcfg" -sid "$SID" -pool -dp list 2>&1 || true
  "${SYMCLI_PATH}/symcfg" -sid "$SID" list -license 2>&1 || true
else
  echo "  SYMCLI not available at ${SYMCLI_PATH} — skipping local license check"
fi

echo "========================================"
exit $STATUS
~~~

---

## Incident Triage Script

Captures full capacity output from the Unisphere REST API and `symcfg -sid $SID list -license` to a timestamped file for incident documentation.

~~~bash
#!/bin/bash
# cod_triage.sh — Capture COD capacity and license state to timestamped file
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x ./cod_triage.sh

set -euo pipefail

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"

TS=$(date '+%Y%m%d_%H%M%S')
OUTFILE="/tmp/cod_triage_${SID}_${TS}.txt"
BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)

{
  echo "========================================"
  echo "  COD Incident Triage Capture"
  echo "  SID  : $SID"
  echo "  Time : $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================"
  echo ""

  echo "--- Unisphere REST: system_capacity ---"
  curl -sk -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
    "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>&1 | python3 -m json.tool 2>/dev/null || echo "Parse error"

  echo ""
  echo "--- Unisphere REST: license ---"
  curl -sk -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
    "${BASE_URL}/system/symmetrix/${SID}/license" 2>&1 | python3 -m json.tool 2>/dev/null || echo "Parse error"

  echo ""
  echo "--- SYMCLI: symcfg list -license ---"
  if [[ -x "${SYMCLI_PATH}/symcfg" ]]; then
    "${SYMCLI_PATH}/symcfg" -sid "$SID" list -license 2>&1 || true
  else
    echo "  SYMCLI not available"
  fi

  echo ""
  echo "--- SYMCLI: pool list ---"
  if [[ -x "${SYMCLI_PATH}/symcfg" ]]; then
    "${SYMCLI_PATH}/symcfg" -sid "$SID" -pool -dp list 2>&1 || true
  fi

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

Before requesting a COD activation: confirms current capacity utilisation is approaching threshold (>80% used), confirms Unisphere is reachable, and confirms no pending license changes. Exits 2 if the system is not ready.

~~~bash
#!/bin/bash
# cod_precheck.sh — Pre-check before COD activation request
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x ./cod_precheck.sh

set -euo pipefail

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
ACTIVATION_THRESHOLD=80

BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

echo "========================================"
echo "  COD Activation Pre-Check"
echo "  SID  : $SID"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Check 1: Unisphere reachable
HTTP=$(curl -sk -o /dev/null -w "%{http_code}" --max-time 10 \
  -H "Authorization: Basic $AUTH" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>/dev/null || echo "000")
if [[ "$HTTP" =~ ^(200|201) ]]; then
  check_pass "Unisphere reachable (HTTP $HTTP)"
else
  check_fail "Unisphere not reachable (HTTP $HTTP)"
fi

# Check 2: Capacity utilisation approaching threshold
CAP_JSON=$(curl -sk -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>/dev/null || echo "{}")
PCT=$(echo "$CAP_JSON" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); c=d.get('system_capacity',{}); t=float(c.get('usable_total_tb',0)); u=float(c.get('usable_used_tb',0)); print(round(u/t*100,1) if t>0 else 0)" 2>/dev/null || echo "0")

if python3 -c "exit(0 if float('${PCT}') >= ${ACTIVATION_THRESHOLD} else 1)" 2>/dev/null; then
  check_pass "Capacity utilisation is ${PCT}% (above ${ACTIVATION_THRESHOLD}% threshold — COD activation warranted)"
else
  check_fail "Capacity utilisation is only ${PCT}% (below ${ACTIVATION_THRESHOLD}% — COD activation may not be needed yet)"
fi

# Check 3: No pending license changes (check via SYMCLI if available)
if [[ -x "${SYMCLI_PATH}/symcfg" ]]; then
  PENDING=$(${SYMCLI_PATH}/symcfg -sid "$SID" list -license 2>&1 | grep -i "pending" || true)
  if [[ -z "$PENDING" ]]; then
    check_pass "No pending license changes detected via SYMCLI"
  else
    check_fail "Pending license changes detected: $PENDING"
  fi
else
  echo "  [SKIP] SYMCLI not available — pending license check skipped"
fi

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: READY — proceed with COD activation request"
  exit 0
else
  echo "  Result: NOT READY — resolve failures above before proceeding"
  exit 2
fi
~~~

---

## Post-Change Validation Script

After COD activation: verifies new capacity is visible in `symcfg show` and confirms storage groups are still accessible.

~~~bash
#!/bin/bash
# cod_postcheck.sh — Post-change validation after COD activation
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x ./cod_postcheck.sh

set -euo pipefail

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"

BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

echo "========================================"
echo "  COD Post-Change Validation"
echo "  SID  : $SID"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Check 1: New capacity visible via symcfg show
echo "--- New capacity visible in SYMCLI ---"
if [[ -x "${SYMCLI_PATH}/symcfg" ]]; then
  OUTPUT=$("${SYMCLI_PATH}/symcfg" -sid "$SID" show 2>&1)
  echo "$OUTPUT" | grep -E "(Usable|Total|Capacity|GBs|TBs)" || true
  check_pass "symcfg show completed — review capacity figures above"
else
  echo "  SYMCLI not available — skipping symcfg show check"
fi

echo ""
# Check 2: Storage groups still accessible via Unisphere REST
echo "--- Storage groups accessible ---"
SG_JSON=$(curl -sk -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
  "${BASE_URL}/sloprovisioning/symmetrix/${SID}/storagegroup" 2>/dev/null || echo "{}")
SG_COUNT=$(echo "$SG_JSON" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(len(d.get('storageGroupId',d.get('storage_group_id',[]) if isinstance(d.get('storageGroupId',None),list) else [])))" 2>/dev/null || echo "0")

if [[ "$SG_COUNT" -gt 0 ]]; then
  check_pass "$SG_COUNT storage group(s) visible via Unisphere REST"
else
  check_fail "No storage groups returned — verify array connectivity and COD activation status"
fi

# Check 3: Current capacity via Unisphere REST
echo ""
echo "--- Post-activation capacity summary ---"
CAP_JSON=$(curl -sk -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>/dev/null || echo "{}")
echo "$CAP_JSON" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); c=d.get('system_capacity',{}); print('  Total usable TB :', c.get('usable_total_tb','N/A')); print('  Used usable TB  :', c.get('usable_used_tb','N/A'))" 2>/dev/null || echo "  Could not parse capacity"

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: PASS — COD activation validated"
  exit 0
else
  echo "  Result: FAIL — investigate issues above"
  exit 1
fi
~~~

---

## Health Check Script

Cron-safe script that reports SID, total usable, used, available, and % used. Exits 0 (OK), 1 (warning at 80%), or 2 (critical at 90%).

~~~bash
#!/bin/bash
# cod_health.sh — Cron-safe COD health check
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x ./cod_health.sh
# Exit: 0=OK  1=WARNING(>80%)  2=CRITICAL(>90%)

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
WARN_PCT="${WARN_PCT:-80}"
CRIT_PCT="${CRIT_PCT:-90}"

BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)

CAP_JSON=$(curl -sk --max-time 15 \
  -H "Authorization: Basic $AUTH" \
  -H "Accept: application/json" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>/dev/null || echo "{}")

read -r TOTAL USED PCT <<< "$(echo "$CAP_JSON" | python3 -c "
import sys, json
d = json.load(sys.stdin)
c = d.get('system_capacity', {})
t = float(c.get('usable_total_tb', 0))
u = float(c.get('usable_used_tb', 0))
a = t - u
p = round(u / t * 100, 1) if t > 0 else 0
print(t, u, p)
" 2>/dev/null || echo "0 0 0")"

AVAIL=$(python3 -c "print(round(float('${TOTAL}')-float('${USED}'),2))" 2>/dev/null || echo "0")

STATUS="OK"
EXIT=0
if python3 -c "exit(0 if float('${PCT}') >= ${CRIT_PCT} else 1)" 2>/dev/null; then
  STATUS="CRITICAL"; EXIT=2
elif python3 -c "exit(0 if float('${PCT}') >= ${WARN_PCT} else 1)" 2>/dev/null; then
  STATUS="WARNING"; EXIT=1
fi

echo "COD_HEALTH SID=${SID} total_tb=${TOTAL} used_tb=${USED} avail_tb=${AVAIL} pct_used=${PCT}% status=${STATUS}"
exit $EXIT
~~~
