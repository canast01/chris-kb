# Scripts

> Part of the [NetApp ONTAP](../) reference.

---

## Cluster Health Check (Perl)

SSH to an ONTAP cluster management LIF, run key health commands, parse the output, and print a PASS/WARNING/CRITICAL summary with an exit code reflecting the worst finding.

~~~perl
#!/usr/bin/perl
use strict;
use warnings;
use Net::SSH2;

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
my $CLUSTER     = $ENV{ONTAP_HOST}  // die "Set ONTAP_HOST\n";
my $USER        = $ENV{ONTAP_USER}  // die "Set ONTAP_USER\n";
my $PASS        = $ENV{ONTAP_PASS}  // die "Set ONTAP_PASS\n";
my $AGG_WARN    = 85;   # aggregate used-percent warning threshold
my $PORT        = 22;

# Exit codes
use constant OK       => 0;
use constant WARNING  => 1;
use constant CRITICAL => 2;

my $worst = OK;
my @messages;

# -------------------------------------------------------------------
# SSH helper
# -------------------------------------------------------------------
sub ssh_run {
    my ($ssh2, $cmd) = @_;
    my $chan = $ssh2->channel() or die "Cannot open SSH channel\n";
    $chan->exec($cmd);
    my $out = '';
    while (!$chan->eof) {
        $chan->read(my $buf, 4096);
        $out .= $buf // '';
    }
    $chan->close;
    return $out;
}

sub set_status {
    my ($level, $msg) = @_;
    push @messages, "[${\( $level == CRITICAL ? 'CRITICAL' : 'WARNING' )}] $msg";
    $worst = $level if $level > $worst;
}

# -------------------------------------------------------------------
# Connect
# -------------------------------------------------------------------
my $ssh2 = Net::SSH2->new();
$ssh2->connect($CLUSTER, $PORT) or die "Cannot connect to $CLUSTER: $!\n";
$ssh2->auth_password($USER, $PASS) or die "Authentication failed\n";

# -------------------------------------------------------------------
# Check 1: Broken disks
# -------------------------------------------------------------------
print "Checking broken disks...\n";
my $disk_out = ssh_run($ssh2, 'storage disk show -broken -fields disk,container-type 2>/dev/null');
my @broken = grep { /\S/ && !/Disk\s+Container/ && !/^\s*$/ } split /\n/, $disk_out;
if (@broken) {
    set_status(CRITICAL, scalar(@broken) . " broken disk(s) found");
} else {
    push @messages, "[OK] No broken disks";
}

# -------------------------------------------------------------------
# Check 2: Aggregate capacity
# -------------------------------------------------------------------
print "Checking aggregate capacity...\n";
my $agg_out = ssh_run($ssh2, 'storage aggregate show -fields aggregate,used-percent,state -type data');
for my $line (split /\n/, $agg_out) {
    next unless $line =~ /^\S/;
    next if $line =~ /aggregate\s+used-percent/;   # header
    next if $line =~ /^\d+ entries/;
    my ($agg, $pct, $state) = split /\s+/, $line;
    next unless defined $pct && $pct =~ /^\d+$/;
    if ($pct >= $AGG_WARN) {
        my $lvl = $pct >= 90 ? CRITICAL : WARNING;
        set_status($lvl, "Aggregate $agg is ${pct}% used");
    }
}
push @messages, "[OK] All aggregates below ${AGG_WARN}%" unless grep { /Aggregate / } @messages;

# -------------------------------------------------------------------
# Check 3: Storage failover (HA)
# -------------------------------------------------------------------
print "Checking storage failover...\n";
my $sfo_out = ssh_run($ssh2, 'storage failover show -fields node,enabled,state');
for my $line (split /\n/, $sfo_out) {
    next if $line =~ /node\s+enabled|^\s*$|^\d+ entries/;
    my ($node, $enabled, $state) = split /\s+/, $line;
    next unless defined $state;
    if ($enabled ne 'true' || $state !~ /Connected|Takeover/) {
        set_status(WARNING, "HA issue on node $node: enabled=$enabled state=$state");
    }
}
push @messages, "[OK] Storage failover healthy" unless grep { /HA issue/ } @messages;

