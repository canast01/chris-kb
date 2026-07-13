---
tags:
  - azure
description: "Azure Monitor Alerts proactively notify you when conditions in your monitored resources are met. Alert rules evaluate signals — metrics, log queries, or..."
---
# Alerts

<div class="kb-summary">
Azure Monitor Alerts proactively notify you when conditions in your monitored resources are met. Alert rules evaluate signals — metrics, log queries, or activity log events — and fire when thresholds are crossed. Action groups define who gets notified and how.

*Applies to: Azure*
</div>

## Alert Flow

```d2
direction: right

signal: "Signal Source\nMetric · Log · Activity Log" {shape: rectangle}
alertRule: "Alert Rule\nthreshold · window · frequency" {shape: rectangle}
fired: "fired" {shape: rectangle}
actionGroup: "Action Group\nemail · SMS · webhook · Logic App" {shape: rectangle}
notify: "Notification\nOps team notified" {shape: rectangle}
resolved: "Alert Resolved\nauto or manual" {shape: rectangle}
suppress: "Suppressed\n(alert processing rule" {shape: rectangle}

signal -> alertRule
alertRule -> fired
actionGroup -> notify
notify -> resolved
```

## Alert Rule Types

| Rule Type          | Signal Source          | Typical Use Case                          |
|--------------------|------------------------|-------------------------------------------|
| Metric alert       | Platform metrics       | CPU > 80%, disk I/O threshold             |
| Log search alert   | KQL query on LA/ADX    | Error count spike, missing heartbeats     |
| Activity log alert | Activity log events    | Resource deletion, RBAC changes           |
| Smart detection    | Application Insights   | Anomaly detection, failure rate changes   |
| Resource health    | Resource health events | VM became unavailable                     |

## Creating Alert Rules

```bash
# Metric alert — CPU > 85% for 5 minutes on a VM
az monitor metrics alert create \
  --name "high-cpu-alert" \
  --resource-group myRG \
  --scopes /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM \
  --condition "avg Percentage CPU > 85" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --action /subscriptions/<sub-id>/resourceGroups/myRG/providers/microsoft.insights/actionGroups/ops-ag \
  --description "VM CPU exceeded 85%"

# Log search alert — no heartbeat in 10 minutes
az monitor scheduled-query create \
  --name "missing-heartbeat" \
  --resource-group myRG \
  --scopes /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.OperationalInsights/workspaces/myWorkspace \
  --condition-query "Heartbeat | summarize LastHeartbeat=max(TimeGenerated) by Computer | where LastHeartbeat < ago(10m)" \
  --condition-threshold 0 \
  --condition-operator GreaterThan \
  --evaluation-frequency 5m \
  --window-duration 10m \
  --severity 1 \
  --action-groups /subscriptions/<sub-id>/resourceGroups/myRG/providers/microsoft.insights/actionGroups/ops-ag
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Insights/metricAlerts/high-cpu-alert",
  "name": "high-cpu-alert",
  "type": "Microsoft.Insights/metricAlerts",
  "location": "global",
  "tags": {},
  "properties": {
    "description": "VM CPU exceeded 85%",
    "severity": 2,
    "enabled": true,
    "scopes": [
      "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM"
    ],
    "evaluationFrequency": "PT1M",
    "windowSize": "PT5M",
    "criteria": {
      "allOf": [
        {
          "metricName": "Percentage CPU",
          "operator": "GreaterThan",
          "threshold": 85.0,
          "timeAggregation": "Average"
        }
      ]
    },
    "actions": [
      {
        "actionGroupId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/microsoft.insights/actionGroups/ops-ag"
      }
    ]
  }
}
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Insights/scheduledQueryRules/missing-heartbeat",
  "name": "missing-heartbeat",
  "type": "Microsoft.Insights/scheduledQueryRules",
  "location": "eastus",
  "properties": {
    "description": "",
    "severity": 1,
    "enabled": true,
    "scopes": [
      "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.OperationalInsights/workspaces/myWorkspace"
    ],
    "evaluationFrequency": "PT5M",
    "windowDuration": "PT10M",
    "criteria": {
      "allOf": [
        {
          "query": "Heartbeat | summarize LastHeartbeat=max(TimeGenerated) by Computer | where LastHeartbeat < ago(10m)",
          "threshold": 0,
          "operator": "GreaterThan"
        }
      ]
    },
    "actions": {
      "actionGroups": [
        "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/microsoft.insights/actionGroups/ops-ag"
      ]
    }
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `(InvalidResourceId) : The provided resource id '<resource-id>' is invalid.` | Verify the subscription ID and resource path are correct by running `az resource list --resource-group myRG` to confirm the exact resource ID. |
    **`(ResourceNotFound) : The resource 'Microsoft.Insights/actionGroups/ops-
