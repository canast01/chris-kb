---
tags:
  - azure
---
# Savings Plans

<div class="kb-summary">
Azure Compute Savings Plans provide discounts (up to 65%) in exchange for a consistent hourly compute spend commitment over 1 or 3 years. Unlike Reserved Instances, savings plans apply automatically across VM families, regions, and compute services, giving more flexibility.

*Applies to: Azure*
</div>

## Cost Commitment Options

```d2
direction: right

decision: "Cost Optimisation\nDecision" {shape: rectangle}
stable: "stable" {shape: rectangle}
reservedInstance: "Reserved Instance\nup to 72% discount\nSKU + region locked" {shape: rectangle}
savingsPlan: "Savings Plan\nup to 65% discount\nflexible across SKU + region" {shape: rectangle}
paygo: "Pay-As-You-Go\nno commitment\nhighest cost" {shape: rectangle}
singleSKU: "singleSKU" {shape: rectangle}

decision -> stable
```

## Savings Plan vs Reserved Instances

| Dimension | Savings Plan | Reserved Instance |
|---|---|---|
| Commitment basis | Hourly spend (e.g., $10/hr) | Specific VM SKU and region |
| Flexibility | Any VM family, region, OS | Instance size flexible within family |
| Max discount | ~65 % | ~72 % |
| Best for | Diverse or shifting workloads | Stable, predictable single-SKU workloads |
| Covered services | VMs, AKS, Azure Functions Premium | VMs, SQL DB, Cosmos DB, Storage, etc. |

## Hourly Commitment

The commitment is expressed as a consistent hourly spend in USD. Azure applies the discounted rate to eligible compute usage up to the committed amount; usage beyond the commitment is billed at pay-as-you-go.

```bash
# List existing savings plan orders
az billing savings-plan-order list \
  --output table

# Show a specific savings plan order
az billing savings-plan-order show \
  --savings-plan-order-id <order-id>

# List savings plans within an order
az billing savings-plan-order savings-plan list \
  --savings-plan-order-id <order-id> \
  --output table

# Show a specific savings plan
az billing savings-plan-order savings-plan show \
  --savings-plan-order-id <order-id> \
  --savings-plan-id <savings-plan-id>
```


```text title="Expected output"
Name                             OrderId                              Status    ExpiryDate          BillingPlan
-------------------------------  ------------------------------------  --------  -------------------  -----------
sp-order-prod-2024              /subscriptions/12a4b5c6-d7e8-9f0a-1b2c-3d4e5f6g7h8i/providers/Microsoft.BillingBenefits/savingsPlanOrders/sp-order-prod-2024  Active    2027-03-15           Monthly
sp-order-dev-2024               /subscriptions/87f6e5d4-c3b2-a1f0-9e8d-7c6b5a4f3e2d/providers/Microsoft.BillingBenefits/savingsPlanOrders/sp-order-dev-2024    Active    2026-11-20           Upfront

{
  "id": "/subscriptions/12a4b5c6-d7e8-9f0a-1b2c-3d4e5f6g7h8i/providers/Microsoft.BillingBenefits/savingsPlanOrders/sp-order-prod-2024",
  "name": "sp-order-prod-2024",
  "status": "Active",
  "expiryDate": "2027-03-15",
  "billingPlan": "Monthly",
  "term": "P3Y"
}

SavingsPlanId                    DisplayName              Status    Term    AppliedScopeType
---------------------------------  -----------------------  --------  ------  ------------------
sp-vm-prod-001                   Production VM Savings    Active    P3Y     Single
sp-sql-prod-002                  SQL Database Savings     Active    P3Y     Shared

{
  "id": "/subscriptions/12a4b5c6-d7e8-9f0a-1b2c-3d4e5f6g7h8i/providers/Microsoft.BillingBenefits/savingsPlanOrders/sp-order-prod-2024/savingsPlans/sp-vm-prod-001",
  "displayName": "Production VM Savings",
  "status": "Active",
  "term": "P3Y",
  "appliedScopeType": "Single",
  "commitment": {
    "currencyCode": "USD",
    "amount": 15000.00
  }
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The resource 'Microsoft.BillingBenefits/savingsPlanOrders/<order-id>' does not exist.`** — Verify the savings plan order ID is correct and exists in your subscription using `az billing savings-plan-order list`.
    **`(AuthorizationFailed) The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.BillingBenefits/savingsPlanOrders/read'.`** — Ensure your Azure account has Billing Reader or Owner role assigned at the subscription or billing account scope.
### Choosing the Right Hourly Commitment

```bash
# Use Advisor to get a recommended commitment amount
az advisor recommendation list \
  --category Cost \
  --query "[?contains(shortDescription.solution, 'savings plan')]" \
  --output table

# Query current compute spend to estimate commitment baseline
az costmanagement query \
  --scope "/subscriptions/<subscription-id>" \
  --type Usage \
  --timeframe MonthToDate \
  --dataset-aggregation '{"totalCost":{"name":"Cost","function":"Sum"}}' \
  --dataset-grouping '[{"type":"Dimension","name":"MeterCategory"}]' \
  --query "properties.rows[?@[1]=='Virtual Machines']"
```


```text title="Expected output"
RecommendationId                          Category    Impact    ShortDescription
────────────────────────────────────────  ──────────  ────────  ──────────────────────────────────────────────────────────
d4f8c2a1-9e3b-4d7f-b1c6-2a5e8f3d9c1b     Cost        High      Consider purchasing a compute savings plan to reduce costs
a7b2e9f1-3c5d-4a8b-9e2f-1d6c7a4b5e8f     Cost        Medium    Savings plan recommendation for your VM workloads

MeterCategory              TotalCost
─────────────────────────  ──────────
Virtual Machines           $4,287.32
Storage                    $892.15
Bandwidth                  $156.48
SQL Database               $423.67
```

