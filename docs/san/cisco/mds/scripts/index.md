# Scripts

> Part of the [Cisco MDS](../) reference.

---

## Fabric Health Check (Bash)

SSH to a Cisco MDS switch, collect key diagnostic outputs, and print a health summary flagging down interfaces, environmental issues, and zoning problems.

~~~bash
#!/bin/bash
# mds_fabric_health.sh
# Usage: MDS_HOST=mds1 MDS_USER=admin ./mds_fabric_health.sh

MDS_HOST="${MDS_HOST:-192.168.1.20}"
MDS_USER="${MDS_USER:-admin}"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10"
PASS=0; WARN=1; CRIT=2
overall=0

run_cmd() {
  ssh $SSH_OPTS "${MDS_USER}@${MDS_HOST}" "$1" 2>/dev/null
}

status_label() {
  case $1 in
    0) echo "PASS"    ;;
    1) echo "WARNING" ;;
    2) echo "CRITICAL";;
  esac
}

echo "==============================="
echo " Cisco MDS Fabric Health Check"
echo " Host : ${MDS_HOST}"
echo " $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "==============================="

# --- show interface brief ---
intf_out=$(run_cmd "show interface brief")
down_fc=$(echo "$intf_out" | awk '/^fc/ && /down/' | wc -l | tr -d ' ')
if   [ "$down_fc" -gt 5 ]; then s=$CRIT
elif [ "$down_fc" -gt 0 ]; then s=$WARN
else s=$PASS; fi
[ $s -gt $overall ] && overall=$s
printf "[%-8s] interface brief    — %d FC interface(s) down\n" "$(status_label $s)" "$down_fc"

# --- show flogi database ---
flogi_out=$(run_cmd "show flogi database")
flogi_count=$(echo "$flogi_out" | grep -c "^fc") || flogi_count=0
printf "[%-8s] flogi database     — %d logged-in device(s)\n" "PASS" "$flogi_count"

# --- show topology ---
topo_out=$(run_cmd "show topology")
isolated=$(echo "$topo_out" | grep -ic "isolated\|no ISL") || isolated=0
if   [ "$isolated" -gt 0 ]; then s=$WARN
else s=$PASS; fi
[ $s -gt $overall ] && overall=$s
printf "[%-8s] topology           — %d isolated switch/ISL issue(s)\n" "$(status_label $s)" "$isolated"

# --- show zoneset active ---
zone_out=$(run_cmd "show zoneset active")
zone_err=$(echo "$zone_out" | grep -ic "error\|mismatch") || zone_err=0
if   [ "$zone_err" -gt 0 ]; then s=$CRIT
else s=$PASS; fi
[ $s -gt $overall ] && overall=$s
printf "[%-8s] zoneset active     — %d zoning error(s)\n" "$(status_label $s)" "$zone_err"

# --- show logging last 50 ---
log_out=$(run_cmd "show logging last 50")
log_crit=$(echo "$log_out" | grep -ic "critical\|ERROR\|link down") || log_crit=0
if   [ "$log_crit" -gt 5 ]; then s=$CRIT
elif [ "$log_crit" -gt 0 ]; then s=$WARN
else s=$PASS; fi
[ $s -gt $overall ] && overall=$s
printf "[%-8s] logging            — %d critical/error log line(s)\n" "$(status_label $s)" "$log_crit"

# --- show environment ---
env_out=$(run_cmd "show environment")
env_warn=$(echo "$env_out" | grep -ic "warning\|critical\|fail\|absent") || env_warn=0
if   [ "$env_warn" -gt 0 ]; then s=$CRIT
else s=$PASS; fi
[ $s -gt $overall ] && overall=$s
printf "[%-8s] environment        — %d environmental alert(s)\n" "$(status_label $s)" "$env_warn"

echo "==============================="
printf " Overall: %s\n" "$(status_label $overall)"
echo "==============================="
exit $overall
~~~

---

## FLOGI Database Report (Python)

SSH to MDS using Paramiko, parse the FLOGI database per VSAN, and flag duplicate FCIDs, unexpected VSAN logins, and unzoned devices.

~~~python
#!/usr/bin/env python3
"""
mds_flogi_report.py
Usage: python3 mds_flogi_report.py
"""

