---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# ONTAP — Escalation

<div class="kb-summary">
How to escalate NetApp ONTAP issues to NetApp support: what data to collect, how to invoke AutoSupport, step-by-step case creation on mysupport.netapp.com, and the escalation path when progress stalls.

*Applies to: ONTAP 9.x*
</div>

```text
┌────────────────────────────────────── NetApp ONTAP — Escalation ──────────────────────────────────────┐
│                                                                                                       │
│  Escalate ONTAP issues to NetApp support when a node is down, an aggregate is                         │
│  degraded, I/O is failing, or SnapMirror is broken in an active DR scenario.                          │
│  Invoke AutoSupport BEFORE opening the case to give NetApp instant system context.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 1 — Collect Data               │  │          Step 2 — Open the SR               │   │
│   │  Invoke AutoSupport tied to the incident     │  │  Go to mysupport.netapp.com → sign in       │   │
│   │  Run: event log show -severity error         │  │  Product: ONTAP; pick your version          │   │
│   │  Note cluster + node + ONTAP version         │  │  Priority: P1 down / P2 major / P3 minor    │   │
│   │  Capture health alerts + failed disks        │  │  Attach event log output + timeline         │   │
│   │  Write timeline: last good → first failure   │  │  AutoSupport case links automatically       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  For P1: open portal case AND call NetApp support at +1-888-463-8277 immediately.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 3 — Escalation Path            │  │         What NOT to Do                      │   │
│   │  TSE: triage + review AutoSupport data       │  │  Do not pull disks without NetApp guidance  │   │
│   │  Specialist SE: if TSE cannot resolve        │  │  Do not destroy an aggregate under repair   │   │
│   │  Duty Manager: request if SLA breached       │  │  Do not delete Snapshots during incident    │   │
│   │  Account team: for P1 running > 4 hours      │  │  Do not upgrade ONTAP mid-incident          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AutoSupport  = telemetry bundle sent to NetApp; required before opening every case                   │
│  TSE          = Technical Support Engineer; first NetApp engineer assigned to a case                  │
│  ONTAP        = NetApp storage OS; unified NAS, SAN, object across AFF, FAS, ONTAP Select             │
│  Aggregate    = RAID group of disks underpinning FlexVols on a node                                   │
│  SVM          = Storage Virtual Machine; logical storage server with protocols and IPs                │
│  SnapMirror   = async or synchronous replication between ONTAP systems for DR and backup              │
│  SR           = Service Request; support case assigned by NetApp; referenced as case number           │
│  SupportEdge  = NetApp support contract tier; P1 response requires 24×7 SupportEdge                   │
│  EMS          = ONTAP Event Management System; generates error/warning/info events                    │
│  SM-BC        = SnapMirror Business Continuity; zero-RPO sync replication                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access required:** ONTAP cluster admin credentials (SSH to cluster management LIF); NetApp support account at mysupport.netapp.com with serial numbers registered
- **Do this first:** invoke AutoSupport (Step 1 below) before opening the case. NetApp's first question will be whether AutoSupport has been sent — having it delivered cuts first-response time significantly
- **Do NOT pull failed disks** without NetApp guidance. A failed disk may still hold RAID group parity that is needed for reconstruction — pulling it prematurely can cause data loss
- **Do NOT destroy aggregates** that are in a degraded or partial state — let NetApp confirm the disk group is fully reconstructed first

---

## Pre-Escalation Self-Check

Run these before opening the case. Many ONTAP issues are resolvable without vendor support.

| Check | Command | Expected result |
|---|---|---|
| Cluster health | `cluster show` | All nodes healthy, quorum achieved |
| Node failover | `storage failover show` | Both nodes show `Connected` and `Takeover Enabled` |
| Health alerts | `system health alert show` | No CRITICAL alerts (resolve or document each one) |
| Disk status | `storage disk show -broken` | Empty output (no broken disks) |
| Aggregate status | `storage aggregate show -fields state,status` | All aggregates `online` |
| Volume space | `volume show -fields used-percent` | No volume above 90% |
| SnapMirror health | `snapmirror show -fields healthy` | All relationships show `true` |
| Network ports | `network port show -fields health-status` | All ports `healthy` |
| NTP sync | `cluster time-service ntp status show` | All nodes synchronized |
| AutoSupport delivery | `system node autosupport history show -node * -most-recent 5` | Recent deliveries with status `sent-successful` |

---

## Step-by-Step Data Collection

Run from the ONTAP cluster management interface (SSH as cluster admin).

### 1. Get the ONTAP version and node serial numbers

```bash
# ONTAP version on all nodes — include in the case description
system node show -fields model,ontap-version,serial-number

