---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# PowerMax — Escalation

<div class="kb-summary">
How to escalate Dell PowerMax issues to Dell Technologies support: what data to collect, how to run symcfg diagnostics and collect the Solutions Enabler bundle, step-by-step case creation on dell.com/support, and the escalation path when progress stalls.

*Applies to: PowerMax 2500 / 8500 running PowerMaxOS 10.x*
</div>
![PowerMax — Escalation](../../../../assets/storage-dell-powermax-troubleshooting-escalation.svg)




---

## Before you begin

- **Access required:** Solutions Enabler (symcli) on a host connected to the PowerMax; Unisphere access (admin credentials); Dell support account at dell.com/support linked to the array serial number; SRS-VE deployed and registered for remote Dell access
- **SupportAssist auto-cases:** PowerMax monitors itself via SupportAssist (Unisphere → Connectivity → SupportAssist) and can auto-open Dell cases for hardware faults. Check dell.com/support → My Cases before creating a duplicate
- **Do NOT failover SRDF** (symrdf failover or symrdf establish in the wrong direction) without Dell direction — an incorrect failover breaks the replication relationship and may require a full resync, causing extended RPO exposure
- **Do NOT use --force flags** on symcli commands without Dell direction — force flags on replication or storage group commands bypass safety checks and can cause data corruption

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| Array serial (SID) | `symcfg list` | Note the 12-digit Symmetrix ID |
| Array health | `symcfg -sid <SID> show` | No directors in OFFLINE state |
| Director status | `symcfg -sid <SID> list -dir all` | All directors Online |
| Drive health | `sympd list -sid <SID>` | No drives in FAILED or DEAD state |
| SRDF state | `symdf list -sid <SID>` | All groups in SYNCHRONIZED or CONSISTENT state |
| Active alerts | Unisphere → Alerts | No critical (red) alerts |
| SupportAssist | Unisphere → Connectivity → SupportAssist | Enabled; last call-home successful |
| Unisphere accessibility | Browse to `https://<unisphere-ip>:8443/univmax` | Login page loads |

---

## Step-by-Step Data Collection

### 1. Get the array serial number and microcode version

```bash
# On a host with Solutions Enabler installed (symcli in PATH)

# List all registered arrays — note the 12-digit Symmetrix ID (SID)
symcfg list

# Full array health and microcode version
symcfg -sid <SID> show > /tmp/pmx-health-$(date +%Y%m%d%H%M).txt

# Solutions Enabler version
symcli -version >> /tmp/pmx-health-$(date +%Y%m%d%H%M).txt
```

### 2. Capture director and port status

```bash
# All directors with their health state
symcfg -sid <SID> list -dir all > /tmp/pmx-directors-$(date +%Y%m%d).txt

# Front-end director port status (host-facing)
symcfg -sid <SID> list -fa all >> /tmp/pmx-directors-$(date +%Y%m%d).txt

# Back-end director port status (drive-facing)
symcfg -sid <SID> list -da all >> /tmp/pmx-directors-$(date +%Y%m%d).txt
```

### 3. Capture drive health

```bash
# All physical drives and their state
sympd list -sid <SID> > /tmp/pmx-drives-$(date +%Y%m%d).txt

# Drives in FAILED or DEAD state only
sympd list -sid <SID> | grep -E "FAILED|DEAD|REPLACING" >> /tmp/pmx-drives-$(date +%Y%m%d).txt
```

### 4. Capture SRDF replication state (if SRDF is in use)

```bash
# All SRDF groups and their state
symdf list -sid <SID> > /tmp/pmx-srdf-$(date +%Y%m%d).txt

# Detailed state of a specific SRDF group
symrdf -sid <SID> -rdfg <rdfg-number> query >> /tmp/pmx-srdf-$(date +%Y%m%d).txt

# RDF director status
symcfg -sid <SID> list -ra all >> /tmp/pmx-srdf-$(date +%Y%m%d).txt
```

### 5. Collect the event log