import os, re, sys
import paramiko

MDS_HOST = os.environ.get("MDS_HOST", "192.168.1.20")
MDS_USER = os.environ.get("MDS_USER", "admin")
SSH_KEY  = os.environ.get("SSH_KEY",  os.path.expanduser("~/.ssh/id_rsa"))

# Expected VSAN IDs — devices logged in elsewhere are flagged
EXPECTED_VSANS = set(map(int, os.environ.get("EXPECTED_VSANS", "10,20").split(",")))


def ssh_run(host, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=MDS_USER, key_filename=SSH_KEY, timeout=15)
    _, stdout, _ = client.exec_command(cmd)
    out = stdout.read().decode()
    client.close()
    return out


def parse_flogi(flogi_out):
    """
    Parse 'show flogi database' output.
    Columns: INTERFACE  VSAN  FCID  PORT WWN  NODE WWN
    Returns list of dicts.
    """
    entries = []
    for line in flogi_out.splitlines():
        # fc1/1     10    0x010200  20:00:00:... 20:00:00:...
        m = re.match(
            r'^(fc\S+)\s+(\d+)\s+(0x[0-9a-fA-F]+)\s+([0-9a-fA-F:]{23})\s+([0-9a-fA-F:]{23})',
            line.strip()
        )
        if m:
            entries.append({
                "interface": m.group(1),
                "vsan":      int(m.group(2)),
                "fcid":      m.group(3),
                "pwwn":      m.group(4),
                "nwwn":      m.group(5),
            })
    return entries


def parse_active_zones(zoneset_out):
    """Return set of all PWWNs referenced in any active zone."""
    return set(re.findall(r'[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){7}', zoneset_out))


flogi_raw    = ssh_run(MDS_HOST, "show flogi database")
zoneset_raw  = ssh_run(MDS_HOST, "show zoneset active vsan all")

entries      = parse_flogi(flogi_raw)
zoned_wwns   = parse_active_zones(zoneset_raw)

# Group by VSAN
vsans = {}
for e in entries:
    vsans.setdefault(e["vsan"], []).append(e)

issues = []

for vsan_id in sorted(vsans):
    vsan_entries = vsans[vsan_id]
    print(f"\n--- VSAN {vsan_id} ({len(vsan_entries)} devices) ---")
    print(f"  {'Interface':<12} {'FCID':<10} {'Port WWN':<26} {'Status'}")
    print("  " + "-" * 70)

    seen_fcids = {}
    for e in sorted(vsan_entries, key=lambda x: x["interface"]):
        flags = []

        # Duplicate FCID detection
        if e["fcid"] in seen_fcids:
            flags.append(f"DUPLICATE_FCID (also on {seen_fcids[e['fcid']]})")
            issues.append(f"VSAN {vsan_id}: Duplicate FCID {e['fcid']} on {e['interface']} and {seen_fcids[e['fcid']]}")
        else:
            seen_fcids[e["fcid"]] = e["interface"]

        # Unexpected VSAN login
        if EXPECTED_VSANS and vsan_id not in EXPECTED_VSANS:
            flags.append(f"UNEXPECTED_VSAN")
            issues.append(f"VSAN {vsan_id}: Device {e['pwwn']} logged into unexpected VSAN")

        # Unzoned device
        if e["pwwn"] not in zoned_wwns:
            flags.append("UNZONED")
            issues.append(f"VSAN {vsan_id}: Device {e['pwwn']} on {e['interface']} is not in any active zone")

        status = ", ".join(flags) if flags else "OK"
        print(f"  {e['interface']:<12} {e['fcid']:<10} {e['pwwn']:<26} {status}")

print(f"\n\n{'='*50}")
if issues:
    print(f"ISSUES FOUND ({len(issues)}):")
    for i in issues:
        print(f"  {i}")
    sys.exit(1)
else:
    print("No issues found.")
    sys.exit(0)
~~~

---

## Zoning Consistency Audit (Perl)

SSH to MDS, cross-reference active zone members against the FLOGI database, and report stale zone entries and unzoned devices per VSAN.

~~~perl
#!/usr/bin/env perl
# mds_zoning_audit.pl
# Usage: MDS_HOST=mds1 MDS_USER=admin perl mds_zoning_audit.pl

