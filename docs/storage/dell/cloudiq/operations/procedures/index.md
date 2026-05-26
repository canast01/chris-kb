# CloudIQ — Procedures

```
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
