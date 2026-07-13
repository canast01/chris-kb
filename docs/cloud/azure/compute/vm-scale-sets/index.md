---
tags:
  - azure
description: "Azure Virtual Machine Scale Sets (VMSS) allow you to deploy and manage a group of identical, load-balanced VMs that can automatically scale in or out..."
---
# VM Scale Sets

<div class="kb-summary">
Azure Virtual Machine Scale Sets (VMSS) allow you to deploy and manage a group of identical, load-balanced VMs that can automatically scale in or out based on demand or a defined schedule.

*Applies to: Azure*
</div>

---

## VMSS Autoscale Flow

```d2
direction: right

monitor: "Azure Monitor\nCPU · custom metrics" {shape: rectangle}
autoscaleEngine: "Autoscale Engine\nevaluates rules every 1 min" {shape: rectangle}
scaleOut: "scaleOut" {shape: rectangle}
scaleIn: "scaleIn" {shape: rectangle}
addInstances: "Add Instances\noverprovision + remove excess" {shape: rectangle}
steady: "Steady State\ncurrent capacity maintained" {shape: rectangle}
removeInstances: "Remove Instances\ncooldown period applies" {shape: rectangle}

monitor -> autoscaleEngine
autoscaleEngine -> scaleOut
autoscaleEngine -> scaleIn
addInstances -> steady
removeInstances -> steady
```

## Core Concepts

| Concept | Description |
|---|---|
| Orchestration Mode | Uniform (identical VMs) or Flexible (mix of VMs, recommended for new deployments) |
| Upgrade Policy | Automatic, Rolling, or Manual — controls how instance updates are applied |
| Overprovision | Azure creates extra VMs temporarily to speed up scale-out, then deletes excess |
| Capacity | Current number of running instances |
| Autoscale | Rules-based or scheduled scaling |

---

## Creating a Scale Set

```bash
# Create a basic Linux scale set (Flexible orchestration, zone-spanning)
az vmss create \
  --resource-group <rg> \
  --name <vmss-name> \
  --image Ubuntu2204 \
  --vm-sku Standard_D2s_v3 \
  --instance-count 2 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --orchestration-mode Flexible \
  --zones 1 2 3

# Create a Windows scale set with a load balancer
az vmss create \
  --resource-group <rg> \
  --name <vmss-name> \
  --image Win2022Datacenter \
  --vm-sku Standard_D2s_v3 \
  --instance-count 2 \
  --admin-username azureuser \
  --admin-password <password> \
  --orchestration-mode Uniform \
  --load-balancer <lb-name> \
  --backend-pool-name <pool-name>

# List all scale sets in a resource group
az vmss list \
  --resource-group <rg> \
  --output table
```


```text title="Expected output"
{
  "fqdns": "",
  "id": "/subscriptions/12a34b5c-6789-0def-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/linux-vmss-01",
  "identity": null,
  "location": "eastus",
  "name": "linux-vmss-01",
  "resourceGroup": "prod-rg",
  "zones": [
    "1",
    "2",
    "3"
  ]
}
{
  "fqdns": "win-vmss-01.eastus.cloudapp.azure.com",
  "id": "/subscriptions/12a34b5c-6789-0def-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/win-vmss-01",
  "location": "eastus",
  "name": "win-vmss-01",
  "resourceGroup": "prod-rg"
}
Name           ResourceGroup    Location    Zones    Orchestration Mode    Capacity
-------------  ---------------  ----------  -------  --------------------  ----------
linux-vmss-01  prod-rg          eastus      1,2,3    Flexible              2
win-vmss-01    prod-rg          eastus               Uniform                2
```

!!! warning "Common errors"
    **`The image 'Ubuntu2204' could not be found.`** — Use a valid image URN like `UbuntuLTS` or `Ubuntu2204` with the full publisher format, or run `az vm image list --output table` to verify available images.
    **`The resource 'Microsoft.Network/loadBalancers/<lb-name>' under resource group '<rg>' was not found.`** — Create the load balancer first with `az network lb create` or verify the `--load-balancer` parameter references an existing resource in the same resource group.
    **`The password does not meet complexity requirements.`** — Ensure the Windows admin password is at least 12 characters and includes uppercase, lowercase, numbers, and special characters.
---

## Scaling Operations

