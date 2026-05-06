# Scripts

> Part of the [Dell PowerMax](../) reference.

---

## SRDF State Monitor

Runs `symrdf list` against a PowerMax SID and parses SRDF pair states. Emits a Nagios-compatible result and exits non-zero if any pair is in a degraded state (Split, Failed Over, or Transmit Idle).

~~~perl
#!/usr/bin/env perl
# powermax_srdf_monitor.pl — SRDF pair state monitor for Dell PowerMax
# Usage: SID=000123456789 SYMCLI_PATH=/usr/symcli/bin ./powermax_srdf_monitor.pl

use strict;
use warnings;

my $sid          = $ENV{SID}          or die "ERROR: SID not set\n";
my $symcli_path  = $ENV{SYMCLI_PATH}  || '/usr/symcli/bin';
my $symrdf       = "$symcli_path/symrdf";

# States considered degraded
my %degraded_states = map { $_ => 1 } qw(
    Split
    Failed_Over
    FailedOver
    Transmit_Idle
    TransmitIdle
    Suspended
    Mixed
    Partitioned
);

# Run symrdf list
my $output = qx{"$symrdf" list -sid "$sid" 2>&1};
if ($? != 0) {
    print "UNKNOWN: symrdf list failed for SID $sid\n$output\n";
    exit 3;
}

my @pairs;
my $worst = 0;   # 0=OK 1=WARN 2=CRIT

# Parse tabular output — columns vary; we look for device and state fields
# Typical format: DEV  R1-SID  R2-SID  RDFG  MODE  STATE  R2-STATE
for my $line (split /\n/, $output) {
    next if $line =~ /^(Symmetrix|Device|---|\s*$)/;

    my @fields = split /\s+/, $line;
    next if @fields < 5;

    my $dev    = $fields[0];
    my $r1_sid = $fields[1] // $sid;
    my $r2_sid = $fields[2] // 'unknown';
    my $state  = $fields[5] // 'unknown';

    push @pairs, {
        dev    => $dev,
        r1_sid => $r1_sid,
        r2_sid => $r2_sid,
        state  => $state,
    };
}

if (!@pairs) {
    print "UNKNOWN: No SRDF pairs parsed for SID $sid\n";
    exit 3;
}

# Print table header
printf "%-15s  %-14s  %-14s  %-20s  %s\n",
    'DEV', 'R1-SID', 'R2-SID', 'STATE', 'STATUS';
printf "%s\n", '-' x 75;

for my $p (@pairs) {
    my $status = 'OK';
    if ($degraded_states{ $p->{state} }) {
        $status  = 'CRITICAL';
        $worst   = 2 if $worst < 2;
    } elsif ($p->{state} =~ /^(R1_Updated|R1Updated|Syncing)$/) {
        $status  = 'WARNING';
        $worst   = 1 if $worst < 1;
    }
    printf "%-15s  %-14s  %-14s  %-20s  %s\n",
        $p->{dev}, $p->{r1_sid}, $p->{r2_sid}, $p->{state}, $status;
}

print "\n";
if ($worst == 2) {
    print "CRITICAL: One or more SRDF pairs are in a degraded state.\n";
    exit 2;
} elsif ($worst == 1) {
    print "WARNING: One or more SRDF pairs require attention.\n";
    exit 1;
} else {
    print "OK: All SRDF pairs are Synchronized or Consistent.\n";
    exit 0;
}
~~~

---

## Array Health Check

Runs a series of SYMCLI commands against a PowerMax SID and prints a consolidated health report covering overall array state, failed disks, storage groups, and a short I/O statistics burst.

~~~bash
#!/bin/bash
# powermax_health_check.sh — Array health check for Dell PowerMax via SYMCLI
# Usage: SID=000123456789 SYMCLI_PATH=/usr/symcli/bin ./powermax_health_check.sh

set -euo pipefail

SID="${SID:-}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"

if [[ -z "$SID" ]]; then
  echo "ERROR: SID is not set." >&2
  exit 1
fi

