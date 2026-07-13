---
tags:
  - azure
description: "Azure Service Health provides personalised alerts and guidance for Azure service issues, planned maintenance, and health advisories that affect the..."
---
# Service Health

<div class="kb-summary">
Azure Service Health provides personalised alerts and guidance for Azure service issues, planned maintenance, and health advisories that affect the services and regions you use. It combines three views: Service Issues, Planned Maintenance, and Health Advisories.

*Applies to: Azure*
</div>

## Service Health Alert Flow

```d2
direction: right

azureIncident: "Azure Incident / Event\nService Issue · Planned Maintenance · Advisory" {shape: rectangle}
serviceHealth: "Azure Service Health\npersonalised for your subscriptions + regions" {shape: rectangle}
healthAlert: "Service Health Alert Rule\nsubscription · region · service filter" {shape: rectangle}
actionGroup: "Action Group\nemail · SMS · webhook · ITSM" {shape: rectangle}
opsTeam: "Operations Team\nincident response" {shape: rectangle}

azureIncident -> serviceHealth
serviceHealth -> healthAlert
healthAlert -> actionGroup
actionGroup -> opsTeam
```

## Service Health Components

| Component           | Description                                                      |
|---------------------|------------------------------------------------------------------|
| Service Issues      | Active incidents impacting Azure services in your regions        |
| Planned Maintenance | Upcoming maintenance that may require action or cause downtime   |
| Health Advisories   | Feature deprecations, breaking changes, required migrations      |
| Resource Health     | Per-resource availability state (Available, Degraded, Unavailable) |
| Security Advisories | Security-related events affecting Azure services                 |

## Querying Service Health Events

```bash
# List all active service health events for a subscription
az monitor activity-log list \
  --start-time $(date -u -v-7d +%Y-%m-%dT%H:%MZ) \
  --filters "category eq 'ServiceHealth'" \
  --output table

# Get resource health for a specific VM
az resource health show \
  --resource-type Microsoft.Compute/virtualMachines \
  --resource-group myRG \
  --resource-name myVM \
  --output json

# List resource health events for a resource
az resource health event list \
  --resource-type Microsoft.Compute/virtualMachines \
  --resource-group myRG \
  --resource-name myVM \
  --output table
```


```text title="Expected output"
Time                             OperationName                ResourceGroup    Status
---------------------------------  ---------------------------  ---------------  --------
2024-01-15T14:32:00.000000+00:00  ServiceHealthEvent           myRG             Succeeded
2024-01-14T09:18:00.000000+00:00  PlatformMaintenance          myRG             Succeeded
2024-01-12T22:45:00.000000+00:00  ServiceHealthEvent           eastus           Succeeded

{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM",
  "name": "myVM",
  "type": "Microsoft.Compute/virtualMachines",
  "location": "eastus",
  "properties": {
    "availabilityState": "Available",
    "healthStatus": "Healthy",
    "reasonType": "NotApplicable"
  }
}

EventTime                        HealthStatus    Summary
---------------------------------  ---------------  -----------------------------------------------
2024-01-10T16:22:00.000000+00:00  Healthy        VM is running normally
2024-01-08T11:05:00.000000+00:00  Degraded       Intermittent network connectivity detected
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachines/myVM' under resource group 'myRG' was not found.`** — Verify the resource group name and VM name are correct using `az vm list --resource-group myRG`.
    **`AuthorizationFailed: The client 'user@example.com' with object id 'xxx' does not have authorization to perform action 'Microsoft.ResourceHealth/availabilityStatuses/read' over scope '/subscriptions/xxx/resourceGroups/myRG'.`** — Ensure your user account has at least Reader role on the subscription or resource group using `az role assignment list --assignee user@example.com`.
## Creating Service Health Alerts

Service Health alerts notify your team when an incident, planned maintenance, or advisory affects services in regions you select.

