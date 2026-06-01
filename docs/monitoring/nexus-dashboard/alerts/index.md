# Nexus Dashboard: Fabric Alerts, Severity, Acknowledgement, and Notification Policies


<div class="kb-summary">
Nexus Dashboard: Fabric Alerts, Severity, Acknowledgement, and Notification Policies reference covering Acknowledging Alerts, Notification Policies, Alert Suppression During Maintenance, Common Alert Issues.
</div>

```text
┌────────────────────────────────────── Nexus Dashboard — Alerts ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             NDI Alert Categories             │                 Alert Actions                  │   │
│   │            Anomaly: ML deviation             │               Acknowledge: seen                │   │
│   │         Compliance: policy mismatch          │              Assign: to engineer               │   │
│   │            Health: score degraded            │             Suppress: known issue              │   │
│   │          Bug: known Cisco SW defect          │               Create ITSM ticket               │   │
│   │            Delta: config changed             │                Export for audit                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  NDI generates alerts from telemetry · delivered via ND console, email, webhook                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Anomaly = NDI ML deviation from baseline; may indicate failure or misconfiguration                   │
│  Compliance = ACI EPG/contract or NX-OS configuration deviating from verified state                   │
│  Health alert = NDI site/fabric health score dropping below threshold                                 │
│  Bug = NDI matching observed symptoms to Cisco known defect database                                  │
│  Delta = Change event; NDI showing what configuration changed and when                                │
│  Acknowledge = Engineer marks alert as seen; stops re-notification                                    │
│  Suppress = Muting known benign alert for a defined period                                            │
│  ITSM ticket = ServiceNow incident created from NDI alert via webhook                                 │
│  Severity = Critical/Major/Minor/Warning; routes to different teams                                   │
│  Affected epoch = NDI time window during which anomaly was detected                                   │
│  Impact = NDI assessment of scope (how many objects affected)                                         │
│  Root cause = NDI correlation linking symptom to underlying network event                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Notification Policies

Nexus Dashboard can send alert notifications via email or syslog.

Navigation: **Nexus Dashboard > Admin > Notifications > Alert Notification**

| Notification Channel | Configuration Path | Use Case |
|---|---|---|
| Email | Admin > Notifications > Email | On-call engineer alerts |
| Syslog | Admin > Notifications > Syslog | SIEM ingestion |
| REST webhook | (via third-party integration) | ServiceNow, PagerDuty |

Email notification configuration:
1. Navigate to **Admin > System Settings > Notifications**.
2. Click **+ Add Email Receiver**.
3. Set SMTP server, port, sender address.
4. Define a notification rule: minimum severity, fabric scope.
5. Test with **Send Test Email**.

## Alert Suppression During Maintenance

For planned maintenance windows, suppress alerts to avoid notification fatigue:

Navigation: **Insights > Alerts > Suppress Alerts**

```bash
# Create a suppression window via API
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/suppressions" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "fabric-upgrade-window",
    "fabricName": "prod-aci-fabric",
    "startTime": "2026-05-10T22:00:00Z",
    "endTime": "2026-05-11T04:00:00Z",
    "reason": "Planned firmware upgrade"
  }'
```

## Common Alert Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Duplicate alerts for same interface | Multiple collection cycles before resolution | Increase de-duplication window in NDI settings |
| Alerts not cleared after fix | Telemetry not yet updated | Wait one collection cycle (default 5 min) |
| No alerts in UI | NDI service not receiving telemetry | Check switch telemetry config and NDI connectivity |
| Email not delivered | SMTP relay not reachable from ND VM | Verify network path and SMTP server configuration |
| Historical alerts missing | Alert retention policy set too low | Increase retention in Admin > System Settings |
