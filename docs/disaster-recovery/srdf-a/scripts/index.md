# Scripts

> Part of the [SRDF/A](../) reference.

---

## SRDF/A Cycle Time Monitor (Bash)

Use SYMCLI to query SRDF/A cycle time and delta set processing time for a given RDF group, compare against configurable thresholds, and print the last 10 samples for trend visibility.

~~~bash
#!/usr/bin/env bash
# srdf-cycle-time-monitor.sh
# Usage: SID=<symm_id> RDF_GROUP=<group_num> ./srdf-cycle-time-monitor.sh
# Optional: WARN_THRESHOLD=30 CRIT_THRESHOLD=60

set -euo pipefail

SID="${SID:?SID (Symmetrix serial) is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
WARN_THRESHOLD="${WARN_THRESHOLD:-30}"
CRIT_THRESHOLD="${CRIT_THRESHOLD:-60}"
SAMPLES=10

echo ""
echo "=== SRDF/A Cycle Time Monitor ==="
echo "SID         : ${SID}"
echo "RDF Group   : ${RDF_GROUP}"
echo "Warn > ${WARN_THRESHOLD}s  |  Crit > ${CRIT_THRESHOLD}s"
echo "Time        : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Collect current cycle time data
RAW_OUTPUT=$(symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" queryall -detail 2>&1) || {
    echo "ERROR: symrdf command failed:"
    echo "${RAW_OUTPUT}"
    exit 2
}

# Parse cycle time (seconds) and delta set processing time
CYCLE_TIME=$(echo "${RAW_OUTPUT}" | grep -i "Cycle Time" | awk '{print $NF}' | head -1)
DELTA_PROC=$(echo "${RAW_OUTPUT}" | grep -i "Delta Set Processing" | awk '{print $NF}' | head -1)

CYCLE_TIME=${CYCLE_TIME:-0}
DELTA_PROC=${DELTA_PROC:-0}

echo "Current Cycle Time             : ${CYCLE_TIME}s"
echo "Current Delta Set Proc Time    : ${DELTA_PROC}s"
echo ""

# Determine status
EXIT_CODE=0
STATUS="OK"

if (( $(echo "${CYCLE_TIME} > ${CRIT_THRESHOLD}" | bc -l) )); then
    STATUS="CRITICAL"
    EXIT_CODE=2
elif (( $(echo "${CYCLE_TIME} > ${WARN_THRESHOLD}" | bc -l) )); then
    STATUS="WARNING"
    EXIT_CODE=1
fi

echo "Status: ${STATUS}"
echo ""

# Collect trend: run symrdf query multiple times (for cron-driven trend use a file cache)
TREND_FILE="/tmp/srdf_cycle_trend_${SID}_${RDF_GROUP}.log"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

# Append current sample
echo "${TIMESTAMP} cycle=${CYCLE_TIME}s delta=${DELTA_PROC}s status=${STATUS}" >> "${TREND_FILE}"

# Print last N samples
echo "Last ${SAMPLES} samples (from ${TREND_FILE}):"
echo "---------------------------------------------------"
if [[ -f "${TREND_FILE}" ]]; then
    tail -n "${SAMPLES}" "${TREND_FILE}"
else
    echo "(no history yet)"
fi

echo ""
exit ${EXIT_CODE}
~~~

---

## SRDF State Checker (Perl)

Use SYMCLI to enumerate all device pairs in an SRDF group, flag any pair not in a Synchronized or Consistent state, and exit with a monitoring-compatible return code.

~~~perl
#!/usr/bin/env perl
# srdf-state-checker.pl
# Usage: perl srdf-state-checker.pl --sid <SID> --rdfg <RDF_GROUP>
# Exit codes: 0=OK, 1=WARN (non-sync devices), 2=CRIT (failed/split/suspended)

use strict;
use warnings;
use Getopt::Long;

my ($sid, $rdfg);
GetOptions(
    "sid=s"  => \$sid,
    "rdfg=s" => \$rdfg,
) or die "Usage: $0 --sid <SID> --rdfg <RDF_GROUP>\n";

die "ERROR: --sid is required\n"  unless defined $sid;
die "ERROR: --rdfg is required\n" unless defined $rdfg;