```bash
# Last 500 array events (faults, alerts, configuration changes)
symevent -sid <SID> list -last 500 > /tmp/pmx-events-$(date +%Y%m%d).txt

# Filter for alerts and faults
symevent -sid <SID> list -last 500 | grep -iE "FAULT|ALERT|FAILED|CRITICAL" >> /tmp/pmx-events-$(date +%Y%m%d).txt
```

### 6. Write the timeline

```text
Array: PowerMax 8500 SID: 000XXXXXXXXXX
PowerMaxOS: 10.1.0.2
Solutions Enabler: 10.1.0.18
Unisphere: 10.1.0.2
Hosts connected: 24 (FC multipath via 4 FE directors)
SRDF: 3 RDF groups to DR site (async, RPO 30s)
Issue first observed: 2026-06-15 08:00 UTC
Last confirmed healthy: 2026-06-15 06:00 UTC
Changes in 24h before the issue:
  - 06:00: Planned drive capacity expansion: 4 x 7.68 TB NVMe drives added to DA-2C
  - 08:00: Unisphere alert: "Director FA-3D OFFLINE"
  - 08:05: 6 host paths to FA-3D ports went dead; multipath reduced from 4 to 2 paths per LUN
SupportAssist: Auto-case created (Dell case XXXXXXXX) at 08:01
Steps already taken:
  - Did NOT failover SRDF
  - Did NOT modify storage groups or masking views
  - symcfg -sid list -dir all: FA-3D shows OFFLINE; all other directors Online
Blast radius: 6 hosts have reduced path count; I/O is continuing via remaining paths; no outage yet
```

---

## How to Open the Case on dell.com/support

1. Go to **dell.com/support** and sign in with your Dell account.

2. Click **My Cases** → **Create New Case**.

3. Under **Product**, enter the array serial number. Dell identifies the PowerMax by the 12-digit Symmetrix ID.

4. Under **Severity**, select:
   - **Severity 1 — Production Down**: I/O has stopped to production hosts; a director is offline and no redundant path exists; SRDF has broken and DR site is out of sync with no valid recovery point; data loss is imminent; no workaround
   - **Severity 2 — Degraded**: A director is offline but multipath is maintaining I/O via remaining paths; SRDF is suspended but data is consistent; drive rebuild is in progress after a failure; workaround is partial
   - **Severity 3 — Non-Critical**: A drive is in a REPLACING state but RAID is protecting data; a specific Unisphere feature is broken; workaround exists
   - **Severity 4 — General**: How-to, capacity planning, upgrade planning, SRDF configuration review

5. In the **Summary** field: symptom + scope. Example: `PowerMax 8500 SID 000XXXXXXXXXX — FA-3D director offline since 08:00 UTC, 6 hosts reduced to 2 paths per LUN`.

6. In the **Description** field, paste:
   - Array SID and PowerMaxOS version from Step 1
   - Director status output from Step 2
   - SRDF state from Step 4 (if relevant)
   - The last 20 lines of the event log from Step 5
   - The timeline from Step 6
   - Any SupportAssist auto-case number if one was created

7. Under **Attachments**, upload:
   - The `pmx-health-*.txt` file from Step 1
   - The `pmx-directors-*.txt` file from Step 2
   - The `pmx-drives-*.txt` file from Step 3
   - The `pmx-events-*.txt` file from Step 5

8. Click **Submit**. You receive a case number immediately.

9. **Severity 1 only:** call Dell support after submission:
    - North America: +1 800 945 3355 (24×7 for production-down)
    - Reference the case number and state "Severity 1 — PowerMax director offline, host I/O at risk" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at dell.com/support with symcfg snapshot + event log attached
         ↓
Step 2 — Dell T1 engineer acknowledges (P1: < 2 hr ProSupport Plus; P2: < 4 hr)
         ↓
Step 3 — If no meaningful progress within 2 hours for P1:
         → Reply in case: "Requesting escalation to PowerMax Senior Engineer"
         → State: "[director offline / I/O stopped / SRDF broken / drive failure]"
         ↓
