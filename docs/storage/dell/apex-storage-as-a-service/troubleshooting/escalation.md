---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# APEX Storage as a Service — Escalation

<div class="kb-summary">
Dell APEX Storage-as-a-Service escalation: how to collect multipath, SCG, and CloudIQ diagnostics, open a support case via the APEX Console or Dell support portal, set severity, and follow the escalation path for storage outages and SLA-impacting events.

*Applies to: APEX Storage-as-a-Service*
</div>

```text
┌──────────────────────────────────── Dell Apex STaaS — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Apex escalation: severity triage, SR creation, log collection, TAC engagement         │   │
│   │           P1 (production down): call Dell immediately + open SR; 4-hour response SLA          │   │
│   │       P2 (degraded): open SR online; 8-hour response; attach multipath and CloudIQ logs       │   │
│   │             Collect before calling: host OS logs, CloudIQ bundle, SCG diagnostics             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Severity and What to Collect       │  │             APEX SR Process                 │   │
│   │       P1: prod down → multipath + dmesg      │  │     APEX Console → Support → New Case       │   │
│   │       P2: degraded → CloudIQ bundle          │  │     OR: support.dell.com → Create SR        │   │
│   │       P3: limited  → iSCSI/FC event log      │  │     Attach CloudIQ + SCG bundle             │   │
│   │       P4: question → usage metrics export    │  │     For P1: call after opening portal SR    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: collect cable/SFP photos for P1 hardware failures · note rack and port labels            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    APEX STaaS     = Dell APEX Storage-as-a-Service; consumption-based storage managed by Dell         │
│    SCG            = Secure Connect Gateway; on-premises gateway for remote support and telemetry      │
│    CloudIQ bundle = Downloadable diagnostic package from CloudIQ portal; attach to SR                 │
│    multipath -ll  = Linux multipath topology; shows which paths to the array are active               │
│    dmesg          = Linux kernel ring buffer; shows SCSI errors and path failover events              │
│    RCA            = Root Cause Analysis; Dell provides written cause and prevention plan for P1/P2    │
│    APEX Console   = Dell APEX management portal; used to open support cases for STaaS                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Storage admin credentials (for the array management interface); APEX Console admin role; Dell support portal account with ProSupport Plus contract linked to the APEX STaaS agreement
- **Gather first:** affected volume names, host names, error messages from the host OS, and whether the issue is a connectivity failure, performance degradation, or a capacity/billing concern
- **Scope:** confirm whether the issue affects a single host, all hosts in a cluster, or all volumes in the APEX STaaS pool
- **Dell responsibility:** under APEX STaaS, Dell is responsible for infrastructure remediation. For hardware failures, drive replacements, and firmware updates, Dell dispatches a field engineer. Your role is to provide host-side diagnostics and coordinate access

---

## Severity Levels

| Severity | Criteria | Response SLA | Contact |
|---|---|---|---|
| P1 — Critical | Production storage completely unavailable; all hosts I/O blocked; no paths to array | 4 hours (24×7) | Open SR via APEX Console + call Dell support phone |
| P2 — Major | Degraded: one path lost; slow I/O; some volumes inaccessible; workaround in place | 8 hours (24×7) | Open SR online |
| P3 — Limited | Non-production issue; isolated volume; performance below expectations but data accessible | Next business day | Open SR online |
| P4 — General | Billing query; usage report; capacity forecast; feature question | Best effort | APEX Console + Dell account team |

## Pre-Escalation Triage Checklist

| Check | Command | Expected |
|---|---|---|
| Multipath paths available | `multipath -ll` (Linux) | At least one path per volume `active ready` |
| SCSI errors in kernel log | `dmesg \| grep -i "scsi\|sd\|i2o"` | No `I/O error` or `path failure` messages |
| iSCSI sessions established (if iSCSI) | `iscsiadm -m session` | Sessions for all target IPs |
| FC HBA ports online (if FC) | `cat /sys/class/fc_host/host*/port_state` | `Online` for all HBA ports |
| Array management accessible | Browse to array management IP | Login page loads |
| SCG connected | SCG web UI → Status | Service: Running; Connection: Connected |
| CloudIQ data current | CloudIQ → Monitoring | Last data < 15 min ago |
| APEX Console status | APEX Console → Subscriptions → <your subscription> | Status: Active |

---

## Step-by-Step Data Collection

### 1. Collect host-side storage diagnostics (Linux)

```bash
# Multipath topology — shows all paths and their current state
multipath -ll 2>&1 | tee /tmp/multipath-$(date +%F-%H%M%S).txt