## Action Groups

Action groups define the notification channels and automation triggered when an alert fires.

```bash
# Create an action group with email and webhook
az monitor action-group create \
  --name "ops-action-group" \
  --resource-group myRG \
  --short-name "OpsAG" \
  --action email primary-email ops@example.com \
  --action webhook ops-webhook https://hooks.example.com/alert

# Add a second email receiver
az monitor action-group update \
  --name "ops-action-group" \
  --resource-group myRG \
  --add-action email secondary-email oncall@example.com

# List action groups in a resource group
az monitor action-group list \
  --resource-group myRG \
  --output table
```


```text title="Expected output"
{
  "eTag": "W/\"1704067234000\"",
  "groupShortName": "OpsAG",
  "id": "/subscriptions/12a34b5c-d6e7-8f9a-0b1c-2d3e4f5a6b7c/resourceGroups/myRG/providers/microsoft.insights/actionGroups/ops-action-group",
  "location": "global",
  "name": "ops-action-group",
  "resourceGroup": "myRG",
  "type": "Microsoft.Insights/actionGroups"
}
{
  "eTag": "W/\"1704067245000\"",
  "groupShortName": "OpsAG",
  "id": "/subscriptions/12a34b5c-d6e7-8f9a-0b1c-2d3e4f5a6b7c/resourceGroups/myRG/providers/microsoft.insights/actionGroups/ops-action-group",
  "location": "global",
  "name": "ops-action-group",
  "resourceGroup": "myRG",
  "type": "Microsoft.Insights/actionGroups"
}
Name                  ResourceGroup    GroupShortName    Location
--------------------  ---------------  ----------------  --------
ops-action-group      myRG             OpsAG             global
backup-action-group   myRG             BAG               global
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `(ResourceNotFound) Resource 'Microsoft.Insights/actionGroups/ops-action-group' does not exist in resource group 'myRG'.` | Verify the resource group name matches and the action group was created successfully in the correct subscription. |
    | `(InvalidParameter) The action group short name 'OpsAG' is invalid. It must be 1-12 characters.` | Reduce the short-name to 12 characters or fewer. |
## Alert Processing Rules

Alert processing rules allow you to suppress, add action groups, or modify alerts after they fire — without changing the alert rule itself. Useful for maintenance windows.

```bash
# Suppress all alerts during a maintenance window
az monitor alert-processing-rule create \
  --name "maintenance-suppression" \
  --resource-group myRG \
  --rule-type Suppression \
  --scopes /subscriptions/<sub-id>/resourceGroups/myRG \
  --schedule-recurrence-type Once \
  --schedule-start-datetime "2026-05-10 02:00:00" \
  --schedule-end-datetime "2026-05-10 06:00:00" \
  --description "Suppress during weekend maintenance"

