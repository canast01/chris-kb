# Scripts

> Part of the [Dell Unity](../) reference.

---

## System Health Check

Uses `uemcli` to run a comprehensive health check against a Dell Unity array: component health, pool capacity, LUN status, active alerts, and storage processor state. Exits non-zero if any component is in a non-OK health state.

~~~bash
#!/bin/bash
# unity_health_check.sh — Dell Unity system health check via uemcli
# Usage: UNITY_HOST=unity01.example.com UNITY_USER=admin UNITY_PASS=secret ./unity_health_check.sh

set -euo pipefail

UNITY_HOST="${UNITY_HOST:-}"
UNITY_USER="${UNITY_USER:-admin}"
UNITY_PASS="${UNITY_PASS:-}"

if [[ -z "$UNITY_HOST" || -z "$UNITY_PASS" ]]; then
  echo "ERROR: UNITY_HOST and UNITY_PASS must be set." >&2
  exit 1
fi

UEMCLI="uemcli -d ${UNITY_HOST} -u ${UNITY_USER} -p ${UNITY_PASS}"
ISSUES=0

section() {
  echo ""
  echo "========================================"
  echo "  $1"
  echo "========================================"
}

echo ""
echo "########################################"
echo "  Dell Unity Health Check"
echo "  Host : $UNITY_HOST"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "########################################"

# --- Component health ---
section "COMPONENT HEALTH (non-OK only)"
HEALTH_OUT=$($UEMCLI /env/health show -filter "health.value ne OK" 2>&1 || true)
if echo "$HEALTH_OUT" | grep -qi "No entries"; then
  echo "  All components healthy."
else
  echo "$HEALTH_OUT"
  # Count degraded components
  DEGRADED=$(echo "$HEALTH_OUT" | grep -c "health.value" || true)
  ISSUES=$((ISSUES + DEGRADED))
fi

# --- Storage pool capacity ---
section "STORAGE POOL CAPACITY"
$UEMCLI /stor/pool show -detail 2>&1 || { echo "  ERROR: could not query pools."; ISSUES=$((ISSUES + 1)); }

# --- LUN overview ---
section "LUN OVERVIEW"
$UEMCLI /store/lun show 2>&1 || { echo "  ERROR: could not query LUNs."; ISSUES=$((ISSUES + 1)); }

# --- Active alerts ---
section "ACTIVE ALERTS"
ALERT_OUT=$($UEMCLI /sys/alert show 2>&1 || true)
echo "$ALERT_OUT"
ALERT_COUNT=$(echo "$ALERT_OUT" | grep -c "^[[:space:]]*[0-9]" || true)
if [[ "$ALERT_COUNT" -gt 0 ]]; then
  ISSUES=$((ISSUES + 1))
fi

# --- Storage processor status ---
section "STORAGE PROCESSOR STATUS"
$UEMCLI /env/sp show 2>&1 || { echo "  ERROR: could not query SPs."; ISSUES=$((ISSUES + 1)); }

