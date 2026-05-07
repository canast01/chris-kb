# Scripts

> Part of the [NetApp SnapMirror](../) reference.

---
## Lag Monitor (Bash)

SSH to the destination ONTAP cluster, parse SnapMirror lag times, colour-code each relationship by severity, and exit with a code reflecting the worst status. Thresholds are configurable via environment variables.

~~~bash
#!/bin/bash
# SnapMirror Lag Monitor with ANSI colour coding
# Usage: ONTAP_HOST=dst-cluster ONTAP_USER=admin ONTAP_PASS=secret ./sm_lag_monitor.sh

set -euo pipefail

CLUSTER="${ONTAP_HOST:?Set ONTAP_HOST}"
USER="${ONTAP_USER:?Set ONTAP_USER}"
PASS="${ONTAP_PASS:?Set ONTAP_PASS}"
WARN_MIN="${SM_WARN_MIN:-30}"
CRIT_MIN="${SM_CRIT_MIN:-60}"

# ANSI colours
RED='\033[0;31m'; YEL='\033[0;33m'; GRN='\033[0;32m'; NC='\033[0m'

worst=0   # 0=OK 1=WARN 2=CRIT

if ! command -v sshpass &>/dev/null; then
    echo "ERROR: sshpass is required (brew install hudochenkov/sshpass/sshpass)" >&2
    exit 3
fi

# ------------------------------------------------------------------
# Convert lag-time string to minutes
# Formats: "0:10:05" or "1day 02:15:00" or "2days 00:00:00"
# ------------------------------------------------------------------
lag_to_minutes() {
    local raw="$1" days=0 hours=0 mins=0

    if [[ "$raw" =~ ([0-9]+)[[:space:]]*day ]]; then
        days="${BASH_REMATCH[1]}"
        raw="${raw#*day}"
        raw="${raw#s}"
        raw="${raw# }"
    fi

    if [[ "$raw" =~ ^([0-9]+):([0-9]+):([0-9]+)$ ]]; then
        hours="${BASH_REMATCH[1]}"
        mins="${BASH_REMATCH[2]}"
    fi

    echo $(( days * 1440 + hours * 60 + mins ))
}

# ------------------------------------------------------------------
# Fetch SnapMirror data from destination cluster
# ------------------------------------------------------------------
RAW=$(sshpass -p "$PASS" ssh \
    -o StrictHostKeyChecking=no \
    -o BatchMode=no \
    -o ConnectTimeout=15 \
    "${USER}@${CLUSTER}" \
    'snapmirror show -fields source-path,destination-path,lag-time,healthy,last-transfer-size,last-transfer-duration 2>/dev/null' 2>/dev/null)

echo
echo "=== SnapMirror Lag Report: ${CLUSTER} ==="
echo "Thresholds — WARN: ${WARN_MIN} min  |  CRIT: ${CRIT_MIN} min"
echo
printf "%-55s %10s  %-8s  %s\n" "RELATIONSHIP" "LAG (min)" "HEALTHY" "STATUS"
printf '%0.s-' {1..100}; echo

while IFS= read -r line; do
    [[ "$line" =~ ^(source-path|[[:space:]]*$|[0-9]+ entries) ]] && continue

    src=$(awk '{print $1}' <<< "$line")
    dst=$(awk '{print $2}' <<< "$line")
    lag=$(awk '{print $3}' <<< "$line")
    healthy=$(awk '{print $4}' <<< "$line")

    [[ -z "$src" || -z "$dst" ]] && continue

    lag_min=$(lag_to_minutes "${lag:-0:00:00}")
    rel="${src} -> ${dst}"

    if [[ "$healthy" != "true" ]]; then
        colour="$RED"; label="CRITICAL (unhealthy)"; (( worst < 2 )) && worst=2
    elif (( lag_min >= CRIT_MIN )); then
        colour="$RED"; label="CRITICAL (lag=${lag_min}m >= ${CRIT_MIN}m)"; (( worst < 2 )) && worst=2
    elif (( lag_min >= WARN_MIN )); then
        colour="$YEL"; label="WARNING  (lag=${lag_min}m >= ${WARN_MIN}m)"; (( worst < 1 )) && worst=1
    else
        colour="$GRN"; label="OK"
    fi

    printf "%-55s %10d  %-8s  " "${rel:0:54}" "$lag_min" "$healthy"
    echo -e "${colour}${label}${NC}"