Step 4 — PowerMax T2 Senior Engineer assigned
         → They will review the symcfg data and may initiate an SRS remote session
         → Confirm SRS-VE is deployed and Dell can connect via it
         → Have Solutions Enabler host access and Unisphere admin credentials ready
         ↓
Step 5 — If issue requires microcode-level investigation or director replacement:
         → Dell dispatches a field engineer for hardware work
         → Provide data center access details (site, cage, rack, unit)
         ↓
Step 6 — For prolonged P1 or SRDF failover decision:
         → Request TAM engagement
         → TAM can arrange engineering bridge and accelerate hardware dispatch
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Failover SRDF without Dell approval | An incorrect failover breaks the replication relationship; resync from DR to primary can take hours and extends RPO exposure | Let Dell assess the SRDF state and confirm the failover direction before any symrdf failover command |
| Modify storage groups or masking views during the incident | Changes to host access during an I/O issue can cause hosts to lose access to their remaining paths | Freeze all storage group and masking view changes until Dell confirms it is safe to proceed |
| Use symcli --force flags without Dell direction | Force flags bypass safety checks and can cause data corruption or invalid SRDF state changes | Only use --force when Dell explicitly instructs and provides the exact command |
| Start a microcode upgrade during an active incident | Microcode upgrades on an array with a faulted director can make the array state unrecoverable | Wait until the director fault is resolved and the array is fully healthy before any upgrade |
| Disable SupportAssist during the case | SupportAssist provides Dell with real-time array telemetry that speeds diagnosis | Keep SupportAssist enabled; the auto-collected data is used by the T2 engineer |
| Remove or replace drives without Dell confirmation | Removing the wrong drive in a RAID-protected group can cause a second fault and potential data loss | Dell will identify the correct replacement drive and dispatch it; only replace after Dell confirms |

---

## Useful Commands for Case Updates

```bash
# Run on a host with Solutions Enabler (symcli) — paste into every case update

# Array health (quick summary)
symcfg -sid <SID> show | grep -E "Microcode|Status|Cache"

# Director states (look for OFFLINE)
symcfg -sid <SID> list -dir all | grep -E "ONLINE|OFFLINE"

# Drive states (look for FAILED/DEAD)
sympd list -sid <SID> | grep -v "Ready" | head -30

# SRDF state (look for Suspended or Invalid)
symdf list -sid <SID>

# Recent events (last 20)
symevent -sid <SID> list -last 20
```

---

## Support SLA Reference

| Tier | Severity | Definition | Initial Response SLA |
|---|---|---|---|
| ProSupport Plus | P1 — Production Down | I/O stopped; director offline; SRDF broken; data at risk | < 2 hours (24×7) |
| ProSupport Plus | P2 — Degraded | Director offline with multipath protecting I/O; SRDF suspended; drive rebuilding | < 4 hours (24×7) |
| ProSupport Plus | P3 — Non-Critical | Drive in REPLACING (protected); specific feature broken; workaround exists | Next business day |
| ProSupport Plus | P4 — General | How-to, planning, SRDF configuration review | Next business day |
| ProSupport | P1 | As above | < 4 hours (24×7) |

---

## See also

- [PowerMax — Diagnostics](diagnostics/)
- [PowerMax — Common Issues](common-issues/)

---

## Verify resolution

- Run `symcfg -sid <SID> show` and confirm no directors are in OFFLINE state
- Run `symcfg -sid <SID> list -dir all` and confirm all FE, BE, and RDF directors are Online
- Run `sympd list -sid <SID>` and confirm no drives are in FAILED or DEAD state
- Run `symdf list -sid <SID>` and confirm all SRDF groups are in SYNCHRONIZED or CONSISTENT state
- Verify on affected hosts that all expected storage paths are active (multipath tool, `mpath`, or `esxcli storage nmp path list`)
- Confirm host I/O is healthy by checking application logs and storage performance metrics in Unisphere
- Monitor Unisphere Alerts for 15 minutes to confirm no new critical alerts appear