```bash
# Manually scale out to 5 instances
az vmss scale \
  --resource-group <rg> \
  --name <vmss-name> \
  --new-capacity 5

# Scale in to 2 instances
az vmss scale \
  --resource-group <rg> \
  --name <vmss-name> \
  --new-capacity 2

# Show current capacity
az vmss show \
  --resource-group <rg> \
  --name <vmss-name> \
  --query "sku.{Capacity:capacity, Name:name, Tier:tier}" \
  --output table

# List all instances in the scale set
az vmss list-instances \
  --resource-group <rg> \
  --name <vmss-name> \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/web-vmss",
  "name": "web-vmss",
  "provisioningState": "Succeeded"
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/web-vmss",
  "name": "web-vmss",
  "provisioningState": "Succeeded"
}
Capacity    Name                Tier
----------  ------------------  --------
2           Standard_D2s_v3     Standard

InstanceId    ProvisioningState    PowerState      VmId
------------  -------------------  ---------------  ------------------------------------
0             Succeeded            VM running       a1b2c3d4-e5f6-7890-abcd-ef1234567890
1             Succeeded            VM running       b2c3d4e5-f6a7-8901-bcde-f12345678901
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name with `az group list` and ensure it exists in your subscription.
    **`ResourceNotFound`** — Confirm the VMSS name is correct by running `az vmss list --resource-group <rg>` to list all scale sets in the resource group.
---

## Autoscale Rules

```bash
# Enable autoscale with min 2, max 10, default 2 instances
az monitor autoscale create \
  --resource-group <rg> \
  --resource <vmss-resource-id> \
  --resource-type Microsoft.Compute/virtualMachineScaleSets \
  --name <autoscale-name> \
  --min-count 2 \
  --max-count 10 \
  --count 2

# Add a scale-out rule (CPU > 70% for 5 minutes — add 2 instances)
az monitor autoscale rule create \
  --resource-group <rg> \
  --autoscale-name <autoscale-name> \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 2

# Add a scale-in rule (CPU < 30% for 10 minutes — remove 1 instance)
az monitor autoscale rule create \
  --resource-group <rg> \
  --autoscale-name <autoscale-name> \
  --condition "Percentage CPU < 30 avg 10m" \
  --scale in 1

# List autoscale settings
az monitor autoscale list \
  --resource-group <rg> \
  --output table
```


```text title="Expected output"
{
  "enabled": true,
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/microsoft.insights/autoscalesettings/vmss-autoscale-prod",
  "location": "eastus",
  "name": "vmss-autoscale-prod",
  "notificationEnabled": false,
  "profiles": [
    {
      "capacity": {
        "default": "2",
        "maximum": "10",
        "minimum": "2"
      },
      "name": "Auto scale based on CPU",
      "rules": []
    }
  ],
  "resourceGroup": "prod-rg",
  "targetResourceUri": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/vmss-prod"
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/microsoft.insights/autoscalesettings/vmss-autoscale-prod/profiles/0/rules/0",
  "metricName": "Percentage CPU",
  "metricResourceId": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/vmss-prod",
  "operator": "GreaterThan",
  "scaleAction": {
    "cooldown": "PT5M",
    "direction": "Increase",
    "type": "ChangeCount",
    "value": "2"
  },
  "statistic": "Average",
  "threshold": 70.0,
  "timeAggregation": "Average",
  "timeWindow": "PT5M"
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/microsoft.insights/autoscalesettings/vmss-autoscale-prod/profiles/0/rules/1",
  "metricName": "Percentage CPU",
  "operator": "LessThan",
  "scaleAction": {
    "cooldown": "PT10M",
    "direction": "Decrease",
    "type": "ChangeCount",
    "value": "1"
  },
  "threshold": 30.0,
  "timeWindow": "PT10M"
}
Name                      ResourceGroup    Enabled    MinCount    MaxCount    DefaultCount
------------------------  ---------------  ---------  ----------  ----------  ---------------
vmss-autoscale-prod       prod-rg          True       2           10          2
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachineScaleSets/<vmss-resource-id>' under resource group '<rg>' was not found.`** — Verify the VMSS resource ID is correct and exists in the specified resource group using `az vmss
---

## Upgrade Policies

| Policy | Behaviour |
|---|---|
| Automatic | Azure upgrades all instances immediately when the model changes |
| Rolling | Instances are updated in batches, maintains availability |
| Manual | Operator manually triggers upgrades per instance |

```bash
# Change upgrade policy to Rolling
az vmss update \
  --resource-group <rg> \
  --name <vmss-name> \
  --set upgradePolicy.mode=Rolling \
  --set upgradePolicy.rollingUpgradePolicy.maxBatchInstancePercent=20 \
  --set upgradePolicy.rollingUpgradePolicy.maxUnhealthyInstancePercent=20

# Manually upgrade specific instances
az vmss update-instances \
  --resource-group <rg> \
  --name <vmss-name> \
  --instance-ids 0 1 2
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/web-vmss-01",
  "name": "web-vmss-01",
  "type": "Microsoft.Compute/virtualMachineScaleSets",
  "location": "eastus",
  "upgradePolicy": {
    "mode": "Rolling",
    "rollingUpgradePolicy": {
      "maxBatchInstancePercent": 20,
      "maxUnhealthyInstancePercent": 20,
      "pauseTimeBetweenBatches": "PT0S"
    }
  },
  "provisioningState": "Succeeded"
}
{
  "value": [
    {
      "instanceId": "0",
      "latestModelApplied": true
    },
    {
      "instanceId": "1",
      "latestModelApplied": true
    },
    {
      "instanceId": "2",
      "latestModelApplied": true
    }
  ]
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound: Resource group '<rg>' could not be found.`** — Verify the resource group name matches exactly and exists in the current subscription using `az group list`.
    **`ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachineScaleSets/<vmss-name>' under resource group '<rg>' was not found.`** — Confirm the VMSS name is correct and exists in the specified resource group with `az vmss list --resource-group <rg>`.
    **`InvalidParameter: Instance IDs '0 1 2' are invalid. Valid instance IDs must be integers between 0 and <max-capacity>.`** — Ensure instance IDs do not exceed the current capacity of the scale set; check with `az vmss show --resource-group <rg> --name <vmss-name> --query 'sku.capacity'`.
