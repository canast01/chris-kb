---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# SRDF/S — Escalation

<div class="kb-summary">
How to escalate Dell SRDF/S (Symmetrix Remote Data Facility Synchronous) replication issues to Dell Technologies support: what data to collect, how to capture symrdf diagnostics, step-by-step case creation on dell.com/support, and the escalation path when progress stalls.

*Applies to: SRDF/S (Metro) on PowerMax 2500 / 8500 running PowerMaxOS 10.x*
</div>
![SRDF/S — Escalation](../../../../assets/storage-dell-srdf-s-troubleshooting-escalation.svg)




---

## Before you begin

- **Access required:** Solutions Enabler (symcli) on a host with connectivity to both the R1 (production) and R2 (DR) PowerMax arrays; Unisphere access for both arrays; Dell support account at dell.com/support linked to both array serial numbers
- **Both arrays required:** SRDF/S issues always require data from both R1 and R2 — `symrdf` output and `symevent` must be captured from both SIDs
- **Do NOT run `symrdf failover`** without Dell direction — SRDF/S failover makes R2 read-write; the critical question is whether R1 and R2 were in sync at the moment of failure; this must be confirmed before any failover
- **Do NOT use `--force` flags** on symrdf commands — force flags on SRDF/S bypass synchronization checks and can leave the pair in an inconsistent state that cannot be restored without a full resync

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| Production SID | `symcfg list` | Note 12-digit Symmetrix ID for R1 array |
| DR SID | `symcfg list` (on DR-side SE host or same host if registered) | Note 12-digit Symmetrix ID for R2 array |
| SRDF group states | `symdf list -sid <R1-SID>` | All groups in Synchronized state |
| SRDF pair state | `symrdf query -g <group>` | Pair state: Synchronized; R1: Ready; R2: WriteDisabled |
| RDF director ports | `symcfg -sid <SID> list -ra all` | All RDF directors Online |
| Host I/O state | Application and OS I/O error logs | No SCSI or FC errors on production hosts |
| Link latency | Unisphere → SRDF → Performance | Link latency within expected range (typically < 1 ms) |
| Recent events | `symevent -sid <SID> list -last 100` | No SRDF FAULT or CRITICAL events |

---

## Step-by-Step Data Collection

### 1. Get array serial numbers and Solutions Enabler version

```bash
# On the Solutions Enabler host

# All registered arrays (should show both R1 and R2 SIDs)
symcfg list

# Solutions Enabler version
symcli -version

# Microcode version on R1 and R2
symcfg -sid <R1-SID> show | grep -i microcode
symcfg -sid <R2-SID> show | grep -i microcode
```

### 2. Capture SRDF group and pair state from both arrays

```bash
# All SRDF groups on R1
symdf list -sid <R1-SID> > /tmp/srdf-s-groups-$(date +%Y%m%d%H%M).txt

# All SRDF groups on R2 (should mirror R1)
symdf list -sid <R2-SID> >> /tmp/srdf-s-groups-$(date +%Y%m%d%H%M).txt

# Detailed pair state for each affected SRDF group
symrdf query -g <group-number> -v > /tmp/srdf-s-detail-$(date +%Y%m%d%H%M).txt

# Check for Partitioned state specifically
symrdf query -g <group-number> -v | grep -iE "Synchronized|Partitioned|Consistent|Invalid|pair state"
```

### 3. Capture RDF director and link state

```bash
# RDF directors on R1
symcfg -sid <R1-SID> list -ra all > /tmp/srdf-s-rdf-$(date +%Y%m%d).txt

# RDF directors on R2
symcfg -sid <R2-SID> list -ra all >> /tmp/srdf-s-rdf-$(date +%Y%m%d).txt

# RDF port-level details
symcfg -sid <R1-SID> list -ra all -v | grep -iE "port|status|online|offline"

# SRDF link bandwidth and latency (Unisphere alternative)
symrdf -sid <R1-SID> -g <group-number> perf summary
```

### 4. Capture event log from both arrays

```bash
# Last 500 events from R1 (production)
symevent -sid <R1-SID> list -last 500 > /tmp/srdf-s-events-r1-$(date +%Y%m%d).txt

# Last 500 events from R2 (DR)
symevent -sid <R2-SID> list -last 500 > /tmp/srdf-s-events-r2-$(date +%Y%m%d).txt

# Filter for SRDF events
grep -iE "SRDF|RDF|partition|fault|link" /tmp/srdf-s-events-r1-$(date +%Y%m%d).txt | head -50
```

