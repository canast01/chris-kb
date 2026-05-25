# Dell Apex STaaS — Scripts

> Part of the [APEX Storage as a Service](../index.md) reference.

---
## Subscription Capacity Monitor

Authenticates to the APEX REST API, retrieves all subscriptions, and checks committed vs. consumed capacity. Warns at 80% and goes critical at 90% of the committed tier.

~~~python
#!/usr/bin/env python3
# apex_capacity_monitor.py — APEX STaaS subscription capacity monitor
# Requirements: requests
# Usage:
#   APEX_CLIENT_ID=xxx APEX_CLIENT_SECRET=yyy ./apex_capacity_monitor.py

import os
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

APEX_CLIENT_ID     = os.environ.get("APEX_CLIENT_ID", "")
APEX_CLIENT_SECRET = os.environ.get("APEX_CLIENT_SECRET", "")
APEX_BASE          = os.environ.get("APEX_BASE", "https://console.cloudapex.dell.com/api/v1")
WARN_PCT           = float(os.environ.get("WARN_PCT", "80"))
CRIT_PCT           = float(os.environ.get("CRIT_PCT", "90"))

if not APEX_CLIENT_ID or not APEX_CLIENT_SECRET:
    print("ERROR: APEX_CLIENT_ID and APEX_CLIENT_SECRET must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()


def get_token():
    resp = session.post(
        f"{APEX_BASE}/auth/token",
        json={"client_id": APEX_CLIENT_ID, "client_secret": APEX_CLIENT_SECRET},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def api_get(token, path):
    resp = session.get(
        f"{APEX_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    exit_code = 0

    print("=" * 60)
    print("  APEX STaaS Subscription Capacity Monitor")
    print("=" * 60)

    try:
        token = get_token()
    except Exception as e:
        print(f"ERROR: Authentication failed: {e}")
        sys.exit(2)

    # List subscriptions
    try:
        subs_data = api_get(token, "/subscriptions")
        subscriptions = subs_data.get("subscriptions", subs_data if isinstance(subs_data, list) else [])
    except Exception as e:
        print(f"ERROR: Could not list subscriptions: {e}")
        sys.exit(2)

    if not subscriptions:
        print("No subscriptions found.")
        sys.exit(0)

    print(f"\n{'SUBSCRIPTION':<35}  {'COMMITTED':>12}  {'CONSUMED':>12}  {'PCT':>6}  STATUS")
    print("-" * 85)

    for sub in subscriptions:
        sub_id   = sub.get("id", "unknown")
        sub_name = sub.get("name", sub_id)

        # Fetch capacity for this subscription
        try:
            cap = api_get(token, f"/subscriptions/{sub_id}/capacity")
        except Exception as e:
            print(f"{sub_name:<35}  ERROR: {e}")
            continue

        committed_tib = float(cap.get("committed_tib", cap.get("committedTiB", 0)))
        consumed_tib  = float(cap.get("consumed_tib",  cap.get("consumedTiB",  0)))
        pct = (consumed_tib / committed_tib * 100) if committed_tib > 0 else 0.0

        if pct >= CRIT_PCT:
            status = "CRITICAL"
            exit_code = max(exit_code, 2)
        elif pct >= WARN_PCT:
            status = "WARNING"
            exit_code = max(exit_code, 1)
        else:
            status = "OK"

        print(f"{sub_name:<35}  {committed_tib:>10.2f}T  {consumed_tib:>10.2f}T  {pct:>5.1f}%  {status}")

    print("-" * 85)
    labels = {0: "OK", 1: "WARNING", 2: "CRITICAL"}
    print(f"\nOverall: {labels.get(exit_code, 'UNKNOWN')}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

### How to run this script — step by step

**Before you start — what you need**
- Python 3.7 or newer installed (python.org)
- The `requests` library: run `pip install requests` in Command Prompt
- An APEX API client ID and client secret from the APEX Console

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `apex_capacity_monitor.py` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `APEX_CLIENT_ID` | Your APEX API client ID | Log into console.cloudapex.dell.com → Settings → API Credentials |
| `APEX_CLIENT_SECRET` | Your APEX API client secret | Shown once when credentials are created |
| `WARN_PCT` | Capacity % threshold for WARNING | Default is `80` |
| `CRIT_PCT` | Capacity % threshold for CRITICAL | Default is `90` |

**Step 3 — Open a terminal**

- **For .py (Python):** Open Command Prompt. Install Python first from python.org if needed.

**Step 4 — Run the script**

```bash
cd C:\Users\YourName\Desktop
set APEX_CLIENT_ID=your-client-id
set APEX_CLIENT_SECRET=your-client-secret
python apex_capacity_monitor.py
```

**What you should see**

A table listing each APEX subscription with committed capacity, consumed capacity, percentage used, and status (OK/WARNING/CRITICAL). The final line shows overall status. The script exits non-zero if any subscription is in WARNING or CRITICAL state.

---

## Active Alert Report

Polls the APEX REST API for all active alerts across subscriptions and prints a formatted report. Exits non-zero if any CRITICAL severity alerts are found.

~~~python
#!/usr/bin/env python3
# apex_alert_report.py — Retrieve and report active APEX STaaS alerts
# Requirements: requests
# Usage: APEX_CLIENT_ID=xxx APEX_CLIENT_SECRET=yyy ./apex_alert_report.py

import os
import sys
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

APEX_CLIENT_ID     = os.environ.get("APEX_CLIENT_ID", "")
APEX_CLIENT_SECRET = os.environ.get("APEX_CLIENT_SECRET", "")
APEX_BASE          = os.environ.get("APEX_BASE", "https://console.cloudapex.dell.com/api/v1")

if not APEX_CLIENT_ID or not APEX_CLIENT_SECRET:
    print("ERROR: APEX_CLIENT_ID and APEX_CLIENT_SECRET must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()


def get_token():
    resp = session.post(
        f"{APEX_BASE}/auth/token",
        json={"client_id": APEX_CLIENT_ID, "client_secret": APEX_CLIENT_SECRET},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def api_get(token, path):
    resp = session.get(
        f"{APEX_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    exit_code = 0
    token = get_token()

    print("=" * 65)
    print("  APEX STaaS Active Alert Report")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    try:
        data = api_get(token, "/alerts?status=active")
        alerts = data.get("alerts", data if isinstance(data, list) else [])
    except Exception as e:
        print(f"ERROR fetching alerts: {e}")
        sys.exit(2)

    if not alerts:
        print("\nNo active alerts.")
        sys.exit(0)

    print(f"\n{'SEVERITY':<12}  {'RESOURCE':<30}  {'DESCRIPTION'}")
    print("-" * 80)

    for alert in alerts:
        severity = alert.get("severity", "UNKNOWN").upper()
        resource = alert.get("resource_name", alert.get("resourceName", "unknown"))
        desc     = alert.get("description", alert.get("message", "no description"))

        print(f"{severity:<12}  {resource:<30}  {desc}")

        if severity in ("CRITICAL", "ERROR"):
            exit_code = max(exit_code, 2)
        elif severity == "WARNING":
            exit_code = max(exit_code, 1)

    print("-" * 80)
    print(f"\nTotal active alerts: {len(alerts)}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

### How to run this script — step by step

**Before you start — what you need**
- Python 3.7 or newer installed (python.org)
- The `requests` library: run `pip install requests` in Command Prompt
- An APEX API client ID and secret

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `apex_alert_report.py` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `APEX_CLIENT_ID` | Your APEX API client ID | console.cloudapex.dell.com → Settings → API Credentials |
| `APEX_CLIENT_SECRET` | Your APEX API client secret | Shown once when credentials are created |

**Step 3 — Open a terminal**

- **For .py (Python):** Open Command Prompt. Install Python first from python.org if needed.

**Step 4 — Run the script**

```bash
cd C:\Users\YourName\Desktop
set APEX_CLIENT_ID=your-client-id
set APEX_CLIENT_SECRET=your-client-secret
python apex_alert_report.py
```

**What you should see**

A table with severity, resource name, and description for each active alert. The final line shows total active alert count. The script exits with a non-zero code if any CRITICAL or ERROR alerts are present.

---

## Ansible APEX Health Playbook

Playbook that calls the APEX REST API via the `uri` module to check subscription capacity and active alerts, printing a summary and failing the play if capacity is critical or critical alerts exist.

~~~yaml
---
# apex_health.yml — Ansible health check playbook for Dell APEX STaaS
# Required vars: apex_client_id, apex_client_secret
# Usage: ansible-playbook apex_health.yml

- name: Dell APEX STaaS Health Check
  hosts: localhost
  gather_facts: false
  vars:
    apex_base: "https://console.cloudapex.dell.com/api/v1"
    apex_client_id: "{{ lookup('env', 'APEX_CLIENT_ID') }}"
    apex_client_secret: "{{ lookup('env', 'APEX_CLIENT_SECRET') }}"
    warn_pct: 80
    crit_pct: 90

  tasks:
    - name: Authenticate to APEX API
      ansible.builtin.uri:
        url: "{{ apex_base }}/auth/token"
        method: POST
        body_format: json
        body:
          client_id: "{{ apex_client_id }}"
          client_secret: "{{ apex_client_secret }}"
        validate_certs: false
        return_content: true
      register: auth_resp
      no_log: true

    - name: Set bearer token
      ansible.builtin.set_fact:
        apex_token: "{{ auth_resp.json.access_token }}"
      no_log: true

    - name: List subscriptions
      ansible.builtin.uri:
        url: "{{ apex_base }}/subscriptions"
        method: GET
        headers:
          Authorization: "Bearer {{ apex_token }}"
        validate_certs: false
        return_content: true
      register: subs_resp

    - name: Show subscriptions
      ansible.builtin.debug:
        msg: "{{ subs_resp.json }}"

    - name: Get active alerts
      ansible.builtin.uri:
        url: "{{ apex_base }}/alerts?status=active"
        method: GET
        headers:
          Authorization: "Bearer {{ apex_token }}"
        validate_certs: false
        return_content: true
      register: alerts_resp

    - name: Show active alerts
      ansible.builtin.debug:
        msg: "{{ alerts_resp.json }}"

    - name: Fail if critical alerts present
      ansible.builtin.fail:
        msg: "Critical APEX alerts detected. Investigate via APEX Console."
      when: >
        alerts_resp.json is defined and
        (alerts_resp.json.alerts | default([]) |
         selectattr('severity', 'equalto', 'CRITICAL') | list | length) > 0
~~~

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on a Linux/macOS control node (or WSL on Windows)
- An APEX API client ID and secret set as environment variables

**Step 1 — Save the file**

1. Copy the code block above
2. Save it as `apex_health.yml` in your Ansible working directory

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `APEX_CLIENT_ID` | Your APEX API client ID | console.cloudapex.dell.com → Settings → API Credentials |
| `APEX_CLIENT_SECRET` | Your APEX API client secret | Shown once when credentials are created |

**Step 3 — Open a terminal**

Open a terminal on your Ansible control node.

**Step 4 — Run the script**

```bash
export APEX_CLIENT_ID=your-client-id
export APEX_CLIENT_SECRET=your-client-secret
ansible-playbook apex_health.yml
```

**What you should see**

Ansible authenticates to the APEX API, lists all subscriptions, and retrieves active alerts. If any CRITICAL alerts are found the play fails with a message to investigate via the APEX Console.

---

## Daily Check Script

Authenticates to the Dell APEX REST API with OAuth2, lists all APEX systems, checks `health_score` for each system, flags any below 80, checks contracted vs consumed capacity, and flags if above 85% consumed.

~~~bash
#!/bin/bash
# apex_daily_check.sh — Daily APEX system health and capacity check
# Usage: APEX_CLIENT_ID=x APEX_CLIENT_SECRET=x ./apex_daily_check.sh
# Exit: 0=OK  1=WARNING  2=error/critical

set -euo pipefail

APEX_CLIENT_ID="${APEX_CLIENT_ID:?Set APEX_CLIENT_ID}"
APEX_CLIENT_SECRET="${APEX_CLIENT_SECRET:?Set APEX_CLIENT_SECRET}"
TOKEN_URL="${TOKEN_URL:-https://api.dell.com/auth/oauth/v2/token}"
API_BASE="${API_BASE:-https://api.dell.com/cloudiq/rest/v1}"
HEALTH_WARN=80
CAP_WARN_PCT=85

FAIL=0
check_pass() { echo "  [PASS] $*"; }
check_warn() { echo "  [WARN] $*"; FAIL=1; }

echo "========================================"
echo "  APEX Daily Check"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Authenticate
TOKEN=$(curl -s --max-time 15 -X POST "$TOKEN_URL" \
  -d "grant_type=client_credentials&client_id=${APEX_CLIENT_ID}&client_secret=${APEX_CLIENT_SECRET}" \
  -H "Content-Type: application/x-www-form-urlencoded" 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: Authentication failed — check APEX_CLIENT_ID and APEX_CLIENT_SECRET" >&2
  exit 2
fi

# List systems
SYSTEMS=$(curl -s --max-time 15 \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "${API_BASE}/systems" 2>/dev/null || echo "{}")

echo "--- System Health Scores ---"
python3 -c "
import sys, json
data = json.load(sys.stdin)
systems = data.get('results', data if isinstance(data, list) else [])
fail = False
for s in systems:
    name  = s.get('system_name', s.get('name', 'unknown'))
    sid   = s.get('id', '')
    score = float(s.get('health_score', s.get('healthScore', 100)))
    warn  = float('${HEALTH_WARN}')
    flag  = '  <<< BELOW THRESHOLD' if score < warn else ''
    if score < warn:
        fail = True
    print(f'  {name:<35} health_score={score}{flag}')
if fail:
    sys.exit(1)
" <<< "$SYSTEMS" || FAIL=1

echo ""
echo "--- Capacity vs Contracted ---"
python3 -c "
import sys, json, subprocess, os
systems = json.load(sys.stdin).get('results', [])
token = '${TOKEN}'
api = '${API_BASE}'
warn_pct = float('${CAP_WARN_PCT}')
fail = False
for s in systems:
    name = s.get('system_name', s.get('name', 'unknown'))
    sid  = s.get('id','')
    import urllib.request
    req = urllib.request.Request(f'{api}/systems/{sid}/capacity',
        headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            cap = json.load(r)
    except Exception:
        cap = {}
    committed = float(cap.get('committed_tib', cap.get('committed_gb', 0)))
    consumed  = float(cap.get('used_tib',      cap.get('used_gb',      0)))
    pct = round(consumed / committed * 100, 1) if committed > 0 else 0.0
    flag = '  <<< ABOVE THRESHOLD' if pct >= warn_pct else ''
    if pct >= warn_pct:
        fail = True
    print(f'  {name:<35} committed={committed:.1f}T consumed={consumed:.1f}T ({pct}%){flag}')
sys.exit(1 if fail else 0)
" <<< "$SYSTEMS" || FAIL=1

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: OK"
  exit 0
else
  echo "  Result: WARNING — review items above"
  exit 1
fi
~~~

---

## Incident Triage Script

Captures all APEX system details, capacity status, active alerts, and recent events to a timestamped file.

~~~bash
#!/bin/bash
# apex_triage.sh — Capture APEX system state for incident triage
# Usage: APEX_CLIENT_ID=x APEX_CLIENT_SECRET=x ./apex_triage.sh

set -euo pipefail

APEX_CLIENT_ID="${APEX_CLIENT_ID:?Set APEX_CLIENT_ID}"
APEX_CLIENT_SECRET="${APEX_CLIENT_SECRET:?Set APEX_CLIENT_SECRET}"
TOKEN_URL="${TOKEN_URL:-https://api.dell.com/auth/oauth/v2/token}"
API_BASE="${API_BASE:-https://api.dell.com/cloudiq/rest/v1}"

TS=$(date '+%Y%m%d_%H%M%S')
OUTFILE="/tmp/apex_triage_${TS}.txt"

TOKEN=$(curl -s --max-time 15 -X POST "$TOKEN_URL" \
  -d "grant_type=client_credentials&client_id=${APEX_CLIENT_ID}&client_secret=${APEX_CLIENT_SECRET}" \
  -H "Content-Type: application/x-www-form-urlencoded" 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: Authentication failed" >&2; exit 2
fi

apex_get() {
  curl -s --max-time 15 \
    -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
    "${API_BASE}/$1" 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "{}"
}

{
  echo "========================================"
  echo "  APEX Incident Triage Capture"
  echo "  Time : $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================"

  echo ""
  echo "--- All APEX Systems ---"
  apex_get "systems"

  echo ""
  echo "--- Active Alerts ---"
  apex_get "alerts?status=active"

  echo ""
  echo "--- Recent Events ---"
  apex_get "events?limit=50"

  # Per-system capacity
  SYSTEMS_JSON=$(curl -s --max-time 15 \
    -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
    "${API_BASE}/systems" 2>/dev/null || echo "{}")
  python3 -c "
import sys, json, urllib.request
systems = json.load(sys.stdin).get('results', [])
for s in systems:
    sid = s.get('id','')
    name = s.get('system_name', s.get('name', sid))
    print(f'\\n--- Capacity: {name} ---')
    req = urllib.request.Request(f'${API_BASE}/systems/{sid}/capacity',
        headers={'Authorization': 'Bearer ${TOKEN}', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(json.dumps(json.load(r), indent=2))
    except Exception as e:
        print(f'Error: {e}')
" <<< "$SYSTEMS_JSON"

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

Before a significant workload increase: confirms APEX system health is above 80, contracted capacity headroom is above 20%, no active CRITICAL alerts exist, and Dell maintenance is not scheduled in the next 4 hours. Exits 2 on failure.

~~~bash
#!/bin/bash
# apex_precheck.sh — Pre-check before significant APEX workload increase
# Usage: APEX_CLIENT_ID=x APEX_CLIENT_SECRET=x ./apex_precheck.sh

set -euo pipefail

APEX_CLIENT_ID="${APEX_CLIENT_ID:?Set APEX_CLIENT_ID}"
APEX_CLIENT_SECRET="${APEX_CLIENT_SECRET:?Set APEX_CLIENT_SECRET}"
TOKEN_URL="${TOKEN_URL:-https://api.dell.com/auth/oauth/v2/token}"
API_BASE="${API_BASE:-https://api.dell.com/cloudiq/rest/v1}"
HEALTH_MIN=80
CAP_HEADROOM_MIN_PCT=20
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

TOKEN=$(curl -s --max-time 15 -X POST "$TOKEN_URL" \
  -d "grant_type=client_credentials&client_id=${APEX_CLIENT_ID}&client_secret=${APEX_CLIENT_SECRET}" \
  -H "Content-Type: application/x-www-form-urlencoded" 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")
[[ -z "$TOKEN" ]] && { echo "ERROR: Auth failed" >&2; exit 2; }

echo "========================================"
echo "  APEX Pre-Change Check"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Check systems
SYSTEMS=$(curl -s --max-time 15 \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "${API_BASE}/systems" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d))" 2>/dev/null || echo "{}")

python3 -c "
import sys, json, urllib.request
data = json.load(sys.stdin)
systems = data.get('results', data if isinstance(data, list) else [])
health_min = float('${HEALTH_MIN}')
headroom_min = float('${CAP_HEADROOM_MIN_PCT}')
fail = False

for s in systems:
    name  = s.get('system_name', s.get('name', 'unknown'))
    sid   = s.get('id', '')
    score = float(s.get('health_score', s.get('healthScore', 100)))

    if score < health_min:
        print(f'  [FAIL] {name}: health_score={score} (min {health_min})')
        fail = True
    else:
        print(f'  [PASS] {name}: health_score={score}')

    req = urllib.request.Request(f'${API_BASE}/systems/{sid}/capacity',
        headers={'Authorization': 'Bearer ${TOKEN}', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            cap = json.load(r)
        committed = float(cap.get('committed_tib', 0))
        consumed  = float(cap.get('used_tib', 0))
        headroom_pct = round((1 - consumed/committed)*100, 1) if committed > 0 else 0.0
        if headroom_pct < headroom_min:
            print(f'  [FAIL] {name}: capacity headroom {headroom_pct}% (min {headroom_min}%)')
            fail = True
        else:
            print(f'  [PASS] {name}: capacity headroom {headroom_pct}%')
    except Exception as e:
        print(f'  [SKIP] {name}: capacity check failed ({e})')

sys.exit(1 if fail else 0)
" <<< "$SYSTEMS" || FAIL=1

# Check for CRITICAL alerts
ALERTS=$(curl -s --max-time 15 \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "${API_BASE}/alerts?status=active" 2>/dev/null || echo "{}")
CRIT_COUNT=$(echo "$ALERTS" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); a=d.get('alerts',d if isinstance(d,list) else []); print(sum(1 for x in a if x.get('severity','').upper() in ('CRITICAL','ERROR')))" 2>/dev/null || echo "0")

if [[ "$CRIT_COUNT" -eq 0 ]]; then
  check_pass "No active CRITICAL alerts"
else
  check_fail "$CRIT_COUNT active CRITICAL alert(s) — resolve before workload increase"
fi

# Note: Dell maintenance schedule check is manual via APEX Console
echo "  [INFO] Verify no Dell maintenance scheduled in next 4h via APEX Console before proceeding"

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: READY — proceed with workload change"
  exit 0
else
  echo "  Result: NOT READY — resolve failures above"
  exit 2
fi
~~~

---

## Post-Change Validation Script

After a workload change: confirms health_score is still above 80, consumed capacity is within expected range of the pre-change baseline plus expected growth, and no new alerts have appeared.

~~~bash
#!/bin/bash
# apex_postcheck.sh — Post-change validation for APEX workload change
# Usage: APEX_CLIENT_ID=x APEX_CLIENT_SECRET=x BASELINE_CONSUMED_TIB=x EXPECTED_GROWTH_TIB=x ./apex_postcheck.sh

set -euo pipefail

APEX_CLIENT_ID="${APEX_CLIENT_ID:?Set APEX_CLIENT_ID}"
APEX_CLIENT_SECRET="${APEX_CLIENT_SECRET:?Set APEX_CLIENT_SECRET}"
TOKEN_URL="${TOKEN_URL:-https://api.dell.com/auth/oauth/v2/token}"
API_BASE="${API_BASE:-https://api.dell.com/cloudiq/rest/v1}"
BASELINE_CONSUMED_TIB="${BASELINE_CONSUMED_TIB:-0}"
EXPECTED_GROWTH_TIB="${EXPECTED_GROWTH_TIB:-1}"
HEALTH_MIN=80
FAIL=0

check_pass() { echo "  [PASS] $*"; }
check_fail() { echo "  [FAIL] $*"; FAIL=1; }

TOKEN=$(curl -s --max-time 15 -X POST "$TOKEN_URL" \
  -d "grant_type=client_credentials&client_id=${APEX_CLIENT_ID}&client_secret=${APEX_CLIENT_SECRET}" \
  -H "Content-Type: application/x-www-form-urlencoded" 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")
[[ -z "$TOKEN" ]] && { echo "ERROR: Auth failed" >&2; exit 2; }

echo "========================================"
echo "  APEX Post-Change Validation"
echo "  Baseline consumed : ${BASELINE_CONSUMED_TIB} TiB"
echo "  Expected growth   : ${EXPECTED_GROWTH_TIB} TiB"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

SYSTEMS=$(curl -s --max-time 15 \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "${API_BASE}/systems" 2>/dev/null || echo "{}")

python3 -c "
import sys, json, urllib.request
data = json.load(sys.stdin)
systems = data.get('results', data if isinstance(data, list) else [])
health_min = float('${HEALTH_MIN}')
baseline = float('${BASELINE_CONSUMED_TIB}')
expected_growth = float('${EXPECTED_GROWTH_TIB}')
fail = False

for s in systems:
    name  = s.get('system_name', s.get('name', 'unknown'))
    sid   = s.get('id','')
    score = float(s.get('health_score', s.get('healthScore', 100)))

    if score < health_min:
        print(f'  [FAIL] {name}: health_score={score} dropped below {health_min}')
        fail = True
    else:
        print(f'  [PASS] {name}: health_score={score}')

    req = urllib.request.Request(f'${API_BASE}/systems/{sid}/capacity',
        headers={'Authorization': 'Bearer ${TOKEN}', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            cap = json.load(r)
        consumed = float(cap.get('used_tib', cap.get('used_gb', 0)))
        max_expected = baseline + expected_growth + 2.0  # +2 TiB tolerance
        delta = round(consumed - baseline, 2)
        if consumed <= max_expected:
            print(f'  [PASS] {name}: consumed={consumed:.2f} TiB (delta={delta:+.2f} TiB vs baseline)')
        else:
            print(f'  [FAIL] {name}: consumed={consumed:.2f} TiB exceeds expected max {max_expected:.2f} TiB')
            fail = True
    except Exception as e:
        print(f'  [SKIP] {name}: capacity check failed ({e})')

sys.exit(1 if fail else 0)
" <<< "$SYSTEMS" || FAIL=1

# Check for new alerts
ALERT_COUNT=$(curl -s --max-time 15 \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "${API_BASE}/alerts?status=active" 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); a=d.get('alerts',d if isinstance(d,list) else []); print(len(a))" 2>/dev/null || echo "0")
echo "  Active alerts post-change: $ALERT_COUNT (verify no new alerts vs pre-change baseline)"

echo ""
echo "========================================"
if [[ "$FAIL" -eq 0 ]]; then
  echo "  Result: PASS — APEX post-change validation successful"
  exit 0
else
  echo "  Result: FAIL — investigate issues above"
  exit 1
fi
~~~

---

## Health Check Script

Cron-safe script reporting system name, health score, contracted vs consumed, percentage used, and alert count. Exits 0 (OK), 1 (warning), or 2 (critical).

~~~bash
#!/bin/bash
# apex_health.sh — Cron-safe APEX health check
# Usage: APEX_CLIENT_ID=x APEX_CLIENT_SECRET=x ./apex_health.sh
# Exit: 0=OK  1=WARNING  2=CRITICAL

APEX_CLIENT_ID="${APEX_CLIENT_ID:?Set APEX_CLIENT_ID}"
APEX_CLIENT_SECRET="${APEX_CLIENT_SECRET:?Set APEX_CLIENT_SECRET}"
TOKEN_URL="${TOKEN_URL:-https://api.dell.com/auth/oauth/v2/token}"
API_BASE="${API_BASE:-https://api.dell.com/cloudiq/rest/v1}"
WARN_PCT="${WARN_PCT:-80}"
CRIT_PCT="${CRIT_PCT:-90}"
HEALTH_WARN="${HEALTH_WARN:-80}"

TOKEN=$(curl -s --max-time 15 -X POST "$TOKEN_URL" \
  -d "grant_type=client_credentials&client_id=${APEX_CLIENT_ID}&client_secret=${APEX_CLIENT_SECRET}" \
  -H "Content-Type: application/x-www-form-urlencoded" 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")

[[ -z "$TOKEN" ]] && { echo "APEX_HEALTH status=CRITICAL reason=auth_failed"; exit 2; }

SYSTEMS=$(curl -s --max-time 15 \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "${API_BASE}/systems" 2>/dev/null || echo "{}")

ALERT_COUNT=$(curl -s --max-time 15 \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" \
  "${API_BASE}/alerts?status=active" 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('alerts',d if isinstance(d,list) else [])))" 2>/dev/null || echo "0")

python3 -c "
import sys, json, urllib.request
data = json.load(sys.stdin)
systems = data.get('results', data if isinstance(data, list) else [])
warn_pct = float('${WARN_PCT}')
crit_pct = float('${CRIT_PCT}')
health_warn = float('${HEALTH_WARN}')
alert_count = int('${ALERT_COUNT}')
worst = 0

for s in systems:
    name  = s.get('system_name', s.get('name', 'unknown'))
    sid   = s.get('id','')
    score = float(s.get('health_score', s.get('healthScore', 100)))

    req = urllib.request.Request(f'${API_BASE}/systems/{sid}/capacity',
        headers={'Authorization': 'Bearer ${TOKEN}', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            cap = json.load(r)
        committed = float(cap.get('committed_tib', 0))
        consumed  = float(cap.get('used_tib', 0))
        pct = round(consumed / committed * 100, 1) if committed > 0 else 0.0
    except Exception:
        committed = consumed = pct = 0

    if pct >= crit_pct or score < health_warn:
        status = 'CRITICAL'
        worst = max(worst, 2)
    elif pct >= warn_pct:
        status = 'WARNING'
        worst = max(worst, 1)
    else:
        status = 'OK'

    print(f'APEX_HEALTH system={name} health_score={score} committed_tib={committed:.1f} consumed_tib={consumed:.1f} pct_used={pct}% alerts={alert_count} status={status}')

sys.exit(worst)
" <<< "$SYSTEMS"
~~~

---

## Windows: APEX Storage Capacity Report via REST API (PowerShell)

Uses the Dell APEX REST API with OAuth2 to fetch all APEX Block storage systems and report contracted vs. used capacity from a Windows PowerShell window.

~~~powershell
# apex_capacity_report.ps1 — APEX Block Storage capacity report (Windows PowerShell)
# Requires: PowerShell 5.1+ (built into Windows 10/11)
# Run: .\apex_capacity_report.ps1

$ClientId     = "your-client-id"      # From APEX Console: Settings → API Credentials
$ClientSecret = "your-client-secret"  # From APEX Console: Settings → API Credentials

$TokenUrl = "https://api.dell.com/auth/oauth/v2/token"
$ApiBase  = "https://api.dell.com/cloudiq/rest/v1"

# Step 1: Get OAuth2 access token
Write-Host "Authenticating to Dell API ..."
try {
    $TokenResp = Invoke-RestMethod -Uri $TokenUrl `
        -Method POST `
        -Body "grant_type=client_credentials&client_id=$ClientId&client_secret=$ClientSecret" `
        -ContentType "application/x-www-form-urlencoded"
    $Token = $TokenResp.access_token
} catch {
    Write-Host "ERROR: Authentication failed - $($_.Exception.Message)"
    exit 1
}

if (-not $Token) {
    Write-Host "ERROR: No access token received. Check client ID and secret."
    exit 1
}
Write-Host "Authentication successful."
$Headers = @{ Authorization = "Bearer $Token"; Accept = "application/json" }

# Step 2: Get APEX Block systems
Write-Host ""
Write-Host "Fetching APEX Block storage systems ..."
try {
    $SysResp = Invoke-RestMethod -Uri "$ApiBase/systems?filter=type+eq+%22APEX_BLOCK%22" -Headers $Headers
    $Systems = $SysResp.results
} catch {
    # Fall back to all systems if filter is not supported
    try {
        $SysResp = Invoke-RestMethod -Uri "$ApiBase/systems" -Headers $Headers
        $Systems = $SysResp.results | Where-Object { $_.type -match "APEX" }
    } catch {
        Write-Host "ERROR: Could not fetch systems - $($_.Exception.Message)"
        exit 1
    }
}

Write-Host ""
Write-Host "========================================"
Write-Host "  APEX Block Storage Capacity Report"
Write-Host "========================================"
Write-Host ""

if (-not $Systems -or $Systems.Count -eq 0) {
    Write-Host "  No APEX Block systems found."
    exit 0
}

$Flagged = 0
foreach ($Sys in $Systems) {
    $Name = $Sys.system_name
    $Type = $Sys.system_type
    $SysId = $Sys.id

    # Get capacity details
    try {
        $Cap = Invoke-RestMethod -Uri "$ApiBase/systems/$SysId/capacity" -Headers $Headers
        $Contracted = [math]::Round($Cap.committed_tib, 2)
        $Used       = [math]::Round($Cap.used_tib, 2)
        $PctUsed    = if ($Contracted -gt 0) { [math]::Round($Used / $Contracted * 100, 1) } else { 0 }
        $Flag       = if ($PctUsed -ge 80) { "  <<< $PctUsed% USED" ; $Flagged++ } else { "" }
    } catch {
        $Contracted = "N/A"
        $Used       = "N/A"
        $PctUsed    = "N/A"
        $Flag       = ""
    }

    Write-Host "  System     : $Name"
    Write-Host "  Type       : $Type"
    Write-Host "  Contracted : $Contracted TiB"
    Write-Host "  Used       : $Used TiB ($PctUsed%)$Flag"
    Write-Host ""
}

Write-Host "========================================"
Write-Host "  Total systems : $($Systems.Count)"
if ($Flagged -gt 0) {
    Write-Host "  WARNING: $Flagged system(s) at 80% or above contracted capacity."
    exit 1
} else {
    Write-Host "  STATUS: OK — All systems below 80% of contracted capacity."
    exit 0
}
~~~

### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or 11 (PowerShell 5.1 is already built in)
- Internet access to api.dell.com
- An APEX API client ID and client secret

**Step 1 — Save the file**

1. Open **Notepad**
2. Copy the entire code block above
3. Click **File → Save As**, change "Save as type" to **All Files**
4. Name it `apex_capacity_report.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put | How to find it |
|---|---|---|
| `$ClientId` | Your APEX API client ID | Log into console.cloudapex.dell.com → Settings → API Credentials → Create credentials |
| `$ClientSecret` | Your APEX API client secret | Shown once when you create the credentials — copy it then |

**Step 3 — Open a terminal**

- **For .ps1 (PowerShell):** Press Windows key → type `PowerShell` → right-click → **Run as Administrator**

**Step 4 — Allow scripts to run (one-time)**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```bash
cd C:\Users\YourName\Desktop
.\apex_capacity_report.ps1
```

**What you should see**

For each APEX Block storage system: the system name, type, contracted capacity in TiB, and current used capacity with percentage. Any system at 80% or above of its contracted amount is flagged. The summary shows how many systems are flagged and the overall status.