---

## Health Probes and Automatic Repairs

```bash
# Enable application health extension for automatic repair
az vmss extension set \
  --resource-group <rg> \
  --vmss-name <vmss-name> \
  --name ApplicationHealthLinux \
  --publisher Microsoft.ManagedServices \
  --version 1.0 \
  --settings '{"protocol": "http", "port": 80, "requestPath": "/health"}'

# Enable automatic repairs on the scale set
az vmss update \
  --resource-group <rg> \
  --name <vmss-name> \
  --enable-automatic-repairs true \
  --automatic-repairs-grace-period PT30M
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/web-vmss/extensions/ApplicationHealthLinux",
  "name": "ApplicationHealthLinux",
  "provisioningState": "Succeeded",
  "publisher": "Microsoft.ManagedServices",
  "type": "Microsoft.Compute/virtualMachineScaleSets/extensions",
  "typeHandlerVersion": "1.0",
  "autoUpgradeMinorVersion": true
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachineScaleSets/web-vmss",
  "name": "web-vmss",
  "automaticRepairsPolicy": {
    "enabled": true,
    "gracePeriod": "PT30M"
  },
  "provisioningState": "Succeeded",
  "type": "Microsoft.Compute/virtualMachineScaleSets"
}
```

!!! warning "Common errors"
    **`Extension with name ApplicationHealthLinux already exists`** — Remove the existing extension with `az vmss extension delete` before re-running the set command.
    **`The resource group '<rg>' could not be found`** — Verify the resource group name with `az group list` and ensure you are using the correct subscription.
    **`Invalid requestPath: must start with /`** — Ensure the health check path in the settings JSON begins with a forward slash (e.g., `"/health"` not `"health"`).
---

## Instance Operations

```bash
# Restart a specific instance
az vmss restart \
  --resource-group <rg> \
  --name <vmss-name> \
  --instance-ids 0

# Deallocate a specific instance
az vmss deallocate \
  --resource-group <rg> \
  --name <vmss-name> \
  --instance-ids 1

# Delete a specific instance
az vmss delete-instances \
  --resource-group <rg> \
  --name <vmss-name> \
  --instance-ids 2

# Run a command on all instances in the set
az vmss run-command invoke \
  --resource-group <rg> \
  --name <vmss-name> \
  --command-id RunShellScript \
  --instance-id 0 \
  --scripts "systemctl status nginx"
```


```text title="Expected output"
{
  "value": [
    {
      "code": "ProvisioningState/succeeded",
      "displayStatus": "Provisioning succeeded",
      "level": "Info",
      "message": "Instance 0 restarted successfully",
      "time": "2024-01-15T10:32:47.123456Z"
    }
  ]
}
{
  "value": [
    {
      "code": "ProvisioningState/succeeded",
      "displayStatus": "Provisioning succeeded",
      "level": "Info",
      "message": "Instance 1 deallocated successfully",
      "time": "2024-01-15T10:33:12.456789Z"
    }
  ]
}
{
  "value": [
    {
      "code": "ProvisioningState/succeeded",
      "displayStatus": "Provisioning succeeded",
      "level": "Info",
      "message": "Instance 2 deleted successfully",
      "time": "2024-01-15T10:33:58.789012Z"
    }
  ]
}
{
  "value": [
    {
      "code": "ComponentStatus/succeeded",
      "displayStatus": "Execution succeeded",
      "level": "Info",
      "message": "● nginx.service - The NGINX HTTP and reverse proxy server\n   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)\n   Active: active (running) since Mon 2024-01-15 10:25:33 UTC; 8min ago",
      "time": "2024-01-15T10:34:22.012345Z"
    }
  ]
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name with `az group list` and ensure it exists in your subscription.
    **`ResourceNotFound`** — Confirm the VMSS name is correct using `az vmss list --resource-group <rg>` and check the spelling.
    **`InvalidInstanceId`** — Ensure the instance ID exists in the scale set; retrieve valid IDs with `az vmss list-instances --resource-group <rg> --name <vmss-name>`.
---

## Scale Set Reference Table

| Setting | Uniform Mode | Flexible Mode |
|---|---|---|
| Identical VM config | Required | Optional |
| Max instances | 1000 (with placement groups) | 1000 |
| Mix VM sizes | No | Yes |
| Standalone VM support | No | Yes |
| Recommended for new workloads | No | Yes |
