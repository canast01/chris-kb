# Scripts

> Part of the [Dell PowerPath](../) reference.

---

## Path Health Check

Runs `powermt display dev=all`, counts total devices, dead paths, and devices with fewer paths than the expected minimum. Prints a summary table of each device with its path counts. Exits non-zero if any dead paths are found. Suitable for cron or a monitoring agent.

~~~bash
#!/bin/bash
# powerpath_health_check.sh — PowerPath path health check
# Usage: EXPECTED_PATHS=4 ./powerpath_health_check.sh

set -euo pipefail

EXPECTED_PATHS="${EXPECTED_PATHS:-4}"
TOTAL_DEVICES=0
DEAD_PATH_DEVICES=0
LOW_PATH_DEVICES=0
OVERALL_DEAD=0

# Capture powermt output
POWERMT_OUT=$(powermt display dev=all 2>&1)
if [[ $? -ne 0 ]]; then
  echo "ERROR: powermt display dev=all failed." >&2
  exit 1
fi

echo ""
echo "========================================"
echo "  PowerPath Path Health Check"
echo "  Expected paths per device : $EXPECTED_PATHS"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""
printf "%-20s  %12s  %10s  %10s  %s\n" \
  "PSEUDO-DEV" "TOTAL-PATHS" "DEAD-PATHS" "ALIVE" "STATUS"
printf "%s\n" "------------------------------------------------------------------------"

# Parse powermt output:
# Pseudo name=emcpowera  dev=sdb,sdc  ... 4 paths, 0 dead
# We detect lines like: Pseudo name=<dev> and "X paths, Y dead"
current_dev=""
while IFS= read -r line; do
  # Match device header line
  if [[ "$line" =~ ^Pseudo\ name=([a-zA-Z0-9_/-]+) ]]; then
    current_dev="${BASH_REMATCH[1]}"
    TOTAL_DEVICES=$((TOTAL_DEVICES + 1))
    continue
  fi

  # Match path count summary line, e.g. "     4 paths, 0 dead"
  if [[ -n "$current_dev" && "$line" =~ ([0-9]+)\ paths,\ ([0-9]+)\ dead ]]; then
    total="${BASH_REMATCH[1]}"
    dead="${BASH_REMATCH[2]}"
    alive=$((total - dead))
    OVERALL_DEAD=$((OVERALL_DEAD + dead))

    status="OK"
    if [[ "$dead" -gt 0 ]]; then
      status="DEAD PATHS"
      DEAD_PATH_DEVICES=$((DEAD_PATH_DEVICES + 1))
    elif [[ "$total" -lt "$EXPECTED_PATHS" ]]; then
      status="LOW PATHS"
      LOW_PATH_DEVICES=$((LOW_PATH_DEVICES + 1))
    fi

    printf "%-20s  %12s  %10s  %10s  %s\n" \
      "$current_dev" "$total" "$dead" "$alive" "$status"
    current_dev=""
  fi
done <<< "$POWERMT_OUT"

echo ""
echo "========================================"
echo "  SUMMARY"
echo "  Total devices    : $TOTAL_DEVICES"
echo "  Devices w/ dead  : $DEAD_PATH_DEVICES"
echo "  Devices low path : $LOW_PATH_DEVICES"
echo "  Total dead paths : $OVERALL_DEAD"
echo "========================================"

if [[ "$OVERALL_DEAD" -gt 0 ]]; then
  echo "STATUS: DEGRADED — Dead paths found. Run 'powermt restore' after fixing the underlying issue."
  exit 1
elif [[ "$LOW_PATH_DEVICES" -gt 0 ]]; then
  echo "STATUS: WARNING — Some devices have fewer than $EXPECTED_PATHS paths."
  exit 1
else
  echo "STATUS: OK — All paths healthy."
  exit 0
fi
~~~

---

## Path Count Validator

Parses `powermt display dev=all` output and validates that every pseudo device has exactly the expected number of paths. Prints PASS/FAIL per device and a final summary. Exits 0 if all pass, 1 if any fail.

~~~perl
#!/usr/bin/env perl
# powerpath_path_validator.pl — Validate path counts for all PowerPath pseudo devices
# Usage: EXPECTED_PATHS=4 ./powerpath_path_validator.pl

use strict;
use warnings;

my $expected = $ENV{EXPECTED_PATHS} // 4;

# Run powermt display dev=all
my @output = qx{powermt display dev=all 2>&1};
if ($? != 0) {
    die "ERROR: powermt display dev=all failed.\n@output\n";
}

my ($current_dev, %results);

for my $line (@output) {
    chomp $line;

    # Match pseudo device header: "Pseudo name=emcpowera"
    if ($line =~ /^Pseudo\s+name=(\S+)/) {
        $current_dev = $1;
        next;
    }

    # Match path count line: "     4 paths, 0 dead"
    if (defined $current_dev && $line =~ /(\d+)\s+paths?,\s*(\d+)\s+dead/) {
        my ($total, $dead) = ($1, $2);
        $results{$current_dev} = {
            total    => $total,
            dead     => $dead,
            alive    => $total - $dead,
        };
        $current_dev = undef;
    }
}

