# Scripts

> Part of the [NetApp Keystone](../) reference.

---

## Keystone Collector Health Check (Bash)

Check Keystone Collector service status, verify the last collection timestamp from the collector log, and confirm the collector can reach the Keystone API endpoint. Exits non-zero if the collector is stopped or the last collection is more than two hours old.

~~~bash
#!/bin/bash
# Keystone Collector Health Check
# Run on the Keystone Collector host.
# Usage: KEYSTONE_API_HOST=keystone.example.com ./keystone_health.sh

set -euo pipefail

KEYSTONE_API_HOST="${KEYSTONE_API_HOST:-keystone.netapp.com}"
LOG_DIR="${KEYSTONE_LOG_DIR:-/var/log/keystone-collector}"
MAX_AGE_HOURS=2

# ANSI colours
RED='\033[0;31m'; YEL='\033[0;33m'; GRN='\033[0;32m'; NC='\033[0m'

worst=0  # 0=OK 1=WARN 2=CRIT

pass()  { echo -e "${GRN}[PASS]${NC}  $*"; }
warn()  { echo -e "${YEL}[WARN]${NC}  $*"; (( worst < 1 )) && worst=1; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; (( worst < 2 )) && worst=2; }

echo "=== Keystone Collector Health Check ==="
echo "Host : $(hostname)"
echo "Time : $(date)"
echo "---------------------------------------"

# ------------------------------------------------------------------
# Check 1: systemd service status
# ------------------------------------------------------------------
if systemctl is-active --quiet keystone-collector 2>/dev/null; then
    pass "keystone-collector service is active"
elif systemctl is-active --quiet keystonecollector 2>/dev/null; then
    pass "keystonecollector service is active"
else
    fail "Keystone Collector service is NOT running"
    echo "       Hint: sudo systemctl start keystone-collector"
fi

# ------------------------------------------------------------------
# Check 2: Last collection timestamp from logs
# ------------------------------------------------------------------
LATEST_LOG=$(find "$LOG_DIR" -maxdepth 2 -name "*.log" -newer /dev/null 2>/dev/null \
             | xargs ls -t 2>/dev/null | head -1)

if [[ -z "$LATEST_LOG" ]]; then
    warn "No log files found in $LOG_DIR"
else
    # Look for the most recent "collection completed" or "data collected" entry
    LAST_LINE=$(grep -iE "collection (complete|success|finished)|data collected" "$LATEST_LOG" 2>/dev/null \
                | tail -1 || true)

    if [[ -z "$LAST_LINE" ]]; then
        warn "No successful collection entry found in $LATEST_LOG"
    else
        # Extract ISO timestamp if present (format: 2024-01-15T14:30:00)
        if [[ "$LAST_LINE" =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}) ]]; then
            LAST_TS="${BASH_REMATCH[1]}"
            LAST_EPOCH=$(date -d "$LAST_TS" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "$LAST_TS" +%s 2>/dev/null || echo 0)
            NOW_EPOCH=$(date +%s)
            AGE_HOURS=$(( (NOW_EPOCH - LAST_EPOCH) / 3600 ))

            if (( AGE_HOURS <= MAX_AGE_HOURS )); then
                pass "Last collection: $LAST_TS (${AGE_HOURS}h ago)"
            else
                fail "Last collection was ${AGE_HOURS}h ago (threshold: ${MAX_AGE_HOURS}h) — $LAST_TS"
            fi
        else
            warn "Cannot parse timestamp from: $LAST_LINE"
        fi
    fi
fi

# ------------------------------------------------------------------
# Check 3: API endpoint reachability
# ------------------------------------------------------------------
API_URL="https://${KEYSTONE_API_HOST}/api/v1/health"
HTTP_CODE=$(curl -sk -o /dev/null -w "%{http_code}" --max-time 10 "$API_URL" 2>/dev/null || echo "000")

if [[ "$HTTP_CODE" =~ ^(200|401|403) ]]; then
    # 401/403 means the endpoint is reachable but auth is required — that is fine for a connectivity test
    pass "Keystone API endpoint reachable (HTTP $HTTP_CODE) — $KEYSTONE_API_HOST"