my %CRIT_STATES = map { $_ => 1 } (
    'Suspended', 'Split', 'Failed Over', 'Not Ready'
);
my %WARN_STATES = map { $_ => 1 } (
    'Transmit Idle', 'Syncing', 'Partitioned'
);

print "\n=== SRDF State Checker ===\n";
print "SID      : $sid\n";
print "RDF Group: $rdfg\n";
print "Time     : " . localtime() . "\n\n";

# Run symrdf list
my $cmd    = "symrdf list -sid $sid -rdfg $rdfg";
my $output = `$cmd 2>&1`;
if ($? != 0) {
    print "ERROR: symrdf command failed:\n$output\n";
    exit 2;
}

my %state_counts;
my @problem_devices;
my @all_rows;

# Parse output: look for lines with device pairs (non-header, non-blank)
for my $line (split /\n/, $output) {
    next if $line =~ /^\s*$/;
    next if $line =~ /^-+/;
    next if $line =~ /^\s*(Sym|RDF|Dev|Local|Remote|Source|Target)/i;

    # Typical symrdf list columns: local_dev remote_dev rdf_state pair_state ...
    # Actual column positions vary by SYMCLI version; parse conservatively.
    my @cols = split(/\s+/, $line);
    next unless @cols >= 4;

    my $local_dev  = $cols[0] // '';
    my $remote_dev = $cols[1] // '';
    # State usually appears around column 4 or 5
    my $state = $cols[4] // $cols[3] // '';

    next unless $local_dev =~ /^[0-9A-Fa-f]{4}$/;  # looks like a device ID

    $state_counts{$state}++;
    push @all_rows, { local => $local_dev, remote => $remote_dev, state => $state };

    if (exists $CRIT_STATES{$state} || exists $WARN_STATES{$state}) {
        push @problem_devices, { local => $local_dev, remote => $remote_dev, state => $state };
    }
}

# Print summary table
print "State Summary:\n";
print sprintf("  %-25s %s\n", "State", "Count");
print "  " . "-" x 35 . "\n";
for my $s (sort keys %state_counts) {
    my $flag = (exists $CRIT_STATES{$s}) ? "  <-- CRITICAL" :
               (exists $WARN_STATES{$s}) ? "  <-- WARN"     : "";
    printf "  %-25s %d%s\n", $s, $state_counts{$s}, $flag;
}

# Print problem devices
if (@problem_devices) {
    print "\nNon-Synchronized Devices:\n";
    print sprintf("  %-12s %-12s %s\n", "Local Dev", "Remote Dev", "State");
    print "  " . "-" x 40 . "\n";
    for my $d (@problem_devices) {
        printf "  %-12s %-12s %s\n", $d->{local}, $d->{remote}, $d->{state};
    }
}

# Determine exit code
my $crit_count = grep { exists $CRIT_STATES{$_->{state}} } @problem_devices;
my $warn_count = grep { exists $WARN_STATES{$_->{state}} } @problem_devices;

print "\n";
if ($crit_count > 0) {
    printf "RESULT: CRITICAL — %d device(s) in critical state.\n", $crit_count;
    exit 2;
} elsif ($warn_count > 0) {
    printf "RESULT: WARNING — %d device(s) in non-optimal state.\n", $warn_count;
    exit 1;
} else {
    printf "RESULT: OK — All %d device(s) synchronized.\n", scalar @all_rows;
    exit 0;
}
~~~

---

## SRDF Planned Failover (Bash)

Perform a planned SRDF failover — compatible with both SRDF/A and SRDF/S. Validates current state, suspends the consistency group, splits devices, and confirms R2 accessibility. Includes dry-run mode.

~~~bash
#!/usr/bin/env bash
# srdf-planned-failover.sh
# Usage: SID=<sid> RDF_GROUP=<rdfg> CG_NAME=<cg> [MODE=sym|cg] [--dry-run]
#
# MODE=sym : operate on all devices in the RDF group via symrdf
# MODE=cg  : operate on a consistency group via symcg + symrdf

set -euo pipefail

SID="${SID:?SID is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
CG_NAME="${CG_NAME:?CG_NAME is required}"
MODE="${MODE:-cg}"
DRY_RUN=false
LOGFILE="/var/log/srdf-failover-$(date +%Y%m%d-%H%M%S).log"

