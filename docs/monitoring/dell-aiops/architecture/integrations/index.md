# Dell AIOps — Integrations

<div class="kb-summary">
Dell AIOps is embedded in CloudIQ — integrations are shared. Supported Dell array types, notification channels, and the APEX Console API are the key integration surfaces.
</div>

## Supported Platforms

Dell AIOps draws telemetry from all arrays registered to CloudIQ via the SCG:

| Platform | AIOps Capabilities |
|---|---|
| PowerMax | Capacity forecasting, SRDF anomaly detection, workload fingerprinting |
| PowerStore | Anomaly detection on latency, capacity forecast |
| PowerScale | Node health anomalies, capacity projection, quota trending |
| Unity XT | Pool capacity forecast, SP health anomaly |
| Data Domain | Dedup ratio anomaly, capacity forecast |

## Notification Channels

| Channel | Trigger | Configuration |
|---|---|---|
| Email | Critical recommendation or anomaly | CloudIQ portal → Settings → Notifications |
| ServiceNow | Critical severity | CloudIQ portal → Settings → ServiceNow connector |
| Webhook | Any severity | CloudIQ portal → Settings → Webhook; POST to custom URL |
| Slack / Teams | Warning+ | Via CloudIQ webhook to Slack incoming webhook URL |

## APEX Console API

The APEX Console (which surfaces AIOps recommendations) is accessible via the CloudIQ REST API:

```bash
# List active AIOps recommendations
curl -H "Authorization: Bearer <token>" \
  https://cloudiq.dell.com/v1/recommendations?status=active

# Acknowledge a recommendation
curl -X PATCH -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "acknowledged", "comment": "Scheduled for next change window"}' \
  https://cloudiq.dell.com/v1/recommendations/{id}
```

## Integration with ServiceNow CMDB

- AIOps anomaly alerts can auto-create ServiceNow incidents linked to the affected CI
- Requires SCG → CloudIQ → ServiceNow connector configured with the correct CMDB table mapping (`cmdb_ci_storage_server`)
- Map CloudIQ array names to ServiceNow CI names to ensure correct CI assignment on incident creation
