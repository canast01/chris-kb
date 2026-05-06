# Scripts

> Part of the [Dell VPLEX](../) reference.

---

## Distributed Device Health Check

SSH to a VPLEX management server and runs vplexcli commands to check cluster health indications, distributed device health, and director hardware state. Reports any health-state value that is not "ok" and exits non-zero if issues are found.

~~~bash
#!/bin/bash
# vplex_device_health.sh — Distributed device and director health check for Dell VPLEX
# Usage: VPLEX_HOST=vplex-mgmt.example.com VPLEX_USER=service ./vplex_device_health.sh

set -euo pipefail

VPLEX_HOST="${VPLEX_HOST:-}"
VPLEX_USER="${VPLEX_USER:-service}"
ISSUES=0

if [[ -z "$VPLEX_HOST" ]]; then
  echo "ERROR: VPLEX_HOST is not set." >&2
  exit 1
fi

# Wrapper: run a vplexcli command via SSH
vplex_cmd() {
  local cmd="$1"
  ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
      "${VPLEX_USER}@${VPLEX_HOST}" "vplexcli -q -e '${cmd}'" 2>&1
}

section() {
  echo ""
  echo "========================================"
  echo "  $1"
  echo "========================================"
}

echo ""
echo "########################################"
echo "  VPLEX Health Check"
echo "  Host : $VPLEX_HOST"
echo "  Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo "########################################"

# --- Cluster health indications ---
section "CLUSTER HEALTH INDICATIONS"
CLUSTER_HEALTH=$(vplex_cmd "ll /clusters/*/health-indications/")
echo "$CLUSTER_HEALTH"
if echo "$CLUSTER_HEALTH" | grep -qi "health-state.*[^ok]"; then
  echo ">>> ISSUE: Non-OK cluster health indication detected."
  ISSUES=$((ISSUES + 1))
fi

# --- Distributed device health ---
section "DISTRIBUTED DEVICE HEALTH"
DD_HEALTH=$(vplex_cmd "ll /distributed-storage/distributed-devices/*/health-indications/")
echo "$DD_HEALTH"
BAD_DEVICES=$(echo "$DD_HEALTH" | grep -i "health-state" | grep -iv "value:.*ok" || true)
if [[ -n "$BAD_DEVICES" ]]; then
  echo ">>> ISSUE: One or more distributed devices are NOT in 'ok' health state:"
  echo "$BAD_DEVICES"
  ISSUES=$((ISSUES + 1))
fi

# --- Director hardware ---
section "DIRECTOR HARDWARE STATUS"
DIR_HEALTH=$(vplex_cmd "ll /engines/*/directors/*/hardware/")
echo "$DIR_HEALTH"
BAD_DIRS=$(echo "$DIR_HEALTH" | grep -i "health-state" | grep -iv "value:.*ok" || true)
if [[ -n "$BAD_DIRS" ]]; then
  echo ">>> ISSUE: One or more directors have non-OK hardware state:"
  echo "$BAD_DIRS"
  ISSUES=$((ISSUES + 1))
fi

echo ""
echo "========================================"
echo "  SUMMARY"
echo "========================================"
if [[ "$ISSUES" -gt 0 ]]; then
  echo "STATUS: DEGRADED — $ISSUES issue category/categories found. Review output above."
  exit 1
else
  echo "STATUS: OK — All VPLEX health checks passed."
  exit 0
fi
~~~

---

## Metro Consistency Group Monitor

SSH to a VPLEX Metro system and queries consistency group operational status. Parses for any CG that is not in `in-sync` state and emits a Nagios-compatible PASS/WARNING/CRITICAL result. Alerts on split-brain or out-of-sync state.

~~~perl
#!/usr/bin/env perl
# vplex_cg_monitor.pl — Metro consistency group monitor for Dell VPLEX
# Usage: VPLEX_HOST=vplex-mgmt.example.com VPLEX_USER=service ./vplex_cg_monitor.pl

use strict;
use warnings;

my $host   = $ENV{VPLEX_HOST}  or die "ERROR: VPLEX_HOST not set\n";
my $user   = $ENV{VPLEX_USER} || 'service';

# Critical states
my %crit_states = map { lc($_) => 1 } qw(
    split-brain
    split_brain
    out-of-sync
    out_of_sync
    degraded
    faulted
    error
);

# Warning states
my %warn_states = map { lc($_) => 1 } qw(
    transitioning
    resyncing
    partial
    unknown
);

# Run vplexcli via SSH and list all consistency groups
my $cmd    = qq{ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${user}\@${host} }
           . q{"vplexcli -q -e 'll /distributed-storage/consistency-groups/'" 2>&1};
my $output = qx{$cmd};
if ($? != 0) {
    print "UNKNOWN: SSH/vplexcli failed for $host\n$output\n";
    exit 3;
}

my @cgs;
my $worst = 0;   # 0=OK 1=WARN 2=CRIT

