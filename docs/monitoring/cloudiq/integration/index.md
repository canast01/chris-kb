# CloudIQ Integration
## Overview

CloudIQ collects telemetry natively from all Dell platforms via the Secure Connect Gateway. External integrations extend alert delivery and data access into broader operational toolsets including ITSM, observability platforms, and notification systems.

## Native Platform Integrations (Inbound via SCG)

All Dell storage and server platforms are registered in the SCG and data flows automatically.

| Platform | Connection Method | Key Data |
|---|---|---|
| PowerStore | REST API from SCG | Health score, capacity, performance, alerts |
| PowerMax / VMAX | REST API from SCG | Health score, capacity, SRDF, performance |
| PowerScale / Isilon | REST API from SCG | Health score, capacity, protocol throughput |
| Unity XT | REST API from SCG | Health score, capacity, replication status |
| Data Domain / PowerProtect | REST API from SCG | Dedup ratios, capacity, replication health |
| PowerEdge (via iDRAC) | iDRAC REST API from SCG | Server health, firmware, hardware faults |

## ServiceNow Integration

CloudIQ can auto-create ServiceNow incidents on CRITICAL alerts via webhook.

```text
CloudIQ portal > Settings > Notifications > Add Notification Rule
- Trigger: Alert Severity = CRITICAL
- Action: Webhook
- URL: https://<servicenow-instance>/api/now/table/incident
- Authentication: Basic or OAuth token
- Payload: map alert object, description, severity to ServiceNow fields
  {
    "short_description": "{{alert.name}} on {{system.name}}",
    "severity": "1",
    "assignment_group": "storage-ops"
  }
```
┌───────────────────────────────────── CloudIQ — Integration Guide ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               ITSM Integration               │  │               Monitoring Stack              │   │
│   │              ServiceNow webhook              │  │               Aria Ops adapter              │   │
│   │             Auto-incident create             │  │             Grafana data source             │   │
│   │               CMDB asset link                │  │              Splunk HTTP Event              │   │
│   │             Alert → incident map             │  │              PagerDuty webhook              │   │
│   │             Bi-directional sync              │  │              Custom REST script             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CloudIQ in Dell cloud · webhook receivers on-prem or in monitoring SaaS platforms                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Webhook = Outbound HTTP POST from CloudIQ when alert fires; JSON body with array details             │
│  ServiceNow webhook = HTTP endpoint in ServiceNow receiving CloudIQ alerts as incidents               │
│  Auto-incident = ServiceNow incident created automatically from CloudIQ alert payload                 │
│  CMDB link = Matching CloudIQ array to ServiceNow CMDB CI using serial number                         │
│  Aria Ops adapter = PAK package pulling CloudIQ health data into Aria Operations                      │
│  Grafana data source = Custom plugin or REST proxy exposing CloudIQ metrics to Grafana                │
│  Splunk HEC = HTTP Event Collector; CloudIQ webhook forwarded for log-based correlation               │
│  PagerDuty webhook = CloudIQ alert forwarded to PagerDuty for on-call routing                         │
│  REST script = Python/shell script polling CloudIQ API and pushing to other systems                   │
│  Bi-directional = ServiceNow incident closure reflected back to CloudIQ alert state                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## REST API Access for Splunk / Grafana

The CloudIQ REST API is used by Splunk Heavy Forwarders or Grafana data source plugins to pull fleet health and capacity data on a scheduled basis.

```python
# Example: fetch all systems and health scores
import requests

TOKEN_URL = "https://api.cloudiq.dell.com/auth/oauth/v2/token"
API_BASE  = "https://api.cloudiq.dell.com/cloudiq/rest/v1"

def get_token(client_id, client_secret):
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    })
    return resp.json()["access_token"]

def list_systems(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_BASE}/systems", headers=headers)
    return resp.json()["results"]
```

## Aria Operations Integration

The Dell CloudIQ management pack for Aria Operations pulls health score and alert data into vROps for correlated VMware + Dell storage dashboards.

```text
Aria Operations > Admin > Solutions > Dell CloudIQ Management Pack
- CloudIQ API URL: https://api.cloudiq.dell.com
- Client ID / Secret: stored in Aria Operations credential store
- Collection interval: 15 minutes
```

## Integration Summary

| Integration | Method | Purpose |
|---|---|---|
| PowerMax / PowerStore / PowerScale / Unity / DD | SCG telemetry (native) | Health, capacity, and performance data |
| ServiceNow | Webhook from CloudIQ alert rules | Auto-ticket on CRITICAL alerts |
| Slack / Teams | Webhook notification | Real-time alert notifications to ops channel |
| Splunk / Grafana | CloudIQ REST API poller | Fleet health and capacity dashboards |
| Aria Operations | CloudIQ management pack | VMware + Dell storage correlation |
| Email | CloudIQ notification rules | WARNING alert distribution to team |
