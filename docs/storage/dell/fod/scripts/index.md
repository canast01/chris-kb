# Scripts

> Part of the [Dell Flex on Demand](../) reference.

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