if (!%results) {
    print "ERROR: No pseudo devices parsed from powermt output.\n";
    exit 1;
}

my ($pass, $fail) = (0, 0);
printf "%-20s  %12s  %10s  %10s  %s\n",
    'DEVICE', 'TOTAL PATHS', 'DEAD', 'ALIVE', 'RESULT';
printf "%s\n", '-' x 68;

for my $dev (sort keys %results) {
    my $r = $results{$dev};
    my $result;
    if ($r->{dead} > 0) {
        $result = "FAIL (dead paths)";
        $fail++;
    } elsif ($r->{total} != $expected) {
        $result = sprintf "FAIL (got %d, want %d)", $r->{total}, $expected;
        $fail++;
    } else {
        $result = "PASS";
        $pass++;
    }
    printf "%-20s  %12d  %10d  %10d  %s\n",
        $dev, $r->{total}, $r->{dead}, $r->{alive}, $result;
}

printf "%s\n", '-' x 68;
printf "Total: %d devices — %d PASS, %d FAIL\n", $pass + $fail, $pass, $fail;

exit($fail > 0 ? 1 : 0);
~~~

---

## Policy Audit

Runs `powermt display options` and `powermt display dev=all`, checks that all pseudo devices are using the CLAROpt (`co`) load balancing policy, and reports any exceptions. If the `--fix` flag is passed, automatically applies CLAROpt to all devices and persists the change with `powermt save`.

~~~bash
#!/bin/bash
# powerpath_policy_audit.sh — Audit and optionally fix PowerPath load balancing policy
# Usage: ./powerpath_policy_audit.sh [--fix]
#
# Without --fix: report devices NOT using CLAROpt and exit non-zero if any found.
# With    --fix: apply CLAROpt to all devices and run powermt save.

set -euo pipefail

FIX_MODE=0
if [[ "${1:-}" == "--fix" ]]; then
  FIX_MODE=1
fi

EXPECTED_POLICY="co"   # CLAROpt abbreviation used in powermt output
WRONG_POLICY_DEVICES=0

echo ""
echo "========================================"
echo "  PowerPath Policy Audit"
echo "  Expected policy : CLAROpt (co)"
echo "  Fix mode        : $([ "$FIX_MODE" -eq 1 ] && echo YES || echo NO)"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Show current global options
echo ""
echo "--- Current Global Options ---"
powermt display options
echo ""

# Parse powermt display dev=all for policy per device
POWERMT_OUT=$(powermt display dev=all 2>&1)
current_dev=""
current_policy=""

echo "--- Policy per Device ---"
printf "%-20s  %-15s  %s\n" "DEVICE" "POLICY" "STATUS"
printf "%s\n" "-------------------------------------------"

while IFS= read -r line; do
  if [[ "$line" =~ ^Pseudo\ name=([a-zA-Z0-9_/-]+) ]]; then
    current_dev="${BASH_REMATCH[1]}"
    current_policy=""
    continue
  fi

  # Policy line looks like: "Logical device ID=xxx  Policy=CLAROpt(co)  ..."
  if [[ -n "$current_dev" && "$line" =~ Policy=([A-Za-z]+)\(([a-z]+)\) ]]; then
    policy_name="${BASH_REMATCH[1]}"
    policy_code="${BASH_REMATCH[2]}"

    if [[ "$policy_code" == "$EXPECTED_POLICY" ]]; then
      printf "%-20s  %-15s  PASS\n" "$current_dev" "$policy_name"
    else
      printf "%-20s  %-15s  FAIL — not CLAROpt\n" "$current_dev" "$policy_name"
      WRONG_POLICY_DEVICES=$((WRONG_POLICY_DEVICES + 1))
    fi
    current_dev=""
  fi
done <<< "$POWERMT_OUT"

echo ""
echo "  Devices with non-CLAROpt policy: $WRONG_POLICY_DEVICES"
echo ""

if [[ "$FIX_MODE" -eq 1 && "$WRONG_POLICY_DEVICES" -gt 0 ]]; then
  echo "--- Applying CLAROpt to all devices ---"
  powermt set policy=CLAROpt class=all
  powermt save
  echo "  CLAROpt applied and configuration saved."
  exit 0
fi

if [[ "$WRONG_POLICY_DEVICES" -gt 0 ]]; then
  echo "STATUS: FAIL — $WRONG_POLICY_DEVICES device(s) not using CLAROpt."
  echo "  Run with --fix to correct automatically."
  exit 1
else
  echo "STATUS: PASS — All devices using CLAROpt policy."
  exit 0
fi
~~~
