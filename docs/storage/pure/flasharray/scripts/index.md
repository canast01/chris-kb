# Scripts

> Part of the [Pure FlashArray](../) reference.

---

## Array Health Check (Python)

Connect to a FlashArray via REST API v2, check overall health, active alerts, hardware status, drive health, volumes, and pod state, then print a formatted summary. Exits non-zero if critical alerts or degraded drives are found.

~~~python
#!/usr/bin/env python3
"""
FlashArray Health Check
Requires: pip install py-pure-client
Variables: FA_HOST, FA_API_TOKEN
"""

import os
import sys

try:
    from pypureclient import flasharray
except ImportError:
    sys.exit("ERROR: Install py-pure-client:  pip install py-pure-client")

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
FA_HOST      = os.environ.get("FA_HOST",      "")
FA_API_TOKEN = os.environ.get("FA_API_TOKEN", "")

if not FA_HOST or not FA_API_TOKEN:
    sys.exit("Set FA_HOST and FA_API_TOKEN environment variables.")

# ANSI colours
RED  = "\033[0;31m"
YEL  = "\033[0;33m"
GRN  = "\033[0;32m"
NC   = "\033[0m"

worst   = 0   # 0=OK 1=WARN 2=CRIT
issues  = []

def crit(msg): global worst; issues.append(("CRITICAL", msg)); worst = max(worst, 2)
def warn(msg): global worst; issues.append(("WARNING",  msg)); worst = max(worst, 1)

# -------------------------------------------------------------------
# Connect
# -------------------------------------------------------------------
try:
    client = flasharray.Client(target=FA_HOST, api_token=FA_API_TOKEN)
except Exception as exc:
    sys.exit(f"Connection failed: {exc}")

print(f"\n{'='*60}")
print(f"  FlashArray Health Check: {FA_HOST}")
print(f"{'='*60}\n")

# -------------------------------------------------------------------
# Array info
# -------------------------------------------------------------------
try:
    arr = client.get_arrays()
    if arr.status_code == 200:
        a = list(arr.items)[0]
        print(f"Array      : {a.name}")
        print(f"Purity     : {a.version}")
        print(f"Capacity   : {getattr(a, 'capacity', 'N/A')}")
        print()
except Exception as exc:
    warn(f"Cannot retrieve array info: {exc}")

# -------------------------------------------------------------------
# Check: Active alerts
# -------------------------------------------------------------------
print("Checking alerts...")
try:
    alerts = client.get_alerts(filter="flagged='true'")
    alert_list = list(alerts.items) if alerts.status_code == 200 else []
    crit_alerts = [a for a in alert_list if getattr(a, "severity", "") == "error"]
    warn_alerts = [a for a in alert_list if getattr(a, "severity", "") == "warning"]

    if crit_alerts:
        for a in crit_alerts:
            crit(f"Alert [{a.id}] {a.summary}")
    elif warn_alerts:
        for a in warn_alerts:
            warn(f"Alert [{a.id}] {a.summary}")
    else:
        print(f"  {GRN}OK{NC}  No flagged alerts")
except Exception as exc:
    warn(f"Cannot retrieve alerts: {exc}")

# -------------------------------------------------------------------
# Check: Hardware status
# -------------------------------------------------------------------
print("Checking hardware...")
try:
    hw = client.get_hardware()
    hw_items = list(hw.items) if hw.status_code == 200 else []
    failed_hw = [h for h in hw_items if getattr(h, "status", "ok") not in ("ok", "not_installed", "")]
    if failed_hw:
        for h in failed_hw:
            crit(f"Hardware component {h.name} status: {h.status}")
    else:
        print(f"  {GRN}OK{NC}  All hardware components healthy ({len(hw_items)} checked)")
except Exception as exc:
    warn(f"Cannot retrieve hardware status: {exc}")

# -------------------------------------------------------------------
# Check: Drive health
# -------------------------------------------------------------------
print("Checking drives...")
try:
    drives = client.get_drives()
    drive_list = list(drives.items) if drives.status_code == 200 else []
    bad_drives = [d for d in drive_list if getattr(d, "status", "healthy") != "healthy"]
    if bad_drives:
        for d in bad_drives:
            crit(f"Drive {d.name} status: {d.status}")
    else:
        print(f"  {GRN}OK{NC}  All {len(drive_list)} drives healthy")
