# Dell AIOps — Integrations

<div class="kb-summary">
Dell AIOps is embedded in CloudIQ — integrations are shared. Supported Dell array types, notification channels, and the APEX Console API are the key integration surfaces.
</div>

```text
┌─────────────────────────────── Dell AIOps — Architecture Integrations ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Infrastructure Inputs             │              Notification Outputs              │   │
│   │             PowerStore REST API              │               ServiceNow webhook               │   │
│   │               PowerScale PAPI                │                 PagerDuty REST                 │   │
│   │              PowerFlex REST API              │              Slack/Teams webhook               │   │
│   │             CloudIQ bridge feed              │                   Email SMTP                   │   │
│   │            VxRail REST / VCF API             │              Grafana data source               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AIOps polls infrastructure APIs · outbound notifications over TCP 443/25 to targets                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PAPI = PowerScale Platform API; REST interface for isilon/PowerScale management                      │
│  REST API = PowerStore/PowerFlex management API; AIOps polls every 5 minutes                          │
│  CloudIQ bridge = Component ingesting CloudIQ health data into AIOps for correlation                  │
│  VCF API = VMware Cloud Foundation API for vSphere and SDDC component metrics                         │
│  Webhook = HTTP POST from AIOps when alert fires; payload in JSON                                     │
│  Grafana data source = AIOps REST API proxied as Grafana data source for custom panels                │
│  SMTP = Email notification from AIOps SMTP client on alert                                            │
│  PagerDuty = On-call routing platform receiving AIOps alerts via Events API v2                        │
│  Slack webhook = Incoming webhook URL for posting alert summaries to a Slack channel                  │
│  Poll interval = Frequency AIOps adapter queries infrastructure API; default 5 minutes                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
