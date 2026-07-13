---
tags:
  - azure
description: "Azure Cost Management budgets let you set spending thresholds and trigger alerts or automated actions when spending approaches or exceeds those..."
---
# Budgets

<div class="kb-summary">
Azure Cost Management budgets let you set spending thresholds and trigger alerts or automated actions when spending approaches or exceeds those thresholds. Budgets are scoped to a management group, subscription, or resource group.

*Applies to: Azure*
</div>

## Budget Alert Flow

```d2
direction: right

budget: "Budget\n(subscription / RG scope" {shape: rectangle}
forecastActual: "Actual or Forecast Spend" {shape: rectangle}
threshold1: "threshold1" {shape: rectangle}
alert80: "Alert Notification\nemail · action group" {shape: rectangle}
actionGroup: "Action Group\nLogic App · webhook · ITSM" {shape: rectangle}
alert100: "Alert Notification\n100% budget reached" {shape: rectangle}
threshold2: "threshold2" {shape: rectangle}

budget -> forecastActual
forecastActual -> threshold1
alert80 -> actionGroup
alert100 -> actionGroup
```

## Creating a Budget

Budgets are created with the `az costmanagement budget create` command. You define the amount, time grain, start/end dates, and notification rules in one call.

```bash
# Create a monthly subscription-level budget with email alert at 80% and 100%
az costmanagement budget create \
  --budget-name "monthly-sub-budget" \
  --scope "/subscriptions/<subscription-id>" \
  --amount 5000 \
  --time-grain Monthly \
  --start-date 2026-05-01 \
  --end-date 2027-05-01 \
  --notifications '[
    {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 80,
      "contactEmails": ["finops@example.com"],
      "thresholdType": "Actual"
    },
    {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 100,
      "contactEmails": ["finops@example.com", "eng-leads@example.com"],
      "thresholdType": "Actual"
    }
  ]'

# List budgets on a subscription
az costmanagement budget list \
  --scope "/subscriptions/<subscription-id>" \
  --output table

# Show a specific budget
az costmanagement budget show \
  --budget-name "monthly-sub-budget" \
  --scope "/subscriptions/<subscription-id>"

# Delete a budget
az costmanagement budget delete \
  --budget-name "monthly-sub-budget" \
  --scope "/subscriptions/<subscription-id>"
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.CostManagement/budgets/monthly-sub-budget",
  "name": "monthly-sub-budget",
  "type": "Microsoft.CostManagement/budgets",
  "properties": {
    "displayName": "monthly-sub-budget",
    "category": "Cost",
    "amount": 5000.0,
    "timeGrain": "Monthly",
    "timePeriod": {
      "startDate": "2026-05-01T00:00:00Z",
      "endDate": "2027-05-01T00:00:00Z"
    },
    "notifications": {
      "Notification1": {
        "enabled": true,
        "operator": "GreaterThan",
        "threshold": 80,
        "thresholdType": "Actual",
        "contactEmails": ["finops@example.com"]
      },
      "Notification2": {
        "enabled": true,
        "operator": "GreaterThan",
        "threshold": 100,
        "thresholdType": "Actual",
        "contactEmails": ["finops@example.com", "eng-leads@example.com"]
      }
    }
  }
}

BudgetName          Category    Amount    TimeGrain    StartDate      EndDate
-------------------  ----------  --------  -----------  ---------------  ---------------
monthly-sub-budget   Cost        5000.0    Monthly      2026-05-01       2027-05-01
q3-resource-budget   Cost        8500.0    Monthly      2026-07-01       2026-09-30
annual-cap-budget    Cost        50000.0   Annually     2026-01-01       2026-12-31

{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.CostManagement/budgets/monthly-sub-budget",
  "name": "monthly-sub-budget",
  "properties": {
    "displayName": "monthly-sub-budget",
    "amount": 5000.0,
    "timeGrain": "Monthly"
  }
}

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: (InvalidRequest) Invalid scope format. Scope must be a valid resource ID.` | Replace `<subscription-id>` with your actual subscription ID (e.g., `a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d`). |
    | `ERROR: (AuthorizationFailed) The client 'user@example.com' with object id 'xxx' does not have authorization to perform action 'Microsoft.CostManagement/budgets/write' over scope '/subscriptions/xxx'.` | Ensure your user account has the Cost Management Contributor role assigned on the subscription. |
    **`ERROR: (BadRequest) Invalid JSON in notifications parameter: Unexpected character in JSON at position 45.
## Scope Options

Budgets can target different scopes. Use the narrowest scope that makes sense for the use case.

| Scope | Resource ID Pattern | Use Case |
|---|---|---|
| Management Group | `/providers/Microsoft.Management/managementGroups/<mg-id>` | Organisation-wide cap |
| Subscription | `/subscriptions/<sub-id>` | Per-environment budget |
| Resource Group | `/subscriptions/<sub-id>/resourceGroups/<rg>` | Per-team or per-project |
| Billing Account | `/providers/Microsoft.Billing/billingAccounts/<id>` | EA/MCA billing control |
| Invoice Section | `/providers/Microsoft.Billing/billingAccounts/<id>/invoiceSections/<id>` | Department-level |

```bash
# Create a resource-group-scoped budget
az costmanagement budget create \
  --budget-name "team-alpha-monthly" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-team-alpha" \
  --amount 1000 \
  --time-grain Monthly \
  --start-date 2026-05-01 \
  --end-date 2027-05-01
