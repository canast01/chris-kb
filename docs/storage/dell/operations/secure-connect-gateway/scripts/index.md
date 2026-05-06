# Scripts

> Part of the [Secure Connect Gateway Operations](../) reference.

---

## Multi-Site SCG Health Poller

Polls the local SCG REST API on multiple SCG appliances (from a management host) and prints a consolidated health summary: service reachability, version, and device connection count. Exits non-zero if any SCG is unreachable or has disconnected devices.

~~~bash
#!/bin/bash
# scg_fleet_health.sh — Poll multiple SCG appliances and report health
# Usage:
#   SCG_HOSTS="scg01.site1.example.com scg02.site2.example.com" \
#   SCG_PASS=admin123 ./scg_fleet_health.sh

set -uo pipefail

SCG_HOSTS="${SCG_HOSTS:-}"
SCG_USER="${SCG_USER:-admin}"
SCG_PASS="${SCG_PASS:-}"
SCG_PORT="${SCG_PORT:-9443}"

if [[ -z "$SCG_HOSTS" || -z "$SCG_PASS" ]]; then
  echo "ERROR: SCG_HOSTS and SCG_PASS must be set." >&2
  exit 1
fi

PASS=0
FAIL=0

echo ""
echo "========================================"
echo "  SCG Fleet Health Poll"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
printf "\n%-35s  %-12s  %-8s  %-12s  %s\n" \
  "SCG HOST" "VERSION" "DEVICES" "NOT-CONN" "STATUS"
printf "%s\n" "----------------------------------------------------------------------"

