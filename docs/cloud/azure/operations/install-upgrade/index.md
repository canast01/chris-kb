---
tags:
  - azure
  - operations
description: "VM image management, patching via Azure Update Manager, and service upgrades."
---
# Azure — Install & Upgrade

<div class="kb-summary">
VM image management, patching via Azure Update Manager, and service upgrades.

*Applies to: Azure*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
azure_vm_patching_workflow: "Azure VM Patching Workflow" {shape: rectangle}
vm_patching: "VM Patching" {shape: rectangle}
aks_upgrade: "AKS Upgrade" {shape: rectangle}
service_retirement_tracking: "Service Retirement Tracking" {shape: rectangle}
subscription_lifecycle: "Subscription Lifecycle" {shape: rectangle}
resource_group_expiry_nonproduction: "Resource Group Expiry (Non-Production)" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> azure_vm_patching_workflow
azure_vm_patching_workflow -> vm_patching
vm_patching -> aks_upgrade
aks_upgrade -> service_retirement_tracking
service_retirement_tracking -> subscription_lifecycle
subscription_lifecycle -> resource_group_expiry_nonproduction
resource_group_expiry_nonproduction -> validate
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Azure VM Patching Workflow

## VM Patching

VM OS images are patched via Azure Update Manager on a monthly schedule:

```bash
# Check patch assessment for a VM
az maintenance assignment list --resource-group <rg> --provider-name Microsoft.Compute \
    --resource-type virtualMachines --resource-name <vm-name>

# Trigger on-demand assessment
az maintenance apply-updates create --resource-group <rg> \
    --provider-name Microsoft.Compute --resource-type virtualMachines --resource-name <vm-name>

# Check patch compliance status
az update-management-v2 assess --resource-group <rg> --vm-name <vm-name>
```


```text title="Expected output"
[
  {
    "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourcegroups/prod-rg/providers/microsoft.compute/virtualmachines/web-vm-01/providers/microsoft.maintenance/configurationassignments/maint-assign-001",
    "location": "eastus",
    "name": "maint-assign-001",
    "resourceGroup": "prod-rg",
    "type": "Microsoft.Maintenance/configurationAssignments"
  }
]

{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourcegroups/prod-rg/providers/microsoft.compute/virtualmachines/web-vm-01/providers/microsoft.maintenance/applyupdates/20240115T143022Z",
  "name": "20240115T143022Z",
  "properties": {
    "lastUpdateTime": "2024-01-15T14:30:22.456Z",
    "resourceId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourcegroups/prod-rg/providers/microsoft.compute/virtualmachines/web-vm-01",
    "status": "InProgress"
  },
  "type": "Microsoft.Maintenance/applyUpdates"
}

{
  "assessmentId": "assess-20240115-prod",
  "machineId": "web-vm-01",
  "patchCount": 12,
  "status": "Compliant",
  "lastAssessmentTime": "2024-01-15T14:25:00Z",
  "criticalUpdates": 2,
  "securityUpdates": 5
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.` | Verify the VM name and resource group name are correct and the VM exists in your subscription. |
    | `Operation returned an invalid status code 'Forbidden'` | Ensure your Azure account has the Contributor or Owner role on the resource group or subscription. |
    | `The operation timed out. Please try again later.` | Retry the command after a few moments, as the maintenance service may be temporarily unavailable. |
Patching waves:
- Development: Patch Tuesday + 1 day (auto-reboot allowed)
- Staging: Patch Tuesday + 3 days
- Production: maintenance window (manual reboot approval required)

## AKS Upgrade

AKS supports N-2 minor Kubernetes versions. Clusters on unsupported versions receive no patches:

```bash
# Check available upgrades
az aks get-upgrades --name <cluster-name> -g <rg> --output table

# Upgrade control plane first
az aks upgrade --name <cluster-name> -g <rg> --kubernetes-version 1.30 --no-wait

# Monitor upgrade progress
az aks show --name <cluster-name> -g <rg> --query 'provisioningState'

# Upgrade node pools after control plane completes
az aks nodepool upgrade --cluster-name <cluster-name> -g <rg> \
    --name <nodepool-name> --kubernetes-version 1.30
```


