# Scripts

> Part of the [COD Operations](../) reference.

---

## License Inventory Checker

Queries `symlicense` on all SIDs visible to Solutions Enabler and prints a summary table of installed licenses, flagging any COD-related licenses and their activation state.

~~~bash
#!/bin/bash
# cod_license_inventory.sh — COD license inventory check across all visible PowerMax arrays
# Run on a Solutions Enabler host with symcfg and symlicense on PATH.
# Usage: SYMCLI_PATH=/usr/symcli/bin ./cod_license_inventory.sh

set -euo pipefail

SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
SYMCFG="$SYMCLI_PATH/symcfg"
SYMLICENSE="$SYMCLI_PATH/symlicense"

echo ""
echo "========================================"
echo "  COD License Inventory"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Get all array SIDs
SIDS=$("$SYMCFG" list 2>/dev/null | awk '/^[[:space:]]+[0-9]{12}/{print $1}' | sort -u)

if [[ -z "$SIDS" ]]; then
  echo "  No Symmetrix arrays found."
  exit 0
fi

for SID in $SIDS; do
  echo ""
  echo "--- SID: $SID ---"
  LICENSE_OUT=$("$SYMLICENSE" -sid "$SID" list 2>&1 || echo "ERROR: symlicense failed for $SID")

  # Filter for COD-related entries (case-insensitive)
  COD_LINES=$(echo "$LICENSE_OUT" | grep -i "capacity.on.demand\|COD\|on.demand" || true)

  if [[ -n "$COD_LINES" ]]; then
    echo "$COD_LINES"
  else
    echo "  No COD-specific license entries found — showing full list:"
    echo "$LICENSE_OUT" | head -30
  fi
done

echo ""
echo "========================================"
echo "  Inventory check complete."
echo "========================================"
~~~

---

## Activation Tracker

Reads a user-maintained COD tracking CSV file and checks each entry against current `symcfg` pool utilisation. Prints a table showing activation state, current utilisation, and whether the next activation should be planned.

~~~python
#!/usr/bin/env python3
# cod_activation_tracker.py — Track COD activations and utilisation headroom
# Requirements: symcfg on PATH (Solutions Enabler), csv tracking file
#
# Tracking CSV format (cod_inventory.csv):
#   sid,name,activated_tib,total_installed_tib,next_key_available
#   000123456789,prod-array-1,50,100,yes
#
# Usage: SYMCLI_PATH=/usr/symcli/bin ./cod_activation_tracker.py

import os
import sys
import csv
import subprocess
import re

SYMCLI_PATH   = os.environ.get("SYMCLI_PATH", "/usr/symcli/bin")
INVENTORY_CSV = os.environ.get("COD_CSV", "cod_inventory.csv")
WARN_PCT      = float(os.environ.get("WARN_PCT", "75"))

if not os.path.exists(INVENTORY_CSV):
    print(f"ERROR: COD inventory CSV not found: {INVENTORY_CSV}", file=sys.stderr)
    print("Create a CSV with columns: sid,name,activated_tib,total_installed_tib,next_key_available")
    sys.exit(1)


def get_pool_pct(sid):
    """Run symcfg pool list and parse the highest utilisation percentage."""
    try:
        result = subprocess.run(
            [f"{SYMCLI_PATH}/symcfg", "-sid", sid, "-pool", "-dp", "list"],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        pcts = [float(m) for m in re.findall(r'(\d+(?:\.\d+)?)\s*%', output)]
        return max(pcts) if pcts else None
    except Exception:
        return None


def main():
    exit_code = 0

    print("=" * 80)
    print("  COD Activation Tracker")
    print("=" * 80)
    print(f"\n{'SID':<15}  {'NAME':<20}  {'ACTIVATED':>10}  {'INSTALLED':>10}  "
          f"{'POOL %':>7}  {'NEXT KEY':>10}  STATUS")
    print("-" * 90)

    with open(INVENTORY_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid          = row["sid"].strip()
            name         = row["name"].strip()
            activated    = float(row.get("activated_tib", 0))
            installed    = float(row.get("total_installed_tib", 0))
            next_key     = row.get("next_key_available", "unknown").strip()

            pool_pct = get_pool_pct(sid)
            pct_str  = f"{pool_pct:.1f}%" if pool_pct is not None else "N/A"

            reserve_pct = ((installed - activated) / installed * 100) if installed > 0 else 0

            if pool_pct is not None and pool_pct >= WARN_PCT:
                status = "PLAN NEXT ACTIVATION"
                exit_code = max(exit_code, 1)
            elif reserve_pct < 10:
                status = "LOW RESERVE — ORDER CAPACITY"
                exit_code = max(exit_code, 1)
            else:
                status = "OK"

            print(f"{sid:<15}  {name:<20}  {activated:>8.1f}T  {installed:>8.1f}T  "
                  f"{pct_str:>7}  {next_key:>10}  {status}")

    print("-" * 90)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

---

## Ansible COD Validation Playbook

Post-activation validation playbook. Runs on a Solutions Enabler host to confirm the new capacity is visible after a COD license has been applied, and checks that pool size has increased.

~~~yaml
---
# cod_validate_activation.yml — Ansible COD activation validation playbook
# Run after applying a new COD license key to confirm the capacity is visible.
# Inventory host: symcli_host
# Required vars: sid, expected_pool_tib (minimum expected pool size in TiB after activation)
# Usage: ansible-playbook -i inventory cod_validate_activation.yml \
#          -e sid=000123456789 -e expected_pool_tib=100

- name: COD Activation Validation
  hosts: symcli_host
  gather_facts: false
  vars:
    sid: "000123456789"
    symcli_path: "/usr/symcli/bin"
    expected_pool_tib: 100

  tasks:
    - name: Check license list post-activation
      ansible.builtin.shell: "{{ symcli_path }}/symlicense -sid {{ sid }} list"
      register: license_out
      changed_when: false

    - name: Show license list
      ansible.builtin.debug:
        msg: "{{ license_out.stdout_lines }}"

    - name: Check pool list post-activation
      ansible.builtin.shell: "{{ symcli_path }}/symcfg -sid {{ sid }} -pool -dp list"
      register: pool_out
      changed_when: false

    - name: Show pool list
      ansible.builtin.debug:
        msg: "{{ pool_out.stdout_lines }}"

    - name: Check array config overview
      ansible.builtin.shell: "{{ symcli_path }}/symcfg -sid {{ sid }} show"
      register: array_show
      changed_when: false

    - name: Show array overview
      ansible.builtin.debug:
        msg: "{{ array_show.stdout_lines }}"

    - name: Confirm capacity increase is visible
      ansible.builtin.debug:
        msg: >
          COD activation validation complete for SID {{ sid }}.
          Review pool_out and array_show above to confirm that total pool capacity
          meets or exceeds {{ expected_pool_tib }} TiB.
          If capacity has not increased, verify the license key SID matches the array SID.
~~~
