# CloudIQ: Proactive Recommendations and Implementation Tracking

```text
AI Recommendations — CloudIQ
┌──────────────────────────────────────┐
│  Telemetry analysis identifies waste │
│  or risk pattern                     │
└────────────────┬─────────────────────┘
                 ▼
┌──────────────────────────────────────┐
│  Recommendation generated            │
│  ┌──────────────────────────────┐    │
│  │ Category: Capacity           │    │
│  │ Priority: HIGH               │    │
│  │ Effort:   LOW                │    │
│  │ Action: thin reclaim on      │    │
│  │         vol03 (saves 2.1TB)  │    │
│  └──────────────────────────────┘    │
└────────────────┬─────────────────────┘
                 ▼
       ┌─────────────────┐
       │  Apply button   │  (guided steps in portal)
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │ Mark Implemented│ → CloudIQ validates next cycle
       └─────────────────┘
```

Dell CloudIQ generates proactive recommendations based on telemetry analysis, configuration assessment, and best practices. Categories include performance optimisation, energy savings, and configuration improvements. This page covers reviewing, implementing, and tracking recommendations.

## Recommendation Categories

Navigation: **CloudIQ > Recommendations**

| Category | Examples |
|---|---|
| Performance | Increase I/O queue depth, rebalance volumes across controllers |
| Capacity | Expand pool before projected full date |
| Data Reduction | Enable compression or deduplication on eligible volumes |
| Resiliency | Upgrade RAID level, replace at-risk drives pre-emptively |
| Configuration | Apply firmware updates, enable recommended settings |
| Energy Savings | Power down idle drives, enable MAID (Massive Array of Idle Disks) |
| Security | Enable at-rest encryption, rotate credentials |

## Viewing Active Recommendations

```bash
# List all active recommendations
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/recommendations?filter=state%20eq%20%27ACTIVE%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {id, category, title, impact, system_name}'

# Filter recommendations by category
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/recommendations?filter=category%20eq%20%27PERFORMANCE%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json"
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
