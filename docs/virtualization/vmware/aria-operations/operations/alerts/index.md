---
tags:
  - aria-operations
  - operations
  - vmware
---
# Aria Operations: Alert Definitions and Policies


<div class="kb-summary">
Aria Operations: Alert Definitions and Policies reference covering Alert Policies, Alert Suppression and Maintenance Windows, Notification Rules and Outbound Plugins, Common Alert Issues.

*Applies to: Aria Ops 8.x*
</div>

```text
┌────────────────────────────────────── Aria Operations — Alerts ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Aria Operations Alert Framework — Symptoms, Recommendations, and Outbound Actions       │   │
│   │             Alert anatomy: Alert Definition → Symptom(s) → Recommendation → Action            │   │
│   │       Symptoms: metric threshold · property change · event (fault/task) · message event       │   │
│   │          Impact: Health · Risk · Efficiency — each drives different response priority         │   │
│   │           Outbound: email · REST · ServiceNow · SNMP trap · Log Insight notification          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Impact type drives dashboard placement: Health=Ops board · Risk=Capacity board                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Symptom Types        │  │         Impact Types        │  │       Outbound Actions      │   │
│   │       Metric threshold      │  │        Health impact        │  │          Email SMTP         │   │
│   │       Property change       │  │         Risk impact         │  │         REST webhook        │   │
│   │        Event (fault)        │  │      Efficiency impact      │  │      ServiceNow ticket      │   │
│   │        Message event        │  │       Criticality 1-5       │  │          SNMP trap          │   │
│   │         KPI symptom         │  │       Wait cycle conf       │  │      Log Insight notify     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Alert engine runs on Aria Ops master node · outbound connectors configured in Administration         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Alert definition  = Named policy grouping one or more symptoms with a recommendation                 │
│  Symptom           = Specific condition triggering an alert (metric, property, event, message)        │
│  Recommendation    = Suggested remediation step linked to an alert definition                         │
│  Health impact     = Alert affecting current operational state (e.g. CPU critical)                    │
│  Risk impact       = Alert indicating future degradation (e.g. disk will fill in 7 days)              │
│  Efficiency impact = Alert flagging resource waste (e.g. oversized idle VMs)                          │
│  Criticality       = 1-5 scale; 1=Critical, 5=Info; drives UI badge colour                            │
│  Wait cycle        = Number of collection cycles a symptom must persist before alert fires            │
│  KPI symptom       = Symptom based on a KPI metric defined in a dashboard super metric                │
│  Super metric      = Custom metric formula combining multiple raw metrics                             │
│  Cancel alert      = Manual or automated resolution of an active alert                                │
│  Outbound action   = Configured connector sending alert payload to external system                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Suppression rules can also be set at the policy level to automatically suppress alerts for objects placed in maintenance mode.

## Notification Rules and Outbound Plugins

Notifications route alert data to email, PagerDuty, SNMP traps, or webhooks.

Navigation: **Administration > Outbound Settings**

| Plugin Type | Use Case |
|---|---|
| Email / SMTP | Alert digest emails, on-call distribution lists |
| REST Notification | Webhook to ServiceNow, Slack, or PagerDuty |
| SNMP Trap | Legacy NMS integration |
| Log File | Local log forwarding for SIEM ingestion |

Notification rules filter by: object type, alert criticality, alert definition name, and policy.

## Common Alert Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Alert fires then immediately cancels | Wait/cancel cycle too low | Increase wait cycle to 3+ |
| Duplicate alerts flooding inbox | No cancel cycle configured | Set cancel cycle to 1 or 2 |
| Alert not firing despite threshold breach | Object not in correct policy | Verify policy assignment in object details |
| Notification not delivered | Outbound plugin misconfigured | Test plugin under Outbound Settings |
| Smart alert thresholds unpredictable | Insufficient data history | Allow 30+ days for baseline learning period |
| Adapter alerts missing | Adapter not collecting | Check adapter instance status under Administration |