# Example output:
# Node         Model       ONTAP-Version  Serial-Number
# -------      --------    -------------  -------------
# node-01      AFF A400    9.13.1P5       8ABC123456
# node-02      AFF A400    9.13.1P5       8ABC123457
```

### 2. Invoke AutoSupport (ties your system data to the case)

```bash
# Invoke full AutoSupport with a message referencing the incident
# Do this BEFORE opening the case — it takes ~5 min to reach NetApp
system node autosupport invoke -node * -type all -message "Production incident: [brief description]"

# Verify delivery — wait 5 minutes, then check
system node autosupport history show -node * -most-recent 5
# Look for "sent-successful" in the Delivery-Status column

# If AutoSupport is not configured or delivery fails, collect locally:
system node autosupport invoke -node * -type all -uri mailto:support@netapp.com
# Or attach the event log output to the case manually
```

### 3. Collect the current health state

```bash
# Overall cluster health
cluster show

# Node failover status
storage failover show

# Active health alerts — paste full output into the case description
system health alert show

# EMS error events in last 24 hours
event log show -severity error -time-range 24h

# Failed or broken disks
storage disk show -broken
storage disk show -fields state | grep -v online | grep -v spare
```

### 4. Collect the aggregate and volume state

```bash
# Aggregate status
storage aggregate show -fields state,status,used-percent

# If a specific aggregate is degraded
storage aggregate show-status -aggregate <aggr-name>

# Volume space
volume show -fields used-percent | sort -k3 -rn | head -20

# SnapMirror relationships
snapmirror show -fields state,lag-time,healthy,relationship-status
```

### 5. Write the timeline

```text
ONTAP version: 9.13.1P5
Cluster: cluster-01 (nodes: node-01, node-02)
Node serial numbers: 8ABC123456, 8ABC123457
Issue first observed: 2026-06-14 14:30 UTC
Last known good state: 2026-06-14 12:00 UTC
Changes in the 24h before the issue:
  - 12:00: ONTAP patch 9.13.1P4 → 9.13.1P5 applied to both nodes
  - 14:25: EMS shows "DISK.degraded" on aggregate aggr_data on node-01
  - 14:30: 3 volumes show "partial" state; host I/O errors reported
Steps already taken:
  - Ran: storage aggregate show-status -aggregate aggr_data
  - Confirmed: 2 of 8 disks show "broken" status
  - Did NOT pull the broken disks or destroy the aggregate