done <<< "$RAW"

echo
case $worst in
    0) echo -e "${GRN}All SnapMirror relationships are healthy and within lag thresholds.${NC}" ;;
    1) echo -e "${YEL}WARNING: One or more relationships exceed the warning lag threshold.${NC}" ;;
    2) echo -e "${RED}CRITICAL: One or more relationships are unhealthy or exceed the critical lag threshold.${NC}" ;;
esac
exit $worst
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Git for Windows installed (download from gitforwindows.org — it is free and includes Git Bash)
- `sshpass` available — this is tricky on Windows. The easiest approach is to use WSL (Windows Subsystem for Linux) instead of Git Bash, and run `sudo apt install sshpass` inside WSL
- Network access to your destination ONTAP cluster management IP
- An ONTAP admin username and password

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sm_lag_monitor.sh` — save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | Where to find it |
|---|---|---|
| `ONTAP_HOST` | Your destination cluster management IP | NetApp System Manager |
| `ONTAP_USER` | ONTAP admin username | Your storage admin |
| `ONTAP_PASS` | ONTAP admin password | Your storage admin |
| `SM_WARN_MIN` | Minutes of lag before WARNING (default: 30) | Your DR policy |
| `SM_CRIT_MIN` | Minutes of lag before CRITICAL (default: 60) | Your DR policy |

**Step 3 — Open a terminal**

Open WSL (Ubuntu from the Start menu), or open Git Bash.

**Step 4 — Set variables and run**

```
export ONTAP_HOST=192.168.1.100
export ONTAP_USER=admin
export ONTAP_PASS=yourpassword
cd /mnt/c/Users/YourName/Desktop
bash sm_lag_monitor.sh
```

**What you should see**

A table listing every SnapMirror relationship with source path, destination path, lag in minutes, healthy flag, and a colour-coded status: green OK, yellow WARNING, red CRITICAL. A summary line at the bottom shows the overall worst state.

---

## Planned DR Failover (Bash)

Perform a controlled SnapMirror failover at the DR site: quiesce all relationships, wait for in-flight transfers to stop, break relationships to make destination volumes read-write, and print host-side mount instructions. Requires confirmation at each destructive step.

~~~bash
#!/bin/bash
# SnapMirror Planned DR Failover Script
# Usage: DEST_CLUSTER=dr-cluster DEST_SVM=svm_dr VOLUMES="vol1 vol2 vol3" \
#          ONTAP_USER=admin ONTAP_PASS=secret ./sm_dr_failover.sh

set -euo pipefail

DEST_CLUSTER="${DEST_CLUSTER:?Set DEST_CLUSTER}"
DEST_SVM="${DEST_SVM:?Set DEST_SVM}"
VOLUMES="${VOLUMES:?Set VOLUMES (space-separated list)}"
USER="${ONTAP_USER:?Set ONTAP_USER}"
PASS="${ONTAP_PASS:?Set ONTAP_PASS}"
WAIT_SECS="${SM_WAIT_SECS:-30}"  # seconds to wait for quiesce to complete

if ! command -v sshpass &>/dev/null; then
    echo "ERROR: sshpass is required." >&2; exit 3
fi

LOG_FILE="/var/log/dr_failover_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

ts() { echo "[$(date '+%Y-%m-%d %H:%M:%S')]"; }
log() { echo "$(ts) $*"; }
confirm() {
    read -rp "$1 [yes/NO]: " ans
    [[ "${ans,,}" == "yes" ]] || { log "Aborted by user."; exit 1; }
}

log "=== SnapMirror Planned DR Failover ==="
log "Destination cluster : $DEST_CLUSTER"
log "Destination SVM     : $DEST_SVM"
log "Volumes             : $VOLUMES"
log "Log file            : $LOG_FILE"

confirm "Proceed with DR failover? This will make destination volumes read-write."

ssh_cmd() {
    sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o BatchMode=no \
        "${USER}@${DEST_CLUSTER}" "$@" 2>/dev/null
}

# ------------------------------------------------------------------
# Step 1: Quiesce all relationships
# ------------------------------------------------------------------
log "Step 1: Quiescing SnapMirror relationships..."
for vol in $VOLUMES; do
    dst_path="${DEST_SVM}:${vol}"
    log "  Quiescing $dst_path"
    ssh_cmd "snapmirror quiesce -destination-path ${dst_path}" || \
        log "  WARNING: quiesce command returned non-zero for $dst_path"
done

# ------------------------------------------------------------------
# Step 2: Wait for in-flight transfers to stop
# ------------------------------------------------------------------
log "Step 2: Waiting ${WAIT_SECS}s for in-flight transfers to complete..."
sleep "$WAIT_SECS"

log "Checking transfer state..."
for vol in $VOLUMES; do
    dst_path="${DEST_SVM}:${vol}"
    state=$(ssh_cmd "snapmirror show -destination-path ${dst_path} -fields transfer-state 2>/dev/null" \
            | grep -v 'transfer-state\|entries' | awk '{print $NF}' || echo "unknown")
    log "  $dst_path transfer-state: $state"
done

confirm "All transfers appear stopped. Proceed to break relationships?"

# ------------------------------------------------------------------
# Step 3: Break relationships
# ------------------------------------------------------------------
log "Step 3: Breaking SnapMirror relationships..."
for vol in $VOLUMES; do
    dst_path="${DEST_SVM}:${vol}"
    log "  Breaking $dst_path"
    ssh_cmd "snapmirror break -destination-path ${dst_path} -force" || \
        { log "ERROR: Failed to break $dst_path — manual intervention required"; exit 2; }
    log "  $dst_path is now read-write"
done

# ------------------------------------------------------------------
# Step 4: Verify destination volumes are read-write
# ------------------------------------------------------------------
log "Step 4: Verifying destination volumes are RW..."
for vol in $VOLUMES; do
    dst_path="${DEST_SVM}:${vol}"
    type=$(ssh_cmd "volume show -vserver ${DEST_SVM} -volume ${vol} -fields type 2>/dev/null" \
           | grep -v 'vserver\|entries' | awk '{print $NF}' || echo "unknown")
    if [[ "$type" == "rw" ]]; then
        log "  PASS: $dst_path is type=rw"
    else
        log "  WARNING: $dst_path type=$type (expected rw)"
    fi
done

# ------------------------------------------------------------------
# Step 5: Host-side instructions
# ------------------------------------------------------------------
log ""
log "=== HOST-SIDE MOUNT INSTRUCTIONS ==="
log "1. On each application host, rescan storage (rescan HBA / iSCSI / NFS remount)"
log "2. For NFS: mount -t nfs ${DEST_CLUSTER_MGMT_IP}:/path/to/export /mnt/target"
log "3. For iSCSI/FC: run multipath -ll to verify new paths; mount filesystem"
log "4. Verify application can see data and start services"
log ""
log "=== IMPORTANT: After DR test, resync relationships before returning to production ==="
log "Command: snapmirror resync -destination-path \${DEST_SVM}:\${vol}"
log ""
log "Failover complete. Log saved to: $LOG_FILE"
~~~

#### How to run this script — step by step

**Before you start — what you need**
- This script performs a real DR failover — it will make your DR volumes writable and break replication. Only run this during a planned DR test or actual disaster. Get sign-off from your manager first
- WSL (Windows Subsystem for Linux) with Ubuntu installed, plus `sshpass` (`sudo apt install sshpass`)
- Network access to your destination ONTAP cluster
- ONTAP admin credentials for the destination cluster

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sm_dr_failover.sh` — save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | Where to find it |
|---|---|---|
| `DEST_CLUSTER` | DR cluster management IP | Your storage admin |
| `DEST_SVM` | Name of the DR SVM (e.g. `svm_dr`) | NetApp System Manager on DR cluster |
| `VOLUMES` | Space-separated list of volume names to fail over | Your DR runbook |
| `ONTAP_USER` | ONTAP admin username | Your storage admin |
| `ONTAP_PASS` | ONTAP admin password | Your storage admin |

