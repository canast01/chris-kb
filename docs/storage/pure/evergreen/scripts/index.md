# Scripts

> Part of the [Pure Storage Evergreen](../) reference.

---

## Pre-Upgrade Path Validation (Bash)

Before a Purity upgrade or Evergreen controller refresh, validate host paths, pod stretch status, mediator reachability, and snapshot count to produce a go/no-go checklist.

~~~bash
#!/bin/bash
# Evergreen Pre-Upgrade Path Validation
# Prints a go/no-go checklist before a Purity upgrade or controller refresh.
# Usage: FA_HOST=flasharray01 FA_API_TOKEN=xxx ./pre_upgrade_validate.sh

set -euo pipefail

FA_HOST="${FA_HOST:?Set FA_HOST}"
FA_API_TOKEN="${FA_API_TOKEN:?Set FA_API_TOKEN}"
MEDIATOR_HOST="${FA_MEDIATOR_HOST:-}"   # optional: override mediator IP check

export PURENETWORK_HOST="$FA_HOST"
export PURENETWORK_API_TOKEN="$FA_API_TOKEN"

GRN='\033[0;32m'; RED='\033[0;31m'; YEL='\033[0;33m'; NC='\033[0m'
PASS=0; WARN=0; FAIL=0

pass()  { echo -e "  ${GRN}[GO]${NC}     $*"; (( PASS++ )); }
warn()  { echo -e "  ${YEL}[WARN]${NC}   $*"; (( WARN++ )); }
fail()  { echo -e "  ${RED}[NO-GO]${NC}  $*"; (( FAIL++ )); }

echo
echo "==================================================="
echo " Evergreen Pre-Upgrade Readiness Checklist"
echo " Array : $FA_HOST"
echo " Time  : $(date)"
echo "==================================================="
echo

# -------------------------------------------------------------------
# Check 1: Array reachable
# -------------------------------------------------------------------
echo "[ 1 ] Array reachability"
if purearray list &>/dev/null; then
    FA_VER=$(purearray list 2>/dev/null | awk 'NR==2{print $2}')
    pass "Array $FA_HOST is reachable — Purity version: ${FA_VER:-unknown}"
else
    fail "Cannot reach array $FA_HOST — check network and API token"
fi