SYMCFG="$SYMCLI_PATH/symcfg"
SYMPD="$SYMCLI_PATH/sympd"
SYMSG="$SYMCLI_PATH/symsg"
SYMSTAT="$SYMCLI_PATH/symstat"

section() {
  echo ""
  echo "========================================"
  echo "  $1"
  echo "========================================"
}

echo ""
echo "########################################"
echo "  PowerMax Health Check"
echo "  SID  : $SID"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "########################################"

section "ARRAY OVERVIEW"
"$SYMCFG" -sid "$SID" show

section "FAILED PHYSICAL DRIVES"
FAILED_PD=$("$SYMPD" list -sid "$SID" -failed 2>&1 || true)
if echo "$FAILED_PD" | grep -qi "no.*device\|no.*failed\|empty"; then
  echo "  No failed drives detected."
else
  echo "$FAILED_PD"
fi

section "STORAGE GROUPS"
"$SYMSG" list -sid "$SID"

section "QUICK I/O STATISTICS (5s interval, 3 samples, R2 side)"
"$SYMSTAT" -sid "$SID" -type r2 -i 5 -c 3 || true

echo ""
echo "========================================"
echo "  Health check complete — $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
~~~

---

## SRDF Planned Failover

Orchestrates a planned SRDF DR failover: suspends the consistency group, verifies the suspended state, splits the pair, activates the R2 side, and prints a summary. Each destructive step requires interactive confirmation.

~~~bash
#!/bin/bash
# powermax_srdf_failover.sh — Planned SRDF failover for Dell PowerMax
# Usage: SID=000123456789 RDF_GROUP=1 CG_NAME=prod-cg ./powermax_srdf_failover.sh
# WARNING: This script performs a DISRUPTIVE failover. Use only during DR tests or actual DR events.

set -euo pipefail

SID="${SID:-}"
RDF_GROUP="${RDF_GROUP:-}"
CG_NAME="${CG_NAME:-}"
SYMCLI_PATH="${SYMCLI_PATH:-/usr/symcli/bin}"
SYMRDF="$SYMCLI_PATH/symrdf"

if [[ -z "$SID" || -z "$RDF_GROUP" || -z "$CG_NAME" ]]; then
  echo "ERROR: SID, RDF_GROUP, and CG_NAME must all be set." >&2
  exit 1
fi

confirm() {
  local msg="$1"
  echo ""
  echo ">>> CONFIRM: $msg"
  read -rp "    Type YES to proceed: " answer
  if [[ "$answer" != "YES" ]]; then
    echo "    Aborted by user."
    exit 1
  fi
}

check_state() {
  local expected="$1"
  echo "  Checking SRDF state (expecting: $expected)..."
  local state
  state=$("$SYMRDF" -sid "$SID" -rdfg "$RDF_GROUP" -cg "$CG_NAME" query \
    | grep -iE "R1 State|R2 State|State" | head -5 || true)
  echo "$state"
  if ! echo "$state" | grep -qi "$expected"; then
    echo "ERROR: Expected state '$expected' not confirmed. Aborting."
    exit 1
  fi
}

echo ""
echo "########################################"
echo "  PowerMax SRDF Planned Failover"
echo "  SID       : $SID"
echo "  RDF Group : $RDF_GROUP"
echo "  CG Name   : $CG_NAME"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "########################################"

# --- Step 1: Suspend consistency group ---
confirm "STEP 1 — Suspend consistency group '${CG_NAME}' (quiesce I/O)."
echo "  Suspending consistency group..."
"$SYMRDF" -sid "$SID" -rdfg "$RDF_GROUP" -cg "$CG_NAME" suspend -force
check_state "Suspended"
echo "  Consistency group suspended successfully."

# --- Step 2: Split SRDF pair ---
confirm "STEP 2 — Split SRDF pair for consistency group '${CG_NAME}'."
echo "  Splitting SRDF pair..."
"$SYMRDF" -sid "$SID" -rdfg "$RDF_GROUP" -cg "$CG_NAME" split -force
check_state "Split"
echo "  SRDF pair split successfully."