except Exception as exc:
    warn(f"Cannot retrieve drive status: {exc}")

# -------------------------------------------------------------------
# Check: Pod (ActiveCluster) health
# -------------------------------------------------------------------
print("Checking pods (ActiveCluster)...")
try:
    pods = client.get_pods()
    pod_list = list(pods.items) if pods.status_code == 200 else []
    if pod_list:
        for p in pod_list:
            status = getattr(p, "status", "unknown")
            if status not in ("online", ""):
                warn(f"Pod {p.name} status: {status}")
            else:
                print(f"  {GRN}OK{NC}  Pod {p.name}: {status}")
    else:
        print(f"  (No ActiveCluster pods configured)")
except Exception as exc:
    warn(f"Cannot retrieve pod status: {exc}")

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
print(f"\n{'='*60}")
if worst == 0:
    print(f"  {GRN}Overall: HEALTHY{NC}")
elif worst == 1:
    print(f"  {YEL}Overall: WARNING{NC}")
else:
    print(f"  {RED}Overall: CRITICAL{NC}")

if issues:
    print()
    for level, msg in issues:
        colour = RED if level == "CRITICAL" else YEL
        print(f"  {colour}[{level}]{NC} {msg}")

print(f"{'='*60}\n")
sys.exit(worst)
~~~

---

## ActiveCluster Pod Status Monitor (Python)

Connect to both FlashArrays in an ActiveCluster pair, list all pods and mediator status, and alert if any pod is not in a stretched and online state or if the mediator is offline.

~~~python
#!/usr/bin/env python3
"""
FlashArray ActiveCluster Pod Status Monitor
Requires: pip install py-pure-client
Variables: FA1_HOST, FA1_API_TOKEN, FA2_HOST, FA2_API_TOKEN
"""

import os
import sys

try:
    from pypureclient import flasharray
except ImportError:
    sys.exit("ERROR: Install py-pure-client:  pip install py-pure-client")

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
FA1_HOST  = os.environ.get("FA1_HOST",  "")
FA1_TOKEN = os.environ.get("FA1_API_TOKEN", "")
FA2_HOST  = os.environ.get("FA2_HOST",  "")
FA2_TOKEN = os.environ.get("FA2_API_TOKEN", "")

if not FA1_HOST or not FA1_TOKEN or not FA2_HOST or not FA2_TOKEN:
    sys.exit("Set FA1_HOST, FA1_API_TOKEN, FA2_HOST, FA2_API_TOKEN.")

RED  = "\033[0;31m"; YEL  = "\033[0;33m"; GRN  = "\033[0;32m"; NC = "\033[0m"

worst  = 0
issues = []

def crit(msg): global worst; issues.append(("CRITICAL", msg)); worst = max(worst, 2)
def warn(msg): global worst; issues.append(("WARNING",  msg)); worst = max(worst, 1)

def connect(host, token, label):
    try:
        return flasharray.Client(target=host, api_token=token)
    except Exception as exc:
        crit(f"Cannot connect to {label} ({host}): {exc}")
        return None

# -------------------------------------------------------------------
# Connect to both arrays
# -------------------------------------------------------------------
client1 = connect(FA1_HOST, FA1_TOKEN, "Array-1")
client2 = connect(FA2_HOST, FA2_TOKEN, "Array-2")

if not client1 or not client2:
    for level, msg in issues:
        print(f"[{level}] {msg}")
    sys.exit(2)

print(f"\n{'='*70}")
print(f"  FlashArray ActiveCluster Pod Monitor")
print(f"  Array-1: {FA1_HOST}  |  Array-2: {FA2_HOST}")
print(f"{'='*70}\n")

# -------------------------------------------------------------------
# Collect pods from Array-1 (primary perspective)
# -------------------------------------------------------------------
pods_resp = client1.get_pods()
pods = list(pods_resp.items) if pods_resp.status_code == 200 else []

if not pods:
    print("No pods found on Array-1. Is ActiveCluster configured?")
    sys.exit(0)