# -------------------------------------------------------------------
# Check 2: Ports online
# -------------------------------------------------------------------
echo "[ 2 ] Port status"
OFFLINE_PORTS=$(pureport list 2>/dev/null | awk 'NR>1 && $3!="online" {print $1}' | paste -sd',' -)
if [[ -z "$OFFLINE_PORTS" ]]; then
    PORT_COUNT=$(pureport list 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
    pass "All $PORT_COUNT ports are online"
else
    fail "Offline ports: $OFFLINE_PORTS — resolve before upgrade"
fi

# -------------------------------------------------------------------
# Check 3: Host paths — check each host has >= 2 paths
# -------------------------------------------------------------------
echo "[ 3 ] Host multipath validation"
SINGLE_PATH_HOSTS=""
while IFS= read -r line; do
    [[ "$line" =~ ^(Name|[[:space:]]*$) ]] && continue
    host=$(awk '{print $1}' <<< "$line")
    paths=$(purehost listconnection "$host" 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
    if (( paths < 2 )); then
        SINGLE_PATH_HOSTS+="$host (${paths} path)  "
    fi
done < <(purehost list 2>/dev/null)

if [[ -z "$SINGLE_PATH_HOSTS" ]]; then
    pass "All hosts have >= 2 paths"
else
    fail "Single-path hosts (UPGRADE BLOCKER): $SINGLE_PATH_HOSTS"
fi

# -------------------------------------------------------------------
# Check 4: Pods stretched and mediator reachable
# -------------------------------------------------------------------
echo "[ 4 ] ActiveCluster pods and mediator"
POD_OUT=$(purepod list 2>/dev/null)
if [[ $(echo "$POD_OUT" | tail -n +2 | wc -l) -eq 0 ]]; then
    warn "No ActiveCluster pods configured (skipping mediator check)"
else
    UNSTRETCHED=""
    while IFS= read -r pline; do
        [[ "$pline" =~ ^(Name|[[:space:]]*$) ]] && continue
        pod_name=$(awk '{print $1}' <<< "$pline")
        pod_status=$(awk '{print $2}' <<< "$pline")
        if [[ "$pod_status" != "online" ]]; then
            UNSTRETCHED+="$pod_name (status=$pod_status)  "
        fi
    done < <(echo "$POD_OUT")

    if [[ -z "$UNSTRETCHED" ]]; then
        pass "All pods are online"
    else
        fail "Pods not online: $UNSTRETCHED"
    fi

    # Mediator connectivity
    MED_HOST=$(purepod list --mediator 2>/dev/null | awk 'NR==2{print $NF}' || true)
    if [[ -z "$MED_HOST" ]]; then
        MED_HOST="$MEDIATOR_HOST"
    fi

    if [[ -n "$MED_HOST" ]]; then
        if curl -sk --max-time 5 "https://${MED_HOST}/mediator/version" &>/dev/null; then
            pass "Mediator reachable: $MED_HOST"
        else
            fail "Mediator NOT reachable: $MED_HOST — resolve before upgrade"
        fi
    else
        warn "Cannot determine mediator host — verify manually"
    fi
fi

# -------------------------------------------------------------------
# Check 5: Snapshot count (high counts slow upgrade)
# -------------------------------------------------------------------
echo "[ 5 ] Snapshot count"
SNAP_COUNT=$(puresnap list 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
if (( SNAP_COUNT < 5000 )); then
    pass "Snapshot count: $SNAP_COUNT"
elif (( SNAP_COUNT < 20000 )); then
    warn "Snapshot count is high ($SNAP_COUNT) — upgrade may take longer; consider cleanup"
else
    fail "Snapshot count very high ($SNAP_COUNT) — eradicate old snapshots before upgrade"
fi

# -------------------------------------------------------------------
# Check 6: Active alerts
# -------------------------------------------------------------------
echo "[ 6 ] Active hardware/software alerts"
ALERT_COUNT=$(purealert list 2>/dev/null | tail -n +2 | grep -c '\S' || true)
if (( ALERT_COUNT == 0 )); then
    pass "No active alerts"
else
    CRIT_ALERTS=$(purealert list 2>/dev/null | tail -n +2 | grep -i 'critical' || true)
    if [[ -n "$CRIT_ALERTS" ]]; then
        fail "$ALERT_COUNT alert(s) open including critical — resolve before upgrade"
    else
        warn "$ALERT_COUNT warning alert(s) open — review before upgrade"
    fi
fi

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
echo
echo "==================================================="
echo " Results: GO=$PASS  WARN=$WARN  NO-GO=$FAIL"
if (( FAIL > 0 )); then
    echo -e " ${RED}VERDICT: NOT READY FOR UPGRADE${NC} — resolve NO-GO items first"
    exit 2
elif (( WARN > 0 )); then
    echo -e " ${YEL}VERDICT: PROCEED WITH CAUTION${NC} — review warnings before starting"
    exit 1
else
    echo -e " ${GRN}VERDICT: READY FOR UPGRADE${NC}"
    exit 0
fi
~~~

---

## Upgrade Readiness Check (Python)

Use the FlashArray REST API to assess upgrade readiness: check the current Purity version, outstanding alerts, pending drive rebuilds, and pod sync state, then print a formatted readiness report with blockers highlighted.

~~~python
#!/usr/bin/env python3
"""
FlashArray Upgrade Readiness Check (Evergreen)
Requires: pip install py-pure-client tabulate
Variables: FA_HOST, FA_API_TOKEN
"""

import os
import sys

try:
    from pypureclient import flasharray
    from tabulate import tabulate
except ImportError:
    sys.exit("ERROR: pip install py-pure-client tabulate")

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
FA_HOST  = os.environ.get("FA_HOST",      "")
FA_TOKEN = os.environ.get("FA_API_TOKEN", "")

if not FA_HOST or not FA_TOKEN:
    sys.exit("Set FA_HOST and FA_API_TOKEN.")

RED  = "\033[0;31m"; YEL  = "\033[0;33m"; GRN  = "\033[0;32m"; NC = "\033[0m"
BOLD = "\033[1m"

checks   = []   # list of (check_name, status, detail)
blockers = []

def add_check(name, status, detail):
    checks.append((name, status, detail))
    if status == "BLOCKER":
        blockers.append(f"{name}: {detail}")

# -------------------------------------------------------------------
# Connect
# -------------------------------------------------------------------
try:
    client = flasharray.Client(target=FA_HOST, api_token=FA_TOKEN)
except Exception as exc:
    sys.exit(f"Connection failed: {exc}")

print(f"\n{BOLD}FlashArray Upgrade Readiness Report{NC}")
print(f"Array: {FA_HOST}  |  Generated: {__import__('datetime').datetime.now():%Y-%m-%d %H:%M}\n")

# -------------------------------------------------------------------
# Check: Array version
# -------------------------------------------------------------------
try:
    arr_resp = client.get_arrays()
    if arr_resp.status_code == 200:
        a = list(arr_resp.items)[0]
        ver = a.version
        add_check("Purity Version", "INFO", ver)
except Exception as exc:
    add_check("Purity Version", "WARN", f"Cannot retrieve: {exc}")

# -------------------------------------------------------------------
# Check: Outstanding alerts
# -------------------------------------------------------------------
try:
    alerts_resp = client.get_alerts(filter="flagged='true'")
    alerts = list(alerts_resp.items) if alerts_resp.status_code == 200 else []
    crit_alerts = [a for a in alerts if getattr(a, "severity", "") == "error"]
    if crit_alerts:
        add_check("Active Alerts", "BLOCKER",
                  f"{len(crit_alerts)} critical alert(s): {', '.join(a.summary for a in crit_alerts[:3])}")
    elif alerts:
        add_check("Active Alerts", "WARN",
                  f"{len(alerts)} warning alert(s) — review before upgrade")
    else:
        add_check("Active Alerts", "OK", "No flagged alerts")
except Exception as exc:
    add_check("Active Alerts", "WARN", f"Cannot check: {exc}")

# -------------------------------------------------------------------
# Check: Drive rebuilds (non-healthy drives)
# -------------------------------------------------------------------
try:
    drives_resp = client.get_drives()
    drives = list(drives_resp.items) if drives_resp.status_code == 200 else []
    rebuilding = [d for d in drives if getattr(d, "status", "healthy") in ("evacuating", "recovering")]
    failed     = [d for d in drives if getattr(d, "status", "healthy") == "failed"]

    if failed:
        add_check("Drive Status", "BLOCKER",
                  f"{len(failed)} failed drive(s): {', '.join(d.name for d in failed)}")
    elif rebuilding:
        add_check("Drive Status", "WARN",
                  f"{len(rebuilding)} drive(s) rebuilding — upgrade will take longer but is not blocked")
    else:
        add_check("Drive Status", "OK", f"All {len(drives)} drives healthy")
except Exception as exc:
    add_check("Drive Status", "WARN", f"Cannot check: {exc}")

# -------------------------------------------------------------------
# Check: Pod sync (ActiveCluster)
# -------------------------------------------------------------------
try:
    pods_resp = client.get_pods()
    pods = list(pods_resp.items) if pods_resp.status_code == 200 else []
    if pods:
        offline_pods = [p for p in pods if getattr(p, "status", "online") not in ("online", "")]
        if offline_pods:
            add_check("ActiveCluster Pods", "BLOCKER",
                      f"{len(offline_pods)} pod(s) not online: {', '.join(p.name for p in offline_pods)}")
        else:
            add_check("ActiveCluster Pods", "OK", f"All {len(pods)} pod(s) online")
    else:
        add_check("ActiveCluster Pods", "INFO", "No pods configured")
except Exception as exc:
    add_check("ActiveCluster Pods", "WARN", f"Cannot check: {exc}")

# -------------------------------------------------------------------
# Print report table
# -------------------------------------------------------------------
rows = []
for check, status, detail in checks:
    if status == "BLOCKER":
        colour, sym = RED, "BLOCKER"
    elif status == "WARN":
        colour, sym = YEL, "WARN"
    elif status == "OK":
        colour, sym = GRN, "OK"
    else:
        colour, sym = NC,  "INFO"

    rows.append([check, f"{colour}{sym}{NC}", detail])

print(tabulate(rows, headers=["Check", "Status", "Detail"], tablefmt="simple"))
print()

if blockers:
    print(f"{RED}UPGRADE BLOCKERS:{NC}")
    for b in blockers:
        print(f"  {RED}x{NC} {b}")
    print()
    print(f"{RED}This array is NOT ready for upgrade. Resolve blockers first.{NC}")
    sys.exit(2)
else:
    warnings = [(n, d) for n, s, d in checks if s == "WARN"]
    if warnings:
        print(f"{YEL}Warnings (review before proceeding):{NC}")
        for n, d in warnings:
            print(f"  {YEL}!{NC} {n}: {d}")
        print()
    print(f"{GRN}No blockers found — array is ready for upgrade.{NC}")
    sys.exit(0)
~~~

---

## Ansible Pre-Upgrade Playbook

Run pre-upgrade readiness checks across an entire FlashArray fleet — retrieve current Purity version, check for active alerts, validate drive health, verify ActiveCluster pod health, and assert there are no blockers before proceeding with any upgrade.

~~~yaml
---
# Evergreen Pre-Upgrade Fleet Check Playbook
# Inventory group: flasharrays
# Host vars: fa_api_token (per host, from vault)
#
# Run: ansible-playbook evergreen_pre_upgrade.yml -i inventory/flasharrays.yml

- name: Evergreen Pre-Upgrade Readiness Check
  hosts: flasharrays
  gather_facts: false
  vars:
    fa_validate_certs: false

  tasks:

    # ---------------------------------------------------------------
    # Authenticate
    # ---------------------------------------------------------------
    - name: Authenticate to FlashArray REST API
      ansible.builtin.uri:
        url:          "https://{{ inventory_hostname }}/api/2.26/login"
        method:       POST
        headers:
          api-token:  "{{ fa_api_token }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
        status_code: [200]
      register: fa_login

    - name: Store auth token
      ansible.builtin.set_fact:
        fa_auth:
          x-auth-token: "{{ fa_login.x_auth_token | default('') }}"
          Content-Type: "application/json"

    # ---------------------------------------------------------------
    # Check 1: Current Purity version
    # ---------------------------------------------------------------
    - name: Get current Purity version
      ansible.builtin.uri:
        url:            "https://{{ inventory_hostname }}/api/2.26/arrays"
        method:         GET
        headers:        "{{ fa_auth }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
      register: fa_arrays

    - name: Report Purity version
      ansible.builtin.debug:
        msg: "{{ inventory_hostname }}: Purity version = {{ fa_arrays.json.items[0].version }}"
      when: fa_arrays.json.items | length > 0

    # ---------------------------------------------------------------
    # Check 2: Active alerts
    # ---------------------------------------------------------------
    - name: Get flagged alerts
      ansible.builtin.uri:
        url:            "https://{{ inventory_hostname }}/api/2.26/alerts?filter=flagged%3D%27true%27"
        method:         GET
        headers:        "{{ fa_auth }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
      register: fa_alerts

    - name: Identify critical alerts
      ansible.builtin.set_fact:
        critical_alerts: >-
          {{ fa_alerts.json.items
             | selectattr('severity', 'equalto', 'error')
             | list }}

    - name: Assert no critical alerts
      ansible.builtin.assert:
        that: critical_alerts | length == 0
        fail_msg: >-
          {{ inventory_hostname }} has {{ critical_alerts | length }} critical alert(s) —
          upgrade BLOCKED.
        success_msg: "{{ inventory_hostname }}: No critical alerts."

    # ---------------------------------------------------------------
    # Check 3: Drive health
    # ---------------------------------------------------------------
    - name: Get drive status
      ansible.builtin.uri:
        url:            "https://{{ inventory_hostname }}/api/2.26/drives"
        method:         GET
        headers:        "{{ fa_auth }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
      register: fa_drives

    - name: Identify failed drives
      ansible.builtin.set_fact:
        failed_drives: >-
          {{ fa_drives.json.items
             | selectattr('status', 'equalto', 'failed')
             | list }}

    - name: Assert no failed drives
      ansible.builtin.assert:
        that: failed_drives | length == 0
        fail_msg: >-
          {{ inventory_hostname }} has {{ failed_drives | length }} failed drive(s):
          {{ failed_drives | map(attribute='name') | list | join(', ') }} — upgrade BLOCKED.
        success_msg: "{{ inventory_hostname }}: All drives healthy."

    # ---------------------------------------------------------------
    # Check 4: ActiveCluster pod health
    # ---------------------------------------------------------------
    - name: Get pod status
      ansible.builtin.uri:
        url:            "https://{{ inventory_hostname }}/api/2.26/pods"
        method:         GET
        headers:        "{{ fa_auth }}"
        validate_certs: "{{ fa_validate_certs }}"
        return_content: true
      register: fa_pods

    - name: Identify offline pods
      ansible.builtin.set_fact:
        offline_pods: >-
          {{ fa_pods.json.items
             | rejectattr('status', 'in', ['online', ''])
             | list }}

    - name: Assert all pods are online
      ansible.builtin.assert:
        that: offline_pods | length == 0
        fail_msg: >-
          {{ inventory_hostname }} has offline pod(s):
          {{ offline_pods | map(attribute='name') | list | join(', ') }} — upgrade BLOCKED.
        success_msg: >-
          {{ inventory_hostname }}: {{ fa_pods.json.items | length }} pod(s) all online.

    # ---------------------------------------------------------------
    # Per-host readiness summary
    # ---------------------------------------------------------------
    - name: Host readiness summary
      ansible.builtin.debug:
        msg: >-
          {{ inventory_hostname }} READY FOR UPGRADE
          | Purity: {{ fa_arrays.json.items[0].version | default('unknown') }}
          | Alerts: {{ fa_alerts.json.items | length }}
          | Drives: {{ fa_drives.json.items | length }} total
          | Pods: {{ fa_pods.json.items | length }}

    # ---------------------------------------------------------------
    # Logout
    # ---------------------------------------------------------------
    - name: Logout from REST API
      ansible.builtin.uri:
        url:            "https://{{ inventory_hostname }}/api/2.26/logout"
        method:         DELETE
        headers:        "{{ fa_auth }}"
        validate_certs: "{{ fa_validate_certs }}"
        status_code: [200, 204]
      ignore_errors: true
~~~
