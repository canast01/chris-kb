# Aria Automation — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Blueprints (Cloud Templates), Deployments, Requests and Catalog, Related Sections.
</div>

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
┌──────────────────────────────────── Aria Automation — Diagnostics ────────────────────────────────────┐
│                                                                                                       │
│  Collect vRA logs and support bundle before engaging VMware support for complex issues.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Collection                │  │                Support Bundle               │   │
│   │        kubectl logs -n prelude --all         │  │           LCM: Logscraper utility           │   │
│   │      /var/log/vmware/vra/ on appliance       │  │       VAMI → Support → Generate bundle      │   │
│   │       journalctl -u vra-cluster -n 500       │  │        Includes k8s pod logs + config       │   │
│   │          ABX run history in vRA UI           │  │       Upload to VMware SR for analysis      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  API-level diagnostics: check connectivity, auth, and response codes systematically.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               API Diagnostics                │  │                DB Diagnostics               │   │
│   │      curl -k /csp/gateway/am/api/login       │  │        psql -U postgres vra DB access       │   │
│   │       GET /deployment/api/deployments        │  │    Check replication: pg_stat_replication   │   │
│   │       Check 401/403/500 response codes       │  │       Check bloat: pg_stat_user_tables      │   │
│   │       Swagger UI /vco/api/docs testing       │  │       Vacuum: VACUUM ANALYZE public.*       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA Linux appliances · k3s Kubernetes · Postgres · vIDM · LCM logscraper                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM logscraper    = LCM utility collecting logs from all Aria products into one archive              │
│  Support bundle    = vRA-generated diagnostic archive; includes pod logs, configs, DB state           │
│  kubectl logs --all = Collect logs from all pods across the prelude namespace at once                 │
│  journalctl        = Linux log viewer for systemd; captures vra-cluster startup messages              │
│  ABX run history   = Per-action execution log in vRA UI showing inputs, outputs, and errors           │
│  Swagger UI        = /vco/api/docs and /automation-ui/api/docs; test APIs interactively               │
│  401/403 response  = Unauthorised/forbidden; check token expiry or role assignment                    │
│  500 response      = Internal server error; look at pod logs for stack trace                          │
│  pg_stat_replication= Postgres view showing standby lag; high lag indicates DB issue                  │
│  VACUUM ANALYZE    = Postgres maintenance command; reclaims space and updates query stats             │
│  psql access       = Direct Postgres client on vRA appliance; use only for diagnostics                │
│  VMware SR         = Support Request; opened with support bundle attached for complex issues          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