```


```text title="Expected output"
{
  "eTag": "\"1d00c8e0-0000-0100-0000-67a4f2c10000\"",
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/rg-team-alpha/providers/Microsoft.CostManagement/budgets/team-alpha-monthly",
  "name": "team-alpha-monthly",
  "properties": {
    "amount": 1000.0,
    "category": "Cost",
    "currentSpend": {
      "amount": 247.53,
      "unit": "USD"
    },
    "endDate": "2027-05-01T00:00:00Z",
    "notifications": {},
    "startDate": "2026-05-01T00:00:00Z",
    "timeGrain": "Monthly",
    "timePeriod": {
      "endDate": "2027-05-01T00:00:00Z",
      "startDate": "2026-05-01T00:00:00Z"
    }
  },
  "type": "Microsoft.CostManagement/budgets"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound: The resource group 'rg-team-alpha' could not be found.` | Verify the resource group name exists in the subscription using `az group list --query "[].name"`. |
    | `InvalidParameter: The value of parameter 'scope' is invalid.` | Ensure the subscription ID is correct and the scope format is exactly `/subscriptions/<sub-id>/resourceGroups/<rg-name>` with no trailing slashes. |
    | `AuthorizationFailed: The client does not have authorization to perform action 'Microsoft.CostManagement/budgets/write'.` | Assign the user or service principal the "Cost Management Contributor" role on the resource group or subscription. |
## Alert Thresholds

Each budget supports up to five notification rules. Notifications fire when actual or forecasted spend crosses a percentage of the budget amount.

### Threshold Types

| Type | Description |
|---|---|
| Actual | Fires when cumulative spend in the period exceeds the threshold |
| Forecasted | Fires when projected end-of-period spend exceeds the threshold |

Recommended tier structure:

| Threshold % | Threshold Type | Purpose |
|---|---|---|
| 70 % | Forecasted | Early awareness |
| 90 % | Forecasted | Time to investigate |
| 80 % | Actual | Confirmed trending high |
| 100 % | Actual | Budget breached |

## Action Groups

In addition to email notifications, budgets can trigger an Azure Action Group to run Logic Apps, webhooks, or Function Apps.

```bash
# Create an Action Group for budget alerts
az monitor action-group create \
  --resource-group rg-finops \
  --name ag-budget-alerts \
  --short-name budg-alert \
  --action email finops-team finops@example.com

# Get the Action Group resource ID
az monitor action-group show \
  --resource-group rg-finops \
  --name ag-budget-alerts \
  --query id \
  --output tsv
```


```text title="Expected output"
{
  "armId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-finops/providers/microsoft.insights/actionGroups/ag-budget-alerts",
  "enabled": true,
  "groupShortName": "budg-alert",
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-finops/providers/microsoft.insights/actionGroups/ag-budget-alerts",
  "location": "global",
  "name": "ag-budget-alerts",
  "resourceGroup": "rg-finops",
  "tags": {},
  "type": "Microsoft.Insights/actionGroups"
}
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-finops/providers/microsoft.insights/actionGroups/ag-budget-alerts
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound : Resource group 'rg-finops' could not be found.` | Create the resource group first with `az group create --name rg-finops --location eastus`. |
    | `InvalidEmailAddress : The email address 'finops@example.com' is invalid or the action cannot be created.` | Verify the email address is correctly formatted and the recipient has accepted the action group notification. |
## Budget Best Practices

| Practice | Rationale |
|---|---|
| Set budgets at subscription and RG level | Dual coverage — broad and granular |
| Use forecasted thresholds at 90% | Early warning before actual breach |
| Attach Action Group for auto-remediation | Enables automated shutdown of non-prod VMs |
| Review and update amounts quarterly | Aligns budgets with approved spend plans |
| Tag budgets with owner metadata | Accountability for overspend |