# -------------------------------------------------------------------
# Check 4: Active health alerts
# -------------------------------------------------------------------
print "Checking health alerts...\n";
my $alert_out = ssh_run($ssh2, 'system health alert show -fields node,monitor,alert-id,severity 2>/dev/null');
my @alerts = grep { /\S/ && !/node\s+monitor/ && !/^\s*$/ && !/^\d+ entries/ } split /\n/, $alert_out;
if (@alerts) {
    set_status(WARNING, scalar(@alerts) . " active health alert(s)");
} else {
    push @messages, "[OK] No active health alerts";
}

# -------------------------------------------------------------------
# Disconnect and report
# -------------------------------------------------------------------
$ssh2->disconnect;

my $label = $worst == CRITICAL ? 'CRITICAL' : $worst == WARNING ? 'WARNING' : 'OK';
print "\n=== ONTAP Cluster Health: $CLUSTER ===\n";
print "$_\n" for @messages;
print "\nOverall status: $label\n";
exit $worst;
~~~

---

## SnapMirror Lag Monitor (Bash)

SSH to an ONTAP destination cluster, parse all SnapMirror relationships, convert lag times to minutes, and print a table with PASS/WARN/CRIT per relationship.

~~~bash
#!/bin/bash
# SnapMirror Lag Monitor
# Usage: ONTAP_HOST=cluster ONTAP_USER=admin ONTAP_PASS=secret ./sm_lag.sh

set -euo pipefail

CLUSTER="${ONTAP_HOST:?Set ONTAP_HOST}"
USER="${ONTAP_USER:?Set ONTAP_USER}"
PASS="${ONTAP_PASS:?Set ONTAP_PASS}"
WARN_MIN="${SM_WARN_MIN:-60}"
CRIT_MIN="${SM_CRIT_MIN:-120}"

# ANSI colours
RED='\033[0;31m'; YEL='\033[0;33m'; GRN='\033[0;32m'; NC='\033[0m'

worst=0   # 0=OK 1=WARN 2=CRIT

lag_to_minutes() {
    # Input formats: "0:10:05" or "1day 02:15:00"
    local raw="$1"
    local days=0 hours=0 mins=0
    if [[ "$raw" =~ ([0-9]+)day ]]; then
        days="${BASH_REMATCH[1]}"
        raw="${raw#*day}"
        raw="${raw#s}"   # strip trailing 's'
        raw="${raw# }"
    fi
    if [[ "$raw" =~ ^([0-9]+):([0-9]+):([0-9]+)$ ]]; then
        hours="${BASH_REMATCH[1]}"
        mins="${BASH_REMATCH[2]}"
    fi
    echo $(( days * 1440 + hours * 60 + mins ))
}

# Fetch SnapMirror data via SSH (password via sshpass; adjust as needed)
if ! command -v sshpass &>/dev/null; then
    echo "ERROR: sshpass required. Install with: brew install hudochenkov/sshpass/sshpass" >&2
    exit 3
fi

RAW=$(sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o BatchMode=no \
    "${USER}@${CLUSTER}" \
    'snapmirror show -fields source-path,destination-path,lag-time,healthy,state 2>/dev/null' 2>/dev/null)

printf "\n%-60s %-15s %-8s %s\n" "RELATIONSHIP" "LAG (min)" "HEALTHY" "STATUS"
printf '%0.s-' {1..100}; echo

