# ServiceNow Work Notes

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

```
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
