# Azure — Health Checks

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure Health Check Flow                   │
└─────────────────────────────────────────────────────────────┘

 ┌──────────────────┐    ┌──────────────────┐
 │  Azure Service   │    │  Resource Health  │
 │  Health          │    │  (per resource)   │
 │  (platform-wide) │    │                  │
 └────────┬─────────┘    └────────┬─────────┘
          │                       │
          └───────────┬───────────┘
                      ▼
           ┌──────────────────────┐
           │   Azure Monitor      │
           │  ┌────────────────┐  │
           │  │ Activity Log   │  │
           │  │ Metric Alerts  │  │
           │  │ Log Analytics  │  │
           │  └────────────────┘  │
           └──────────┬───────────┘
                      │ alert fires
                      ▼
           ┌──────────────────────┐
           │    Action Group      │
           │  email / SMS / ITSM  │
           └──────────────────────┘
```

> Service health, VM status, load balancer health, and monitor alert review.

See also: [Operations](../) for the full daily checklist and incident triage procedures.

---

## Quick Commands

```bash
# List VMs with power state
az vm list --show-details \
  --query '[*].[name,resourceGroup,powerState,provisioningState]' \
  -o table

# Load balancer status
az network lb show \
  --name <lb-name> \
  --resource-group <rg> \
  --query '{name:name,provisioningState:provisioningState}' \
  -o table

# Activity log — last 50 events
az monitor activity-log list --max-events 50 \
  --query '[*].[eventTimestamp,level,operationName.localizedValue,status.localizedValue]' \
  -o table

# Failed backup jobs
az backup job list \
  --vault-name $VAULT \
  -g $RG \
  --query '[?properties.status==`Failed`].[properties.jobType,properties.startTime,properties.errorDetails]' \
  -o table

# Azure Service Health — active incidents
az rest --method get \
  --url "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.ResourceHealth/events?api-version=2022-10-01"
```
