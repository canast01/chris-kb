---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# SRDF/S — Common Issues

<div class="kb-summary">
SRDF/S troubleshooting: synchronous link failures, invalid track accumulation, host I/O impact during link faults, `symrdf failover` under failure, and escalation.

*Applies to: SRDF/S*
</div>
![SRDF/S — Common Issues](../../../../assets/storage-dell-srdf-s-troubleshooting-common-issues.svg)

> Part of the [SRDF/S Troubleshooting](index.md) reference.

SRDF/S issues typically manifest as pair state transitions away from `Synchronized`, elevated host write latency, or unexpected failover splits. Because SRDF/S is synchronous, any WAN degradation **directly impacts production write latency** — treat RTT increases above 5ms as a storage incident, not purely a network event.

Always collect `symrdf query -g <group> -v` and array event logs before engaging Dell support.

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
linkdown_recovery_decision_tree: "Link-Down Recovery Decision Tree" {shape: rectangle}
pair_in_invalid_state: "Pair in `Invalid` State" {shape: rectangle}
pair_in_split_state: "Pair in `Split` State" {shape: rectangle}
isl_fcip_link_failure: "ISL / FCIP Link Failure" {shape: rectangle}
unintended_failover_during_maintenan: "Unintended Failover During Maintenance" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> linkdown_recovery_decision_tree: investigate
symptom -> pair_in_invalid_state: investigate
symptom -> pair_in_split_state: investigate
symptom -> isl_fcip_link_failure: investigate
symptom -> unintended_failover_during_maintenan: investigate
diagnostic_flow -> resolution
linkdown_recovery_decision_tree -> resolution
pair_in_invalid_state -> resolution
pair_in_split_state -> resolution
isl_fcip_link_failure -> resolution
unintended_failover_during_maintenan -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "See Link-Down Recovery —\nCheck physical link then resume" {shape: rectangle}
R2: "See Link-Down Recovery —\nResume pair after link restored" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "See Link-Down Recovery —\nEscalate to network team" {shape: rectangle}
R4: "See Common Issues —\nPair in Consistent state: monitor" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "See ISL / FCIP Link Failure —\nRestore link then resync pair" {shape: rectangle}
R6: "See Root Causes —\nFCIP MTU mismatch or GRE overhead" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "See Pair in Split State —\nConfirm authoritative side" {shape: rectangle}
R8: "See Unintended Failover —\nSuspend before maintenance" {shape: rectangle}
D5: "D5" {shape: rectangle}
R9: "See Invalid State —\nResync R1 to R2" {shape: rectangle}
R10: "See Invalid State —\nFailback from R2: engage Dell Support" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "B4" {shape: rectangle}
B5: "B5" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
D4 -> R7
D4 -> R8
D5 -> R9
D5 -> R10
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Link-Down Recovery Decision Tree

```d2
direction: right

linkAlert: "Alert: SRDF/S Link Down\nor Pairs not Synchronized" {shape: rectangle}
checkPairState: "Check Pair State\nsymrdf -g dgname -sid sid query" {shape: rectangle}
pairStateVal: "pairStateVal" {shape: rectangle}
writeDisabled: "Write Disabled\n→ Array stopped writes\nto protect consistency" {shape: rectangle}
invalidState: "Invalid State\n→ Possible data divergence" {shape: rectangle}
suspended: "Suspended\n→ Link dropped or manual suspend" {shape: rectangle}
partitioned: "Partitioned\n→ Link interrupted mid-transfer" {shape: rectangle}
checkPhysLink: "Check Physical Link\nFCIP tunnel / dark fibre state" {shape: rectangle}
linkUp: "linkUp" {shape: rectangle}
checkRTT: "Check RTT\nping -c 20 dr-site-ip" {shape: rectangle}
escalateNet: "Escalate to Network Team\nRTT still elevated" {shape: rectangle}
rttNormal: "rttNormal" {shape: rectangle}
resyncPair: "Resync Pair\nsymrdf -g dgname -sid sid resync -noprompt" {shape: rectangle}
resumePair: "Resume Pair\nsymrdf -g dgname -sid sid resume -noprompt" {shape: rectangle}
monitorSync: "Monitor SyncInProg\nuntil Synchronized" {shape: rectangle}
checkDataAuth: "Identify Authoritative Side\nDo NOT resync without confirming" {shape: rectangle}
engageSupport: "Engage Dell Support\nData consistency risk" {shape: rectangle}

linkAlert -> checkPairState
checkPairState -> pairStateVal
pairStateVal -> writeDisabled
pairStateVal -> invalidState
pairStateVal -> suspended
pairStateVal -> partitioned
writeDisabled -> checkPhysLink
suspended -> checkPhysLink
partitioned -> checkPhysLink
checkPhysLink -> linkUp
linkUp -> checkRTT
linkUp -> escalateNet
checkRTT -> rttNormal
rttNormal -> resyncPair
rttNormal -> resumePair
rttNormal -> escalateNet
resyncPair -> monitorSync
resumePair -> monitorSync
invalidState -> checkDataAuth
checkDataAuth -> engageSupport
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

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Srdf S — Diagnostics](../diagnostics/)
- [Srdf S — Escalation](../escalation/)
- [Srdf S — Health Checks](../../operations/health-checks/)