```text title="Expected output"
Name             ResourceGroup    CurrentVersion    Upgrades
---------------  ---------------  ----------------  ----------
prod-cluster-01  infrastructure   1.28.5            1.29.11, 1.30.0
Kubernetes version upgrade initiated for cluster prod-cluster-01
Succeeded
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The resource 'Microsoft.ContainerService/managedClusters/<cluster-name>' under resource group '<rg>' was not found.` | Verify the cluster name and resource group name are correct and exist in your subscription. |
    | `Upgrade failed: Node pool <nodepool-name> not found in cluster <cluster-name>.` | Confirm the node pool name matches exactly (case-sensitive) by running `az aks nodepool list --cluster-name <cluster-name> -g <rg>`. |
    | `Kubernetes version 1.30 is not available for upgrade from version 1.28.5.` | Check available versions with `az aks get-upgrades --name <cluster-name> -g <rg>` and select a supported target version. |
## Service Retirement Tracking

Monitor Azure service retirements:
- Azure Portal → Home → Recommendations → Retirements
- Subscribe to Azure Updates: [azure.microsoft.com/en-us/updates](https://azure.microsoft.com/en-us/updates/)
- Azure Advisor: Operational Excellence recommendations

```bash
# Check Advisor recommendations
az advisor recommendation list --category OperationalExcellence \
    --query "[?contains(shortDescription.solution, 'Upgrade')]"
```


```text title="Expected output"
[
  {
    "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourcegroups/prod-rg/providers/microsoft.compute/virtualmachines/vm-app-01/providers/microsoft.advisor/recommendations/upgrade-vm-sku-001",
    "name": "upgrade-vm-sku-001",
    "type": "Microsoft.Advisor/recommendations",
    "category": "OperationalExcellence",
    "impact": "Medium",
    "shortDescription": {
      "problem": "VM SKU is outdated",
      "solution": "Upgrade to newer generation VM SKU for better performance"
    },
    "description": "Your virtual machine vm-app-01 is running on Standard_D2s_v3. Consider upgrading to Standard_D2s_v4 for improved CPU and memory efficiency.",
    "lastUpdated": "2024-01-15T10:32:45Z",
    "resourceMetadata": {
      "resourceId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourcegroups/prod-rg/providers/microsoft.compute/virtualmachines/vm-app-01"
    }
  },
  {
    "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourcegroups/prod-rg/providers/microsoft.sql/servers/sqldb-prod/databases/appdb/providers/microsoft.advisor/recommendations/upgrade-sql-edition-002",
    "name": "upgrade-sql-edition-002",
    "type": "Microsoft.Advisor/recommendations",
    "category": "OperationalExcellence",
    "impact": "High",
    "shortDescription": {
      "problem": "SQL Database edition is outdated",
      "solution": "Upgrade SQL Database to latest edition for security and performance"
    },
    "description": "Your SQL Database appdb is running on Standard edition. Upgrade to Premium edition to benefit from enhanced security features and SLA improvements.",
    "lastUpdated": "2024-01-14T09:15:22Z"
  }
]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: The following arguments are required: --subscription` | Add `--subscription <subscription-id>` or set the default subscription with `az account set --subscription <id>`. |
    | `ERROR: (AuthorizationFailed) The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.Advisor/recommendations/read' over scope '/subscriptions/...'` | Ensure your Azure account has Reader or Advisor role assigned at the subscription level using `az role assignment create`. |
## Subscription Lifecycle

```bash
# List all subscriptions in tenant
az account list --all --output table

# Move subscription to different management group
az management-group subscriptions add --name <sub-id> --management-group <mg-id>

# Decommission subscription
# 1. Cancel all resources
# 2. Remove from management groups
# 3. Cancel subscription (requires Billing Admin role)
az account set --subscription <sub-id>
# Cancel in Azure Portal → Subscriptions → Cancel
```


```text title="Expected output"
Name                                   CloudName    SubscriptionId                       TenantId                             State
------------------------------------   -----------  ------------------------------------  ------------------------------------  -------
Production-East                        AzureCloud   a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d  f5e6d7c8-b9a0-1c2d-3e4f-5a6b7c8d9e0f  Enabled
Development-West                       AzureCloud   b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e  f5e6d7c8-b9a0-1c2d-3e4f-5a6b7c8d9e0f  Enabled
Staging-Central                        AzureCloud   c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f  f5e6d7c8-b9a0-1c2d-3e4f-5a6b7c8d9e0f  Enabled
(no output — command completes silently)
Subscription 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d' set as default.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The subscription 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d' could not be found.` | Verify the subscription ID is correct and you have access to it using `az account list`. |
    | `You do not have permission to perform action 'Microsoft.Management/managementGroups/subscriptions/write' on scope '/providers/Microsoft.Management/managementGroups/<mg-id>'.` | Ensure your account has Management Group Contributor or Owner role on the target management group. |
90-day hold period after cancellation before permanent deletion.

## Resource Group Expiry (Non-Production)

Tag non-production resource groups with expiry:

```bash
# Tag with expiry date
az group update --name <rg-name> --tags ExpiryDate=2026-12-31 Environment=dev

# Script to find expired RGs (run monthly)
az group list --query "[?tags.ExpiryDate < '$(date +%Y-%m-%d)'].{Name:name,ExpiryDate:tags.ExpiryDate}" --output table
```


```text title="Expected output"
Name                          ExpiryDate
------------------------------  ----------
rg-legacy-services            2024-08-15
rg-temp-testing               2025-03-22
rg-sandbox-old                2024-11-10
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The following arguments are required: --name, --tags` | Ensure `<rg-name>` is replaced with an actual resource group name and tags are formatted as key=value pairs. |
    | `InvalidTemplateDeployment : The template is invalid: The property 'tags' cannot be found on the resource of type 'Microsoft.Resources/resourceGroups'.` | Verify the resource group exists and you have sufficient permissions (Contributor or Owner role) to modify tags. |
Expired RGs are notified to owner 14 days before deletion.

## Entra ID App Registration Lifecycle

```bash
# List app registrations with credential expiry
az ad app list --all --query "[*].{AppId:appId,DisplayName:displayName}" -o table

# Check credential expiry dates
az ad app credential list --id <app-id>

# Rotate client secret
az ad app credential reset --id <app-id> --credential-description "rotation-$(date +%Y%m)"
```


```text title="Expected output"
AppId                                DisplayName
------------------------------------  --------------------------------
a1b2c3d4-e5f6-7890-abcd-ef1234567890  MyWebApp
b2c3d4e5-f6a7-8901-bcde-f12345678901  DataProcessorService
c3d4e5f6-a7b8-9012-cdef-123456789012  ReportingAPI
d4e5f6a7-b8c9-0123-defg-234567890123  AuthenticationService

CredentialId                          StartDate             EndDate
------------------------------------  --------------------  --------------------
cred-001-uuid-string-here-1234567890  2023-01-15T10:30:00Z  2025-01-15T10:30:00Z
cred-002-uuid-string-here-2345678901  2023-06-20T14:22:00Z  2024-06-20T14:22:00Z

{
  "appId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "password": "Eby8vdM02xNOcqFlqUwJPLMeuL7DJH5V7EdgH1xF32s=",
  "keyId": "new-cred-uuid-5678901234567890abcd",
  "startDate": "2024-01-10T16:45:22.123456Z",
  "endDate": "2026-01-10T16:45:22.123456Z"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The following arguments are required: --id` | Provide the app registration ID using `--id <app-id>` parameter in the credential commands. |
    | `Operation failed with status: 'Forbidden'. Details: Authorization_RequestDenied` | Ensure your Azure account has sufficient permissions (Application Administrator or Global Administrator role) to manage app credentials. |
    | `ResourceNotFound: Resource not found` | Verify the app ID exists and is correctly formatted as a valid UUID. |
Alert 60 days before credential expiry — expired credentials break CI/CD pipelines silently.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Azure — Deploy](../../deploy/)
