---
tags:
  - azure
description: "Azure Update Manager (the successor to Azure Automation Update Management) provides centralised OS patch management for Azure VMs, Arc-connected servers..."
---
# Patching

<div class="kb-summary">
Azure Update Manager (the successor to Azure Automation Update Management) provides centralised OS patch management for Azure VMs, Arc-connected servers, and on-premises machines. This page covers assessments, maintenance windows, and compliance reporting.

*Applies to: Azure*
</div>

---

## Azure Update Manager Flow

```d2
direction: right

assess: "Patch Assessment\ncheck available updates" {shape: rectangle}
maintenanceConfig: "Maintenance Configuration\nschedule · reboot policy · scope" {shape: rectangle}
patchOrch: "Patch Orchestration\nAzure-managed or customer-managed" {shape: rectangle}
patchInstall: "Patch Installation\nOS-native package manager" {shape: rectangle}
reboot: "reboot" {shape: rectangle}
rebootVM: "Reboot VM\nwithin maintenance window" {shape: rectangle}
compliance: "Compliance Report\nAzure Update Manager dashboard" {shape: rectangle}

assess -> maintenanceConfig
maintenanceConfig -> patchOrch
patchOrch -> patchInstall
patchInstall -> reboot
rebootVM -> compliance
```

## Azure Update Manager Overview

| Feature | Description |
|---|---|
| Patch Assessment | On-demand or periodic scan to identify available OS updates |
| Patch Orchestration | Azure-managed or customer-managed scheduling |
| Maintenance Configuration | Defines patching schedule, reboot policy, and scope |
| Compliance View | Aggregated patch status across all machines |
| Hotpatch | In-place kernel patching without reboot (Windows Server Datacenter Azure Edition) |

---

## Checking Update Status

```bash
# Check patch assessment for a single VM
az maintenance update list \
  --resource-group <rg> \
  --resource-name <vm-name> \
  --resource-type virtualMachines \
  --provider-name Microsoft.Compute \
  --output table

# Trigger an on-demand patch assessment
az maintenance assess \
  --resource-group <rg> \
  --resource-name <vm-name> \
  --resource-type virtualMachines \
  --provider-name Microsoft.Compute

# List all VMs and their patch assessment status
az vm list \
  --resource-group <rg> \
  --query "[].{Name:name, OSType:storageProfile.osDisk.osType, PatchMode:osProfile.linuxConfiguration.patchSettings.patchMode}" \
  --output table
```


```text title="Expected output"
Name                          OSType    PatchMode
------------------------------  --------  -----------
prod-web-01                    Linux     AutomaticByPlatform
prod-web-02                    Linux     ImageDefault
prod-db-01                     Linux     Manual
staging-app-vm                 Windows   AutomaticByOS
dev-test-01                    Linux     AutomaticByPlatform

AssessmentState    : Success
LastAssessmentTime : 2024-01-15T09:42:31.2847392Z
AvailablePatches   : 18
CriticalPatches    : 3
SecurityPatches    : 12
OtherPatches       : 3
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.` | Verify the VM name and resource group name are correct with `az vm list --resource-group <rg>`. |
    | `AuthorizationFailed : The client '<user>' with object id '<id>' does not have authorization to perform action 'Microsoft.Maintenance/updates/read' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name>'.` | Ensure your Azure account has the "Maintenance Reader" or "Contributor" role assigned to the resource group. |
---

## Patch Modes

```bash
# Set patch mode to AutomaticByPlatform (Azure-managed patching)
az vm update \
  --resource-group <rg> \
  --name <vm-name> \
  --set osProfile.linuxConfiguration.patchSettings.patchMode=AutomaticByPlatform

# Set patch mode to ImageDefault (use image's built-in update mechanism)
az vm update \
  --resource-group <rg> \
  --name <vm-name> \
  --set osProfile.linuxConfiguration.patchSettings.patchMode=ImageDefault

# Set Windows VM to AutomaticByPlatform
az vm update \
  --resource-group <rg> \
  --name <win-vm-name> \
  --set osProfile.windowsConfiguration.patchSettings.patchMode=AutomaticByPlatform
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/linux-vm-01",
  "location": "eastus",
  "name": "linux-vm-01",
  "osProfile": {
    "linuxConfiguration": {
      "patchSettings": {
        "patchMode": "AutomaticByPlatform"
      }
    }
  },
  "provisioningState": "Succeeded",
  "vmId": "f7e8d9c0-b1a2-3c4d-5e6f-7g8h9i0j1k2l"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/linux-vm-01",
  "location": "eastus",
  "name": "linux-vm-01",
  "osProfile": {
    "linuxConfiguration": {
      "patchSettings": {
        "patchMode": "ImageDefault"
      }
    }
  },
  "provisioningState": "Succeeded",
  "vmId": "f7e8d9c0-b1a2-3c4d-5e6f-7g8h9i0j1k2l"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/win-vm-01",
  "location": "eastus",
  "name": "win-vm-01",
  "osProfile": {
    "windowsConfiguration": {
      "patchSettings": {
        "patchMode": "AutomaticByPlatform"
      }
    }
  },
  "provisioningState": "Succeeded",
  "vmId": "a2b3c4d5-e6f7-4g8h-9i0j-1k2l3m4n5o6p"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.` | Verify the resource group name and VM name are correct using `az vm list --resource-group <rg>`. |
    | `InvalidApiVersionParameter : The api-version '2021-03-01' does not support 'patchSettings' for this resource type.` | Update the Azure CLI to the latest version with `az upgrade` to support patch settings on your VM SKU. |
