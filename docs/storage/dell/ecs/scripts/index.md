# Scripts

> Part of the [Dell ECS](../) reference.

---

## Node & Capacity Health Check

Queries the ECS Management REST API to check node status, cluster capacity utilisation, and active alerts. Warns if capacity exceeds 80% and goes critical above 90%.

~~~python
#!/usr/bin/env python3
# ecs_health_check.py — Node and capacity health check via ECS Management REST API
# Requirements: requests
# Usage: ECS_HOST=ecs01.example.com ECS_USER=sysadmin ECS_PASS=secret ./ecs_health_check.py

import os
import sys
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ECS_HOST = os.environ.get("ECS_HOST", "")
ECS_USER = os.environ.get("ECS_USER", "sysadmin")
ECS_PASS = os.environ.get("ECS_PASS", "")

WARN_PCT  = 80
CRIT_PCT  = 90
BASE_URL  = f"https://{ECS_HOST}:4443"

if not ECS_HOST or not ECS_PASS:
    print("ERROR: ECS_HOST and ECS_PASS must be set.", file=sys.stderr)
    sys.exit(1)


def authenticate(session):
    """Authenticate and return the auth token."""
    resp = session.get(f"{BASE_URL}/login", auth=(ECS_USER, ECS_PASS), verify=False)
    resp.raise_for_status()
    token = resp.headers.get("X-SDS-AUTH-TOKEN")
    if not token:
        raise RuntimeError("Authentication failed: no token in response headers.")
    return token


