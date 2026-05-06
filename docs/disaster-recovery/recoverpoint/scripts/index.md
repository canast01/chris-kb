# Scripts

> Part of the [RecoverPoint](../) reference.

---

## Consistency Group Health Monitor (Python)

Query the RecoverPoint REST API to report the replication state, lag, and RPO compliance for every consistency group.

~~~python
#!/usr/bin/env python3
# rp-cg-health.py
# Usage: RP_HOST=<host> RP_USER=<user> RP_PASS=<pass> python3 rp-cg-health.py

import os
import sys
import requests
import urllib3
from datetime import timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RP_HOST = os.environ.get("RP_HOST", "")
RP_USER = os.environ.get("RP_USER", "")
RP_PASS = os.environ.get("RP_PASS", "")

if not all([RP_HOST, RP_USER, RP_PASS]):
    sys.exit("ERROR: RP_HOST, RP_USER, and RP_PASS must be set.")

BASE_URL  = f"https://{RP_HOST}/fapi/rest/4_5"
SESSION   = requests.Session()
SESSION.auth    = (RP_USER, RP_PASS)
SESSION.verify  = False
SESSION.headers.update({"Content-Type": "application/json", "Accept": "application/json"})


def api_get(path: str) -> dict:
    r = SESSION.get(f"{BASE_URL}{path}")
    r.raise_for_status()
    return r.json()


def ms_to_human(ms: int) -> str:
    if ms is None:
        return "N/A"
    td = timedelta(milliseconds=ms)
    total_sec = int(td.total_seconds())
    if total_sec < 60:
        return f"{total_sec}s"
    if total_sec < 3600:
        return f"{total_sec // 60}m {total_sec % 60}s"
    return f"{total_sec // 3600}h {(total_sec % 3600) // 60}m"


print()
print("=== RecoverPoint Consistency Group Health Monitor ===")
print(f"Host : {RP_HOST}")
print()

# Cluster statistics
try:
    cluster_stats = api_get("/cluster/statistics")
    print(f"Cluster Status   : {cluster_stats.get('clusterUID', {}).get('id', 'unknown')}")
except Exception as exc:
    print(f"WARNING: Could not retrieve cluster statistics: {exc}")

# CG list
cgs = api_get("/groups")
cg_list = cgs.get("innerSet", [])

print(f"Consistency Groups: {len(cg_list)}")
print()
print(f"{'CG Name':<35} {'State':<15} {'Lag':<12} {'RPO':<12} {'Compliant'}")
print("-" * 82)

exit_code   = 0
non_active  = []

for cg in cg_list:
    gid     = cg.get("groupUID", {}).get("id")
    name    = cg.get("name", f"cg-{gid}")

    try:
        links = api_get(f"/groups/{gid}/links")
        link_set = links.get("innerSet", [])
    except Exception:
        link_set = []

    for link in link_set:
        state       = link.get("linkState", "unknown")
        lag_ms      = link.get("lagInMicros", None)
        if lag_ms:
            lag_ms = lag_ms // 1000  # convert microseconds to ms
        rpo_ms      = link.get("RPOInMicros", None)
        if rpo_ms:
            rpo_ms = rpo_ms // 1000

        lag_str = ms_to_human(lag_ms)
        rpo_str = ms_to_human(rpo_ms)

        compliant = "N/A"
        if lag_ms is not None and rpo_ms is not None:
            compliant = "YES" if lag_ms <= rpo_ms else "NO"

        if state != "Active":
            non_active.append((name, state))
            exit_code = 1

        flag = "" if state == "Active" else "  <-- ALERT"
        print(f"{name:<35} {state:<15} {lag_str:<12} {rpo_str:<12} {compliant}{flag}")

print()
if non_active:
    print(f"RESULT: DEGRADED — {len(non_active)} CG(s) not in Active state:")
    for cg_name, cg_state in non_active:
        print(f"  {cg_name}: {cg_state}")
    sys.exit(1)
else:
    print("RESULT: ALL CGs ACTIVE")
    sys.exit(0)
~~~

---

## DR Test Failover Script (Bash)

Authenticate against the RecoverPoint REST API, locate a consistency group by name, start image access at the latest bookmark for DR testing, and optionally roll back to restore production replication.

~~~bash
#!/usr/bin/env bash
# rp-dr-test-failover.sh
# Usage:
#   ./rp-dr-test-failover.sh                 -- start image access (DR test)
#   ./rp-dr-test-failover.sh --rollback      -- disable image access, resume replication

set -euo pipefail

