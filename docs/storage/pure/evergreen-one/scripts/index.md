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

#### How to run this script — step by step

**Before you start — what you need**
- Python 3 installed (download from python.org — tick "Add Python to PATH")
- A Pure1 Application ID and RSA private key file — these are created at pure1.purestorage.com under **Settings → API Registration → Create Application**. When you create an application, you generate an RSA key pair and upload the public key. Keep the private key file (a `.pem` file) on your machine
- Internet access to reach api.pure1.purestorage.com

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `eo1_usage.py` — save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | Where to find it |
|---|---|---|
| `PURE1_APP_ID` | Your Pure1 Application ID | pure1.purestorage.com → Settings → API Registration |
| `PURE1_PRIVATE_KEY_FILE` | Full path to your RSA private key `.pem` file | The file you downloaded when creating the application |

**Step 3 — Open Command Prompt and install packages**

```
pip install requests pyjwt cryptography tabulate
```

**Step 4 — Set variables and run**

```
set PURE1_APP_ID=pure1:apikey:abc123
set PURE1_PRIVATE_KEY_FILE=C:\Users\YourName\Desktop\pure1_private_key.pem
cd %USERPROFILE%\Desktop
python eo1_usage.py
```

**What you should see**

A table listing every array in your Evergreen//One subscription with its service tier, committed capacity, consumed capacity, burst used, and percentage of committed consumed. Any array over 90% of committed capacity is flagged with a warning. A summary at the bottom shows total assets and lists any warnings. This is your primary report for Evergreen//One consumption tracking.

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

#### How to run this script — step by step

**Before you start — what you need**
- Python 3 installed (python.org — tick "Add Python to PATH")
- A Pure1 Application ID and RSA private key file (same setup as the Consumption Usage Report script above)
- Internet access to reach api.pure1.purestorage.com

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `eo1_sla_check.py` — save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | Where to find it |
|---|---|---|
| `PURE1_APP_ID` | Your Pure1 Application ID | pure1.purestorage.com → Settings → API Registration |
| `PURE1_PRIVATE_KEY_FILE` | Full path to your RSA private key `.pem` file | The file you saved when creating the Pure1 application |

**Step 3 — Open Command Prompt and install packages**

```
pip install requests pyjwt cryptography tabulate
```

**Step 4 — Set variables and run**

```
set PURE1_APP_ID=pure1:apikey:abc123
set PURE1_PRIVATE_KEY_FILE=C:\Users\YourName\Desktop\pure1_private_key.pem
cd %USERPROFILE%\Desktop
python eo1_sla_check.py
```

**What you should see**

A table showing each Evergreen//One array with its 30-day average availability percentage, average read latency, and average write latency. Arrays meeting the SLA (99.9999% availability, sub-1ms latency) show COMPLIANT in green. Any metric below the SLA threshold shows BREACH in red next to the specific value. If any breach is found, a summary at the bottom lists each one and tells you to contact the Pure account team for SLA credit review.

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

#### How to run this script — step by step

