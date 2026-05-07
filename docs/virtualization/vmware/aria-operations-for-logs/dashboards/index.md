# Aria Operations for Logs — Dashboards

## Overview

Dashboards in Aria Operations for Logs provide persistent, shareable views of log data. They are composed of widgets that display query results, field histograms, and time-series counts. Dashboards are useful for operational monitoring and compliance reporting.

## Creating Dashboards

Dashboards are created via the UI at **Dashboards > New Dashboard**, or via the API:

```bash
# List existing dashboards
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/dashboards \
  | python3 -m json.tool

# Create a new dashboard
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/dashboards \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security Events",
    "shared": true,
    "widgets": []
  }' | python3 -m json.tool

# Clone an existing dashboard
curl -sk -X POST -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/dashboards/<dashboard-id>/clone" \
  -H "Content-Type: application/json" \
  -d '{"name": "Security Events - Copy"}'
```

## Log Widgets

Widgets are the building blocks of a dashboard. Each widget runs a query against ingested log data.

Widget types available:

| Widget Type | Description | Best Used For |
|---|---|---|
| Event Count Over Time | Bar chart of event frequency | Volume monitoring, spike detection |
| Field Table | Table of extracted field values | IP/hostname/user-based summaries |
| Field Distribution | Pie or bar chart of field values | Top-N analysis |
| Text | Free text for labels and notes | Section headers, instructions |
| Log Count | Single number tile | KPI / SLA metrics |

```bash
# Add a widget to a dashboard
curl -sk -X POST -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/dashboards/<dashboard-id>/widgets" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Failed SSH Logins",
    "widgetType": "EVENT_COUNT_OVER_TIME",
    "query": "text contains \"Failed password\"",
    "timeRange": "LAST_1_HOUR"
  }'
```

## Field Extraction

Custom fields are extracted from log messages using regex. Extracted fields can be used in widgets, alerts, and queries.

```bash
# Create a custom extracted field
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/fields \
  -H "Content-Type: application/json" \
  -d '{
    "name": "source_ip",
    "displayName": "Source IP",
    "regex": "from ([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})",
    "regexFlags": [],
    "discoverable": true
  }'

# List all custom extracted fields
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/fields \
  | python3 -m json.tool

# Verify a regex extraction against sample log text
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/fields/test \
  -H "Content-Type: application/json" \
  -d '{
    "regex": "from ([0-9.]+)",
    "sample": "sshd: Failed password for root from 192.168.1.10 port 44231"
  }' | python3 -m json.tool
```

Field extraction reference:

| Log Format | Extraction Approach | Example Regex |
|---|---|---|
| Key=value pairs | Named group on value | `user=(\S+)` |
| JSON logs | Use built-in JSON parser | — (automatic) |
| Apache/Nginx access logs | Use built-in content pack | — (content pack) |
| Syslog RFC5424 | Structured data auto-parsed | — (automatic) |
| Custom app logs | Regex per field | `\[ERROR\] (.+)` |

## Time Range Settings

Dashboard time range controls all widgets unless a widget overrides it:

```bash
# Set dashboard default time range via API
curl -sk -X PUT -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/dashboards/<dashboard-id>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security Events",
    "defaultTimeRange": "LAST_6_HOURS"
  }'
```

Available time range values:

| Value | Description |
|---|---|
| `LAST_5_MINUTES` | Last 5 minutes |
| `LAST_1_HOUR` | Last 1 hour |
| `LAST_6_HOURS` | Last 6 hours |
| `LAST_24_HOURS` | Last 24 hours |
| `LAST_7_DAYS` | Last 7 days |
| `CUSTOM` | User-specified start and end timestamps |

## Dashboard Sharing and Export

```bash
# Share a dashboard with all users
curl -sk -X PUT -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/dashboards/<dashboard-id>" \
  -H "Content-Type: application/json" \
  -d '{"shared": true}'

# Export all dashboards to JSON (for backup or migration)
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/dashboards \
  | python3 -m json.tool > vrli-dashboards-backup.json

# Import dashboards from JSON
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/dashboards/import \
  -H "Content-Type: application/json" \
  -d @vrli-dashboards-backup.json
```
