# ServiceNow Changes

Change request workflow, change types (normal, standard, emergency), and CAB process.

## Change Types

| Type | Risk | Approval Required | Pre-approved | Examples |
|------|------|------------------|-------------|---------|
| Standard | Low | No (pre-approved) | Yes | Routine patching, password resets |
| Normal | Medium–High | Yes (CAB) | No | Infrastructure changes, deployments |
| Emergency | High | Emergency CAB | No | Production outage fixes |

## Change Request Fields

Key fields to populate when raising a change:

```
Category:         Infrastructure / Application / Network / Security
Risk:             Low / Medium / High / Critical
Impact:           1 (Enterprise) to 4 (Minimal)
Assignment group: Platform / Network / Security
Planned start:    Date and time (UTC)
Planned end:      Date and time (UTC)
Short description: <Component>: <what is changing>
Description:      Full details including scope and method
```

```bash
# Create a change request via REST API
curl -u user:token -X POST \
  "https://your-instance.service-now.com/api/now/table/change_request" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "short_description": "Upgrade Postgres to 15.6 on prod-db-01",
    "category": "Database",
    "risk": "2",
    "impact": "2",
    "type": "normal",
    "assignment_group": "platform-team",
    "start_date": "2025-05-10 02:00:00",
    "end_date": "2025-05-10 04:00:00"
  }'

# Get a change request by number
curl -u user:token \
  "https://your-instance.service-now.com/api/now/table/change_request?number=CHG0012345"
```

## Normal Change Workflow

```
Draft → Assess → Authorize → Scheduled → Implement → Review → Closed

Draft:      Requester fills in all fields and attachments
Assess:     Change manager reviews risk, impact, and scope
Authorize:  CAB approves (or rejects) the change
Scheduled:  Change is confirmed for the maintenance window
Implement:  Work is performed; work notes updated in real time
Review:     Post-implementation review; confirm success or document issues
Closed:     Change closed as Successful / Unsuccessful / Cancelled
```

```bash
# Move a change to a new state
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/change_request/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{"state": "-1"}'   # -1 = Authorize, 0 = Scheduled, 1 = Implement
```

## Emergency Change Process

Emergency changes skip the standard CAB approval but require retrospective review.

```bash
# Create an emergency change
curl -u user:token -X POST \
  "https://your-instance.service-now.com/api/now/table/change_request" \
  -H "Content-Type: application/json" \
  -d '{
    "short_description": "Emergency: revert broken nginx config on prod-lb-01",
    "type": "emergency",
    "risk": "3",
    "justification": "Production outage since 14:32 UTC. Revert to last known good config."
  }'
```

Emergency CAB checklist:
- [ ] Incident ticket linked to the change
- [ ] On-call manager verbally approves before work starts
- [ ] Change notes updated with start time
- [ ] Post-implementation review scheduled within 48 hours

## CAB Preparation

```bash
# Query upcoming normal changes pending CAB review
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/change_request" \
  --data-urlencode 'sysparm_query=state=-1^type=normal' \
  --data-urlencode 'sysparm_fields=number,short_description,risk,start_date,assignment_group'

# Export CAB agenda to CSV
curl -s -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/change_request" \
  --data-urlencode 'sysparm_query=state=-1^type=normal' \
  --data-urlencode 'sysparm_fields=number,short_description,risk,start_date' \
  | jq -r '.result[] | [.number, .short_description, .risk, .start_date] | @csv'
```

| CAB Role | Responsibility |
|---------|---------------|
| Change Manager | Chairs meeting, final approval authority |
| Technical Lead | Assesses technical risk |
| Business Rep | Assesses business impact |
| Security Team | Reviews security-sensitive changes |
| Requester | Presents and answers questions |