# List alert processing rules
az monitor alert-processing-rule list \
  --resource-group myRG \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Microsoft.AlertsManagement/alertProcessingRules/maintenance-suppression",
  "name": "maintenance-suppression",
  "resourceGroup": "myRG",
  "ruleType": "Suppression",
  "scopes": [
    "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG"
  ],
  "schedule": {
    "recurrenceType": "Once",
    "startDateTime": "2026-05-10T02:00:00Z",
    "endDateTime": "2026-05-10T06:00:00Z"
  },
  "description": "Suppress during weekend maintenance",
  "enabled": true
}
Name                          ResourceGroup    RuleType      Enabled
------------------------------  ---------------  -----------  ---------
maintenance-suppression       myRG             Suppression   True
critical-alert-filter         myRG             Suppression   True
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Invalid resource ID format. The scope must be a valid Azure resource ID.` | Ensure the subscription ID in the `--scopes` parameter is a valid UUID and matches your actual subscription. |
    | `The resource group 'myRG' could not be found.` | Verify the resource group exists in your subscription using `az group list` and correct the `--resource-group` parameter. |
    | `The provided schedule times are invalid: start time must be before end time.` | Confirm that `--schedule-start-datetime` is earlier than `--schedule-end-datetime` in ISO 8601 format. |
## Alert Severity Levels

| Severity | Label     | Typical Meaning                         |
|----------|-----------|-----------------------------------------|
| 0        | Critical  | Service down, data loss imminent        |
| 1        | Error     | Significant degradation                 |
| 2        | Warning   | Approaching threshold, needs attention  |
| 3        | Informational | Notable event, no immediate action  |
| 4        | Verbose   | Diagnostic detail                       |

## Viewing and Managing Fired Alerts

```bash
# List currently fired alerts
az monitor alerts-management list \
  --resource-group myRG \
  --output table

# Get details on a specific alert
az monitor alerts-management show \
  --id /subscriptions/<sub-id>/providers/Microsoft.AlertsManagement/alerts/<alert-id>

# Change alert state to Acknowledged
az monitor alerts-management update \
  --id /subscriptions/<sub-id>/providers/Microsoft.AlertsManagement/alerts/<alert-id> \
  --status Acknowledged
```


```text title="Expected output"
ResourceGroup    Name                          State        Severity    MonitorService
---------------  ----------------------------  -----------  ----------  ----------------
myRG             High CPU on vm-prod-01        Fired        High        Platform
myRG             Low Disk Space - sql-db-02    Fired        Medium      Application Insights
myRG             Memory Alert - app-server-03  Fired        Critical    VM Insights
myRG             Network Latency Spike         Fired        Low         Application Insights

Id: /subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.AlertsManagement/alerts/alert-12345678-90ab-cdef-1234-567890abcdef
Name: High CPU on vm-prod-01
State: Fired
Severity: High
MonitorService: Platform
Description: CPU utilization exceeded 90% threshold for 5 minutes
LastModifiedDateTime: 2024-01-15T14:32:18.5432109Z
LastModifiedBy: System

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The resource with id '/subscriptions/<sub-id>/providers/Microsoft.AlertsManagement/alerts/<alert-id>' does not exist.` | Replace `<sub-id>` and `<alert-id>` with actual values from the `az monitor alerts-management list` output. |
    | `AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'microsoft.alertsManagement/alerts/read' over scope '/subscriptions/<sub-id>/resourceGroups/myRG'.` | Ensure your Azure account has the "Monitoring Contributor" or "Alert Management Operator" role assigned to the resource group or subscription. |
## Alert Rule Maintenance

```bash
# Disable an alert rule (e.g. during planned work)
az monitor metrics alert update \
  --name "high-cpu-alert" \
  --resource-group myRG \
  --enabled false

# Re-enable after maintenance
az monitor metrics alert update \
  --name "high-cpu-alert" \
  --resource-group myRG \
  --enabled true

# Delete an obsolete alert rule
az monitor metrics alert delete \
  --name "high-cpu-alert" \
  --resource-group myRG
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/myRG/providers/microsoft.insights/metricsAlerts/high-cpu-alert",
  "location": "global",
  "name": "high-cpu-alert",
  "resourceGroup": "myRG",
  "enabled": false,
  "severity": 3,
  "scopes": [
    "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/prod-vm-01"
  ],
  "evaluationFrequency": "PT1M",
  "windowSize": "PT5M"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/myRG/providers/microsoft.insights/metricsAlerts/high-cpu-alert",
  "name": "high-cpu-alert",
  "enabled": true,
  "resourceGroup": "myRG"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `(ResourceNotFound) The alert rule 'high-cpu-alert' does not exist in resource group 'myRG'.` | Verify the alert name and resource group with `az monitor metrics alert list --resource-group myRG`. |
    | `(AuthorizationFailed) The client 'user@example.com' with object id 'abc123...' does not have authorization to perform action 'microsoft.insights/metricsAlerts/write' over scope '/subscriptions/...'.` | Ensure your Azure account has the Monitoring Contributor role assigned to the subscription or resource group. |