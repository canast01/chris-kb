# ServiceNow — Procedures


<div class="kb-summary">
Procedures reference covering Incidents, Incident Lifecycle, Priority Matrix, SLA Targets, Assignment Rules and 21 more sections.
</div>

## Incidents

Incident lifecycle, SLA management, assignment rules, and escalation procedures.

## Incident Lifecycle

```yaml
New → In Progress → On Hold → Resolved → Closed

New:         Ticket created; not yet assigned or acknowledged
In Progress: Assignee is actively working the issue
On Hold:     Waiting for external input (vendor, customer info)
Resolved:    Fix applied; awaiting confirmation from caller
Closed:      Caller confirmed resolution or auto-closed after N days
```
┌───────────────────────────────── ServiceNow — Operations Procedures ──────────────────────────────────┐
│                                                                                                       │
│  Standard operating procedures for day-to-day ServiceNow instance management.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              User Provisioning               │  │               Group Management              │   │
│   │        Create user → set role + group        │  │        Create group → assign members        │   │
│   │       Assign role via group membership       │  │        Group roles inherit to members       │   │
│   │    Disable user → revoke active sessions     │  │        Manager sets delegation rules        │   │
│   │         LDAP import → auto-provision         │  │       On-call rotation via rota tables      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    User and group changes → verify role inheritance and session cleanup                               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Catalog Management              │  │              Change Procedures              │   │
│   │       New item → variables + workflow        │  │      Change type: normal/standard/emrg      │   │
│   │        Publish after UAT in sub-prod         │  │       CAB approval for normal changes       │   │
│   │       Retire item → hide + close tasks       │  │         Post-impl review within 48 h        │   │
│   │       Variable sets reuse across items       │  │      Conflict detection via CI rel. map     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS · sub-prod instance · CAB meeting cadence · LDAP/AD                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LDAP import  = scheduled job pulls AD users into sys_user table                                      │
│  Variable set = reusable group of catalog variables shared across items                               │
│  Sub-prod     = non-production instance (dev/test) for safe UAT                                       │
│  Rota tables  = on-call schedule; drives escalation in incident rules                                 │
│  Delegation   = user sets absence delegate for approvals during leave                                 │
│  CAB          = Change Advisory Board; approves normal change records                                 │
│  Conflict det = system checks scheduled maintenance windows for overlaps                              │
│  Post-impl    = post-implementation review; closes PIR task within 48 h                               │
│  CI rel. map  = CMDB relationship map; shows impact of CIs for change                                 │
│  Emrg change  = emergency change; faster approval path for critical fixes                             │
│  Revoke sess  = user.invalidateSessions() clears active login tokens                                  │
│  Role inherit = group role automatically applies to all group members                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

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

---

## Changes

Change request workflow, change types (normal, standard, emergency), and CAB process.

## Change Types

| Type | Risk | Approval Required | Pre-approved | Examples |
|------|------|------------------|-------------|---------|
| Standard | Low | No (pre-approved) | Yes | Routine patching, password resets |
| Normal | Medium–High | Yes (CAB) | No | Infrastructure changes, deployments |
| Emergency | High | Emergency CAB | No | Production outage fixes |

## Change Request Fields

Key fields to populate when raising a change:

```yaml
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

```yaml
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

---

## Requests

Service catalog, request items, approval workflows, and fulfillment tracking.

## Service Catalog Overview

The Service Catalog is the self-service portal where users submit requests for IT services.

```text
Structure:
  Service Catalog
  └── Category (e.g., Infrastructure, Access, Software)
      └── Catalog Item (e.g., "Request new VM")
          └── Request (sc_request) — top-level record
              └── Request Item (sc_req_item) — one per catalog item ordered
                  └── Approval records
                  └── Tasks (sc_task) — fulfillment steps
```

```bash
# Query open requests for a user
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sc_request" \
  --data-urlencode 'sysparm_query=requested_for=jsmith^active=true' \
  --data-urlencode 'sysparm_fields=number,short_description,state,opened_at'

# Get request items for a request
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sc_req_item" \
  --data-urlencode 'sysparm_query=request.number=REQ0001234' \
  --data-urlencode 'sysparm_fields=number,cat_item,state,approval'
```

## Catalog Item Variables

Request items carry variables (the form fields the user filled in).

```bash
# Get variables for a request item
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sc_item_option_mtom" \
  --data-urlencode 'sysparm_query=request_item=RITM_SYS_ID' \
  --data-urlencode 'sysparm_fields=sc_item_option.item_option_new.question_text,sc_item_option.value'

# Create a request programmatically (submit a catalog item)
curl -u user:token -X POST \
  "https://your-instance.service-now.com/api/sn_sc/servicecatalog/items/CATALOG_ITEM_SYS_ID/order_now" \
  -H "Content-Type: application/json" \
  -d '{
    "sysparm_quantity": "1",
    "variables": {
      "environment": "dev",
      "instance_type": "t3.medium",
      "requested_by_date": "2025-05-15"
    }
  }'
```

## Approval Workflow

```bash
# Query pending approvals for a request
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sysapproval_approver" \
  --data-urlencode 'sysparm_query=sysapproval.number=REQ0001234^state=requested' \
  --data-urlencode 'sysparm_fields=approver,state,due_date'

# Approve a request item as the approver
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/sysapproval_approver/APPROVAL_SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{"state": "approved", "comments": "Approved for dev environment use"}'

# Reject an approval
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/sysapproval_approver/APPROVAL_SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{"state": "rejected", "comments": "Budget approval required first"}'
```