use strict;
use warnings;

my $MDS_HOST  = $ENV{MDS_HOST}  // '192.168.1.20';
my $MDS_USER  = $ENV{MDS_USER}  // 'admin';
my $SSH_OPTS  = '-o StrictHostKeyChecking=no -o ConnectTimeout=10 -o BatchMode=yes';

sub ssh_cmd {
    my ($cmd) = @_;
    return `ssh $SSH_OPTS ${MDS_USER}\@${MDS_HOST} "$cmd" 2>/dev/null`;
}

my $zoneset_out = ssh_cmd('show zoneset active vsan all');
my $flogi_out   = ssh_cmd('show flogi database vsan all');

# --- Parse logged-in WWNs per VSAN ---
my %logged_in;  # vsan -> { pwwn -> interface }
for my $line (split /\n/, $flogi_out) {
    if ($line =~ /^(fc\S+)\s+(\d+)\s+0x[0-9a-fA-F]+\s+([0-9a-fA-F:]{23})/) {
        $logged_in{$2}{$3} = $1;
    }
}

# --- Parse active zone members per VSAN ---
my %zone_members;  # vsan -> zone -> [wwns]
my ($cur_vsan, $cur_zone);
for my $line (split /\n/, $zoneset_out) {
    if ($line =~ /vsan\s+(\d+)/i) {
        $cur_vsan = $1;
    } elsif ($line =~ /^\s+zone\s+name\s+(\S+)/i) {
        $cur_zone = $1;
    } elsif ($cur_vsan && $cur_zone && $line =~ /([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){7})/) {
        push @{$zone_members{$cur_vsan}{$cur_zone}}, $1;
    }
}

my @findings;

for my $vsan (sort { $a <=> $b } keys %zone_members) {
    my $li = $logged_in{$vsan} // {};

    # Collect all zoned WWNs for this VSAN
    my %zoned_wwns;
    for my $zone (keys %{$zone_members{$vsan}}) {
        for my $wwn (@{$zone_members{$vsan}{$zone}}) {
            $zoned_wwns{$wwn} = $zone;

            # Stale zone member (in zone but not logged in)
            unless (exists $li->{$wwn}) {
                push @findings,
                    sprintf("WARN  VSAN %4d  STALE    zone=%-30s  wwn=%s  (not logged in)", $vsan, $zone, $wwn);
            }
        }
    }

    # Unzoned devices (logged in but not in any zone)
    for my $pwwn (keys %{$li}) {
        unless (exists $zoned_wwns{$pwwn}) {
            push @findings,
                sprintf("CRIT  VSAN %4d  UNZONED  intf=%-10s  wwn=%s", $vsan, $li->{$pwwn}, $pwwn);
        }
    }
}

printf "=== MDS Zoning Consistency Audit: %s ===\n\n", $MDS_HOST;

if (@findings) {
    print "$_\n" for sort @findings;
} else {
    print "No issues found.\n";
}

my $crits = scalar grep { /^CRIT/ } @findings;
my $warns = scalar grep { /^WARN/ } @findings;
printf "\nSummary: %d critical, %d warnings\n", $crits, $warns;
exit $crits ? 2 : $warns ? 1 : 0;
~~~

---

## Interface Error Counter Monitor (Bash)

Collect FC interface error counters from MDS, compare against a stored baseline, and alert on significant increments.

~~~bash
#!/bin/bash
# mds_interface_errors.sh
# Usage: MDS_HOST=mds1 MDS_USER=admin ./mds_interface_errors.sh
# Run via cron every 15 minutes.

MDS_HOST="${MDS_HOST:-192.168.1.20}"
MDS_USER="${MDS_USER:-admin}"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10 -o BatchMode=yes"
BASELINE_FILE="/var/tmp/mds_err_baseline_${MDS_HOST}.dat"
ALERT_THRESHOLD=100   # increment threshold to alert
CRIT_THRESHOLD=1000
TS=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

# Collect current error counters
raw=$(ssh $SSH_OPTS "${MDS_USER}@${MDS_HOST}" "show interface counters errors" 2>/dev/null)

if [ -z "$raw" ]; then
  echo "[$TS] ERROR: Could not connect to $MDS_HOST" >&2
  exit 2