elif [[ "$HTTP_CODE" == "000" ]]; then
    fail "Cannot reach Keystone API endpoint — $KEYSTONE_API_HOST (connection refused or DNS failure)"
else
    warn "Keystone API returned unexpected status HTTP $HTTP_CODE — $KEYSTONE_API_HOST"
fi

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------
echo "---------------------------------------"
case $worst in
    0) echo -e "${GRN}Overall: PASS${NC}" ;;
    1) echo -e "${YEL}Overall: WARNING${NC}" ;;
    2) echo -e "${RED}Overall: FAIL${NC}" ;;
esac
exit $worst
~~~

---

## Keystone Usage Report (Python)

Authenticate to the NetApp BlueXP / Keystone API with an API key, retrieve committed vs. consumed capacity per service level tier, calculate burst usage percentage, and print a formatted table. Warns if burst exceeds 10% of committed for any tier.

~~~python
#!/usr/bin/env python3
"""
Keystone Usage Report
Requires: pip install requests tabulate
Variables: KEYSTONE_API_HOST, API_KEY, SUBSCRIPTION_ID
"""

import os
import sys
import requests
from tabulate import tabulate

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
API_HOST        = os.environ.get("KEYSTONE_API_HOST", "keystone.netapp.com")
API_KEY         = os.environ.get("API_KEY",           "")
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID",   "")
BURST_WARN_PCT  = 10   # warn if burst > this % of committed

if not API_KEY or not SUBSCRIPTION_ID:
    sys.exit("ERROR: Set API_KEY and SUBSCRIPTION_ID environment variables.")

BASE_URL = f"https://{API_HOST}/api/v1"
HEADERS  = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type":  "application/json",
}

# ANSI colours
RED = "\033[0;31m"; YEL = "\033[0;33m"; GRN = "\033[0;32m"; NC = "\033[0m"

# -------------------------------------------------------------------
# Fetch subscription usage
# -------------------------------------------------------------------
def fetch_usage():
    url = f"{BASE_URL}/subscriptions/{SUBSCRIPTION_ID}/usage"
    resp = requests.get(url, headers=HEADERS, timeout=30, verify=True)
    resp.raise_for_status()
    return resp.json()

# -------------------------------------------------------------------
# Parse service level tiers from the API response
# -------------------------------------------------------------------
def parse_tiers(data):
    tiers = []
    # Adjust the key path to match your actual API response schema
    service_levels = data.get("service_levels", data.get("tiers", []))
    for sl in service_levels:
        name      = sl.get("name", sl.get("service_level", "unknown"))
        committed = float(sl.get("committed_tib", sl.get("committed", 0)))
        consumed  = float(sl.get("consumed_tib",  sl.get("consumed",  0)))
        burst     = float(sl.get("burst_tib",     sl.get("burst",     0)))
        burst_pct = (burst / committed * 100) if committed > 0 else 0.0
        tiers.append({
            "tier":      name,
            "committed": committed,
            "consumed":  consumed,
            "burst":     burst,
            "burst_pct": burst_pct,
        })
    return tiers

# -------------------------------------------------------------------
# Print the usage table
# -------------------------------------------------------------------
def print_table(tiers):
    rows = []
    warnings = []
    for t in tiers:
        pct_of_committed = (t["consumed"] / t["committed"] * 100) if t["committed"] > 0 else 0
        burst_flag = ""
        if t["burst_pct"] > BURST_WARN_PCT:
            burst_flag = f"{YEL} WARN{NC}"
            warnings.append(f"{t['tier']}: {t['burst_pct']:.1f}% burst of committed")

        rows.append([
            t["tier"],
            f"{t['committed']:.2f} TiB",
            f"{t['consumed']:.2f} TiB",
            f"{t['burst']:.2f} TiB",
            f"{t['burst_pct']:.1f}%{burst_flag}",
            f"{pct_of_committed:.1f}%",
        ])

    print(f"\nKeystone Usage Report — Subscription: {SUBSCRIPTION_ID}")
    print("=" * 80)
    print(tabulate(
        rows,
        headers=["Tier", "Committed", "Consumed", "Burst Used", "Burst %", "% of Committed"],
        tablefmt="simple",
    ))
    print()

    if warnings:
        print(f"{YEL}Burst warnings:{NC}")
        for w in warnings:
            print(f"  - {w}")
        print()

    return bool(warnings)

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    try:
        data  = fetch_usage()
        tiers = parse_tiers(data)
    except requests.HTTPError as exc:
        sys.exit(f"API error: {exc}")
    except Exception as exc:
        sys.exit(f"Unexpected error: {exc}")

    if not tiers:
        print("No service level data returned. Check SUBSCRIPTION_ID.")
        sys.exit(1)

    had_warnings = print_table(tiers)
    sys.exit(1 if had_warnings else 0)

