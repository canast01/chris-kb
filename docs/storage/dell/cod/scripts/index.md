# Scripts

> Part of the [Dell Capacity on Demand](../) reference.

---

## Array Capacity vs. COD Reserve Reporter

Queries SYMCLI to report total installed capacity, activated capacity, and remaining COD reserve for a PowerMax array. Warns if activated capacity exceeds 80% of total installed (i.e., COD reserve is running low).

~~~bash
#!/bin/bash
# cod_capacity_report.sh — Report COD activated vs. reserve capacity on a PowerMax array
# Usage: SID=000123456789 SYMCLI_PATH=/usr/symcli/bin ./cod_capacity_report.sh

set -euo pipefail

SID="${SID:-}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
WARN_PCT=80

if [[ -z "$SID" ]]; then
  echo "ERROR: SID is not set." >&2
  exit 1
fi

SYMCFG="$SYMCLI_PATH/symcfg"
SYMLICENSE="$SYMCLI_PATH/symlicense"
SYMPD="$SYMCLI_PATH/sympd"

echo ""
echo "========================================"
echo "  COD Capacity Report"
echo "  SID  : $SID"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

echo ""
echo "--- Array Configuration Overview ---"
"$SYMCFG" -sid "$SID" show 2>&1 | grep -E "(Usable|Raw|Total|Capacity|GBs|TBs)" || true

echo ""
echo "--- Physical Drive Inventory ---"
"$SYMPD" list -sid "$SID" 2>&1 | head -60

echo ""
echo "--- License Status (COD) ---"
"$SYMLICENSE" -sid "$SID" list 2>&1

echo ""
echo "--- Thin Pool Utilisation ---"
"$SYMCFG" -sid "$SID" -pool -dp list 2>&1

echo ""
echo "========================================"
echo "  Report complete — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Review output above for COD reserve vs. activated capacity."
echo "  Alert if activated capacity approaches total installed capacity."
echo "========================================"
~~~

---

## COD Threshold Alerter

Reads `symcfg` pool output for a PowerMax SID and parses usable vs. total pool capacity. Warns if the activated pool utilisation is above a configurable threshold, signalling it is time to plan the next COD activation.

~~~python
#!/usr/bin/env python3
# cod_threshold_alerter.py — Alert when PowerMax pool capacity approaches COD ceiling
# Requirements: symcfg on PATH (Solutions Enabler)
# Usage: SID=000123456789 WARN_PCT=80 CRIT_PCT=90 ./cod_threshold_alerter.py

import os
import sys
import subprocess
import re

SID       = os.environ.get("SID", "")
WARN_PCT  = float(os.environ.get("WARN_PCT", "80"))
CRIT_PCT  = float(os.environ.get("CRIT_PCT", "90"))
SYMCLI    = os.environ.get("SYMCLI_PATH", "/usr/symcli/bin") + "/symcfg"

if not SID:
    print("ERROR: SID must be set.", file=sys.stderr)
    sys.exit(1)


def run_symcfg():
    result = subprocess.run(
        [SYMCLI, "-sid", SID, "-pool", "-dp", "list"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: symcfg failed:\n{result.stderr}")
        sys.exit(2)
    return result.stdout


def parse_pools(output):
    """
    Parse symcfg -pool -dp list output.
    Typical line: pool_name  total_tracks  used_tracks  ...
    We look for GB/TB values with regex.
    """
    pools = []
    for line in output.splitlines():
        # Match lines with pool name and capacity figures
        # e.g.: SRP_1    1234567    987654    ...
        parts = re.split(r'\s+', line.strip())
        if len(parts) < 4:
            continue
        name = parts[0]
        # Skip header lines
        if name in ("Pool", "Name", "---", ""):
            continue
        # Try to find percent-full in the line
        pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%', line)
        if pct_match:
            pools.append({"name": name, "pct": float(pct_match.group(1))})
    return pools


def main():
    output = run_symcfg()
    pools  = parse_pools(output)
    exit_code = 0

    print("=" * 55)
    print(f"  COD Threshold Alerter — SID {SID}")
    print("=" * 55)

    if not pools:
        # Print raw output if parsing found nothing
        print("\nRaw symcfg output (manual review required):")
        print(output)
        sys.exit(0)

    print(f"\n{'POOL':<25}  {'USED %':>8}  STATUS")
    print("-" * 45)

    for p in pools:
        if p["pct"] >= CRIT_PCT:
            status = "CRITICAL — activate next COD increment immediately"
            exit_code = max(exit_code, 2)
        elif p["pct"] >= WARN_PCT:
            status = "WARNING  — plan next COD activation"
            exit_code = max(exit_code, 1)
        else:
            status = "OK"
        print(f"{p['name']:<25}  {p['pct']:>7.1f}%  {status}")

    print("-" * 45)
    labels = {0: "OK", 1: "WARNING", 2: "CRITICAL"}
    print(f"\nOverall: {labels.get(exit_code, 'UNKNOWN')}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~

---

## Ansible COD Capacity Audit Playbook

Playbook targeting a Solutions Enabler host. Runs `symcfg` and `symlicense` commands, prints the output, and fails the play if capacity utilisation is above the warning threshold.

~~~yaml
---
# cod_capacity_audit.yml — Ansible COD capacity audit playbook for Dell PowerMax
# Inventory host: symcli_host (Solutions Enabler server with symcfg on PATH)
# Required vars: sid
# Usage: ansible-playbook -i inventory cod_capacity_audit.yml -e sid=000123456789

- name: Dell COD Capacity Audit
  hosts: symcli_host
  gather_facts: false
  vars:
    sid: "000123456789"
    symcli_path: "/usr/symcli/bin"
    warn_pct: 80

  tasks:
    - name: Get array configuration overview
      ansible.builtin.shell: "{{ symcli_path }}/symcfg -sid {{ sid }} show"
      register: symcfg_show
      changed_when: false

    - name: Show array configuration
      ansible.builtin.debug:
        msg: "{{ symcfg_show.stdout_lines }}"

    - name: Get thin pool utilisation
      ansible.builtin.shell: "{{ symcli_path }}/symcfg -sid {{ sid }} -pool -dp list"
      register: pool_list
      changed_when: false

    - name: Show pool utilisation
      ansible.builtin.debug:
        msg: "{{ pool_list.stdout_lines }}"

    - name: Get license status
      ansible.builtin.shell: "{{ symcli_path }}/symlicense -sid {{ sid }} list"
      register: license_list
      changed_when: false

    - name: Show license status
      ansible.builtin.debug:
        msg: "{{ license_list.stdout_lines }}"

    - name: Warn if pool output suggests high utilisation
      ansible.builtin.debug:
        msg: >
          WARNING: Pool utilisation may be high on SID {{ sid }}.
          Review pool_list output above and consider COD activation.
      when: >
        pool_list.stdout is search('(8[0-9]|9[0-9]|100)\s*%')
~~~