def api_get(session, token, path):
    """GET a JSON endpoint from the ECS Management API."""
    resp = session.get(
        f"{BASE_URL}{path}",
        headers={"X-SDS-AUTH-TOKEN": token, "Accept": "application/json"},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    exit_code = 0
    session = requests.Session()

    print("=" * 50)
    print("  ECS Health Check")
    print(f"  Host : {ECS_HOST}")
    print("=" * 50)

    # Authenticate
    try:
        token = authenticate(session)
        print("\n[AUTH] Login successful.\n")
    except Exception as e:
        print(f"[AUTH] FAILED: {e}")
        sys.exit(2)

    # --- Node health ---
    print("--- Node Status ---")
    try:
        nodes_data = api_get(session, token, "/vdc/nodes")
        nodes = nodes_data.get("node", [])
        for node in nodes:
            name  = node.get("nodename", node.get("ip", "unknown"))
            state = node.get("nodestatus", "UNKNOWN")
            marker = "" if state == "GOOD" else "  <<< DEGRADED"
            print(f"  {name:<30} {state}{marker}")
            if state != "GOOD":
                exit_code = max(exit_code, 2)
    except Exception as e:
        print(f"  ERROR fetching nodes: {e}")
        exit_code = max(exit_code, 2)

    # --- Capacity ---
    print("\n--- Capacity ---")
    try:
        cap = api_get(session, token, "/vdc/capacity")
        total_gb = int(cap.get("totalProvisioned_gb", 0))
        used_gb  = int(cap.get("usedCapacity_gb", 0))
        pct_used = (used_gb / total_gb * 100) if total_gb > 0 else 0
        print(f"  Total  : {total_gb:>8} GB")
        print(f"  Used   : {used_gb:>8} GB  ({pct_used:.1f}%)")
        if pct_used >= CRIT_PCT:
            print(f"  STATUS : CRITICAL — capacity at {pct_used:.1f}% (threshold {CRIT_PCT}%)")
            exit_code = max(exit_code, 2)
        elif pct_used >= WARN_PCT:
            print(f"  STATUS : WARNING  — capacity at {pct_used:.1f}% (threshold {WARN_PCT}%)")
            exit_code = max(exit_code, 1)
        else:
            print(f"  STATUS : OK")
    except Exception as e:
        print(f"  ERROR fetching capacity: {e}")
        exit_code = max(exit_code, 2)

    # --- Alerts ---
    print("\n--- Active Alerts ---")
    try:
        alerts_data = api_get(session, token, "/vdc/alerts")
        alerts = alerts_data.get("alert", [])
        if not alerts:
            print("  No active alerts.")
        for alert in alerts:
            severity = alert.get("severity", "UNKNOWN")
            desc     = alert.get("description", "no description")
            print(f"  [{severity}] {desc}")
            if severity in ("CRITICAL", "ERROR"):
                exit_code = max(exit_code, 2)
            elif severity in ("WARNING",):
                exit_code = max(exit_code, 1)
    except Exception as e:
        print(f"  ERROR fetching alerts: {e}")
        exit_code = max(exit_code, 2)

    # Logout
    try:
        session.get(
            f"{BASE_URL}/logout",
            headers={"X-SDS-AUTH-TOKEN": token},
            verify=False,
        )
    except Exception:
        pass

    print("\n" + "=" * 50)
    labels = {0: "OK", 1: "WARNING", 2: "CRITICAL"}
    print(f"  OVERALL STATUS: {labels.get(exit_code, 'UNKNOWN')}")
    print("=" * 50)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

---

## Bucket Audit

Authenticates to the ECS REST API, iterates all namespaces and their buckets, and prints a report of bucket name, owner, total size, and object count. Flags any bucket whose size exceeds a configurable threshold.

~~~python
#!/usr/bin/env python3
# ecs_bucket_audit.py — Audit all ECS namespaces and buckets via REST API
# Requirements: requests
# Usage: ECS_HOST=ecs01.example.com ECS_USER=sysadmin ECS_PASS=secret \
#        WARN_SIZE_GB=500 ./ecs_bucket_audit.py

import os
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ECS_HOST    = os.environ.get("ECS_HOST", "")
ECS_USER    = os.environ.get("ECS_USER", "sysadmin")
ECS_PASS    = os.environ.get("ECS_PASS", "")
WARN_SIZE_GB = int(os.environ.get("WARN_SIZE_GB", "500"))
BASE_URL    = f"https://{ECS_HOST}:4443"

if not ECS_HOST or not ECS_PASS:
    print("ERROR: ECS_HOST and ECS_PASS must be set.", file=sys.stderr)
    sys.exit(1)


def authenticate(session):
    resp = session.get(f"{BASE_URL}/login", auth=(ECS_USER, ECS_PASS), verify=False)
    resp.raise_for_status()
    token = resp.headers.get("X-SDS-AUTH-TOKEN")
    if not token:
        raise RuntimeError("No auth token received.")
    return token


def api_get(session, token, path):
    resp = session.get(
        f"{BASE_URL}{path}",
        headers={"X-SDS-AUTH-TOKEN": token, "Accept": "application/json"},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()


def bytes_to_gb(b):
    try:
        return float(b) / (1024 ** 3)
    except (TypeError, ValueError):
        return 0.0


def main():
    session = requests.Session()

    print(f"{'NAMESPACE':<25}  {'BUCKET':<30}  {'OWNER':<20}  {'SIZE (GB)':>10}  {'OBJECTS':>10}  FLAG")
    print("-" * 110)

    token = authenticate(session)

    # List namespaces
    ns_data = api_get(session, token, "/object/namespaces")
    namespaces = ns_data.get("namespace", [])

    flagged = 0
    for ns in namespaces:
        ns_name = ns.get("name", "unknown")

        try:
            bucket_data = api_get(session, token, f"/object/bucket?namespace={ns_name}")
            buckets = bucket_data.get("object_bucket", [])
        except Exception as e:
            print(f"  ERROR listing buckets for namespace {ns_name}: {e}")
            continue

        for bucket in buckets:
            bname   = bucket.get("name", "unknown")
            owner   = bucket.get("owner", "unknown")
            size_b  = bucket.get("total_size", 0)
            obj_cnt = bucket.get("total_objects", 0)
            size_gb = bytes_to_gb(size_b)
            flag    = ""
            if size_gb >= WARN_SIZE_GB:
                flag = f"  <<< OVER {WARN_SIZE_GB} GB"
                flagged += 1
            print(f"{ns_name:<25}  {bname:<30}  {owner:<20}  {size_gb:>10.2f}  {obj_cnt:>10}  {flag}")

    # Logout
    try:
        session.get(f"{BASE_URL}/logout",
                    headers={"X-SDS-AUTH-TOKEN": token}, verify=False)
    except Exception:
        pass

    print("-" * 110)
    print(f"\nTotal buckets flagged over {WARN_SIZE_GB} GB threshold: {flagged}")
    sys.exit(0 if flagged == 0 else 1)


if __name__ == "__main__":
    main()
~~~

---

## S3 Connectivity Check

Uses the AWS CLI with a custom `--endpoint-url` to test S3 connectivity to an ECS cluster. Performs list, put, get, and delete operations against a test bucket and prints PASS/FAIL for each step.

~~~bash
#!/bin/bash
# ecs_s3_check.sh — S3 connectivity check against Dell ECS using the AWS CLI
# Requirements: aws CLI installed and on PATH
# Usage:
#   ECS_S3_ENDPOINT=https://ecs01.example.com:9021
#   AWS_ACCESS_KEY_ID=mykey
#   AWS_SECRET_ACCESS_KEY=mysecret
#   TEST_BUCKET=s3-check-bucket
#   ./ecs_s3_check.sh

set -uo pipefail

ECS_S3_ENDPOINT="${ECS_S3_ENDPOINT:-}"
AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-}"
AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-}"
TEST_BUCKET="${TEST_BUCKET:-ecs-connectivity-test}"
TEST_KEY="ecs-check-$(date +%s).txt"
TEST_CONTENT="ECS S3 connectivity check object"
TMP_FILE=$(mktemp)
PASS=0
FAIL=0

