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

## Utilisation Monitoring

Monitor savings plan utilisation to ensure the committed hourly spend is being consumed.

```bash
# Get utilisation summary for a savings plan
az consumption savings-plan-utilization-summary list \
  --savings-plan-order-id <order-id> \
  --grain daily \
  --output table
```

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