Blast radius: 3 volumes with 12 NFS mounts are degraded; ESXi hosts show I/O errors
AutoSupport sent: Yes — invoked at 14:35 UTC with message "aggr_data degraded, case pending"
```

---

## How to Open the SR on mysupport.netapp.com

1. Go to **mysupport.netapp.com** and sign in with your NetApp SSO account. If you do not have one: click **Register** and use your company email — entitlement is linked to your NetApp support contract and system serial numbers.

2. Click **Support** → **Cases & Claims** → **Create a New Case** (or click the **Create Case** button in the top navigation).

3. Under **Select a Product**, choose **ONTAP** (for FAS/AFF hardware) or **ONTAP Select** for software-only deployments.

4. Under **Software Version**, select your ONTAP version from the drop-down.

5. Under **Serial Number**, enter the node serial number from Step 1. This validates entitlement and links the case to your AutoSupport data.

6. Under **Priority**, select:
   - **P1 — Critical**: Node down or in takeover; aggregate failed; I/O completely stopped; data inaccessible; no workaround
   - **P2 — High**: Aggregate or volume degraded; significant performance impact; SnapMirror broken in active DR; workaround exists but impractical
   - **P3 — Medium**: Non-critical feature affected; workaround available; single volume or protocol degraded
   - **P4 — Low**: How-to question, pre-upgrade planning, or non-urgent configuration review

7. In the **Title** field, write one sentence: platform + symptom + scope. Example: `AFF A400 cluster-01 — aggr_data degraded, 2 disks broken, 3 volumes partial, 12 NFS mounts affected`.

8. In the **Description** field, paste:
   - ONTAP version and serial numbers from Step 1
   - The AutoSupport invocation message and confirmation of delivery from Step 2
   - The health alert output from Step 3
   - The aggregate and volume state from Step 4
   - The timeline from Step 5
   - What you have already tried

9. Under **Attachments**, upload any files not captured by AutoSupport (manual event log exports, performance captures).

10. Click **Submit**. You will receive a case number immediately by email. The case is automatically linked to your AutoSupport data.

11. **P1 only:** call NetApp support immediately after submission:
    - **Global/North America:** +1-888-463-8277 (24×7 with SupportEdge)
    - **EMEA:** check mysupport.netapp.com for your regional number
    - State "P1 — [node down / aggregate failed / I/O stopped]" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at mysupport.netapp.com with AutoSupport invoked and event log attached
         ↓
Step 2 — TSE (Technical Support Engineer) acknowledges and reviews AutoSupport data
         (P1: within 1 hour; P2: within 2 hours)
         ↓
Step 3 — If no meaningful progress after 2 hours for P1 or 4 hours for P2:
         → Reply in case: "Requesting escalation to ONTAP Specialist or Escalation Engineer"
         → State: "[node offline / 12 NFS hosts without storage / DR capability lost]"
         ↓
Step 4 — Product Specialist or Escalation Engineer is assigned
         → They may request a live WebEx session for cluster access
         → Have SSH to cluster management LIF and ONTAP System Manager ready
         ↓
Step 5 — If issue requires firmware or code-level investigation:
         → Escalation Engineer involves NetApp Engineering
         → Engineering may provide a hotpatch or workaround procedure
         ↓
Step 6 — For P1 with no resolution after 4 hours:
         → Call +1-888-463-8277 and request escalation to Support Duty Manager
         → Contact your NetApp Account Manager to engage executive escalation
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Pull broken disks from a degraded aggregate | Disk may still hold parity needed for reconstruction; removing it can cause data loss | Wait for NetApp to confirm the aggregate is not in a state where removal causes further loss |
| Destroy a degraded aggregate | Unrecoverable data loss if any data is still readable | Let NetApp guide the recovery sequence |
| Delete Snapshots during an incident | Snapshots may be the only recovery path if volumes fail further | Leave Snapshots intact until NetApp confirms they are not needed |
| Run `storage disk unfail` or `storage disk assign` without guidance | Can assign disks incorrectly and corrupt RAID groups | Let NetApp provide the exact commands for your situation |
| Upgrade ONTAP mid-incident | Adds variables; may change log format; upgrade may be blocked by the current issue | Freeze all changes until the case is resolved |
| Open multiple parallel cases for the same incident | Splits NetApp's diagnostic context across cases | Use one case; add all updates to it |

---

## Useful Commands for Case Updates

Paste these into case replies to show NetApp the current state.

```bash
# Cluster health snapshot — paste into every case update
cluster show
storage failover show
system health alert show

# EMS events since the incident
event log show -severity error -time-range 24h

# Aggregate status (if storage issue)
storage aggregate show -fields state,status,used-percent
storage aggregate show-status -aggregate <aggr-name>

# Disk status
storage disk show -broken
storage disk show -fields state,aggregate,position | grep -v online | grep -v spare

# SnapMirror (if DR/replication issue)
snapmirror show -fields state,lag-time,healthy
snapmirror show -destination-path <vserver>:<volume> -instance

# Node performance (for latency/throughput issues)
node run -node <nodename> sysstat -c 5 -x 2

# Volume IOPS and latency
qos statistics performance show
```

---

## Support SLA Reference

| Priority | Definition | Initial Response SLA |
|---|---|---|
| P1 — Critical | Node down; aggregate failed; I/O stopped; data inaccessible | 1 hour (24×7 — requires SupportEdge 24×7) |
| P2 — High | Aggregate degraded; major replication failure; significant I/O impact | 2 hours (24×7 — requires SupportEdge 24×7) |
| P3 — Medium | Partial degradation; workaround exists; single volume or protocol affected | 4 hours (business hours) |
| P4 — Low | How-to question, planning, non-impacting issue | Next business day |

---

## See also

- [ONTAP — Diagnostics](diagnostics/)
- [ONTAP — Common Issues](common-issues/)

---

## Verify resolution

- Run `cluster show` and confirm all nodes are healthy and in quorum
- Run `storage failover show` — both nodes show `Connected` and `Takeover Enabled`
- Run `system health alert show` — no active CRITICAL alerts
- Run `storage aggregate show` — all aggregates show `online` status
- Run `storage disk show -broken` — no broken disks remaining (or replacement confirmed)
- Verify SnapMirror relationships: `snapmirror show -fields healthy` shows `true` for all
- Run an I/O test from an affected host and confirm storage responds within expected latency
- Invoke a final AutoSupport tied to the resolved case: `system node autosupport invoke -node * -type all -message "case <number> resolved"`
