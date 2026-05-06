# Scripts

> Part of the [Dell Secure Connect Gateway](../) reference.

---

## Connectivity Health Check

Tests outbound HTTPS connectivity from the SCG host to the required Dell support endpoints, checks the SCG service status, and prints a PASS/FAIL summary for each check. Suitable for cron or a monitoring probe.

~~~bash
#!/bin/bash
# scg_connectivity_check.sh — Secure Connect Gateway connectivity health check
# Run this script ON the SCG appliance or Linux host running the SCG service.
# Usage: ./scg_connectivity_check.sh

set -uo pipefail

PASS=0
FAIL=0

DELL_ENDPOINTS=(
  "https://esrs.emc.com"
  "https://cloudiq.dell.com"
  "https://download.emc.com"
  "https://support.dell.com"
)

SCG_LOCAL_API="https://localhost:9443/scg/api/v1/system/version"

check() {
  local label="$1"
  local result="$2"
  if [[ "$result" -eq 0 ]]; then
    printf "  %-50s  PASS\n" "$label"
    PASS=$((PASS + 1))
  else
    printf "  %-50s  FAIL\n" "$label"
    FAIL=$((FAIL + 1))
  fi
}

echo ""
echo "========================================"
echo "  SCG Connectivity Health Check"
echo "  Host : $(hostname -f 2>/dev/null || hostname)"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# --- Outbound endpoint reachability ---
echo "--- Outbound Dell Endpoint Reachability ---"
for endpoint in "${DELL_ENDPOINTS[@]}"; do
  curl -so /dev/null --max-time 10 --connect-timeout 8 "$endpoint" 2>/dev/null
  check "$endpoint" $?
done

# --- SCG service ---
echo ""
echo "--- SCG Service Status ---"
if command -v systemctl &>/dev/null; then
  systemctl is-active --quiet dell-scg 2>/dev/null
  check "dell-scg systemd service active" $?
else
  service dell-scg status &>/dev/null
  check "dell-scg init.d service active" $?
fi

# --- SCG local API ---
echo ""
echo "--- SCG Local API ---"
SCG_PASS="${SCG_PASS:-admin}"
API_RESP=$(curl -sk --max-time 10 -u "admin:${SCG_PASS}" "$SCG_LOCAL_API" 2>/dev/null)
if echo "$API_RESP" | grep -q "version"; then
  check "SCG local API reachable" 0
  SCG_VER=$(echo "$API_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('version','unknown'))" 2>/dev/null || echo "unknown")
  echo "  SCG Version: $SCG_VER"
else
  check "SCG local API reachable" 1
fi

echo ""
echo "========================================"
echo "  Results: $PASS passed, $FAIL failed"
echo "========================================"