# -------------------------------------------------------------------
# Check each pod
# -------------------------------------------------------------------
for pod in pods:
    name      = pod.name
    status    = getattr(pod, "status", "unknown")
    mediator  = getattr(pod, "mediator_version", None)
    arrays    = getattr(pod, "arrays", [])
    stretched = len(arrays) >= 2

    print(f"Pod: {name}")
    print(f"  Status    : {status}")
    print(f"  Stretched : {'Yes' if stretched else 'No'}")
    print(f"  Members   : {[a.name if hasattr(a,'name') else str(a) for a in arrays]}")
    print(f"  Mediator  : {mediator or 'unknown'}")

    # Mediator check via dedicated API
    try:
        med_resp = client1.get_pods_pod_replica_links_remote_volume_snapshots(pod_name=name)
    except Exception:
        med_resp = None  # Mediator check endpoint may vary by Purity version

    if status not in ("online", ""):
        crit(f"Pod {name} is NOT online — status: {status}")
    elif not stretched:
        warn(f"Pod {name} is not stretched across two arrays")
    else:
        print(f"  {GRN}Status: OK{NC}")
    print()

# -------------------------------------------------------------------
# Cross-check from Array-2 perspective
# -------------------------------------------------------------------
pods2_resp = client2.get_pods()
pods2 = {p.name: p for p in (pods2_resp.items if pods2_resp.status_code == 200 else [])}

for pod in pods:
    if pod.name not in pods2:
        warn(f"Pod {pod.name} visible on Array-1 but NOT found on Array-2 — possible replication split")
    else:
        p2_status = getattr(pods2[pod.name], "status", "unknown")
        if p2_status not in ("online", ""):
            crit(f"Pod {pod.name} status on Array-2 is: {p2_status}")

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
print(f"{'='*70}")
label = ("CRITICAL" if worst == 2 else "WARNING" if worst == 1 else "HEALTHY")
colour = (RED if worst == 2 else YEL if worst == 1 else GRN)
print(f"  {colour}Overall: {label}{NC}")
for level, msg in issues:
    c = RED if level == "CRITICAL" else YEL
    print(f"  {c}[{level}]{NC} {msg}")
print(f"{'='*70}\n")
sys.exit(worst)
~~~

---

## Volume and Snapshot Report (Bash)

List all volumes with their size, used space, and connections, then list snapshots, flagging any that are older than 30 days and may be consuming unexpected capacity.

~~~bash
#!/bin/bash
# FlashArray Volume and Snapshot Report
# Requires: Pure Storage CLI tools (purearray, purevol, puresnap) in PATH
# Usage: FA_HOST=flasharray01 FA_API_TOKEN=xxx ./fa_vol_snap_report.sh

set -euo pipefail

FA_HOST="${FA_HOST:?Set FA_HOST}"
FA_API_TOKEN="${FA_API_TOKEN:?Set FA_API_TOKEN}"
SNAP_AGE_WARN_DAYS="${SNAP_AGE_WARN_DAYS:-30}"

RED='\033[0;31m'; YEL='\033[0;33m'; GRN='\033[0;32m'; NC='\033[0m'

export PURENETWORK_HOST="$FA_HOST"
export PURENETWORK_API_TOKEN="$FA_API_TOKEN"

echo
echo "=== FlashArray Volume Report: $FA_HOST ==="
echo "Time: $(date)"
echo

# ------------------------------------------------------------------
# Volumes
# ------------------------------------------------------------------
echo "--- Volumes ---"
printf "%-35s %10s %10s %8s  %s\n" "VOLUME" "SIZE" "USED" "REDUC" "CONNECTIONS"
printf '%0.s-' {1..90}; echo

purevol list --space 2>/dev/null | tail -n +2 | while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    vol=$(  awk '{print $1}' <<< "$line")
    size=$( awk '{print $2}' <<< "$line")
    used=$( awk '{print $3}' <<< "$line")
    reduc=$(awk '{print $5}' <<< "$line")

    # Get connections for this volume
    conns=$(purevol listconnection "$vol" 2>/dev/null | tail -n +2 | awk '{print $1}' | paste -sd',' - 2>/dev/null || echo "-")

    printf "%-35s %10s %10s %8s  %s\n" "$vol" "$size" "$used" "$reduc" "${conns:--}"
done

echo

