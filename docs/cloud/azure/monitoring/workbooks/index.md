# Workbooks


<div class="kb-summary">
Azure Monitor Workbooks are interactive, parameterised reports that combine text, queries, metrics, and visualisations in a single pane.
</div>
```
┌─────────────────────────────────────── Cloud Azure Monitoring ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Azure: Cloud Azure Monitoring platform                            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                     Management: Cloud Azure Monitoring management console                     │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Monitoring infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Monitoring platform overview and core concepts                    │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
