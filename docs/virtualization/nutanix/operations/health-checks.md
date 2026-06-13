---
tags:
  - nutanix
  - operations
  - health-checks
  - ncc
search:
  boost: 1.5
---
# Nutanix — Health Checks

<div class="kb-summary">
Daily and weekly Nutanix cluster health check routine — NCC automated tests, cluster status verification, storage capacity review, CVM health, and alert triage. Includes the "Run This Routine" command sequence.

*Applies to: AOS 6.x · AHV*
</div>

---

## Before you begin

- **Access:** CVM SSH (nutanix user) or Prism Element admin
- **Duration:** 5–10 minutes for daily checks; 20–30 minutes including NCC full run
- **Frequency:** Daily for critical clusters; weekly NCC for dev/test

---

## Run This Routine

Run this sequence in order. Each step validates the output before proceeding.

### 1. Cluster Status

```bash
ssh nutanix@<any-cvm-ip>
cluster status | head -40
```

**Expected output:** All services listed as `UP`. If any service shows `DOWN`, investigate that service before continuing.

```bash
# Check all CVMs are reachable and services are running
allssh "genesis status | head -5"
```

**Expected:** Each CVM returns `Genesis is running.`

### 2. NCC Quick Check (Critical Tests Only)

```bash
# Fast — runs only critical checks (~3 min)
ncc --health_checks run_all --include_category=critical 2>&1 | tail -30
```

**Expected:** `PASS` for all critical checks. Any `FAIL` must be investigated immediately.

```bash
# Full NCC run (all 400+ checks) — run weekly or before maintenance
ncc --health_checks run_all 2>&1 | tee /tmp/ncc-$(date +%Y%m%d).txt

# Summary view
ncc --health_checks run_all 2>&1 | grep -E "FAIL|WARN|ERROR" | grep -v "^#"
```

### 3. Cluster Resilience

```bash
# Verify cluster can tolerate a node failure
ncli cluster get-domain-fault-tolerance-status type=node
```

**Expected:** `CAN_TOLERATE_FAILURE_COUNT` ≥ 1 (RF2) or ≥ 2 (RF3).

If `CAN_TOLERATE_FAILURE_COUNT=0`, the cluster cannot tolerate any additional failure — investigate immediately (node down, disk missing, degraded objects).

### 4. Storage Capacity

```bash
# Cluster-level storage summary
ncli cluster info | grep -i "storage\|capacity\|used"

# Per-container usage
ncli ctr list | grep -E "name|usage|capacity"

# Detailed storage with efficiency metrics
ncli cluster get-usage-stats
```

**Expected:** Used capacity below 70% on each container. Alert at 70%; critical at 80%.

```bash
# Check for any storage-related alerts
ncli alert list severity=critical
ncli alert list severity=warning
```

### 5. CVM Health

```bash
# Verify all CVMs are up (should show all IPs)
ncli host list | grep -E "name|cvm-ip"

# Check CVM services on each node
allssh "genesis status" | grep -v "is running"
# Expected: no output (all running)

# Check Cassandra ring health (metadata store)
allssh "nodetool status" | grep -v "^UN"
# Expected: no output — all nodes should be UN (Up/Normal)
```

### 6. AHV Host Health

```bash
# List all AHV hosts and their state
acli host.list

# Check for any hosts in maintenance mode unexpectedly
acli host.list | grep -i maintenance

# Check AHV memory usage on each host
allssh "free -m | grep Mem"
```

**Expected:** All hosts show `normal` state; no unexpected maintenance mode entries.

### 7. VM Health

```bash
# Count powered-on vs total VMs
acli vm.list | grep -c "on$"
acli vm.list | wc -l

# Check for VMs in unexpected states (paused, suspended, unknown)
acli vm.list | grep -v -E "\s+on$|\s+off$" | grep -v "^NAME"

# Check for VMs with no NIC (common misconfiguration)
acli vm.list --include_filter=num_nics=0 2>/dev/null
```

### 8. Alert Review

```bash
# Check active critical alerts
ncli alert list severity=critical | head -30

# Check alerts from last 24 hours
ncli alert list resolved=false start-time=$(date -d "24 hours ago" +%s)000000

# Acknowledge resolved alerts
# ncli alert acknowledge id=<alert-id>
```

**From Prism Element:** Home → Alerts → filter by Severity = Critical. Acknowledge or create tickets for all unacknowledged critical alerts.

---

## Key Checks — What to Look For

| Check | Normal | Investigate if |
|---|---|---|
| NCC critical tests | All PASS | Any FAIL |
| Cluster resilience | CAN_TOLERATE ≥ 1 | = 0 |
| Storage capacity | < 70% | > 70% |
| Cassandra ring | All nodes UN | Any node DN/? |
| Genesis services | All UP | Any DOWN |
| Active critical alerts | 0 | > 0 |
| CVMs reachable | All respond | Any unreachable |

---

## Weekly Extended Checks

```bash
# Check data resiliency status — any degraded or rebuilding objects?
ncli cluster get-domain-fault-tolerance-status type=disk

# Check for any scheduled NCC failures from last 7 days
ncli ncc get-ncc-result | grep -E "FAIL|WARN" | tail -20

# Check disk health
ncli disk list | grep -v NORMAL

# LCM inventory — any pending upgrades?
# Prism Central → LCM → Inventory → check for available updates
```

---

## See also

- [Nutanix — Common Issues](../troubleshooting/common-issues/)
- [Nutanix — Procedures](procedures/)
- [Nutanix — CLI Reference](cli-reference/)