# kernel SCSI errors and path events (last 500 lines)
dmesg | grep -iE "scsi|sd[a-z]|dm-|path|i2o|fail|error|reset" | tail -500 \
  > /tmp/dmesg-storage-$(date +%F-%H%M%S).txt

# System log for SCSI / storage events
grep -E "scsi|multipathd|iscsid|fcoe|HBA" /var/log/syslog | tail -200 \
  > /tmp/syslog-storage-$(date +%F-%H%M%S).txt

# iSCSI session details (if iSCSI)
iscsiadm -m session -P 3 2>&1 > /tmp/iscsi-sessions.txt

# FC HBA state (if FC)
for hba in /sys/class/fc_host/host*; do
  echo "=== $hba ==="
  cat $hba/port_name $hba/port_state $hba/speed 2>/dev/null
done > /tmp/fc-hba-state.txt

# Disk error count from SMART (if accessible)
for disk in /dev/sd*; do
  smartctl -A $disk 2>/dev/null | grep -E "Reallocated|Uncorrectable|Pending" \
    && echo "Checked: $disk"
done > /tmp/smart-errors.txt
```

### 2. Collect host-side diagnostics (Windows)

```powershell
# Multipath status
mpclaim -s -d | Out-File C:\Temp\mpclaim-$(Get-Date -Format yyyyMMdd-HHmmss).txt

# Disk management state
Get-Disk | Select-Object Number, FriendlyName, OperationalStatus, HealthStatus | \
  Export-Csv C:\Temp\disks.csv -NoTypeInformation

# Event log for disk errors (last 4 hours)
$start = (Get-Date).AddHours(-4)
Get-WinEvent -LogName System -StartTime $start |
  Where-Object { $_.Id -in 7,11,15,51,52 -and $_.ProviderName -like "*Disk*" } |
  Select-Object TimeCreated, Id, Message | Export-Csv C:\Temp\disk-events.csv -NoTypeInformation

# iSCSI sessions (if iSCSI)
Get-IscsiSession | Format-List | Out-File C:\Temp\iscsi-sessions.txt
```

### 3. Collect SCG and CloudIQ diagnostics

```bash
# SCG log bundle (SSH to SCG appliance)
ssh admin@<scg-hostname>
scg logs collect --output /tmp/scg-logs-$(date +%F).zip
# OR: SCG web UI → Admin → Support Bundle → Download

# CloudIQ diagnostic bundle
# Navigate to: CloudIQ → Monitoring → select the affected system → Actions → Download Diagnostics
# Save as: cloudiq-diagnostics-<system-name>-<date>.zip

# APEX Console events
# Navigate to: APEX Console → Subscriptions → <your subscription> → Events
# Export the last 7 days of events as CSV
```

### 4. Write the timeline

```text
APEX STaaS subscription: APEX-SUB-12345 (from APEX Console)
Affected storage system: PowerStore 1000T SN: PST00xxxxxxxx
SCG version: 5.18.0.1

Affected hosts:
  - linux-host-01.corp.local (RHEL 8.6) — 4 volumes
  - linux-host-02.corp.local (RHEL 8.6) — 4 volumes

Issue first observed: 2026-06-15 06:00 UTC
Last known good I/O: 2026-06-15 05:45 UTC

Error observed:
  - multipath -ll shows all paths "faulty" for dm-2 and dm-3 (volumes prod-vol-01 and prod-vol-02)
  - dmesg shows: "sd 2:0:0:0: [sdb] tag#0 FAILED Result: hostbyte=DID_NO_CONNECT driverbyte=DRIVER_OK"
  - CloudIQ shows port NAS-A offline since 06:02 UTC

Steps already taken:
  - Verified SFP cables seated on both host HBAs
  - Confirmed array management IP reachable from host
  - Confirmed iSCSI target IP reachable (ping OK; iSCSI login failing)

Changes in prior 24h:
  - No host changes
  - Dell notified us of a scheduled firmware update window — update was applied at 05:30 UTC

Blast radius:
  - 2 volumes inaccessible to 2 production hosts
  - Database on prod-vol-01 offline
