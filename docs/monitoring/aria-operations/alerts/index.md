# Aria Operations: Alert Definitions and Policies

```
Alert Lifecycle — Aria Operations
┌──────────────────┐
│ Metric threshold │  (symptom fires for N cycles)
│   violation      │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Alert Definition │  (symptom AND/OR logic evaluated)
│  matched         │
└────────┬─────────┘
         ▼
┌──────────────────┐
│  Alert created   │  criticality: Critical / Immediate / Warning
│  (Active state)  │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Notification     │  policy routes alert
│  Policy match    │
└────────┬─────────┘
         │
    ┌────┴──────────┬──────────────┐
    ▼               ▼              ▼
┌────────┐   ┌──────────┐  ┌────────────┐
│ Email  │   │  Ticket  │  │   SNMP     │
│ (SMTP) │   │  (REST   │  │   Trap     │
│        │   │ webhook) │  │            │
└────────┘   └──────────┘  └────────────┘
```

VMware Aria Operations (formerly vRealize Operations) generates alerts based on symptom definitions, recommendations, and policies. This page covers creating alert definitions, configuring thresholds, managing suppression, and applying alert policies.

## Alert Anatomy: Symptoms and Definitions

Alerts are composed of one or more **symptoms**. A symptom fires when a metric crosses a threshold or a property matches a condition. Alert definitions group symptoms using AND/OR logic.

Navigation: **Alerts > Alert Definitions > Add**

Key fields when creating an alert definition:

| Field | Description |
|-------|-------------|
| Base Object Type | The resource kind the alert applies to (e.g., Virtual Machine) |
| Impact | Availability, Performance, Capacity, Compliance, or Efficiency |
| Criticality | Critical, Immediate, Warning, Information |
| Wait Cycle | How many collection cycles a symptom must be true before firing |
| Cancel Cycle | How many cycles must be false before the alert cancels |

## Symptom Definitions and Thresholds

Symptom definitions live under **Alerts > Symptom Definitions**. Metric symptoms compare a collected metric against a static or dynamic threshold.

```bash
# Export all alert definitions via REST API
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/alertdefinitions" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" | jq '.alertDefinitions[].name'

# Get symptom definitions for Virtual Machine object type
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/symptomdefinitions?adapterKind=VMWARE&resourceKind=VirtualMachine" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" | jq '.symptomDefinitions[] | {id, name}'
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
