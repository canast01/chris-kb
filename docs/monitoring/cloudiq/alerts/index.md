# CloudIQ: Alert Types, Severity, and Notification Configuration

```
┌────────────────────────────────────────── CloudIQ — Alerts ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Alert Categories               │                 Alert Actions                  │   │
│   │          Health: score < threshold           │           Acknowledge: mark as seen            │   │
│   │          Capacity: fill date < 90d           │            Snooze: mute for N hours            │   │
│   │          Performance: latency spike          │          Dismiss: remove if false-pos          │   │
│   │          Hardware: component fault           │             Create service request             │   │
│   │            Anomaly: ML deviation             │             Link to recommendation             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Alerts generated in Dell cloud · delivered via email/webhook · viewed at cloudiq.dell.com            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Alert = CloudIQ notification for a condition requiring attention on an array                         │
│  Health alert = Fired when array health score drops below configured threshold                        │
│  Capacity alert = Fired when projected full date is within defined horizon (default 90 days)          │
│  Performance alert = Fired when latency or IOPS deviates significantly from baseline                  │
│  Hardware alert = Firmware-detected component fault forwarded via telemetry                           │
│  Anomaly alert = ML-detected statistical deviation not matching known fault pattern                   │
│  Acknowledge = Confirms alert reviewed; suppresses repeat notification                                │
│  Snooze = Temporary suppression for a defined window; re-fires after window expires                   │
│  Dismiss = Permanent closure of alert; used for confirmed false-positives                             │
│  Service request = Dell support case created from CloudIQ alert with pre-populated diagnostics        │
│  Recommendation = AI-generated fix linked to alert; addresses root cause                              │
│  Severity = Alert priority: Critical, Warning, Informational                                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