for arg in "$@"; do
    [[ "$arg" == "--dry-run" ]] && DRY_RUN=true
done

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

run_cmd() {
    log "CMD: $*"
    if ! ${DRY_RUN}; then
        "$@" 2>&1 | tee -a "${LOGFILE}"
    else
        log "[DRY-RUN] Would run: $*"
    fi
}

log "=== SRDF Planned Failover ==="
log "SID=${SID}  RDFG=${RDF_GROUP}  CG=${CG_NAME}  MODE=${MODE}"
${DRY_RUN} && log "*** DRY-RUN MODE — no changes will be made ***"

# --- Step 1: Verify current state ---
log "Step 1: Verifying current SRDF state..."
CURRENT_STATE=$(symrdf query -sid "${SID}" -rdfg "${RDF_GROUP}" 2>&1 | \
    grep -E "Synchronized|Consistent" | head -1 || true)

if [[ -z "${CURRENT_STATE}" ]]; then
    log "ERROR: SRDF group does not appear to be in Synchronized or Consistent state."
    log "       Verify with: symrdf query -sid ${SID} -rdfg ${RDF_GROUP}"
    log "       Do NOT proceed with failover until state is confirmed."
    exit 1
fi
log "State confirmed: ${CURRENT_STATE}"

# --- Step 2: Suspend CG / RDF group ---
log "Step 2: Suspending SRDF relationships..."
if [[ "${MODE}" == "cg" ]]; then
    run_cmd symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" -cg "${CG_NAME}" suspend -noprompt
else
    run_cmd symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" suspend -noprompt
fi

# --- Step 3: Wait for suspend confirmation ---
log "Step 3: Waiting for Suspended state..."
MAX_WAIT=120
ELAPSED=0
while [[ $ELAPSED -lt $MAX_WAIT ]]; do
    if ${DRY_RUN}; then
        log "[DRY-RUN] Skipping state wait."
        break
    fi
    SUSPEND_CHECK=$(symrdf query -sid "${SID}" -rdfg "${RDF_GROUP}" 2>&1 | \
        grep -c "Suspended" || true)
    if [[ "${SUSPEND_CHECK}" -gt 0 ]]; then
        log "Suspended state confirmed."
        break
    fi
    log "Waiting for Suspended... (${ELAPSED}s elapsed)"
    sleep 10
    ELAPSED=$((ELAPSED + 10))
done

if [[ $ELAPSED -ge $MAX_WAIT ]] && ! ${DRY_RUN}; then
    log "ERROR: Timed out waiting for Suspended state."
    exit 1
fi

# --- Step 4: Split ---
log "Step 4: Splitting SRDF group..."
if [[ "${MODE}" == "cg" ]]; then
    run_cmd symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" -cg "${CG_NAME}" split -noprompt
else
    run_cmd symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" split -noprompt
fi

# --- Step 5: Verify R2 accessibility ---
log "Step 5: Verifying R2 device states..."
if ! ${DRY_RUN}; then
    R2_CHECK=$(symrdf query -sid "${SID}" -rdfg "${RDF_GROUP}" 2>&1 | grep -E "Write Disabled|R/W" | head -5)
    log "R2 device states:"
    echo "${R2_CHECK}" | while IFS= read -r line; do log "  ${line}"; done
fi

# --- Step 6: Instructions for host team ---
log ""
log "=== NEXT STEPS FOR HOST TEAM ==="
log "  1. Present / mount the R2 LUNs on the DR hosts."
log "     (LUNs should now be in Write Disabled or R/W state depending on SRDF mode.)"
log "  2. Run fsck / volume group activation as required."
log "  3. Start application services in the DR site."
log "  4. Validate application connectivity."
log "  5. When returning to production, run srdf-resync-after-dr-test.sh."
log ""
log "Failover script complete. Log: ${LOGFILE}"
~~~

---

## SRDF Resync After DR Test (Bash)

Re-establish and resynchronize SRDF relationships back to production after a DR test, once the host team confirms they have unmounted R2 copies.