if __name__ == "__main__":
    main()
~~~

---

## Volume Service Level Audit (Bash)

SSH to the ONTAP cluster backing a Keystone subscription, list all volumes and their assigned QoS policy groups, and flag any volumes that have no QoS policy assigned. Unclassified volumes may be billed at the wrong Keystone service level tier.

~~~bash
#!/bin/bash
# Keystone Volume Service Level Audit
# Usage: ONTAP_HOST=cluster ONTAP_USER=admin ONTAP_PASS=secret ./keystone_vol_audit.sh

set -euo pipefail

CLUSTER="${ONTAP_HOST:?Set ONTAP_HOST}"
USER="${ONTAP_USER:?Set ONTAP_USER}"
PASS="${ONTAP_PASS:?Set ONTAP_PASS}"

if ! command -v sshpass &>/dev/null; then
    echo "ERROR: sshpass required." >&2
    exit 3
fi

RAW=$(sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no \
    "${USER}@${CLUSTER}" \
    'volume show -fields vserver,volume,qos-policy-group,state 2>/dev/null' 2>/dev/null)

# ANSI colours
RED='\033[0;31m'; GRN='\033[0;32m'; NC='\033[0m'

total=0
unclassified=0
declare -A tier_count

printf "\n%-30s %-35s %-30s %s\n" "VSERVER" "VOLUME" "QOS POLICY (SERVICE LEVEL)" "FLAG"
printf '%0.s-' {1..110}; echo

while IFS= read -r line; do
    [[ "$line" =~ ^(Vserver|vserver|[[:space:]]*$|[0-9]+ entries) ]] && continue

    vserver=$(echo "$line" | awk '{print $1}')
    volume=$(echo "$line"  | awk '{print $2}')
    qos=$(echo "$line"     | awk '{print $3}')
    state=$(echo "$line"   | awk '{print $4}')

    [[ -z "$vserver" || -z "$volume" ]] && continue
    [[ "$state" == "offline" ]] && continue   # skip offline volumes

    (( total++ ))

    if [[ -z "$qos" || "$qos" == "-" || "$qos" == "none" ]]; then
        flag="${RED}NO QOS — unclassified${NC}"
        (( unclassified++ ))
    else
        flag="${GRN}OK${NC}"
        tier_count["$qos"]=$(( ${tier_count["$qos"]:-0} + 1 ))
    fi

    printf "%-30s %-35s %-30s " "$vserver" "$volume" "${qos:--}"
    echo -e "$flag"
done <<< "$RAW"

echo
printf '%0.s-' {1..110}; echo
echo "Total volumes checked : $total"
echo -e "Unclassified volumes  : ${RED}${unclassified}${NC}"

if (( ${#tier_count[@]} > 0 )); then
    echo
    echo "Volumes per QoS policy:"
    for tier in "${!tier_count[@]}"; do
        printf "  %-30s : %d volumes\n" "$tier" "${tier_count[$tier]}"
    done
fi

echo
if (( unclassified > 0 )); then
    echo -e "${RED}ACTION REQUIRED: $unclassified volume(s) have no QoS policy and may be billed at the wrong Keystone tier.${NC}"
    echo "Fix: volume modify -vserver <svm> -volume <vol> -qos-policy-group <keystone-psl>"
    exit 1
else
    echo -e "${GRN}All volumes have a QoS policy assigned.${NC}"
    exit 0
fi
~~~