| Approval State | Meaning |
|---------------|---------|
| `requested` | Awaiting approver action |
| `approved` | Approver said yes |
| `rejected` | Approver said no — request cancelled |
| `not_required` | Auto-approved (below threshold) |
| `cancelled` | Request was cancelled before approval |

## Fulfillment Tasks

```bash
# List fulfillment tasks for a request item
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sc_task" \
  --data-urlencode 'sysparm_query=request_item.number=RITM0001234' \
  --data-urlencode 'sysparm_fields=number,short_description,state,assigned_to'

# Update a fulfillment task
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/sc_task/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "2",
    "work_notes": "VM provisioned in dev VPC. IP: 10.0.4.55"
  }'

# Close a fulfillment task
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/sc_task/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{"state": "3", "work_notes": "Confirmed by requester — closing task"}'
```

## Request SLAs and Monitoring

```bash
# Find overdue request items
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sc_req_item" \
  --data-urlencode 'sysparm_query=due_date<javascript:gs.now()^active=true^state!=3' \
  --data-urlencode 'sysparm_fields=number,cat_item,due_date,assigned_to,state'
```

| Request State | Numeric | Description |
|--------------|---------|-------------|
| Open | 1 | Not started |
| Work In Progress | 2 | Fulfillment underway |
| Closed Complete | 3 | Delivered successfully |
| Closed Incomplete | 4 | Could not fulfill |
| Closed Skipped | 7 | Skipped due to approval rejection |

---

## Work Notes

Work notes vs comments, resolution notes, audit trail, and best practices.

## Work Notes vs Comments (Additional Comments)

ServiceNow has two note fields on every ticket. Understanding the difference prevents accidental information disclosure.

| Field | Visible To | Triggers Notification | Use For |
|-------|-----------|----------------------|---------|
| Work Notes | Internal team only | Assignee group | Technical investigation, internal updates |
| Additional Comments | Requester / caller | Requester + team | Customer-facing communication |
| Resolution Notes | Requester | Yes (on resolve) | Summary of fix for the end user |

Never put credentials, internal IP addresses, or sensitive system details in Additional Comments.

## Adding Work Notes via API

```bash
# Add a work note to an incident
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/incident/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{"work_notes": "Checked error logs on prod-api-01. OOM kill at 14:28 UTC. Restarting service and monitoring."}'

# Add an additional comment (customer-visible)
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/incident/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{"comments": "We have identified the issue and are working on a fix. Expected resolution within 2 hours."}'

# Add a work note to a change request
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/change_request/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{"work_notes": "Step 1 complete: database backup verified. Proceeding to step 2."}'
```

## Work Note Best Practices

Good work notes make handoffs seamless and post-incident reviews accurate.

```bash
# Good work note format
[14:35 UTC] Checked nginx access logs — confirmed 503s starting 14:28 UTC
[14:40 UTC] Correlated with deployment at 14:25 UTC by @jsmith
[14:42 UTC] Rolled back to previous image. Error rate dropping.
[14:50 UTC] Error rate back to baseline 0.1%. Monitoring for 30 min before closing.
```

Work note checklist:
- Include timestamps in UTC
- Note who performed each action
- Record what was checked, not just what was done
- Log any commands run and their output if relevant
- Note what was ruled out (helps future investigators)

## Resolution Notes

Resolution notes are shown to the end user when a ticket is resolved. They should be jargon-free.

```bash
# Set resolution notes when closing an incident
curl -u user:token -X PATCH \
  "https://your-instance.service-now.com/api/now/table/incident/SYS_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "6",
    "close_code": "Solved (Permanently)",
    "close_notes": "A misconfigured deployment caused the service to run out of memory. We have rolled back to the previous version and applied a fix. The service has been stable since 15:00 UTC. We will deploy the corrected version during the next maintenance window."
  }'
```

## Reading the Audit Trail

The audit trail records every field change with the old value, new value, and who made the change.

```bash
# Get audit history for a record
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sys_audit" \
  --data-urlencode 'sysparm_query=documentkey=SYS_ID' \
  --data-urlencode 'sysparm_fields=fieldname,oldvalue,newvalue,sys_created_by,sys_created_on' \
  | jq '.result[] | {field: .fieldname, from: .oldvalue, to: .newvalue, by: .sys_created_by, at: .sys_created_on}'

# Get journal entries (work notes + comments) for a ticket
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sys_journal_field" \
  --data-urlencode 'sysparm_query=element_id=SYS_ID' \
  --data-urlencode 'sysparm_fields=name,element,value,sys_created_by,sys_created_on' \
  | jq '.result | sort_by(.sys_created_on)[] | {type: .element, author: .sys_created_by, time: .sys_created_on, note: .value}'
```

## Bulk Note Operations

```bash
# Add the same work note to multiple incidents (e.g., all P1s during a major outage)
INCIDENTS="INC0001 INC0002 INC0003"
NOTE="Major outage identified — root cause is BGP flap on core-rtr-01. Bridge open in #incident-bridge."

for INC in $INCIDENTS; do
  SYS_ID=$(curl -s -u user:token -G \
    "https://your-instance.service-now.com/api/now/table/incident" \
    --data-urlencode "sysparm_query=number=${INC}" \
    | jq -r '.result[0].sys_id')
  curl -s -u user:token -X PATCH \
    "https://your-instance.service-now.com/api/now/table/incident/${SYS_ID}" \
    -H "Content-Type: application/json" \
    -d "{\"work_notes\": \"${NOTE}\"}"
done
```

| Journal Type | `element` Value | Visibility |
|-------------|----------------|-----------|
| Work notes | `work_notes` | Internal only |
| Additional comments | `comments` | Customer-visible |
| Resolution notes | `close_notes` | Customer (on resolve) |