[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
~~~

---

## Device Registration Auditor

Queries the SCG REST API to list all registered devices, checks each device's connectivity status, and flags any device that is not in a connected/active state. Useful for quarterly audits and decommission cleanup.

~~~python
#!/usr/bin/env python3
# scg_device_audit.py — Audit registered devices on Dell Secure Connect Gateway
# Run on the SCG host or any host with network access to the SCG management interface.
# Requirements: requests
# Usage: SCG_HOST=scg01.example.com SCG_PASS=admin123 ./scg_device_audit.py

import os
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCG_HOST  = os.environ.get("SCG_HOST", "localhost")
SCG_USER  = os.environ.get("SCG_USER", "admin")
SCG_PASS  = os.environ.get("SCG_PASS", "")
SCG_PORT  = os.environ.get("SCG_PORT", "9443")
BASE_URL  = f"https://{SCG_HOST}:{SCG_PORT}/scg/api/v1"

if not SCG_PASS:
    print("ERROR: SCG_PASS must be set.", file=sys.stderr)
    sys.exit(1)

session = requests.Session()
AUTH = (SCG_USER, SCG_PASS)


def api_get(path):
    resp = session.get(f"{BASE_URL}{path}", auth=AUTH, verify=False, timeout=15)
    resp.raise_for_status()
    return resp.json()


def main():
    print("=" * 70)
    print(f"  SCG Device Registration Audit — {SCG_HOST}")
    print("=" * 70)

    # Get SCG version
    try:
        ver_data = api_get("/system/version")
        print(f"\n  SCG Version: {ver_data.get('version', 'unknown')}")
    except Exception as e:
        print(f"  WARNING: Could not retrieve SCG version: {e}")

    # List devices
    try:
        devices_data = api_get("/devices")
        devices = devices_data.get("devices", devices_data if isinstance(devices_data, list) else [])
    except Exception as e:
        print(f"\nERROR: Could not list devices: {e}")
        sys.exit(2)

    if not devices:
        print("\n  No devices registered.")
        sys.exit(0)

    not_connected = 0
    print(f"\n{'DEVICE NAME':<35}  {'TYPE':<20}  {'IP/HOST':<20}  {'STATUS'}")
    print("-" * 90)

    for dev in devices:
        name   = dev.get("name",   dev.get("hostname",  "unknown"))
        dtype  = dev.get("type",   dev.get("deviceType","unknown"))
        ip     = dev.get("ip",     dev.get("address",   "unknown"))
        status = dev.get("status", dev.get("connectivity", dev.get("state", "unknown"))).upper()

        marker = ""
        if status not in ("CONNECTED", "ACTIVE", "OK"):
            marker = "  <<< NOT CONNECTED"
            not_connected += 1

        print(f"{name:<35}  {dtype:<20}  {ip:<20}  {status}{marker}")

    print("-" * 90)
    print(f"\nTotal: {len(devices)} devices   Not connected: {not_connected}")

    if not_connected > 0:
        print(f"\nWARNING: {not_connected} device(s) not connected. "
              "Re-register from the array side or remove stale entries.")
        sys.exit(1)
    else:
        print("\nOK: All registered devices are connected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
~~~

---

## Ansible SCG Status Playbook

Playbook targeting the SCG host. Checks the SCG service status, verifies outbound connectivity to Dell endpoints, queries the local API for registered devices, and fails if any device is disconnected or the service is not running.

~~~yaml
---
# scg_status.yml — Ansible status check playbook for Dell Secure Connect Gateway
# Inventory host: scg (the SCG appliance or Linux host running dell-scg)
# Usage: ansible-playbook -i inventory scg_status.yml

- name: Dell Secure Connect Gateway Status Check
  hosts: scg
  gather_facts: false
  vars:
    scg_user: admin
    scg_pass: "{{ vault_scg_pass }}"
    scg_port: 9443
    dell_endpoints:
      - "https://esrs.emc.com"
      - "https://cloudiq.dell.com"

  tasks:
    - name: Check SCG service is running
      ansible.builtin.shell: |
        systemctl is-active dell-scg 2>/dev/null || service dell-scg status 2>/dev/null
      register: scg_service
      changed_when: false
      failed_when: false

    - name: Show SCG service status
      ansible.builtin.debug:
        msg: "{{ scg_service.stdout_lines }}"

    - name: Fail if SCG service is not active
      ansible.builtin.fail:
        msg: "dell-scg service is not running on {{ inventory_hostname }}"
      when: "'active' not in scg_service.stdout and 'running' not in scg_service.stdout"

    - name: Test outbound connectivity to Dell endpoints
      ansible.builtin.shell: >
        curl -so /dev/null --max-time 10 --connect-timeout 8 {{ item }} && echo PASS || echo FAIL
      loop: "{{ dell_endpoints }}"
      register: connectivity_results
      changed_when: false

    - name: Show connectivity results
      ansible.builtin.debug:
        msg: "{{ item.item }}: {{ item.stdout }}"
      loop: "{{ connectivity_results.results }}"
      loop_control:
        label: "{{ item.item }}"

    - name: Fail if any Dell endpoint is unreachable
      ansible.builtin.fail:
        msg: "Connectivity to {{ item.item }} FAILED on {{ inventory_hostname }}"
      when: "'FAIL' in item.stdout"
      loop: "{{ connectivity_results.results }}"
      loop_control:
        label: "{{ item.item }}"

    - name: Query SCG registered devices
      ansible.builtin.uri:
        url: "https://{{ inventory_hostname }}:{{ scg_port }}/scg/api/v1/devices"
        method: GET
        user: "{{ scg_user }}"
        password: "{{ scg_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
      register: devices_resp

    - name: Show registered devices
      ansible.builtin.debug:
        msg: "{{ devices_resp.json }}"

    - name: All checks passed
      ansible.builtin.debug:
        msg: "SCG health check completed successfully on {{ inventory_hostname }}."
~~~
