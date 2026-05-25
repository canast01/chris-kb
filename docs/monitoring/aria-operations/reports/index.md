# Aria Operations: Scheduled Reports and PDF Export

```text
Reports Pipeline — Aria Operations
┌──────────────────┐
│ Report Template  │  (capacity / health / compliance / VM)
│  created in UI   │
└────────┬─────────┘
         ▼
┌──────────────────┐     ┌───────────────────┐
│ Schedule defined │────►│  Trigger: weekly  │
│  (day/time/freq) │     │  Monday 07:00 UTC │
└────────┬─────────┘     └───────────────────┘
         ▼
┌──────────────────┐
│ Report generated │  PDF or CSV
│ (server-side)    │
└────────┬─────────┘
         │
    ┌────┴───────────┐
    ▼                ▼
┌────────┐    ┌────────────┐
│ Email  │    │ Download   │
│ distro │    │ (Generated │
│  list  │    │  Reports)  │
└────────┘    └────────────┘
```

Aria Operations reports provide point-in-time and scheduled summaries of health, capacity, and compliance data. This page covers creating report templates, scheduling delivery, configuring PDF export, and managing distribution lists.

## Report Templates and Types

Reports are built from templates. Aria Operations ships with built-in templates; custom templates can be created from scratch or by cloning an existing one.

Navigation: **Reports > Report Templates**

| Template Category | Examples |
|---|---|
| Capacity | Cluster capacity summary, datastore utilisation, time remaining |
| Health | Infrastructure health overview, host/VM health detail |
| Compliance | Policy compliance, configuration drift |
| Alerts | Alert history, alert trends |
| VM | VM inventory, rightsizing candidates, idle VMs |
| Custom | User-defined with selected views and metrics |

## Creating a Custom Report Template

1. Navigate to **Reports > Report Templates > + Add**.
2. Choose **Subject** (the root object type the report covers).
3. Add **Views** (table views, metric charts, scoreboard summaries).
4. Configure **Filters** to scope to specific groups or tags.
5. Set **Page Layout**: portrait or landscape, header/footer text, logo.
6. Save the template.

```bash
# List report templates via API
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/reportdefinitions" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" | jq '.reportDefinitions[] | {id, name}'

# Trigger an on-demand report generation
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/reports" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "reportDefinitionId": "<templateId>",
    "subject": {"resourceId": "<resourceId>"}
  }'
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
