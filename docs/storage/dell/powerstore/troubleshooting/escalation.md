---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# PowerStore — Escalation

<div class="kb-summary">
How to escalate Dell PowerStore issues to Dell support: what data to collect, how to generate the support bundle, step-by-step case creation on the Dell portal, and the escalation path when progress stalls.

*Applies to: PowerStore 3.x*
</div>
![PowerStore — Escalation](../../../../assets/storage-dell-powerstore-troubleshooting-escalation.svg)




---

## Before you begin

- **Access required:** PowerStore Manager (PSM) admin credentials; Dell account at dell.com/support with ProSupport contract linked to the system service tag
- **Check SupportAssist first:** if SupportAssist is enabled and connected, Dell may have already automatically opened a case for qualifying hardware faults. Check **PSM → Help → My Cases** before opening a duplicate
- **Do NOT reboot a controller** without Dell guidance — in a degraded state a reboot may take the array offline. Dell support will tell you if a reboot is the right action
- **Do NOT replace failed drives** without Dell confirming the replacement sequence — pulling drives in the wrong order from a degraded RAID group can cause data loss

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Where to look | Expected result |
|---|---|---|
| PowerStoreOS version | PSM → Help → About | Note full version string |
| Service tag | PSM → Hardware → Appliance → Properties | 7-char tag e.g. `ABC1234` |
| Active alerts | PSM → Alerts dashboard or REST API | Review all Critical/Major alerts |
| Controller health | PSM → Hardware → Controllers | Both controllers show Online |
| Drive health | PSM → Hardware → Drives | No drives in Failed or Degraded state |
| Appliance health | PSM → Dashboard → Hardware Health | All appliances show Healthy |
| Volume health | PSM → Storage → Volumes | No volumes in Degraded state |
| SupportAssist status | PSM → Settings → Support → SupportAssist | Status: Connected |
| Existing auto-case | PSM → Help → My Cases | Check for Dell-opened case before creating new |

---

## Step-by-Step Data Collection

### 1. Get the PowerStoreOS version and service tag

In PSM: click **Help → About** and note the full PowerStoreOS version string.

Then click **Hardware → Appliance → Properties** to find the service tag. The service tag is required for all Dell support cases. If PSM is unavailable:

```bash
# PowerStore REST API — get the version (authenticated curl)
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/software_installed" \
  -H "Authorization: Basic <base64-user:pass>"

# Get the appliance model and serial number
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/appliance" \
  -H "Authorization: Basic <base64-user:pass>"
```

### 2. Capture all active alerts

```bash
# Get all active alerts via REST API — paste full output into the case description
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/alert?state=active" \
  -H "Authorization: Basic <base64-user:pass>"

# Alternative: PSM → Alerts → filter by Status=Active; Export to CSV
```

### 3. Check hardware health (controller and drive state)

In PSM: click **Hardware → Appliance** and screenshot the hardware topology view showing controller and drive status.

```bash
# REST: check controller health
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/hardware?type=Node" \
  -H "Authorization: Basic <base64-user:pass>"

# REST: check drive health
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/hardware?type=Drive" \
  -H "Authorization: Basic <base64-user:pass>"
```

### 4. Collect the support bundle

The support bundle packages all PSM logs, configuration data, and event history.

1. In PSM: click **Help → Collect Support Materials**.
2. Select the affected appliance(s).
3. Click **Collect** and wait 5–15 minutes for the bundle to be generated.
4. Download the resulting archive when the collection completes.

This archive is the most important attachment for the Dell support case.

If PSM is inaccessible:

```bash
# REST: trigger a support bundle collection
curl -k -X POST "https://<powerstore-mgmt-ip>/api/rest/support_material" \
  -H "Authorization: Basic <base64-user:pass>" \
  -H "Content-Type: application/json" \
  -d '{"appliance_ids": ["<appliance-id>"]}'
```

### 5. Write the timeline

```text
PowerStoreOS version: 3.5.0.0.0.14
Service tag: ABC1234
Appliance model: PowerStore 1200T
Issue first observed: 2026-06-14 14:30 UTC
Last known good state: 2026-06-14 12:00 UTC
Changes in 24h before the issue:
  - 12:00: Firmware update applied via PSM to both controllers
  - 14:30: Alert fired: "Node A hardware fault — node degraded"
  - 14:35: 4 hosts lost I/O access to volumes on this appliance
Steps already taken:
  - Reviewed PSM alerts: 3 Critical alerts for hardware fault on Node A
  - Checked SupportAssist: no automatic case found
  - Did NOT reboot controllers or replace drives
Blast radius: 4 ESXi hosts cannot access storage; 20 VMs have I/O stalled
```

---

## How to Open the SR on www.dell.com/support

1. Go to **www.dell.com/support** and sign in with your Dell account. The account must be linked to a ProSupport or ProSupport Plus contract associated with the system service tag.

2. Click **Get Support** → **Service Requests** → **Create a New Service Request**.

3. Under **Product**, search for **PowerStore** and select your appliance model.

4. Enter the **Service Tag** (7-character code from Step 1). This validates entitlement and links Dell's system database to the case.

5. Under **Problem Type**, select **Hardware** for physical faults or **Software** for PSM, REST API, or data management issues.

