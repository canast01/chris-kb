# Workbooks

Azure Monitor Workbooks are interactive, parameterised reports that combine text, queries, metrics, and visualisations in a single pane.

```
┌──────────────────────────────────────────────────────────────┐
│                   Workbook Architecture                      │
│                                                              │
│  Parameters  ┌─────────────────────────────────────────┐     │
│  ┌─────────┐  │  Time range │ Subscription │ Resource   │    │
│  │ User    │─►│  (filter all queries below)            │     │
│  │ selects │  └─────────────────────────────────────────┘    │
│  └─────────┘            │ applied to                         │
│                         ▼                                    │
│  Data Sources                                                │
│  ┌───────────┐  ┌───────────┐  ┌───────────────────────┐     │
│  │  Metrics  │  │   Logs    │  │  Azure Resource       │     │
│  │  (charts) │  │  (KQL)    │  │  Graph (ARG)          │     │
│  └─────┬─────┘  └─────┬─────┘  └──────────┬────────────┘     │
│        └──────────────┴──────────────────┘                   │
│                               │                              │
│                               ▼                              │
│  Visualisations  ┌────────────────────────────────────┐      │
│                  │  Grid │ Chart │ Map │ Text │ Tiles  │     │
│                  └────────────────────────────────────┘      │
│                               │ share via RBAC               │
│                               ▼                              │
│             Team workbook  (kind: shared)                    │
└──────────────────────────────────────────────────────────────┘
``` They are used for operational dashboards, cost reports, capacity planning, and compliance views that require richer formatting than a standard dashboard.

## Workbook Templates

Azure provides built-in workbook templates for common scenarios. Templates can be accessed from the Workbooks gallery in the Azure Monitor or individual service blades (e.g., App Gateway, AKS, Security Center).

```bash
# List workbooks in a resource group
az monitor workbook list \
  --resource-group myRG \
  --output table

# Show a specific workbook definition
az monitor workbook show \
  --resource-group myRG \
  --name <workbook-resource-id> \
  --output json

# Create a workbook from a JSON template file
az monitor workbook create \
  --resource-group myRG \
  --name "vm-performance-workbook" \
  --display-name "VM Performance Overview" \
  --serialized-data @workbook-template.json \
  --source-id /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.OperationalInsights/workspaces/myWorkspace \
  --kind shared
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
