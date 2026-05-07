# ServiceNow Incidents

Incident lifecycle, SLA management, assignment rules, and escalation procedures.

## Incident Lifecycle

```
New → In Progress → On Hold → Resolved → Closed

New:         Ticket created; not yet assigned or acknowledged
In Progress: Assignee is actively working the issue
On Hold:     Waiting for external input (vendor, customer info)
Resolved:    Fix applied; awaiting confirmation from caller
Closed:      Caller confirmed resolution or auto-closed after N days
```

```bash
# Create an incident via REST API
curl -u user:token -X POST \
  "https://your-instance.service-now.com/api/now/table/incident" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "short_description": "prod-api-01: 503 errors spike — 14:32 UTC",
    "description": "Monitoring alert triggered. Error rate 45%. Impacting checkout flow.",
    "category": "application",
    "impact": "1",
    "urgency": "1",
    "caller_id": "jsmith",
    "assignment_group": "platform-team"
  }'

# Get an incident by number
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/incident" \
  --data-urlencode 'sysparm_query=number=INC0012345'
```

## Priority Matrix

Priority = f(Impact, Urgency)

| | Urgency 1 (Critical) | Urgency 2 (High) | Urgency 3 (Medium) | Urgency 4 (Low) |
|--|---------------------|-----------------|-------------------|----------------|
| Impact 1 (Enterprise) | P1 | P2 | P2 | P3 |
| Impact 2 (Department) | P2 | P2 | P3 | P3 |
| Impact 3 (Group) | P2 | P3 | P3 | P4 |
| Impact 4 (Individual) | P3 | P3 | P4 | P4 |

## SLA Targets

```bash
# Query SLA records for an incident
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/task_sla" \
  --data-urlencode 'sysparm_query=task.number=INC0012345' \
  --data-urlencode 'sysparm_fields=sla.name,has_breached,time_left,stop_time'

# List all breached SLAs
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/task_sla" \
  --data-urlencode 'sysparm_query=has_breached=true^task.active=true' \
  --data-urlencode 'sysparm_fields=task.number,sla.name,stage'
```

| Priority | Response SLA | Resolution SLA |
|----------|-------------|---------------|
| P1 | 15 minutes | 4 hours |
| P2 | 30 minutes | 8 hours |
| P3 | 2 hours | 3 business days |
| P4 | 8 hours | 7 business days |

## Assignment Rules

Incidents are auto-assigned based on:
- **Category** (Application, Network, Database, Security)
- **CI** (the affected configuration item routes to its owning group)
- **Keywords** in the short description

```bash
# Manually reassign an incident
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/incident/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "assignment_group": "network-ops",
    "assigned_to": "jdoe",
    "work_notes": "Reassigned to network-ops — suspected BGP issue"
  }'

# Query unassigned P1/P2 incidents
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/incident" \
  --data-urlencode 'sysparm_query=priority<=2^assigned_to=NULL^active=true' \
  --data-urlencode 'sysparm_fields=number,short_description,priority,opened_at'
```

## Escalation Procedures

```bash
# Flag an incident for escalation
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/incident/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "escalation": "1",
    "work_notes": "Escalating — no progress after 2 hours. Notified manager."
  }'
```

Escalation checklist for P1:
- [ ] On-call manager notified within 15 minutes
- [ ] Bridge/war room opened
- [ ] Status page updated (if customer-facing)
- [ ] Executive stakeholders notified at 30-minute mark
- [ ] Vendor engaged if internal resolution is blocked
- [ ] Incident commander assigned for P1 outages > 1 hour

## Resolving and Closing

```bash
# Resolve an incident
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/incident/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "6",
    "close_code": "Solved (Permanently)",
    "close_notes": "Root cause: memory leak in v2.3.0. Fixed in v2.3.1. Deployed 15:45 UTC.",
    "resolved_by": "jsmith"
  }'
```
