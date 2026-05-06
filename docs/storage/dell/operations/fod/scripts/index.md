# Scripts

> Part of the [FOD Operations](../) reference.

---

## CloudIQ Burst Usage Reporter

Queries CloudIQ for all FOD-enrolled systems and reports current consumption vs. committed baseline. Identifies systems currently in burst and outputs a summary suitable for a billing review meeting.

~~~python
#!/usr/bin/env python3
# fod_ops_burst_reporter.py — FOD burst usage report via CloudIQ REST API
# Requirements: requests
# Usage: CLOUDIQ_CLIENT_ID=xxx CLOUDIQ_CLIENT_SECRET=yyy ./fod_ops_burst_reporter.py

import os
import sys
import requests
from datetime import datetime

CLIENT_ID     = os.environ.get("CLOUDIQ_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("CLOUDIQ_CLIENT_SECRET", "")
CLOUDIQ_BASE  = "https://cloudiq.dell.com"
API_BASE      = f"{CLOUDIQ_BASE}/cloudiq/rest/v1"

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: CLOUDIQ_CLIENT_ID and CLOUDIQ_CLIENT_SECRET must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()


def get_token():
    resp = session.post(
        f"{CLOUDIQ_BASE}/auth/v1/token",
        data={"grant_type": "client_credentials",
              "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def api_get(token, path, params=None):
    resp = session.get(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    token = get_token()

    systems_data = api_get(token, "/storage-systems")
    systems      = systems_data.get("results", [])

    print("=" * 80)
    print("  FOD Burst Usage Report")
    print(f"  Billing Period: {datetime.now().strftime('%Y-%m')}")
    print(f"  Generated    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    total_burst = 0.0
    burst_systems = []

    print(f"\n{'SYSTEM':<30}  {'TYPE':<15}  {'COMMITTED':>12}  {'USED':>12}  {'BURST':>10}  STATUS")
    print("-" * 90)

    for sys_obj in systems:
        sys_id   = sys_obj.get("id", "unknown")
        sys_name = sys_obj.get("system_name", sys_obj.get("name", sys_id))
        sys_type = sys_obj.get("system_type", sys_obj.get("type", "unknown"))

        try:
            cap = api_get(token, f"/storage-systems/{sys_id}/capacity")
        except Exception:
            cap = {}

        committed = float(cap.get("committed_tib", 0))
        used      = float(cap.get("used_tib", 0))
        burst     = max(0.0, used - committed)

        if burst > 0:
            status = "IN BURST"
            total_burst += burst
            burst_systems.append(sys_name)
        elif committed > 0 and used / committed >= 0.9:
            status = "NEAR LIMIT"
        else:
            status = "OK"

        c_str = f"{committed:.2f} TiB" if committed else "N/A"
        u_str = f"{used:.2f} TiB"      if used      else "N/A"
        b_str = f"{burst:.2f} TiB"     if burst > 0 else "-"

        print(f"{sys_name:<30}  {sys_type:<15}  {c_str:>12}  {u_str:>12}  {b_str:>10}  {status}")

    print("-" * 90)
    print(f"\nTotal burst across all systems: {total_burst:.2f} TiB")
    print(f"Systems in burst: {len(burst_systems)}")
    if burst_systems:
        for s in burst_systems:
            print(f"  - {s}")
    print("\nAction: Cross-reference with APEX Console → Billing & Usage before month close.")
    sys.exit(1 if burst_systems else 0)


if __name__ == "__main__":
    main()
~~~

---

## Month-End Billing Extractor

Extracts CloudIQ capacity utilisation history for the current calendar month for all storage systems and outputs it as CSV. Designed to be run on the last working day of the month and archived for finance reconciliation.

~~~bash
#!/bin/bash
# fod_month_end_extract.sh — Extract CloudIQ capacity data for FOD billing reconciliation
# Requirements: curl, jq
# Usage: CLOUDIQ_CLIENT_ID=xxx CLOUDIQ_CLIENT_SECRET=yyy ./fod_month_end_extract.sh > fod_$(date +%Y%m).csv

set -euo pipefail

CLIENT_ID="${CLOUDIQ_CLIENT_ID:-}"
CLIENT_SECRET="${CLOUDIQ_CLIENT_SECRET:-}"
CLOUDIQ_BASE="https://cloudiq.dell.com"
API_BASE="${CLOUDIQ_BASE}/cloudiq/rest/v1"

if [[ -z "$CLIENT_ID" || -z "$CLIENT_SECRET" ]]; then
  echo "ERROR: CLOUDIQ_CLIENT_ID and CLOUDIQ_CLIENT_SECRET must be set." >&2
  exit 1
fi

# Get token
TOKEN=$(curl -s -X POST "${CLOUDIQ_BASE}/auth/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}" \
  | jq -r '.access_token')

if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
  echo "ERROR: Failed to get CloudIQ token." >&2
  exit 1
fi

AUTH_HEADER="Authorization: Bearer ${TOKEN}"

# Get list of systems
SYSTEMS=$(curl -s -H "$AUTH_HEADER" "${API_BASE}/storage-systems" | jq -r '.results[]? | [.id, .system_name, .system_type] | @tsv')

# Print CSV header
echo "system_id,system_name,system_type,committed_tib,used_tib,burst_tib,report_date"

REPORT_DATE=$(date '+%Y-%m-%d')

while IFS=$'\t' read -r SID SNAME STYPE; do
  [[ -z "$SID" ]] && continue

  CAP=$(curl -s -H "$AUTH_HEADER" "${API_BASE}/storage-systems/${SID}/capacity" 2>/dev/null || echo "{}")
  COMMITTED=$(echo "$CAP" | jq -r '.committed_tib // 0')
  USED=$(echo "$CAP"      | jq -r '.used_tib // 0')
  BURST=$(echo "$COMMITTED $USED" | awk '{b=$2-$1; print (b>0)?b:0}')

  echo "${SID},${SNAME},${STYPE},${COMMITTED},${USED},${BURST},${REPORT_DATE}"
done <<< "$SYSTEMS"
~~~

---

## Ansible FOD Audit Playbook

Playbook targeting localhost. Retrieves CloudIQ capacity data for all storage systems, prints a burst summary, and fails the play if any system is in burst — suitable for a scheduled monthly audit run.

~~~yaml
---
# fod_ops_audit.yml — Ansible FOD burst audit playbook
# Usage: ansible-playbook fod_ops_audit.yml

- name: FOD Monthly Burst Audit
  hosts: localhost
  gather_facts: false
  vars:
    cloudiq_base: "https://cloudiq.dell.com"
    client_id: "{{ lookup('env', 'CLOUDIQ_CLIENT_ID') }}"
    client_secret: "{{ lookup('env', 'CLOUDIQ_CLIENT_SECRET') }}"

  tasks:
    - name: Authenticate to CloudIQ
      ansible.builtin.uri:
        url: "{{ cloudiq_base }}/auth/v1/token"
        method: POST
        body_format: form-urlencoded
        body:
          grant_type: client_credentials
          client_id: "{{ client_id }}"
          client_secret: "{{ client_secret }}"
        return_content: true
      register: auth_resp
      no_log: true

    - name: Set token
      ansible.builtin.set_fact:
        ciq_token: "{{ auth_resp.json.access_token }}"
      no_log: true

    - name: Get all storage systems
      ansible.builtin.uri:
        url: "{{ cloudiq_base }}/cloudiq/rest/v1/storage-systems"
        headers:
          Authorization: "Bearer {{ ciq_token }}"
        return_content: true
      register: systems_resp

    - name: Get capacity for each system
      ansible.builtin.uri:
        url: "{{ cloudiq_base }}/cloudiq/rest/v1/storage-systems/{{ item.id }}/capacity"
        headers:
          Authorization: "Bearer {{ ciq_token }}"
        return_content: true
      loop: "{{ systems_resp.json.results | default([]) }}"
      loop_control:
        label: "{{ item.system_name | default(item.id) }}"
      register: cap_results
      ignore_errors: true

    - name: Report capacity per system
      ansible.builtin.debug:
        msg: >
          {{ item.item.system_name | default(item.item.id) }}:
          committed={{ item.json.committed_tib | default('N/A') }} TiB,
          used={{ item.json.used_tib | default('N/A') }} TiB
      loop: "{{ cap_results.results }}"
      loop_control:
        label: "{{ item.item.system_name | default(item.item.id) }}"

    - name: Notify on burst systems
      ansible.builtin.debug:
        msg: >
          FOD audit complete. Review results above and compare committed vs used
          for each system. Any system where used_tib exceeds committed_tib is in
          burst and will incur additional FOD charges this billing period.
~~~