```bash
# Create an action group for service health notifications
az monitor action-group create \
  --name "service-health-ag" \
  --resource-group myRG \
  --short-name "SvcHlth" \
  --action email infra-lead infra@example.com

# Create a Service Health alert for incidents in East US
az monitor activity-log alert create \
  --name "svc-health-incident-alert" \
  --resource-group myRG \
  --condition "category=ServiceHealth and properties.incidentType=Incident and properties.impactedServices[*].ServiceName=Virtual Machines and properties.impactedServices[*].ImpactedRegions[*].RegionName=East US" \
  --action-group /subscriptions/<sub-id>/resourceGroups/myRG/providers/microsoft.insights/actionGroups/service-health-ag \
  --description "Alert for VM incidents in East US"

# Alert for planned maintenance events
az monitor activity-log alert create \
  --name "svc-health-maintenance-alert" \
  --resource-group myRG \
  --condition "category=ServiceHealth and properties.incidentType=Maintenance" \
  --action-group /subscriptions/<sub-id>/resourceGroups/myRG/providers/microsoft.insights/actionGroups/service-health-ag
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/microsoft.insights/actionGroups/service-health-ag",
  "location": "global",
  "name": "service-health-ag",
  "resourceGroup": "myRG",
  "shortName": "SvcHlth",
  "type": "Microsoft.Insights/actionGroups"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/microsoft.insights/activityLogAlerts/svc-health-incident-alert",
  "name": "svc-health-incident-alert",
  "resourceGroup": "myRG",
  "type": "Microsoft.Insights/activityLogAlerts",
  "enabled": true,
  "condition": {
    "allOf": [
      {
        "field": "category",
        "equals": "ServiceHealth"
      },
      {
        "field": "properties.incidentType",
        "equals": "Incident"
      }
    ]
  }
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/microsoft.insights/activityLogAlerts/svc-health-maintenance-alert",
  "name": "svc-health-maintenance-alert",
  "resourceGroup": "myRG",
  "type": "Microsoft.Insights/activityLogAlerts",
  "enabled": true
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound : The resource group 'myRG' could not be found.`** — Verify the resource group exists in your subscription with `az group list` and use the correct name.
    **`InvalidResourceId : The provided resource ID for action group is invalid or does not exist.`** — Replace `<sub-id>` with your actual subscription ID from `az account show --query id -o tsv`.
    **`BadRequest : The condition syntax is invalid.`** — Simplify the condition to use only supported fields like `category=ServiceHealth and properties.incidentType=Incident` without nested array filters.
## Resource Health States

| State        | Meaning                                                         |
|--------------|-----------------------------------------------------------------|
| Available    | Resource is operating normally                                  |
| Degraded     | Resource is available but with reduced performance              |
| Unavailable  | Resource is not available (platform or customer initiated)      |
| Unknown      | Resource health state has not been received for > 10 minutes    |

```bash
# List all resources in a resource group with non-Available health
az resource health list \
  --resource-group myRG \
  --output table

# Get availability status for all VMs in subscription
az graph query -q "
  HealthResources
  | where type == 'microsoft.resourcehealth/availabilitystatuses'
  | where properties.availabilityState != 'Available'
  | project name, resourceGroup, properties.availabilityState
" --output table
```


```text title="Expected output"
Name                             ResourceGroup    AvailabilityState
---------------------------------  ---------------  -------------------
vm-prod-01                         myRG             Degraded
storage-account-backup             myRG             Unknown
app-service-web-01                 myRG             Unavailable

Name                             ResourceGroup    AvailabilityState
---------------------------------  ---------------  -------------------
vm-prod-01                         myRG             Degraded
vm-staging-02                      stagingRG        Unknown
cosmos-db-primary                  prodRG           Unavailable
sql-db-failover                    prodRG           Degraded
keyvault-east                      securityRG       Unknown
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource group 'myRG' could not be found.`** — Verify the resource group name with `az group list` and correct the `--resource-group` parameter.
    **`AuthorizationFailed: The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.ResourceHealth/availabilityStatuses/read' over scope '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourcegroups/myRG'.`** — Ensure your Azure account has the Reader role or higher on the resource group using `az role assignment create --role Reader --assignee <user-id> --scope /subscriptions/<sub-id>/resourceGroups/myRG`.
