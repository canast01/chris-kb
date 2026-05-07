# Dell AIOps: Troubleshooting False Positives, Missing Data, and Integration Failures

This page covers common operational problems with Dell AIOps: AI alert false positives, data gaps in the analytics pipeline, and failures in the integration between AIOps and connected systems.

## Diagnosing False Positive AI Alerts

False positives occur when the model fires an alert for a normal but unusual event (scheduled backup, bulk migration, test run).

```bash
# List recent AI alerts with confidence scores
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/alerts?filter=state%20eq%20%27ACTIVE%27&select=id,type,metric,confidence,started_at,system_name" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | select(.confidence < 0.75)'

# Dismiss and flag a false positive for model feedback
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/alerts/<alertId>/dismiss" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"reason": "FALSE_POSITIVE", "comment": "Weekly backup job 22:00–02:00, expected anomaly"}'
```

False positive indicators:

| Indicator | Meaning |
|---|---|
| `confidence` < 0.70 | Model uncertainty — treat with low urgency |
| Alert occurs at same time daily/weekly | Recurring scheduled job, not a real anomaly |
| Anomaly duration < 15 minutes | Transient spike, unlikely real issue |
| Alert clears before acknowledged | Self-correcting condition |

## Missing Data in AIOps Analytics

If the AIOps UI shows blank charts, missing predictions, or "Insufficient Data" messages:

1. Verify the system is connected and sending telemetry.
2. Check the last contact timestamp.
3. Confirm the system type is supported by AIOps (not all CloudIQ system types have full AIOps coverage).

```bash
# Check system connectivity and last telemetry received
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage_systems?select=name,connectivity_status,last_contact_timestamp" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | select(.connectivity_status != "CONNECTED")'
```

Data gap causes and resolution:

| Cause | Symptom | Fix |
|---|---|---|
| SRS/ESRS gateway offline | All data stops at same time | Restart gateway service; check internet path |
| System firmware bug | Gaps in specific metric streams | Apply firmware update for known telemetry issues |
| New system < 14 days old | No predictions, limited insights | Wait for baseline accumulation period |
| System type not fully supported | Only basic health visible | Check AIOps supported systems matrix |
| Tenant configuration error | System in wrong site group | Reassign system to correct site in CloudIQ settings |

## Integration Failures

AIOps integrates with CloudIQ system registration, ESRS telemetry, and optional ITSM connectors (ServiceNow). Integration failures prevent alerts from being acted upon.

```bash
# Test CloudIQ API authentication
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/auth/oauth/v2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=<clientId>&client_secret=<clientSecret>" \
  | jq '{access_token, expires_in}'
```

Common integration issues:

| Integration | Error | Fix |
|---|---|---|
| CloudIQ API auth | 401 Unauthorized | Regenerate API client credentials in Settings |
| ServiceNow webhook | 403 Forbidden | Verify ServiceNow MID server and integration user |
| ESRS telemetry | No data after gateway restart | Restart phone-home agent on storage system |
| Email notifications | Connection refused to SMTP | Check relay hostname and port in notification settings |

## Reviewing AIOps System Events

CloudIQ maintains an audit log of AIOps model events, which is useful when investigating why an alert fired or was suppressed.

```bash
# Get AIOps audit events for the last 7 days
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/audit_events?filter=created_at%20gt%20%272026-04-30%27&order_by=created_at%20desc" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {event_type, description, created_at}'
```

## Common Troubleshooting Reference

| Problem | First Check | Second Check |
|---|---|---|
| AIOps alert flood | confidence scores of firing alerts | Scheduled jobs overlapping baseline window |
| Predictions disappeared | System connectivity status | Data collection gap > 48 hours |
| Recommendation not generating | Days since system registered | System type support matrix |
| Alert correlation groups wrong | Systems in same site group | Regroup systems in CloudIQ topology settings |
| API returns 429 Too Many Requests | Rate limit exceeded | Implement exponential backoff; reduce polling frequency |
