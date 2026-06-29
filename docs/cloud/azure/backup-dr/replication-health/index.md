---
tags:
  - azure
---
# Replication Health

<div class="kb-summary">
Monitoring ASR replication health is critical for validating that DR protection is active and within acceptable RPO thresholds. Health states reflect the ongoing synchronisation between source and target regions.

*Applies to: Azure*
</div>

---

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Replication Health \u2014 Thresholds",
    "fontSize": 13,
    "fontWeight": "normal"
  },
  "width": 480,
  "height": {
    "step": 26
  },
  "data": {
    "values": [
      {
        "metric": "ResyncProgressPercentage",
        "zone": "Safe",
        "val": 0
      },
      {
        "metric": "ResyncProgressPercentage",
        "zone": "Alert",
        "val": 100
      }
    ]
  },
  "mark": {
    "type": "bar",
    "cornerRadiusEnd": 3
  },
  "encoding": {
    "y": {
      "field": "metric",
      "type": "nominal",
      "axis": {
        "title": null,
        "labelLimit": 200
      },
      "sort": null
    },
    "x": {
      "field": "val",
      "type": "quantitative",
      "stack": "normalize",
      "axis": {
        "title": "Threshold boundary",
        "format": ".0%"
      }
    },
    "color": {
      "field": "zone",
      "type": "nominal",
      "scale": {
        "domain": [
          "Safe",
          "Alert"
        ],
        "range": [
          "#15803d",
          "#dc2626"
        ]
      },
      "legend": {
        "title": "Zone"
      }
    },
    "order": {
      "field": "zone",
      "sort": [
        "Safe",
        "Alert"
      ]
    },
    "tooltip": [
      {
        "field": "metric",
        "type": "nominal",
        "title": "Metric"
      },
      {
        "field": "zone",
        "type": "nominal",
        "title": "Zone"
      },
      {
        "field": "val",
        "type": "quantitative",
        "title": "Segment %",
        "format": ".0f"
      }
    ]
  }
}
```

## Replication Health Monitoring Flow

```d2
direction: right

asr: "ASR Replicated Item" {shape: rectangle}
healthCheck: "Replication Health Check\nRPO · sync lag · cache utilisation" {shape: rectangle}
normal: "Normal\nRPO within threshold" {shape: rectangle}
warning: "Warning\nRPO breach · minor issue" {shape: rectangle}
investigateWarning: "Investigate\ncheck cache storage · network" {shape: rectangle}
critical: "Critical\nReplication stopped" {shape: rectangle}
investigateCritical: "Immediate action\ncheck agent · connectivity · vault" {shape: rectangle}
notConfigured: "None\nNo protection" {shape: rectangle}

asr -> healthCheck
healthCheck -> normal
healthCheck -> warning
warning -> investigateWarning
healthCheck -> critical
critical -> investigateCritical
healthCheck -> notConfigured
```

## Health States and Meanings

| State | Meaning | Action Required |
|---|---|---|
| Normal | Replication is healthy, RPO within threshold | None |
| Warning | RPO breached or minor issue detected | Investigate RPO, check cache storage |
| Critical | Replication stopped or severely degraded | Immediate remediation needed |
| None | Replication not configured | Enable protection |

---

## Checking Replication Health via REST

```bash
# List all replicated items with health and RPO
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems?api-version=2022-10-01" \
  --query "value[].{Name:name, Health:properties.replicationHealth, RPO:properties.rpoInSeconds, ActiveLocation:properties.activeLocation}" \
  --output table

# Show detailed health for a single item
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems/<item-name>?api-version=2022-10-01" \
  --query "properties.{Health:replicationHealth, RPO:rpoInSeconds, TestFailoverState:testFailoverState, LastSync:lastSuccessfulTestFailoverTime}" \
  --output json
```


```text title="Expected output"
Name                          Health    RPO      ActiveLocation
------------------------------  --------  -------  ----------------
prod-web-vm-01                Normal    300      primaryLocation
prod-db-vm-02                 Warning   1847     primaryLocation
prod-app-vm-03                Normal    285      primaryLocation
dr-cache-vm-04                Critical  5923     secondaryLocation
prod-web-vm-05                Normal    312      primaryLocation