export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
# Prevent AWS CLI from looking for a region in config — ECS doesn't need it
export AWS_DEFAULT_REGION="us-east-1"

if [[ -z "$ECS_S3_ENDPOINT" || -z "$AWS_ACCESS_KEY_ID" || -z "$AWS_SECRET_ACCESS_KEY" ]]; then
  echo "ERROR: ECS_S3_ENDPOINT, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY must be set."
  exit 1
fi

S3_OPTS="--endpoint-url ${ECS_S3_ENDPOINT} --no-verify-ssl"

check() {
  local step="$1"
  local result="$2"
  if [[ "$result" -eq 0 ]]; then
    printf "  %-30s  PASS\n" "$step"
    PASS=$((PASS + 1))
  else
    printf "  %-30s  FAIL\n" "$step"
    FAIL=$((FAIL + 1))
  fi
}

echo "========================================"
echo "  ECS S3 Connectivity Check"
echo "  Endpoint : $ECS_S3_ENDPOINT"
echo "  Bucket   : $TEST_BUCKET"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Step 1: List bucket
aws s3 ls "s3://${TEST_BUCKET}" $S3_OPTS > /dev/null 2>&1
check "List bucket" $?

# Step 2: Put test object
echo "$TEST_CONTENT" > "$TMP_FILE"
aws s3 cp "$TMP_FILE" "s3://${TEST_BUCKET}/${TEST_KEY}" $S3_OPTS > /dev/null 2>&1
check "Put test object" $?

# Step 3: Get test object back
GET_TMP=$(mktemp)
aws s3 cp "s3://${TEST_BUCKET}/${TEST_KEY}" "$GET_TMP" $S3_OPTS > /dev/null 2>&1
GET_RESULT=$?
if [[ $GET_RESULT -eq 0 ]]; then
  CONTENT=$(cat "$GET_TMP")
  if [[ "$CONTENT" == "$TEST_CONTENT" ]]; then
    check "Get test object (content match)" 0
  else
    check "Get test object (content match)" 1
  fi
else
  check "Get test object" $GET_RESULT
fi
rm -f "$GET_TMP"

# Step 4: Delete test object
aws s3 rm "s3://${TEST_BUCKET}/${TEST_KEY}" $S3_OPTS > /dev/null 2>&1
check "Delete test object" $?

# Cleanup
rm -f "$TMP_FILE"

echo ""
echo "========================================"
echo "  Results: $PASS passed, $FAIL failed"
echo "========================================"

[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
~~~