**Before you start — what you need**
- WSL (Windows Subsystem for Linux) with Ubuntu, or a Linux server where you want to schedule this script as a cron job
- Inside WSL/Linux: `curl`, `openssl`, `python3`, and `awk` — all standard on Ubuntu
- A Pure1 Application ID and RSA private key file
- A mail client (`mailx` or `sendmail`) if you want email alerts — or just run it manually to see the output
- Your committed capacity in TiB (from your Evergreen//One contract)

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `eo1_burst_alert.sh` — save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | Where to find it |
|---|---|---|
| `PURE1_APP_ID` | Your Pure1 Application ID | pure1.purestorage.com → Settings → API Registration |
| `PURE1_PRIVATE_KEY_FILE` | Full path to your RSA private key `.pem` file | The file you saved when creating the application |
| `COMMITTED_TB` | Your total committed capacity in TiB, e.g. `100` | Your Evergreen//One contract |
| `WARN_BURST_PCT` | Burst % threshold for an alert (default: 20) | Your preference |
| `ALERT_EMAIL` | Email address to receive alerts | Your preference |

**Step 3 — Open WSL**

Open Ubuntu from the Start menu.

**Step 4 — Set variables and run**

```
export PURE1_APP_ID="pure1:apikey:abc123"
export PURE1_PRIVATE_KEY_FILE="/home/youruser/pure1_private_key.pem"
export COMMITTED_TB=100
export WARN_BURST_PCT=20
export ALERT_EMAIL="storage-alerts@company.com"
cd /mnt/c/Users/YourName/Desktop
bash eo1_burst_alert.sh
```

**What you should see**

Timestamped log lines showing the authentication, the burst consumption fetched from Pure1, and the calculated burst percentage. If burst is below the threshold, it prints `OK: Burst X% is within threshold` and exits cleanly. If burst exceeds the threshold, it prints an alert body and (if a mail client is configured) sends an email to your alert address.

---

## Windows: Evergreen//One Subscription Check via Pure1 API (PowerShell)

Authenticate to the Pure1 REST API using an API key, retrieve Evergreen//One subscription details and asset information, and print a formatted report. Warns if within 90 days of term end or above 90% capacity usage.

~~~powershell
# eo1_subscription_check.ps1 — Evergreen//One Subscription Check via Pure1 API (Windows PowerShell)
# Requires: PowerShell 5.1+ (pre-installed on Windows 10/11)
# Pure1 API tokens generated at: https://pure1.purestorage.com (Settings -> API Registration)
# Run: .\eo1_subscription_check.ps1

$Pure1ApiKey = "your-pure1-api-key"   # Generate at pure1.purestorage.com -> Settings -> API Registration

# Handle SSL
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

$Pure1Base = "https://api.pure1.purestorage.com/api/1.0"

# --- Step 1: Authenticate ---
Write-Host "Authenticating to Pure1 API ..." -ForegroundColor Cyan

try {
    $TokenResp = Invoke-RestMethod `
        -Uri    "$Pure1Base/oauth2/1.0/token" `
        -Method POST `
        -Body   "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange&subject_token=$([uri]::EscapeDataString($Pure1ApiKey))&subject_token_type=urn%3Apure%3Aoauth%3Atoken-type%3Aapi-token" `
        -ContentType "application/x-www-form-urlencoded" `
        -ErrorAction Stop
} catch {
    Write-Error "Authentication failed: $($_.Exception.Message)"
    Write-Host "Tip: Generate your API key at https://pure1.purestorage.com -> Settings -> API Registration" -ForegroundColor Yellow
    exit 1
}

$AccessToken = $TokenResp.access_token
if (-not $AccessToken) {
    Write-Error "No access token returned. Check API key."
    exit 1
}

$AuthHeaders = @{ Authorization = "Bearer $AccessToken" }
Write-Host "Authenticated." -ForegroundColor Green

# --- Step 2: Get subscriptions ---
Write-Host "`nFetching Evergreen//One subscriptions ..." -ForegroundColor Cyan

try {
    $SubsResp = Invoke-RestMethod `
        -Uri     "$Pure1Base/subscriptions" `
        -Headers $AuthHeaders `
        -Method  GET `
        -ErrorAction Stop
} catch {
    Write-Error "Failed to retrieve subscriptions: $($_.Exception.Message)"
    exit 1
}

$Subscriptions = $SubsResp.items
if (-not $Subscriptions -or $Subscriptions.Count -eq 0) {
    Write-Host "No Evergreen//One subscriptions found."
    exit 0
}

Write-Host "Found $($Subscriptions.Count) subscription(s).`n"

# --- Step 3: Get subscription assets ---
try {
    $AssetsResp = Invoke-RestMethod `
        -Uri     "$Pure1Base/subscription-assets" `
        -Headers $AuthHeaders `
        -Method  GET `
        -ErrorAction Stop
} catch {
    Write-Warning "Could not retrieve subscription assets: $($_.Exception.Message)"
    $AssetsResp = $null
}

$Assets = if ($AssetsResp) { $AssetsResp.items } else { @() }

# --- Step 4: Print report ---
Write-Host "=== Evergreen//One Subscription Report ===" -ForegroundColor Cyan
Write-Host ("Generated: {0}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"))
Write-Host ("-" * 80)

$today    = Get-Date
$warnings = @()

foreach ($sub in $Subscriptions) {
    $subName = $sub.name ?? $sub.display_name ?? "unknown"
    $subId   = $sub.id

    # Term dates
    $startDate = if ($sub.start_date) { [datetime]$sub.start_date } else { $null }
    $endDate   = if ($sub.end_date)   { [datetime]$sub.end_date   } else { $null }
    $daysLeft  = if ($endDate) { [math]::Round(($endDate - $today).TotalDays) } else { $null }

    # Reserved/used capacity from the subscription record
    $reservedTiB = [double]($sub.reserved_tib  ?? $sub.committed_tib  ?? 0)
    $usedTiB     = [double]($sub.consumed_tib  ?? $sub.used_tib       ?? 0)
    $pctUsed     = if ($reservedTiB -gt 0) { [math]::Round($usedTiB / $reservedTiB * 100, 1) } else { 0 }
    $status      = $sub.status ?? "unknown"

    Write-Host "`n  Subscription : $subName" -ForegroundColor Yellow
    Write-Host ("  Status       : {0}" -f $status)
    Write-Host ("  Start        : {0}" -f (if ($startDate) { $startDate.ToString("yyyy-MM-dd") } else { "N/A" }))
    Write-Host ("  End          : {0}" -f (if ($endDate) { $endDate.ToString("yyyy-MM-dd") } else { "N/A" }))

    if ($daysLeft -ne $null) {
        if ($daysLeft -le 90) {
            Write-Host ("  Days to end  : {0} *** EXPIRING SOON ***" -f $daysLeft) -ForegroundColor Red
            $warnings += "Subscription '$subName' expires in $daysLeft days ($($endDate.ToString('yyyy-MM-dd')))"
        } else {
            Write-Host ("  Days to end  : {0}" -f $daysLeft) -ForegroundColor Green
        }
    }

    Write-Host ("  Reserved     : {0:F2} TiB" -f $reservedTiB)

    $capColour = if ($pctUsed -ge 90) { "Red" } elseif ($pctUsed -ge 80) { "Yellow" } else { "Green" }
    Write-Host ("  Used         : {0:F2} TiB ({1:F1}%)" -f $usedTiB, $pctUsed) -ForegroundColor $capColour

    if ($pctUsed -ge 90) {
        $warnings += "Subscription '$subName' is at $pctUsed% capacity ($($usedTiB)/$($reservedTiB) TiB)"
    }
}

# --- Assets summary ---
if ($Assets -and $Assets.Count -gt 0) {
    Write-Host "`n--- Assets Included in Subscription ---"
    Write-Host ("  {0,-35} {1,-20} {2,12} {3,12}" -f "Asset", "Type", "Reserved", "Used")
    Write-Host ("  " + "-" * 82)
    foreach ($asset in $Assets) {
        $assetName = $asset.name ?? "unknown"
        $assetType = $asset.subscription_asset_type ?? $asset.model ?? "unknown"
        $resTiB    = [double]($asset.reserved_tib ?? 0)
        $usedTiB_a = [double]($asset.consumed_tib ?? 0)
        Write-Host ("  {0,-35} {1,-20} {2,10:F2} TiB {3,10:F2} TiB" -f $assetName, $assetType, $resTiB, $usedTiB_a)
    }
}

Write-Host "`n" + ("-" * 80)

if ($warnings.Count -gt 0) {
    Write-Host "`n*** WARNINGS ***" -ForegroundColor Red
    foreach ($w in $warnings) {
        Write-Host "  ! $w" -ForegroundColor Red
    }
    Write-Host "`nContact your Pure account team to discuss renewal or capacity expansion." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "All subscriptions are within capacity and term limits." -ForegroundColor Green
    exit 0
}
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Windows 10 or Windows 11 PC (PowerShell is already installed — nothing to download)
- A Pure1 API key — log in to pure1.purestorage.com, go to **Settings → API Registration**, and create a new API token. This is simpler than the JWT method used in the Python scripts — just a single token string
- Internet access to reach api.pure1.purestorage.com

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `eo1_subscription_check.ps1` — save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file in Notepad and change this line near the top:

| Variable | What to put here | Where to find it |
|---|---|---|
| `$Pure1ApiKey` | Your Pure1 API token | pure1.purestorage.com → Settings → API Registration |

**Step 3 — Open PowerShell as Administrator**

Press the Windows key, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as Administrator**.

**Step 4 — Allow script execution (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
cd C:\Users\YourName\Desktop
.\eo1_subscription_check.ps1
```

**What you should see**

A report showing each Evergreen//One subscription with its status, start date, end date, days remaining, reserved capacity, and current usage percentage. If any subscription is within 90 days of its term end, it is highlighted in red with `*** EXPIRING SOON ***`. If any subscription is above 90% capacity, it is also flagged in red. Below the subscription section, a table lists all the individual assets (arrays) included in the subscription. If warnings exist, the script prints a summary and exits with code 1 so it can be used in monitoring scripts.