while IFS= read -r line; do
    # Skip header and summary lines
    [[ "$line" =~ ^(source-path|[[:space:]]*$|[0-9]+ entries) ]] && continue

    src=$(echo "$line" | awk '{print $1}')
    dst=$(echo "$line" | awk '{print $2}')
    lag=$(echo "$line" | awk '{print $3}')
    healthy=$(echo "$line" | awk '{print $4}')
    state=$(echo "$line" | awk '{print $5}')

    [[ -z "$src" || -z "$dst" ]] && continue

    lag_min=$(lag_to_minutes "${lag:-0:00:00}")
    rel="${src} -> ${dst}"

    if [[ "$healthy" != "true" ]]; then
        status="${RED}UNHEALTHY${NC}"
        (( worst < 2 )) && worst=2
    elif (( lag_min >= CRIT_MIN )); then
        status="${RED}CRITICAL (lag)${NC}"
        (( worst < 2 )) && worst=2
    elif (( lag_min >= WARN_MIN )); then
        status="${YEL}WARNING (lag)${NC}"
        (( worst < 1 )) && worst=1
    else
        status="${GRN}OK${NC}"
    fi

    printf "%-60s %-15s %-8s " "${rel:0:59}" "$lag_min" "$healthy"
    echo -e "$status"
done <<< "$RAW"

echo
case $worst in
    0) echo -e "${GRN}All SnapMirror relationships are healthy.${NC}" ;;
    1) echo -e "${YEL}WARNING: One or more relationships exceed the lag warning threshold.${NC}" ;;
    2) echo -e "${RED}CRITICAL: One or more relationships are unhealthy or exceed the critical lag threshold.${NC}" ;;
esac
exit $worst
~~~

---

## Volume Capacity Reporter (Python)

SSH to ONTAP, collect volume space data, print a table sorted by utilisation, highlight volumes approaching capacity, and optionally export to CSV.

~~~python
#!/usr/bin/env python3
"""
ONTAP Volume Capacity Reporter
Usage: python3 vol_reporter.py [--csv output.csv]
Requires: pip install paramiko tabulate
"""

import argparse
import csv
import sys
import paramiko

# -------------------------------------------------------------------
# Configuration (override with environment variables or edit here)
# -------------------------------------------------------------------
import os
CLUSTER  = os.environ.get("ONTAP_HOST", "")
USER     = os.environ.get("ONTAP_USER", "admin")
PASS     = os.environ.get("ONTAP_PASS", "")
WARN_PCT = 80
CRIT_PCT = 90

if not CLUSTER or not PASS:
    sys.exit("Set ONTAP_HOST and ONTAP_PASS environment variables.")

# ANSI colours
RED  = "\033[0;31m"
YEL  = "\033[0;33m"
GRN  = "\033[0;32m"
NC   = "\033[0m"

# -------------------------------------------------------------------
# SSH helper
# -------------------------------------------------------------------
def ssh_run(client, command):
    _, stdout, _ = client.exec_command(command)
    return stdout.read().decode(errors="replace")

# -------------------------------------------------------------------
# Parse ONTAP volume show output
# -------------------------------------------------------------------
def parse_volumes(raw):
    volumes = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("Vserver") or line.startswith("---") or "entries were displayed" in line:
            continue
        parts = line.split()
        if len(parts) < 6:
            continue
        vserver, volume, size, used, pct_raw, state, *_ = parts
        try:
            pct = int(pct_raw.rstrip("%"))
        except ValueError:
            continue
        volumes.append({
            "vserver": vserver,
            "volume":  volume,
            "size":    size,
            "used":    used,
            "pct":     pct,
            "state":   state,
        })
    return sorted(volumes, key=lambda v: v["pct"], reverse=True)

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="ONTAP Volume Capacity Reporter")
    parser.add_argument("--csv", metavar="FILE", help="Export results to CSV file")
    args = parser.parse_args()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(CLUSTER, username=USER, password=PASS, look_for_keys=False)

    raw = ssh_run(client, "volume show -fields vserver,volume,size,used,percent-used,state 2>/dev/null")
    client.close()

    volumes = parse_volumes(raw)

    # Print table header
    header = f"{'VSERVER':<25} {'VOLUME':<30} {'SIZE':>8} {'USED':>8} {'PCT':>5}  {'STATE':<10}  STATUS"
    print(f"\nONTAP Volume Capacity Report — {CLUSTER}")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for v in volumes:
        pct = v["pct"]
        if pct >= CRIT_PCT:
            colour, tag = RED, "CRITICAL"
        elif pct >= WARN_PCT:
            colour, tag = YEL, "WARNING"
        else:
            colour, tag = GRN, "OK"

        row = (
            f"{v['vserver']:<25} {v['volume']:<30} {v['size']:>8} {v['used']:>8} {pct:>4}%"
            f"  {v['state']:<10}  {tag}"
        )
        print(f"{colour}{row}{NC}")

    print(f"\nTotal volumes: {len(volumes)}")
    criticals = [v for v in volumes if v["pct"] >= CRIT_PCT]
    warnings  = [v for v in volumes if WARN_PCT <= v["pct"] < CRIT_PCT]
    if criticals:
        print(f"{RED}{len(criticals)} volume(s) CRITICAL (>= {CRIT_PCT}% used){NC}")
    if warnings:
        print(f"{YEL}{len(warnings)} volume(s) WARNING (>= {WARN_PCT}% used){NC}")

    # Optional CSV export
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["vserver","volume","size","used","pct","state"])
            writer.writeheader()
            writer.writerows(volumes)
        print(f"\nExported to {args.csv}")

