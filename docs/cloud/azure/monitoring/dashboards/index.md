---
tags:
  - azure
description: "Azure Dashboards provide a shared, customisable view of Azure resource telemetry. A minimal dashboard JSON skeleton:"
---
# Dashboards

<div class="kb-summary">
Azure Dashboards provide a shared, customisable view of Azure resource telemetry. A minimal dashboard JSON skeleton:

*Applies to: Azure*
</div>

Azure Dashboards provide a shared, customisable view of Azure resource telemetry.

A minimal dashboard JSON skeleton:

```json
{
  "properties": {
    "lenses": {
      "0": {
        "order": 0,
        "parts": {
          "0": {
            "position": { "x": 0, "y": 0, "colSpan": 6, "rowSpan": 4 },
            "metadata": {
              "type": "Extension/HubsExtension/PartType/MarkdownPart",
              "settings": {
                "content": { "settings": { "content": "# Ops Overview" } }
              }
            }
          }
        }
      }
    },
    "metadata": { "model": {} }
  },
  "location": "eastus",
  "tags": { "hidden-title": "Ops Overview Dashboard" }
}
```

```d2
direction: down

pinning_metrics_charts: "Pinning Metrics Charts" {shape: rectangle}
common_dashboard_tile_types: "Common Dashboard Tile Types" {shape: rectangle}
sharing_dashboards: "Sharing Dashboards" {shape: rectangle}
exporting_and_importing_dashboard_js: "Exporting and Importing Dashboard JSON" {shape: rectangle}
dashboard_governance: "Dashboard Governance" {shape: rectangle}

pinning_metrics_charts -> common_dashboard_tile_types: uses
common_dashboard_tile_types -> sharing_dashboards: uses
sharing_dashboards -> exporting_and_importing_dashboard_js: uses
exporting_and_importing_dashboard_js -> dashboard_governance: uses
```

## Pinning Metrics Charts

Charts from Metrics Explorer can be pinned directly to a dashboard from the portal. Each chart tile is parameterised by resource, metric, aggregation, and time range.

```bash
# Query a metric to verify it renders as expected before pinning
az monitor metrics list \
  --resource /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM \
  --metric "Percentage CPU" \
  --interval PT1M \
  --aggregation Average \
  --output table

# List available metrics on a resource (to find metric names for charts)
az monitor metrics list-definitions \
  --resource /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW \
  --output table
```


```text title="Expected output"
Timeseries                                Name              Aggregation    Value
--------------------------------------------------  ----------------  ---------------  -------
2024-01-15T14:30:00+00:00 - 2024-01-15T14:31:00  Percentage CPU    Average         23.45
2024-01-15T14:31:00+00:00 - 2024-01-15T14:32:00  Percentage CPU    Average         25.67
2024-01-15T14:32:00+00:00 - 2024-01-15T14:33:00  Percentage CPU    Average         22.89
2024-01-15T14:33:00+00:00 - 2024-01-15T14:34:00  Percentage CPU    Average         26.12

Name                          Dimensions    Aggregations
-------------------------------  -----------  ----------------
Percentage CPU                 None          Average, Maximum, Minimum
Available Memory Bytes         None          Average, Maximum, Minimum
Network In Total               None          Average, Total
Network Out Total              None          Average, Total
Disk Read Bytes/sec            None          Average, Maximum
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The resource '/subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM' could not be found.` | Verify the subscription ID, resource group name, and VM name are correct, and that the resource exists in the current subscription context. |
    | `Metric 'Percentage CPU' does not have a definition for the specified resource.` | Run `az monitor metrics list-definitions` on the resource to confirm the exact metric name (e.g., it may be "Percentage CPU" vs "% Processor Time" depending on resource type). |
## Common Dashboard Tile Types

| Tile Type              | Description                                       |
|------------------------|---------------------------------------------------|
| Metrics chart          | Time-series chart from Azure Monitor metrics      |
| Log query              | KQL results table or chart from Log Analytics     |
| Resource health        | Current health state for a specific resource      |
| Markdown               | Free-text instructions, links, or section headers |
| Resource group         | Summary tile for a resource group                 |
| Clock/Time             | Displays current UTC time                         |

## Sharing Dashboards

Dashboards are stored as ARM resources. Sharing is controlled via Azure RBAC on the dashboard resource.