{
  "Health": "Normal",
  "RPO": 298,
  "TestFailoverState": "None",
  "LastSync": "2024-01-15T14:32:47.123Z"
}
```

!!! warning "Common errors"
    **`The subscription '<sub-id>' could not be found.`** — Replace `<sub-id>` with your actual subscription ID from `az account show --query id`.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>' under resource group '<dr-rg>' was not found.`** — Verify the vault name and resource group exist in the correct subscription using `az recovery-services vault list -g <dr-rg>`.
    **`Authorization failed for request. Caller is not authorized to perform action 'Microsoft.RecoveryServices/vaults/replicationProtectedItems/read' on resource.`** — Ensure your account has Reader or Site Recovery Operator role on the Recovery Services vault using `az role assignment list --scope /subscriptions/<sub-id>/resourceGroups/<dr-rg>`.
---

## RPO Warnings

RPO (Recovery Point Objective) warnings appear when the time since the last synchronised recovery point exceeds the policy threshold.

```bash
# Identify items with RPO warnings (RPO > 300 seconds = 5 minutes)
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems?api-version=2022-10-01" \
  --query "value[?properties.rpoInSeconds > \`300\`].{Name:name, RPO:properties.rpoInSeconds, Health:properties.replicationHealth}" \
  --output table
```


```text title="Expected output"
Name                                    RPO    Health
--------------------------------------  -----  ----------------
vm-prod-db-01                           487    Warning
vm-prod-app-tier-02                     612    Warning
vm-staging-web-01                       305    Degraded
vm-prod-cache-redis                     1203   Critical
vm-dr-failover-test-03                  401    Warning
```

!!! warning "Common errors"
    **`ERROR: The subscription '<sub-id>' could not be found.`** — Replace `<sub-id>` with your actual subscription ID from `az account show --query id -o tsv`.
    
    **`ERROR: The resource group '<dr-rg>' could not be found in the subscription.`** — Verify the resource group name with `az group list --query "[].name" -o tsv` and ensure it exists in the correct subscription.
    
    **`ERROR: The vault '<vault-name>' could not be found in the specified resource group.`** — Confirm the Recovery Services vault name using `az backup vault list --resource-group <dr-rg> --query "[].name" -o tsv`.
Common RPO warning causes:

| Cause | Symptom | Resolution |
|---|---|---|
| Cache storage account throttling | RPO > 30 min, high churn VMs | Increase cache storage account tier |
| Network bandwidth saturation | Slow delta sync | Check ExpressRoute / VPN throughput |
| VM under heavy write load | Rapid RPO growth | Reduce write churn, review disk types |
| Mobility service outdated | Health = Warning | Update the Mobility service extension |
| Process server overloaded | Multiple VMs degraded | Scale out process servers |

---

## Triggering a Resync

If replication is stuck or health is critical, a resync forces a full re-synchronisation from the source.

```bash
# Trigger resync for a protected item
az rest --method POST \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationFabrics/<fabric>/replicationProtectionContainers/<container>/replicationProtectedItems/<item-name>/resync?api-version=2022-10-01" \
  --body '{}'

# Monitor resync job
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationJobs?api-version=2022-10-01" \
  --query "value[?properties.jobType=='Resync'].{Name:name, State:properties.state, Progress:properties.stateDescription}" \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dr-rg-prod/providers/Microsoft.RecoveryServices/vaults/vault-dr-01/replicationJobs/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "name": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "type": "Microsoft.RecoveryServices/vaults/replicationJobs",
  "properties": {
    "jobType": "Resync",
    "state": "InProgress",
    "stateDescription": "Resync in progress"
  }
}

Name                                  State         Progress
----                                  -----         --------
a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d  InProgress    Resync in progress
b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e  Succeeded     Resync completed
```

!!! warning "Common errors"
    **`The URI is invalid.`** — Replace all placeholder values (`<sub-id>`, `<dr-rg>`, `<vault-name>`, `<fabric>`, `<container>`, `<item-name>`) with actual resource names from your Azure environment.
    **`AuthorizationFailed: The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/replicationJobs/read' over scope...`** — Ensure your Azure account has the "Site Recovery Contributor" or "Backup Operator" role assigned on the Recovery Services vault.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>/replicationProtectedItems/<item-name>' under resource group '<dr-rg>' was not found.`** — Verify the protected item name and container name are correct by running `az recovery-services-backup item list --vault-name <vault-name> --resource-group <dr-rg>`.
---

## Monitoring via Azure Monitor Alerts

