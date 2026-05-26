# Dell AIOps Integration
## Overview

Dell AIOps is integrated into the broader operational toolchain via CloudIQ's notification and API layers. All telemetry flows inbound through the Secure Connect Gateway; alerts and recommendations flow outbound to ITSM, notification, and observability platforms.

## CloudIQ / SCG (Inbound Telemetry)

All Dell storage systems must be registered in CloudIQ via the SCG. This is the prerequisite for all AIOps capabilities — without SCG-connected telemetry, AIOps has no data source.

```text
Verify collection status:
CloudIQ portal > Assets > [System] — check "Last Seen" timestamp
SCG admin UI > Systems > [System] > Connection Status
```
```

For Critical recommendations, target the **incident** table rather than change_request for immediate response.

## Aria Operations Integration

The Dell CloudIQ management pack for Aria Operations pulls AIOps health score and recommendation data into vROps, enabling correlated VMware + Dell storage views.

```text
Aria Operations > Admin > Solutions > Dell CloudIQ Management Pack
- API URL: https://api.cloudiq.dell.com
- Client ID / Secret: (from CloudIQ API client — read-only)
- Collection interval: 15 minutes
```

This integration allows correlating VM workload contention in Aria Operations with storage anomalies detected by Dell AIOps, enabling end-to-end root cause analysis across the VMware + Dell stack.

## Email and Webhook Notifications

```text
# Critical recommendations → PagerDuty
CloudIQ > Settings > Notifications > Rule: AIOps-Critical
- Trigger: Recommendation Severity = Critical
- Action: Webhook (PagerDuty Events API v2)

# High recommendations → Email + Teams
CloudIQ > Settings > Notifications > Rule: AIOps-High
- Trigger: Recommendation Severity = High
- Action: Email (storage-ops@company.com) + Webhook (Teams channel)
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