**Step 3 — Open WSL**

Open the Ubuntu app from the Start menu.

**Step 4 — Run the script**

```
export DEST_CLUSTER=192.168.2.100
export DEST_SVM=svm_dr
export VOLUMES="vol1 vol2 vol3"
export ONTAP_USER=admin
export ONTAP_PASS=yourpassword
cd /mnt/c/Users/YourName/Desktop
bash sm_dr_failover.sh
```

**What you should see**

The script prompts you to confirm before each destructive step. It logs every action with a timestamp. After breaking the relationships it prints host-side mount instructions and saves a full log file to `/var/log/`. You can review the log file afterwards to document the failover.

---

## Relationship Health Report (Perl)

SSH to both source and destination clusters, collect SnapMirror relationship data, cross-reference to verify all expected relationships exist, and report any missing or broken-off relationships.

~~~perl
#!/usr/bin/perl
use strict;
use warnings;
use Net::SSH2;

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
my $SRC_CLUSTER  = $ENV{SM_SRC_HOST}  // die "Set SM_SRC_HOST\n";
my $DST_CLUSTER  = $ENV{SM_DST_HOST}  // die "Set SM_DST_HOST\n";
my $USER         = $ENV{ONTAP_USER}   // die "Set ONTAP_USER\n";
my $PASS         = $ENV{ONTAP_PASS}   // die "Set ONTAP_PASS\n";

