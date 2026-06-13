---
tags:
  - dell
  - operations
---
# CloudIQ: Alert Types, Severity, and Notification Configuration


<div class="kb-summary">
CloudIQ: Alert Types, Severity, and Notification Configuration reference covering Notification Configuration, Dismissing and Acknowledging Alerts, Common Alert Issues.
</div>

```text
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

## Common Alert Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| No alerts appearing | System not registered or phone-home blocked | Check system connectivity and SRS/ESRS config |
| Email notifications not received | Recipient not added or spam filter | Verify recipients in Settings > Notifications |
| Alerts not clearing after fix | System has not reported resolved state | Wait for next telemetry cycle (up to 30 min) |
| Duplicate alerts for same event | Multiple notification rules overlapping | Review and deduplicate notification rules |
| Historical alerts missing | Retention limit reached | CloudIQ retains 90 days of alert history by default |