```

---

## How to Open an APEX Support Case

**Via APEX Console** (preferred for STaaS issues):

1. Sign in to **apex.dell.com** and navigate to **Subscriptions** → your STaaS subscription.
2. Click **Create Support Request** (top right of the subscription page).
3. Select the affected storage system and issue category.
4. Under **Severity**, select P1 for production I/O blocked, P2 for degraded.
5. Paste the timeline and host diagnostic summary.
6. Upload attachments: multipath output, dmesg, SCG logs, CloudIQ diagnostics.

**Via support.dell.com** (if APEX Console is unavailable):

1. Go to **support.dell.com** and sign in.
2. Click **Create Service Request** and search for your PowerStore / PowerFlex array by serial number.
3. Under **Category**, select **Storage — Connectivity** or **APEX — STaaS SLA**.
4. Complete the description with the timeline and host diagnostics.

5. **For P1:** On the case confirmation page, use the phone number shown for your region. Call immediately — do not wait for email response. Tell the agent: "This is a P1 APEX STaaS production outage; case number [case-id]".

---

## Escalation Path

```text
Step 1 — Open P1 SR via APEX Console or support.dell.com with multipath + SCG logs
         ↓
Step 2 — For P1: call Dell support phone immediately after opening the portal SR
         (number on case confirmation page; 24×7 for P1)
         ↓
Step 3 — Dell T1 reviews case and determines whether issue is host-side or infrastructure-side
         → Host-side: Dell guides host reconfiguration (HBA, iSCSI, multipath settings)
         → Infrastructure-side: Dell dispatches hardware engineer for on-site remediation
         ↓
Step 4 — If no meaningful progress in 4 hours for P1 / 8 hours for P2:
         → Add case update: "Requesting escalation — production storage offline since [time]"
         → Contact your Dell account team to escalate to TAC manager
         ↓
Step 5 — For P1 unresolved > 4 hours:
         → Request executive escalation through Dell account team
         → Provide business impact: affected hosts, databases/applications offline, revenue impact
         ↓
Step 6 — After resolution: request a written RCA (Root Cause Analysis) from Dell
         → RCA is standard for P1 events under ProSupport Plus
         → RCA should include root cause, timeline, corrective action, and preventive measures
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Remove and re-add failed multipath devices on the host before Dell diagnosis | Removes the evidence needed to identify whether the failure was I/O path, fabric, or array-side | Keep the failed paths in multipath; capture `multipath -ll` before any changes |
| Reboot the affected hosts before collecting dmesg | dmesg output is lost on reboot | Save dmesg to a file first; reboot only after collection is complete or with Dell guidance |
| Perform any firmware or driver updates on production hosts during the incident | Adds variables; can mask the root cause | Freeze all host changes during P1; communicate with Dell before any host-side action |
| Contact Dell directly on the hardware serial number instead of the APEX subscription | Dell may route to the wrong team (hardware support vs STaaS service team) | Always open cases via APEX Console → your STaaS subscription; reference the subscription ID |

---

## Useful Commands for Case Updates

```bash
# Quick state snapshot — paste into every case update
multipath -ll 2>&1 | head -40
dmesg | grep -i "fail\|error\|path" | tail -20
iscsiadm -m session 2>&1 || echo "Not using iSCSI"

# CloudIQ: get system health via API
TOKEN="<your-cloudiq-api-key>"
curl -sk "https://cloudiq.dell.com/cloudiq/api/v1/systems" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
for s in json.load(sys.stdin).get('results', []):
    print(f\"{s['system_name']}: health={s.get('system_health_score')} last_seen={s.get('last_seen_timestamp')}\")
"

# Test connectivity to iSCSI target IP
ping -c 4 <iscsi-target-ip>
nc -zv <iscsi-target-ip> 3260

# Test FC path connectivity
systool -c fc_host -v | grep -E "node_name|port_name|port_state|speed"
```

---

## Verify resolution

- Confirm `multipath -ll` shows all expected paths `active ready` for all volumes
- Verify application can write to the storage: write a small test file to each affected volume
- Check CloudIQ dashboard — system health score returned to expected level; no offline ports
- Monitor host syslog and dmesg for 30 minutes after resolution for any residual path errors
- Request RCA from Dell for any P1 or P2 event (standard under ProSupport Plus)

---

## See also

- [APEX Storage as a Service — Diagnostics](diagnostics/)
- [APEX Storage as a Service — Common Issues](common-issues/)
