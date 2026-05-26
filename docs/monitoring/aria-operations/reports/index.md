# Aria Operations: Scheduled Reports and PDF Export

```
┌────────────────────────────────────── Aria Operations — Reports ──────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Built-in Reports      │  │        Custom Reports       │  │          Scheduling         │   │
│   │      Inventory summary      │  │      Add/remove metrics     │  │     Hourly/daily/weekly     │   │
│   │      Capacity overview      │  │     Filter by group/tag     │  │      Email on complete      │   │
│   │        VM rightsizing       │  │      Time range select      │  │      SMTP outbound plug     │   │
│   │        Alert summary        │  │        Export PDF/CSV       │  │        Recipient list       │   │
│   │       Host performance      │  │        Clone template       │  │      Retention: 30 days     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Reports generated on master node · PDF export uses embedded renderer · SCP delivery optional         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Report template = Reusable definition of metrics, filters, and format for a report                   │
│  Clone template = Copying a built-in report template to create a customised version                   │
│  Subject view = Scope of objects a report runs against (group, tag, or all objects)                   │
│  Metric column = Individual metric added as column in tabular report section                          │
│  PDF export = Formatted report rendered to PDF; useful for executive or compliance sharing            │
│  CSV export = Raw metric data in comma-separated format for spreadsheet analysis                      │
│  Scheduled report = Report configured to run automatically at a defined interval                      │
│  SMTP outbound = Email delivery plugin configured in Administration > Outbound Settings               │
│  Rightsizing report = Identifies over/under-provisioned VMs based on utilisation thresholds           │
│  Retention = Number of past report runs kept in Aria Ops; older runs purged automatically             │
│  Time range = Historical window for report data (last 24h, 7d, 30d, custom)                           │
│  Recipient list = Named list of email addresses for scheduled report delivery                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

## Scheduling Reports

Reports can be sent on a recurring schedule (daily, weekly, monthly) to one or more email addresses.

Navigation: **Reports > Report Templates > [Template] > Schedule**

Schedule configuration fields:

| Field | Options |
|---|---|
| Frequency | Once, Hourly, Daily, Weekly, Monthly |
| Time | Specific time of day (uses Aria Ops server timezone) |
| Email recipients | Comma-separated addresses |
| Format | PDF (default), CSV |
| Traverse All Levels | Include sub-objects in a group hierarchy |

```bash
# Create a scheduled report via API
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/reportdefinitions/<templateId>/schedules" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "recurrence": "WEEKLY",
    "dayOfWeek": "MONDAY",
    "hours": 7,
    "minutes": 0,
    "emailTo": ["ops-team@example.com"],
    "reportFormat": "PDF"
  }'
```

## Downloading Generated Reports

Completed reports are stored in **Reports > Generated Reports**. Reports expire after 30 days by default.

```bash
# List generated reports
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/reports" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" | jq '.reports[] | {id, name, generatedOn}'

# Download a report as PDF
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/reports/<reportId>/download" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -o report.pdf
```

## Report Output Formats

| Format | Use Case | Notes |
|---|---|---|
| PDF | Management delivery, archiving | Preserves charts and layout |
| CSV | Data export for spreadsheet analysis | Flat data only, no charts |

## Common Report Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Report email not received | SMTP not configured | Check Administration > Outbound Settings > Email |
| Report shows blank sections | View has no data for selected object | Verify object has metrics and is collecting |
| PDF layout broken | Too many columns in table view | Reduce columns or switch to landscape |
| Scheduled report never runs | Schedule timezone mismatch | Confirm server timezone in Administration |
| Report generation fails | Large dataset timeout | Reduce scope, use group-level filtering |