6. Under **Severity**, select:
   - **P1 — Critical**: Both controllers unreachable; all hosts have lost storage access; no I/O can proceed; production is down; no workaround
   - **P2 — High**: Single controller degraded; drive failure reducing redundancy; significant I/O performance degradation; Metro or replication broken; production impacted
   - **P3 — Medium**: Non-critical feature affected; alert that has a workaround; one volume unavailable while other volumes remain accessible
   - **P4 — Low**: How-to question, planning, documentation request, or non-urgent configuration review

7. In the **Description** field, paste:
   - PowerStoreOS version and service tag from Step 1
   - Active alerts from Step 2
   - Hardware state from Step 3
   - The timeline from Step 5

8. Under **Attachments**, upload the support bundle from Step 4. If the file is too large for the portal, Dell will provide a secure upload link.

9. Click **Submit**. You will receive a case number by email immediately.

10. **P1 only:** call Dell support immediately after submission:
    - Global: **+1 800 945 3355** (24×7 for ProSupport P1)
    - UK: +44 0800 028 2847
    - Germany: +49 0800 000 3672
    - State "P1 — PowerStore controller degraded / hosts have no storage" at the start of the call.

---

## Escalation Path

```text
Step 1 — Check SupportAssist for auto-opened case; if none, open case at dell.com/support
         ↓
Step 2 — Dell support engineer acknowledges (P1: within 1 hr; P2: within 4 hr)
         ↓
Step 3 — If no meaningful progress in 1 hour for P1 or 4 hours for P2:
         → Reply in case: "Requesting escalation to Senior Engineer / TAM"
         → State: "[hosts have no storage / Node A down / Metro broken]"
         ↓
Step 4 — TAM (Technical Account Manager) assigned for ProSupport Plus contracts
         → TAM escalates to engineering and can expedite hardware dispatch
         → Have PSM and REST API access ready for a remote session
         ↓
Step 5 — If hardware is confirmed failed:
         → Dell initiates hardware dispatch per your ProSupport contract SLA
         → For NBD: next business day; for 4h: parts dispatched within 4 hours
         ↓
Step 6 — For P1 open more than 4 hours with no resolution:
         → Call Dell support and request escalation to the Duty Manager
         → Contact your Dell Account Executive for executive-level escalation
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Reboot a controller without Dell guidance | May cause both nodes to enter a recovery state simultaneously, taking the array offline | Wait for Dell to confirm the exact command and timing for the reboot |
| Replace failed drives without Dell confirmation | Pulling drives in the wrong order from a degraded RAID group can cause unrecoverable data loss | Let Dell provide the replacement procedure and part number |
| Modify volumes or host mappings mid-case | Changes the configuration Dell is analysing; may fix symptoms while masking the root cause | Freeze all storage configuration changes until the case is closed |
| Disable SupportAssist during the case | Severs Dell's telemetry visibility; prevents automatic dispatch of replacement parts | Leave SupportAssist enabled; it accelerates diagnosis and part dispatch |
| Apply a PSM firmware update mid-incident | Changes the PSM software version and log format mid-investigation | Freeze all firmware and software updates until Dell advises |
| Open multiple parallel cases for the same appliance | Splits Dell's diagnostic context; delays assignment | Use one case; add all updates to the same service request |

---

## Useful Commands for Case Updates

```bash
# Active alerts snapshot — paste into every case update
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/alert?state=active" \
  -H "Authorization: Basic <base64-user:pass>"

# Hardware health
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/hardware?type=Node" \
  -H "Authorization: Basic <base64-user:pass>"

# Drive health
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/hardware?type=Drive" \
  -H "Authorization: Basic <base64-user:pass>"

# Recent event log (last 50 events)
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/event?order=created_timestamp%20desc&limit=50" \
  -H "Authorization: Basic <base64-user:pass>"

# Volume health
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/volume?select=name,state,size" \
  -H "Authorization: Basic <base64-user:pass>"

# Replication session state (Metro / async)
curl -k -X GET "https://<powerstore-mgmt-ip>/api/rest/replication_session" \
  -H "Authorization: Basic <base64-user:pass>"
```

---

## Support SLA Reference

| Priority | Definition | Initial Response SLA |
|---|---|---|
| P1 — Critical | Array completely down; all I/O stopped; data inaccessible | 1 hour (24×7 — requires ProSupport 24×7) |
| P2 — High | Single controller degraded; drive failure; replication broken | 4 hours (24×7 — requires ProSupport 24×7) |
| P3 — Medium | Non-critical feature degraded; workaround available | Next business day |
| P4 — Low | How-to, planning, documentation, advisory review | Next business day |

---

## See also

- [PowerStore — Diagnostics](diagnostics/)
- [PowerStore — Common Issues](common-issues/)

---

## Verify resolution

- Check PSM → Dashboard → Hardware Health: all appliances show Healthy
- Check PSM → Alerts: no active Critical or Major alerts related to the original issue
- Run REST `GET /api/rest/hardware?type=Node` and confirm both controllers show `Online`
- Run REST `GET /api/rest/hardware?type=Drive` and confirm no drives in `Failed` or `Degraded` state
- Confirm hosts can access storage: run an I/O test from an affected host
- Check PSM → Storage → Volumes: all volumes show `Ready` state
- Monitor for 15 minutes after the fix before confirming resolution to Dell