fi

declare -A current

while IFS= read -r line; do
  # Match interface line: fc1/1 is up
  if [[ $line =~ ^(fc[0-9/]+) ]]; then
    cur_intf="${BASH_REMATCH[1]}"
  fi
  # Match counter lines: "   2 input errors"
  if [[ -n "$cur_intf" && $line =~ ([0-9]+)[[:space:]]+(input errors|output errors|discards|buffer credit recovery|link failures) ]]; then
    key="${cur_intf}__${BASH_REMATCH[2]// /_}"
    current["$key"]="${BASH_REMATCH[1]}"
  fi
done <<< "$raw"

# Load baseline
declare -A baseline
if [ -f "$BASELINE_FILE" ]; then
  while IFS=$'\t' read -r k v; do
    baseline["$k"]="$v"
  done < "$BASELINE_FILE"
fi

# Compare
alerts=()
for key in "${!current[@]}"; do
  cur="${current[$key]}"
  base="${baseline[$key]:-0}"
  delta=$(( cur - base ))
  (( delta < 0 )) && delta=0  # counter reset
  if (( delta >= CRIT_THRESHOLD )); then
    alerts+=("CRIT  ${key/__/  }  delta=${delta}")
  elif (( delta >= ALERT_THRESHOLD )); then
    alerts+=("WARN  ${key/__/  }  delta=${delta}")
  fi
done

# Print results
echo "[$TS] MDS Interface Error Monitor — $MDS_HOST"
if [ ${#alerts[@]} -gt 0 ]; then
  printf '%s\n' "${alerts[@]}"
  rc=1
else
  echo "OK — all counter deltas within threshold"
  rc=0
fi

# Save new baseline
: > "$BASELINE_FILE"
for key in "${!current[@]}"; do
  printf '%s\t%s\n' "$key" "${current[$key]}" >> "$BASELINE_FILE"
done

exit $rc
~~~

---

## Ansible MDS Config Backup Playbook

Capture running configuration, NX-OS version, and active zoning from all MDS switches in the `cisco_mds` group, then archive with a datestamp.

~~~yaml
---
# mds_backup.yml
# Usage: ansible-playbook -i inventory mds_backup.yml
# Inventory group: cisco_mds
# Required vars: mds_user, backup_path

- name: Cisco MDS — Configuration Backup
  hosts: cisco_mds
  gather_facts: false
  vars:
    mds_user: admin
    backup_path: /backups/mds
    date_stamp: "{{ lookup('pipe', 'date +%Y%m%d_%H%M%S') }}"
    local_tmp: "/tmp/mds_backup_{{ inventory_hostname }}_{{ date_stamp }}"

  tasks:

    - name: Create local temp directory
      ansible.builtin.file:
        path: "{{ local_tmp }}"
        state: directory
        mode: "0750"
      delegate_to: localhost

    - name: Capture running configuration
      ansible.builtin.raw: show running-config
      register: running_config

    - name: Save running-config to local file
      ansible.builtin.copy:
        content: "{{ running_config.stdout }}"
        dest: "{{ local_tmp }}/running-config.txt"
      delegate_to: localhost

    - name: Capture NX-OS version
      ansible.builtin.raw: show version
      register: show_version

    - name: Save version output
      ansible.builtin.copy:
        content: "{{ show_version.stdout }}"
        dest: "{{ local_tmp }}/version.txt"
      delegate_to: localhost

    - name: Capture active zoneset (all VSANs)
      ansible.builtin.raw: show zoneset active vsan all
      register: zoneset_active

    - name: Save zoneset output
      ansible.builtin.copy:
        content: "{{ zoneset_active.stdout }}"
        dest: "{{ local_tmp }}/zoneset-active.txt"
      delegate_to: localhost

    - name: Archive outputs to backup server
      ansible.builtin.archive:
        path: "{{ local_tmp }}"
        dest: "{{ backup_path }}/{{ inventory_hostname }}_backup_{{ date_stamp }}.tar.gz"
        format: gz
      delegate_to: localhost

    - name: Report completion
      ansible.builtin.debug:
        msg: "Backup complete: {{ backup_path }}/{{ inventory_hostname }}_backup_{{ date_stamp }}.tar.gz"
~~~
