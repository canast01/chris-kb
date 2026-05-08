# CloudIQ — Procedures

> Part of the [CloudIQ](../../) reference.

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
