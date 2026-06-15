---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# SnapMirror — Escalation

<div class="kb-summary">
How to escalate NetApp SnapMirror replication issues to NetApp support: what data to collect, how to invoke AutoSupport on both clusters, step-by-step case creation on mysupport.netapp.com, and the escalation path when progress stalls.

*Applies to: SnapMirror Async, Sync, SM-BC, SVM-DR on ONTAP 9.x*
</div>

```text
┌────────────────────────────── NetApp SnapMirror — Escalation ─────────────────────────────────────────┐
│                                                                                                       │
│  Escalate SnapMirror issues to NetApp support when a DR relationship has broken and the               │
│  destination volume is not current, SM-BC is in a quorum-loss state and I/O is failing,               │
│  a SnapMirror Sync relationship is reporting errors and is no longer synchronous, or                  │
│  a resync after planned failover is failing and the relationship cannot be restored.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 1 — Collect Data               │  │          Step 2 — Open the SR               │   │
│   │  snapmirror show -expanded (both clusters)   │  │  Go to mysupport.netapp.com → sign in       │   │
│   │  Invoke AutoSupport on source AND dest       │  │  Product: ONTAP; both cluster serials       │   │
│   │  event log show -message-name snapmirror.*   │  │  Priority: P1 DR broken / P2 lag at risk    │   │
│   │  network interface show -role intercluster   │  │  Attach SnapMirror show + EMS events        │   │
│   │  Write timeline: last success → first error  │  │  For P1: also call +1-888-463-8277          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  For P1 (DR unavailable / SM-BC quorum lost): open case AND call NetApp immediately.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 3 — Escalation Path            │  │         What NOT to Do                      │   │
│   │  TSE: triage + review AutoSupport from both  │  │  Do not run snapmirror break without NetApp │   │
│   │  SE: if DR failover is being considered      │  │  Do not delete destination snapshots        │   │
│   │  Duty Manager: request if SLA breached       │  │  Do not resync before NetApp confirms       │   │
│   │  TAM: especially for SM-BC implementations  │  │  Do not upgrade ONTAP mid-incident          │    │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SnapMirror     = ONTAP replication; transfers only changed blocks after initial baseline sync        │
│  intercluster LIF= dedicated logical interface for SnapMirror traffic between clusters                │
│  Async XDP      = extended data protection; async replication; RPO in minutes; most common DR mode    │
│  SnapMirror Sync= RPO=0; every write on source is synchronous to destination before ACK to host       │
│  SM-BC          = SnapMirror Business Continuity; active-active SAN zero-RPO with Mediator            │
│  Mediator       = ONTAP Mediator; quorum service for SM-BC; Linux VM at a third site                  │
│  SVM-DR         = SVM-level replication including configuration, volumes, and NAS protocol config     │
│  resync         = re-establishes a broken relationship from the last common snapshot                  │
│  snapmirror break= makes destination volume read-write; breaks the relationship                       │
│  SnapVault      = SnapMirror variant for backup retention; longer retention schedules                 │
│  AutoSupport    = ONTAP telemetry; must be invoked on BOTH clusters before opening a NetApp case      │
│  TSE            = Technical Support Engineer; first NetApp engineer assigned to a case                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access required:** Cluster admin SSH access to both source and destination ONTAP clusters; NetApp support account at mysupport.netapp.com with both cluster serial numbers registered and active support contracts
- **Both clusters required:** SnapMirror issues require data from both sides — NetApp will need AutoSupport, EMS logs, and the `snapmirror show` output from both the source and destination cluster
- **Do NOT run `snapmirror break`** without NetApp guidance — breaking a SnapMirror relationship in an error state (rather than a clean break) may leave the destination in an inconsistent state, requiring a full baseline resync
- **Do NOT delete snapshots on the destination** — the common base snapshot is the only recovery point for the resync after the relationship is restored; deleting it forces a full baseline transfer

---

## Pre-Escalation Self-Check

Run these on both clusters before opening the case.

| Check | Command | Expected result |
|---|---|---|
| Relationship health | `snapmirror show -fields healthy` | All relationships show `true` |
| Relationship state | `snapmirror show -fields state,status` | State: SnapMirrored; Status: Idle or Transferring |
| Lag time | `snapmirror show -fields lag-time` | Below RPO target for each relationship |
| Last transfer success | `snapmirror show -fields last-transfer-end-timestamp` | Recent timestamp (within RPO window) |
| Intercluster LIFs | `network interface show -role intercluster` | All intercluster LIFs are `up` |
| Intercluster connectivity | `network interface show -role intercluster -fields address` then ping each peer LIF | Reachable |
| Mediator (SM-BC only) | `snapmirror mediator show` | Mediator reachable; quorum active |
| AutoSupport delivery | `system node autosupport history show -node * -most-recent 3` | Recent successful deliveries |

---

## Step-by-Step Data Collection

### 1. Get ONTAP versions and cluster serial numbers (both clusters)

```bash
# Run on BOTH the source and destination clusters