## Planned Maintenance Queries

```bash
# Query activity log for upcoming maintenance events
az monitor activity-log list \
  --start-time $(date -u -v-30d +%Y-%m-%dT%H:%MZ) \
  --filters "category eq 'ServiceHealth' and properties.incidentType eq 'Maintenance'" \
  --output json | jq '.[] | {time: .eventTimestamp, title: .properties.title, services: .properties.impactedServices}'
```


```text title="Expected output"
{
  "time": "2024-12-15T09:30:00Z",
  "title": "Planned Maintenance: Azure Virtual Machines in East US",
  "services": [
    {
      "serviceName": "Virtual Machines",
      "regions": [
        "East US",
        "East US 2"
      ]
    }
  ]
}
{
  "time": "2024-12-18T14:22:00Z",
  "title": "Planned Maintenance: Azure SQL Database - West Europe",
  "services": [
    {
      "serviceName": "SQL Database",
      "regions": [
        "West Europe"
      ]
    }
  ]
}
{
  "time": "2024-12-20T06:15:00Z",
  "title": "Planned Maintenance: Azure App Service Infrastructure Update",
  "services": [
    {
      "serviceName": "App Service",
      "regions": [
        "Central US",
        "North Europe",
        "Southeast Asia"
      ]
    }
  ]
}
```

!!! warning "Common errors"
    **`ERROR: (InvalidFilterExpression) The filter expression is invalid.`** — Verify the filter syntax matches Azure Monitor's OData format; use single quotes around the entire filter string and check property names against the activity log schema.
    **`jq: error (at <stdin>:1): Cannot index array with string "eventTimestamp"`** — The query returned an empty array; extend the `--start-time` window (e.g., `-v-90d` instead of `-v-30d`) or remove the `incidentType` filter to broaden results.
    **`ERROR: (AuthorizationFailed) The client does not have authorization to perform action 'microsoft.insights/eventtypes/values/read'.`** — Ensure your Azure account has the "Monitoring Reader" or "Reader" role assigned at the subscription scope.
## Root Cause Analysis (RCA) Reports

After a service incident is resolved, Microsoft publishes a Post-Incident Review (PIR) / RCA document. Access it via the Service Health blade in the Azure portal under the specific incident, or subscribe to email notifications that include the PIR link when published.

```bash
# Get incident details from activity log
az monitor activity-log list \
  --start-time 2026-05-01T00:00:00Z \
  --filters "category eq 'ServiceHealth'" \
  --output json | jq '.[] | select(.properties.incidentType == "Incident") | {title: .properties.title, summary: .properties.communication, stage: .properties.stage}'
```


```text title="Expected output"
{
  "title": "Azure App Service - Intermittent Connection Timeouts",
  "summary": "We are investigating reports of intermittent connection timeouts affecting Azure App Service instances in East US 2 region. Estimated time to resolution: 45 minutes.",
  "stage": "Active"
}
{
  "title": "Azure SQL Database - Planned Maintenance",
  "summary": "Scheduled maintenance window for Azure SQL Database in West Europe. Expected duration: 2 hours. No data loss expected.",
  "stage": "Resolved"
}
{
  "title": "Azure Storage - Authentication Service Degradation",
  "summary": "Partial service degradation affecting blob storage authentication in Southeast Asia. Our team is actively working on mitigation.",
  "stage": "Active"
}
```

!!! warning "Common errors"
    **`jq: error (at <stdin>:0): Cannot index null with string "properties"`** — Ensure the activity log returned valid JSON by removing the `jq` filter temporarily to verify the response structure.
    **`The provided filter value is invalid`** — Use the correct ServiceHealth filter syntax: `"category eq 'ServiceHealth' and level eq 'Error'"` or verify the filter parameter name with `az monitor activity-log list --help`.