# Dell AIOps: Actionable Recommendations and Implementation Tracking

```text
Recommendations — Dell AIOps
┌──────────────────────────────────────────┐
│  Analysis engine outputs                 │
│  ┌──────────────────────────────────┐    │
│  │ Type: Hardware                   │    │
│  │ Action: Replace drive slot 12    │    │
│  │ Priority: HIGH  │ Effort: LOW    │    │
│  └──────────────────────────────────┘    │
│  ┌──────────────────────────────────┐    │
│  │ Type: Config                     │    │
│  │ Action: Tune I/O queue depth     │    │
│  │ Priority: MEDIUM │ Effort: LOW   │    │
│  └──────────────────────────────────┘    │
│  ┌──────────────────────────────────┐    │
│  │ Type: Capacity                   │    │
│  │ Action: Expand pool (< 30 days)  │    │
│  │ Priority: HIGH   │ Effort: HIGH  │    │
│  └──────────────────────────────────┘    │
└─────────────────────┬────────────────────┘
                      ▼
          ┌─────────────────────┐
          │  Implement / Dismiss│
          │  Mark as done       │
          │  CloudIQ validates  │
          └─────────────────────┘
```
┌──────────────────────────────────── Dell AIOps — Recommendations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         AIOps AI generates recommendations from anomalies, insights, and health scores        │   │
│   │            Categories: Performance, Capacity, Availability, Security, Configuration           │   │
│   │               Priority: Critical → High → Medium → Low based on estimated impact              │   │
│   │          Each recommendation: problem, affected systems, steps, and expected outcome          │   │
│   │                     Status flow: Open → In Progress → Resolved / Dismissed                    │   │
│   │              Linked to ITSM: recommendation can trigger ServiceNow problem record             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Recommendations computed by AIOps ML engine · tracked in AIOps DB · exported via API                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Recommendation = AI-generated action linking a detected issue to a corrective step                   │
│  Priority = Urgency classification: Critical (act now)/High (act soon)/Medium/Low                     │
│  Affected systems = Infrastructure components contributing to the recommendation                      │
│  Expected outcome = Estimated improvement if recommendation is implemented                            │
│  In Progress = Status indicating team has started working on the recommendation                       │
│  Resolved = Recommendation closed; AIOps validates via subsequent telemetry                           │
│  Dismissed = Closed without action; requires reason comment for audit trail                           │
│  ServiceNow problem = ITSM record created from recommendation for tracking in change process          │
│  SLA = Internal target for acting on Critical recs (e.g., within 2 business days)                     │
│  Configuration rec = Flagging settings that deviate from Dell best practice baseline                  │
│  Weekly review = Dedicated recurring meeting to action or defer open recommendations                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Priority and effort matrix:

| Priority | Effort | Action |
|---|---|---|
| HIGH | LOW | Implement immediately — high value, low risk |
| HIGH | HIGH | Schedule in next change window |
| MEDIUM | LOW | Batch into routine maintenance |
| MEDIUM | HIGH | Evaluate carefully; may require planning |
| LOW | LOW | Implement opportunistically |
| LOW | HIGH | Defer unless other work requires it |

## Implementing Recommendations

Each recommendation includes a **Steps** tab with a numbered implementation procedure. For firmware updates, a link to the Dell EMC support portal download is included.

```bash
# Mark recommendation as in-progress
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/recommendations/<recId>/start" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Scheduled for change window CR-2026-0512"}'

# Mark recommendation as implemented
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/recommendations/<recId>/implement" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Applied firmware 5.3.1 — validated performance improvement"}'

# Dismiss recommendation (not applicable)
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/recommendations/<recId>/dismiss" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"reason": "NOT_APPLICABLE", "comment": "System decommissioning in 60 days"}'
```

## Implementation Tracking Dashboard

Navigation: **CloudIQ > AIOps > Recommendations > Summary**

| Column | Description |
|---|---|
| Total Active | Open recommendations requiring action |
| In Progress | Acknowledged and being implemented |
| Implemented (30d) | Completed in last 30 days |
| Dismissed | Accepted or deferred |
| Effectiveness Score | % of implemented recommendations that resolved the issue |

## Firmware Recommendation Workflow

When AIOps recommends a firmware update:
1. Note the current and target version in the recommendation detail.
2. Download the firmware from `support.dell.com` using the provided bundle ID.
3. Schedule a maintenance window.
4. Apply using the system's native update tool (e.g., PowerStore Manager, OneFS rolling upgrade).
5. Return to CloudIQ and mark as implemented.

```bash
# Check current firmware on all PowerStore systems via API
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage_systems?select=name,software_version&filter=type%20eq%20%27POWERSTORE%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {name, software_version}'
```

## Common Recommendation Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Recommendation reappears after implementation | Change not fully applied | Verify on system side; re-mark as implemented |
| Steps reference UI that no longer exists | Outdated recommendation content | Follow equivalent steps in current UI; submit feedback |
| Conflicting recommendations | Two models suggest opposing changes | Open a support case for guidance |
| No recommendations generated | System newly registered | Wait 7 days for analysis cycle |
