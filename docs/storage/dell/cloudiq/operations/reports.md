---
tags:
  - dell
  - operations
---
# CloudIQ — Reporting
![CloudIQ — Reporting](../../../../assets/storage-dell-cloudiq-operations-reports.svg)

```bash
# Trigger an on-demand health report via CloudIQ API
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/reports" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "HEALTH_SUMMARY",
    "system_ids": ["<systemId1>", "<systemId2>"],
    "date_range": {
      "start": "2026-04-01T00:00:00Z",
      "end": "2026-04-30T23:59:59Z"
    },
    "format": "PDF"
  }'

# Check report generation status
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/reports/<reportId>" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '{status, download_url}'

# Download completed report
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/reports/<reportId>/download" \
  -H "Authorization: Bearer <access_token>" \
  -o cloudiq-health-report.pdf
```


```text title="Expected output"
{
  "report_id": "rpt-8f4c2e91-a3d5-4b7e-9c1f-6e2d5a8b3c4f",
  "type": "HEALTH_SUMMARY",
  "system_ids": ["SYS-001-EMC01", "SYS-002-EMC02"],
  "status": "PENDING",
  "created_at": "2026-04-15T14:32:18Z",
  "estimated_completion": "2026-04-15T14:37:18Z"
}
{
  "status": "COMPLETED",
  "download_url": "https://cloudiq.apis.dell.com/cloudiq/rest/v1/reports/rpt-8f4c2e91-a3d5-4b7e-9c1f-6e2d5a8b3c4f/download"
}
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 2847k  100 2847k    0     0   1.2M      0  0:00:02  0:00:02 --:--:--  0:00:02
```

!!! warning "Common errors"
    **`{"error": "INVALID_TOKEN", "message": "Access token has expired or is invalid"}`** — Regenerate a fresh access token using Dell CloudIQ authentication endpoint and update the Bearer token.
    **`{"error": "SYSTEM_NOT_FOUND", "message": "System ID SYS-001-EMC01 not found in your account"}`** — Verify system IDs are registered in CloudIQ and match your account's managed systems list.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification or use `--cacert` with a valid CA bundle path.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [CloudIQ: Alert Types, Severity, and Notification Configuration](alerts.md)
- [Dell CloudIQ Backup and Restore](backup-restore.md)
- [CloudIQ: Capacity Forecasting and Pool Utilisation](capacity.md)
- [CloudIQ — Operations](index.md)
- [CloudIQ — Architecture](../../architecture/)
- [CloudIQ — Initial Setup](../../deploy/)
- [CloudIQ — Security](../../security/)
- [CloudIQ — Troubleshooting](../../troubleshooting/)