### 5. Write the timeline

```text
R1 array: PowerMax 8500, SID: 000XXXXXXXXXX (production, Site A — primary data center)
R2 array: PowerMax 2500, SID: 000YYYYYYYYYY (DR, Site B — DR site; 50 km apart)
PowerMaxOS: 10.1.0.2 (both)
Solutions Enabler: 10.1.0.18
SRDF configuration: SRDF/S synchronous (zero RPO); 1 RDF group (Group 5: 400 devices)
Link: Dark fiber 10 Gbps; normal latency 0.3 ms round-trip
Host connectivity: 48 production hosts connected to R1 via FC
Issue first observed: 2026-06-15 11:30 UTC
Last confirmed Synchronized state: 2026-06-15 11:25 UTC
Changes in 24h before the issue:
  - 11:25: Network team patched fiber amplifier on the dark fiber link
  - 11:30: symdf list: Group 5 transitions to "Partitioned" state
  - 11:32: Production hosts: SCSI I/O latency increase from 0.4 ms to 45 ms (SRDF/S holding writes)
  - 11:35: SRDF Adaptive Copy NOT enabled; hosts now queueing I/O; some applications timing out
Steps already taken:
  - Did NOT run symrdf failover
  - Did NOT enable Adaptive Copy
  - Fiber team: investigating if amplifier patch caused link instability
  - symrdf query -g 5: Pair state = Partitioned; R1 = Ready; R2 = WriteDisabled
Blast radius: 48 production hosts experiencing I/O delays (holding writes pending R2 ACK); applications queuing
```

---

## How to Open the Case on dell.com/support

1. Go to **dell.com/support** and sign in with your Dell account.

2. Click **My Cases** → **Create New Case**.

3. Under **Product**, enter the R1 (production) array serial number. Select **Dell PowerMax** as the product family.

4. Under **Severity**, select:
   - **Severity 1 — Production Down**: SRDF/S link failure has stopped host I/O (writes queueing indefinitely); Partitioned state with no automatic recovery; I/O timeouts causing application outages; failover required but blocked
   - **Severity 2 — Degraded**: SRDF/S in Partitioned state but Adaptive Copy is buffering writes; link is intermittent; latency has increased but I/O has not stopped; failover not yet required
   - **Severity 3 — Non-Critical**: SRDF/S degraded to a lower performance mode but synchronized; specific device group has a pair state warning; workaround available
   - **Severity 4 — General**: How-to, link sizing, Metro architecture planning, cycle time tuning

5. In the **Summary** field: symptom + impact. Example: `PowerMax 8500 SRDF/S Metro — Group 5 Partitioned since 11:30 UTC, 48 production hosts experiencing I/O latency, applications queuing`.

6. In the **Description** field, paste:
   - R1 and R2 SIDs and PowerMaxOS versions from Step 1
   - `symdf list` output from Step 2
   - `symrdf query` pair state detail from Step 2
   - RDF director states from Step 3
   - The event log SRDF entries from Step 4
   - The timeline from Step 5

7. Under **Attachments**, upload:
   - `srdf-s-groups-*.txt` and `srdf-s-detail-*.txt` from Steps 1 and 2
   - `srdf-s-rdf-*.txt` from Step 3
   - `srdf-s-events-r1-*.txt` and `srdf-s-events-r2-*.txt` from Step 4

8. Click **Submit**. You receive a case number immediately.

9. **Severity 1 only:** call Dell support after submission:
    - North America: +1 800 945 3355 (24×7 for production-down)
    - State "Severity 1 — SRDF/S Partitioned, host I/O queuing, applications timing out, case XXXXXXXX" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at dell.com/support with symrdf output + event logs from both arrays
         ↓
Step 2 — Dell T1 engineer acknowledges (P1: < 2 hr ProSupport Plus; P2: < 4 hr)
         ↓
Step 3 — If no meaningful progress within 1 hour for P1 (I/O impacting applications):
         → Reply: "Requesting escalation to PowerMax SRDF/S Senior Engineer"
         → State: "[Partitioned state / I/O queuing / host latency / link failure]"
         ↓
