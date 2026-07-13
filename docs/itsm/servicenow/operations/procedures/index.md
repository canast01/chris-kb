---
tags:
  - operations
  - servicenow
---
# ServiceNow — Operations Procedures

```yaml
New → In Progress → On Hold → Resolved → Closed

New:         Ticket created; not yet assigned or acknowledged
In Progress: Assignee is actively working the issue
On Hold:     Waiting for external input (vendor, customer info)
Resolved:    Fix applied; awaiting confirmation from caller
Closed:      Caller confirmed resolution or auto-closed after N days
```

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

```text title="Expected output"
{
  "result": {
    "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "number": "INC0010847",
    "assignment_group": "network-ops",
    "assigned_to": "jdoe",
    "work_notes": "Reassigned to network-ops — suspected BGP issue",
    "sys_updated_on": "2024-01-15 14:32:18"
  }
}
{
  "result": [
    {
      "number": "INC0010851",
      "short_description": "Database replication lag detected on prod-db-02",
      "priority": "1",
      "opened_at": "2024-01-15 13:47:22"
    },
    {
      "number": "INC0010849",
      "short_description": "VPN gateway failover incomplete",
      "priority": "2",
      "opened_at": "2024-01-15 12:15:09"
    },
    {
      "number": "INC0010848",
      "short_description": "Load balancer health check failures",
      "priority": "1",
      "opened_at": "2024-01-15 11:53:44"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `{"error":{"message":"Invalid table API (incident)","status":"failure"}}` | Verify the ServiceNow instance URL and that the REST API is enabled for the incident table. |
    | `{"error":{"message":"Invalid field name (assigned_to)","status":"failure"}}` | Use the correct field name `assignment_group` or check your instance's field naming convention; some instances use `assigned_to_user` instead. |
    | `curl: (7) Failed to connect to your-instance.service-now.com port 443: Connection refused` | Replace `your-instance` with your actual ServiceNow instance hostname (e.g., `dev12345.service-now.com`). |
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

```text title="Expected output"
{
  "result": {
    "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "number": "INC0010847",
    "short_description": "Database connection timeout on prod-db-03",
    "state": "2",
    "escalation": "1",
    "escalation_time": "2024-01-15 14:32:18",
    "work_notes": "Escalating — no progress after 2 hours. Notified manager.",
    "assigned_to": "62826bf03710200044e0bfc578601e57",
    "assignment_group": "Database Support Team",
    "priority": "2",
    "updated_on": "2024-01-15 14:32:18"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `401 Unauthorized` | Verify your ServiceNow instance URL, username, and API token are correct and the token has not expired. |
    | `404 Not Found` | Replace `SYS_ID` with the actual incident system ID (e.g., `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`). |
    | `403 Forbidden` | Confirm your user account has the `incident_write` or `admin` role in ServiceNow to modify incidents. |
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

```text title="Expected output"
{
  "result": {
    "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "number": "CHG0010847",
    "state": "-1",
    "short_description": "Database patch deployment",
    "assignment_group": "Change Management",
    "assigned_to": "admin@company.com",
    "created_on": "2024-01-15 09:23:45",
    "updated_on": "2024-01-15 14:52:12",
    "status": "Authorize"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.service-now.com port 443: Name or service not known` | Replace `your-instance` with your actual ServiceNow instance name (e.g., `dev123456`). |
    | `{"error":{"message":"Invalid field value","detail":"Invalid state value: -1"},"status":"failure"}` | Verify the state value is valid for your change type; some change models may not support the Authorize state. |
    | `{"error":{"message":"Invalid table API (change_request)"},"status":"failure"}` | Confirm the table name is correct; use `change_request` for standard changes or check your instance's custom change table name. |
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

```text title="Expected output"
{
  "result": {
    "sys_id": "a7f2c8d9e1b4a5f6c9d2e3f4a5b6c7d8",
    "number": "CHG0087543",
    "short_description": "Emergency: revert broken nginx config on prod-lb-01",
    "type": "emergency",
    "risk": "3",
    "state": "1",
    "created_on": "2024-01-15 14:35:22",
    "created_by": "user",
    "assignment_group": "Infrastructure Team",
    "status": "pending_approval"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: your-instance.service-now.com` | Replace `your-instance` with your actual ServiceNow instance hostname (e.g., `dev12345.service-now.com`). |
    | `{"error":{"message":"Invalid table API (change_request)","status":"failure"},"status":"failure"}` | Verify the correct table name is `change_request` and your API version supports it; check ServiceNow instance REST API documentation. |
    | `{"error":{"message":"Invalid field value [type=emergency]","status":"invalid_field_value"}}` | Use valid change type values from your instance (typically `standard`, `normal`, or `emergency`); check your change_request table field definitions. |
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

```text title="Expected output"
{
  "result": [
    {
      "number": "CHG0042857",
      "short_description": "Database connection pool upgrade to v8.2",
      "risk": "medium",
      "start_date": "2024-01-15 02:00:00",
      "assignment_group": "Database Team"
    },
    {
      "number": "CHG0042891",
      "short_description": "Load balancer SSL certificate renewal",
      "risk": "low",
      "start_date": "2024-01-16 23:30:00",
      "assignment_group": "Network Operations"
    },
    {
      "number": "CHG0042903",
      "short_description": "Kubernetes cluster patch 1.28.4",
      "risk": "high",
      "start_date": "2024-01-18 01:00:00",
      "assignment_group": "Platform Engineering"
    }
  ]
}
"CHG0042857","Database connection pool upgrade to v8.2","medium","2024-01-15 02:00:00"
"CHG0042891","Load balancer SSL certificate renewal","low","2024-01-16 23:30:00"
"CHG0042903","Kubernetes cluster patch 1.28.4","high","2024-01-18 01:00:00"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.service-now.com port 443: Connection refused` | Replace `your-instance` with your actual ServiceNow instance hostname (e.g., `acme-dev.service-now.com`). |
    | `{"error":{"message":"Invalid table API (change_request)","status":"failure"},"status":"failure"}` | Verify the table name is correct; use `change_request` or check your instance's table naming convention via the ServiceNow API explorer. |
    | `jq: parse error: Invalid numeric literal at line 1 column 7` | Ensure the API response is valid JSON by checking authentication credentials and that the `-s` flag is present to suppress curl progress output. |
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

```text title="Expected output"
{
  "result": [
    {
      "number": "REQ0001847",
      "short_description": "Laptop provisioning request",
      "state": "1",
      "opened_at": "2024-01-15 09:23:45"
    },
    {
      "number": "REQ0001823",
      "short_description": "VPN access for contractor",
      "state": "2",
      "opened_at": "2024-01-14 14:12:30"
    },
    {
      "number": "REQ0001801",
      "short_description": "Software license renewal",
      "state": "1",
      "opened_at": "2024-01-12 11:05:18"
    }
  ]
}
{
  "result": [
    {
      "number": "RITM0010456",
      "cat_item": "Laptop - Standard Build",
      "state": "On Hold",
      "approval": "Approved"
    },
    {
      "number": "RITM0010457",
      "cat_item": "Windows 11 Pro License",
      "state": "Pending",
      "approval": "Pending"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: your-instance.service-now.com` | Replace `your-instance` with your actual ServiceNow instance name (e.g., `dev123456`). |
    | `{"error":{"message":"Invalid table API (sc_request)","status":"failure"},"status":"failure"}` | Verify the table name is correct and your API user has read access to the sc_request table in ServiceNow. |
    | `{"error":{"message":"Invalid query: requested_for=jsmith^active=true","status":"failure"}}` | Ensure field names and query syntax match your ServiceNow instance schema; use the ServiceNow API explorer to validate field names. |
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

```text title="Expected output"
{
  "result": [
    {
      "sc_item_option": {
        "item_option_new": {
          "question_text": "Select Environment"
        },
        "value": "dev"
      },
      "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2"
    },
    {
      "sc_item_option": {
        "item_option_new": {
          "question_text": "Instance Type"
        },
        "value": "t3.medium"
      },
      "sys_id": "m2n3o4p5q6r7s8t9u0v1w2x3"
    }
  ]
}
{
  "result": {
    "request_number": "REQ0010847",
    "sys_id": "7f8g9h0i1j2k3l4m5n6o7p8q",
    "status": "pending_approval",
    "order_id": "ORD0005623",
    "message": "Request submitted successfully"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host name` | Verify the ServiceNow instance URL is correct and replace `your-instance` with your actual instance name. |
    | `{"error":{"message":"Invalid table API (Invalid Offset)","status":"failure"}}` | Ensure the RITM_SYS_ID and CATALOG_ITEM_SYS_ID are valid sys_id values from your ServiceNow instance. |
    | `{"error":{"message":"Invalid request. User does not have permission to access this API","status":"failure"}}` | Confirm the API user account has the `catalog_admin` or `itil` role and appropriate table ACLs in ServiceNow. |
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

```text title="Expected output"
{
  "result": [
    {
      "approver": "john.smith@company.com",
      "state": "requested",
      "due_date": "2024-01-15 17:00:00",
      "sys_id": "e8d4a5f2c1b9e3a7d2f5c8a1b4e7f0d3"
    },
    {
      "approver": "sarah.jones@company.com",
      "state": "requested",
      "due_date": "2024-01-15 17:00:00",
      "sys_id": "f9e5b6g3d2c0f4b8e3g6d9b2c5f8a1e4"
    }
  ]
}

{
  "result": {
    "sys_id": "e8d4a5f2c1b9e3a7d2f5c8a1b4e7f0d3",
    "state": "approved",
    "comments": "Approved for dev environment use",
    "updated_on": "2024-01-12 09:34:22"
  }
}

{
  "result": {
    "sys_id": "f9e5b6g3d2c0f4b8e3g6d9b2c5f8a1e4",
    "state": "rejected",
    "comments": "Budget approval required first",
    "updated_on": "2024-01-12 09:35:18"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.service-now.com port 443: Connection refused` | Replace `your-instance` with your actual ServiceNow instance hostname (e.g., `dev12345.service-now.com`). |
    | `{"error":{"message":"Invalid table API (Invalid Referral Record)","status":"failure"},"status":"failure"}` | Verify the `APPROVAL_SYS_ID` is a valid sys_id from the query results; use the exact value from the first API call's response. |
    | `{"error":{"message":"Invalid field name: state","status":"failure"}}` | Confirm the field name is `state` (not `status`); check your ServiceNow instance's sysapproval_approver table schema for correct field names. |
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

```text title="Expected output"
{
  "result": [
    {
      "number": "TASK0010456",
      "short_description": "Provision Ubuntu 20.04 VM",
      "state": "1",
      "assigned_to": {
        "display_value": "alice.chen@company.com",
        "value": "46d44a23c0a8016700b2d4be33ee4019"
      }
    },
    {
      "number": "TASK0010457",
      "short_description": "Configure network security group",
      "state": "1",
      "assigned_to": {
        "display_value": "bob.martinez@company.com",
        "value": "62f8c41ac0a8016700c3e5cf44ff5021"
      }
    }
  ]
}
{
  "result": {
    "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "number": "TASK0010456",
    "state": "2",
    "work_notes": "VM provisioned in dev VPC. IP: 10.0.4.55"
  }
}
{
  "result": {
    "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "number": "TASK0010456",
    "state": "3",
    "work_notes": "Confirmed by requester — closing task"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Invalid table API (Invalid table: sc_task)` | Verify the ServiceNow instance URL and API version; use `/api/now/v2/table/sc_task` if on a newer instance. |
    | `401 Unauthorized` | Confirm the API user credentials and token are correct, and that the user has the `itil` or `sn_request_read` role. |
    | `Invalid field name: SYS_ID` | Replace `SYS_ID` with the actual task system ID (e.g., `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`) from the GET response. |
```bash
# Find overdue request items
curl -u user:token -G \
  "https://your-instance.service-now.com/api/now/table/sc_req_item" \
  --data-urlencode 'sysparm_query=due_date<javascript:gs.now()^active=true^state!=3' \
  --data-urlencode 'sysparm_fields=number,cat_item,due_date,assigned_to,state'
```

```text title="Expected output"
{
  "result": [
    {
      "number": "REQ0010234",
      "cat_item": "Software License Renewal",
      "due_date": "2024-01-15 09:30:00",
      "assigned_to": "john.smith",
      "state": "1"
    },
    {
      "number": "REQ0010198",
      "cat_item": "Hardware Provisioning",
      "due_date": "2024-01-12 14:22:00",
      "assigned_to": "sarah.jones",
      "state": "2"
    },
    {
      "number": "REQ0010156",
      "cat_item": "Access Request",
      "due_date": "2024-01-10 11:15:00",
      "assigned_to": "mike.chen",
      "state": "1"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.service-now.com port 443: Connection refused` | Replace `your-instance` with your actual ServiceNow instance hostname (e.g., `dev12345.service-now.com`). |
    | `{"error":{"message":"Invalid table API GET request","status":"failure"},"status":"failure"}` | Verify the table name is correct; use `sc_request` for requests or `sc_req_item` for request items, and confirm your user has table API read access. |
    | `{"error":{"message":"Invalid query: due_date<javascript:gs.now()","status":"failure"}}` | Replace the JavaScript function with a valid ISO date string like `due_date<2024-01-20` or use the REST API's native query syntax without `javascript:` prefix. |
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

```text title="Expected output"
{
  "result": {
    "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2",
    "number": "INC0010156",
    "short_description": "Production API service OOM crash",
    "state": "2",
    "work_notes": "Checked error logs on prod-api-01. OOM kill at 14:28 UTC. Restarting service and monitoring.",
    "work_notes_list": [
      {
        "element": "work_notes",
        "element_id": "a1b2c3d4e5f6g7h8i9j0k1l2",
        "sys_created_on": "2024-01-15 14:32:18",
        "value": "Checked error logs on prod-api-01. OOM kill at 14:28 UTC. Restarting service and monitoring."
      }
    ]
  }
}
{
  "result": {
    "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2",
    "number": "INC0010156",
    "comments": "We have identified the issue and are working on a fix. Expected resolution within 2 hours.",
    "comments_list": [
      {
        "element": "comments",
        "element_id": "a1b2c3d4e5f6g7h8i9j0k1l2",
        "sys_created_on": "2024-01-15 14:33:05",
        "value": "We have identified the issue and are working on a fix. Expected resolution within 2 hours."
      }
    ]
  }
}
{
  "result": {
    "sys_id": "b2c3d4e5f6g7h8i9j0k1l2m3",
    "number": "CHG0005847",
    "type": "standard",
    "state": "in_progress",
    "work_notes": "Step 1 complete: database backup verified. Proceeding to step 2.",
    "work_notes_list": [
      {
        "element": "work_notes",
        "element_id": "b2c3d4e5f6g7h8i9j0k1l2m3",
        "sys_created_on": "2024-01-15 14:34:22",
        "value": "Step 1 complete: database backup verified. Proceeding to step 2."
      }
    ]
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Invalid table API (Invalid table name [incident])` | Verify the table name is correct (use `incident` for incidents, `change_request` for changes) and check your ServiceNow instance API version supports the endpoint. |
    | `401 Unauthorized` | Confirm your API user credentials and token are valid, and that the user has the `itil` or `admin` role with API access permissions. |
    | `Invalid field name [work_notes]` | Check that the field name matches your ServiceNow instance configuration; some instances use `work_notes_list` or custom field names instead of `work_notes`. |
```bash
# Good work note format
[14:35 UTC] Checked nginx access logs — confirmed 503s starting 14:28 UTC
[14:40 UTC] Correlated with deployment at 14:25 UTC by @jsmith
[14:42 UTC] Rolled back to previous image. Error rate dropping.
[14:50 UTC] Error rate back to baseline 0.1%. Monitoring for 30 min before closing.
```

```text title="Expected output"
(no output — command completes silently)
```
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

```text title="Expected output"
{
  "result": {
    "sys_id": "a1b2c3d4e5f6g7h8i9j0k1l2",
    "number": "INC0010847",
    "short_description": "Production API service unavailable",
    "state": "6",
    "close_code": "Solved (Permanently)",
    "close_notes": "A misconfigured deployment caused the service to run out of memory. We have rolled back to the previous version and applied a fix. The service has been stable since 15:00 UTC. We will deploy the corrected version during the next maintenance window.",
    "closed_by": "admin.user",
    "closed_at": "2024-01-15 16:42:33",
    "resolution_time": "02:15:30",
    "caller_id": "john.smith",
    "assignment_group": "Platform Engineering"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.service-now.com port 443: Connection refused` | Replace `your-instance` with your actual ServiceNow instance hostname (e.g., `dev123456.service-now.com`). |
    | `{"error":{"message":"Invalid table API (incident)","status":"failure"},"status":"failure"}` | Verify the incident table name is correct and your API user has read/write permissions on the incident table. |
    | `{"error":{"message":"Invalid field value [6]","status":"failure"}}` | Confirm that state value `6` (Closed) is valid in your ServiceNow instance; some configurations use different state codes. |
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

```text title="Expected output"
{
  "field": "state",
  "from": "1",
  "to": "2",
  "by": "admin.user",
  "at": "2024-01-15 09:23:47"
}
{
  "field": "assigned_to",
  "from": "d4c5e8f2a1b3c9d7e2f4a5b6c7d8e9f0",
  "to": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "by": "change.manager",
  "at": "2024-01-15 10:15:22"
}
{
  "field": "priority",
  "from": "3",
  "to": "2",
  "by": "incident.owner",
  "at": "2024-01-15 11:42:08"
}
{
  "type": "work_notes",
  "author": "tech.support",
  "time": "2024-01-15 09:45:33",
  "note": "Investigated database connectivity issue. Restarted connection pool."
}
{
  "type": "comments",
  "author": "admin.user",
  "time": "2024-01-15 10:22:15",
  "note": "Escalated to infrastructure team for network diagnostics."
}
{
  "type": "work_notes",
  "author": "network.eng",
  "time": "2024-01-15 11:58:42",
  "note": "Identified misconfigured firewall rule. Applied hotfix."
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to your-instance.service-now.com port 443: Name or service not known` | Replace `your-instance` with your actual ServiceNow instance hostname (e.g., `dev12345.service-now.com`). |
    | `{"error":{"message":"Invalid table API GET request","status":"failure"},"status":"failure"}` | Verify the API user has read access to `sys_audit` and `sys_journal_field` tables; check role assignments in ServiceNow. |
    | `jq: parse error: Cannot index string with string "fieldname"` | Ensure the API response contains valid JSON by checking authentication credentials and confirming the table name is correct. |
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


```text title="Expected output"
{"sys_id":"62d4a8f847c12110a6c1f8b3c9e2d1a4","number":"INC0001","work_notes":"Major outage identified — root cause is BGP flap on core-rtr-01. Bridge open in #incident-bridge.","updated_on":"2024-01-15 14:32:18"}
{"sys_id":"73e5b9g958d23221b7d2g9c4d0f3e2b5","number":"INC0002","work_notes":"Major outage identified — root cause is BGP flap on core-rtr-01. Bridge open in #incident-bridge.","updated_on":"2024-01-15 14:32:19"}
{"sys_id":"84f6c0h069e34332c8e3h0d5e1g4f3c6","number":"INC0003","work_notes":"Major outage identified — root cause is BGP flap on core-rtr-01. Bridge open in #incident-bridge.","updated_on":"2024-01-15 14:32:20"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: your-instance.service-now.com` | Replace `your-instance` with your actual ServiceNow instance hostname (e.g., `dev12345.service-now.com`). |
    | `jq: parse error: Cannot index null with string "result"` | Verify the incident number exists and your API user has read permissions on the incident table; check credentials with a test query first. |
    | `{"error":{"message":"Invalid field name: work_notes","status":"failure"}}` | Use the correct field name `work_notes_list` or append to existing notes using `work_notes` as a JSON array instead of a string. |
---

```d2
direction: right

create_an_incident: "Create an Incident" {shape: rectangle}
escalate_an_incident: "Escalate an Incident" {shape: rectangle}
create_a_change_request: "Create a Change Request" {shape: rectangle}
approve_or_reject_a_change: "Approve or Reject a Change" {shape: rectangle}
create_a_problem_record: "Create a Problem Record" {shape: rectangle}
configure_a_business_rule_or_workflo: "Configure a Business Rule or Workflow" {shape: rectangle}

create_an_incident -> escalate_an_incident
escalate_an_incident -> create_a_change_request
create_a_change_request -> approve_or_reject_a_change
approve_or_reject_a_change -> create_a_problem_record
create_a_problem_record -> configure_a_business_rule_or_workflo
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Create an Incident

Log a new incident when a service disruption or degradation is detected or reported.

1. Navigate to **Incident > New** in the ServiceNow menu.
2. Set **Category** and **Subcategory** to classify the issue type.
3. Set **Impact** (scope of users affected) and **Urgency** (speed of business impact required) — these drive the calculated Priority.
4. Set the **Assignment Group** to route the ticket to the correct team.
5. Enter a clear short description and detailed description of the issue.
6. Click **Submit** and note the INC number for tracking and communication.

---

## Escalate an Incident

Escalate when the assigned team is unable to resolve within the SLA threshold or when business impact increases.

1. Open the INC record.
2. Change the **Assignment Group** to the escalation team (e.g., a senior ops or vendor team).
3. Increase the **Priority** level if the impact has grown.
4. Add a **Work Note** documenting the escalation reason, actions taken to date, and who was notified.
5. Notify the on-call engineer or escalation contact via chat or phone — do not rely on the ticket notification alone.

---

## Create a Change Request

Raise a Change Request before making any modification to production infrastructure or services.

1. Navigate to **Change > Create New**.
2. Select the change type: **Normal** (CAB approval required), **Standard** (pre-approved template), or **Emergency** (expedited approval path).
3. Fill in: short description, full description, implementation plan, back-out plan, and risk assessment.
4. Set planned start and end dates, assignment group, and impacted CIs.
5. Submit the record — it enters the approval workflow automatically based on change type.

---

## Approve or Reject a Change

Review and action pending change approvals assigned to you or your group.

1. Navigate to **My Approvals** in the ServiceNow menu.
2. Open the change record awaiting approval.
3. Review the description, implementation plan, back-out plan, and risk rating.
4. Click **Approve** or **Reject** — add a comment explaining the decision, especially for rejections.
5. Normal changes follow CAB review; the CAB chair collates approvals before scheduling the change.

---

## Create a Problem Record

Raise a Problem record when an incident recurs or when root cause investigation is required.

1. Navigate to **Problem > New**.
2. Link all related incident records to the Problem to establish impact.
3. Assign to the problem management team responsible for the affected service.
4. Document any known **workaround** so incident teams can apply it while the root cause is investigated.
5. Investigate root cause — update the record with findings as they develop.
6. When resolved, document the Root Cause Analysis (RCA) and close the Problem record.

---

## Configure a Business Rule or Workflow

Business rules automate field updates, notifications, or record creation on insert or update events.

1. Navigate to **ServiceNow Studio** or **Process Automation > Business Rules**.
2. Select the correct application scope to avoid modifying out-of-box rules.
3. Create a new business rule: set **When** (Before / After), **Operation** (Insert / Update / Delete), and the **Table** it applies to.
4. Write the **Condition** (filter) and **Script** (server-side JavaScript).
5. Test the rule in the development instance by triggering the relevant record operation.
6. Promote to production only after UAT passes in the dev/test instance.

---

## Import Users from Active Directory (LDAP)

Use LDAP integration to auto-provision and sync user accounts from Active Directory into ServiceNow.

1. Navigate to **LDAP > New LDAP Server**.
2. Configure the server: hostname, port, Base DN, and bind credentials (service account).
3. Click **Test Connection** to verify connectivity.
4. Configure the **Import Set** (staging table) and **Transform Map** (field mapping from LDAP attributes to `sys_user` fields).
5. Schedule the import to run on a recurring basis (e.g., every 30 minutes) to keep accounts in sync.
6. Verify imported users appear in **User Management** with correct groups and roles.

---

## Export Data to Excel / CSV

Export list view data for reporting, auditing, or offline analysis.

1. Navigate to the module containing the records you need (e.g., **Incident**, **Change**, **CMDB**).
2. Apply filters to scope the export (e.g., date range, assignment group, state).
3. Right-click any column header and select **Export**, or use the list **Actions** menu and choose **Export**.
4. Choose the format: **Excel** (`.xlsx`) or **CSV** — CSV is preferred for large datasets or scripted processing.
5. Download the file from the browser.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Servicenow — Health Checks](../health-checks/)
- [Servicenow — CLI Reference](../cli-reference/)
- [Servicenow — Common Issues](../../troubleshooting/common-issues/)
