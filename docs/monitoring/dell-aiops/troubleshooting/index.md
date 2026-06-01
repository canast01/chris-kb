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
┌──────────────────────────────────── Dell AIOps — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Adapter Not Collecting            │  │               Platform Issues               │   │
│   │               Check credential               │  │             Check /api/v1/health            │   │
│   │             Verify network reach             │  │               Restart services              │   │
│   │              Review adapter log              │  │               Check disk space              │   │
│   │               Re-save adapter                │  │             Time-series DB check            │   │
│   │                Check firewall                │  │            Collect support bundle           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Logs: /var/log/aiops/ on each node · support bundle via aiops-admin support collect                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Adapter log = Per-adapter log in /var/log/aiops/adapters/; shows collection errors                   │
│  Health endpoint = GET /api/v1/health returns status of all AIOps services                            │
│  Re-save adapter = Resaving adapter config resets its state; often fixes transient errors             │
│  Disk space = Time-series DB fills disk over time; monitor and archive/purge old data                 │
│  Time-series DB = Check DB health with aiops-admin db status                                          │
│  Support bundle = aiops-admin support collect creates compressed log archive                          │
│  Service restart = aiops-admin service restart <name> to recover failed service                       │
│  Firewall = Check management host can reach infrastructure API ports (443, 8080)                      │
│  Credential = Wrong or expired password causes No Data state; update in adapter settings              │
│  Network reach = Test from AIOps host: curl -k https://<array>:443/api/types                          │
│  Log level = Increase to DEBUG in adapter settings for detailed collection tracing                    │
│  Dell support = Open case at support.dell.com; attach support bundle                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

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