Step 4 — PowerMax T2 Senior Engineer assigned
         → SRDF/S P1s are urgent — T2 may request immediate remote session via SRS-VE
         → Have Solutions Enabler host, Unisphere, and fiber/network team contact ready
         ↓
Step 5 — If issue requires deciding between Adaptive Copy, failover, or link restore:
         → Dell will provide explicit command sequence and risk assessment for each option
         → Do not make this decision independently
         ↓
Step 6 — For P1 with I/O stopped > 30 minutes:
         → Request TAM engagement immediately
         → TAM to arrange engineering bridge and coordinate failover decision if link cannot be restored
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Run `symrdf failover` without Dell confirming R2 pair consistency | SRDF/S failover makes R2 read-write; if the link failed mid-write, R2 may have inconsistent data from the last write that was not fully committed | Let Dell confirm whether the last write cycle at the moment of failure was complete before any failover |
| Enable Adaptive Copy without Dell direction | Adaptive Copy allows writes to continue to R1 without waiting for R2; this extends the data gap and changes the RPO exposure; the correct response depends on the business decision | Confirm with Dell and the business whether extending the data gap is acceptable before enabling Adaptive Copy |
| Use `--force` on symrdf commands | Force flags bypass SRDF/S write-ordering and consistency checks; on a Partitioned group, a forced operation can permanently diverge R1 and R2 | Only use force on Dell's explicit instruction |
| Modify host masking views or disconnect hosts during the incident | Changing host access during an SRDF/S Partitioned state changes the I/O state Dell is trying to diagnose | Freeze all host-side changes until Dell confirms the SRDF state is understood |
| Pull or replace the RDF director HBA before Dell confirms it as the faulty component | Pulling the wrong component can extend the outage | Let Dell review the RDF director logs before any hardware change |
| Start a PowerMax microcode upgrade during the incident | Microcode upgrades on a PowerMax with a Partitioned SRDF/S group are blocked and will fail; attempting an upgrade will add a new error state | Wait for SRDF/S to return to Synchronized before any upgrade |

---

## Useful Commands for Case Updates

```bash
# Run on Solutions Enabler host — paste into every case update

# SRDF group states
symdf list -sid <R1-SID>

# Pair state detail for affected group
symrdf query -g <group-number> -v | grep -iE "pair state|R1 state|R2 state|synchronized|partitioned"

# RDF director states
symcfg -sid <R1-SID> list -ra all | grep -E "ONLINE|OFFLINE"
symcfg -sid <R2-SID> list -ra all | grep -E "ONLINE|OFFLINE"

# Recent SRDF events (last 20)
symevent -sid <R1-SID> list -last 20 | grep -iE "SRDF|RDF|partition|fault"
```

---

## Support SLA Reference

| Tier | Severity | Definition | Initial Response SLA |
|---|---|---|---|
| ProSupport Plus | P1 — Production Down | SRDF/S Partitioned; I/O stopped or queuing; host application outage | < 2 hours (24×7) |
| ProSupport Plus | P2 — Degraded | Partitioned with Adaptive Copy; latency elevated; RPO exposure growing | < 4 hours (24×7) |
| ProSupport Plus | P3 — Non-Critical | Performance degraded but synchronized; pair state warning on subset | Next business day |
| ProSupport Plus | P4 — General | How-to, link sizing, Metro architecture planning | Next business day |
| ProSupport | P1 | As above | < 4 hours (24×7) |

---

## See also

- [SRDF/S — Diagnostics](diagnostics/)
- [SRDF/S — Common Issues](common-issues/)

---

## Verify resolution

- Run `symdf list -sid <R1-SID>` and confirm all SRDF groups show Synchronized state
- Run `symrdf query -g <group>` for each group and confirm R1 = Ready, R2 = WriteDisabled, pair state = Synchronized
- Confirm host I/O latency has returned to baseline: check application logs and Unisphere performance metrics
- Run `symcfg -sid <SID> list -ra all` on both arrays and confirm all RDF directors are Online
- Run `symevent -sid <R1-SID> list -last 50` and confirm no new SRDF FAULT or CRITICAL events
- Monitor SRDF/S pair state for 15 minutes to confirm the groups remain in Synchronized state and do not transition to Partitioned again