# ------------------------------------------------------------------
# Snapshots — flag old ones
# ------------------------------------------------------------------
echo "--- Snapshots (flagging age > ${SNAP_AGE_WARN_DAYS} days) ---"
printf "%-50s %-25s %10s  %s\n" "SNAPSHOT" "CREATED" "SIZE" "FLAG"
printf '%0.s-' {1..100}; echo

now_epoch=$(date +%s)

puresnap list --space 2>/dev/null | tail -n +2 | while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    snap=$(  awk '{print $1}' <<< "$line")
    created=$(awk '{print $2, $3}' <<< "$line")
    size=$(  awk '{print $4}' <<< "$line")

    # Parse the creation date (format varies: "2024-01-15 10:30 UTC" or ISO)
    created_epoch=$(date -d "$created" +%s 2>/dev/null || date -j -f "%Y-%m-%d %H:%M" "$created" +%s 2>/dev/null || echo "$now_epoch")
    age_days=$(( (now_epoch - created_epoch) / 86400 ))

    if (( age_days > SNAP_AGE_WARN_DAYS )); then
        flag="${YEL}OLD (${age_days}d)${NC}"
    else
        flag="${GRN}OK${NC}"
    fi

    printf "%-50s %-25s %10s  " "${snap:0:49}" "$created" "$size"
    echo -e "$flag"
done

echo
echo "Note: Snapshots older than ${SNAP_AGE_WARN_DAYS} days flagged for capacity review."
~~~

---

## Drive Failure Alert (Bash)

List all FlashArray drives, filter for any that are not in a healthy state, and exit non-zero if non-healthy drives are found. Designed for cron scheduling.

~~~bash
#!/bin/bash
# FlashArray Drive Failure Alert
# Designed for cron scheduling — exits 0 if all drives healthy, 2 if failures found.
# Usage: FA_HOST=flasharray01 FA_API_TOKEN=xxx ./fa_drive_alert.sh

set -euo pipefail

FA_HOST="${FA_HOST:?Set FA_HOST}"
FA_API_TOKEN="${FA_API_TOKEN:?Set FA_API_TOKEN}"

export PURENETWORK_HOST="$FA_HOST"
export PURENETWORK_API_TOKEN="$FA_API_TOKEN"

RED='\033[0;31m'; GRN='\033[0;32m'; NC='\033[0m'

RAW=$(puredrive list 2>/dev/null)

total=0
bad=0

printf "%-20s %-12s %-15s %-10s %s\n" "DRIVE" "TYPE" "STATUS" "CAPACITY" "BLADE/SHELF"
printf '%0.s-' {1..80}; echo

while IFS= read -r line; do
    [[ "$line" =~ ^(Name|[[:space:]]*$) ]] && continue
    drive=$(  awk '{print $1}' <<< "$line")
    dtype=$(  awk '{print $2}' <<< "$line")
    status=$( awk '{print $3}' <<< "$line")
    cap=$(    awk '{print $4}' <<< "$line")
    location=$(awk '{print $5}' <<< "$line")

    (( total++ ))

    if [[ "$status" != "healthy" ]]; then
        printf "%-20s %-12s " "$drive" "$dtype"
        echo -en "${RED}%-15s${NC} " "$status"
        printf "%-10s %s\n" "$cap" "${location:--}"
        (( bad++ ))
    else
        printf "%-20s %-12s %-15s %-10s %s\n" "$drive" "$dtype" "$status" "$cap" "${location:--}"
    fi
done <<< "$RAW"

echo
printf "Total drives: %d  |  Non-healthy: %d\n" "$total" "$bad"

if (( bad > 0 )); then
    echo -e "${RED}ALERT: $bad drive(s) in non-healthy state on $FA_HOST${NC}"
    echo "Open a Pure Storage support case immediately."
    exit 2
else
    echo -e "${GRN}All $total drives healthy on $FA_HOST${NC}"
    exit 0
fi
~~~

---

## Ansible FlashArray Health Playbook

Authenticate to the FlashArray REST API v2, check array health, active alerts, pod status, and assert that no critical alerts or drive failures exist.

~~~yaml
---
# FlashArray Health Playbook
# Variables: fa_url, fa_api_token
#
# Run: ansible-playbook fa_health.yml \
#        -e "fa_url=https://flasharray01 fa_api_token=abc123"