| Patch Mode | Who Controls Schedule | Reboot |
|---|---|---|
| `AutomaticByOS` | Windows Update (Windows only) | Automatic |
| `AutomaticByPlatform` | Azure Update Manager | Controlled |
| `ImageDefault` | Image's own mechanism | As configured |
| `Manual` | Operator | Manual |

---

## Maintenance Configurations

```bash
# Create a maintenance configuration (patching schedule)
az maintenance configuration create \
  --resource-group <rg> \
  --name <config-name> \
  --maintenance-scope InGuestPatch \
  --location eastus \
  --start-date-time "2026-05-10 02:00" \
  --duration "02:00" \
  --recur-every "Week Saturday" \
  --time-zone "UTC" \
  --reboot-setting IfRequired \
  --extension-properties '{"InGuestPatchMode":"User"}'

# List all maintenance configurations
az maintenance configuration list \
  --resource-group <rg> \
  --output table

# Show details of a maintenance configuration
az maintenance configuration show \
  --resource-group <rg> \
  --name <config-name>
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Maintenance/maintenanceConfigurations/patch-schedule-prod",
  "location": "eastus",
  "name": "patch-schedule-prod",
  "properties": {
    "duration": "02:00",
    "extensionProperties": {
      "InGuestPatchMode": "User"
    },
    "maintenanceScope": "InGuestPatch",
    "recurrencePattern": {
      "interval": 1,
      "patternType": "Weekly",
      "weekDays": [
        "Saturday"
      ]
    },
    "rebootSetting": "IfRequired",
    "startDateTime": "2026-05-10T02:00:00",
    "timeZone": "UTC"
  },
  "resourceGroup": "prod-rg",
  "type": "Microsoft.Maintenance/maintenanceConfigurations"
}

ResourceGroup              Name                    Location    MaintenanceScope
-----------------------  ----------------------  ----------  -----------------
prod-rg                   patch-schedule-prod    eastus      InGuestPatch
prod-rg                   patch-schedule-dev     eastus      InGuestPatch
prod-rg                   patch-schedule-test    westus2     InGuestPatch

(output from show command identical to create output above)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound: Resource group '<rg>' could not be found.` | Verify the resource group name with `az group list` and ensure you are in the correct subscription. |
    | `InvalidParameter: The value of parameter 'recur-every' is invalid. Accepted values are 'Week <DayOfWeek>' or 'Month <DayOfMonth>'.` | Use correct recurrence format such as `--recur-every "Week Saturday"` or `--recur-every "Month 15"`. |
    | `MissingRequiredParameter: --maintenance-scope is required` | Include `--maintenance-scope InGuestPatch` or `--maintenance-scope OSImage` in the command. |
---

## Assigning VMs to Maintenance Configurations

```bash
# Assign a VM to a maintenance configuration
az maintenance assignment create \
  --resource-group <rg> \
  --resource-name <vm-name> \
  --resource-type virtualMachines \
  --provider-name Microsoft.Compute \
  --configuration-assignment-name <assignment-name> \
  --maintenance-configuration-id <config-resource-id>

# List all maintenance assignments for a resource group
az maintenance assignment list \
  --resource-group <rg> \
  --output table

# Remove a maintenance assignment
az maintenance assignment delete \
  --resource-group <rg> \
  --resource-name <vm-name> \
  --resource-type virtualMachines \
  --provider-name Microsoft.Compute \
  --configuration-assignment-name <assignment-name>
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourcegroups/prod-rg/providers/microsoft.maintenance/maintenanceconfigurations/patch-tue-config/assignments/vm-patch-assign-001",
  "location": "eastus",
  "name": "vm-patch-assign-001",
  "resourceGroup": "prod-rg",
  "systemData": {
    "createdAt": "2024-01-15T10:32:45.123456+00:00",
    "createdBy": "admin@contoso.com",
    "createdByType": "User"
  },
  "type": "Microsoft.Maintenance/maintenanceConfigurations/assignments"
}

ConfigurationAssignmentName    ResourceGroup    ResourceName    ProviderName
-----------------------------  ---------------  ---------------  --------------------
vm-patch-assign-001           prod-rg          web-vm-01        Microsoft.Compute
vm-patch-assign-002           prod-rg          web-vm-02        Microsoft.Compute
patch-db-assign-001           prod-rg          sql-vm-prod      Microsoft.Compute

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The resource with id '<config-resource-id>' does not exist.` | Verify the maintenance configuration exists in the same subscription and region using `az maintenance configuration list`. |
    | `The resource 'Microsoft.Compute/virtualMachines/<vm-name>' does not exist in resource group '<rg>'.` | Confirm the VM name and resource group are correct with `az vm list --resource-group <rg>`. |
    | `The assignment '<assignment-name>' does not exist for resource '<vm-name>'.` | List existing assignments with `az maintenance assignment list --resource-group <rg>` to verify the assignment name before deletion. |