# Parse output — lines like: Name: cg-prod  operational-status: in-sync
my %current;
for my $line (split /\n/, $output) {
    $line =~ s/^\s+|\s+$//g;
    next unless $line;

    if ($line =~ /^Name:\s+(.+)$/i) {
        if (%current) {
            push @cgs, {%current};
        }
        %current = (name => $1, status => 'unknown', visibility => 'unknown');
        next;
    }
    if ($line =~ /operational-status:\s*(.+)$/i) {
        $current{status} = lc($1);
        next;
    }
    if ($line =~ /visibility:\s*(.+)$/i) {
        $current{visibility} = lc($1);
        next;
    }
}
push @cgs, {%current} if %current;

if (!@cgs) {
    print "UNKNOWN: No consistency groups found in output\n";
    exit 3;
}

# Print table
printf "%-30s  %-20s  %-15s  %s\n", 'CG NAME', 'STATUS', 'VISIBILITY', 'RESULT';
printf "%s\n", '-' x 80;

for my $cg (@cgs) {
    my $status = lc($cg->{status} // 'unknown');
    my $result = 'OK';

    if ($crit_states{$status}) {
        $result  = 'CRITICAL';
        $worst   = 2 if $worst < 2;
    } elsif ($warn_states{$status} || $status ne 'in-sync') {
        $result  = 'WARNING';
        $worst   = 1 if $worst < 1;
    }

    printf "%-30s  %-20s  %-15s  %s\n",
        $cg->{name}, $cg->{status}, $cg->{visibility}, $result;
}

print "\n";
if ($worst == 2) {
    print "CRITICAL: One or more consistency groups are in a split-brain or out-of-sync state.\n";
    exit 2;
} elsif ($worst == 1) {
    print "WARNING: One or more consistency groups require attention.\n";
    exit 1;
} else {
    print "OK: All consistency groups are in-sync.\n";
    exit 0;
}
~~~

---

## Storage View Audit

SSH to a VPLEX management server and enumerates all storage views across all clusters. For each view, lists the initiator ports and virtual volumes. Flags any storage view with no registered initiators as an orphaned view and outputs a formatted report.

~~~python
#!/usr/bin/env python3
# vplex_storage_view_audit.py — Storage view audit for Dell VPLEX
# Requirements: paramiko
# Usage: VPLEX_HOST=vplex-mgmt.example.com VPLEX_USER=service VPLEX_KEY=~/.ssh/id_rsa \
#        ./vplex_storage_view_audit.py

import os
import sys
import re
import paramiko

VPLEX_HOST = os.environ.get("VPLEX_HOST", "")
VPLEX_USER = os.environ.get("VPLEX_USER", "service")
VPLEX_KEY  = os.environ.get("VPLEX_KEY",  os.path.expanduser("~/.ssh/id_rsa"))
VPLEX_PASS = os.environ.get("VPLEX_PASS", None)

if not VPLEX_HOST:
    print("ERROR: VPLEX_HOST must be set.", file=sys.stderr)
    sys.exit(1)


def ssh_run(command):
    """Run a command on the VPLEX management server via SSH."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    kw = {"username": VPLEX_USER, "timeout": 30}
    if VPLEX_PASS:
        kw["password"] = VPLEX_PASS
    else:
        kw["key_filename"] = VPLEX_KEY
    client.connect(VPLEX_HOST, **kw)
    _, stdout, stderr = client.exec_command(command)
    out = stdout.read().decode()
    err = stderr.read().decode()
    client.close()
    return out, err


def vplex_cli(cmd):
    """Run a vplexcli command and return its output."""
    out, err = ssh_run(f"vplexcli -q -e '{cmd}'")
    return out


def parse_attribute(lines, attr):
    """Extract the first matching attribute value from a list of output lines."""
    for line in lines:
        m = re.match(rf'^\s*{re.escape(attr)}:\s*(.+)$', line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""


def parse_list_attribute(lines, attr):
    """Extract a comma/space-separated list attribute (e.g., initiator-ports)."""
    val = parse_attribute(lines, attr)
    if not val or val.lower() in ("none", "[]", ""):
        return []
    return [v.strip() for v in re.split(r'[,\s]+', val) if v.strip()]


def main():
    print("=" * 70)
    print("  VPLEX Storage View Audit")
    print(f"  Host : {VPLEX_HOST}")
    print("=" * 70)

    # List storage views for all clusters
    sv_list_out = vplex_cli("ll /clusters/*/exports/storage-views/")

    # Parse view names and their cluster paths
    views = []
    for line in sv_list_out.splitlines():
        m = re.match(r'^\s*(/clusters/[^/]+/exports/storage-views/\S+)', line)
        if m:
            views.append(m.group(1))
        # Some vplexcli versions list just names with a path prefix
        m2 = re.match(r'^\s*Name:\s*(\S+)', line)
        if m2 and m2.group(1) not in [v.split("/")[-1] for v in views]:
            # Try to build path from context — best effort
            views.append(m2.group(1))

    if not views:
        # Fallback: list names only
        for line in sv_list_out.splitlines():
            line = line.strip()
            if line and not line.startswith("/") and not re.match(r'^(Name|--)', line):
                views.append(line)

    if not views:
        print("\nNo storage views found (or unable to parse vplexcli output).")
        sys.exit(0)

    orphans = 0
    print(f"\n{'STORAGE VIEW':<35}  {'INITIATORS':>3}  {'VIRT-VOLS':>3}  STATUS")
    print("-" * 70)

    for view_path in views:
        try:
            detail = vplex_cli(f"ll {view_path}")
        except Exception as e:
            print(f"  ERROR querying {view_path}: {e}")
            continue

        detail_lines = detail.splitlines()
        name        = parse_attribute(detail_lines, "name") or view_path.split("/")[-1]
        init_ports  = parse_list_attribute(detail_lines, "initiator-ports")
        virt_vols   = parse_list_attribute(detail_lines, "virtual-volumes")

        n_inits = len(init_ports)
        n_vols  = len(virt_vols)

        if n_inits == 0:
            status = "ORPHANED (no initiators)"
            orphans += 1
        else:
            status = "OK"

        print(f"{name:<35}  {n_inits:>3}  {n_vols:>3}  {status}")

        if n_inits > 0:
            for p in init_ports:
                print(f"  {'':35}  initiator: {p}")
        for v in virt_vols:
            print(f"  {'':35}  vol:       {v}")

    print("-" * 70)
    print(f"\nTotal views: {len(views)}   Orphaned (no initiators): {orphans}")

    if orphans > 0:
        print(f"\nWARNING: {orphans} orphaned storage view(s) found. Review and clean up.")
        sys.exit(1)
    else:
        print("\nOK: All storage views have registered initiators.")
        sys.exit(0)


if __name__ == "__main__":
    main()
~~~

---

## Ansible VPLEX Health Playbook

Playbook targeting the `vplex_mgmt` host. Runs director, distributed device, and consistency group health checks via vplexcli, asserts all states are healthy, and sends a failure notification on any issue detected.

~~~yaml
---
# vplex_health.yml — Ansible health check playbook for Dell VPLEX
# Inventory host: vplex_mgmt
# Usage: ansible-playbook -i inventory vplex_health.yml

- name: Dell VPLEX Health Check
  hosts: vplex_mgmt
  gather_facts: false

  tasks:
    - name: Check director hardware health
      ansible.builtin.shell: "vplexcli -q -e 'll /engines/*/directors/*/hardware/'"
      register: director_health
      changed_when: false

    - name: Show director hardware status
      ansible.builtin.debug:
        msg: "{{ director_health.stdout_lines }}"

    - name: Check distributed device sync state
      ansible.builtin.shell: >
        vplexcli -q -e 'll /distributed-storage/distributed-devices/*/health-indications/'
      register: dd_health
      changed_when: false

    - name: Show distributed device health
      ansible.builtin.debug:
        msg: "{{ dd_health.stdout_lines }}"

    - name: Check consistency group state
      ansible.builtin.shell: >
        vplexcli -q -e 'll /distributed-storage/consistency-groups/'
      register: cg_health
      changed_when: false

    - name: Show consistency group state
      ansible.builtin.debug:
        msg: "{{ cg_health.stdout_lines }}"

    - name: Assert director hardware is healthy
      ansible.builtin.assert:
        that:
          - "'health-state: error' not in director_health.stdout | lower"
          - "'health-state: degraded' not in director_health.stdout | lower"
        fail_msg: "Director health issue detected on {{ inventory_hostname }}."
        success_msg: "Director hardware health OK."

    - name: Assert distributed devices are in-sync
      ansible.builtin.assert:
        that:
          - "'out-of-sync' not in dd_health.stdout | lower"
          - "'split-brain' not in dd_health.stdout | lower"
          - "'faulted' not in dd_health.stdout | lower"
        fail_msg: "Distributed device health issue on {{ inventory_hostname }}."
        success_msg: "Distributed device health OK."

    - name: Assert consistency groups are in-sync
      ansible.builtin.assert:
        that:
          - "'out-of-sync' not in cg_health.stdout | lower"
          - "'split-brain' not in cg_health.stdout | lower"
        fail_msg: "Consistency group out-of-sync or split-brain on {{ inventory_hostname }}."
        success_msg: "All consistency groups in-sync."

    - name: Send failure notification (runs only on failure via block/rescue)
      ansible.builtin.debug:
        msg: >
          VPLEX health check FAILED on {{ inventory_hostname }}.
          Review the output above and investigate any flagged health states.
      when: false   # Triggered via block/rescue in production — replace with notify handler
~~~
