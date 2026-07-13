---
tags:
  - azure
description: "Azure Monitor Workbooks are interactive, parameterised reports that combine text, queries, metrics, and visualisations in a single pane."
---
# Workbooks

<div class="kb-summary">
Azure Monitor Workbooks are interactive, parameterised reports that combine text, queries, metrics, and visualisations in a single pane.

*Applies to: Azure*
</div>

```d2
direction: down

workbook_parameters: "Workbook Parameters" {shape: rectangle}
custom_visualisations: "Custom Visualisations" {shape: rectangle}
sharing_workbooks: "Sharing Workbooks" {shape: rectangle}
exporting_and_version_control: "Exporting and Version Control" {shape: rectangle}
builtin_workbook_gallery: "Built-in Workbook Gallery" {shape: rectangle}
workbook_governance_tips: "Workbook Governance Tips" {shape: rectangle}

workbook_parameters -> custom_visualisations: uses
custom_visualisations -> sharing_workbooks: uses
sharing_workbooks -> exporting_and_version_control: uses
exporting_and_version_control -> builtin_workbook_gallery: uses
builtin_workbook_gallery -> workbook_governance_tips: uses
```

## Workbook Parameters

Parameters allow users to filter workbook data dynamically. Common parameter types include time range, subscription, resource group, resource, and free text.

| Parameter Type    | Use Case                                          |
|-------------------|---------------------------------------------------|
| Time range        | Filter all queries to a selected time window      |
| Resource group    | Scope queries to a specific resource group        |
| Resource          | Select a specific resource to inspect             |
| Drop-down         | Choose from a static or dynamic list of values    |
| Text              | Free text input for dynamic KQL filters           |
| Subscription      | Scope to a specific subscription                  |

## Custom Visualisations

Workbooks support multiple visualisation types within a single document:

```kql
// Example: VM CPU heatmap — paste into a Workbook query step
Perf
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| where TimeGenerated > {TimeRange:start}
| summarize AvgCPU=avg(CounterValue) by Computer, bin(TimeGenerated, 1h)
| render timechart
```

```kql
// Table of VMs missing heartbeat
Heartbeat
| summarize LastHeartbeat=max(TimeGenerated) by Computer
| where LastHeartbeat < ago(10m)
| project Computer, LastHeartbeat, MinutesSinceHeartbeat=datetime_diff('minute', now(), LastHeartbeat)
| order by MinutesSinceHeartbeat desc
```

## Sharing Workbooks

Workbooks are ARM resources stored in a resource group. Sharing is managed via RBAC.

```bash
# Assign Reader to a workbook so a team can view it
az role assignment create \
  --assignee team-group@example.com \
  --role Reader \
  --scope /subscriptions/<sub-id>/resourceGroups/myRG/providers/microsoft.insights/workbooks/<workbook-guid>

# Make a workbook shared (visible to everyone with workspace access)
az monitor workbook update \
  --resource-group myRG \
  --name <workbook-resource-id> \
  --kind shared
```


```text title="Expected output"
{
  "canDelegate": false,
  "condition": null,
  "conditionVersion": null,
  "createdBy": "admin@example.com",
  "createdOn": "2024-01-15T09:42:33.847291+00:00",
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d/providers/Microsoft.Authorization/roleAssignments/12345678-1234-1234-1234-123456789012",
  "name": "12345678-1234-1234-1234-123456789012",
  "principalId": "87654321-4321-4321-4321-210987654321",
  "principalType": "Group",
  "roleDefinitionId": "/subscriptions/a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
  "roleDefinitionName": "Reader",
  "scope": "/subscriptions/a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d/resourceGroups/myRG/providers/microsoft.insights/workbooks/5f8a9b2c-1d3e-4f5a-8b9c-2d3e4f5a6b7c",
  "updatedBy": "admin@example.com",
  "updatedOn": "2024-01-15T09:42:33.847291+00:00"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d/resourceGroups/myRG/providers/microsoft.insights/workbooks/5f8a9b2c-1d3e-4f5a-8b9c-2d3e4f5a6b7c",
  "kind": "shared",
  "location": "eastus",
  "name": "SalesMetricsWorkbook",
  "resourceGroup": "myRG",
  "tags": {
    "environment": "production"
  },
  "type": "microsoft.insights/workbooks"
}
```

!!! warning "Common errors"
    **`The provided information does not map to a valid role.`** — Verify the role name is correct (e.g., "Reader", "Contributor") using `az role definition list --query "[].name"`.
    **`ResourceNotFound: The Resource 'Microsoft.Insights/workbooks/<workbook-resource-id>' under resource group 'myRG' was not found.`** — Confirm the workbook name/resource ID exists in the specified resource group using `az monitor workbook list --resource-group myRG`.
## Exporting and Version Control

```bash
# Export workbook definition for version control
az monitor workbook show \
  --resource-group myRG \
  --name <workbook-resource-id> \
  --output json | jq '.properties.serializedData' > workbook-export.json

# Deploy workbook via Bicep/ARM (common in IaC pipelines)
# The serializedData field contains the full JSON workbook definition
az deployment group create \
  --resource-group myRG \
  --template-file workbook-deploy.bicep \
  --parameters workbookDisplayName="VM Performance Overview"
```


```text title="Expected output"
{
  "version": "1.0.0",
  "isLocked": false,
  "items": [
    {
      "type": 1,
      "content": {
        "json": "# VM Performance Dashboard\n\nThis workbook tracks CPU, memory, and disk metrics across production VMs."
      }
    },
    {
      "type": 10,
      "content": {
        "chartType": "unstacked column",
        "xAxis": "TimeGenerated",
        "yAxis": "Percentage"
      }
    }
  ],
  "styleSettings": {},
  "fromTemplateId": null
}
Deployment in progress..
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/myRG/providers/Microsoft.Insights/workbooks/vm-perf-workbook-20240115",
  "name": "vm-perf-workbook-20240115",
  "type": "Microsoft.Insights/workbooks",
  "location": "eastus",
  "properties": {
    "displayName": "VM Performance Overview",
    "sourceId": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/myRG",
    "category": "workbook",
    "tags": {}
  }
}
```

!!! warning "Common errors"
    **`The workbook resource '<workbook-resource-id>' could not be found in resource group 'myRG'.`** — Verify the workbook exists with `az monitor workbook list --resource-group myRG` and use the correct resource ID or name.
    **`Template validation failed: 'workbookDisplayName' is not a recognized parameter in workbook-deploy.bicep.`** — Check the Bicep template file for the exact parameter name and ensure it matches the `@param` declaration.
    **`jq: parse error: Cannot index string with string "properties"`** — Ensure the `az monitor workbook show` command succeeds and returns valid JSON before piping to jq; add `--debug` to diagnose the API response.
## Built-in Workbook Gallery

| Category          | Notable Templates                                     |
|-------------------|-------------------------------------------------------|
| Virtual Machines  | VM Insights Performance, VM Health                    |
| Networking        | Azure Firewall Workbook, NSG Flow Logs Analysis       |
| Security          | Defender for Cloud Coverage, Security Alerts          |
| Cost              | Azure Cost Optimization                               |
| AKS               | Cluster Health, Node and Pod Usage                    |
| Storage           | Storage Account Insights                              |

## Workbook Governance Tips

- Store workbook JSON in a Git repository for audit and rollback
- Use the `shared` kind for team workbooks; `user` kind for personal drafts
- Parameterise subscription and workspace inputs to make workbooks environment-agnostic
- Tag workbooks with `owner` and `team` tags for lifecycle management