RP_HOST="${RP_HOST:?RP_HOST is required}"
RP_USER="${RP_USER:?RP_USER is required}"
RP_PASS="${RP_PASS:?RP_PASS is required}"
CG_NAME="${CG_NAME:?CG_NAME (consistency group name) is required}"
BOOKMARK_POLICY="${BOOKMARK_POLICY:-latest}"
ROLLBACK=false
LOGFILE="/var/log/rp-dr-test-$(date +%Y%m%d-%H%M%S).log"

for arg in "$@"; do
    [[ "$arg" == "--rollback" ]] && ROLLBACK=true
done

BASE_URL="https://${RP_HOST}/fapi/rest/4_5"
CURL_OPTS=(-sk -u "${RP_USER}:${RP_PASS}" -H "Content-Type: application/json" -H "Accept: application/json")

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "${LOGFILE}"; }

rp_get()  { curl "${CURL_OPTS[@]}" "${BASE_URL}${1}"; }
rp_post() { curl "${CURL_OPTS[@]}" -X POST -d "${2:-}" "${BASE_URL}${1}"; }

log "=== RecoverPoint DR Test Failover ==="
log "CG: ${CG_NAME}  | Mode: $( ${ROLLBACK} && echo ROLLBACK || echo FAILOVER-TEST )"

# --- Step 1: Find CG ID by name ---
log "Step 1: Locating CG '${CG_NAME}'..."
CG_LIST=$(rp_get "/groups")
CG_ID=$(python3 - <<EOF
import json, sys
data = json.loads('''${CG_LIST}''')
for cg in data.get('innerSet', []):
    if cg.get('name') == '${CG_NAME}':
        print(cg['groupUID']['id'])
        sys.exit(0)
sys.exit(1)
EOF
)

if [[ -z "${CG_ID}" ]]; then
    log "ERROR: CG '${CG_NAME}' not found."
    exit 1
fi
log "Found CG ID: ${CG_ID}"

if ${ROLLBACK}; then
    # --- Rollback: disable image access and resume replication ---
    log "Step 2 (Rollback): Disabling image access for CG ${CG_ID}..."
    rp_post "/groups/${CG_ID}/disable_image_access" '{}'
    log "Step 3 (Rollback): Resuming replication..."
    rp_post "/groups/${CG_ID}/start_transfer" '{}'
    log "Rollback complete. Production replication resumed."
    exit 0
fi

# --- Step 2: Get latest bookmark ---
log "Step 2: Retrieving latest bookmark..."
COPIES=$(rp_get "/groups/${CG_ID}/copies")
COPY_ID=$(python3 - <<EOF
import json, sys
data = json.loads('''${COPIES}''')
copies = data.get('innerSet', [])
# Use the remote copy (non-production)
for c in copies:
    if not c.get('copySettings', {}).get('isProductionCopy', True):
        print(c['copyUID']['globalCopyUID']['copyUID'])
        sys.exit(0)
sys.exit(1)
EOF
)

if [[ -z "${COPY_ID}" ]]; then
    log "ERROR: Could not determine remote copy ID."
    exit 1
fi
log "Remote copy ID: ${COPY_ID}"

