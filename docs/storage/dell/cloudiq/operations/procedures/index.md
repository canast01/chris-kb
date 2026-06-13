---
tags:
  - dell
  - operations
---
# CloudIQ — Procedures


<div class="kb-summary">
Procedures reference covering Maintenance Window.
</div>

```text
┌──────────────────────────────── Dell CloudIQ — Operational Procedures ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CloudIQ procedures: alert handling, report generation, and array lifecycle management     │   │
│   │     Alert procedures: acknowledge, suppress, bulk-resolve, escalate to SR, export history     │   │
│   │   Report procedures: generate capacity and perf reports, schedule email delivery, export CSV  │   │
│   │    Array procedures: add new array to SCG, update credentials, remove decommissioned arrays   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Trigger → acknowledge/suppress → action → validate resolution → document in ITSM ticket            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Alert Procedures      │  │      Report Procedures      │  │       Array Procedures      │   │
│   │      Acknowledge alert      │  │       Capacity report       │  │          Add array          │   │
│   │      Create suppression     │  │         Perf report         │  │         Update creds        │   │
│   │         Bulk resolve        │  │        Email schedule       │  │         Remove array        │   │
│   │        Escalate to SR       │  │       Custom dashboard      │  │      Recheck telemetry      │   │
│   │        Export history       │  │        Export CSV/PDF       │  │         Site removal        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All procedures executed in CloudIQ portal or SCG management UI; no CLI access needed               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Category     │    Procedure     │       Steps       │       Tool       │    Frequency     │   │
│   │      Alerts      │   Acknowledge    │      2 steps      │      Portal      │    As needed     │   │
│   │     Reports      │ Capacity report  │      3 steps      │      Portal      │      Weekly      │   │
│   │      Arrays      │    Add to SCG    │      4 steps      │      SCG UI      │   Per onboard    │   │
│   │      Users       │     Add user     │      3 steps      │      Portal      │     Per hire     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: procedures touch only CloudIQ portal and SCG UI — no direct array CLI required           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Acknowledge    = Marking alert as reviewed; does not resolve; creates audit trail entry            │
│    Suppression    = Rule that silences repeated alerts for a known condition; has expiry date         │
│    Bulk resolve   = Closing multiple alerts at once; useful after maintenance window completes        │
│    Escalate to SR = Opening a Dell Service Request from within CloudIQ alert detail view              │
│    Capacity report = Pre-built CloudIQ report showing pool usage, forecast, and top consumers         │
│    Custom dashboard = User-defined widget layout in CloudIQ showing selected arrays/metrics           │
│    Export CSV     = Downloading CloudIQ data as spreadsheet; used for external reporting tools        │
│    Add array      = Entering array mgmt IP and credentials in SCG so CloudIQ can collect telemetry    │
│    Update creds   = Refreshing array admin password in SCG when array password is changed             │
│    Remove array   = Deleting array from SCG and CloudIQ; telemetry history retained for 90 days       │
│    Site removal   = Decommissioning an SCG site; requires all arrays removed first                    │
│    Email schedule = CloudIQ automated report delivery to specified addresses on a set cadence         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [CloudIQ](../../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Maintenance Window

1. Before the window: note the current health score for all affected systems as a baseline
2. Suppress CloudIQ alerts for the duration of the maintenance window via REST API:
   ```bash
   # Create a maintenance window (suppresses alerts for the specified system)
   curl -s -X POST \
     -H "Authorization: Bearer ${CLOUDIQ_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "resource_id": "<system_object_id>",
       "resource_type": "STORAGE_SYSTEM",
       "start_time": "2026-05-06T20:00:00Z",
       "end_time": "2026-05-06T23:00:00Z",
       "description": "Planned maintenance window"
     }' \
     "${CLOUDIQ_BASE}/maintenance-windows"
   ```
3. Perform the planned maintenance on the storage system
4. After the window: remove or allow the maintenance window to expire
5. Re-verify that alert notifications resume (send a test or wait for the next scheduled health poll)
6. Confirm the system reconnects and health score is visible in the dashboard

---

## Connect a Storage System to CloudIQ

1. Install the CloudIQ SupportAssist agent (SCG — Secure Connect Gateway) on a VM or physical host in the same management network as the storage system
2. In the SCG management UI, add the storage system: enter the management IP, admin username, and password
3. SCG begins collecting telemetry and forwarding it to the Dell CloudIQ cloud endpoint over HTTPS (port 443 outbound)
4. Log in to the CloudIQ portal (cloudiq.dell.com) and confirm the system appears under **Infrastructure → Storage Systems**
5. Allow up to 15 minutes for the first telemetry collection to complete; verify health score and capacity data are populating correctly

## Acknowledge an Alert

1. Log in to the CloudIQ portal and navigate to **Alerts**
2. Locate the alert using filters (severity, system, date range)
3. Select the alert and click **Acknowledge**
4. Add notes describing the investigation status or known cause
5. Optionally assign the alert to an owner (team member or queue)
6. Track the alert to resolution — alerts remain in the acknowledged state until manually resolved or auto-closed by CloudIQ when the condition clears

## Create a Custom Capacity Report

1. Navigate to **CloudIQ → Capacity**
2. Use the system selector to choose which storage systems to include in the report
3. Apply any desired filters (site, model, tier)
4. To export on demand: click **Export** and select CSV format — download the file for use in external reporting tools
5. To schedule a recurring report: click **Schedule Report** → set frequency (daily, weekly, monthly) → enter email recipients → save
6. Confirm delivery by checking the specified email inbox after the first scheduled run

## Configure Threshold-Based Notifications

1. Navigate to **CloudIQ → Settings → Notifications**
2. Click **Add Rule** and select the notification type (e.g. capacity threshold)
3. Set the threshold value (e.g. pool capacity used > 80%)
4. Select the scope: all systems, a specific site, or individual systems
5. Configure email recipients for the notification
6. Save the rule, then click **Test** to send a test notification and confirm delivery
7. Verify the rule appears in the active notifications list

## Review Performance Anomaly

1. Navigate to **CloudIQ → Performance** and locate the anomaly (flagged automatically by CloudIQ ML)
2. Click the anomaly to open the detail view — review the contributing metrics (latency, IOPS, bandwidth) and the time range
3. Correlate the anomaly start time with any change activity recorded in the ITSM change log
4. If the anomaly aligns with a known change or maintenance window, add a note and **Dismiss** the anomaly
5. If the anomaly is unexplained, drill into the affected volumes or hosts for further investigation and open a Dell support case if needed
6. Document the outcome in the ITSM ticket

## Request Proactive Recommendation Implementation

1. Navigate to **CloudIQ → Recommendations**
2. Review the list of active recommendations — each includes a description, impact assessment, and affected systems
3. Select the recommendation and click **View Details** to review the full impact and any prerequisites
4. For self-service actions (e.g. configuration tuning): follow the embedded steps and implement within an approved change window
5. For actions requiring Dell support (e.g. firmware update, hardware replacement): click **Schedule with Dell** — this opens a Dell support engagement
6. After implementation, confirm the recommendation is marked as resolved in CloudIQ

## Export System Inventory Report

1. Navigate to **CloudIQ → Inventory**
2. Select the systems to include (or leave unfiltered for all managed systems)
3. Click **Export** and select CSV format
4. The downloaded file includes model, serial number, firmware version, site, and management IP for each managed system
5. Use the CSV for asset audits, CMDB updates, or capacity planning reviews

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
