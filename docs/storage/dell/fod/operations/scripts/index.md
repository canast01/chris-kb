# Scripts

> Part of the [Dell Flex on Demand](../index.md) reference.

---
## Metered Usage Reporter

Queries the CloudIQ REST API to pull capacity metrics for all FOD-enrolled systems and prints a monthly usage report showing committed baseline, current consumed, and burst delta. Flags any system where consumption exceeds the committed tier.

~~~python
#!/usr/bin/env python3
# fod_usage_reporter.py — FOD metered usage report via CloudIQ REST API
# Requirements: requests
# Usage: CLOUDIQ_TOKEN=xxx ./fod_usage_reporter.py

import os
import sys
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLOUDIQ_TOKEN = os.environ.get("CLOUDIQ_TOKEN", "")
CLOUDIQ_BASE  = os.environ.get("CLOUDIQ_BASE", "https://cloudiq.dell.com/cloudiq/rest/v1")

if not CLOUDIQ_TOKEN:
    print("ERROR: CLOUDIQ_TOKEN must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()
HEADERS = {
    "Authorization": f"Bearer {CLOUDIQ_TOKEN}",
    "Accept": "application/json",
}


def api_get(path, params=None):
    resp = session.get(f"{CLOUDIQ_BASE}{path}", headers=HEADERS,
                       params=params, verify=False)
    resp.raise_for_status()
    return resp.json()


def main():
    print("=" * 70)
    print("  Dell Flex on Demand — Metered Usage Report")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # List all storage systems
    try:
        systems_data = api_get("/storage-systems")
        systems = systems_data.get("results", systems_data if isinstance(systems_data, list) else [])
    except Exception as e:
        print(f"ERROR: Could not retrieve storage systems: {e}")
        sys.exit(2)

    if not systems:
        print("No storage systems found.")
        sys.exit(0)

    burst_systems = 0
    print(f"\n{'SYSTEM':<30}  {'TYPE':<15}  {'COMMITTED':>12}  {'USED':>12}  {'BURST':>10}  STATUS")
    print("-" * 95)

    for sys_obj in systems:
        sys_id   = sys_obj.get("id", "unknown")
        sys_name = sys_obj.get("system_name", sys_obj.get("name", sys_id))
        sys_type = sys_obj.get("system_type", sys_obj.get("type", "unknown"))

        # Attempt to get capacity details
        try:
            cap = api_get(f"/storage-systems/{sys_id}/capacity")
        except Exception:
            cap = {}

        committed = float(cap.get("committed_tib", cap.get("committed_gb", 0)))
        used      = float(cap.get("used_tib",      cap.get("used_gb",      0)))
        unit      = "TiB" if "committed_tib" in cap else "GiB"
        burst     = max(0.0, used - committed)

        if burst > 0:
            status = "BURST"
            burst_systems += 1
        elif committed > 0 and (used / committed) >= 0.9:
            status = "NEAR LIMIT"
        else:
            status = "OK"

        print(f"{sys_name:<30}  {sys_type:<15}  {committed:>10.2f}{unit}  {used:>10.2f}{unit}"
              f"  {burst:>8.2f}{unit}  {status}")

    print("-" * 95)
    print(f"\nSystems currently in burst: {burst_systems}")
    sys.exit(1 if burst_systems > 0 else 0)


if __name__ == "__main__":
    main()
~~~

### How to run this script — step by step

**Before you start — what you need**
- Python 3.7 or newer installed (python.org)
- The `requests` library: run `pip install requests` in Command Prompt
- A CloudIQ API bearer token — see the CloudIQ portal to generate one, or use client credentials to get one

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `fod_usage_reporter.py` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `CLOUDIQ_TOKEN` | Your CloudIQ API bearer token | cloudiq.dell.com → Settings → API Access → generate a token |

**Step 3 — Open a terminal**

- **For .py (Python):** Open Command Prompt. Install Python first from python.org if needed.

**Step 4 — Run the script**

```bash
cd C:\Users\YourName\Desktop
set CLOUDIQ_TOKEN=eyJhbGciOiJSUzI1N...
python fod_usage_reporter.py
```

**What you should see**

A table listing each storage system with its committed tier, current usage, burst amount (how much over the committed tier), and status. Systems in burst are marked BURST, systems near the limit (90% of committed) are marked NEAR LIMIT, and healthy systems are OK. The final line shows how many systems are currently in burst.

---

## Burst Detection Script

Polls the CloudIQ API for a specific system and checks whether current usage exceeds the committed FOD baseline. Designed for cron or monitoring integration — prints a single status line and exits with an appropriate code.

~~~bash
#!/bin/bash
# fod_burst_detect.sh — Detect FOD burst consumption for a specific system via CloudIQ API
# Usage:
#   CLOUDIQ_TOKEN=xxx SYSTEM_ID=PS-001234 COMMITTED_TIB=50 ./fod_burst_detect.sh

set -euo pipefail

CLOUDIQ_TOKEN="${CLOUDIQ_TOKEN:-}"
SYSTEM_ID="${SYSTEM_ID:-}"
COMMITTED_TIB="${COMMITTED_TIB:-0}"
CLOUDIQ_BASE="${CLOUDIQ_BASE:-https://cloudiq.dell.com/cloudiq/rest/v1}"

if [[ -z "$CLOUDIQ_TOKEN" || -z "$SYSTEM_ID" ]]; then
  echo "ERROR: CLOUDIQ_TOKEN and SYSTEM_ID must be set." >&2
  exit 1
fi

# Fetch capacity for the system
RESPONSE=$(curl -s -f \
  -H "Authorization: Bearer ${CLOUDIQ_TOKEN}" \
  -H "Accept: application/json" \
  "${CLOUDIQ_BASE}/storage-systems/${SYSTEM_ID}/capacity" 2>&1)

if [[ $? -ne 0 ]]; then
  echo "UNKNOWN: CloudIQ API call failed for system ${SYSTEM_ID}"
  exit 3
fi

# Extract used_tib from JSON (requires jq)
USED_TIB=$(echo "$RESPONSE" | jq -r '.used_tib // .usedTiB // 0' 2>/dev/null || echo "0")

# Compare with bc
BURST=$(echo "$USED_TIB - $COMMITTED_TIB" | bc)
IS_BURST=$(echo "$BURST > 0" | bc)

if [[ "$IS_BURST" -eq 1 ]]; then
  echo "WARNING: System ${SYSTEM_ID} is in burst. Used=${USED_TIB} TiB, Committed=${COMMITTED_TIB} TiB, Burst=${BURST} TiB"
  exit 1
else
  echo "OK: System ${SYSTEM_ID} within committed baseline. Used=${USED_TIB} TiB, Committed=${COMMITTED_TIB} TiB"
  exit 0
fi
~~~

### How to run this script — step by step

**Before you start — what you need**
- A Linux/macOS computer or Windows with Git Bash installed
- `curl` and `jq` installed (both available in Git Bash; install jq from https://stedolan.github.io/jq/)
- A CloudIQ bearer token and the specific System ID you want to check

**Step 1 — Save the file**

1. Open **Notepad** or Git Bash editor
2. Copy the entire code block above
3. Save it as `fod_burst_detect.sh` on your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `CLOUDIQ_TOKEN` | CloudIQ bearer token | cloudiq.dell.com → Settings → API Access |
| `SYSTEM_ID` | The system ID to check | Found in the CloudIQ portal under Storage Systems — look for the `id` field |
| `COMMITTED_TIB` | Your committed FOD tier in TiB | Check your FOD contract or CloudIQ capacity page |

**Step 3 — Open a terminal**

- **For .sh (Bash):** Install Git for Windows (gitforwindows.org) and open Git Bash.

**Step 4 — Run the script**

```bash
cd ~/Desktop
chmod +x fod_burst_detect.sh
export CLOUDIQ_TOKEN=eyJhbGciOiJSUzI1N...
export SYSTEM_ID=PS-001234
export COMMITTED_TIB=50
./fod_burst_detect.sh
```

**What you should see**

A single line: either `OK: System PS-001234 within committed baseline. Used=45.3 TiB, Committed=50 TiB` or `WARNING: System PS-001234 is in burst.` with the overage shown. Exit code 0 means OK, exit code 1 means burst.

---

## Ansible FOD Audit Playbook

Playbook targeting localhost that calls the CloudIQ REST API to list all storage systems and their capacity, prints a summary, and warns if any system shows burst consumption.

~~~yaml
---
# fod_audit.yml — Ansible FOD usage audit playbook via CloudIQ REST API
# Usage: CLOUDIQ_TOKEN=xxx ansible-playbook fod_audit.yml

- name: Dell Flex on Demand Audit
  hosts: localhost
  gather_facts: false
  vars:
    cloudiq_base: "https://cloudiq.dell.com/cloudiq/rest/v1"
    cloudiq_token: "{{ lookup('env', 'CLOUDIQ_TOKEN') }}"

  tasks:
    - name: List all storage systems from CloudIQ
      ansible.builtin.uri:
        url: "{{ cloudiq_base }}/storage-systems"
        method: GET
        headers:
          Authorization: "Bearer {{ cloudiq_token }}"
        validate_certs: false
        return_content: true
      register: systems_resp

    - name: Show storage systems
      ansible.builtin.debug:
        msg: "{{ systems_resp.json }}"

    - name: Get capacity for each system
      ansible.builtin.uri:
        url: "{{ cloudiq_base }}/storage-systems/{{ item.id }}/capacity"
        method: GET
        headers:
          Authorization: "Bearer {{ cloudiq_token }}"
        validate_certs: false
        return_content: true
      loop: "{{ systems_resp.json.results | default([]) }}"
      loop_control:
        label: "{{ item.system_name | default(item.id) }}"
      register: capacity_results
      ignore_errors: true

    - name: Show capacity per system
      ansible.builtin.debug:
        msg: >
          System: {{ item.item.system_name | default(item.item.id) }}
          Capacity: {{ item.json | default({}) }}
      loop: "{{ capacity_results.results }}"
      loop_control:
        label: "{{ item.item.system_name | default(item.item.id) }}"

    - name: Warn if any system shows burst indicators
      ansible.builtin.debug:
        msg: >
          NOTICE: Review capacity results above for any system where used_tib
          exceeds committed_tib — those systems are incurring FOD burst charges.
~~~

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on a Linux/macOS control node (or WSL on Windows)
- A CloudIQ bearer token set as an environment variable

**Step 1 — Save the file**

1. Copy the code block above
2. Save it as `fod_audit.yml` in your Ansible working directory

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `CLOUDIQ_TOKEN` | Your CloudIQ bearer token | cloudiq.dell.com → Settings → API Access |

**Step 3 — Open a terminal**

Open a terminal on your Ansible control node.

**Step 4 — Run the script**

```bash
export CLOUDIQ_TOKEN=eyJhbGciOiJSUzI1N...
ansible-playbook fod_audit.yml
```

**What you should see**

Ansible lists all storage systems from CloudIQ and then fetches capacity details for each one. The final task prints a notice reminding you to check any system where `used_tib` is greater than `committed_tib` — those systems are in FOD burst and may incur additional charges.

---

## Windows: FOD License Status via Unisphere REST API (PowerShell)

Queries the Unisphere for PowerMax REST API to show array information and license details including FOD status — all from a PowerShell window on Windows.

~~~powershell
# fod_license_status.ps1 — FOD license status via Unisphere REST API (Windows PowerShell)
# Requires: PowerShell 5.1+ (built into Windows 10/11)
# Run: .\fod_license_status.ps1

$UnisphereHost = "192.168.1.100"   # IP or hostname of your Unisphere for PowerMax server
$UnisphereUser = "sysadmin"        # Unisphere username
$UnispherePass = "yourpassword"    # Unisphere password
$SID           = "000123456789"    # Your PowerMax system ID (12 digits)

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

$Creds   = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${UnisphereUser}:${UnispherePass}"))
$Headers = @{ Authorization = "Basic $Creds"; Accept = "application/json" }
$BaseUrl = "https://${UnisphereHost}:8443/univmax/restapi/100"

# Step 1: Get array info (model, total capacity)
Write-Host "Querying array info for SID $SID ..."
try {
    $ArrayResp = Invoke-RestMethod -Uri "$BaseUrl/system/symmetrix/$SID" -Headers $Headers
    $Model    = $ArrayResp.symmetrix.model
    $UcapTb   = $ArrayResp.symmetrix.system_capacity.usable_total_tb
    $UusedTb  = $ArrayResp.symmetrix.system_capacity.usable_used_tb

    Write-Host ""
    Write-Host "========================================"
    Write-Host "  Array Information"
    Write-Host "========================================"
    Write-Host "  SID             : $SID"
    Write-Host "  Model           : $Model"
    Write-Host "  Total Usable TB : $UcapTb"
    Write-Host "  Used Usable TB  : $UusedTb"
} catch {
    Write-Host "WARNING: Could not retrieve array info - $($_.Exception.Message)"
}

# Step 2: Get license details (FOD status)
Write-Host ""
Write-Host "Querying license details ..."
try {
    $LicResp = Invoke-RestMethod -Uri "$BaseUrl/system/symmetrix/$SID/license" -Headers $Headers
    Write-Host ""
    Write-Host "========================================"
    Write-Host "  License Features (including FOD)"
    Write-Host "========================================"
    $Features = $LicResp.feature
    if (-not $Features) {
        Write-Host "  No license features returned."
    } else {
        foreach ($Feature in $Features) {
            $Name    = $Feature.name
            $Enabled = if ($Feature.enabled) { "ENABLED" } else { "DISABLED" }
            $IsFod   = if ($Name -match "Flex|FOD|on.Demand") { "  <-- FOD related" } else { "" }
            Write-Host "  $Name : $Enabled$IsFod"
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
- Windows 10 or 11 (PowerShell 5.1 is already built in)
- Network access to your Unisphere for PowerMax server on port 8443
- Unisphere username and password with at least read-only access
- The 12-digit SID of your PowerMax array

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `fod_license_status.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `$UnisphereHost` | IP or hostname of Unisphere for PowerMax | Ask your storage admin |
| `$UnisphereUser` | Unisphere username | Default is `sysadmin` |
| `$UnispherePass` | Unisphere password | Ask your storage admin |
| `$SID` | PowerMax system ID | Shown in Unisphere under System → Arrays |

**Step 3 — Open a terminal**

- **For .ps1 (PowerShell):** Press Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time)**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
.\fod_license_status.ps1
```

**What you should see**

An array information block showing model, total usable capacity, and used capacity. Then a license features list — each feature shows ENABLED or DISABLED. Features related to Flex on Demand are marked with `<-- FOD related` to make them easy to spot.

---

## Daily Check Script

Queries Unisphere REST for current capacity, calculates burst consumption, and flags if approaching the burst ceiling (>70% of burst budget used).

~~~bash
#!/bin/bash
# fod_daily_check.sh — Daily FOD capacity and burst check via Unisphere REST API
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x ./fod_daily_check.sh
# Exit: 0=OK  1=approaching burst ceiling  2=error

set -euo pipefail

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
BURST_WARN_PCT="${BURST_WARN_PCT:-70}"

BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)

echo "========================================"
echo "  FOD Daily Check"
echo "  SID  : $SID"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

CAP_JSON=$(curl -sk --max-time 15 \
  -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>/dev/null || echo "{}")

if [[ -z "$CAP_JSON" || "$CAP_JSON" == "{}" ]]; then
  echo "ERROR: Could not retrieve capacity from Unisphere at ${UNISPHERE_HOST}" >&2
  exit 2
fi

python3 -c "
import sys, json
d = json.load(sys.stdin)
c = d.get('system_capacity', {})
total    = float(c.get('usable_total_tb', 0))
used     = float(c.get('usable_used_tb', 0))
subscribed = float(c.get('subscribed_total_tb', 0))

burst = max(0.0, used - total)
burst_budget = max(0.0, subscribed - total)
burst_pct = round(burst / burst_budget * 100, 1) if burst_budget > 0 else 0.0

print(f'  Total usable    : {total} TB')
print(f'  Used            : {used} TB')
print(f'  Subscribed      : {subscribed} TB')
print(f'  Burst consumed  : {burst:.2f} TB')
print(f'  Burst budget    : {burst_budget:.2f} TB')
print(f'  Burst % used    : {burst_pct}%')

warn = float('${BURST_WARN_PCT}')
if burst_pct >= warn:
    print(f'  Status          : WARNING — burst ceiling {burst_pct}% used (threshold {warn}%)')
    sys.exit(1)
else:
    print(f'  Status          : OK')
    sys.exit(0)
" <<< "$CAP_JSON"
~~~

---

## Incident Triage Script

Captures FOD status, full license output, and capacity allocations to a timestamped file.

~~~bash
#!/bin/bash
# fod_triage.sh — Capture FOD status and capacity state to timestamped file
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x ./fod_triage.sh

set -euo pipefail

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"

TS=$(date '+%Y%m%d_%H%M%S')
OUTFILE="/tmp/fod_triage_${SID}_${TS}.txt"
BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)

{
  echo "========================================"
  echo "  FOD Incident Triage Capture"
  echo "  SID  : $SID"
  echo "  Time : $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================"

  for ENDPOINT in system_capacity license; do
    echo ""
    echo "--- Unisphere REST: ${ENDPOINT} ---"
    curl -sk -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
      "${BASE_URL}/system/symmetrix/${SID}/${ENDPOINT}" 2>&1 | python3 -m json.tool 2>/dev/null || echo "Parse error"
  done

  echo ""
  echo "--- Unisphere REST: capacity_allocations ---"
  curl -sk -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
    "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>&1 | python3 -m json.tool 2>/dev/null || echo "Parse error"

  echo ""
  echo "--- Symmetrix info (SYMCLI if available) ---"
  SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
  if [[ -x "${SYMCLI_PATH}/symcfg" ]]; then
    "${SYMCLI_PATH}/symcfg" -sid "$SID" show 2>&1 || true
    "${SYMCLI_PATH}/symcfg" -sid "$SID" list -license 2>&1 || true
  else
    echo "  SYMCLI not available"
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

Before a planned workload increase: confirms burst headroom is available, confirms the FOD billing cycle is not within the last 5 days (to avoid double-burst charges), and confirms Unisphere is reachable. Exits 2 if not ready.

~~~bash
#!/bin/bash
# fod_precheck.sh — Pre-check before planned workload increase under FOD
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x BILLING_DAY_OF_MONTH=1 ./fod_precheck.sh

set -euo pipefail

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
BILLING_DAY_OF_MONTH="${BILLING_DAY_OF_MONTH:-1}"   # Day of month billing cycle resets
BURST_HEADROOM_WARN_PCT=90  # flag if burst budget is >90% consumed

BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

echo "========================================"
echo "  FOD Pre-Change Check"
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

# Check 2: Burst headroom available
CAP_JSON=$(curl -sk -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>/dev/null || echo "{}")
python3 -c "
import sys, json
d = json.load(sys.stdin)
c = d.get('system_capacity', {})
total = float(c.get('usable_total_tb', 0))
used  = float(c.get('usable_used_tb', 0))
subscribed = float(c.get('subscribed_total_tb', 0))
burst = max(0.0, used - total)
burst_budget = max(0.0, subscribed - total)
burst_pct = round(burst / burst_budget * 100, 1) if burst_budget > 0 else 0.0
warn = float('${BURST_HEADROOM_WARN_PCT}')
if burst_pct >= warn:
    print(f'  [FAIL] Burst budget {burst_pct}% consumed — insufficient headroom for workload increase')
    sys.exit(1)
else:
    print(f'  [PASS] Burst headroom available ({burst_pct}% of burst budget consumed)')
    sys.exit(0)
" <<< "$CAP_JSON" || FAIL=1

# Check 3: Not within last 5 days of billing period
TODAY=$(date '+%d')
DAYS_IN_MONTH=$(date -d "$(date '+%Y-%m-01') +1 month -1 day" '+%d' 2>/dev/null || \
                python3 -c "import calendar,datetime; d=datetime.date.today(); print(calendar.monthrange(d.year,d.month)[1])")
DAYS_UNTIL_RESET=$(( (BILLING_DAY_OF_MONTH - 10#$TODAY + DAYS_IN_MONTH) % DAYS_IN_MONTH ))
if [[ "$DAYS_UNTIL_RESET" -le 5 && "$DAYS_UNTIL_RESET" -ge 0 ]]; then
  check_fail "Within 5 days of billing period end (${DAYS_UNTIL_RESET} days) — risk of double-burst charges"
else
  check_pass "Not within last 5 days of billing period (${DAYS_UNTIL_RESET} days until cycle reset)"
fi

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: READY — proceed with planned workload increase"
  exit 0
else
  echo "  Result: NOT READY — resolve failures above before proceeding"
  exit 2
fi
~~~

---

## Post-Change Validation Script

After a workload change: confirms FOD consumption has returned to baseline within expected range, checks for unexpected burst activation, and generates a usage report.

~~~bash
#!/bin/bash
# fod_postcheck.sh — Post-change validation after FOD workload change
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x BASELINE_USED_TB=x ./fod_postcheck.sh

set -euo pipefail

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
BASELINE_USED_TB="${BASELINE_USED_TB:-0}"  # Set to pre-change used TB value

BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

echo "========================================"
echo "  FOD Post-Change Validation"
echo "  SID      : $SID"
echo "  Baseline : ${BASELINE_USED_TB} TB used (pre-change)"
echo "  Date     : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

CAP_JSON=$(curl -sk --max-time 15 \
  -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>/dev/null || echo "{}")

python3 -c "
import sys, json
d = json.load(sys.stdin)
c = d.get('system_capacity', {})
total = float(c.get('usable_total_tb', 0))
used  = float(c.get('usable_used_tb', 0))
subscribed = float(c.get('subscribed_total_tb', 0))
burst = max(0.0, used - total)
burst_budget = max(0.0, subscribed - total)
burst_pct = round(burst / burst_budget * 100, 1) if burst_budget > 0 else 0.0
baseline = float('${BASELINE_USED_TB}')
delta = round(used - baseline, 2)

print(f'  Total usable   : {total} TB')
print(f'  Used (current) : {used} TB')
print(f'  Delta from baseline: {delta:+.2f} TB')
print(f'  Burst active   : {\"YES\" if burst > 0 else \"NO\"} ({burst:.2f} TB burst)')
print(f'  Burst %        : {burst_pct}%')
print()

fail = False
if burst > 0:
    print('  [WARN] Burst is currently active — monitor for return to baseline')
    fail = True
else:
    print('  [PASS] No burst activation detected')

if delta > 5.0:
    print(f'  [WARN] Usage increased by {delta} TB vs baseline — verify this is expected')
else:
    print(f'  [PASS] Usage delta ({delta:+.2f} TB) within expected range')

sys.exit(1 if fail else 0)
" <<< "$CAP_JSON" || FAIL=1

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: PASS — FOD post-change validation successful"
  exit 0
else
  echo "  Result: WARN — review items above and re-check after 1h"
  exit 1
fi
~~~

---

## Health Check Script

Cron-safe script reporting current capacity allocation, burst status (active/inactive), percentage of burst budget consumed, and days remaining in the billing period. Exits 0 (OK), 1 (warning), or 2 (critical).

~~~bash
#!/bin/bash
# fod_health.sh — Cron-safe FOD health check
# Usage: UNISPHERE_HOST=x SID=x UNISPHERE_USER=x UNISPHERE_PASS=x ./fod_health.sh
# Exit: 0=OK  1=WARNING  2=CRITICAL

UNISPHERE_HOST="${UNISPHERE_HOST:?Set UNISPHERE_HOST}"
SID="${SID:?Set SID}"
UNISPHERE_USER="${UNISPHERE_USER:?Set UNISPHERE_USER}"
UNISPHERE_PASS="${UNISPHERE_PASS:?Set UNISPHERE_PASS}"
BILLING_DAY_OF_MONTH="${BILLING_DAY_OF_MONTH:-1}"
WARN_BURST_PCT="${WARN_BURST_PCT:-70}"
CRIT_BURST_PCT="${CRIT_BURST_PCT:-90}"

BASE_URL="https://${UNISPHERE_HOST}:8443/univmax/restapi/100"
AUTH=$(printf '%s:%s' "$UNISPHERE_USER" "$UNISPHERE_PASS" | base64)

CAP_JSON=$(curl -sk --max-time 15 \
  -H "Authorization: Basic $AUTH" -H "Accept: application/json" \
  "${BASE_URL}/system/symmetrix/${SID}/system_capacity" 2>/dev/null || echo "{}")

TODAY=$(date '+%d')
DAYS_IN_MONTH=$(python3 -c "import calendar,datetime; d=datetime.date.today(); print(calendar.monthrange(d.year,d.month)[1])" 2>/dev/null || echo "30")
DAYS_LEFT=$(( (BILLING_DAY_OF_MONTH - 10#$TODAY + DAYS_IN_MONTH) % DAYS_IN_MONTH ))

python3 -c "
import sys, json
d = json.load(sys.stdin)
c = d.get('system_capacity', {})
total = float(c.get('usable_total_tb', 0))
used  = float(c.get('usable_used_tb', 0))
subscribed = float(c.get('subscribed_total_tb', 0))
burst = max(0.0, used - total)
burst_budget = max(0.0, subscribed - total)
burst_pct = round(burst / burst_budget * 100, 1) if burst_budget > 0 else 0.0
burst_active = 'YES' if burst > 0 else 'NO'
warn = float('${WARN_BURST_PCT}')
crit = float('${CRIT_BURST_PCT}')
days_left = int('${DAYS_LEFT}')

print(f'FOD_HEALTH SID=${SID} total_tb={total} used_tb={used} subscribed_tb={subscribed} burst_active={burst_active} burst_pct={burst_pct}% billing_days_remaining={days_left}')

if burst_pct >= crit:
    sys.exit(2)
elif burst_pct >= warn:
    sys.exit(1)
else:
    sys.exit(0)
" <<< "$CAP_JSON"
~~~