```bash
# Assign Reader role to a user on a specific dashboard
az role assignment create \
  --assignee user@example.com \
  --role Reader \
  --scope /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Portal/dashboards/ops-overview-dashboard

# Share at subscription level (all dashboards visible)
az role assignment create \
  --assignee user@example.com \
  --role Reader \
  --scope /subscriptions/<sub-id>
```


```text title="Expected output"
{
  "canDelegate": false,
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/myRG/providers/Microsoft.Portal/dashboards/ops-overview-dashboard/providers/Microsoft.Authorization/roleAssignments/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "principalId": "98765432-f1e2-d3c4-b5a6-789012345678",
  "principalType": "User",
  "roleDefinitionId": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
  "scope": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/myRG/providers/Microsoft.Portal/dashboards/ops-overview-dashboard",
  "type": "Microsoft.Authorization/roleAssignments"
}
{
  "canDelegate": false,
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/providers/Microsoft.Authorization/roleAssignments/b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "name": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "principalId": "98765432-f1e2-d3c4-b5a6-789012345678",
  "principalType": "User",
  "roleDefinitionId": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
  "scope": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234",
  "type": "Microsoft.Authorization/roleAssignments"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The user, group or service principal does not exist in the directory` | Verify the user email exists in your Azure AD tenant with `az ad user show --id user@example.com`. |
    | `The scope provided is invalid` | Ensure the subscription ID is correct and the dashboard resource path exists by running `az portal dashboard list --resource-group myRG`. |
    | `Authorization failed: User does not have permission to perform action 'Microsoft.Authorization/roleAssignments/write'` | Confirm your account has Owner or User Access Administrator role on the target scope with `az role assignment list --assignee <your-id>`. |
## Exporting and Importing Dashboard JSON

Dashboards can be exported as JSON for version control or cross-environment deployment.

```bash
# Export dashboard definition
az portal dashboard show \
  --resource-group myRG \
  --name "ops-overview-dashboard" \
  --output json > ops-dashboard-export.json

# Update a dashboard from a modified JSON file
az portal dashboard update \
  --resource-group myRG \
  --name "ops-overview-dashboard" \
  --input-path ops-dashboard-export.json
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Microsoft.Portal/dashboards/ops-overview-dashboard",
  "location": "eastus",
  "name": "ops-overview-dashboard",
  "properties": {
    "lenses": {
      "0": {
        "order": 0,
        "parts": {
          "0": {
            "position": {
              "x": 0,
              "y": 0,
              "rowSpan": 4,
              "colSpan": 6
            },
            "metadata": {
              "inputs": [],
              "type": "Extension/HubsExtension/PartType/MarkdownPart",
              "settings": {
                "content": {
                  "settings": {
                    "content": "# Operations Overview"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "resourceGroup": "myRG",
  "tags": {},
  "type": "Microsoft.Portal/dashboards"
}

Dashboard updated successfully.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound : The Resource 'Microsoft.Portal/dashboards/ops-overview-dashboard' under resource group 'myRG' was not found.` | Verify the dashboard name and resource group exist using `az portal dashboard list --resource-group myRG`. |
    | `InvalidTemplate : The template is invalid.` | Ensure the JSON file is valid and contains all required properties by validating the exported JSON structure before modification. |
## Dashboard Governance

```bash
# Tag a dashboard for environment tracking
az tag update \
  --resource-id /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Portal/dashboards/ops-overview-dashboard \
  --operation merge \
  --tags environment=production owner=platform-team

# Delete an obsolete dashboard
az portal dashboard delete \
  --resource-group myRG \
  --name "old-dashboard" \
  --yes
```


```text title="Expected output"
(no output — command completes silently)
Are you sure you want to perform this operation? (y/n): y
Deleting dashboard 'old-dashboard' in resource group 'myRG'...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The resource with id /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Portal/dashboards/ops-overview-dashboard does not exist.` | Verify the subscription ID, resource group name, and dashboard name are correct using `az portal dashboard list --resource-group myRG`. |
    | `(ResourceNotFound) The resource 'old-dashboard' does not exist in the resource group 'myRG'.` | Confirm the dashboard exists and check the exact name with `az portal dashboard list --resource-group myRG --query "[].name"`. |