# ONTAP version and node serial numbers
system node show -fields model,ontap-version,serial-number

# Cluster name
cluster identity show
```

### 2. Invoke AutoSupport on both clusters

```bash
# Run on BOTH clusters before opening the case
# This sends full diagnostic data to NetApp and links it to your case

system node autosupport invoke \
  -node * \
  -type all \
  -message "SnapMirror P1 incident: [brief description e.g. async relationship broken, DR unavailable]"

# Verify delivery (wait 5 minutes)
system node autosupport history show -node * -most-recent 5
# Look for "sent-successful" status
```

### 3. Capture the SnapMirror relationship state

```bash
# Run on the DESTINATION cluster (most complete view)

# Full relationship details including error message
snapmirror show -expanded > /tmp/sm-show-$(date +%Y%m%d%H%M).txt

# Relationship status with lag and last transfer info
snapmirror show -fields state,status,lag-time,healthy,last-transfer-end-timestamp,unhealthy-reason

# Transfer history for affected relationships
snapmirror show-history -destination-path <svm>:<volume>

# Current active transfers
snapmirror show -fields state | grep "Transferring"
```

### 4. Capture EMS events related to SnapMirror

```bash
# Run on BOTH clusters

# SnapMirror-specific EMS events (most relevant)
event log show -message-name snapmirror.* -time-range 24h

# All error events in the last 24 hours
event log show -severity error -time-range 24h

# For SM-BC: Mediator events
event log show -message-name smbc.* -time-range 24h
event log show -message-name mediator.* -time-range 24h
```

### 5. Check intercluster network and Mediator state

```bash
# Intercluster LIF states and addresses
network interface show -role intercluster

# Cluster peer status
cluster peer show -instance

# Connectivity test between clusters (run from both sides)
cluster peer ping -originating-node <node> -destination-cluster <peer-cluster-name>

# SM-BC Mediator status (if SM-BC is affected)
snapmirror mediator show
```

### 6. Write the timeline

```text
Source cluster: src-cluster-01 (AFF A400, ONTAP 9.13.1P5, SN: XXXXXXXX)
Destination cluster: dst-cluster-01 (FAS2820, ONTAP 9.13.1P5, SN: XXXXXXXX)
Relationship type: Async XDP (MirrorAllSnapshots policy)
Protected volumes: 12 volumes across 3 SVMs (SVM-ORACLE, SVM-SAP, SVM-SQLSERVER)
Replication link: 1 Gbps WAN MPLS between Site A and Site B
Issue first observed: 2026-06-15 10:00 UTC
Last successful transfer: 2026-06-15 08:00 UTC (RPO = 2 hours behind)
Changes in 24h before the issue:
  - 08:00: Network maintenance on MPLS circuit; 15-minute outage
  - 08:30: MPLS restored; SnapMirror transfers expected to resume
  - 10:00: snapmirror show: all 12 relationships in "Broken-Off" state, error "network layer error"
AutoSupport invoked: Yes — src-cluster-01 at 10:05 UTC, dst-cluster-01 at 10:07 UTC
Steps already taken:
  - Verified MPLS circuit is restored; inter-cluster LIFs can ping each other
  - Did NOT run snapmirror resync (awaiting NetApp guidance on common snapshot state)
  - Did NOT delete any destination snapshots
