# Dell AIOps Integration

<div class="kb-summary">
Dell AIOps Integration reference covering Overview, CloudIQ / SCG (Inbound Telemetry), Email and Webhook Notifications, SIEM Integration, Integration Summary and 1 more sections.
</div>

## Overview

Dell AIOps is integrated into the broader operational toolchain via CloudIQ's notification and API layers. All telemetry flows inbound through the Secure Connect Gateway; alerts and recommendations flow outbound to ITSM, notification, and observability platforms.

## CloudIQ / SCG (Inbound Telemetry)

All Dell storage systems must be registered in CloudIQ via the SCG. This is the prerequisite for all AIOps capabilities — without SCG-connected telemetry, AIOps has no data source.

```text
Verify collection status:
CloudIQ portal > Assets > [System] — check "Last Seen" timestamp
SCG admin UI > Systems > [System] > Connection Status
```
┌─────────────────────────────────── Dell AIOps — Integration Guide ────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               ITSM Integration               │  │             Observability Stack             │   │
│   │              ServiceNow webhook              │  │             Grafana data source             │   │
│   │             Auto incident create             │  │              Splunk HEC forward             │   │
│   │                CMDB CI update                │  │             Elastic integration             │   │
│   │              PagerDuty routing               │  │              Custom REST client             │   │
│   │              Jira issue create               │  │             Prometheus exporter             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AIOps on-prem · outbound TCP 443 to ITSM/SaaS targets · no inbound connections required              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ServiceNow webhook = AIOps POST to ServiceNow event endpoint on alert fire                           │
│  CMDB CI = Configuration Item in ServiceNow matched to AIOps monitored system                         │
│  Auto incident = ServiceNow incident created automatically from AIOps alert payload                   │
│  PagerDuty = On-call routing; AIOps sends Events API v2 payload for escalation                        │
│  Jira issue = AIOps creates Jira bug/task for recommendation tracking in dev teams                    │
│  Grafana data source = AIOps REST API configured as Grafana JSON data source                          │
│  Splunk HEC = HTTP Event Collector; AIOps forwards alerts as events for SIEM correlation              │
│  Prometheus exporter = AIOps /metrics endpoint scraped by Prometheus                                  │
│  Elastic integration = AIOps alert forwarded to Elasticsearch for log analytics                       │
│  REST client = Custom script polling AIOps API and pushing to proprietary system                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────── Dell AIOps — Integration Guide ────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               ITSM Integration               │  │             Observability Stack             │   │
│   │              ServiceNow webhook              │  │             Grafana data source             │   │
│   │             Auto incident create             │  │              Splunk HEC forward             │   │
│   │                CMDB CI update                │  │             Elastic integration             │   │
│   │              PagerDuty routing               │  │              Custom REST client             │   │
│   │              Jira issue create               │  │             Prometheus exporter             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AIOps on-prem · outbound TCP 443 to ITSM/SaaS targets · no inbound connections required              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ServiceNow webhook = AIOps POST to ServiceNow event endpoint on alert fire                           │
│  CMDB CI = Configuration Item in ServiceNow matched to AIOps monitored system                         │
│  Auto incident = ServiceNow incident created automatically from AIOps alert payload                   │
│  PagerDuty = On-call routing; AIOps sends Events API v2 payload for escalation                        │
│  Jira issue = AIOps creates Jira bug/task for recommendation tracking in dev teams                    │
│  Grafana data source = AIOps REST API configured as Grafana JSON data source                          │
│  Splunk HEC = HTTP Event Collector; AIOps forwards alerts as events for SIEM correlation              │
│  Prometheus exporter = AIOps /metrics endpoint scraped by Prometheus                                  │
│  Elastic integration = AIOps alert forwarded to Elasticsearch for log analytics                       │
│  REST client = Custom script polling AIOps API and pushing to proprietary system                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## SIEM Integration

AIOps audit events are available from the CloudIQ audit log. Export to SIEM for long-term retention and correlation with security events.

```text
# Automated audit log export (weekly):
GET https://api.cloudiq.dell.com/cloudiq/rest/v1/audit-logs?filter=created_at gt <timestamp>
Authorization: Bearer <token>
```

Forward the export to Splunk or Elastic via the existing log pipeline.

## Integration Summary

| Integration | Direction | Purpose |
|---|---|---|
| CloudIQ / SCG | Inbound | Storage telemetry and health data source |
| ServiceNow ITSM | Outbound | Recommendation-driven change/incident ticketing |
| Aria Operations | Bidirectional | Correlated VMware + Dell storage visibility |
| Email Notifications | Outbound | Critical/High recommendation alerts |
| PagerDuty | Outbound | Critical recommendation on-call paging |
| Teams / Slack Webhook | Outbound | Real-time recommendation notifications |
| SIEM (Splunk/Elastic) | Outbound | Audit log forwarding for compliance |

## Integration Health Checks

Verify all integrations are functional as part of the monthly ops review:

```text
- ServiceNow: trigger a test notification and confirm ticket creation
- PagerDuty: verify the integration key is current and test alert fires correctly
- Aria Operations CloudIQ MP: confirm adapter is in Collecting state
- SIEM: confirm audit log export job completed successfully
```