for SCG_HOST in $SCG_HOSTS; do
  BASE_URL="https://${SCG_HOST}:${SCG_PORT}/scg/api/v1"

  # Get version
  VER_JSON=$(curl -sk --max-time 10 -u "${SCG_USER}:${SCG_PASS}" \
    "${BASE_URL}/system/version" 2>/dev/null || echo "{}")
  VERSION=$(echo "$VER_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('version','N/A'))" 2>/dev/null || echo "UNREACHABLE")

  if [[ "$VERSION" == "UNREACHABLE" || "$VERSION" == "N/A" ]]; then
    printf "%-35s  %-12s  %-8s  %-12s  FAIL — unreachable\n" \
      "$SCG_HOST" "N/A" "N/A" "N/A"
    FAIL=$((FAIL + 1))
    continue
  fi

  # Get devices
  DEV_JSON=$(curl -sk --max-time 15 -u "${SCG_USER}:${SCG_PASS}" \
    "${BASE_URL}/devices" 2>/dev/null || echo "{}")
  TOTAL=$(echo "$DEV_JSON" | python3 -c "
import sys, json
d = json.load(sys.stdin)
devs = d.get('devices', d if isinstance(d, list) else [])
print(len(devs))
" 2>/dev/null || echo "0")

  NOT_CONN=$(echo "$DEV_JSON" | python3 -c "
import sys, json
d = json.load(sys.stdin)
devs = d.get('devices', d if isinstance(d, list) else [])
not_conn = [x for x in devs if str(x.get('status', x.get('state', x.get('connectivity', '')))).upper()
            not in ('CONNECTED', 'ACTIVE', 'OK')]
print(len(not_conn))
" 2>/dev/null || echo "0")

  if [[ "$NOT_CONN" -gt 0 ]]; then
    STATUS="WARN — ${NOT_CONN} disconnected"
    FAIL=$((FAIL + 1))
  else
    STATUS="OK"
    PASS=$((PASS + 1))
  fi

  printf "%-35s  %-12s  %-8s  %-12s  %s\n" \
    "$SCG_HOST" "$VERSION" "$TOTAL" "$NOT_CONN" "$STATUS"
done

echo ""
echo "========================================"
echo "  Results: $PASS healthy, $FAIL issues"
echo "========================================"
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
~~~

---

## Device Registration Diff Tool

Compares the list of devices registered on an SCG against an expected inventory file. Reports devices that are registered but not in the expected list (stale) and devices in the expected list but not registered (missing). Useful for quarterly audits.

~~~python
#!/usr/bin/env python3
# scg_registration_diff.py — Diff SCG registered devices against expected inventory
# Requirements: requests
# Inventory file format (one hostname or IP per line, lines starting with # are comments):
#   # Site A arrays
#   powermax01.example.com
#   unity01.example.com
#
# Usage: SCG_HOST=scg01 SCG_PASS=admin123 INVENTORY=expected_devices.txt ./scg_registration_diff.py

import os
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCG_HOST      = os.environ.get("SCG_HOST", "localhost")
SCG_USER      = os.environ.get("SCG_USER", "admin")
SCG_PASS      = os.environ.get("SCG_PASS", "")
SCG_PORT      = os.environ.get("SCG_PORT", "9443")
INVENTORY_FILE= os.environ.get("INVENTORY", "expected_devices.txt")
BASE_URL      = f"https://{SCG_HOST}:{SCG_PORT}/scg/api/v1"

if not SCG_PASS:
    print("ERROR: SCG_PASS must be set.", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(INVENTORY_FILE):
    print(f"ERROR: Inventory file not found: {INVENTORY_FILE}", file=sys.stderr)
    sys.exit(1)

session = requests.Session()


def get_registered_devices():
    resp = session.get(f"{BASE_URL}/devices", auth=(SCG_USER, SCG_PASS), verify=False, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    devs = data.get("devices", data if isinstance(data, list) else [])
    return {
        d.get("name", d.get("hostname", d.get("ip", "unknown"))).lower()
        for d in devs
    }


def load_inventory():
    expected = set()
    with open(INVENTORY_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            expected.add(line.lower())
    return expected


def main():
    print("=" * 55)
    print(f"  SCG Device Registration Diff — {SCG_HOST}")
    print("=" * 55)

    try:
        registered = get_registered_devices()
    except Exception as e:
        print(f"ERROR: Could not retrieve registered devices: {e}")
        sys.exit(2)

    expected = load_inventory()

    stale   = registered - expected   # In SCG but not in inventory (possibly decommissioned)
    missing = expected - registered   # In inventory but not in SCG (need to register)

    print(f"\n  Registered in SCG : {len(registered)}")
    print(f"  Expected inventory: {len(expected)}")
    print(f"  Stale (extra)     : {len(stale)}")
    print(f"  Missing           : {len(missing)}")

    if stale:
        print(f"\n--- Stale (registered but not in expected inventory) ---")
        for d in sorted(stale):
            print(f"  {d}  <<< consider removing if decommissioned")

    if missing:
        print(f"\n--- Missing (in inventory but NOT registered) ---")
        for d in sorted(missing):
            print(f"  {d}  <<< re-register from array management interface")

    if not stale and not missing:
        print("\nOK: Registered devices match expected inventory exactly.")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
~~~

---

## Ansible SCG Remediation Playbook

Playbook targeting one or more SCG hosts. Checks the SCG service, restarts it if not running, verifies outbound Dell endpoint connectivity, and outputs device registration counts. Designed for post-incident remediation.

~~~yaml
---
# scg_remediate.yml — Ansible SCG remediation and validation playbook
# Inventory group: scg_hosts
# Usage: ansible-playbook -i inventory scg_remediate.yml

- name: SCG Remediation and Validation
  hosts: scg_hosts
  gather_facts: false
  vars:
    scg_user: admin
    scg_pass: "{{ vault_scg_pass }}"
    scg_port: 9443
    dell_endpoints:
      - "https://esrs.emc.com"
      - "https://cloudiq.dell.com"

  tasks:
    - name: Check SCG service status
      ansible.builtin.shell: |
        systemctl is-active dell-scg 2>/dev/null && echo ACTIVE || echo INACTIVE
      register: scg_status
      changed_when: false

    - name: Start SCG service if not active
      ansible.builtin.systemd:
        name: dell-scg
        state: started
        enabled: true
      when: "'INACTIVE' in scg_status.stdout"
      become: true

    - name: Wait for SCG API to become available
      ansible.builtin.uri:
        url: "https://{{ inventory_hostname }}:{{ scg_port }}/scg/api/v1/system/version"
        method: GET
        user: "{{ scg_user }}"
        password: "{{ scg_pass }}"
        force_basic_auth: true
        validate_certs: false
        status_code: 200
      register: api_wait
      retries: 6
      delay: 10
      until: api_wait.status == 200

    - name: Show SCG version
      ansible.builtin.debug:
        msg: "SCG version: {{ api_wait.json.version | default('unknown') }}"

    - name: Test outbound Dell endpoint connectivity
      ansible.builtin.shell: >
        curl -so /dev/null --max-time 10 --connect-timeout 8 {{ item }} && echo PASS || echo FAIL
      loop: "{{ dell_endpoints }}"
      register: conn_results
      changed_when: false

    - name: Report connectivity
      ansible.builtin.debug:
        msg: "{{ item.item }}: {{ item.stdout }}"
      loop: "{{ conn_results.results }}"
      loop_control:
        label: "{{ item.item }}"

    - name: Fail if any Dell endpoint unreachable
      ansible.builtin.fail:
        msg: "Cannot reach {{ item.item }} from {{ inventory_hostname }} — check firewall rules."
      when: "'FAIL' in item.stdout"
      loop: "{{ conn_results.results }}"
      loop_control:
        label: "{{ item.item }}"

    - name: Get registered device count
      ansible.builtin.uri:
        url: "https://{{ inventory_hostname }}:{{ scg_port }}/scg/api/v1/devices"
        method: GET
        user: "{{ scg_user }}"
        password: "{{ scg_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
      register: devices_resp

    - name: Report device count
      ansible.builtin.debug:
        msg: >
          SCG {{ inventory_hostname }} is healthy.
          Registered devices: {{ (devices_resp.json.devices | default([])) | length }}.
          Verify all expected arrays appear as Connected in the SCG GUI.
~~~
