---
tags:
  - dell
description: "Dell AIOps Integration reference covering Overview, CloudIQ / SCG (Inbound Telemetry), Email and Webhook Notifications, SIEM Integration, Integration..."
---
# Dell AIOps Integration

<div class="kb-summary">
Dell AIOps Integration reference covering Overview, CloudIQ / SCG (Inbound Telemetry), Email and Webhook Notifications, SIEM Integration, Integration Summary and 1 more sections.

*Applies to: Dell AIOps*
</div>

```d2
direction: down

cloudiq_scg_inbound_telemetry: "CloudIQ / SCG (Inbound Telemetry)" {shape: rectangle}
siem_integration: "SIEM Integration" {shape: rectangle}
integration_summary: "Integration Summary" {shape: rectangle}
integration_health_checks: "Integration Health Checks" {shape: rectangle}

cloudiq_scg_inbound_telemetry -> siem_integration: uses
siem_integration -> integration_summary: uses
integration_summary -> integration_health_checks: uses
```

## Overview

Dell AIOps is integrated into the broader operational toolchain via CloudIQ's notification and API layers. All telemetry flows inbound through the Secure Connect Gateway; alerts and recommendations flow outbound to ITSM, notification, and observability platforms.

## CloudIQ / SCG (Inbound Telemetry)

All Dell storage systems must be registered in CloudIQ via the SCG. This is the prerequisite for all AIOps capabilities — without SCG-connected telemetry, AIOps has no data source.

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
