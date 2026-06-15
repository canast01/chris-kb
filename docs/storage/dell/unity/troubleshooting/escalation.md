---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# Unity XT — Escalation

<div class="kb-summary">
How to escalate Dell Unity XT issues to Dell Technologies support: what data to collect, how to run uemcli diagnostics and generate the service information bundle, step-by-step case creation on dell.com/support, and the escalation path when progress stalls.

*Applies to: Unity XT 380F / 480F / 680F / 880F running OE 5.x*
</div>

```text
┌──────────────────────────────── Dell Unity XT — Escalation ───────────────────────────────────────────┐
│                                                                                                       │
│  Escalate Unity XT issues to Dell support when a Storage Processor (SP) is offline and the            │
│  array is in single-SP mode, NFS or iSCSI I/O has stopped for production hosts, a drive failure       │
│  has pushed a pool below its protection threshold, or an OE upgrade has failed mid-way through.       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 1 — Collect Data               │  │          Step 2 — Open the Case             │   │
│   │  uemcli /sys/general show (health + version) │  │  Go to dell.com/support → My Cases          │   │
│   │  uemcli /env/health show (component faults)  │  │  Select product by SP serial number         │   │
│   │  uemcli /sys/alert show (active alerts)      │  │  Severity: P1 SP down / P2 degraded         │   │
│   │  Generate service bundle (Unisphere UI)      │  │  Attach service bundle + alert history      │   │
│   │  Write timeline: last healthy → first fault  │  │  For P1: also call Dell support             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  For P1: open portal case AND call Dell immediately.                                                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 3 — Escalation Path            │  │         What NOT to Do                      │   │
│   │  T1: triage + confirm bundle received        │  │  Do not reboot both SPs simultaneously      │   │
│   │  T2: Unity SE assigned; deep array review    │  │  Do not modify pools during single-SP mode  │   │
│   │  TAM: engage for P1 or prolonged issues      │  │  Do not pull drives without Dell guidance   │   │
│   │  GPS: on-site senior engineering for complex │  │  Do not start OE upgrade during incident    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SP-A / SP-B     = Storage Processors; active-active HA pair; one failing = single-SP mode            │
│  OE              = Operating Environment; Unity operating system; version in uemcli /sys/sw show      │
│  uemcli          = Unity CLI; `uemcli -d <sp-ip> -u admin -p <pw> /command` on management host        │
│  pool            = collection of drives forming usable storage capacity; FAST VP tiers data           │
│  FAST VP         = Fully Automated Storage Tiering VP; moves hot/cold data between drive tiers        │
│  NAS server      = virtual file server on Unity; owns IP, DNS, shares; independent per-tenant         │
│  service bundle  = Unity diagnostic archive; generated via Unisphere or uemcli; mandatory             │
│  SupportAssist   = Dell telemetry and auto-case creation; configured in Unisphere                     │
│  ProSupport Plus = Dell highest support tier; 24×7; P1 response < 2 hr                                │
│  TAM             = Technical Account Manager; named Dell contact for critical case escalation         │
│  GPS             = Global Priority Services; senior on-site or remote Dell engineering                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access required:** uemcli on a management host (or direct Unisphere access at `https://<sp-ip>/`); Unisphere admin credentials; Dell support account at dell.com/support linked to the array SP serial numbers
- **Check SupportAssist first:** Unity XT monitors itself and auto-opens cases for hardware faults (SP failure, drive failure, PSU). Check dell.com/support → My Cases before creating a duplicate
- **Do NOT reboot both SPs simultaneously** — with SP-B down, rebooting SP-A removes all array access; always leave at least one SP running
- **Do NOT modify storage pools** during single-SP mode — pool operations require both SPs; attempting pool changes on a single SP can leave the pool in an inconsistent state

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| OE version | `uemcli /sys/sw show` | Note OE version |
| SP serial numbers | Unisphere → Hardware → Storage Processors | Note SP-A and SP-B service tags |
| System health | `uemcli /sys/general show` | `Model`, `Health` fields — note any non-OK health |
| Component health | `uemcli /env/health show -filter "health.value ne OK"` | Empty output (all OK) |
| Active alerts | `uemcli /sys/alert show` | No critical (severity = ERROR or CRITICAL) alerts |
| Pool health | `uemcli /stor/pool show` | All pools in OK health state |
| Drive health | `uemcli /env/disk show -filter "health.value ne OK"` | Empty output (no failed drives) |
| SupportAssist | Unisphere → Settings → Support → SupportAssist | Enabled; test alert last successful |

---

## Step-by-Step Data Collection

### 1. Get the OE version and SP serial numbers

```bash
# Run uemcli from a management host with the CLI installed
# Format: uemcli -d <sp-ip> -u admin -p <password> <command>

# OE version (note full version string including build)
uemcli -d <sp-ip> -u admin -p <password> /sys/sw show

# System info (model, serial, health)
uemcli -d <sp-ip> -u admin -p <password> /sys/general show

# SP serial numbers and health
uemcli -d <sp-ip> -u admin -p <password> /env/sp show
```