# --- Step 3: Enable image access at latest bookmark ---
log "Step 3: Enabling image access at latest bookmark on copy ${COPY_ID}..."
REQUEST_BODY=$(python3 -c "
import json
print(json.dumps({
    'copyUID': {'globalCopyUID': {'copyUID': int('${COPY_ID}')}},
    'scenario': 'LOGGED_ACCESS',
    'imageAccessMode': 'VIRTUAL_ACCESS_WITH_ROLL',
    'bookmark': {'bookmarkType': 'LATEST'}
}))
")

rp_post "/groups/${CG_ID}/enable_image_access" "${REQUEST_BODY}"
log "Image access request submitted."

# --- Step 4: Wait for access to be enabled ---
log "Step 4: Waiting for image access to become active..."
MAX_WAIT=120
ELAPSED=0
while [[ $ELAPSED -lt $MAX_WAIT ]]; do
    STATE=$(rp_get "/groups/${CG_ID}/links" | python3 -c "
import json, sys
data = json.load(sys.stdin)
links = data.get('innerSet', [])
if links:
    print(links[0].get('linkState', 'unknown'))
else:
    print('unknown')
")
    log "Current link state: ${STATE}"
    if [[ "${STATE}" == "ImageAccess" ]] || [[ "${STATE}" == "ImageAccessEnabled" ]]; then
        break
    fi
    sleep 10
    ELAPSED=$((ELAPSED + 10))
done

if [[ $ELAPSED -ge $MAX_WAIT ]]; then
    log "WARNING: Timed out waiting for image access. Check RecoverPoint UI."
    exit 1
fi

# --- Step 5: Print accessible volumes ---
log "Step 5: Image access enabled. Copy volumes are now accessible."
VOLUMES=$(rp_get "/groups/${CG_ID}/copies/${COPY_ID}/volumes" 2>/dev/null || echo '{"innerSet":[]}')
python3 - <<EOF
import json
data = json.loads('''${VOLUMES}''')
for v in data.get('innerSet', []):
    print(f"  Volume: {v.get('name', 'unknown')}  WWN: {v.get('wwn', 'N/A')}")
EOF

log "DR test failover complete. Remember to run --rollback when done."
log "Log: ${LOGFILE}"
~~~

---

## RPO Compliance Report (Python)

Query all RecoverPoint consistency groups, compare current lag to configured RPO, and flag any CG whose lag exceeds 2x the RPO.

~~~python
#!/usr/bin/env python3
# rp-rpo-compliance.py
# Usage: RP_HOST=<host> RP_USER=<user> RP_PASS=<pass> python3 rp-rpo-compliance.py

import os
import sys
import requests
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RP_HOST = os.environ.get("RP_HOST", "")
RP_USER = os.environ.get("RP_USER", "")
RP_PASS = os.environ.get("RP_PASS", "")

if not all([RP_HOST, RP_USER, RP_PASS]):
    sys.exit("ERROR: RP_HOST, RP_USER, and RP_PASS must be set.")

BASE_URL = f"https://{RP_HOST}/fapi/rest/4_5"
SESSION  = requests.Session()
SESSION.auth    = (RP_USER, RP_PASS)
SESSION.verify  = False
SESSION.headers.update({"Content-Type": "application/json", "Accept": "application/json"})


def api_get(path: str) -> dict:
    r = SESSION.get(f"{BASE_URL}{path}")
    r.raise_for_status()
    return r.json()


def micros_to_sec(us: int) -> float:
    return us / 1_000_000 if us else 0.0


def fmt_sec(sec: float) -> str:
    if sec is None:
        return "N/A"
    s = int(sec)
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s // 60}m {s % 60}s"
    return f"{s // 3600}h {(s % 3600) // 60}m"


print()
print("=== RecoverPoint RPO Compliance Report ===")
print(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Host      : {RP_HOST}")
print()

cg_data = api_get("/groups")
cg_list = cg_data.get("innerSet", [])

print(f"{'CG Name':<35} {'Configured RPO':<16} {'Current Lag':<14} {'Status':<12} {'Max Lag 24h'}")
print("-" * 90)

violations   = []
exit_code    = 0

for cg in cg_list:
    gid  = cg.get("groupUID", {}).get("id")
    name = cg.get("name", f"cg-{gid}")

    # Get link details for current lag and RPO
    try:
        links = api_get(f"/groups/{gid}/links")
        link_list = links.get("innerSet", [])
    except Exception:
        link_list = []

    for link in link_list:
        rpo_us      = link.get("RPOInMicros", 0)
        lag_us      = link.get("lagInMicros", 0)

        rpo_sec     = micros_to_sec(rpo_us)
        lag_sec     = micros_to_sec(lag_us)

        # Attempt to retrieve trend data for max lag over 24h
        # RP statistics API returns time-series; we take the max value.
        max_lag_sec = None
        try:
            stats_url = f"/groups/{gid}/statistics"
            stats     = api_get(stats_url)
            lag_samples = [
                micros_to_sec(s.get("lagInMicros", 0))
                for s in stats.get("innerSet", [])
                if s.get("lagInMicros") is not None
            ]
            if lag_samples:
                max_lag_sec = max(lag_samples)
        except Exception:
            pass  # statistics endpoint may not be available on all RP versions

        # Compliance
        if rpo_sec > 0 and lag_sec > rpo_sec:
            status = "OVER RPO"
            exit_code = 1
        elif rpo_sec > 0:
            status = "OK"
        else:
            status = "NO RPO SET"

        # 2x RPO violation
        flagged = ""
        if rpo_sec > 0 and lag_sec > (2 * rpo_sec):
            flagged = "  *** LAG > 2x RPO ***"
            violations.append(name)
            exit_code = 1

        max_lag_str = fmt_sec(max_lag_sec) if max_lag_sec is not None else "N/A"
        print(f"{name:<35} {fmt_sec(rpo_sec):<16} {fmt_sec(lag_sec):<14} {status:<12} {max_lag_str}{flagged}")

print()
if violations:
    print(f"VIOLATIONS: {len(violations)} CG(s) exceeded 2x RPO:")
    for v in violations:
        print(f"  - {v}")
elif exit_code != 0:
    print("WARNING: Some CGs are over RPO but within 2x threshold.")
else:
    print("RESULT: All CGs within RPO.")

sys.exit(exit_code)
~~~
