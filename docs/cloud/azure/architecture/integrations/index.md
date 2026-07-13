---
tags:
  - architecture
  - azure
description: "Azure Integration reference covering Azure VM Deployment Flow, Azure AD Connect (Hybrid Identity), Azure Monitor → SIEM, GitHub Actions + OIDC Federation..."
---
# Azure Integration

<div class="kb-summary">
Azure Integration reference covering Azure VM Deployment Flow, Azure AD Connect (Hybrid Identity), Azure Monitor → SIEM, GitHub Actions + OIDC Federation, Terraform Remote State and 2 more sections.

*Applies to: Azure*
</div>

## Azure VM Deployment Flow

```d2
direction: right

request: "Deployment Request\nPortal / CLI / Terraform" {shape: rectangle}
rbacCheck: "RBAC Check\nMicrosoft.Compute/virtualMachines/write" {shape: rectangle}
policyCheck: "Azure Policy Evaluation\nallowed SKUs · allowed regions" {shape: rectangle}
resourceGroup: "Resource Group\nrg-prod-euw-app" {shape: rectangle}
vnetPlace: "VNet / Subnet Placement\nsnet-prod-euw-app" {shape: rectangle}
nsgApply: "NSG Applied\ndefault rules + custom" {shape: rectangle}
diskAttach: "Managed Disk\nOS + data disks attached" {shape: rectangle}
extensions: "Extensions Applied\nMonitor Agent · Defender · Custom Script" {shape: rectangle}
running: "VM Running\nProvisioning State: Succeeded" {shape: rectangle}

request -> rbacCheck
rbacCheck -> policyCheck
policyCheck -> resourceGroup
resourceGroup -> vnetPlace
vnetPlace -> nsgApply
nsgApply -> diskAttach
diskAttach -> extensions
extensions -> running
```

## Azure AD Connect (Hybrid Identity)

```powershell
# Check AD Connect sync status
Import-Module ADSync
Get-ADSyncScheduler           # Verify SyncCycleEnabled = True
Get-ADSyncConnectorRunStatus  # Last sync status
```

Verify sync health in Entra ID admin center: Identity → Hybrid management → Azure AD Connect.

If sync fails:
```powershell
Start-ADSyncSyncCycle -PolicyType Delta   # Force delta sync
Start-ADSyncSyncCycle -PolicyType Initial # Full sync (slow — only if required)
```

## Azure Monitor → SIEM

Configure diagnostic settings to send to Log Analytics and Event Hub:

```bash
# Enable diagnostic settings on a resource (example: NSG)
az monitor diagnostic-settings create --name "to-log-analytics" \
    --resource <nsg-resource-id> \
    --workspace <log-analytics-workspace-id> \
    --logs '[{"category": "NetworkSecurityGroupEvent", "enabled": true}]'

# Stream to Splunk/Elastic via Event Hub
az eventhubs eventhub create --name azure-logs --namespace-name <ns> -g <rg>
# Configure Splunk Add-on for Microsoft Cloud Services to pull from Event Hub
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/prod-rg/providers/microsoft.insights/diagnosticsettings/to-log-analytics",
  "name": "to-log-analytics",
  "properties": {
    "workspaceId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/prod-rg/providers/microsoft.operationalinsights/workspaces/prod-law",
    "logs": [
      {
        "category": "NetworkSecurityGroupEvent",
        "enabled": true,
        "retentionPolicy": {
          "enabled": false,
          "days": 0
        }
      }
    ],
    "metrics": []
  },
  "type": "Microsoft.Insights/diagnosticSettings"
}
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.EventHub/namespaces/prod-ns/eventhubs/azure-logs",
  "name": "azure-logs",
  "type": "Microsoft.EventHub/eventhubs",
  "location": "eastus",
  "properties": {
    "messageRetentionInDays": 1,
    "partitionCount": 4,
    "status": "Active",
    "createdAt": "2024-01-15T10:32:45.123Z"
  }
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource '<nsg-resource-id>' could not be found.`** — Verify the NSG resource ID is correct and exists in the specified subscription using `az network nsg show -g <rg> -n <nsg-name>`.
    **`InvalidOperation: The workspace '<log-analytics-workspace-id>' does not exist or the user does not have access.`** — Confirm the Log Analytics workspace ID is valid and your account has Contributor role on that workspace using `az monitor log-analytics workspace show --resource-group <rg> -n <workspace-name>`.
    **`BadRequest: The namespace '<ns>' already exists in the resource group.`** — Use a unique Event Hub namespace name or retrieve the existing one with `az eventhubs namespace list -g <rg>`.
