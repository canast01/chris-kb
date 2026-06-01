# Pure1 Integration

<div class="kb-summary">
Pure1 Integration reference covering Overview, Native Array Integration, Email Alert Integration, Aria Operations Integration (Pure Storage Management Pack), Splunk Integration and 1 more sections.
</div>

## Overview

Pure1 integrates natively with all Pure Storage FlashArray and FlashBlade systems via outbound telemetry. External integrations extend Pure1 data and alerts into ITSM, observability, on-call, and notification platforms.

## Native Array Integration

All Pure arrays connect to Pure1 automatically over outbound HTTPS. No on-premises collector is required.

```bash
# Verify array connectivity from Purity CLI
purearray list --connection
# Expected: pure1.purestorage.com connected

# Check array network configuration
purearray list --network

# Set proxy if needed
purearray set --proxy https://<proxy-host>:<port>
```
┌────────────────────────────────────── Pure1 — Integration Guide ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               ITSM Integration               │  │               Monitoring Stack              │   │
│   │              ServiceNow webhook              │  │                 Aria Ops PAK                │   │
│   │                Auto-incident                 │  │                Grafana panels               │   │
│   │               PagerDuty events               │  │                  Splunk HEC                 │   │
│   │                Slack webhook                 │  │              Custom REST script             │   │
│   │                 Email alerts                 │  │                py-pure-client               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Pure1 in cloud · webhooks outbound to ITSM SaaS · REST API for on-prem consumers                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ServiceNow webhook = Pure1 POST to ServiceNow event endpoint on proactive alert                      │
│  Auto-incident = ServiceNow incident created from Pure1 alert payload                                 │
│  PagerDuty = On-call routing; Pure1 webhook delivers to PagerDuty Events API v2                       │
│  Slack webhook = Pure1 proactive alert posted to storage channel                                      │
│  Aria Ops PAK = VMware adapter pulling FlashArray/FlashBlade metrics into Aria Ops                    │
│  Grafana panels = Pure1 REST API proxied as Grafana data source                                       │
│  Splunk HEC = Pure1 alerts forwarded as events to Splunk for SIEM correlation                         │
│  py-pure-client = Pure-provided Python library for Pure1 and Purity REST APIs                         │
│  Custom REST script = Polling Pure1 API and pushing to proprietary dashboard/tooling                  │
│  Email = Pure1 SMTP notification for proactive alerts; configure in org settings                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

Separate rules for WARNING (email) and CRITICAL (PagerDuty + ServiceNow) are the recommended pattern.

## Aria Operations Integration (Pure Storage Management Pack)

The Pure Storage Management Pack for Aria Operations pulls FlashArray metrics into vROps for correlated VMware + storage dashboards.

```text
Aria Operations > Admin > Solutions > Pure Storage Management Pack
- Pure1 API endpoint: https://api.pure1.purestorage.com
- API key / private key: (service account key from Pure1)
- Collection interval: 5 minutes
```

Key metrics available in Aria Operations from this integration:
- Array IOPS, throughput, latency
- Volume-level performance
- Array capacity used / available / data reduction ratio

## Splunk Integration

A Splunk Heavy Forwarder or a scheduled script pulls Pure1 API data for fleet health and capacity dashboards in Splunk.

```python
# Example: scheduled Pure1 API pull for Splunk index
# Runs every 15 minutes via Splunk scripted input or cron

import requests, json, time

# Auth using Pure1 RSA private key (see scripts/pure1/authentication.py)
headers = {"Authorization": f"Bearer {get_pure1_token()}"}
resp    = requests.get("https://api.pure1.purestorage.com/api/1.latest/arrays",
                       headers=headers)
for array in resp.json()["items"]:
    event = {
        "source": "pure1",
        "name": array["name"],
        "os": array.get("os"),
        "version": array.get("version"),
        "time": int(time.time())
    }
    print(json.dumps(event))  # Splunk scripted input reads stdout
```

## Integration Summary

| Integration | Method | Purpose |
|---|---|---|
| FlashArray / FlashBlade | Outbound HTTPS (native — Purity) | Fleet health, capacity, performance telemetry |
| Aria Operations | Pure Storage Management Pack | vROps dashboards with Pure array data |
| Splunk | Pure1 REST API poller | Capacity and alert events in Splunk |
| ServiceNow | Pure1 alert webhook | Auto-ticket creation on CRITICAL alerts |
| PagerDuty | Pure1 alert webhook | On-call notification for CRITICAL alerts |
| Slack / Teams | Pure1 alert webhook | Real-time alert notifications to ops channel |
| Email | Pure1 notification rules | WARNING alert distribution |
