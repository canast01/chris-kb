# Alerts

Azure Monitor Alerts proactively notify you when conditions in your monitored resources are met. Alert rules evaluate signals — metrics, log queries, or activity log events — and fire when thresholds are crossed. Action groups define who gets notified and how.

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