### 2. Capture component health and active alerts

```bash
# All components that are NOT in OK health state
uemcli -d <sp-ip> -u admin -p <password> /env/health show \
  -filter "health.value ne OK" > /tmp/unity-health-$(date +%Y%m%d%H%M).txt

# All active alerts
uemcli -d <sp-ip> -u admin -p <password> /sys/alert show \
  > /tmp/unity-alerts-$(date +%Y%m%d%H%M).txt

# Alert history (last 72 hours)
uemcli -d <sp-ip> -u admin -p <password> /sys/alert/hist show \
  >> /tmp/unity-alerts-$(date +%Y%m%d%H%M).txt

# Drive health (look for FAILED or DEGRADED)
uemcli -d <sp-ip> -u admin -p <password> /env/disk show >> /tmp/unity-health-$(date +%Y%m%d%H%M).txt
```

### 3. Capture pool and storage health

```bash
# Pool health and capacity
uemcli -d <sp-ip> -u admin -p <password> /stor/pool show \
  > /tmp/unity-pools-$(date +%Y%m%d).txt

# LUNs with non-OK health (for block issues)
uemcli -d <sp-ip> -u admin -p <password> /stor/prov/luns show \
  -filter "health.value ne OK" >> /tmp/unity-pools-$(date +%Y%m%d).txt

# NAS servers (for NFS/SMB issues)
uemcli -d <sp-ip> -u admin -p <password> /net/nas/server show \
  >> /tmp/unity-pools-$(date +%Y%m%d).txt
```

### 4. Generate the service information bundle

**Via Unisphere UI (preferred):**
1. Log in to `https://<sp-ip>/` and navigate to **Settings → Support → Service Information**.
2. Click **Collect** and wait for the bundle to complete (5–15 minutes).
3. Click **Download** and save the bundle to your workstation.

**Via uemcli (if Unisphere UI is inaccessible):**
```bash
# Trigger service bundle collection
uemcli -d <sp-ip> -u admin -p <password> /sys/serviceinfo collect

# Check status
uemcli -d <sp-ip> -u admin -p <password> /sys/serviceinfo show

# Download when complete (follow the download URL from the status output)
```

### 5. Write the timeline

```text
Unity model: Unity XT 480F
OE version: 5.4.1.0
SP-A serial: XXXXXXXX; SP-B serial: XXXXXXXX
Array management IP: 10.0.10.10
Hosts connected: 16 (8 via FC, 8 via iSCSI)
Protocols: FC LUNs for VMware, iSCSI LUNs for Oracle RAC, NFS for Linux file servers
Issue first observed: 2026-06-15 09:00 UTC
Last confirmed healthy: 2026-06-15 07:00 UTC
Changes in 24h before the issue:
  - 07:00: Drive expansion: 4 x 7.68 TB SSD drives added to Pool-01 via hot-add
  - 09:00: Unisphere alert: "SP-B: Status = Fault"
  - 09:05: SP-B shows as offline; array in single-SP mode (SP-A active)
  - 09:10: iSCSI LUNs on Oracle RAC: path count halved; I/O continuing on remaining paths
SupportAssist: Auto-case created (Dell case XXXXXXXX) at 09:01
Steps already taken:
  - Did NOT reboot SP-A
  - Did NOT modify pools or add drives
  - uemcli /env/sp show: SP-A OK; SP-B FAULT (hardware fault code XXXX)
Blast radius: SP-B offline; all hosts at half path count; I/O continuing on SP-A; full pool ops blocked
```

---

## How to Open the Case on dell.com/support

1. Go to **dell.com/support** and sign in with your Dell account.

2. Click **My Cases** → **Create New Case**.

3. Under **Product**, enter the SP serial number (from Unisphere → Hardware). Dell associates the case with the array hardware by SP service tag.

4. Under **Severity**, select:
   - **Severity 1 — Production Down**: SP-A is offline (array inaccessible); NFS/iSCSI I/O has stopped to production hosts; a pool is in a DEGRADED state with no remaining redundancy; OE upgrade has failed leaving SPs at different versions; no workaround
   - **Severity 2 — Degraded**: SP-B is offline but SP-A is serving I/O in single-SP mode; a drive has failed and the pool is rebuilding but still accessible; NAS server is unreachable but block LUNs are OK; workaround partial
   - **Severity 3 — Non-Critical**: A specific Unisphere feature is broken; a replication session is suspended but data is consistent; pool is rebalancing; workaround exists
   - **Severity 4 — General**: How-to, upgrade planning, capacity review, NAS configuration question

5. In the **Summary** field: symptom + scope. Example: `Unity XT 480F — SP-B offline since 09:00 UTC, array in single-SP mode, iSCSI hosts at 50% path count`.

6. In the **Description** field, paste:
   - OE version and SP serial numbers from Step 1
   - Component health output from Step 2
   - The timeline from Step 5
   - Any SupportAssist auto-case number if one was created

