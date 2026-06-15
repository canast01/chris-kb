---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# RecoverPoint — Escalation

<div class="kb-summary">
How to escalate Dell RecoverPoint (RP4VM) replication issues to Dell Technologies support: what data to collect, how to collect RPA support bundles, step-by-step case creation on dell.com/support, and the escalation path when progress stalls.

*Applies to: RecoverPoint for Virtual Machines (RP4VM) 5.x / 6.x*
</div>

```text
┌──────────────────────────────── Dell RecoverPoint — Escalation ───────────────────────────────────────┐
│                                                                                                       │
│  Escalate RecoverPoint issues to Dell support when all consistency groups for a production            │
│  workload are paused and journal data is being lost, a failover is required but the CG cannot         │
│  be enabled at the recovery site, the journal volume has filled causing replication to stop,          │
│  or an RPA upgrade has left appliances at mixed versions and CGs cannot be activated.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 1 — Collect Data               │  │          Step 2 — Open the Case             │   │
│   │  get support_bundle on each RPA              │  │  Go to dell.com/support → My Cases          │   │
│   │  Note RP version (both sites A and B)        │  │  Select product by RPA cluster serial       │   │
│   │  Capture CG state and lag from RP UI         │  │  Severity: P1 CG offline / P2 lag critical  │   │
│   │  Check journal fill level per CG             │  │  Attach RPA bundles from both sites         │   │
│   │  Write timeline: last sync → first error     │  │  For P1: also call Dell support             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  For P1: open portal case AND call Dell immediately.                                                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 3 — Escalation Path            │  │         What NOT to Do                      │   │
│   │  T1: triage + confirm RPA bundles received   │  │  Do not fail over without Dell confirmation │   │
│   │  T2: RP SE assigned; CG and journal analysis │  │  Do not delete journal volumes              │   │
│   │  Engineering: for CG state or RPA code issues│  │  Do not pause/resume CGs without Dell OK   │    │
│   │  TAM: engage for P1 data loss risk           │  │  Do not upgrade RP mid-incident             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA             = RecoverPoint Appliance; virtual appliance managing journal and replication         │
│  CG              = Consistency Group; set of volumes protected together; journal is per-CG            │
│  journal         = write-order-consistent storage capturing all writes for point-in-time access       │
│  splitter        = intercepts host writes at hypervisor level; sends copy to RPA                      │
│  lag             = time between latest write on source and latest entry committed to journal          │
│  bookmark        = named marker in journal; enables recovery to a known application state             │
│  image access    = mounting a journal point-in-time to a host for testing or recovery                 │
│  failover        = activating the replica at the recovery site; breaks the replication link           │
│  test copy       = non-disruptive image access for DR testing without breaking replication            │
│  RPO             = Recovery Point Objective; lag is the real-time measure of RPO                      │
│  CDP             = Continuous Data Protection; every write journaled at sub-second granularity        │
│  reverse replication = after failover, replicates from recovery site back to re-sync production       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access required:** SSH to each RPA appliance (admin user); RecoverPoint management console access (Unisphere for RecoverPoint or the standalone RP management console); Dell support account at dell.com/support linked to the RPA cluster serial number
- **Both sites required:** RecoverPoint issues almost always require RPA bundles from both Site A and Site B — collect and upload bundles from all RPA appliances at both sites
- **Do NOT fail over** a consistency group without Dell confirmation — an incorrect failover can break the replication relationship, and if the source data was not yet fully journaled at the target, the failover image may be incomplete
- **Do NOT delete journal volumes** — the journal is the only record of all writes since the last baseline; deleting it makes point-in-time recovery impossible

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command / Location | Expected result |
|---|---|---|
| RP version (Site A) | SSH to RPA-A: `get system_info` or RP UI → About | Note full version string |
| RP version (Site B) | SSH to RPA-B: `get system_info` | Both sites same version |
| CG state | RP Management Console → Consistency Groups | All CGs in Active Replicating state |
| Replication lag | RP Console → CG → Copy status → Lag | Below RPO target |
| Journal fill level | RP Console → CG → Journal → Journal utilization | Below 80% |
| RPA health | RP Console → Infrastructure | All RPAs Online |
| Link state | RP Console → Infrastructure → Links | WAN links Connected |
| Journal volume accessible | Storage array hosting journal LUNs | All journal LUNs presented and accessible |

---

## Step-by-Step Data Collection

### 1. Get the RP version and cluster serial numbers

```bash
# SSH to each RPA as admin
ssh admin@<rpa-site-a-ip>

