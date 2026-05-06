# Scripts

> Part of the [Dell Data Domain](../) reference.

---

## Daily Health Check

SSH to a Data Domain appliance and print a formatted health summary covering filesystem space, compression ratio, active alerts, replication state, and system uptime. Exits non-zero if any active alerts are found.

~~~bash
#!/bin/bash
# dd_health_check.sh — Daily health check for a Dell Data Domain appliance
# Usage: DD_HOST=dd01.example.com DD_USER=sysadmin ./dd_health_check.sh

set -euo pipefail

DD_HOST="${DD_HOST:-}"
DD_USER="${DD_USER:-sysadmin}"
ALERT_COUNT=0

if [[ -z "$DD_HOST" ]]; then
  echo "ERROR: DD_HOST is not set." >&2
  exit 1
fi

run_cmd() {
  local label="$1"
  local cmd="$2"
  echo "========================================"
  echo "  $label"
  echo "========================================"
  ssh -o StrictHostKeyChecking=no -o BatchMode=yes "${DD_USER}@${DD_HOST}" "$cmd"
  echo ""
}

echo ""
echo "########################################"
echo "  Data Domain Health Check"
echo "  Host : $DD_HOST"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "########################################"
echo ""

run_cmd "FILESYSTEM SPACE"         "filesys show space"
run_cmd "COMPRESSION RATIO"        "filesys show compression"
run_cmd "SYSTEM UPTIME"            "system show uptime"
run_cmd "REPLICATION STATE"        "replication show"

echo "========================================"
echo "  ACTIVE ALERTS"
echo "========================================"
ALERTS=$(ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
  "${DD_USER}@${DD_HOST}" "alerts show current")
echo "$ALERTS"
echo ""

# Count non-header, non-empty alert lines
ALERT_COUNT=$(echo "$ALERTS" | grep -cE '^\s+[0-9]+' || true)