# -------------------------------------------------------------------
# SSH helper
# -------------------------------------------------------------------
sub ssh_connect {
    my ($host) = @_;
    my $s = Net::SSH2->new();
    $s->connect($host, 22) or die "Cannot connect to $host: $!\n";
    $s->auth_password($USER, $PASS) or die "Auth failed for $host\n";
    return $s;
}

sub ssh_run {
    my ($ssh2, $cmd) = @_;
    my $ch = $ssh2->channel() or die "Channel error\n";
    $ch->exec($cmd);
    my $out = '';
    while (!$ch->eof) { $ch->read(my $buf, 4096); $out .= $buf // '' }
    $ch->close;
    return $out;
}

# -------------------------------------------------------------------
# Parse snapmirror show output from destination
# Returns: hashref  dst_path => { src, healthy, state, lag }
# -------------------------------------------------------------------
sub parse_dst_relationships {
    my ($raw) = @_;
    my %rels;
    for my $line (split /\n/, $raw) {
        next if $line =~ /^(source-path|[[:space:]]*$|\d+ entr)/;
        my ($src, $dst, $lag, $healthy, $state) = split /\s+/, $line;
        next unless defined $dst && $dst =~ /:/;
        $rels{$dst} = { src => $src // '', healthy => $healthy // 'unknown',
                        state => $state // '', lag => $lag // '' };
    }
    return %rels;
}

# -------------------------------------------------------------------
# Parse snapmirror list-destinations from source
# Returns: list of destination paths that source expects to replicate to
# -------------------------------------------------------------------
sub parse_src_destinations {
    my ($raw) = @_;
    my @expected;
    for my $line (split /\n/, $raw) {
        next if $line =~ /^(source|[[:space:]]*$|\d+ entr)/;
        my @cols = split /\s+/, $line;
        # Format: source-path  destination-path  ...
        my $dst_path = $cols[1] // '';
        push @expected, $dst_path if $dst_path =~ /:/;
    }
    return @expected;
}

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
print "Connecting to source cluster: $SRC_CLUSTER\n";
my $src_ssh = ssh_connect($SRC_CLUSTER);
my $src_raw = ssh_run($src_ssh, 'snapmirror list-destinations -fields source-path,destination-path 2>/dev/null');
$src_ssh->disconnect;

print "Connecting to destination cluster: $DST_CLUSTER\n";
my $dst_ssh = ssh_connect($DST_CLUSTER);
my $dst_raw = ssh_run($dst_ssh, 'snapmirror show -fields source-path,destination-path,lag-time,healthy,state 2>/dev/null');
$dst_ssh->disconnect;

my %dst_rels    = parse_dst_relationships($dst_raw);
my @src_expected = parse_src_destinations($src_raw);

# -------------------------------------------------------------------
# Cross-reference and report
# -------------------------------------------------------------------
my $ts = localtime;
print "\n=== SnapMirror Relationship Health Report ===\n";
print "Source      : $SRC_CLUSTER\n";
print "Destination : $DST_CLUSTER\n";
print "Time        : $ts\n";
print "-" x 80 . "\n";
printf "%-50s %-10s %-15s %s\n", "DESTINATION PATH", "HEALTHY", "STATE", "LAG";
print "-" x 80 . "\n";

my ($ok, $warn, $missing) = (0, 0, 0);

for my $dst (sort keys %dst_rels) {
    my $r = $dst_rels{$dst};
    my $flag = ($r->{healthy} ne 'true' || $r->{state} =~ /broken/) ? '*** ISSUE' : '';
    printf "%-50s %-10s %-15s %s %s\n",
        $dst, $r->{healthy}, $r->{state}, $r->{lag}, $flag;
    if ($flag) { $warn++ } else { $ok++ }
}

# Check for expected relationships missing from destination
print "\n--- Missing Relationships (expected by source but not on destination) ---\n";
for my $expected (@src_expected) {
    unless (exists $dst_rels{$expected}) {
        print "  MISSING: $expected\n";
        $missing++;
    }
}
print "  (none)\n" unless $missing;

print "\n";
printf "Summary: OK=%d  ISSUES=%d  MISSING=%d\n", $ok, $warn, $missing;
exit(($warn + $missing > 0) ? 1 : 0);
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Strawberry Perl installed on Windows (download from strawberryperl.com)
- The `Net::SSH2` Perl module (installed via cpan)
- Network access to both your source and destination ONTAP cluster management IPs
- ONTAP admin credentials (the same username/password must work on both clusters)

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sm_health_report.pl` — save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | Where to find it |
|---|---|---|
| `SM_SRC_HOST` | Source cluster management IP | NetApp System Manager |
| `SM_DST_HOST` | Destination cluster management IP | NetApp System Manager |
| `ONTAP_USER` | ONTAP admin username | Your storage admin |
| `ONTAP_PASS` | ONTAP admin password | Your storage admin |

**Step 3 — Open Command Prompt**

Press the Windows key, type `cmd`, press Enter.

**Step 4 — Install the Perl module and set variables**

```
cpan Net::SSH2
set SM_SRC_HOST=192.168.1.100
set SM_DST_HOST=192.168.2.100
set ONTAP_USER=admin
set ONTAP_PASS=yourpassword
```

**Step 5 — Run the script**

```
cd %USERPROFILE%\Desktop
perl sm_health_report.pl
```

**What you should see**

The script connects to both clusters, retrieves SnapMirror data, and prints a table of all destination relationships showing the destination path, healthy flag, state, and lag time. Any relationship with issues is flagged with `*** ISSUE`. Below the table it lists any relationships that the source expects to exist but are missing from the destination. A summary line shows OK/ISSUES/MISSING counts.

---

## Ansible SnapMirror Resync Playbook

Resync SnapMirror relationships after a DR test — verify destination volumes exist, resync each relationship, wait for healthy status with retries, and print a completion summary.

~~~yaml
---
# SnapMirror Resync Playbook
# Use after a DR test to re-establish SnapMirror protection.
# Variables: dest_cluster, dest_svm, volumes (list), ontap_username, ontap_password
#
# Example:
# ansible-playbook sm_resync.yml \
#   -e "dest_cluster=dr-cluster dest_svm=svm_dr ontap_username=admin ontap_password=secret" \
#   -e '{"volumes":["vol1","vol2","vol3"]}'

- name: SnapMirror Resync After DR Test
  hosts: localhost
  gather_facts: false
  vars:
    ontap_validate_certs: false
    resync_retries: 12
    resync_delay:   30    # seconds between health checks

  tasks:

    - name: Verify destination SVM exists
      netapp.ontap.na_ontap_rest_info:
        hostname:         "{{ dest_cluster }}"
        username:         "{{ ontap_username }}"
        password:         "{{ ontap_password }}"
        validate_certs:   "{{ ontap_validate_certs }}"
        gather_subset:
          - storage/volumes
        parameters:
          svm.name: "{{ dest_svm }}"
      register: vol_info

    - name: Assert destination volumes exist
      ansible.builtin.assert:
        that:
          - item in (vol_info.ontap_info['storage/volumes'].records | map(attribute='name') | list)
        fail_msg: "Destination volume {{ item }} not found on {{ dest_cluster }}:{{ dest_svm }}"
      loop: "{{ volumes }}"

    - name: Resync each SnapMirror relationship
      netapp.ontap.na_ontap_snapmirror:
        state:          present
        relationship_state: active
        initialize:     false
        destination_endpoint:
          cluster:      "{{ dest_cluster }}"
          path:         "{{ dest_svm }}:{{ item }}"
        hostname:       "{{ dest_cluster }}"
        username:       "{{ ontap_username }}"
        password:       "{{ ontap_password }}"
        validate_certs: "{{ ontap_validate_certs }}"
        use_rest:       always
      loop: "{{ volumes }}"
      register: resync_results

    - name: Wait for relationships to become healthy
      netapp.ontap.na_ontap_rest_info:
        hostname:       "{{ dest_cluster }}"
        username:       "{{ ontap_username }}"
        password:       "{{ ontap_password }}"
        validate_certs: "{{ ontap_validate_certs }}"
        gather_subset:
          - snapmirror/relationships
        parameters:
          destination.path: "{{ dest_svm }}:{{ item }}"
      register: sm_status
      until: >-
        sm_status.ontap_info['snapmirror/relationships'].records | length > 0 and
        sm_status.ontap_info['snapmirror/relationships'].records[0].healthy == true
      retries: "{{ resync_retries }}"
      delay:   "{{ resync_delay }}"
      loop: "{{ volumes }}"

    - name: Collect final relationship status
      ansible.builtin.set_fact:
        final_status: >-
          {{ final_status | default([]) + [{
            'volume':  item.item,
            'healthy': item.ontap_info['snapmirror/relationships'].records[0].healthy
                       | default(false),
            'lag':     item.ontap_info['snapmirror/relationships'].records[0].lag_time
                       | default('unknown')
          }] }}
      loop: "{{ sm_status.results }}"

    - name: Print completion summary
      ansible.builtin.debug:
        msg: >-
          {{ item.volume }}: healthy={{ item.healthy }}  lag={{ item.lag }}
      loop: "{{ final_status }}"

    - name: Assert all relationships are healthy
      ansible.builtin.assert:
        that: "item.healthy == true"
        fail_msg: "Relationship for {{ item.volume }} is still unhealthy after resync."
      loop: "{{ final_status }}"

    - name: Resync complete
      ansible.builtin.debug:
        msg: >-
          All {{ volumes | length }} SnapMirror relationships successfully resynced
          on {{ dest_cluster }}:{{ dest_svm }}.
~~~

#### How to run this script — step by step

**Before you start — what you need**
- WSL (Windows Subsystem for Linux) with Ubuntu installed
- Inside WSL: `sudo apt install ansible python3-pip` and then `ansible-galaxy collection install netapp.ontap`
- You should run this playbook after a DR test, once you are ready to re-establish SnapMirror protection on the destination cluster
- Network access to the destination ONTAP cluster
- ONTAP admin credentials

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sm_resync.yml` — save it to your Desktop

**Step 2 — Fill in your details**

You pass all values on the command line — no need to edit the file.

| Variable | What to put here | Where to find it |
|---|---|---|
| `dest_cluster` | DR cluster management IP | Your storage admin |
| `dest_svm` | DR SVM name | NetApp System Manager on DR cluster |
| `volumes` | List of volume names, e.g. `["vol1","vol2"]` | Your DR runbook |
| `ontap_username` | ONTAP admin username | Your storage admin |
| `ontap_password` | ONTAP admin password | Your storage admin |

**Step 3 — Open WSL**

Open the Ubuntu app from the Start menu.

**Step 4 — Run the playbook**

```
cp /mnt/c/Users/YourName/Desktop/sm_resync.yml ~/
cd ~
ansible-playbook sm_resync.yml \
  -e "dest_cluster=192.168.2.100 dest_svm=svm_dr ontap_username=admin ontap_password=yourpassword" \
  -e '{"volumes":["vol1","vol2","vol3"]}'
```

**What you should see**

Ansible checks that each destination volume exists, then triggers a resync for each SnapMirror relationship. It polls every 30 seconds (up to 12 retries = 6 minutes) waiting for each relationship to become healthy. When all relationships are healthy, it prints a summary with the lag time for each, then confirms the resync is complete.

---

## Windows: SnapMirror Relationship Status via REST API (PowerShell)

Use the ONTAP REST API on the destination cluster to retrieve all SnapMirror relationships, filter for any that are not in a healthy `snapmirrored` state, and print a formatted status report. No SSH or third-party tools required.

~~~powershell
# sm_status_rest.ps1 — SnapMirror Relationship Status via REST API (Windows PowerShell)
# Requires: PowerShell 5.1+ (pre-installed on Windows 10/11)
# Run: .\sm_status_rest.ps1

$DestCluster = "192.168.2.100"   # Your destination cluster management IP or hostname
$OntapUser   = "admin"            # ONTAP username
$OntapPass   = "yourpassword"     # ONTAP password

# Handle self-signed SSL certificates
if (-not ([System.Management.Automation.PSTypeName]'TrustAll').Type) {
    Add-Type @"
    using System.Net; using System.Security.Cryptography.X509Certificates;
    public class TrustAll : ICertificatePolicy {
        public bool CheckValidationResult(ServicePoint s, X509Certificate c, WebRequest r, int p) { return true; }
    }
"@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAll
}
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Build basic auth header
$AuthBytes  = [System.Text.Encoding]::ASCII.GetBytes("${OntapUser}:${OntapPass}")
$AuthBase64 = [Convert]::ToBase64String($AuthBytes)
$Headers    = @{ Authorization = "Basic $AuthBase64" }

$BaseUrl = "https://$DestCluster/api"

Write-Host "`n=== SnapMirror Relationship Status Report ===" -ForegroundColor Cyan
Write-Host "Cluster: $DestCluster  |  Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Host ("-" * 70)

# Fetch all SnapMirror relationships with relevant fields
try {
    $resp = Invoke-RestMethod `
        -Uri     "$BaseUrl/snapmirror/relationships?fields=source,destination,state,healthy,lag_time" `
        -Headers $Headers `
        -Method  GET `
        -ErrorAction Stop
} catch {
    Write-Error "Failed to retrieve SnapMirror relationships: $($_.Exception.Message)"
    exit 1
}

$relationships = $resp.records
if (-not $relationships -or $relationships.Count -eq 0) {
    Write-Host "No SnapMirror relationships found on this cluster."
    exit 0
}

Write-Host "Total relationships: $($relationships.Count)`n"

$issues = 0

foreach ($rel in $relationships | Sort-Object { $_.healthy }) {
    $source  = "$($rel.source.svm.name):$($rel.source.path)"
    $dest    = "$($rel.destination.svm.name):$($rel.destination.path)"
    $state   = $rel.state
    $healthy = $rel.healthy
    $lag     = $rel.lag_time

    # Convert lag_time (ISO 8601 duration like PT1H30M) to readable format
    $lagDisplay = if ($lag) { $lag } else { "N/A" }

    if ($healthy -eq $true -and $state -eq "snapmirrored") {
        Write-Host ("  [OK]     {0,-45} -> {1,-35} lag={2}" -f $source, $dest, $lagDisplay) -ForegroundColor Green
    } else {
        Write-Host ("  [ISSUE]  {0,-45} -> {1,-35} state={2}  healthy={3}  lag={4}" -f `
            $source, $dest, $state, $healthy, $lagDisplay) -ForegroundColor Red
        $issues++
    }
}

Write-Host "`n" + ("-" * 70)
if ($issues -gt 0) {
    Write-Host "$issues relationship(s) are NOT in a healthy snapmirrored state." -ForegroundColor Red
    exit 1
} else {
    Write-Host "All $($relationships.Count) SnapMirror relationships are healthy." -ForegroundColor Green
    exit 0
}
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Windows 10 or Windows 11 PC (PowerShell is already installed)
- Network access to your destination ONTAP cluster management IP
- An ONTAP admin username and password

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sm_status_rest.ps1` — save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file in Notepad and change these lines near the top:

| Variable | What to put here | Where to find it |
|---|---|---|
| `$DestCluster` | Destination cluster management IP or hostname | NetApp System Manager |
| `$OntapUser` | ONTAP admin username | Your storage admin |
| `$OntapPass` | ONTAP admin password | Your storage admin |

**Step 3 — Open PowerShell as Administrator**

Press the Windows key, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as Administrator**.

**Step 4 — Allow script execution (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
cd C:\Users\YourName\Desktop
.\sm_status_rest.ps1
```

**What you should see**

A list of every SnapMirror relationship on the destination cluster. Healthy relationships (state=snapmirrored, healthy=true) appear in green with their lag time. Any relationship that is not healthy or not in snapmirrored state appears in red with full details. The script exits with code 1 if any issues are found.

---

## Windows: SnapMirror Lag Alert via Plink (CMD)

Use plink.exe to SSH into the ONTAP cluster, run the SnapMirror show command, and highlight any relationship where the `healthy` field is false. Works from any Windows Command Prompt.

~~~batch
@echo off
REM sm_lag_alert.bat — SnapMirror Lag Alert via Plink (Windows CMD)
REM Uses plink.exe (part of PuTTY) to SSH into the ONTAP cluster.
REM Download PuTTY from: https://www.putty.org (free, trusted tool)
REM
REM FIRST-TIME SETUP: Run once to accept the host fingerprint:
REM   plink.exe -ssh admin@192.168.1.100
REM   Type 'y' when asked, then Ctrl+C to exit.

set CLUSTER_HOST=192.168.1.100
set SSH_USER=admin
set PLINK=plink.exe

echo.
echo === SnapMirror Lag and Health Alert ===
echo Cluster: %CLUSTER_HOST%
echo Time: %date% %time%
echo.

REM --- Fetch SnapMirror relationships ---
echo --- All SnapMirror Relationships ---
%PLINK% -ssh -l %SSH_USER% -batch %CLUSTER_HOST% "snapmirror show -fields source-path,destination-path,mirror-state,lag-time,healthy"

if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not connect to %CLUSTER_HOST%. Check hostname, username, and that plink.exe is in PATH.
    goto :end
)

echo.

REM --- Highlight unhealthy relationships ---
echo --- UNHEALTHY Relationships (healthy = false) ---
%PLINK% -ssh -l %SSH_USER% -batch %CLUSTER_HOST% "snapmirror show -fields source-path,destination-path,mirror-state,lag-time,healthy" | findstr /I "false"

if %ERRORLEVEL% equ 1 (
    echo All SnapMirror relationships are healthy.
) else if %ERRORLEVEL% neq 0 (
    echo ERROR: Could not retrieve SnapMirror data.
)

echo.
echo === Alert check complete ===

:end
~~~

#### How to run this script — step by step

**Before you start — what you need**
- PuTTY installed (download from putty.org — it is free). Make sure `plink.exe` is installed and accessible from Command Prompt
- Network access to your ONTAP cluster management IP
- An ONTAP admin username and password

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sm_lag_alert.bat` — save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file in Notepad and change these lines near the top:

| Variable | What to put here | Where to find it |
|---|---|---|
| `CLUSTER_HOST` | Your cluster management IP or hostname | NetApp System Manager |
| `SSH_USER` | ONTAP SSH username (usually `admin`) | Your storage admin |

**Step 3 — First-time host key acceptance**

Open Command Prompt and run:
```
plink.exe -ssh admin@192.168.1.100
```
Type `y` when prompted to trust the host key, then press Ctrl+C.

**Step 4 — Add password to plink commands (optional)**

For unattended use, add `-pw yourpassword` to each plink line in the script, right after `-batch`.

**Step 5 — Run the script**

Double-click `sm_lag_alert.bat` on your Desktop, or run from Command Prompt:
```
cd %USERPROFILE%\Desktop
sm_lag_alert.bat
```

**What you should see**

First, the script prints all SnapMirror relationships with their source/destination paths, mirror state, lag time, and healthy flag. Then it prints a second section showing only the relationships where healthy is `false`. If all relationships are healthy, it prints "All SnapMirror relationships are healthy." instead.