# System information (version, serial)
get system_info

# RP cluster serial number (used to open the support case)
get cluster_info
```

Collect from every RPA at both Site A and Site B. The version and serial must match (or a version mismatch may itself be the issue).

### 2. Capture consistency group state and lag

In the RecoverPoint Management Console:
1. Navigate to **Protect** → **Consistency Groups**.
2. For each affected CG, note:
   - State (Active Replicating / Paused / Error)
   - Replication lag (in seconds or minutes)
   - Journal utilization percentage
   - Last consistent image timestamp
3. Take a screenshot or export the CG state table.

```bash
# From RPA CLI — show all CG names and states
get cg_state
```

### 3. Check journal fill level and link state

```bash
# SSH to RPA

# Journal state per CG
get journal_state

# WAN link state between sites
get link_status

# RPA cluster health
get rpa_state
```

### 4. Collect RPA support bundles from all appliances

```bash
# SSH to each RPA (run on every RPA at both Site A and Site B)
ssh admin@<rpa-ip>

# Generate the support bundle
get support_bundle

# The bundle is saved locally on the RPA; download via SFTP
# sftp admin@<rpa-ip>
# get support_bundle_*.tar
```

Collect one bundle from each RPA appliance. For a 2-site setup with 2 RPAs per site: 4 bundles total.

### 5. Write the timeline

```text
RP version: Site A = 6.0.1.3 SP1, Site B = 6.0.1.3 SP1 (same version — good)
RPA cluster: Site A (rpa-a1, rpa-a2), Site B (rpa-b1, rpa-b2)
Cluster serial: XXXXXXXX (Site A), XXXXXXXX (Site B)
CGs: 12 consistency groups protecting 48 VMs (SAP HANA, Oracle 19c, SQL Server)
Replication type: CDP (Continuous Data Protection)
Issue first observed: 2026-06-15 08:00 UTC
Last confirmed healthy: 2026-06-15 06:00 UTC
Changes in 24h before the issue:
  - 06:00: Journal volumes on storage array expanded (added 2 TB to CG-ORACLE journal)
  - 08:00: RP Console: CG-ORACLE shows state "Paused — journal full (102%)"
  - 08:05: CG-SAP and CG-SQL also pause as journal capacity fills
  - 08:10: WAN link between sites shows "Reduced bandwidth (saturation event)"
Steps already taken:
  - Did NOT fail over any CG
  - Did NOT delete journal data
  - Journal volumes confirmed accessible on storage array; utilization 102% on CG-ORACLE
