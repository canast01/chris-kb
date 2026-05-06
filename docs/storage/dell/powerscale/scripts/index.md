# Scripts

> Part of the [Dell PowerScale](../) reference.

---

## Cluster Health Check

SSH to a PowerScale node and runs key `isi` commands to check node state, storage pool utilisation, active jobs, recent events, and SyncIQ policy status. Exits non-zero if any node is in SMARTFAIL or DOWN state.

~~~perl
#!/usr/bin/env perl
# powerscale_health_check.pl — Cluster health check for Dell PowerScale / OneFS
# Usage: PS_HOST=ps01.example.com PS_USER=root ./powerscale_health_check.pl

use strict;
use warnings;

my $ps_host = $ENV{PS_HOST} or die "ERROR: PS_HOST not set\n";
my $ps_user = $ENV{PS_USER} || 'root';

sub run_cmd {
    my ($label, $cmd) = @_;
    print "\n" . "=" x 50 . "\n";
    print "  $label\n";
    print "=" x 50 . "\n";
    my $out = qx{ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${ps_user}\@${ps_host} "$cmd" 2>&1};
    print $out;
    return $out;
}

print "\n" . "#" x 50 . "\n";
print "  PowerScale Cluster Health Check\n";
print "  Host : $ps_host\n";
print "  Date : " . localtime() . "\n";
print "#" x 50 . "\n";

my $isi_status   = run_cmd("NODE STATUS (isi status)",   "isi status");
my $pool_list    = run_cmd("STORAGE POOLS",              "isi storagepool list");
my $job_list     = run_cmd("ACTIVE JOBS",                "isi job list");
my $event_list   = run_cmd("RECENT EVENTS (last 20)",    "isi event list --limit 20");
my $sync_list    = run_cmd("SYNCIQ POLICIES",            "isi sync policies list");

# Check for SMARTFAIL or DOWN nodes in isi status output
my $issues = 0;
for my $line (split /\n/, $isi_status) {
    if ($line =~ /\b(SMARTFAIL|DOWN)\b/i) {
        print "\n>>> ALERT: Node issue detected: $line\n";
        $issues++;
    }
}

# Check for FAILED jobs
for my $line (split /\n/, $job_list) {
    if ($line =~ /\bFAILED\b/i) {
        print "\n>>> ALERT: Failed job detected: $line\n";
        $issues++;
    }
}

# Check for CRITICAL events
for my $line (split /\n/, $event_list) {
    if ($line =~ /\bCRITICAL\b/i) {
        print "\n>>> ALERT: Critical event: $line\n";
        $issues++;
    }
}

print "\n" . "=" x 50 . "\n";
if ($issues > 0) {
    print "  STATUS: DEGRADED — $issues issue(s) found. Review output above.\n";
    exit 1;
} else {
    print "  STATUS: OK — No critical issues detected.\n";
    exit 0;
}
~~~

---

## SyncIQ Policy Monitor

Runs `isi sync policies list -v` and `isi sync reports list` to check the state and last run result of every SyncIQ replication policy. Prints a table of policy name, state, last run time, and duration. Exits non-zero if any policy is in a FAILED state.

~~~bash
#!/bin/bash
# powerscale_synciq_monitor.sh — Monitor SyncIQ policy health on Dell PowerScale
# Usage: PS_HOST=ps01.example.com PS_USER=root ./powerscale_synciq_monitor.sh

set -euo pipefail

PS_HOST="${PS_HOST:-}"
PS_USER="${PS_USER:-root}"

if [[ -z "$PS_HOST" ]]; then
  echo "ERROR: PS_HOST is not set." >&2
  exit 1
fi

SSH="ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${PS_USER}@${PS_HOST}"

echo ""
echo "========================================"
echo "  SyncIQ Policy Monitor"
echo "  Host : $PS_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Fetch policy list
POLICIES=$($SSH "isi sync policies list -v" 2>&1)
# Fetch recent reports (last 5 per policy)
REPORTS=$($SSH "isi sync reports list --limit 5" 2>&1)

echo ""
echo "--- Policy Details ---"
echo "$POLICIES"
echo ""
echo "--- Recent Reports ---"
echo "$REPORTS"

echo ""
echo "--- Policy Summary Table ---"
printf "%-30s  %-12s  %-25s  %s\n" "POLICY" "STATE" "LAST-RUN" "STATUS"
printf "%s\n" "----------------------------------------------------------------------"

FAILED=0
# Parse policy list for name and last run state
# "isi sync policies list" output has Name, State, Last_Run_State columns
while IFS= read -r line; do
  # Skip headers and blank lines
  [[ "$line" =~ ^(Name|---|$) ]] && continue
  [[ -z "$line" ]] && continue

  policy=$(echo "$line"   | awk '{print $1}')
  state=$(echo "$line"    | awk '{print $2}')
  last_run=$(echo "$line" | awk '{print $3, $4}')

  [[ -z "$policy" || "$policy" == "Name" ]] && continue

  status="OK"
  if [[ "${state^^}" == "FAILED" ]]; then
    status="FAILED"
    FAILED=$((FAILED + 1))
  elif [[ "${state^^}" == "RUNNING" ]]; then
    status="RUNNING"
  fi

  printf "%-30s  %-12s  %-25s  %s\n" "$policy" "$state" "$last_run" "$status"
