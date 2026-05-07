# Aria Automation — Deployments

## Overview

A deployment is a running instance of a blueprint. Deployments have a lifecycle (create, update, delete) and support day-2 actions such as resize, snapshot, and power operations. All deployment operations are tracked and auditable.

## Deployment Lifecycle

```bash
# Get API bearer token
TOKEN=$(curl -sk -X POST https://<vra-fqdn>/csp/gateway/am/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# List all deployments
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/deployment/api/deployments \
  | python3 -m json.tool

# Get a specific deployment
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/deployment/api/deployments/<deployment-id> \
  | python3 -m json.tool

# Delete a deployment
curl -sk -X DELETE -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/deployment/api/deployments/<deployment-id>
```

Deployment status values:

| Status | Meaning | Action |
|---|---|---|
| `CREATE_SUCCESSFUL` | Deployment created without errors | None — healthy state |
| `CREATE_FAILED` | One or more resources failed to provision | Check deployment events log |
| `UPDATE_SUCCESSFUL` | Day-2 action completed | None |
| `UPDATE_FAILED` | Day-2 action failed | Check action log; retry or rollback |
| `DELETE_SUCCESSFUL` | All resources cleaned up | None |
| `DELETE_FAILED` | Some resources not deleted | Manual cleanup may be required |

## Day-2 Actions

Day-2 actions are post-deployment operations. Available actions depend on the blueprint resource types and organisation policy.

```bash
# List available day-2 actions for a deployment
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/actions" \
  | python3 -m json.tool

# Execute a day-2 action (e.g., PowerOff)
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/requests" \
  -H "Content-Type: application/json" \
  -d '{
    "actionId": "Cloud.vSphere.Machine.PowerOff",
    "reason": "Maintenance window",
    "inputs": {}
  }'

# Check day-2 action request status
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/requests/<request-id>" \
  | python3 -m json.tool
```

Common day-2 actions:

| Action | Description | Requires Approval |
|---|---|---|
| PowerOn / PowerOff | Start or stop the VM | No |
| Reboot | Graceful restart | No |
| Resize | Change CPU or memory | Configurable |
| Snapshot | Create VM snapshot | Configurable |
| Revert Snapshot | Restore to snapshot | Configurable |
| Add Disk | Attach additional disk | Yes (typically) |
| Delete | Remove all resources | Yes (typically) |

## Resize Operations

```bash
# Submit a resize request (CPU and memory)
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/requests" \
  -H "Content-Type: application/json" \
  -d '{
    "actionId": "Cloud.vSphere.Machine.Resize",
    "reason": "Capacity increase request RITM0012345",
    "inputs": {
      "cpuCount": 4,
      "memoryInMB": 8192
    }
  }'
```

## Snapshot Management

```bash
# Create a snapshot of a deployment VM
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/requests" \
  -H "Content-Type: application/json" \
  -d '{
    "actionId": "Cloud.vSphere.Machine.CreateSnapshot",
    "inputs": {
      "name": "pre-patching-2026-05-07",
      "description": "Snapshot before OS patch",
      "memory": false,
      "quiesce": true
    }
  }'

# List snapshots for a VM resource
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/resources/<resource-id>/snapshots" \
  | python3 -m json.tool
```

## Deployment Events and Audit Log

```bash
# Get deployment events (full audit trail)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/events" \
  | python3 -m json.tool

# Filter events by type
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/events?eventTypes=FAILED" \
  | python3 -m json.tool
```