!!! warning "Common errors"
    **`The subscription '<subscription-id>' could not be found.`** — Replace `<subscription-id>` with your actual subscription ID from `az account show --query id -o tsv`.
    **`InvalidApiVersionForOperation: The api-version '2021-10-01' does not support operations for this resource.`** — Update the Azure CLI to the latest version with `az upgrade`.
    **`No recommendations found matching the specified criteria.`** — Ensure your subscription has been enrolled in Azure Advisor for at least 24 hours and has active compute resources.
## Flexibility Scope

Savings plans apply across the breadth of Azure compute. The scope determines which subscriptions benefit.

| Scope | Description |
|---|---|
| Shared | Applies to all eligible compute across all subscriptions in the billing account |
| Single subscription | Applies only within the nominated subscription |
| Management group | Applies to all subscriptions in the management group |

```bash
# Update the scope of an existing savings plan
az billing savings-plan-order savings-plan update \
  --savings-plan-order-id <order-id> \
  --savings-plan-id <savings-plan-id> \
  --applied-scope-type Shared
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.BillingBenefits/savingsPlanOrders/sporder-20240115-abc123/savingsPlans/sp-789def456",
  "name": "sp-789def456",
  "type": "Microsoft.BillingBenefits/savingsPlans",
  "properties": {
    "displayName": "Compute Savings Plan",
    "provisioningState": "Succeeded",
    "appliedScopeType": "Shared",
    "appliedScopeProperties": null,
    "commitment": {
      "grain": "Hourly",
      "currencyCode": "USD",
      "amount": 3650.0
    },
    "userFriendlyAppliedScopeType": "Shared",
    "effectiveDateTime": "2024-01-15T00:00:00Z",
    "expiryDateTime": "2025-01-15T00:00:00Z",
    "purchaseDateTime": "2024-01-15T12:30:45Z",
    "status": "Active"
  }
}
```

!!! warning "Common errors"
    **`The savings plan order ID '<order-id>' does not exist or you do not have access to it.`** — Verify the order ID is correct and you have appropriate permissions on the subscription using `az billing savings-plan-order list`.
    **`Invalid appliedScopeType 'Shared'. Valid values are: 'Single', 'Shared', 'ManagementGroup'.`** — Ensure the `--applied-scope-type` parameter uses one of the three valid scope types.
    **`The savings plan cannot be updated because it is in 'Expired' status.`** — Only active or pending savings plans can be updated; check the plan status with `az billing savings-plan-order savings-plan show`.
## Utilisation Monitoring

Monitor savings plan utilisation to ensure the committed hourly spend is being consumed.

```bash
# Get utilisation summary for a savings plan
az consumption savings-plan-utilization-summary list \
  --savings-plan-order-id <order-id> \
  --grain daily \
  --output table
```


```text title="Expected output"
Grain    UsageDate            UtilizationPercentage    TotalHours    UsedHours
-------  -------------------  ----------------------  -----------  -----------
Daily    2024-01-15T00:00:00Z  87.5                    24           21
Daily    2024-01-16T00:00:00Z  92.3                    24           22.15
Daily    2024-01-17T00:00:00Z  78.9                    24           18.94
Daily    2024-01-18T00:00:00Z  100.0                   24           24
Daily    2024-01-19T00:00:00Z  65.4                    24           15.7
Daily    2024-01-20T00:00:00Z  81.2                    24           19.49
```

!!! warning "Common errors"
    **`The provided savings plan order ID is invalid or does not exist.`** — Verify the order ID format and confirm it exists in your subscription using `az consumption savings-plan-order list`.
    **`AuthorizationFailed: The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.Consumption/savingsPlanOrders/read'.`** — Ensure your Azure account has the Reader or Contributor role assigned on the subscription or savings plan resource.
    **`--savings-plan-order-id: expected one argument`** — Replace `<order-id>` with an actual savings plan order ID value (e.g., `spplan-12345678-1234-1234-1234-123456789012`).
### Utilisation Benchmarks

| Utilisation % | Status | Action |
|---|---|---|
| > 90 % | Healthy | No action required |
| 75–90 % | Acceptable | Review scope; ensure all eligible subs are covered |
| 50–75 % | Warning | Reduce commitment at next renewal or expand scope |
| < 50 % | Critical | Investigate — workload may have been decommissioned |

## Combining Savings Plans and Reserved Instances

Savings plans and RIs can coexist. Azure applies the RI discount first (because it is more specific), then applies the savings plan discount to remaining eligible usage.

| Scenario | Recommendation |
|---|---|
| Stable VM fleet | Use RIs for the stable base; savings plan for variable remainder |
| Diverse or changing SKUs | Savings plan only — avoids RI exchange overhead |
| AKS node pools | Savings plan (VM family flexibility across node pool changes) |
| SQL Managed Instance | Reserved Instances (savings plan does not cover SQL MI) |

## Purchase Checklist

- Confirm baseline compute spend over the last 30–90 days.
- Identify what percentage is consistent (good for RI) vs variable (good for savings plan).
- Use Advisor recommendations for suggested commitment amount.
- Choose 1-year term unless workload stability for 3 years is confirmed.
- Set `Shared` scope unless subscription isolation is required for chargeback.
- Review utilisation after 7 days and adjust scope if utilisation is below 80 %.