if __name__ == "__main__":
    main()
~~~

---

## Ansible ONTAP Health Playbook

Query the ONTAP REST API to check cluster health, aggregate space, and SnapMirror relationships, then fail if any aggregate exceeds 85% or any SnapMirror relationship is unhealthy.

~~~yaml
---
# ONTAP Health Playbook
# Requirements: ansible-galaxy collection install netapp.ontap
# Variables: ontap_hostname, ontap_username, ontap_password
#
# Run: ansible-playbook ontap_health.yml \
#        -e "ontap_hostname=cluster1 ontap_username=admin ontap_password=secret"

- name: ONTAP Health Check
  hosts: localhost
  gather_facts: false
  vars:
    ontap_validate_certs: false
    agg_warn_pct: 85

  tasks:

    - name: Get cluster health
      ansible.builtin.uri:
        url: "https://{{ ontap_hostname }}/api/cluster"
        method: GET
        user: "{{ ontap_username }}"
        password: "{{ ontap_password }}"
        force_basic_auth: true
        validate_certs: "{{ ontap_validate_certs }}"
        return_content: true
      register: cluster_info

    - name: Print cluster health
      ansible.builtin.debug:
        msg: >-
          Cluster: {{ cluster_info.json.name }}
          | Version: {{ cluster_info.json.version.full }}
          | Healthy: {{ cluster_info.json.metric.status | default('unknown') }}

    - name: Get aggregate space
      ansible.builtin.uri:
        url: "https://{{ ontap_hostname }}/api/storage/aggregates?fields=name,space,state"
        method: GET
        user: "{{ ontap_username }}"
        password: "{{ ontap_password }}"
        force_basic_auth: true
        validate_certs: "{{ ontap_validate_certs }}"
        return_content: true
      register: agg_info

    - name: Build list of over-threshold aggregates
      ansible.builtin.set_fact:
        over_threshold: >-
          {{ agg_info.json.records
             | selectattr('space', 'defined')
             | selectattr('name', 'match', '^(?!aggr0_)')
             | selectattr('space.block_storage.used_percent', 'ge', agg_warn_pct)
             | map(attribute='name')
             | list }}

    - name: Report aggregate status
      ansible.builtin.debug:
        msg: "{{ item.name }} — {{ item.space.block_storage.used_percent }}% used"
      loop: "{{ agg_info.json.records }}"
      when: item.space is defined

    - name: Fail if aggregates over threshold
      ansible.builtin.fail:
        msg: "Aggregates over {{ agg_warn_pct }}%: {{ over_threshold | join(', ') }}"
      when: over_threshold | length > 0

    - name: Get SnapMirror relationships
      ansible.builtin.uri:
        url: "https://{{ ontap_hostname }}/api/snapmirror/relationships?fields=source,destination,healthy,lag_time,state"
        method: GET
        user: "{{ ontap_username }}"
        password: "{{ ontap_password }}"
        force_basic_auth: true
        validate_certs: "{{ ontap_validate_certs }}"
        return_content: true
      register: sm_info

    - name: Build list of unhealthy SnapMirror relationships
      ansible.builtin.set_fact:
        unhealthy_sm: >-
          {{ sm_info.json.records
             | rejectattr('healthy', 'equalto', true)
             | map(attribute='destination.path')
             | list }}

    - name: Report SnapMirror status
      ansible.builtin.debug:
        msg: >-
          {{ item.destination.path }}
          healthy={{ item.healthy }}
          lag={{ item.lag_time | default('unknown') }}
      loop: "{{ sm_info.json.records }}"

    - name: Fail if unhealthy SnapMirror relationships exist
      ansible.builtin.fail:
        msg: "Unhealthy SnapMirror relationships: {{ unhealthy_sm | join(', ') }}"
      when: unhealthy_sm | length > 0

    - name: Health check passed
      ansible.builtin.debug:
        msg: "All ONTAP health checks passed."