Blast radius: 12 CGs paused; replication stopped; RPO growing; DR images stale since 06:00 UTC
```

---

## How to Open the Case on dell.com/support

1. Go to **dell.com/support** and sign in with your Dell account.

2. Click **My Cases** → **Create New Case**.

3. Under **Product**, select **Dell RecoverPoint** or **Dell RecoverPoint for Virtual Machines (RP4VM)**. Enter the RPA cluster serial number from Step 1.

4. Under **Severity**, select:
   - **Severity 1 — Production Down**: All CGs for a critical workload are paused and journal data is being lost; a failover is required to activate DR but the CG cannot be enabled at the recovery site; data loss is imminent; no workaround
   - **Severity 2 — Degraded**: Replication lag is growing and approaching RPO violation; journal fill level above 80% and still growing; CG is active but in a degraded state; workaround is partial
   - **Severity 3 — Non-Critical**: A single CG is paused but others are healthy; replication is active at degraded performance; image access is available for DR testing; workaround exists
   - **Severity 4 — General**: How-to, upgrade planning, compatibility question, CG design review

5. In the **Summary** field: symptom + scope. Example: `RecoverPoint 6.0.1.3 — CG-ORACLE paused (journal full 102%), 12 CGs stopped, DR images stale since 06:00 UTC`.

6. In the **Description** field, paste:
   - RP versions at both sites from Step 1
   - CG states and lag from Step 2
   - Journal fill levels and link state from Step 3
   - The timeline from Step 5

7. Under **Attachments**, upload:
   - RPA support bundles from all appliances at both sites (Step 4)

8. Click **Submit**. You receive a case number immediately.

9. **Severity 1 only:** call Dell support after submission:
    - North America: +1 800 945 3355 (24×7 for production-down)
    - State "Severity 1 — RecoverPoint all CGs paused, DR images stale, data loss risk, case XXXXXXXX" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at dell.com/support with RPA bundles from both sites attached
         ↓
Step 2 — Dell T1 engineer acknowledges (P1: < 2 hr ProSupport Plus; P2: < 4 hr)
         ↓
Step 3 — If no meaningful progress within 2 hours for P1:
         → Reply in case: "Requesting escalation to RecoverPoint Senior Engineer"
         → State: "[all CGs paused / journal full / failover blocked / data loss risk]"
         ↓
Step 4 — RP T2 Senior Engineer assigned
         → They will review the RPA bundles and may request console access to the RP management UI
         → Have console access to both Site A and Site B RP management ready
         ↓
Step 5 — If issue involves a CG state that cannot be resolved by reconfiguration:
         → T2 escalates to RecoverPoint Engineering
         → Engineering may provide targeted CG state recovery or journal reset procedure
         ↓
Step 6 — For active data loss or failover required:
         → Request TAM engagement immediately
         → TAM can arrange bridge call with Engineering and coordinate emergency failover guidance
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Fail over a CG without Dell confirmation when the CG is in an error state | Failing over from an error state may activate an incomplete or inconsistent image; if the last consistent journal point is hours old, the application may start with corrupted data | Let Dell confirm what the last valid consistent image is before any failover |
| Delete journal volumes to free space | The journal is the only record of all writes; deleting it makes all point-in-time images between the baseline and now inaccessible | Expand the journal volumes on the storage array; engage Dell to assess whether journal trimming is safe |
| Pause and resume CGs without Dell guidance during a journal full event | Pausing a CG mid-write can leave the journal in an inconsistent commit state; resuming on a partially committed journal may produce corrupted images | Let Dell direct the exact pause/resume sequence to ensure journal consistency is maintained |
| Upgrade RecoverPoint mid-incident | An upgrade on an RPA cluster with paused CGs can leave appliances at mixed versions and make CG activation impossible | Resolve the CG pause and confirm the RP cluster is fully healthy before any upgrade |
| Access image (image access mode) on a journal that is still filling | Accessing a journal image while the journal is full can lock the image access state and make the CG unavailable for additional writes | Wait until journal capacity is resolved before initiating image access |
| Remove and re-add a splitter without Dell direction | Removing the splitter disconnects the host from the RPA; on reconnect, the CG must do a full baseline sync that may take hours or days for large VMs | Only remove/re-add splitters with Dell's documented procedure for splitter maintenance |

---

## Useful Commands for Case Updates

```bash
# SSH to each RPA — paste into every case update

# RPA version and cluster info
get system_info
get cluster_info

# CG states
get cg_state

# Journal fill levels
get journal_state

# WAN link state
get link_status

# RPA health
get rpa_state
```

---

## Support SLA Reference

| Tier | Severity | Definition | Initial Response SLA |
|---|---|---|---|
| ProSupport Plus | P1 — Production Down | All CGs paused; DR images stale; data loss imminent; failover blocked | < 2 hours (24×7) |
| ProSupport Plus | P2 — Degraded | Lag growing; journal filling; CG active but RPO at risk | < 4 hours (24×7) |
| ProSupport Plus | P3 — Non-Critical | Single CG paused; others healthy; workaround available | Next business day |
| ProSupport Plus | P4 — General | How-to, design review, upgrade planning | Next business day |
| ProSupport | P1 | As above | < 4 hours (24×7) |

---

## See also

- [RecoverPoint — Diagnostics](diagnostics/)
- [RecoverPoint — Common Issues](common-issues/)

---

## Verify resolution

- RecoverPoint Management Console: all CGs show Active Replicating state
- Replication lag for each CG is below the RPO target (typically < 30 seconds for CDP)
- Journal utilization is below 80% for all CGs
- WAN links between Site A and Site B show Connected with normal bandwidth utilization
- Run `get cg_state` on each RPA and confirm all CGs show Active
- Run `get journal_state` and confirm journal fill levels are decreasing or stable below threshold
- Create a test bookmark in the RP console and confirm image access works for a non-production CG
- Monitor CG state and lag for 15 minutes to confirm no CGs pause again
