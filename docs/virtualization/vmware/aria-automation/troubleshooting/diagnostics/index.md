# Aria Automation — Diagnostics

## Blueprints (Cloud Templates)

### Blueprint Structure

A Cloud Template YAML has three top-level sections:

```yaml
formatVersion: 1
inputs:
  vmName:
    type: string
    title: VM Name
    default: my-vm
  cpuCount:
    type: integer
    title: CPU Count
    default: 2
    enum: [2, 4, 8]

resources:
  Cloud_vSphere_Machine_1:
    type: Cloud.vSphere.Machine
    properties:
      name: ${input.vmName}
      image: ubuntu-22-04
      flavor: medium
      cpuCount: ${input.cpuCount}
      memoryInMB: 4096
      networks:
        - network: ${resource.Cloud_vSphere_Network_1.id}
          assignment: static
      tags:
        - key: owner
          value: ${env.requestedBy}

  Cloud_vSphere_Network_1:
    type: Cloud.vSphere.Network
    properties:
      networkType: existing
      name: VLAN-100-Servers
```

### Blueprint Validation

```bash
# Validate blueprint YAML locally (requires vRA CLI)
vra-cli blueprint validate --file ./blueprint.yaml

# Validate via API
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/validate \
  -H "Content-Type: application/json" \
  -d @blueprint.json
```

### Blueprint Versioning

```bash
# List blueprints via vRA API
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints \
  | python3 -m json.tool

# Create a new blueprint version
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/<blueprint-id>/versions \
  -H "Content-Type: application/json" \
  -d '{"version": "1.2", "description": "Added NSX segment"}'

# Publish a version to Service Catalog
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/<blueprint-id>/versions/<version>/actions/publish
```

---

## Deployments

### Deployment Status Values

| Status | Meaning | Action |
|---|---|---|
| `CREATE_SUCCESSFUL` | Deployment created without errors | None — healthy state |
| `CREATE_FAILED` | One or more resources failed to provision | Check deployment events log |
| `UPDATE_SUCCESSFUL` | Day-2 action completed | None |
| `UPDATE_FAILED` | Day-2 action failed | Check action log; retry or rollback |
| `DELETE_SUCCESSFUL` | All resources cleaned up | None |
| `DELETE_FAILED` | Some resources not deleted | Manual cleanup may be required |

### Deployment Lifecycle Commands

```bash
# List all deployments
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/deployment/api/deployments \
  | python3 -m json.tool

# Get a specific deployment
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/deployment/api/deployments/<deployment-id> \
  | python3 -m json.tool

# Get deployment events (full audit trail)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/events" \
  | python3 -m json.tool

# Filter events by type
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/events?eventTypes=FAILED" \
  | python3 -m json.tool
```

### Day-2 Actions

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
```

---

## Requests and Catalog

### Request Status Values

| Status | Meaning | Next Step |
|---|---|---|
| `PENDING_APPROVAL` | Waiting for approver action | Approver notified by email |
| `APPROVAL_REJECTED` | Approver rejected the request | Requester notified; no provisioning |
| `IN_PROGRESS` | Provisioning underway | Monitor deployment events |
| `SUCCESSFUL` | Deployment complete | Check deployment in Deployments tab |
| `FAILED` | Provisioning error occurred | Review request events for root cause |
| `CANCELLED` | Requester or admin cancelled | No resources created |

### Request Troubleshooting Commands

```bash
# List all requests
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

# Filter requests by status
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests?requestState=FAILED" \
  | python3 -m json.tool
```

---

## Related Sections

- [Operations](../../operations/index.md) — health checks and procedures
- [Escalation](../escalation/index.md) — opening vendor support cases