# --- Step 3: Activate R2 devices ---
confirm "STEP 3 — Activate R2 devices (failover). Hosts at R2 site will gain write access."
echo "  Activating R2 devices via failover..."
"$SYMRDF" -sid "$SID" -rdfg "$RDF_GROUP" -cg "$CG_NAME" failover -force
echo "  Failover command issued."

# --- Summary ---
echo ""
echo "========================================"
echo "  FAILOVER SUMMARY"
echo "========================================"
"$SYMRDF" -sid "$SID" -rdfg "$RDF_GROUP" -cg "$CG_NAME" query || true
echo ""
echo "  Planned failover complete — $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Next steps:"
echo "    1. Confirm R2 hosts can see and mount the failed-over devices."
echo "    2. Validate application recovery at the DR site."
echo "    3. When ready to fail back, use: symrdf ... restore"
echo "========================================"
~~~

---

## Ansible PowerMax Health Playbook

Playbook targeting an Unisphere API host. Uses the `uri` module to authenticate to the Unisphere REST API, retrieve the array list and active alerts, and print each result.

~~~yaml
---
# powermax_health.yml — Ansible health check playbook for Dell PowerMax via Unisphere REST API
# Inventory host: powermax (the Unisphere server)
# Required vars: unisphere_host, unisphere_user, unisphere_pass, sid
# Usage: ansible-playbook -i inventory powermax_health.yml

- name: Dell PowerMax Health Check via Unisphere REST API
  hosts: powermax
  gather_facts: false
  vars:
    unisphere_host: unisphere.example.com
    unisphere_user: smc
    unisphere_pass: "{{ vault_unisphere_pass }}"
    sid: "000123456789"
    api_base: "https://{{ unisphere_host }}:8443/univmax/restapi"
    api_version: "100"

  tasks:
    - name: List Symmetrix arrays
      ansible.builtin.uri:
        url: "{{ api_base }}/{{ api_version }}/system/symmetrix"
        method: GET
        user: "{{ unisphere_user }}"
        password: "{{ unisphere_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
        headers:
          Content-Type: "application/json"
      register: array_list_resp

    - name: Show array list
      ansible.builtin.debug:
        msg: "Arrays visible: {{ array_list_resp.json.symmetrixId | default([]) }}"

    - name: Get array details for SID
      ansible.builtin.uri:
        url: "{{ api_base }}/{{ api_version }}/system/symmetrix/{{ sid }}"
        method: GET
        user: "{{ unisphere_user }}"
        password: "{{ unisphere_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
        headers:
          Content-Type: "application/json"
      register: array_detail_resp

    - name: Show array health state
      ansible.builtin.debug:
        msg:
          - "SID         : {{ array_detail_resp.json.symmetrixId | default('unknown') }}"
          - "Model       : {{ array_detail_resp.json.model | default('unknown') }}"
          - "Microcode   : {{ array_detail_resp.json.microcode | default('unknown') }}"
          - "All Flash   : {{ array_detail_resp.json.all_flash | default('unknown') }}"

    - name: Get active alerts for array
      ansible.builtin.uri:
        url: "{{ api_base }}/{{ api_version }}/system/alert_summary"
        method: GET
        user: "{{ unisphere_user }}"
        password: "{{ unisphere_pass }}"
        force_basic_auth: true
        validate_certs: false
        return_content: true
        headers:
          Content-Type: "application/json"
      register: alerts_resp

    - name: Show active alerts summary
      ansible.builtin.debug:
        msg: "{{ alerts_resp.json | default({}) }}"

    - name: Fail if critical alerts found
      ansible.builtin.fail:
        msg: "Critical alerts present on array {{ sid }}. Investigate immediately."
      when: >
        alerts_resp.json is defined and
        alerts_resp.json.serverAlertSummary is defined and
        (alerts_resp.json.serverAlertSummary.numCriticalAlerts | default(0) | int) > 0
~~~