~~~bash
#!/usr/bin/env bash
# srdf-resync-after-dr-test.sh
# Usage: SID=<sid> RDF_GROUP=<rdfg> CG_NAME=<cg> ./srdf-resync-after-dr-test.sh
#
# Run ONLY after DR hosts have confirmed they have stopped I/O and unmounted R2 volumes.

set -euo pipefail

SID="${SID:?SID is required}"
RDF_GROUP="${RDF_GROUP:?RDF_GROUP is required}"
CG_NAME="${CG_NAME:?CG_NAME is required}"
MODE="${MODE:-cg}"
LOGFILE="/var/log/srdf-resync-$(date +%Y%m%d-%H%M%S).log"
SYNC_POLL_INTERVAL=30
SYNC_TIMEOUT=3600

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

run_cmd() {
    log "CMD: $*"
    "$@" 2>&1 | tee -a "${LOGFILE}"
}

log "=== SRDF Resync After DR Test ==="
log "SID=${SID}  RDFG=${RDF_GROUP}  CG=${CG_NAME}  MODE=${MODE}"

# --- Step 1: Confirm host acknowledgement ---
log "Step 1: Verifying preconditions..."
echo ""
echo "IMPORTANT: This script will re-establish SRDF replication."
echo "           R2 volumes will become READ-ONLY / Write Disabled."
echo ""
read -r -p "Confirm DR hosts have stopped I/O and unmounted R2 LUNs? [yes/no]: " CONFIRM
if [[ "${CONFIRM}" != "yes" ]]; then
    log "Aborted by operator. Please ensure DR hosts are off R2 volumes before resyncing."
    exit 1
fi

# --- Step 2: Establish SRDF relationships ---
log "Step 2: Establishing SRDF relationships (R1->R2 direction)..."
if [[ "${MODE}" == "cg" ]]; then
    run_cmd symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" -cg "${CG_NAME}" establish -noprompt
else
    run_cmd symrdf -sid "${SID}" -rdfg "${RDF_GROUP}" establish -noprompt
fi

log "Establish command submitted. Starting sync progress monitor..."

# --- Step 3: Wait for sync to complete ---
ELAPSED=0
while [[ $ELAPSED -lt $SYNC_TIMEOUT ]]; do
    SYNC_STATUS=$(symrdf query -sid "${SID}" -rdfg "${RDF_GROUP}" 2>&1)

    SYNC_COUNT=$(echo "${SYNC_STATUS}" | grep -c "Synchronized" || true)
    SYNCING_COUNT=$(echo "${SYNC_STATUS}" | grep -c "Syncing" || true)
    TOTAL=$(echo "${SYNC_STATUS}" | grep -cE "^[0-9A-Fa-f]{4}" || true)

    log "Progress: ${SYNC_COUNT}/${TOTAL} Synchronized, ${SYNCING_COUNT} still Syncing..."

    if [[ "${SYNCING_COUNT}" -eq 0 ]] && [[ "${SYNC_COUNT}" -gt 0 ]]; then
        log "All devices appear Synchronized."
        break
    fi

    sleep "${SYNC_POLL_INTERVAL}"
    ELAPSED=$((ELAPSED + SYNC_POLL_INTERVAL))
done

if [[ $ELAPSED -ge $SYNC_TIMEOUT ]]; then
    log "WARNING: Sync timed out after ${SYNC_TIMEOUT}s. Check manually with:"
    log "  symrdf query -sid ${SID} -rdfg ${RDF_GROUP}"
    exit 1
fi

# --- Step 4: Final state verification ---
log "Step 4: Final state verification..."
FINAL_STATE=$(symrdf query -sid "${SID}" -rdfg "${RDF_GROUP}" 2>&1 | \
    grep -E "Synchronized|Consistent" | wc -l || true)

if [[ "${FINAL_STATE}" -eq 0 ]]; then
    log "WARNING: Final verification failed — no Synchronized devices found."
    log "Review output of: symrdf query -sid ${SID} -rdfg ${RDF_GROUP}"
    exit 1
fi

log "Step 4: Verified. ${FINAL_STATE} device pair(s) confirmed Synchronized."

log ""
log "=== RESYNC COMPLETE ==="
log "Production SRDF replication is restored."
log "Log: ${LOGFILE}"
~~~
