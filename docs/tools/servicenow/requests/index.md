# ServiceNow Requests

Service catalog, request items, approval workflows, and fulfillment tracking.

## Service Catalog Overview

The Service Catalog is the self-service portal where users submit requests for IT services.

```
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