Blast radius: DR capability lost for 12 volumes; RPO currently 2 hours and growing; DBA alerted
```

---

## How to Open the SR on mysupport.netapp.com

1. Go to **mysupport.netapp.com** and sign in with your NetApp SSO account.

2. Click **Support** → **Cases & Claims** → **Create a New Case**.

3. Under **Product**, choose **ONTAP** for FAS/AFF hardware.

4. Under **Serial Number**, enter the source cluster node serial number. Repeat for the destination cluster in the case description.

5. Under **Priority**, select:
   - **P1 — Critical**: SM-BC quorum lost and host I/O is failing; all SnapMirror relationships are broken and DR is completely unavailable; a restore is failing during an active disaster recovery
   - **P2 — High**: SnapMirror relationship broken with lag growing; resync failing after a planned maintenance window; SM-BC Mediator unreachable but I/O is continuing; RPO violation imminent
   - **P3 — Medium**: A single relationship is broken; others are healthy; workaround available; no immediate DR risk
   - **P4 — Low**: How-to, SnapMirror design review, pre-migration planning, SVM-DR configuration question

6. In the **Summary** field: relationship type + symptom. Example: `ONTAP 9.13.1P5 — 12 Async XDP SnapMirror relationships Broken-Off after MPLS maintenance, DR unavailable, RPO 2h and growing`.

7. In the **Description** field, paste:
   - ONTAP versions from both clusters (Step 1)
   - AutoSupport invocation confirmation from both clusters (Step 2)
   - `snapmirror show` output for affected relationships (Step 3)
   - SnapMirror EMS events from both clusters (Step 4)
   - Intercluster LIF and cluster peer state (Step 5)
   - The timeline (Step 6)

8. Under **Attachments**, upload any large files not captured by AutoSupport.

9. Click **Submit**. You receive a case number immediately.

10. **P1 only:** call NetApp support after submission:
    - North America: +1-888-463-8277 (24×7 with SupportEdge 24×7)
    - State "P1 — SnapMirror DR unavailable, [X] relationships broken, RPO growing, case XXXXXXXX" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at mysupport.netapp.com with AutoSupport invoked on both clusters
         ↓
Step 2 — TSE acknowledges and reviews AutoSupport + snapmirror show data
         (P1: < 1 hr; P2: < 2 hr — requires SupportEdge 24×7)
         ↓
Step 3 — If no meaningful progress in 2 hours for P1:
         → Reply: "Requesting escalation to SnapMirror Specialist Engineer"
         → State: "[all relationships broken / SM-BC quorum lost / resync failing]"
         ↓
Step 4 — Product Specialist Engineer assigned
         → They will review EMS events and may request live cluster access (WebEx session)
         → Have SSH to both cluster management LIFs ready
         ↓
Step 5 — If issue involves code-level problem (SM-BC quorum state, resync algorithm bug):
         → Specialist escalates to NetApp ONTAP Engineering
         → Engineering may provide targeted EMS debug commands or a hotpatch
         ↓
Step 6 — For P1 with DR completely unavailable > 2 hours:
         → Call +1-888-463-8277 and request a Duty Manager escalation
         → Engage NetApp account team for executive escalation
         → TAM involvement: essential for SM-BC implementations where quorum loss affects SAN I/O
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Run `snapmirror break` on a relationship in an error state | Breaking in an error state may leave the destination volume in an inconsistent state; the relationship can only be restored via a full resync | Let NetApp confirm the destination state before any break; a controlled break should only happen in a clean state |
| Delete destination snapshots | The common base snapshot is the only anchor for the resync after the relationship is restored; deleting it forces a full baseline transfer that may take hours or days | Leave all destination snapshots intact; only delete after NetApp confirms all common snapshots are no longer needed |
| Run `snapmirror resync` without NetApp confirmation of the common snapshot | A resync without a common snapshot triggers a full baseline; on large volumes this can take days and extends the DR gap | Confirm with NetApp which common snapshot exists before attempting any resync |
| Upgrade ONTAP mid-incident | Adding a new ONTAP version to an already-broken replication state creates additional variables | Freeze all ONTAP upgrades until the SnapMirror relationship is restored and confirmed healthy |
| Delete and recreate the SnapMirror relationship | Recreating the relationship also destroys all existing destination data and requires a full baseline | Only delete and recreate on explicit NetApp instruction, after confirming that no resync from the existing state is possible |
| Modify intercluster LIF configurations during the incident | Changing LIF IPs or routing mid-incident changes the network state NetApp is diagnosing | Freeze all network changes on the intercluster network until NetApp confirms the root cause |

---

## Useful Commands for Case Updates

```bash
# Run on DESTINATION cluster — paste into every case update

# Relationship health and lag
snapmirror show -fields state,status,lag-time,healthy,unhealthy-reason

# Active SnapMirror EMS events (last 2 hours)
event log show -message-name snapmirror.* -time-range 2h

# Intercluster LIF states
network interface show -role intercluster

# Cluster peer connectivity
cluster peer show

# Mediator status (SM-BC only)
snapmirror mediator show
```

---

## Support SLA Reference

| Priority | Definition | Initial Response SLA |
|---|---|---|
| P1 — Critical | SM-BC quorum lost; all DR relationships broken; restore failing; DR unavailable | < 1 hour (24×7 — SupportEdge 24×7 required) |
| P2 — High | Relationship broken with growing lag; resync failing; RPO at risk | < 2 hours (24×7 — SupportEdge 24×7 required) |
| P3 — Medium | Single relationship broken; others healthy; workaround available | < 4 hours (business hours) |
| P4 — Low | How-to, design review, migration planning | Next business day |

---

## See also

- [SnapMirror — Diagnostics](diagnostics/)
- [SnapMirror — Common Issues](common-issues/)

---

## Verify resolution

- Run `snapmirror show -fields healthy` on the destination cluster and confirm all relationships show `true`
- Run `snapmirror show -fields lag-time` and confirm lag is within the RPO target for each relationship
- Run `snapmirror show -fields last-transfer-end-timestamp` and confirm recent successful transfers
- Run `event log show -message-name snapmirror.* -time-range 2h` on both clusters and confirm no new error events
- Run `cluster peer show` and confirm all cluster peers are reachable
- For SM-BC: run `snapmirror mediator show` and confirm the Mediator is reachable and quorum is active
- Invoke a final AutoSupport tied to the case: `system node autosupport invoke -node * -type all -message "case XXXXXXXX resolved"`
- Monitor the relationship lag for 30 minutes to confirm transfers are completing within the RPO target