~~~

---

## Aggregate Space Alert (Perl)

Connect to ONTAP via SSH, check aggregate utilisation, and print a per-aggregate status report suitable for cron scheduling. Skips `aggr0_*` root aggregates.

~~~perl
#!/usr/bin/perl
use strict;
use warnings;
use Net::SSH2;

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
my $CLUSTER  = $ENV{ONTAP_HOST}  // die "Set ONTAP_HOST\n";
my $USER     = $ENV{ONTAP_USER}  // die "Set ONTAP_USER\n";
my $PASS     = $ENV{ONTAP_PASS}  // die "Set ONTAP_PASS\n";
my $WARN_PCT = 80;
my $CRIT_PCT = 90;

my $ssh2 = Net::SSH2->new();
$ssh2->connect($CLUSTER, 22) or die "SSH connect failed: $!\n";
$ssh2->auth_password($USER, $PASS) or die "Auth failed\n";

my $chan = $ssh2->channel() or die "Channel failed\n";
$chan->exec('storage aggregate show -fields aggregate,used-percent,state -type data 2>/dev/null');
my $raw = '';
while (!$chan->eof) { $chan->read(my $buf, 4096); $raw .= $buf // '' }
$chan->close;
$ssh2->disconnect;

# -------------------------------------------------------------------
# Parse and report
# -------------------------------------------------------------------
my ($ok, $warn, $crit) = (0, 0, 0);
my @report;

for my $line (split /\n/, $raw) {
    $line =~ s/^\s+|\s+$//g;
    next unless $line =~ /\S/;
    next if $line =~ /^aggregate\s+used-percent/i;
    next if $line =~ /^\d+ entr/;

    my ($agg, $pct, $state) = split /\s+/, $line, 3;
    next unless defined $pct && $pct =~ /^\d+$/;

    # Skip root aggregates
    next if $agg =~ /^aggr0_/;

    my $status;
    if ($pct >= $CRIT_PCT) { $status = 'CRITICAL'; $crit++ }
    elsif ($pct >= $WARN_PCT) { $status = 'WARNING'; $warn++ }
    else { $status = 'OK'; $ok++ }

    push @report, sprintf("  %-35s %3d%%  state=%-10s  %s", $agg, $pct, $state // '?', $status);
}

# -------------------------------------------------------------------
# Output
# -------------------------------------------------------------------
my $ts = localtime;
print "=== ONTAP Aggregate Space Report ===\n";
print "Cluster : $CLUSTER\n";
print "Time    : $ts\n";
print "Warn at : ${WARN_PCT}%  |  Crit at : ${CRIT_PCT}%\n";
print "-" x 70 . "\n";
print "$_\n" for @report;
print "-" x 70 . "\n";
printf "Summary : OK=%d  WARNING=%d  CRITICAL=%d\n", $ok, $warn, $crit;

exit 2 if $crit;
exit 1 if $warn;
exit 0;
~~~