```bash
# Create an alert for replication health degradation
az monitor metrics alert create \
  --name asr-replication-health-alert \
  --resource-group <rg> \
  --scopes <vault-resource-id> \
  --condition "avg ReplicationHealthErrors > 0" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --description "ASR replication health degraded"

# List all metric alerts for the vault
az monitor metrics alert list \
  --resource-group <rg> \
  --output table
```


```text title="Expected output"
{
  "actions": [],
  "creationTime": "2024-01-15T09:32:47.123456+00:00",
  "description": "ASR replication health degraded",
  "enabled": true,
  "evaluationFrequency": "PT1M",
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Insights/metricAlerts/asr-replication-health-alert",
  "location": "global",
  "name": "asr-replication-health-alert",
  "resourceGroup": "prod-rg",
  "severity": 2,
  "windowSize": "PT5M"
}
Name                                    ResourceGroup    Enabled    Severity
--------------------------------------  ---------------  ---------  ----------
asr-replication-health-alert            prod-rg          True       2
vm-cpu-utilization-alert                prod-rg          True       1
vault-backup-failure-alert               prod-rg          True       3
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource '/subscriptions/.../providers/Microsoft.RecoveryServices/vaults/<vault-resource-id>' could not be found.`** — Verify the vault resource ID is correct and exists in the specified resource group using `az recovery-services vault list --resource-group <rg>`.
    **`InvalidMetricName: The metric 'ReplicationHealthErrors' is not valid for this resource type.`** — Replace with the correct metric name `ReplicationHealthStatus` or `ReplicationLatency` by checking available metrics with `az monitor metrics list-definitions --resource <vault-resource-id>`.
---

## Replication Jobs Monitoring

```bash
# List replication jobs in the past 24 hours
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationJobs?api-version=2022-10-01" \
  --query "value[].{Name:name, Type:properties.jobType, State:properties.state, StartTime:properties.startTime, EndTime:properties.endTime}" \
  --output table

# List failed replication jobs only
az rest --method GET \
  --uri "https://management.azure.com/subscriptions/<sub-id>/resourceGroups/<dr-rg>/providers/Microsoft.RecoveryServices/vaults/<vault-name>/replicationJobs?api-version=2022-10-01" \
  --query "value[?properties.state=='Failed'].{Name:name, Type:properties.jobType, Error:properties.errors[0].details[0].message}" \
  --output table
```


```text title="Expected output"
Name                                          Type                State      StartTime                 EndTime
--------------------------------------------  ------------------  ---------  ------------------------  ------------------------
dr-vm-sync-20250115-001                       Replication         Completed  2025-01-15T08:23:45.123Z  2025-01-15T08:45:12.456Z
dr-vm-sync-20250115-002                       Replication         Completed  2025-01-15T09:10:33.789Z  2025-01-15T09:32:01.012Z
dr-failover-test-20250114-001                 TestFailover        Completed  2025-01-14T22:15:22.345Z  2025-01-14T22:58:44.678Z
dr-vm-sync-20250115-003                       Replication         InProgress 2025-01-15T10:05:17.234Z  None
dr-resync-20250114-001                        Resynchronize       Failed     2025-01-14T19:42:11.567Z  2025-01-14T20:15:33.890Z

Name                                          Type                Error
--------------------------------------------  ------------------  -----------------------------------------------
dr-resync-20250114-001                        Resynchronize       Target resource group not found in subscription
```

!!! warning "Common errors"
    **`AuthorizationError: The client '<client-id>' does not have authorization to perform action 'Microsoft.RecoveryServices/vaults/read'`** — Ensure your Azure CLI account has the Reader or Contributor role on the Recovery Services vault resource.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>' under resource group '<dr-rg>' was not found`** — Verify the subscription ID, resource group name, and vault name are correct and exist in your Azure subscription.
    **`InvalidApiVersion: The api-version '2022-10-01' is not supported for this resource type`** — Update the api-version parameter to a currently supported version by running `az provider show --namespace Microsoft.RecoveryServices --query "resourceTypes[?resourceType=='vaults/replicationJobs'].apiVersions"`.
---

## Replication Health Dashboard Metrics

Key metrics to surface in an Azure Monitor workbook or dashboard:

| Metric | Alert Threshold | Dashboard Widget |
|---|---|---|
| `RPOInSeconds` | > 300 | Line chart, 1h window |
| `ReplicationHealthErrors` | > 0 | Alert count tile |
| `ReplicationDataUploadRate` | < expected baseline | Area chart |
| `ResyncProgressPercentage` | Stuck at < 100% | Progress tile |