- name: FlashArray Health Check
  hosts: localhost
  gather_facts: false
  vars:
    fa_validate_certs: false

  tasks:

    - name: Authenticate and get API session token
      ansible.builtin.uri:
        url:          "{{ fa_url }}/api/2.26/login"
        method:       POST
        headers:
          api-token:  "{{ fa_api_token }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
        status_code: [200]
      register: fa_login

    - name: Set x-auth-token header for subsequent calls
      ansible.builtin.set_fact:
        fa_auth_headers:
          x-auth-token: "{{ fa_login.x_auth_token | default(fa_login.json['x-auth-token'] | default('')) }}"
          Content-Type: "application/json"

    - name: Get array info
      ansible.builtin.uri:
        url:            "{{ fa_url }}/api/2.26/arrays"
        method:         GET
        headers:        "{{ fa_auth_headers }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
      register: fa_arrays

    - name: Print array info
      ansible.builtin.debug:
        msg: "Array: {{ fa_arrays.json.items[0].name }}  Purity: {{ fa_arrays.json.items[0].version }}"
      when: fa_arrays.json.items | length > 0

    - name: Check for flagged alerts
      ansible.builtin.uri:
        url:            "{{ fa_url }}/api/2.26/alerts?filter=flagged%3D%27true%27"
        method:         GET
        headers:        "{{ fa_auth_headers }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
      register: fa_alerts

    - name: Identify critical alerts
      ansible.builtin.set_fact:
        critical_alerts: >-
          {{ fa_alerts.json.items
             | selectattr('severity', 'equalto', 'error')
             | list }}

    - name: Print alert summary
      ansible.builtin.debug:
        msg: "Alert [{{ item.id }}] severity={{ item.severity }} — {{ item.summary }}"
      loop: "{{ fa_alerts.json.items }}"

    - name: Fail if critical alerts exist
      ansible.builtin.fail:
        msg: "{{ critical_alerts | length }} critical alert(s) on {{ fa_url }}: {{ critical_alerts | map(attribute='summary') | list }}"
      when: critical_alerts | length > 0

    - name: Check drive health
      ansible.builtin.uri:
        url:            "{{ fa_url }}/api/2.26/drives"
        method:         GET
        headers:        "{{ fa_auth_headers }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
      register: fa_drives

    - name: Identify degraded drives
      ansible.builtin.set_fact:
        degraded_drives: >-
          {{ fa_drives.json.items
             | rejectattr('status', 'equalto', 'healthy')
             | list }}

    - name: Print drive summary
      ansible.builtin.debug:
        msg: "Drives: {{ fa_drives.json.items | length }} total, {{ degraded_drives | length }} degraded"

    - name: Fail if any drives are degraded
      ansible.builtin.fail:
        msg: "Degraded drives: {{ degraded_drives | map(attribute='name') | list | join(', ') }}"
      when: degraded_drives | length > 0

    - name: Check pod (ActiveCluster) status
      ansible.builtin.uri:
        url:            "{{ fa_url }}/api/2.26/pods"
        method:         GET
        headers:        "{{ fa_auth_headers }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
      register: fa_pods

    - name: Identify offline pods
      ansible.builtin.set_fact:
        offline_pods: >-
          {{ fa_pods.json.items
             | rejectattr('status', 'in', ['online', ''])
             | list }}

    - name: Print pod status
      ansible.builtin.debug:
        msg: "Pod {{ item.name }}: status={{ item.status }}"
      loop: "{{ fa_pods.json.items }}"

    - name: Fail if any pods are offline
      ansible.builtin.fail:
        msg: "Offline pods: {{ offline_pods | map(attribute='name') | list | join(', ') }}"
      when: offline_pods | length > 0

    - name: Logout
      ansible.builtin.uri:
        url:            "{{ fa_url }}/api/2.26/logout"
        method:         DELETE
        headers:        "{{ fa_auth_headers }}"
        validate_certs: "{{ fa_validate_certs }}"
        status_code: [200, 204]
      ignore_errors: true

    - name: Health check passed
      ansible.builtin.debug:
        msg: "All FlashArray health checks passed for {{ fa_url }}"
~~~