done <<< "$POLICIES"

echo ""
if [[ "$FAILED" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $FAILED SyncIQ policy/policies in FAILED state."
  exit 1
else
  echo "STATUS: OK — All SyncIQ policies healthy."
  exit 0
fi
~~~

---

## Quota Report

Runs `isi quota quotas list -v` and formats the output as a CSV-style report showing path, quota type, current usage, soft threshold, hard threshold, and percentage used. Flags any quota over 80% with a WARNING marker. Suitable for redirecting to a file or piping to a reporting system.

~~~bash
#!/bin/bash
# powerscale_quota_report.sh — Generate a quota utilisation report for Dell PowerScale
# Usage: PS_HOST=ps01.example.com PS_USER=root ./powerscale_quota_report.sh [> quota_report.csv]

set -euo pipefail

PS_HOST="${PS_HOST:-}"
PS_USER="${PS_USER:-root}"
WARN_PCT=80

if [[ -z "$PS_HOST" ]]; then
  echo "ERROR: PS_HOST is not set." >&2
  exit 1
fi

SSH="ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${PS_USER}@${PS_HOST}"

QUOTA_OUT=$($SSH "isi quota quotas list -v" 2>&1)

# Print CSV header
echo "PATH,TYPE,USAGE_GB,SOFT_GB,HARD_GB,PCT_USED,FLAG"

OVER_THRESHOLD=0

# Parse the verbose isi quota output
# Each quota entry block has: Path: ..., Type: ..., Usage(Bytes): ..., Soft(Bytes): ..., Hard(Bytes): ...
current_path="" current_type="" usage_b=0 soft_b=0 hard_b=0

bytes_to_gb() {
  local b="$1"
  if [[ "$b" =~ ^[0-9]+$ && "$b" -gt 0 ]]; then
    echo "scale=2; $b / 1073741824" | bc
  else
    echo "0.00"
  fi
}

emit_row() {
  [[ -z "$current_path" ]] && return
  local usage_gb soft_gb hard_gb pct flag
  usage_gb=$(bytes_to_gb "$usage_b")
  soft_gb=$(bytes_to_gb "$soft_b")
  hard_gb=$(bytes_to_gb "$hard_b")

  if [[ "$hard_b" -gt 0 ]]; then
    pct=$(echo "scale=1; $usage_b * 100 / $hard_b" | bc)
  else
    pct="N/A"
  fi

  flag=""
  if [[ "$pct" != "N/A" ]] && (( $(echo "$pct >= $WARN_PCT" | bc -l) )); then
    flag="WARNING"
    OVER_THRESHOLD=$((OVER_THRESHOLD + 1))
  fi

  echo "${current_path},${current_type},${usage_gb},${soft_gb},${hard_gb},${pct},${flag}"
}

while IFS= read -r line; do
  if [[ "$line" =~ ^[[:space:]]*Path:[[:space:]]+(.*) ]]; then
    emit_row
    current_path="${BASH_REMATCH[1]}"
    current_type="" usage_b=0 soft_b=0 hard_b=0
  elif [[ "$line" =~ ^[[:space:]]*Type:[[:space:]]+(.*) ]]; then
    current_type="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ [Uu]sage.*:[[:space:]]*([0-9]+) ]]; then
    usage_b="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ [Ss]oft.*:[[:space:]]*([0-9]+) ]]; then
    soft_b="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ [Hh]ard.*:[[:space:]]*([0-9]+) ]]; then
    hard_b="${BASH_REMATCH[1]}"
  fi
done <<< "$QUOTA_OUT"

# Emit last entry
emit_row

if [[ "$OVER_THRESHOLD" -gt 0 ]]; then
  echo "# $OVER_THRESHOLD quota(s) at or above ${WARN_PCT}% — review flagged rows." >&2
fi
exit 0
~~~

---

## Ansible SyncIQ Health Playbook

Playbook targeting the `powerscale` host group. Runs SyncIQ policy list, recent reports, and cluster status via the shell module, then fails the play if any FAILED policy state is detected.

~~~yaml
---
# powerscale_synciq_health.yml — Ansible SyncIQ health check playbook for Dell PowerScale
# Inventory group: powerscale
# Usage: ansible-playbook -i inventory powerscale_synciq_health.yml

- name: Dell PowerScale SyncIQ Health Check
  hosts: powerscale
  gather_facts: false

  tasks:
    - name: List SyncIQ policies
      ansible.builtin.shell: "isi sync policies list -v"
      register: policies_out
      changed_when: false

    - name: Show SyncIQ policy list
      ansible.builtin.debug:
        msg: "{{ policies_out.stdout_lines }}"

    - name: List recent SyncIQ reports
      ansible.builtin.shell: "isi sync reports list --limit 5"
      register: reports_out
      changed_when: false

    - name: Show SyncIQ reports
      ansible.builtin.debug:
        msg: "{{ reports_out.stdout_lines }}"

    - name: Get cluster status
      ansible.builtin.shell: "isi status"
      register: cluster_status
      changed_when: false

    - name: Show cluster status
      ansible.builtin.debug:
        msg: "{{ cluster_status.stdout_lines }}"

    - name: Fail if any SyncIQ policy is in FAILED state
      ansible.builtin.fail:
        msg: >
          SyncIQ policy FAILED state detected on {{ inventory_hostname }}.
          Review the policy output above and check 'isi sync reports list' for details.
      when: "'FAILED' in policies_out.stdout"

    - name: Confirm all checks passed
      ansible.builtin.debug:
        msg: "SyncIQ health check passed for {{ inventory_hostname }}."
~~~

---

## Performance Baseline Check

SSH to a PowerScale node using paramiko to run `isi statistics query current` for key performance counters. Compares current values to configurable baselines and alerts if CPU exceeds 80% or disk latency exceeds 10 ms.

~~~python
#!/usr/bin/env python3
# powerscale_perf_check.py — Performance baseline check for Dell PowerScale via SSH
# Requirements: paramiko
# Usage:
#   PS_HOST=ps01.example.com PS_USER=root PS_KEY=~/.ssh/id_rsa ./powerscale_perf_check.py

import os
import sys
import re
import paramiko

PS_HOST    = os.environ.get("PS_HOST", "")
PS_USER    = os.environ.get("PS_USER", "root")
PS_KEY     = os.environ.get("PS_KEY", os.path.expanduser("~/.ssh/id_rsa"))
PS_PASS    = os.environ.get("PS_PASS", None)   # Used if no key

# Baseline thresholds
THRESHOLDS = {
    "CPU":     {"warn": 80.0,   "unit": "%",  "label": "CPU Utilisation"},
    "NetIn":   {"warn": None,   "unit": "B/s","label": "Network In"},
    "NetOut":  {"warn": None,   "unit": "B/s","label": "Network Out"},
    "DiskIn":  {"warn": 10.0,   "unit": "ms", "label": "Disk Read Latency"},
    "DiskOut": {"warn": 10.0,   "unit": "ms", "label": "Disk Write Latency"},
}

if not PS_HOST:
    print("ERROR: PS_HOST must be set.", file=sys.stderr)
    sys.exit(1)


def ssh_run(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connect_kwargs = {"username": PS_USER, "timeout": 30}
    if PS_PASS:
        connect_kwargs["password"] = PS_PASS
    else:
        connect_kwargs["key_filename"] = PS_KEY

    client.connect(PS_HOST, **connect_kwargs)
    stdin, stdout, stderr = client.exec_command(command)
    out = stdout.read().decode()
    err = stderr.read().decode()
    client.close()
    return out, err


def parse_stats(output):
    """
    Parse isi statistics query current output.
    Expected format: Key   Node  Value  Time
    """
    stats = {}
    for line in output.splitlines():
        line = line.strip()
        if not line or line.startswith("Key"):
            continue
        parts = re.split(r'\s+', line, maxsplit=3)
        if len(parts) >= 3:
            key, node, value = parts[0], parts[1], parts[2]
            # Store per-key list (multiple nodes)
            stats.setdefault(key, []).append(float(value) if re.match(r'^[\d.]+$', value) else 0.0)
    return stats


def main():
    keys = ",".join(THRESHOLDS.keys())
    cmd  = f"isi statistics query current --keys {keys} --format=tsv 2>/dev/null || " \
           f"isi statistics query current --stats {keys}"

    print("=" * 55)
    print(f"  PowerScale Performance Baseline Check")
    print(f"  Host : {PS_HOST}")
    print("=" * 55)

    try:
        out, err = ssh_run(cmd)
    except Exception as e:
        print(f"ERROR: SSH failed: {e}")
        sys.exit(2)

    if not out.strip():
        print(f"ERROR: No statistics output received.\nStderr: {err}")
        sys.exit(2)

    stats = parse_stats(out)
    exit_code = 0

    print(f"\n{'METRIC':<25}  {'CURRENT':>10}  {'THRESHOLD':>10}  STATUS")
    print("-" * 60)

    for key, cfg in THRESHOLDS.items():
        values = stats.get(key, [])
        if not values:
            current = None
            current_str = "N/A"
        else:
            current = max(values)   # Report worst-case node
            current_str = f"{current:.2f} {cfg['unit']}"

        warn = cfg["warn"]
        if current is not None and warn is not None and current >= warn:
            status = "WARNING"
            exit_code = max(exit_code, 1)
        elif current is None:
            status = "NO DATA"
        else:
            status = "OK"

        thresh_str = f"{warn} {cfg['unit']}" if warn is not None else "N/A"
        print(f"{cfg['label']:<25}  {current_str:>10}  {thresh_str:>10}  {status}")

    print("\n" + "=" * 55)
    labels = {0: "OK", 1: "WARNING", 2: "CRITICAL"}
    print(f"  OVERALL: {labels.get(exit_code, 'UNKNOWN')}")
    print("=" * 55)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
~~~