echo "========================================"
echo "  SUMMARY"
echo "========================================"
if [[ "$ALERT_COUNT" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $ALERT_COUNT active alert(s) found."
  exit 1
else
  echo "STATUS: OK — No active alerts."
  exit 0
fi
~~~

---

## Replication Lag Monitor

SSH to a Data Domain appliance and parse `replication show` output. Extracts lag time per replication context and emits Nagios-compatible WARNING or CRITICAL output. Designed to be called directly by Icinga, Nagios, or a monitoring relay.

~~~perl
#!/usr/bin/env perl
# dd_repl_monitor.pl — Data Domain replication lag monitor
# Usage: DD_HOST=dd01 DD_USER=sysadmin WARN_MIN=30 CRIT_MIN=60 ./dd_repl_monitor.pl

use strict;
use warnings;

my $dd_host  = $ENV{DD_HOST}  or die "ERROR: DD_HOST not set\n";
my $dd_user  = $ENV{DD_USER}  || 'sysadmin';
my $warn_min = $ENV{WARN_MIN} // 30;
my $crit_min = $ENV{CRIT_MIN} // 60;

# Fetch replication show output via SSH
my $output = qx{ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${dd_user}\@${dd_host} "replication show" 2>&1};
if ($? != 0) {
    print "UNKNOWN: SSH to $dd_host failed\n";
    exit 3;
}

my @contexts;
my $worst_state = 0;  # 0=OK 1=WARN 2=CRIT

# Parse replication show output
# Example line: ctx:1  source:mtree://dd01/data/col1/veeam  dest:mtree://dd02/...  state:Normal  lag:00:15:23
for my $line (split /\n/, $output) {
    next unless $line =~ /\bctx:/;

    my ($ctx)   = $line =~ /ctx:(\S+)/;
    my ($state) = $line =~ /state:(\S+)/;
    my ($lag)   = $line =~ /lag:(\d+:\d+:\d+)/;

    $ctx   //= 'unknown';
    $state //= 'unknown';
    $lag   //= '00:00:00';

    # Convert lag HH:MM:SS to minutes
    my ($hh, $mm, $ss) = split /:/, $lag;
    my $lag_minutes = ($hh // 0) * 60 + ($mm // 0) + int(($ss // 0) / 60);

    my $status = 'OK';
    if ($lag_minutes >= $crit_min) {
        $status      = 'CRITICAL';
        $worst_state = 2 if $worst_state < 2;
    } elsif ($lag_minutes >= $warn_min) {
        $status      = 'WARNING';
        $worst_state = 1 if $worst_state < 1;
    }

    push @contexts, {
        ctx        => $ctx,
        state      => $state,
        lag        => $lag,
        lag_min    => $lag_minutes,
        status     => $status,
    };
}

if (!@contexts) {
    print "UNKNOWN: No replication contexts found in output\n";
    exit 3;
}

# Print results table
printf "%-6s  %-14s  %-10s  %8s  %s\n",
    'CTX', 'STATE', 'LAG', 'LAG(min)', 'STATUS';
printf "%s\n", '-' x 60;
for my $c (@contexts) {
    printf "%-6s  %-14s  %-10s  %8d  %s\n",
        $c->{ctx}, $c->{state}, $c->{lag}, $c->{lag_min}, $c->{status};
}

# Exit with worst state
if ($worst_state == 2) {
    print "\nCRITICAL: One or more replication contexts exceed ${crit_min}-minute lag threshold.\n";
    exit 2;
} elsif ($worst_state == 1) {
    print "\nWARNING: One or more replication contexts exceed ${warn_min}-minute lag threshold.\n";
    exit 1;
} else {
    print "\nOK: All replication contexts within lag thresholds.\n";
    exit 0;
}
~~~

---

## Ansible Daily Check Playbook

Playbook targeting the `data_domain` host group. Runs filesystem space, alert, and replication checks via SSH and prints each result using the `debug` module.

~~~yaml
---
# dd_daily_check.yml — Ansible daily health check playbook for Data Domain
# Inventory group: data_domain
# Required vars: dd_user (default: sysadmin)
# Usage: ansible-playbook -i inventory dd_daily_check.yml

- name: Dell Data Domain Daily Health Check
  hosts: data_domain
  gather_facts: false
  vars:
    dd_user: sysadmin

  tasks:
    - name: Check filesystem space
      ansible.builtin.raw: "filesys show space"
      register: filesys_space
      changed_when: false

    - name: Show filesystem space output
      ansible.builtin.debug:
        msg: "{{ filesys_space.stdout_lines }}"

    - name: Check active alerts
      ansible.builtin.raw: "alerts show current"
      register: alerts_output
      changed_when: false

    - name: Show active alerts output
      ansible.builtin.debug:
        msg: "{{ alerts_output.stdout_lines }}"

    - name: Check replication state
      ansible.builtin.raw: "replication show"
      register: repl_output
      changed_when: false

    - name: Show replication state output
      ansible.builtin.debug:
        msg: "{{ repl_output.stdout_lines }}"

    - name: Fail if active alerts detected
      ansible.builtin.fail:
        msg: "Active alerts found on {{ inventory_hostname }}. Review output above."
      when: >
        alerts_output.stdout is defined and
        alerts_output.stdout | regex_search('[0-9]+\\s+\\w+\\s+\\w+')
~~~

---

## DDBoost Client Check

Runs `ddboost show clients` and `ddboost status`, parses for disconnected clients, and prints a formatted table. Exits non-zero if any client is found in a disconnected or unknown state.

~~~bash
#!/bin/bash
# dd_ddboost_check.sh — Check DDBoost client connectivity on a Data Domain appliance
# Usage: DD_HOST=dd01.example.com DD_USER=sysadmin ./dd_ddboost_check.sh

set -euo pipefail

DD_HOST="${DD_HOST:-}"
DD_USER="${DD_USER:-sysadmin}"

if [[ -z "$DD_HOST" ]]; then
  echo "ERROR: DD_HOST is not set." >&2
  exit 1
fi

echo "========================================"
echo "  DDBoost Client Check — $DD_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Fetch DDBoost clients list
CLIENTS=$(ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
  "${DD_USER}@${DD_HOST}" "ddboost show clients")

# Fetch DDBoost overall status
STATUS=$(ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
  "${DD_USER}@${DD_HOST}" "ddboost status")

echo "--- DDBoost Status ---"
echo "$STATUS"
echo ""
echo "--- Client Table ---"
printf "%-30s  %-15s  %-10s\n" "CLIENT" "IP/HOSTNAME" "STATE"
printf "%s\n" "--------------------------------------------------------------"

DISCONNECTED=0
# Parse client lines — format: <name>  <ip>  <state>  ...
while IFS= read -r line; do
  # Skip header and blank lines
  [[ "$line" =~ ^(Client|---|$) ]] && continue
  [[ -z "$line" ]] && continue

  client=$(echo "$line" | awk '{print $1}')
  ip=$(echo "$line"     | awk '{print $2}')
  state=$(echo "$line"  | awk '{print $3}')

  [[ -z "$client" ]] && continue

  if [[ "${state,,}" != "connected" ]]; then
    DISCONNECTED=$((DISCONNECTED + 1))
    printf "%-30s  %-15s  %-10s  <<< DISCONNECTED\n" "$client" "$ip" "$state"
  else
    printf "%-30s  %-15s  %-10s\n" "$client" "$ip" "$state"
  fi
done <<< "$CLIENTS"

echo ""
echo "========================================"
if [[ "$DISCONNECTED" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $DISCONNECTED disconnected DDBoost client(s)."
  exit 1
else
  echo "STATUS: OK — All DDBoost clients connected."
  exit 0
fi
~~~