---

## On-Demand Patching

```bash
# Apply patches immediately on a Linux VM
az vm install-patches \
  --resource-group <rg> \
  --name <vm-name> \
  --maximum-duration PT2H \
  --reboot-setting IfRequired \
  --classifications-to-include-linux Critical Security

# Apply patches on a Windows VM with specific KB exclusions
az vm install-patches \
  --resource-group <rg> \
  --name <win-vm-name> \
  --maximum-duration PT1H \
  --reboot-setting IfRequired \
  --classifications-to-include-windows Critical Security UpdateRollup
```


```text title="Expected output"
{
  "rebootStatus": "NotNeeded",
  "maintenanceWindowExceeded": false,
  "excludedPatchCount": 0,
  "notSelectedPatchCount": 0,
  "pendingPatchCount": 0,
  "installedPatchCount": 12,
  "failedPatchCount": 0,
  "startDateTime": "2024-01-15T09:32:14.5821547Z",
  "patches": [
    {
      "patchId": "5031043",
      "name": "2024-01 Cumulative Update for Windows Server 2022",
      "version": "5031043",
      "classifications": [
        "Critical",
        "Security"
      ],
      "installationState": "Installed"
    },
    {
      "patchId": "KB5034765",
      "name": "Security Update for .NET Framework",
      "classifications": [
        "Security"
      ],
      "installationState": "Installed"
    }
  ],
  "errors": []
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.` | Verify the resource group name and VM name are correct using `az vm list --resource-group <rg>`. |
    | `AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/installPatches/action' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name>'.` | Ensure your Azure account has the Virtual Machine Contributor or higher role assigned on the resource group. |
    | `InvalidParameter: The value of parameter 'maximum-duration' is invalid. Supplied value: 'PT2H'. Valid values are between 'PT30M' and 'PT5H'.` | Use a duration between 30 minutes and 5 hours in ISO 8601 format (e.g., `PT1H30M`). |
---

## Compliance and Reporting

```bash
# Query patch compliance via Log Analytics (requires AMA + DCR configured)
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "Update | where TimeGenerated > ago(7d) | summarize count() by UpdateState, Classification, Computer | order by UpdateState" \
  --output table

# List updates pending on a specific VM
az maintenance update list \
  --resource-group <rg> \
  --resource-name <vm-name> \
  --resource-type virtualMachines \
  --provider-name Microsoft.Compute \
  --query "[?properties.status!='Installed'].{KB:properties.kbId, Classification:properties.classifications[0], Title:properties.title}" \
  --output table
```


```text title="Expected output"
UpdateState    Classification       Computer                Count_
Installed      Security             vm-prod-01              42
Installed      Critical             vm-prod-02              38
NotStarted     Security             vm-dev-03               12
Failed         Cumulative           vm-test-04              3
Installed      Other                vm-prod-01              8

KB           Classification    Title
KB5034765    Security          2024-01 Cumulative Update for Windows Server 2022
KB5034201    Critical          Security Update for .NET Framework
KB5033890    Other             Monthly Rollup for Windows 11
KB5033456    Security          Servicing Stack Update
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: (ResourceNotFound) The resource 'Microsoft.OperationalInsights/workspaces/<workspace-id>' could not be found.` | Verify the workspace ID is correct and exists in the current subscription with `az monitor log-analytics workspace list`. |
    | `ERROR: The resource group '<rg>' could not be found.` | Confirm the resource group name and subscription context with `az group list` and `az account show`. |
| Classification | Description |
|---|---|
| Critical | Vulnerabilities exploitable without user interaction |
| Security | CVE-rated fixes |
| UpdateRollup | Cumulative monthly rollup (Windows) |
| FeaturePack | New functionality bundled in an update |
| ServicePack | Cumulative application updates |
| Definition | Antivirus / Defender signature updates |
