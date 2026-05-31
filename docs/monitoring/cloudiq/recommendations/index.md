# CloudIQ: Proactive Recommendations and Implementation Tracking

```text
┌──────────────────────────────────── CloudIQ — AI Recommendations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           CloudIQ AI generates recommendations based on health issues and anomalies           │   │
│   │            Categories: Performance, Capacity, Availability, Security, Best Practice           │   │
│   │          Priority: Critical (act now), High (act soon), Medium (plan), Low (optional)         │   │
│   │          Each recommendation: problem description, impact, suggested action, KB link          │   │
│   │                    Track status: Open → In Progress → Resolved → Dismissed                    │   │
│   │         Resolution improves health score once Dell cloud receives confirming telemetry        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Recommendations computed in Dell cloud from fleet-wide ML · no on-prem component                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Recommendation = AI action item linking a detected issue to a corrective step                        │
│  Priority = Urgency classification: Critical/High/Medium/Low                                          │
│  KB link = Dell Knowledge Base article linked from recommendation for detailed steps                  │
│  Impact = Estimated health score improvement if recommendation is implemented                         │
│  In Progress = Status indicating team has started working on the recommendation                       │
│  Resolved = Recommendation marked done; CloudIQ validates via subsequent telemetry                    │
│  Dismissed = Recommendation closed without action; should include a reason comment                    │
│  Fleet-wide ML = Models trained on all registered Dell arrays globally for pattern matching           │
│  Best practice = Recommendation to align configuration with Dell recommended settings                 │
│  Security recommendation = Flagging insecure configuration (weak auth, unencrypted replication)       │
│  Confirming telemetry = Subsequent metric push showing issue condition no longer present              │
│  SLA = Internal target for acting on Critical/High recommendations (e.g., within 3 business days)     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Recommendation priority fields:

| Field | Values | Meaning |
|---|---|---|
| `priority` | HIGH, MEDIUM, LOW | Business impact if unaddressed |
| `effort` | LOW, MEDIUM, HIGH | Implementation complexity |
| `impact` | Description string | Expected outcome after implementation |
| `state` | ACTIVE, DISMISSED, IMPLEMENTED | Current status |

## Implementing a Recommendation

1. Navigate to the recommendation detail page.
2. Review the **Steps** tab for guided implementation instructions.
3. Click **Mark as Implemented** once the change is applied.
4. CloudIQ will validate the change in the next telemetry cycle and confirm effectiveness.

```bash
# Mark a recommendation as implemented via API
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/recommendations/<recId>/implement" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Completed by ops team, INC0054321"}'

# Dismiss a recommendation (accepted risk or not applicable)
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/recommendations/<recId>/dismiss" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Not applicable — system is scheduled for decommission"}'
```

## Energy Savings Recommendations

CloudIQ calculates estimated annual kWh savings for drive power-down and MAID recommendations.

| Recommendation | Typical Saving | Applicability |
|---|---|---|
| Enable drive spin-down for cold tiers | 5–15% drive power | NL-SAS drives in archive pools |
| Remove idle/powered-off arrays | Full array power | Confirmed decommission candidates |
| Right-temperature cooling zones | Varies | DataCenter DCIM integration required |

## Tracking Recommendation History

Implemented and dismissed recommendations are retained in history for auditing.

Navigation: **CloudIQ > Recommendations > History tab**

```bash
# View recommendation history (all states)
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/recommendations?filter=state%20ne%20%27ACTIVE%27&select=id,title,state,updated_at" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json"
```

## Common Recommendation Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| No recommendations appearing | New system, insufficient history | Wait 7+ days for telemetry analysis |
| Recommendation keeps reappearing | Not fully implemented | Verify change was applied on system side |
| Incorrect impact estimate | Edge case in analytics model | Dismiss with note, open feedback via support portal |
| Firmware recommendation not applying | System in production, change window needed | Schedule and mark as in-progress with comment |
