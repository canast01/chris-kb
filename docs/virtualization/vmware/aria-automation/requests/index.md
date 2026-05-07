# Aria Automation — Requests

## Overview

The Service Catalog is the self-service portal where end users request items published from blueprints, pipelines, and ABX actions. Requests flow through optional approval policies before provisioning begins. All requests are tracked and auditable.

## Service Catalog Requests

```bash
# Get API token
TOKEN=$(curl -sk -X POST https://<vra-fqdn>/csp/gateway/am/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# List catalog items available to the current user
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/catalog/api/items \
  | python3 -m json.tool

# Get the schema (inputs) for a catalog item
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/items/<item-id>/schema" \
  | python3 -m json.tool

# Submit a catalog request
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/catalog/api/items/<item-id>/request \
  -H "Content-Type: application/json" \
  -d '{
    "deploymentName": "web-server-prod-01",
    "projectId": "<project-id>",
    "reason": "New server for project X",
    "inputs": {
      "vmName": "web-prod-01",
      "environment": "prod",
      "cpuCount": 4
    }
  }'
```

## Request Tracking

```bash
# List all requests (paginated)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests?page=0&size=20" \
  | python3 -m json.tool

# Get a specific request
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests/<request-id>" \
  | python3 -m json.tool

# Get request events/log
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests/<request-id>/events" \
  | python3 -m json.tool
```

Request status values:

| Status | Meaning | Next Step |
|---|---|---|
| `PENDING_APPROVAL` | Waiting for approver action | Approver notified by email |
| `APPROVAL_REJECTED` | Approver rejected the request | Requester notified; no provisioning |
| `IN_PROGRESS` | Provisioning underway | Monitor deployment events |
| `SUCCESSFUL` | Deployment complete | Check deployment in Deployments tab |
| `FAILED` | Provisioning error occurred | Review request events for root cause |
| `CANCELLED` | Requester or admin cancelled | No resources created |

## Approval Policies

Approval policies gate requests before provisioning. They can be configured per catalog item, project, or globally.

```bash
# List approval policies
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/catalog/api/policies \
  | python3 -m json.tool

# Create a new approval policy
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/catalog/api/policies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "prod-approval-policy",
    "typeId": "com.vmware.policy.approval",
    "projectId": "<project-id>",
    "definition": {
      "approvalMode": "ANY_OF",
      "approvers": [
        {"type": "USER", "value": "manager@example.com"}
      ],
      "autoApprovalExpiry": 3,
      "autoApprovalDecision": "REJECT"
    }
  }'
```

Approval policy options:

| Option | Values | Description |
|---|---|---|
| `approvalMode` | `ANY_OF`, `ALL_OF` | One or all approvers must approve |
| `autoApprovalDecision` | `APPROVE`, `REJECT` | Action if approver does not respond |
| `autoApprovalExpiry` | Integer (days) | Days before auto-decision triggers |

## Request Filters and Reporting

```bash
# Filter requests by status
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests?requestState=FAILED" \
  | python3 -m json.tool

# Filter requests by requester
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests?requestedBy=user@example.com" \
  | python3 -m json.tool

# Filter by date range
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests?from=2026-05-01T00:00:00Z&to=2026-05-07T23:59:59Z" \
  | python3 -m json.tool
```

## Catalog Item Management

```bash
# List all catalog sources
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/catalog/api/admin/sources \
  | python3 -m json.tool

# Sync a catalog source (pull latest blueprints)
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/admin/sources/<source-id>/sync"

# Update catalog item visibility (share with project)
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/catalog/api/admin/items/<item-id>/share \
  -H "Content-Type: application/json" \
  -d '{"projectIds": ["<project-id>"]}'
```
