---
tags:
  - azure
description: "Azure Reserved Instances (RIs) offer significant discounts (up to 72%) over pay-as-you-go pricing in exchange for a 1-year or 3-year commitment..."
---
# Reservations

<div class="kb-summary">
Azure Reserved Instances (RIs) offer significant discounts (up to 72%) over pay-as-you-go pricing in exchange for a 1-year or 3-year commitment. Reservations apply to VMs, SQL Databases, Cosmos DB, Storage, and other services.

*Applies to: Azure*
</div>

## Reservation Discount Application

```d2
direction: right

purchase: "Purchase Reservation\n1-yr or 3-yr commitment" {shape: rectangle}
scope: "scope" {shape: rectangle}
shared: "Shared Scope\napplies across all subscriptions" {shape: rectangle}
single: "Single Subscription Scope\napplies to one subscription" {shape: rectangle}
rgScope: "Resource Group Scope\nnarrowest" {shape: rectangle}
usage: "Matching Resource Usage\nsame SKU · region · OS" {shape: rectangle}
discount: "Reservation Discount Applied\n(automatic — no action needed" {shape: rectangle}
unused: "Unused Capacity\nno refund — choose carefully" {shape: rectangle}

purchase -> scope
scope -> shared
shared -> single
single -> rgScope
rgScope -> usage
usage -> discount
usage -> unused
```

## RI Purchasing

Reservations are purchased at the billing account or subscription level. The reservation scope determines which subscriptions benefit from the discount.

```bash
# List available reservation orders
az reservation reservation-order list \
  --output table

# Show details of a specific reservation order
az reservation reservation-order show \
  --reservation-order-id <order-id>

# List reservations within an order
az reservation reservation list \
  --reservation-order-id <order-id> \
  --output table

# Show a specific reservation
az reservation reservation show \
  --reservation-order-id <order-id> \
  --reservation-id <reservation-id>
```


```text title="Expected output"
ReservationOrderId                       DisplayName                    CreatedDateTime      ExpiryDateTime       BenefitStartTime     Term
---------------------------------------- ------------------------------ -------------------- -------------------- -------------------- ------
00000000-0000-0000-0000-000000000001     Reserved Instance - Compute    2023-06-15T10:30:00Z 2025-06-15T10:30:00Z 2023-06-15T00:00:00Z P1Y
00000000-0000-0000-0000-000000000002     Reserved Instance - Storage    2023-08-22T14:15:00Z 2026-08-22T14:15:00Z 2023-08-22T00:00:00Z P3Y

ReservationId                            DisplayName                    State      ExpiryDate           ProvisioningState
------------------------------------ -------------------------------- ---------- -------------------- ------------------
11111111-1111-1111-1111-111111111111 Reserved Instance - Compute-1    Succeeded  2025-06-15T00:00:00Z Succeeded
11111111-1111-1111-1111-111111111112 Reserved Instance - Compute-2    Succeeded  2025-06-15T00:00:00Z Succeeded

{
  "id": "/providers/Microsoft.Capacity/reservationOrders/00000000-0000-0000-0000-000000000001/reservations/11111111-1111-1111-1111-111111111111",
  "name": "11111111-1111-1111-1111-111111111111",
  "properties": {
    "displayName": "Reserved Instance - Compute-1",
    "appliedScopes": [
      "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    ],
    "quantity": 1,
    "provisioningState": "Succeeded",
    "expiryDate": "2025-06-15",
    "skuDescription": "Compute_Standard_D2s_v3_1_Year"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The provided reservation order ID '<order-id>' does not exist.` | Replace `<order-id>` with a valid reservation order ID from the `az reservation reservation-order list` output. |
    | `Authorization failed for template deployment. The client '<client-id>' with object id '<object-id>' does not have permission to perform action 'Microsoft.Capacity/reservationOrders/read' over scope '/subscriptions/<subscription-id>'.` | Ensure your Azure account has the Reader role or higher on the subscription containing the reservations. |
### Purchase Workflow

Reservations are purchased through the Azure portal or REST API. The CLI is used primarily for post-purchase management (listing, scope changes, exchange/refund).

| Step | Action |
|---|---|
| 1. Identify candidates | Use Advisor recommendations to find VMs suitable for RIs |
| 2. Validate workload | Confirm VM runs 24/7 with consistent SKU requirements |
| 3. Choose term | 1-year (~40% savings) vs 3-year (~72% savings) |
| 4. Choose scope | Shared (all subscriptions) vs single subscription |
| 5. Purchase | Portal → Reservations → Add |
| 6. Monitor utilisation | Check within 7 days; low utilisation = misconfigured scope |

## Reservation Scope

Scope determines which Azure usage the reservation discount is applied to.

| Scope | Description |
|---|---|
| Shared | Applies across all subscriptions in the billing account/enrolment |
| Single subscription | Applies only to the nominated subscription |
| Single resource group | Applies only to VMs in the nominated resource group |
| Management group | Applies to all subscriptions in the management group |

```bash
# Update the scope of an existing reservation
az reservation reservation update \
  --reservation-order-id <order-id> \
  --reservation-id <reservation-id> \
  --applied-scope-type Shared
```


