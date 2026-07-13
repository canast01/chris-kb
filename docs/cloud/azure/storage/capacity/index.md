---
tags:
  - azure
description: "Capacity Monitoring reference covering Overview, Storage Account Metrics, Capacity Alerts, Container-Level Capacity, Forecasting and Trend Analysis and 1..."
---
# Azure Storage — Capacity Monitoring

<div class="kb-summary">
Capacity Monitoring reference covering Overview, Storage Account Metrics, Capacity Alerts, Container-Level Capacity, Forecasting and Trend Analysis and 1 more sections.

*Applies to: Azure*
</div>

```d2
direction: down

storage_account_metrics: "Storage Account Metrics" {shape: rectangle}
capacity_alerts: "Capacity Alerts" {shape: rectangle}
containerlevel_capacity: "Container-Level Capacity" {shape: rectangle}
forecasting_and_trend_analysis: "Forecasting and Trend Analysis" {shape: rectangle}
storage_account_limits_reference: "Storage Account Limits Reference" {shape: rectangle}

storage_account_metrics -> capacity_alerts: uses
capacity_alerts -> containerlevel_capacity: uses
containerlevel_capacity -> forecasting_and_trend_analysis: uses
forecasting_and_trend_analysis -> storage_account_limits_reference: uses
```

## Overview

Monitoring storage capacity in Azure involves tracking used capacity at the account and container level, setting metric alerts before quotas are hit, and projecting growth to plan ahead. Azure Monitor provides built-in storage metrics with 93-day retention.

## Storage Account Metrics

```bash
# Get current used capacity for a storage account (bytes)
az monitor metrics list \
  --resource "/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01" \
  --metric "UsedCapacity" \
  --interval PT1H \
  --output table

# Get blob service used capacity
az monitor metrics list \
  --resource "/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01/blobServices/default" \
  --metric "BlobCapacity" \
  --aggregation Average \
  --interval P1D \
  --output table

# Get file share used capacity
az monitor metrics list \
  --resource "/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodfiles01/fileServices/default" \
  --metric "FileCapacity" \
  --aggregation Average \
  --interval P1D \
  --output table
```


```text title="Expected output"
Name           Aggregation    ResourceId                                                                                                                                    Timestamp            Value
-------------  -------------  ------------------------------------------------------------------------------------------------------------------------------------------  -------------------  -----------
UsedCapacity   Average        /subscriptions/a7f3c2e1-9b4d-4f8a-b2c5-1e8d9f3a4b6c/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01  2024-01-15T14:00:00Z  847362560000
UsedCapacity   Average        /subscriptions/a7f3c2e1-9b4d-4f8a-b2c5-1e8d9f3a4b6c/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01  2024-01-15T13:00:00Z  846891024000

Name           Aggregation    ResourceId                                                                                                                                                      Timestamp            Value
-------------  -------------  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------  -------------------  -----------
BlobCapacity   Average        /subscriptions/a7f3c2e1-9b4d-4f8a-b2c5-1e8d9f3a4b6c/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01/blobServices/default  2024-01-15T00:00:00Z  847362560000

Name            Aggregation    ResourceId                                                                                                                                                        Timestamp            Value
--------------  -------------  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------  -------------------  -----------
FileCapacity    Average        /subscriptions/a7f3c2e1-9b4d-4f8a-b2c5-1e8d9f3a4b6c/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodfiles01/fileServices/default  2024-01-15T00:00:00Z  124578816000
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The resource '/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01' does not exist.` | Verify the subscription ID, resource group name, and storage account name are correct using `az storage account list`. |
    | `AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Insights/metrics/read' over scope '/subscriptions/<sub-id>/resourceGroups/rg-storage-prod'.` | Assign the "Monitoring Reader" role to your user or service principal on the storage account or resource group. |
    | `InvalidMetricName: The metric 'BlobCapacity' is not supported for this resource type.` | Confirm the metric name matches the resource type; use `az monitor metrics list-definitions --resource <resource-id>` to list available metrics. |
Key storage capacity metrics:

| Metric Name | Scope | Description |
|---|---|---|
| `UsedCapacity` | Storage Account | Total bytes used across all services |
| `BlobCapacity` | Blob service | Bytes used by blobs (by tier) |
| `FileCapacity` | File service | Bytes used by file shares |
| `TableCapacity` | Table service | Bytes used by table storage |
| `QueueCapacity` | Queue service | Bytes used by queues |
| `BlobCount` | Blob service | Number of blobs in the account |

## Capacity Alerts

```bash
# Create a metric alert for blob storage capacity (alert at 80% of 1 TiB)
az monitor metrics alert create \
  --name "blob-capacity-80pct" \
  --resource-group rg-storage-prod \
  --scopes "/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01/blobServices/default" \
  --condition "avg BlobCapacity > 858993459200" \
  --window-size 1h \
  --evaluation-frequency 1h \
  --action "/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/microsoft.insights/actionGroups/ag-storage-ops" \
  --description "Blob storage exceeds 80% of 1 TiB"

# List existing metric alerts for storage
az monitor metrics alert list \
  --resource-group rg-storage-prod \
  --output table

# Disable an alert
az monitor metrics alert update \
  --name "blob-capacity-80pct" \
  --resource-group rg-storage-prod \
  --enabled false
```