7. Under **Attachments**, upload:
   - The service information bundle from Step 4
   - The health and alert output files from Steps 2 and 3

8. Click **Submit**. You receive a case number immediately.

9. **Severity 1 only:** call Dell support after submission:
    - North America: +1 800 945 3355 (24×7 for production-down)
    - State "Severity 1 — Unity XT SP offline, single-SP mode, production I/O at risk, case XXXXXXXX" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at dell.com/support with service bundle + health + alert output attached
         ↓
Step 2 — Dell T1 engineer acknowledges (P1: < 2 hr ProSupport Plus; P2: < 4 hr)
         ↓
Step 3 — If no meaningful progress within 2 hours for P1:
         → Reply in case: "Requesting escalation to Unity XT Senior Engineer"
         → State: "[SP offline / I/O stopped / pool degraded / OE upgrade failed]"
         ↓
Step 4 — Unity T2 Senior Engineer assigned
         → They will review the service bundle and may request Unisphere or uemcli access
         → Have Unisphere admin credentials and uemcli CLI host access ready
         ↓
Step 5 — If issue requires SP replacement or drive hardware dispatch:
         → Dell dispatches a field engineer with replacement hardware
         → Provide physical access details (data center, rack, unit position)
         ↓
Step 6 — For prolonged P1 or complex OE upgrade recovery:
         → Request TAM engagement (Technical Account Manager)
         → For on-site senior engineering: request Global Priority Services (GPS)
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Reboot SP-A while SP-B is already offline | Rebooting the only healthy SP removes all array access; hosts lose I/O completely | Keep SP-A running; let Dell assess SP-B's fault before any SP restart |
| Modify pool configurations (add drives, expand) during single-SP mode | Pool operations on Unity require both SPs; adding or expanding pools with one SP offline can leave the pool in an inconsistent state | Freeze all pool modifications until both SPs are healthy and Dell confirms it is safe |
| Pull a drive that the array shows as faulted without Dell confirmation | A drive the array shows as faulted may still hold valid data if the SP that manages it is offline; pulling prematurely can cause data loss | Let Dell identify the exact faulted drive via the service bundle before any physical removal |
| Start a Unity OE upgrade during an active incident | Upgrading with a faulted SP or degraded pool can leave SPs at different OE versions, making recovery much harder | Wait for Dell to confirm both SPs are healthy and the pool is fully protected before any upgrade |
| Disable SupportAssist during the case | SupportAssist provides Dell with real-time array telemetry; disabling it cuts off the auto-collected data the T2 engineer uses | Keep SupportAssist enabled; the auto-collected call-home data is used to accelerate diagnosis |
| Create a second case for the same incident | Splits diagnostic history across two cases; slows down T2 assignment | Add all updates to the existing case; only create a new case if Dell explicitly instructs |

---

## Useful Commands for Case Updates

```bash
# Run from management host with uemcli installed — paste into every case update

# System health summary
uemcli -d <sp-ip> -u admin -p <password> /sys/general show

# SP health (look for FAULT or DEGRADED on either SP)
uemcli -d <sp-ip> -u admin -p <password> /env/sp show

# All non-OK components
uemcli -d <sp-ip> -u admin -p <password> /env/health show \
  -filter "health.value ne OK"

# Active alerts
uemcli -d <sp-ip> -u admin -p <password> /sys/alert show

# Pool health
uemcli -d <sp-ip> -u admin -p <password> /stor/pool show
```

---

## Support SLA Reference

| Tier | Severity | Definition | Initial Response SLA |
|---|---|---|---|
| ProSupport Plus | P1 — Production Down | SP offline; I/O stopped; pool degraded below protection threshold | < 2 hours (24×7) |
| ProSupport Plus | P2 — Degraded | Single SP offline; I/O continuing via remaining SP; pool rebuilding | < 4 hours (24×7) |
| ProSupport Plus | P3 — Non-Critical | Specific feature broken; pool rebalancing; replication suspended | Next business day |
| ProSupport Plus | P4 — General | How-to, planning, upgrade review | Next business day |
| ProSupport | P1 | As above | < 4 hours (24×7) |
| ProSupport | P2–P4 | As above | Next business day |

---

## See also

- [Unity — Diagnostics](diagnostics/)
- [Unity — Common Issues](common-issues/)

---

## Verify resolution

- Run `uemcli /env/sp show` and confirm both SP-A and SP-B are in OK health state
- Run `uemcli /env/health show -filter "health.value ne OK"` and confirm empty output (all components OK)
- Run `uemcli /sys/alert show` and confirm no active critical or error alerts
- Run `uemcli /stor/pool show` and confirm all pools are in OK health state with full redundancy
- Verify host path counts are restored to expected levels (multipath tool on each affected host)
- Confirm host I/O is healthy: check application logs and Unisphere performance graphs
- If a drive was replaced: confirm the replacement drive is in READY state and the pool rebuild is complete
- Monitor Unisphere alerts for 15 minutes to confirm no new critical alerts appear
