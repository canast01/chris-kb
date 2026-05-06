# Scripts

> Part of the [Pure Storage Evergreen//One](../) reference.

---

## Consumption Usage Report (Python)

Authenticate to the Pure1 REST API using a JWT signed with your private key, fetch subscription asset usage metrics, and print a table showing committed vs. consumed vs. burst per array. Warns if any array is consuming more than 90% of committed capacity.

~~~python
#!/usr/bin/env python3
"""
Evergreen//One Consumption Usage Report
Requires: pip install requests pyjwt cryptography tabulate
Variables: PURE1_APP_ID, PURE1_PRIVATE_KEY_FILE
"""

import os
import sys
import time

try:
    import jwt
    import requests
    from tabulate import tabulate
except ImportError:
    sys.exit("ERROR: pip install requests pyjwt cryptography tabulate")

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
APP_ID          = os.environ.get("PURE1_APP_ID",          "")
PRIVATE_KEY_FILE = os.environ.get("PURE1_PRIVATE_KEY_FILE", "")
PURE1_API_BASE  = "https://api.pure1.purestorage.com/api/1.0"
WARN_PCT        = 90   # warn if consumed > this % of committed

if not APP_ID or not PRIVATE_KEY_FILE:
    sys.exit("Set PURE1_APP_ID and PURE1_PRIVATE_KEY_FILE environment variables.")

# -------------------------------------------------------------------
# Generate JWT for Pure1 authentication
# -------------------------------------------------------------------
def get_pure1_token():
    with open(PRIVATE_KEY_FILE, "r") as f:
        private_key = f.read()

    payload = {
        "iss": APP_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token if isinstance(token, str) else token.decode("utf-8")

def get_access_token(jwt_token):
    resp = requests.post(
        f"{PURE1_API_BASE}/oauth2/1.0/token",
        data={"grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
              "subject_token": jwt_token,
              "subject_token_type": "urn:ietf:params:oauth:token-type:jwt"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

# -------------------------------------------------------------------
# Fetch subscription assets
# -------------------------------------------------------------------
def fetch_subscription_assets(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        f"{PURE1_API_BASE}/subscriptions/assets",
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("items", [])

# -------------------------------------------------------------------
# Parse asset data
# -------------------------------------------------------------------
def parse_assets(assets):
    rows = []
    warnings = []

    for asset in assets:
        array_name = asset.get("name", asset.get("display_name", "unknown"))
        tier        = asset.get("subscription_asset_type", asset.get("service_tier", "unknown"))

        # Capacity values in TiB (field names may vary by API version)
        committed = float(asset.get("reserved_tib",       asset.get("committed_tib",  0)) or 0)
        consumed  = float(asset.get("consumed_tib",       asset.get("used_tib",        0)) or 0)
        burst     = float(asset.get("burst_consumed_tib", asset.get("burst_tib",        0)) or 0)

        pct_consumed = (consumed / committed * 100) if committed > 0 else 0.0

        flag = ""
        if pct_consumed >= WARN_PCT:
            flag = " [WARN: >{WARN_PCT}%]"
            warnings.append(f"{array_name}: {pct_consumed:.1f}% of committed consumed")

        rows.append([
            array_name,
            tier,
            f"{committed:.2f} TiB",
            f"{consumed:.2f} TiB",
            f"{burst:.2f} TiB",
            f"{pct_consumed:.1f}%{flag}",
        ])

    return rows, warnings

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
RED  = "\033[0;31m"; YEL  = "\033[0;33m"; GRN  = "\033[0;32m"; NC = "\033[0m"

print(f"\nEvergreen//One Consumption Usage Report")
print(f"Pure1 App ID: {APP_ID}")
print(f"Generated   : {__import__('datetime').datetime.now():%Y-%m-%d %H:%M}\n")

try:
    jwt_token    = get_pure1_token()
    access_token = get_access_token(jwt_token)
    assets       = fetch_subscription_assets(access_token)
except Exception as exc:
    sys.exit(f"API error: {exc}")

if not assets:
    print("No subscription assets returned. Check APP_ID and subscription.")
    sys.exit(0)

rows, warnings = parse_assets(assets)

print(tabulate(
    rows,
    headers=["Array", "Tier", "Committed", "Consumed", "Burst Used", "% Consumed"],
    tablefmt="simple",
))

print(f"\nTotal assets: {len(assets)}")

if warnings:
    print(f"\n{YEL}Consumption warnings:{NC}")
    for w in warnings:
        print(f"  {YEL}!{NC} {w}")
    print(f"\n{YEL}Consider requesting additional committed capacity or reviewing growth.{NC}")
    sys.exit(1)
else:
    print(f"\n{GRN}All arrays are within {WARN_PCT}% of committed capacity.{NC}")
    sys.exit(0)
~~~

---

## SLA Compliance Check (Python)

Fetch 30-day availability, read latency, and write latency metrics from the Pure1 API for all Evergreen//One arrays, compare against SLA guarantees (99.9999% availability, sub-1ms read latency), and print a compliance report flagging any breaches.

~~~python
#!/usr/bin/env python3
"""
Evergreen//One SLA Compliance Check
Checks: availability >= 99.9999%, read latency < 1ms, write latency < 1ms
Requires: pip install requests pyjwt cryptography tabulate
Variables: PURE1_APP_ID, PURE1_PRIVATE_KEY_FILE
"""

import os
import sys
import time
import datetime

try:
    import jwt
    import requests
    from tabulate import tabulate
except ImportError:
    sys.exit("ERROR: pip install requests pyjwt cryptography tabulate")

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
APP_ID           = os.environ.get("PURE1_APP_ID",           "")
PRIVATE_KEY_FILE = os.environ.get("PURE1_PRIVATE_KEY_FILE", "")
PURE1_API_BASE   = "https://api.pure1.purestorage.com/api/1.0"

# SLA thresholds
SLA_AVAIL_PCT    = 99.9999   # minimum availability %
SLA_READ_MS      = 1.0       # maximum average read latency in ms
SLA_WRITE_MS     = 1.0       # maximum average write latency in ms
LOOKBACK_DAYS    = 30

if not APP_ID or not PRIVATE_KEY_FILE:
    sys.exit("Set PURE1_APP_ID and PURE1_PRIVATE_KEY_FILE.")

RED  = "\033[0;31m"; YEL  = "\033[0;33m"; GRN  = "\033[0;32m"; NC = "\033[0m"

# -------------------------------------------------------------------
# Auth helpers (same as consumption report)
# -------------------------------------------------------------------
def get_pure1_token():
    with open(PRIVATE_KEY_FILE) as f:
        key = f.read()
    payload = {"iss": APP_ID, "iat": int(time.time()), "exp": int(time.time()) + 3600}
    tok = jwt.encode(payload, key, algorithm="RS256")
    return tok if isinstance(tok, str) else tok.decode()

def get_access_token(jwt_tok):
    resp = requests.post(
        f"{PURE1_API_BASE}/oauth2/1.0/token",
        data={"grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
              "subject_token": jwt_tok,
              "subject_token_type": "urn:ietf:params:oauth:token-type:jwt"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

# -------------------------------------------------------------------
# Fetch metrics
# -------------------------------------------------------------------
def fetch_metrics(token, metric_keys):
    end_ms   = int(time.time() * 1000)
    start_ms = end_ms - LOOKBACK_DAYS * 86400 * 1000
    headers  = {"Authorization": f"Bearer {token}"}

    params = {
        "names":      ",".join(metric_keys),
        "start_time": start_ms,
        "end_time":   end_ms,
        "aggregation":"avg",
        "resolution": 86400000,   # daily resolution
    }
    resp = requests.get(
        f"{PURE1_API_BASE}/metrics/history",
        headers=headers,
        params=params,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("items", [])

def fetch_arrays(token):
    resp = requests.get(
        f"{PURE1_API_BASE}/arrays",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("items", [])

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
print(f"\nEvergreen//One SLA Compliance Report")
print(f"Lookback: {LOOKBACK_DAYS} days  |  Generated: {datetime.datetime.now():%Y-%m-%d %H:%M}\n")
print(f"SLA Thresholds: Availability >= {SLA_AVAIL_PCT}%  |  Read latency < {SLA_READ_MS}ms  |  Write latency < {SLA_WRITE_MS}ms\n")

try:
    jwt_tok = get_pure1_token()
    token   = get_access_token(jwt_tok)
    arrays  = fetch_arrays(token)
    metrics = fetch_metrics(token, [
        "array_read_latency_us",
        "array_write_latency_us",
        "array_availability_percent",
    ])
except Exception as exc:
    sys.exit(f"API error: {exc}")

# Organise metrics by array name
from collections import defaultdict
array_metrics = defaultdict(dict)
for m in metrics:
    res_name = m.get("resource", {}).get("name", "unknown")
    metric_key = m.get("name", "")
    data = m.get("data", [])
    if data:
        avg_val = sum(d[1] for d in data if d[1] is not None) / max(len(data), 1)
        array_metrics[res_name][metric_key] = avg_val

# -------------------------------------------------------------------
# Build compliance table
# -------------------------------------------------------------------
rows = []
breaches = []

for array in arrays:
    name    = array.get("name", "unknown")
    metrics = array_metrics.get(name, {})

    avail_pct   = metrics.get("array_availability_percent", None)
    read_us     = metrics.get("array_read_latency_us",  None)
    write_us    = metrics.get("array_write_latency_us", None)

    read_ms  = read_us  / 1000 if read_us  is not None else None
    write_ms = write_us / 1000 if write_us is not None else None

    avail_str   = f"{avail_pct:.6f}%"  if avail_pct  is not None else "N/A"
    read_str    = f"{read_ms:.3f} ms"  if read_ms    is not None else "N/A"
    write_str   = f"{write_ms:.3f} ms" if write_ms   is not None else "N/A"

    row_breach = False

    if avail_pct is not None and avail_pct < SLA_AVAIL_PCT:
        avail_str = f"{RED}{avail_str} BREACH{NC}"
        breaches.append(f"{name}: availability {avail_pct:.6f}% < {SLA_AVAIL_PCT}%")
        row_breach = True

    if read_ms is not None and read_ms > SLA_READ_MS:
        read_str = f"{RED}{read_str} BREACH{NC}"
        breaches.append(f"{name}: read latency {read_ms:.3f}ms > {SLA_READ_MS}ms")
        row_breach = True

    if write_ms is not None and write_ms > SLA_WRITE_MS:
        write_str = f"{RED}{write_str} BREACH{NC}"
        breaches.append(f"{name}: write latency {write_ms:.3f}ms > {SLA_WRITE_MS}ms")
        row_breach = True

    status = f"{RED}BREACH{NC}" if row_breach else f"{GRN}COMPLIANT{NC}"
    rows.append([name, avail_str, read_str, write_str, status])

print(tabulate(
    rows,
    headers=["Array", "Availability (avg)", "Read Latency (avg)", "Write Latency (avg)", "SLA Status"],
    tablefmt="simple",
))

print()
if breaches:
    print(f"{RED}SLA BREACHES DETECTED:{NC}")
    for b in breaches:
        print(f"  {RED}x{NC} {b}")
    print(f"\nContact Pure account team with breach details for SLA credit review.")
    sys.exit(2)
else:
    print(f"{GRN}All arrays are SLA-compliant for the {LOOKBACK_DAYS}-day review period.{NC}")
    sys.exit(0)
~~~

---

## Burst Alert Script (Bash)

Lightweight cron-friendly script that fetches current burst capacity usage from the Pure1 API using JWT authentication via curl, and sends an email alert if burst exceeds the configured warning percentage.

~~~bash
#!/bin/bash
# Evergreen//One Burst Capacity Alert
# Cron-friendly: sends email if burst > WARN_BURST_PCT of committed.
# Usage: Set variables below or export them before running.
# Cron example: */30 * * * * /opt/scripts/burst_alert.sh >> /var/log/burst_alert.log 2>&1

set -euo pipefail

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
PURE1_APP_ID="${PURE1_APP_ID:?Set PURE1_APP_ID}"
PURE1_PRIVATE_KEY="${PURE1_PRIVATE_KEY_FILE:?Set PURE1_PRIVATE_KEY_FILE}"
COMMITTED_TB="${COMMITTED_TB:?Set COMMITTED_TB (e.g., 100)}"
WARN_BURST_PCT="${WARN_BURST_PCT:-20}"
ALERT_EMAIL="${ALERT_EMAIL:?Set ALERT_EMAIL}"
PURE1_API="https://api.pure1.purestorage.com/api/1.0"

# -------------------------------------------------------------------
# Dependencies
# -------------------------------------------------------------------
for cmd in curl openssl python3 awk; do
    command -v "$cmd" &>/dev/null || { echo "ERROR: $cmd not found"; exit 3; }
done

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

log "Starting Evergreen//One burst alert check"

# -------------------------------------------------------------------
# Generate JWT using openssl + python3 (no additional pip packages)
# -------------------------------------------------------------------
NOW=$(date +%s)
EXP=$(( NOW + 3600 ))

# Build JWT header and payload in base64url encoding
b64url() {
    python3 -c "
import base64, sys
data = sys.stdin.buffer.read()
print(base64.urlsafe_b64encode(data).rstrip(b'=').decode())
"
}

HEADER=$(printf '{"alg":"RS256","typ":"JWT"}' | b64url)
PAYLOAD=$(printf '{"iss":"%s","iat":%d,"exp":%d}' "$PURE1_APP_ID" "$NOW" "$EXP" | b64url)
SIGNING_INPUT="${HEADER}.${PAYLOAD}"

SIGNATURE=$(printf '%s' "$SIGNING_INPUT" | \
    openssl dgst -sha256 -sign "$PURE1_PRIVATE_KEY" 2>/dev/null | \
    python3 -c "
import base64, sys
data = sys.stdin.buffer.read()
print(base64.urlsafe_b64encode(data).rstrip(b'=').decode())
")

JWT_TOKEN="${SIGNING_INPUT}.${SIGNATURE}"

# -------------------------------------------------------------------
# Exchange JWT for API access token
# -------------------------------------------------------------------
ACCESS_TOKEN=$(curl -sf \
    -X POST "${PURE1_API}/oauth2/1.0/token" \
    --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
    --data-urlencode "subject_token=${JWT_TOKEN}" \
    --data-urlencode "subject_token_type=urn:ietf:params:oauth:token-type:jwt" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")

log "Authenticated to Pure1"

# -------------------------------------------------------------------
# Fetch subscription asset usage
# -------------------------------------------------------------------
USAGE_JSON=$(curl -sf \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    "${PURE1_API}/subscriptions/assets" 2>/dev/null)

# Extract burst_consumed_tib (sum across all assets)
BURST_TB=$(python3 -c "
import json, sys
data = json.loads('''${USAGE_JSON}''')
burst = sum(float(a.get('burst_consumed_tib', 0) or 0) for a in data.get('items', []))
print(f'{burst:.2f}')
" 2>/dev/null || echo "0")

log "Burst consumed: ${BURST_TB} TiB  |  Committed: ${COMMITTED_TB} TiB"

# -------------------------------------------------------------------
# Calculate burst percentage and compare to threshold
# -------------------------------------------------------------------
BURST_PCT=$(awk "BEGIN{printf \"%.1f\", ($BURST_TB/$COMMITTED_TB)*100}" 2>/dev/null || echo "0")
log "Burst usage: ${BURST_PCT}% of committed (warn at ${WARN_BURST_PCT}%)"

OVER_WARN=$(awk "BEGIN{print ($BURST_PCT+0 > $WARN_BURST_PCT+0) ? 1 : 0}")

if (( OVER_WARN )); then
    SUBJECT="ALERT: Evergreen//One burst usage at ${BURST_PCT}% of committed (${BURST_TB} TiB)"
    BODY="Evergreen//One Burst Alert
==============================
Time       : $(date)
Committed  : ${COMMITTED_TB} TiB
Burst Used : ${BURST_TB} TiB
Burst Pct  : ${BURST_PCT}%
Threshold  : ${WARN_BURST_PCT}%

ACTION: Review growth in Pure1 (https://pure1.purestorage.com) and
consider reducing snapshot/volume usage or requesting additional committed
capacity before the billing period closes."

    log "ALERT: Burst ${BURST_PCT}% > threshold ${WARN_BURST_PCT}% — sending email to ${ALERT_EMAIL}"

    if command -v mailx &>/dev/null; then
        echo "$BODY" | mailx -s "$SUBJECT" "$ALERT_EMAIL"
    elif command -v sendmail &>/dev/null; then
        {
            echo "To: $ALERT_EMAIL"
            echo "Subject: $SUBJECT"
            echo "Content-Type: text/plain"
            echo
            echo "$BODY"
        } | sendmail -t
    else
        log "WARNING: No mail client found (mailx/sendmail) — cannot send alert"
        echo "$BODY"
        exit 1
    fi

    log "Alert email sent."
    exit 1
else
    log "OK: Burst ${BURST_PCT}% is within threshold ${WARN_BURST_PCT}% — no alert needed."
    exit 0
fi
~~~
