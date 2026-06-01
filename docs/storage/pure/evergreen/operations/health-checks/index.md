# Evergreen — Health Checks


<div class="kb-summary">
Health Checks reference covering Quick Health Check (5 minutes), Full Health Check (20 minutes), Health Check Checklist Template, Evergreen Subscription Checks, Common Issues During Health Checks.
</div>

```text
Evergreen Health Check — Daily Sequence
  Pure1 portal ──► All arrays green?
          │
          ▼
  purealert list ──► No error/warning alerts?
          │
          ▼
  puredrive list ──► All drives healthy?
          │
          ▼
  purearray list --controller ──► Both controllers ok?
          │
          ▼
  purearray phonehome list ──► Phone-home active?
          │
          ▼
  Pure1 → Subscription dashboard ──► Capacity within entitlement?
          │
          ▼
          PASS
```

> Part of the [Evergreen Operations](../index.md) reference.

---

Regular health checks confirm that FlashArray is operating within expected parameters and that the Evergreen support relationship (Phone Home, entitlement, replacement readiness) is functioning.

## Quick Health Check (5 minutes)

Run from Pure1 UI or CLI. No impact to production.

### Via Pure1 UI

```text
Pure1 → Arrays → select array → Overview tab

Check:
  ✓ Array status: Green (no active alerts)
  ✓ Both controllers: Online
  ✓ All drives: Healthy
  ✓ Phone Home: Last contact < 24 hours ago
  ✓ Capacity: < 70% used
```

### Via CLI

```bash
ssh pureuser@<flasharray-ip>

# 1. Overall hardware health
purehw list | grep -v Healthy
# Expected: no output (all components healthy)

# 2. Active alerts
purealert list --flagged
# Expected: no output (no open alerts)

# 3. Controller status
purehw list --type ct
# Expected: CT0 and CT1 both Healthy

# 4. Array capacity
purearray list --space
# Check: capacity_utilization < 0.70

# 5. Phone Home status
puresupport list
# Check: phonehome_enabled = true, last_contact < 24h
```

## Full Health Check (20 minutes)

Run monthly and before/after Purity upgrades or hardware changes.

### 1. Hardware Inventory

```bash
# All hardware components with status
purehw list

# Non-healthy components only
purehw list | grep -iv "^Name\|healthy\|^---\|^$"
# Pass: no output

# Drive-specific detail
purehw list --type drive | awk 'NR<=1 || $3 != "Healthy"'
```

### 2. Capacity Deep-Dive

```bash
# Array-level space breakdown
purearray list --space

# Top 10 volumes by space consumption
purevol list --space | sort -k5 -rh | head -10

# Snapshot space — top consumers
puresnapshot list --space | sort -k5 -rh | head -10

# Check data reduction ratio (should be > 2:1 for most workloads)
purearray list --space | awk 'NR==2 {print "Data reduction ratio: " $7}'
```

### 3. Performance Baseline

```bash
# Current array IOPS, bandwidth, latency
purearray list --performance

# Per-volume performance — identify any outliers
purevol list --performance | sort -k4 -rn | head -10   # by read IOPS
purevol list --performance | sort -k6 -rn | head -10   # by read latency (µs)

# Port utilisation
pureport list --performance
# Flag: any port at > 70% bandwidth sustained
```

### 4. Replication Health

```bash
# ActiveCluster / async replication status
purepgroup list --schedule
purepgroup list --transfer

# Check replication lag
purepgroup list --transfer | awk 'NR>1 {print $1, $5, $6}'
# Column 5/6 = bytes pending / time lag

# Protection group snapshots
purepgroup list --snap | tail -5
```

### 5. Network and Connectivity

```bash
# Port errors — check for any non-zero error counters
pureport list --performance | awk 'NR==1 || $NF != "0"'

# FC path status (if applicable)
purehost list --performance | head -20

# Phone Home and log forwarding
puresupport list
puresupport set --list   # show current support configuration
```

### 6. Purity Version Check

```bash
# Current Purity version
purearray list | grep -i version

# Check for available upgrade (via Pure1 UI)
# Pure1 → Arrays → select array → Settings → Software
```

Compare against [Pure Storage EOL/support matrix](https://support.purestorage.com) to confirm the installed version is within support window.

### 7. Host Connectivity

```bash
# All registered hosts and their volumes
purehost list
purevol list --host

# Verify each production host has expected number of paths
purehostgroup list --connect
# Expect: each host group connected to expected volume groups

# Check for hosts with only 1 path (multipath misconfiguration risk)
purehost list --performance | awk 'NR>1 && $2 < 2 {print $1, "WARNING: only " $2 " paths"}'
```

## Health Check Checklist Template

| Check | Result | Notes |
|---|---|---|
| Both controllers Online | | |
| All drives Healthy | | |
| 0 flagged alerts | | |
| Phone Home last contact < 24h | | |
| Capacity < 70% used | | |
| Data reduction ratio > 2:1 | | |
| Array latency < 1ms (read + write) | | |
| Replication lag within RPO target | | |
| No port errors | | |
| All hosts have ≥ 2 paths | | |
| Purity version within support | | |

## Evergreen Subscription Checks

Validate annually and before a contract renewal:

```bash
# Confirm Phone Home is enabled and connected
purearray list --csv | grep phone_home

# Check entitlement and support expiry via Pure1
# Pure1 → Administration → Subscriptions
# Verify:
#   - Subscription tier (Forever / Flex)
#   - Contract end date
#   - Capacity entitlement matches deployed capacity
#   - Controller refresh date (Ever Modern — typically year 3 of subscription)
```

## Common Issues During Health Checks

| Finding | Action |
|---|---|
| Drive not Healthy | Open Pure support case — drive replacement covered by Evergreen; no action needed before Pure ships replacement |
| Controller Offline | Open Priority 1 support case by phone immediately |
| Phone Home last contact > 24h | Check firewall rules for TCP 443 outbound to `pure1.purestorage.com`; check proxy config |
| Capacity > 80% | Review and eradicate stale snapshots; plan Evergreen capacity expansion |
| Replication lag > RPO | Investigate network bandwidth between sites; check source array load |
| Host with 1 path | Investigate multipathing on the host; rescan HBA; check zoning |
