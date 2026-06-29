---
tags:
  - azure
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

| Classification | Description |
|---|---|
| Critical | Vulnerabilities exploitable without user interaction |
| Security | CVE-rated fixes |
| UpdateRollup | Cumulative monthly rollup (Windows) |
| FeaturePack | New functionality bundled in an update |
| ServicePack | Cumulative application updates |
| Definition | Antivirus / Defender signature updates |