```text title="Expected output"
{
  "id": "/providers/microsoft.capacity/reservationOrders/50000000-aaaa-bbbb-cccc-100000000000/reservations/60000000-dddd-eeee-ffff-200000000000",
  "name": "60000000-dddd-eeee-ffff-200000000000",
  "type": "Microsoft.Capacity/reservationOrders/reservations",
  "sku": {
    "name": "Standard_D2s_v3"
  },
  "properties": {
    "appliedScopeType": "Shared",
    "appliedScopes": [],
    "quantity": 1,
    "provisioningState": "Succeeded",
    "displayName": "Compute_SavingsPlan",
    "effectiveDateTime": "2024-01-15T00:00:00Z",
    "lastUpdatedDateTime": "2024-01-20T14:32:18.5432109Z",
    "expiryDate": "2025-01-15"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `InvalidParameterValue: The provided reservation order ID is invalid or not found.` | Verify the reservation order ID exists in your subscription using `az reservation reservation-order list`. |
    | `AuthorizationFailed: The client does not have permission to perform action 'Microsoft.Capacity/reservationOrders/reservations/write' on scope.` | Ensure your Azure account has Owner or Contributor role on the subscription containing the reservation. |
    | `BadRequest: Cannot change scope type from Single to Shared when reservation has applied scopes defined.` | Remove existing applied scopes first using `az reservation reservation update --applied-scopes ""` before changing scope type. |
## Exchange and Refund

Reservations can be exchanged for a different SKU or region, or refunded (subject to a 12% early termination fee and $50,000/year refund cap).

```bash
# Get the reservation details needed before an exchange
az reservation reservation show \
  --reservation-order-id <order-id> \
  --reservation-id <reservation-id> \
  --query "{SKU:sku.name, Scope:properties.appliedScopeType, Quantity:properties.quantity, ExpiryDate:properties.expiryDate}"

# Exchanges and refunds are processed via the portal or REST API
# REST endpoint: POST /providers/Microsoft.Capacity/reservationOrders/{orderId}/exchange
```


```text title="Expected output"
{
  "SKU": "Standard_D2s_v3",
  "Scope": "Shared",
  "Quantity": 5,
  "ExpiryDate": "2026-03-15T00:00:00Z"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The provided reservation order ID '<order-id>' is invalid or does not exist.` | Verify the reservation order ID by running `az reservation reservation-order list` and copy the exact ID from the output. |
    | `No subscriptions found in your account. Please call 'az account set' to select a subscription.` | Set your active subscription with `az account set --subscription <subscription-id>` before running the command. |
## Utilisation Monitoring

Low utilisation means the discount is being wasted. Track utilisation and act quickly if it drops below 80%.

```bash
# Get utilisation summary for all reservations
az consumption reservation summary list \
  --reservation-order-id <order-id> \
  --grain daily \
  --output table

# Get detail-level utilisation
az consumption reservation detail list \
  --reservation-order-id <order-id> \
  --start-date 2026-05-01 \
  --end-date 2026-05-07 \
  --output table
```


```text title="Expected output"
ReservationOrderId                       ReservationId                            UsageDate            SkuName                  TotalReservedQuantity    TotalUsedQuantity    UnusedQuantity    UtilizationPercentage
---------------------------------------- ---------------------------------------- -------------------- ---------------------- ----------------------- -------------------- ------------------- ----------------------
550e8400-e29b-41d4-a716-446655440000     6ba7b810-9dad-11d1-80b4-00c04fd430c8     2026-05-01           Standard_D4s_v3         100.0                  87.5                 12.5                 87.5
550e8400-e29b-41d4-a716-446655440000     6ba7b810-9dad-11d1-80b4-00c04fd430c8     2026-05-02           Standard_D4s_v3         100.0                  92.0                 8.0                  92.0
550e8400-e29b-41d4-a716-446655440000     6ba7b810-9dad-11d1-80b4-00c04fd430c8     2026-05-03           Standard_D4s_v3         100.0                  100.0                0.0                  100.0
550e8400-e29b-41d4-a716-446655440000     6ba7b810-9dad-11d1-80b4-00c04fd430c8     2026-05-04           Standard_D4s_v3         100.0                  78.5                 21.5                 78.5
550e8400-e29b-41d4-a716-446655440000     6ba7b810-9dad-11d1-80b4-00c04fd430c8     2026-05-05           Standard_D4s_v3         100.0                  95.0                 5.0                  95.0

ReservationOrderId                       ReservationId                            InstanceId                                                           UsageDate            SkuName                  ReservedQuantity    UsedQuantity    ChargeType
---------------------------------------- ---------------------------------------- ------------------------------------------------------------------ -------------------- ---------------------- ------------------- -------------- ----------------
550e8400-e29b-41d4-a716-446655440000     6ba7b810-9dad-11d1-80b4-00c04fd430c8     /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/vm-prod-01     2026-05-01           Standard_D4s_v3         50.0                45.0            Reserved
550e8400-e29b-41d4-a716-446655440000     6ba7b810-9dad-11d1-80b4-00c04fd430c8     /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/vm-prod-02     2026-05-01           Standard_D4s_v3         50.0                42.5            Reserved
550e8400-e29
```
### Utilisation Thresholds

| Utilisation % | Status | Action |
|---|---|---|
| > 95 % | Healthy | No action |
| 80–95 % | Acceptable | Monitor; consider scope widening |
| 60–80 % | Warning | Review scope or consider exchange |
| < 60 % | Critical | Exchange or refund; investigate misconfiguration |

## Reservation Best Practices

- Purchase RIs only for stable, predictable workloads — not dev/test or auto-scaled services with variable SKUs.
- Start with `Shared` scope to maximise coverage across all subscriptions.
- Set a calendar reminder at 90 days before expiry to decide on renewal or exchange.
- Review Advisor's RI recommendations monthly — it surfaces new candidates as workloads stabilise.
- Track savings using the amortised cost export to quantify RI benefit over pay-as-you-go.
