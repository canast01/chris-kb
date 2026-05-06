# SRDF/S Troubleshooting

> Part of the [SRDF/S](../) reference.

SRDF/S issues typically manifest as pair state transitions away from `Synchronized`, elevated host write latency, or unexpected failover splits. Because SRDF/S is synchronous, any WAN degradation **directly impacts production write latency** — treat RTT increases above 5ms as a storage incident, not purely a network event.

Always collect `symrdf query -g <group> -v` and array event logs before engaging Dell support.

---

## High Host Write Latency

**Symptom:** Applications report write slowness; storage latency exceeds baseline; no hardware alerts.

```bash
# Check current SRDF link RTT and write pending counts
symcfg -sid <r1_sid> list -rdfg <group_num> -v | grep -E "RTT\|Pending\|Link"

# Check write latency per device
symdev -sid <r1_sid> show <dev_id> | grep -E "Write|Response"

# Check array performance overview in Unisphere
# Performance → Directors → SRDF directors → check write pending
```

**Root cause:** Any increase in the WAN RTT adds directly to host write latency for SRDF/S. Every 1ms of additional RTT adds ~2ms to host write response time.

**Immediate action:**
1. Get the current RTT from the network team — compare to the baseline measured at deployment.
2. If RTT has spiked, check for WAN link congestion or routing path changes.
3. Engage the network team if RTT is elevated — do not accept "the link is up" as resolution; RTT matters.

---

## Pair Enters Write Disabled State

**Symptom:** `symrdf query` shows pair state as `Write Disabled`; hosts may report I/O errors.

`Write Disabled` indicates the R1 array could not complete writes to R2 within the write timeout threshold (typically due to RTT spike or link loss). The R1 array disables writes on the affected R1 devices to preserve data consistency.

```bash
# Confirm Write Disabled state
symrdf -g <dgname> -sid <r1_sid> query | grep "Write Disabled"

# Check for link errors
symcfg -sid <r1_sid> list -rdfg <group_num> -v
```

**Recovery:**

1. Resolve the underlying link or RTT issue first.
2. Once the link is stable, re-establish the SRDF pair:

```bash
# Resync from R1 to R2 (R1 data is authoritative in this scenario)
symrdf -g <dgname> -sid <r1_sid> resync -noprompt

# Monitor until pair returns to Synchronized
symrdf -g <dgname> -sid <r1_sid> query
```

---

## Pair in `Invalid` State

**Symptom:** Pair state shows `Invalid` — typically after an unresolved split or an earlier failover that was not cleanly restored.

```bash
# Check the event log for the event that caused the Invalid state
symevent -sid <r1_sid> list -last 30 | grep -i "SRDF\|Invalid\|failover"
```

**Resolution (R1 is authoritative — no real failover occurred):**

```bash
symrdf -g <dgname> -sid <r1_sid> resync -noprompt
# Pushes R1 data to R2 and re-establishes sync
```

**Resolution (R2 has the latest data — a real failover occurred):**

```bash
# Confirm with application team that R2 has the correct data
# Then fail back to R1
symrdf -g <dgname> -sid <r2_sid> failback -noprompt
```

**Do not resync or restore without first confirming which side has the authoritative data.** An incorrect resync will permanently overwrite data.

---

## Pair in `Split` State

A `Split` state means both R1 and R2 are R/W and data is diverging. This is normal during a planned failover but is an incident if unexpected.

```bash
# Check when the split occurred
symevent -sid <r1_sid> list -last 24h | grep -i "split\|SRDF"

# Identify which side has writes since the split
symdev -sid <r1_sid> show <dev_id> | grep "Modified"
symdev -sid <r2_sid> show <dev_id> | grep "Modified"
```

**Never re-establish a split pair without application team sign-off.** Restoring R1 overwrites any R2 writes made during the split period and vice versa.

---

## ISL / FCIP Link Failure

**Symptom:** SRDF link is down; pairs move to `Suspended` or `Write Disabled`.

```bash
# Check SRDF director port state
symcfg -sid <r1_sid> list -dir all -v | grep -E "RDF|Port|State"

# From SAN switch (Cisco MDS)
show fcip session
show port-channel summary  # if using port-channel
show interface gigabitEthernet X/X

# From Brocade
portshow <port>
portcfgshow  # check FCIP port config
```

**Recovery after link restoration:**

```bash
# Pair should auto-resume once link is restored (depending on configuration)
# If pairs remain Suspended, manually resume:
symrdf -g <dgname> -sid <r1_sid> resume -noprompt

# Verify Synchronized state is reached (may take time to fully sync)
symrdf -g <dgname> -sid <r1_sid> query
```

---

## Unintended Failover During Maintenance

**Cause:** Maintenance was performed without declaring a maintenance window; SRDF monitors triggered automatic protection responses.

**Prevention:**

```bash
# Before any maintenance that touches SRDF links, directors, or the arrays:
# Step 1 — Suspend SRDF/S pair (converts to async temporarily)
symrdf -g <dgname> -sid <r1_sid> suspend -noprompt

# Step 2 — Disable SRDF health monitoring alerts in the monitoring platform for the duration

# Step 3 — Perform maintenance

# Step 4 — Resume and verify Synchronized state before re-enabling monitoring
symrdf -g <dgname> -sid <r1_sid> resume -noprompt
symrdf -g <dgname> -sid <r1_sid> query
```