## GitHub Actions + OIDC Federation

No client secrets — use OIDC:

```bash
# Create federated credential on service principal
az ad app federated-credential create --id <app-id> --parameters '{
  "name": "github-actions-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:org/repo:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'
```

```yaml
# .github/workflows/deploy.yml
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

## Terraform Remote State

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "corpterraformstateprod"
    container_name       = "tfstate"
    key                  = "prod/vnet/terraform.tfstate"
  }
}
```

State storage account standards:
- Versioning enabled
- Soft delete enabled (30-day retention)
- Network access restricted to Terraform runner IPs

## Azure Backup

```bash
# List recovery vaults
az backup vault list --output table

# List protected items in vault
az backup item list --vault-name <vault> -g <rg> --output table

# Trigger ad-hoc backup
az backup protection backup-now --vault-name <vault> -g <rg> \
    --item-name <vm-name> --container-name <container> \
    --backup-management-type AzureIaasVM --retain-until 2026-12-31
```


```text title="Expected output"
Name                          ResourceGroup        Location    Type
-----------------------------  -------------------  ----------  ----------------
prod-recovery-vault-eastus    infrastructure-prod  eastus      Microsoft.RecoveryServices/vaults
dr-recovery-vault-westus2     infrastructure-dr    westus2     Microsoft.RecoveryServices/vaults
backup-vault-central          infrastructure-test  centralus   Microsoft.RecoveryServices/vaults

VaultName                     ResourceGroup        BackupManagementType    ProtectionStatus
-----------------------------  -------------------  ----------------------  ----------------
prod-recovery-vault-eastus    infrastructure-prod  AzureIaasVM             Healthy
prod-recovery-vault-eastus    infrastructure-prod  AzureIaasVM             Protected
dr-recovery-vault-westus2     infrastructure-dr    AzureIaasVM             Healthy

Backup triggered for item 'web-server-01' in vault 'prod-recovery-vault-eastus'. Job ID: 123e4567-e89b-12d3-a456-426614174000
```

!!! warning "Common errors"
    **`ResourceNotFound : The specified vault 'invalid-vault' could not be found in resource group 'infrastructure-prod'.`** — Verify the vault name and resource group name match exactly using `az backup vault list`.
    **`MissingRequiredArgument: the following arguments are required: --container-name`** — Retrieve the correct container name with `az backup container list --vault-name <vault> -g <rg>` before running backup-now.
    **`InvalidArgument: The retain-until date '2026-12-31' must be in the future and within 99 years from today.`** — Use a valid future date in YYYY-MM-DD format that is less than 99 years away.
## Key Vault Integration

```bash
# Verify Key Vault is accessible
az keyvault show --name <kv-name> --query 'properties.provisioningState'

# Grant access to a managed identity
az keyvault set-policy --name <kv-name> \
    --object-id <managed-identity-object-id> \
    --secret-permissions get list

# Test secret retrieval
az keyvault secret show --vault-name <kv-name> --name <secret-name>
```


```text title="Expected output"
"Succeeded"
(no output — command completes silently)
{
  "attributes": {
    "created": 1704067200,
    "enabled": true,
    "expires": null,
    "notBefore": null,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": 1704067200
  },
  "id": "https://prod-kv-eastus.vault.azure.net/secrets/db-password/a7f2c9e1b4d6f8h2j5k8l1m4n7p0q3r6",
  "name": "db-password",
  "tags": null,
  "value": "P@ssw0rd123!SecureValue"
}
```

!!! warning "Common errors"
    **`(KeyVaultAccessDenied) The user, group or application 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have secrets get permission on key vault 'prod-kv-eastus'.`** — Run the `az keyvault set-policy` command to grant the managed identity `get` and `list` permissions on the vault.
    **`(ResourceNotFound) The Resource 'Microsoft.KeyVault/vaults/<kv-name>' under resource group '<rg-name>' was not found.`** — Verify the Key Vault name and resource group are correct, and that the vault exists in your current Azure subscription.
    **`(InvalidSecretName) The secret name '<secret-name>' is invalid.`** — Confirm the secret name exists in the vault by running `az keyvault secret list --vault-name <kv-name>` to list all available secrets.
---

## See also

- [Azure — Design Standards](../design-standards/)