```text title="Expected output"
{
  "actions": [
    {
      "actionGroupId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/microsoft.insights/actionGroups/ag-storage-ops",
      "webHookProperties": {}
    }
  ],
  "criteria": {
    "allOf": [
      {
        "metricName": "BlobCapacity",
        "metricNamespace": "Microsoft.Storage/storageAccounts/blobServices",
        "operator": "GreaterThan",
        "threshold": 858993459200,
        "timeAggregation": "Average"
      }
    ],
    "odata.type": "Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria"
  },
  "description": "Blob storage exceeds 80% of 1 TiB",
  "enabled": true,
  "evaluationFrequency": "PT1H",
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/microsoft.insights/metricalerts/blob-capacity-80pct",
  "name": "blob-capacity-80pct",
  "resourceGroup": "rg-storage-prod",
  "windowSize": "PT1H"
}

Name                      ResourceGroup         Enabled    Severity
------------------------  --------------------  ---------  ----------
blob-capacity-80pct       rg-storage-prod       True       3
storage-iops-threshold    rg-storage-prod       True       2
egress-bandwidth-limit    rg-storage-prod       False      3

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The resource '/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01/blobServices/default' could not be found.` | Verify the storage account name and subscription ID are correct, and that the blobServices/default resource exists. |
    | `InvalidActionGroup: The action group '/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/microsoft.insights/actionGroups/ag-storage-ops' does not exist or is in a different resource group.` | Ensure the action group exists in the same resource group and subscription as the alert. |
## Container-Level Capacity

```bash
# List containers with their approximate sizes
az storage container list \
  --account-name stprodblobs01 \
  --output table

# Get container blob count and total size using az CLI stats
az storage blob list \
  --account-name stprodblobs01 \
  --container-name backups \
  --query "length(@)" \
  --output tsv

# Calculate total size of all blobs in a container
az storage blob list \
  --account-name stprodblobs01 \
  --container-name backups \
  --query "sum([].properties.contentLength)" \
  --output tsv

# List blobs sorted by size (largest first)
az storage blob list \
  --account-name stprodblobs01 \
  --container-name backups \
  --query "sort_by(@, &properties.contentLength) | reverse(@)[].{name:name, size:properties.contentLength}" \
  --output table
```


```text title="Expected output"
Name                Lease Status    Last Modified
------------------- --------------- ---------------------------------
backups             unlocked        2024-01-15T09:42:33+00:00
logs                unlocked        2024-01-15T08:21:19+00:00
archives            unlocked        2024-01-14T16:55:02+00:00
temp-uploads        unlocked        2024-01-15T11:03:47+00:00
2847

1073741824000

Name                                          Size
------------------------------------------------- ----------------
daily-backup-2024-01-15-prod.vhd              536870912000
weekly-backup-2024-01-08-prod.vhd             268435456000
monthly-backup-2024-01-01-prod.vhd            214748364800
incremental-backup-2024-01-15-app.vhd         107374182400
temp-restore-cache-20240115.tmp               53687091200
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The specified account does not exist.` | Verify the storage account name is correct and exists in the current subscription with `az storage account list`. |
    | `AuthorizationPermissionMismatch: This request is not authorized to perform this operation.` | Ensure your Azure CLI session has Storage Blob Data Reader or higher role assigned via `az role assignment list --assignee $(az account show --query user.name -o tsv)`. |
## Forecasting and Trend Analysis

```bash
# Pull 30 days of daily capacity data for trend analysis
az monitor metrics list \
  --resource "/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01/blobServices/default" \
  --metric "BlobCapacity" \
  --aggregation Average \
  --interval P1D \
  --start-time "$(date -u -d '30 days ago' '+%Y-%m-%dT%H:%MZ')" \
  --end-time "$(date -u '+%Y-%m-%dT%H:%MZ')" \
  --output json > capacity-trend.json

# Convert bytes to GiB in output for readability
cat capacity-trend.json | python3 -c "
import json,sys
data = json.load(sys.stdin)
for ts in data['value'][0]['timeseries'][0]['data']:
    gib = (ts.get('average') or 0) / 1073741824
    print(f\"{ts['timeStamp']}: {gib:.2f} GiB\")
"
```


```text title="Expected output"
2024-11-14T18:45:00Z: 487.34 GiB
2024-11-15T18:45:00Z: 489.12 GiB
2024-11-16T18:45:00Z: 491.87 GiB
2024-11-17T18:45:00Z: 495.23 GiB
2024-11-18T18:45:00Z: 498.56 GiB
2024-11-19T18:45:00Z: 502.14 GiB
2024-11-20T18:45:00Z: 505.78 GiB
2024-11-21T18:45:00Z: 509.45 GiB
2024-11-22T18:45:00Z: 513.92 GiB
2024-11-23T18:45:00Z: 518.67 GiB
...
2024-12-14T18:45:00Z: 612.34 GiB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The resource '/subscriptions/<sub-id>/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01/blobServices/default' could not be found.` | Verify the subscription ID, resource group name, and storage account name are correct and exist in your Azure tenant. |
    | `KeyError: 'timeseries'` | Ensure the metric "BlobCapacity" returned data for the specified time range; if the storage account is new, metrics may not be available for the full 30-day window. |
## Storage Account Limits Reference

| Resource | Limit | Notes |
|---|---|---|
| Max storage account capacity | 5 PiB | Default; can request increase |
| Max ingress bandwidth (LRS) | 10 Gbps | Region-dependent |
| Max egress bandwidth (LRS) | 50 Gbps | Region-dependent |
| Max IOPS (block blobs) | 20,000 per account | — |
| Max containers per account | Unlimited | — |
| Max blob size (block blob) | 190.7 TiB | 50,000 blocks x 4 GiB |
