# CloudIQ: Alert Types, Severity, and Notification Configuration

```text
Proactive Alert Flow — CloudIQ
┌─────────────────────────────┐
│  System telemetry (SRS)     │  (PowerStore / PowerMax / PowerScale)
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  CloudIQ AI/ML engine       │  detects anomaly or threshold breach
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  Alert created              │
│  ┌────────────────────────┐ │
│  │ Severity: Critical     │ │
│  │ Root cause identified  │ │
│  │ Recommended action     │ │
│  └────────────────────────┘ │
└──────────────┬──────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌────────────┐   ┌─────────────┐
│  Email     │   │   Portal    │
│ notification│  │  (CloudIQ   │
│  (distro)  │   │   UI)       │
└────────────┘   └─────────────┘
```

Dell CloudIQ surfaces alerts from connected storage, data protection, networking, and hyperconverged infrastructure systems. This page covers alert types, severity levels, notification setup, and dismissal workflows.

## Alert Types and Sources

CloudIQ aggregates alerts from all registered systems. Alerts are sourced from the hardware itself (telemetry pushed via phone-home) and enriched by CloudIQ's analytics engine.

Navigation: **CloudIQ > Alerts**

| Alert Source | Examples |
|---|---|
| PowerStore | Drive failure, replication lag, pool near-full |
| PowerMax / VMAX | Director offline, SRDF link degraded |
| PowerScale (Isilon) | Node down, quota exceeded, SRS connectivity |
| PowerProtect / Avamar | Job failure, catalogue corruption, capacity |
| PowerEdge Servers | Drive predictive failure, RAID degradation |
| PowerSwitch | Port down, STP topology change |

## Severity Levels

| Severity | Colour | Meaning | Response Time |
|---|---|---|---|
| Critical | Red | System or service impact is occurring | Immediate |
| Major | Orange | Risk of imminent impact | Within 1 hour |
| Minor | Yellow | Degraded state, no immediate impact | Business hours |
| Informational | Blue | Configuration or state change logged | Review when convenient |

## Viewing and Filtering Alerts

```bash
# Query active alerts via CloudIQ REST API v1
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/alerts?filter=state%20eq%20%27ACTIVE%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {id, severity, summary, system_name}'

# Filter by severity
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/alerts?filter=severity%20eq%20%27CRITICAL%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json"
```

## Notification Configuration

CloudIQ sends alert notifications via email. Configure recipients at the tenant level.

Navigation: **CloudIQ > Settings > Notifications**

Steps to configure email alerts:
1. Go to **Settings > Notifications > Alert Notifications**.
2. Click **+ Add Recipient**.
3. Enter email address and select severity threshold.
4. Choose specific systems or **All Systems**.
5. Save and send a test notification.

| Option | Description |
|---|---|
| Severity Threshold | Minimum severity that triggers an email |
| System Scope | All systems, or specific registered systems |
| Digest vs Immediate | Send each alert individually or in a daily digest |
| Test Notification | Sends a synthetic alert to verify delivery |

## Dismissing and Acknowledging Alerts

Alerts can be dismissed when the issue is known and accepted, or acknowledged to indicate someone is investigating.

```bash
# Acknowledge an alert via API
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/alerts/<alertId>/acknowledge" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Investigating - ticket INC0012345"}'

# Dismiss an alert
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/alerts/<alertId>/dismiss" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Accepted risk - hardware replacement scheduled"}'
```

## Common Alert Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| No alerts appearing | System not registered or phone-home blocked | Check system connectivity and SRS/ESRS config |
| Email notifications not received | Recipient not added or spam filter | Verify recipients in Settings > Notifications |
| Alerts not clearing after fix | System has not reported resolved state | Wait for next telemetry cycle (up to 30 min) |
| Duplicate alerts for same event | Multiple notification rules overlapping | Review and deduplicate notification rules |
| Historical alerts missing | Retention limit reached | CloudIQ retains 90 days of alert history by default |
