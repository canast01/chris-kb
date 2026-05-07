# Cost Alerts

Azure Cost Management supports multiple alert types to notify teams of unexpected or excessive spending. Alerts complement budgets and provide finer-grained visibility into spend anomalies.

## Alert Types

| Alert Type | Trigger | Configuration |
|---|---|---|
| Budget alerts | Spend crosses a budget threshold | Defined on the budget object |
| Anomaly alerts | ML-detected unusual spend pattern | Enabled per subscription in Cost Management |
| Credit alerts | Azure credit balance falls below threshold | EA/MCA accounts only |
| Department quota alerts | Department quota approaching | EA accounts only |

## Anomaly Alerts

Anomaly detection uses machine learning to identify spend spikes that deviate from historical patterns. No manual threshold is required — Azure learns the baseline automatically.

```bash
# List existing cost alerts on a scope
az costmanagement alert list \
  --scope "/subscriptions/<subscription-id>" \
  --output table

# Show a specific alert
az costmanagement alert show \
  --alert-id <alert-id> \
  --scope "/subscriptions/<subscription-id>"

# Dismiss an anomaly alert
az costmanagement alert dismiss \
  --alert-id <alert-id> \
  --scope "/subscriptions/<subscription-id>"
```

### Anomaly Alert Properties

| Property | Description |
|---|---|
| Detection confidence | Low / Medium / High |
| Affected service | Azure service with the spike |
| Spike amount | Estimated overspend vs baseline |
| Detection date | When the anomaly was identified |
| Affected period | Start and end of the anomalous window |

## Budget Alerts

Budget alerts are the most commonly used cost alert type. They fire based on percentage thresholds against a named budget.

```bash
# List all budget-linked alerts on a subscription
az costmanagement alert list \
  --scope "/subscriptions/<subscription-id>" \
  --query "[?properties.definition.type=='Budget']" \
  --output table

# View notification config on a budget
az costmanagement budget show \
  --budget-name "monthly-sub-budget" \
  --scope "/subscriptions/<subscription-id>" \
  --query "properties.notifications"
```

## Alert Channels

Alerts are delivered through one or more of the following channels:

| Channel | Configuration |
|---|---|
| Email (direct) | List of email addresses on the budget notification |
| Action Group | Azure Monitor Action Group (email, SMS, webhook, Logic App) |
| Azure Monitor alerts | Via diagnostic settings and metric alert rules |

```bash
# Create an Action Group with email and webhook receivers
az monitor action-group create \
  --resource-group rg-finops \
  --name ag-cost-critical \
  --short-name cost-crit \
  --action email finops-lead finops@example.com \
  --action webhook cost-webhook https://hooks.example.com/cost-alert

# List Action Groups in the finops resource group
az monitor action-group list \
  --resource-group rg-finops \
  --output table
```

## Threshold Configuration

For budget-based alerts the threshold is a percentage of the budget amount. Thresholds should be set in tiers to give progressive warning.

| Threshold % | Threshold Type | Recipient | Purpose |
|---|---|---|---|
| 70 % | Forecasted | Team lead | Early awareness |
| 90 % | Forecasted | Team lead + FinOps | Time to investigate |
| 80 % | Actual | Team lead | Confirmed trending high |
| 100 % | Actual | Team lead + FinOps + Management | Budget breached |

## Alert State Management

Alerts have a state of `Active`, `Overridden`, `Resolved`, or `Dismissed`. Dismissed alerts are suppressed until the next billing period resets.

```bash
# List active alerts only
az costmanagement alert list \
  --scope "/subscriptions/<subscription-id>" \
  --query "[?properties.status=='Active']" \
  --output table
```

## Alert Best Practices

- Always pair anomaly detection with a budget alert — anomaly detection catches unexpected spikes; budgets catch slow overruns.
- Route alerts to a shared team mailbox and an Action Group webhook so alerts are never missed during holidays.
- Review dismissed alerts monthly — a pattern of dismissals may indicate a budget that needs updating.
- Test alert delivery by temporarily lowering the budget threshold to a value already exceeded, then restore after confirming receipt.
