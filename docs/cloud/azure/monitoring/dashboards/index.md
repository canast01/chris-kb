---
tags:
  - azure
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