echo ""
echo "========================================"
echo "  SUMMARY"
echo "========================================"
if [[ "$ISSUES" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $ISSUES issue category/categories found. Review sections above."
  exit 1
else
  echo "STATUS: OK — All health checks passed."
  exit 0
fi
~~~

---

## Storage Processor Monitor

Uses `uemcli` to check the health state of SP A and SP B and to enumerate all network interfaces. Alerts in PASS/WARNING/CRITICAL format if either SP is Faulted or if any interface is down.

~~~perl
#!/usr/bin/env perl
# unity_sp_monitor.pl — Storage processor health monitor for Dell Unity
# Usage: UNITY_HOST=unity01.example.com UNITY_USER=admin UNITY_PASS=secret ./unity_sp_monitor.pl

use strict;
use warnings;

my $host = $ENV{UNITY_HOST} or die "ERROR: UNITY_HOST not set\n";
my $user = $ENV{UNITY_USER} || 'admin';
my $pass = $ENV{UNITY_PASS} or die "ERROR: UNITY_PASS not set\n";

my $uemcli = "uemcli -d $host -u $user -p $pass";
my $worst  = 0;  # 0=OK 1=WARN 2=CRIT

sub run {
    my ($args) = @_;
    my $out = qx{$uemcli $args 2>&1};
    return $out;
}

# --- SP health check ---
print "\n--- Storage Processor Health ---\n";
my $sp_out = run("/env/sp show");
print $sp_out;

# Parse SP state — look for lines containing "Faulted" or unexpected states
for my $line (split /\n/, $sp_out) {
    if ($line =~ /\bFault(?:ed)?\b/i) {
        print ">>> CRITICAL: SP fault detected: $line\n";
        $worst = 2 if $worst < 2;
    } elsif ($line =~ /\b(Service Mode|Unknown)\b/i) {
        print ">>> WARNING: SP in unusual state: $line\n";
        $worst = 1 if $worst < 1;
    }
}

# --- Network interface check ---
print "\n--- Network Interfaces ---\n";
my $net_out = run("/net/if show");
print $net_out;

my $down_if = 0;
for my $line (split /\n/, $net_out) {
    if ($line =~ /\b(Down|Disabled)\b/i) {
        print ">>> WARNING: Interface in down/disabled state: $line\n";
        $worst = 1 if $worst < 1;
        $down_if++;
    }
}

# --- Summary ---
print "\n" . "=" x 50 . "\n";
if ($worst == 2) {
    print "  STATUS: CRITICAL — One or more SPs are faulted.\n";
} elsif ($worst == 1) {
    print "  STATUS: WARNING — SP or interface issue detected.\n";
} else {
    print "  STATUS: PASS — Both SPs healthy, all interfaces up.\n";
}
print "=" x 50 . "\n";

exit($worst == 2 ? 2 : ($worst == 1 ? 1 : 0));
~~~

---

## Replication Session Check

Runs `uemcli /rep/session show -detail` and parses each replication session for its state. Prints a formatted table of session name, source, destination, state, and last sync time. Exits non-zero if any session is in an Error state.

~~~bash
#!/bin/bash
# unity_repl_check.sh — Replication session health check for Dell Unity
# Usage: UNITY_HOST=unity01.example.com UNITY_USER=admin UNITY_PASS=secret ./unity_repl_check.sh

set -euo pipefail

UNITY_HOST="${UNITY_HOST:-}"
UNITY_USER="${UNITY_USER:-admin}"
UNITY_PASS="${UNITY_PASS:-}"

if [[ -z "$UNITY_HOST" || -z "$UNITY_PASS" ]]; then
  echo "ERROR: UNITY_HOST and UNITY_PASS must be set." >&2
  exit 1
fi

UEMCLI="uemcli -d ${UNITY_HOST} -u ${UNITY_USER} -p ${UNITY_PASS}"

echo ""
echo "========================================"
echo "  Unity Replication Session Check"
echo "  Host : $UNITY_HOST"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Fetch all replication sessions in detail
SESSIONS=$($UEMCLI /rep/session show -detail 2>&1)

echo ""
echo "--- Raw Session Output ---"
echo "$SESSIONS"
echo ""
echo "--- Session Summary Table ---"
printf "%-25s  %-20s  %-20s  %-10s  %s\n" \
  "SESSION" "SOURCE" "DESTINATION" "STATE" "LAST-SYNC"
printf "%s\n" "----------------------------------------------------------------------"

ERRORS=0
current_name="" current_src="" current_dst="" current_state="" current_sync=""

flush_row() {
  [[ -z "$current_name" ]] && return
  local marker=""
  if [[ "${current_state,,}" == "error" || "${current_state,,}" == "faulted" ]]; then
    marker="  <<< ERROR"
    ERRORS=$((ERRORS + 1))
  fi
  printf "%-25s  %-20s  %-20s  %-10s  %s%s\n" \
    "$current_name" "$current_src" "$current_dst" "$current_state" "$current_sync" "$marker"
}

while IFS= read -r line; do
  # New session block starts with "ID = ..." or "Name = ..."
  if [[ "$line" =~ ^[[:space:]]*ID[[:space:]]*=[[:space:]]*(.*) ]]; then
    flush_row
    current_name="${BASH_REMATCH[1]}"
    current_src="" current_dst="" current_state="" current_sync=""
  elif [[ "$line" =~ [Ss]ource[[:space:]]*Resource.*=[[:space:]]*(.*) ]]; then
    current_src="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ [Dd]estination[[:space:]]*Resource.*=[[:space:]]*(.*) ]]; then
    current_dst="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ [Ss]tate[[:space:]]*=[[:space:]]*(.*) ]]; then
    current_state="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ [Ll]ast[[:space:]][Ss]ync[[:space:]]Time.*=[[:space:]]*(.*) ]]; then
    current_sync="${BASH_REMATCH[1]}"
  fi
done <<< "$SESSIONS"

# Flush last entry
flush_row

echo ""
if [[ "$ERRORS" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $ERRORS replication session(s) in Error state."
  exit 1
else
  echo "STATUS: OK — All replication sessions healthy."
  exit 0
fi
~~~

---

## Ansible Unity Health Playbook

Playbook that uses the `shell` module to run `uemcli` health commands against a Unity array. Registers outputs for pool health, LUN status, active alerts, and replication sessions, and uses `fail when` to catch any detected issues.

~~~yaml
---
# unity_health.yml — Ansible health check playbook for Dell Unity
# Inventory host: unity (the Unity management IP or DNS name)
# Required vars: unity_host, unity_user, unity_pass
# Usage: ansible-playbook -i inventory unity_health.yml

- name: Dell Unity Health Check
  hosts: unity
  gather_facts: false
  vars:
    unity_host: unity01.example.com
    unity_user: admin
    unity_pass: "{{ vault_unity_pass }}"

  tasks:
    - name: Check pool health and capacity
      ansible.builtin.shell: >
        uemcli -d {{ unity_host }} -u {{ unity_user }} -p {{ unity_pass }}
        /stor/pool show -detail
      register: pool_health
      changed_when: false
      no_log: true

    - name: Show pool health
      ansible.builtin.debug:
        msg: "{{ pool_health.stdout_lines }}"

    - name: Check LUN health
      ansible.builtin.shell: >
        uemcli -d {{ unity_host }} -u {{ unity_user }} -p {{ unity_pass }}
        /store/lun show
      register: lun_health
      changed_when: false
      no_log: true

    - name: Show LUN health
      ansible.builtin.debug:
        msg: "{{ lun_health.stdout_lines }}"

    - name: Check active alerts
      ansible.builtin.shell: >
        uemcli -d {{ unity_host }} -u {{ unity_user }} -p {{ unity_pass }}
        /sys/alert show
      register: alert_check
      changed_when: false
      no_log: true

    - name: Show active alerts
      ansible.builtin.debug:
        msg: "{{ alert_check.stdout_lines }}"

    - name: Check replication sessions
      ansible.builtin.shell: >
        uemcli -d {{ unity_host }} -u {{ unity_user }} -p {{ unity_pass }}
        /rep/session show
      register: rep_sessions
      changed_when: false
      no_log: true

    - name: Show replication session status
      ansible.builtin.debug:
        msg: "{{ rep_sessions.stdout_lines }}"

    - name: Fail if non-OK health components found
      ansible.builtin.fail:
        msg: "Non-OK health state detected on Unity {{ unity_host }}. Review output above."
      when: >
        pool_health.stdout is search('health\\.value') or
        lun_health.stdout is search('Faulted')

    - name: Fail if replication session in Error state
      ansible.builtin.fail:
        msg: "Replication session Error state detected on {{ unity_host }}."
      when: "'Error' in rep_sessions.stdout or 'Faulted' in rep_sessions.stdout"

    - name: All checks passed
      ansible.builtin.debug:
        msg: "Dell Unity health check completed successfully for {{ unity_host }}."
~~~
