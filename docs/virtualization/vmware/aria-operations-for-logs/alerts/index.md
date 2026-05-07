# Aria Operations for Logs — Alerts

## Overview

Log-based alerts in Aria Operations for Logs (vRealize Log Insight) trigger notifications when query results meet defined thresholds. Alerts can fire via email, webhook, or integration with Aria Operations.

## Alert Types and Configuration

Alerts are created from saved queries. Navigate to **Interactive Analytics**, build your query, then click **Create Alert**.

```bash
# List all configured alerts via API
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/alerts \
  | python3 -m json.tool

# Get details of a specific alert
curl -sk -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/alerts/<alert-id>" \
  | python3 -m json.tool

# Disable an alert
curl -sk -X PUT -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/alerts/<alert-id>/state/DISABLED" \
  -H "Content-Type: application/json"

# Enable an alert
curl -sk -X PUT -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/alerts/<alert-id>/state/ENABLED" \
  -H "Content-Type: application/json"
```

## Alert Query Syntax

Alerts are built on the same query language used in Interactive Analytics:

```
# Alert on SSH failed logins (count > 10 in 5 min)
text contains "Failed password" AND hostname contains "prod-" 

# Alert on vCenter alarm events
appname = "vpxd" AND text contains "alarm" AND text contains "triggered"

# Alert on disk full events across all Linux hosts
text matches "No space left on device" AND source != "dev"

# Alert on firewall denies from specific subnet
text contains "DENY" AND text contains "10.0.1." AND appname = "pfsense"
```

## Alert Threshold Settings

| Threshold Type | Use Case | Example |
|---|---|---|
| Count | Fire when N events occur in time window | `> 10 in 5 minutes` |
| Rate of change | Fire when event rate increases sharply | `> 50% increase in 10 minutes` |
| Static (presence) | Fire when any matching event appears | Any occurrence of `"kernel panic"` |

## Notification Webhooks

Webhooks send alert payloads to external systems such as Teams, Slack, or custom endpoints.

```bash
# List configured notification destinations
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/notification/channels \
  | python3 -m json.tool

# Create a webhook notification channel
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/notification/channels \
  -H "Content-Type: application/json" \
  -d '{
    "type": "WEBHOOK",
    "name": "teams-alerts",
    "webhookUrl": "https://example.webhook.office.com/webhookb2/...",
    "contentType": "application/json",
    "body": "{\"text\": \"Alert: ${alertName} - ${hitCount} events\"}"
  }'

# Test a notification channel
curl -sk -X POST -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/notification/channels/<channel-id>/test"
```

Webhook payload variables:

| Variable | Value |
|---|---|
| `${alertName}` | Name of the alert |
| `${hitCount}` | Number of matching events |
| `${url}` | Deep link to alert in vRLI UI |
| `${fields}` | Extracted field values from the matching log |
| `${timestamp}` | Alert trigger time (epoch ms) |

## Alert Queries via API

```bash
# Run an ad-hoc alert query to test before creating an alert
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/events/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "text contains \"Failed password\"",
    "startTimeMillis": 1714950000000,
    "endTimeMillis": 1714953600000,
    "numResults": 100
  }' | python3 -m json.tool

# List active (recently triggered) alerts
curl -sk -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/alerts?status=ACTIVE" \
  | python3 -m json.tool
```

## Integration with Aria Operations

When integrated with Aria Operations (vROps), alerts in vRLI can create alerts/symptoms in the vROps console:

```bash
# Configure vROps integration from vRLI
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/operations-server-config \
  -H "Content-Type: application/json" \
  -d '{
    "serverHost": "<vrops-fqdn>",
    "serverPort": 443,
    "username": "admin",
    "password": "<password>",
    "enabled": true
  }'
```
