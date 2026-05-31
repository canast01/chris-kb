# Aria Operations: Alert Definitions and Policies

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

Common threshold types:

| Symptom Type | Example Use Case |
|---|---|
| Metric / Property — Static Threshold | CPU Usage > 90% for 3 cycles |
| Metric / Property — Dynamic Threshold | Deviation from learned baseline (smart alerts) |
| Message Event | Specific log event received from adapter |
| Fault | Hardware fault reported by adapter |
| Property | VM snapshot age > 7 days |

## Alert Policies

Policies control which alerts are active, their priority, and notification routing. Every object belongs to a policy, with a **Default Policy** at the base.

Navigation: **Administration > Policies > Policy Library**

- Create child policies for specific clusters or datastores to override thresholds without modifying the global policy.
- Policy priority order: higher number = higher priority; child policies override parent policies for matching objects.

```bash
# List all policies
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/policies" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" | jq '.policy[] | {id, name, priority}'

# Assign a policy to a resource group via API
curl -sk -X PUT \
  "https://aria-ops.example.com/suite-api/api/policies/<policyId>/resources" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Content-Type: application/json" \
  -d '{"resourceIds": ["<resourceId>"]}'
```

## Alert Suppression and Maintenance Windows

Suppress alerts during maintenance to prevent noise flooding on-call channels.

Navigation: **Alerts > Active Alerts** — select alert(s) > **Suppress**

```bash
# Suppress an alert for 4 hours via API
# suppressUntilEpoch is milliseconds since epoch
SUPPRESS_UNTIL=$(( $(date +%s) * 1000 + 14400000 ))
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/alerts/suppress" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Content-Type: application/json" \
  -d "{\"alertIds\": [\"<alertId>\"], \"suppressUntilEpoch\": ${SUPPRESS_UNTIL}}"
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
