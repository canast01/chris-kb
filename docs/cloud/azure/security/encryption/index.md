---
tags:
  - azure
  - security
description: "Azure encrypts all data at rest by default using platform-managed keys (PMK). Customer-managed keys (CMK) in Azure Key Vault give you control over the..."
---
# Azure — Encryption

<div class="kb-summary">
Azure encrypts all data at rest by default using platform-managed keys (PMK). Customer-managed keys (CMK) in Azure Key Vault give you control over the encryption key lifecycle. Data in transit is protected by TLS 1.2+ for all Azure service endpoints.

*Applies to: Azure*
</div>

---

```d2
direction: down

encryption_coverage_by_service: "Encryption Coverage by Service" {shape: rectangle}
azure_key_vault: "Azure Key Vault" {shape: rectangle}
customermanaged_keys_for_storage: "Customer-Managed Keys for Storage" {shape: rectangle}
customermanaged_keys_for_managed_dis: "Customer-Managed Keys for Managed Disks" {shape: rectangle}
azure_disk_encryption_ade: "Azure Disk Encryption (ADE)" {shape: rectangle}
tls_enforcement: "TLS Enforcement" {shape: rectangle}

encryption_coverage_by_service -> azure_key_vault: hardens
azure_key_vault -> customermanaged_keys_for_storage: hardens
customermanaged_keys_for_storage -> customermanaged_keys_for_managed_dis: hardens
customermanaged_keys_for_managed_dis -> azure_disk_encryption_ade: hardens
azure_disk_encryption_ade -> tls_enforcement: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Encryption Coverage by Service

| Service | At Rest | In Transit | CMK Support |
|---|---|---|---|
| Azure Storage (blobs, files, queues, tables) | AES-256, PMK default | TLS 1.2+ | Yes — Key Vault |
| Managed Disks | AES-256, PMK default | N/A (internal) | Yes — Disk Encryption Set |
| Azure SQL / SQL MI | TDE, PMK default | TLS 1.2+ | Yes — Key Vault |
| Azure Key Vault | AES-256, PMK | TLS 1.2+ | Yes — HSM-backed |
| Azure Backup | AES-256 | TLS 1.2+ | Yes — Key Vault |
| AKS (etcd) | AES-256, PMK | TLS 1.2+ | Yes — Key Vault |
| Azure Kubernetes node disks | PMK default | N/A | Yes — Disk Encryption Set |

---

## Azure Key Vault

Key Vault stores and controls access to keys, secrets, and certificates. All access is logged to Azure Monitor.

```bash
# Create a Key Vault (soft-delete and purge protection required for CMK)
az keyvault create \
  --name <kv-name> \
  --resource-group <rg-name> \
  --location <region> \
  --sku standard \
  --enable-soft-delete true \
  --enable-purge-protection true \
  --retention-days 90

# Set access policy (legacy model — prefer RBAC)
az keyvault set-policy \
  --name <kv-name> \
  --object-id <principal-object-id> \
  --key-permissions get list create delete unwrapKey wrapKey \
  --secret-permissions get list set delete

# Enable RBAC authorization (preferred over access policies)
az keyvault update \
  --name <kv-name> \
  --resource-group <rg-name> \
  --enable-rbac-authorization true

# Assign Key Vault Crypto Officer to an identity
az role assignment create \
  --role "Key Vault Crypto Officer" \
  --assignee <principal-object-id> \
  --scope <key-vault-resource-id>

# Check Key Vault firewall — restrict to known subnets and private endpoint
az keyvault network-rule list --name <kv-name>
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/kv-prod-sec-001",
  "location": "eastus",
  "name": "kv-prod-sec-001",
  "properties": {
    "enablePurgeProtection": true,
    "enableSoftDelete": true,
    "enableRbacAuthorization": false,
    "retentionDays": 90,
    "sku": "standard"
  },
  "resourceGroup": "prod-rg",
  "type": "Microsoft.KeyVault/vaults"
}
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/objectId/98f76543-21ab-cdef-5678-90abcdef1234",
  "permissions": {
    "keys": ["get", "list", "create", "delete", "unwrapKey", "wrapKey"],
    "secrets": ["get", "list", "set", "delete"]
  }
}
(no output — command completes silently)
{
  "canDelegate": false,
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/kv-prod-sec-001/providers/Microsoft.Authorization/roleAssignments/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "principalId": "98f76543-21ab-cdef-5678-90abcdef1234",
  "principalType": "ServicePrincipal",
  "roleDefinitionId": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/providers/Microsoft.Authorization/roleDefinitions/14b78a9a-5a6c-4d36-9478-88fefc3126de",
  "scope": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/kv-prod-sec-001",
  "type": "Microsoft.Authorization/roleAssignments"
}
{
  "bypass": "AzureServices",
  "defaultAction": "Allow",
  "ipRules": [],
  "virtualNetworkRules": [
    {
      "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Network/virtualNetworks/vnet-prod/subnets/app-subnet",
      "ignoreMissingVnetServiceEndpoint": false
    }
  ]
}
```

!!! warning "Common errors"
    **`The operation failed because the Key Vault name 'kv-name' is not globally unique.`** — Replace `<kv-name>` with a globally unique name (e.g., `kv-prod-sec-001-$(date +%s)`).
    **`Principal object ID not
### Key Vault Operations

```bash
# Create a key
az keyvault key create \
  --vault-name <kv-name> \
  --name <key-name> \
  --kty RSA \
  --size 4096 \
  --ops wrapKey unwrapKey

# List keys
az keyvault key list --vault-name <kv-name> --output table

# List secrets
az keyvault secret list --vault-name <kv-name> --output table

# Show a secret value
az keyvault secret show --vault-name <kv-name> --name <secret-name> --query value -o tsv

# Set a secret
az keyvault secret set \
  --vault-name <kv-name> \
  --name <secret-name> \
  --value "<secret-value>"

# Rotate a key (creates a new version; old version retained until explicitly deleted)
az keyvault key rotate --vault-name <kv-name> --name <key-name>
```


```text title="Expected output"
Key created successfully with kid: https://prodkv-eastus.vault.azure.net/keys/encryption-key-prod/a7f2c9e1b4d6f8h2j5k3l9m1n4o7p2q5

Name                 Enabled  Expires  Created             Updated
-------------------  -------  -------  ------------------  ------------------
encryption-key-prod  True              2024-01-15T09:42:18Z 2024-01-15T09:42:18Z
db-backup-key        True              2024-01-14T14:22:05Z 2024-01-14T14:22:05Z

Name                    Enabled  Expires  Created             Updated
-------------------     -------  -------  ------------------  ------------------
db-password             True              2024-01-12T11:33:22Z 2024-01-13T08:15:44Z
api-token-staging       True              2024-01-10T16:45:10Z 2024-01-10T16:45:10Z
tls-cert-passphrase     True              2024-01-08T13:20:33Z 2024-01-08T13:20:33Z

MyP@ssw0rd!Secure#2024

(no output — command completes silently)

Key rotated successfully. New version: a7f2c9e1b4d6f8h2j5k3l9m1n4o7p2q6
```

!!! warning "Common errors"
    **`The user, group or application 'appid=<id>;oid=<oid>' does not have secrets get permission on key vault '<kv-name>'.`** — Add the required permissions using `az keyvault set-policy --vault-name <kv-name> --object-id <oid> --secret-permissions get list`.
    **`Vault '<kv-name>' not found.`** — Verify the vault name is correct and exists in your subscription with `az keyvault list --output table`.
    **`The operation 'wrapKey' is not allowed by the key policy.`** — Update the key operations when creating it or use `az keyvault key update` to add the missing operations to the key's policy.
---

## Customer-Managed Keys for Storage

```bash
# Create a key for storage encryption
az keyvault key create \
  --vault-name <kv-name> \
  --name storage-cmk \
  --kty RSA \
  --size 4096

# Enable CMK on a storage account
az storage account update \
  --name <storage-account> \
  --resource-group <rg-name> \
  --encryption-key-source Microsoft.Keyvault \
  --encryption-key-vault "https://<kv-name>.vault.azure.net" \
  --encryption-key-name storage-cmk \
  --encryption-key-version <key-version>

# Verify CMK is active
az storage account show \
  --name <storage-account> \
  --query "encryption" \
  --output json
```


```text title="Expected output"
{
  "keySource": "Microsoft.Keyvault",
  "keyvaultproperties": {
    "keyname": "storage-cmk",
    "keyversion": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "keyvaulturi": "https://prod-kv-001.vault.azure.net"
  },
  "services": {
    "blob": {
      "enabled": true,
      "lastEnabledTime": "2024-01-15T09:42:33.000000+00:00"
    },
    "file": {
      "enabled": true,
      "lastEnabledTime": "2024-01-15T09:42:33.000000+00:00"
    },
    "queue": {
      "enabled": true,
      "lastEnabledTime": "2024-01-15T09:42:33.000000+00:00"
    },
    "table": {
      "enabled": true,
      "lastEnabledTime": "2024-01-15T09:42:33.000000+00:00"
    }
  }
}
```

!!! warning "Common errors"
    **`The client does not have permission to perform action 'Microsoft.KeyVault/vaults/keys/write' over scope`** — Ensure your Azure user or service principal has Key Vault Crypto Officer or equivalent role assigned on the key vault.
    **`The Key Vault URI provided is invalid or the key does not exist`** — Verify the key vault name is correct, the key exists with `az keyvault key list --vault-name <kv-name>`, and the storage account has network access to the key vault.
    **`Storage account does not support customer-managed keys in this region`** — Confirm the storage account region supports CMK (most standard regions do) and use a supported account kind like StorageV2 or BlobStorage.
---

## Customer-Managed Keys for Managed Disks

Disk Encryption Sets (DES) link a Key Vault key to managed disk encryption.

```bash
# Create a Disk Encryption Set
az disk-encryption-set create \
  --name <des-name> \
  --resource-group <rg-name> \
  --location <region> \
  --key-url "https://<kv-name>.vault.azure.net/keys/<key-name>/<key-version>" \
  --source-vault <kv-resource-id>

# Grant the DES access to the Key Vault key
DES_IDENTITY=$(az disk-encryption-set show \
  --name <des-name> \
  --resource-group <rg-name> \
  --query "identity.principalId" -o tsv)

az role assignment create \
  --role "Key Vault Crypto Service Encryption User" \
  --assignee $DES_IDENTITY \
  --scope <kv-resource-id>

# Create a managed disk using the DES
az disk create \
  --name <disk-name> \
  --resource-group <rg-name> \
  --size-gb 128 \
  --disk-encryption-set <des-resource-id>

# Apply DES to an existing VM's OS disk
az vm update \
  --name <vm-name> \
  --resource-group <rg-name> \
  --disk-encryption-set <des-resource-id>
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/prod-rg/providers/Microsoft.Compute/diskEncryptionSets/des-prod-001",
  "location": "eastus",
  "name": "des-prod-001",
  "resourceGroup": "prod-rg",
  "identity": {
    "principalId": "f7e8d9c0-b1a2-3c4d-5e6f-7a8b9c0d1e2f",
    "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
    "type": "SystemAssigned"
  },
  "keyVaultProperties": {
    "keyUrl": "https://kv-prod.vault.azure.net/keys/cmk-key-01/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
  }
}
f7e8d9c0-b1a2-3c4d-5e6f-7a8b9c0d1e2f
{
  "canDelegate": false,
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/prod-rg/providers/Microsoft.Authorization/roleAssignments/9d8c7b6a-5f4e-3d2c-1b0a-f9e8d7c6b5a4",
  "principalId": "f7e8d9c0-b1a2-3c4d-5e6f-7a8b9c0d1e2f",
  "principalType": "ServicePrincipal",
  "roleDefinitionId": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/providers/Microsoft.Authorization/roleDefinitions/e147488a-f6f5-4113-8e2d-b22465e65bf6",
  "scope": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/kv-prod"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/prod-rg/providers/Microsoft.Compute/disks/disk-data-001",
  "name": "disk-data-001",
  "resourceGroup": "prod-rg",
  "location": "eastus",
  "sizeGb": 128,
  "encryptionSettings": {
    "enabled": true
  }
}
{
  "id": "/subscriptions/a1b2c3
```
---

## Azure Disk Encryption (ADE)

ADE encrypts VM disks at the OS level using BitLocker (Windows) or DM-Crypt (Linux). Keys are stored in Key Vault.

```bash
# Enable ADE on a Windows VM
az vm encryption enable \
  --name <vm-name> \
  --resource-group <rg-name> \
  --disk-encryption-keyvault <kv-resource-id>

# Enable ADE on a Linux VM
az vm encryption enable \
  --name <vm-name> \
  --resource-group <rg-name> \
  --disk-encryption-keyvault <kv-resource-id> \
  --volume-type All

# Check ADE status
az vm encryption show \
  --name <vm-name> \
  --resource-group <rg-name>
```


```text title="Expected output"
{
  "disks": [
    {
      "name": "myvm_OsDisk_1_a1b2c3d4e5f6g7h8",
      "encryptionSettings": {
        "enabled": true,
        "version": "1.1"
      },
      "statuses": [
        {
          "code": "ProvisioningState/succeeded",
          "displayStatus": "Provisioning succeeded",
          "time": "2024-01-15T14:32:18.000000+00:00"
        }
      ]
    },
    {
      "name": "myvm_DataDisk_0_b2c3d4e5f6g7h8i9",
      "encryptionSettings": {
        "enabled": true,
        "version": "1.1"
      },
      "statuses": [
        {
          "code": "ProvisioningState/succeeded",
          "displayStatus": "Provisioning succeeded",
          "time": "2024-01-15T14:35:22.000000+00:00"
        }
      ]
    }
  ],
  "osProfile": {
    "computerName": "myvm"
  }
}
```

!!! warning "Common errors"
    **`The Key Vault 'kv-name' is not enabled for disk encryption.`** — Enable the Key Vault for Azure Disk Encryption by running `az keyvault update --name <kv-name> --enabled-for-disk-encryption true`.
    **`The user does not have permission to perform action 'Microsoft.KeyVault/vaults/keys/read' on resource.`** — Ensure the VM's managed identity or service principal has Key Vault Crypto Officer or equivalent RBAC role assigned.
    **`VM must be deallocated before encryption can be enabled.`** — Stop the VM first with `az vm deallocate --name <vm-name> --resource-group <rg-name>`, then retry the encryption command.
> **ADE vs Server-Side Encryption (SSE):** SSE with CMK (Disk Encryption Set) encrypts at the storage layer — simpler to manage and works for all disk types. ADE encrypts at the OS layer — required for some compliance standards (FIPS 140-2). Do not apply both; pick one per workload.

---

## TLS Enforcement

### Storage Account

```bash
# Require TLS 1.2 minimum on storage accounts
az storage account update \
  --name <storage-account> \
  --resource-group <rg-name> \
  --min-tls-version TLS1_2

# Verify minimum TLS version
az storage account show \
  --name <storage-account> \
  --query "minimumTlsVersion"

# Require HTTPS-only (disable HTTP)
az storage account update \
  --name <storage-account> \
  --resource-group <rg-name> \
  --https-only true
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b5c-6d7e-8f9g-0h1i-2j3k4l5m6n7o/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstg2024",
  "name": "prodstg2024",
  "type": "Microsoft.Storage/storageAccounts",
  "location": "eastus",
  "minimumTlsVersion": "TLS1_2"
}
"TLS1_2"
{
  "id": "/subscriptions/12a34b5c-6d7e-8f9g-0h1i-2j3k4l5m6n7o/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstg2024",
  "name": "prodstg2024",
  "type": "Microsoft.Storage/storageAccounts",
  "httpsTrafficOnlyEnabled": true,
  "minimumTlsVersion": "TLS1_2"
}
```

!!! warning "Common errors"
    **`The resource 'Microsoft.Storage/storageAccounts/<storage-account>' under resource group '<rg-name>' was not found.`** — Verify the storage account name and resource group name are correct and exist in your subscription.
    **`The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Storage/storageAccounts/write' over scope '/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.Storage/storageAccounts/<storage-account>'.`** — Ensure your Azure account has Storage Account Contributor or Owner role on the target resource group.
### App Service / API Management

```bash
# Set minimum TLS on App Service
az webapp config set \
  --name <app-name> \
  --resource-group <rg-name> \
  --min-tls-version 1.2

# Enforce HTTPS redirect
az webapp update \
  --name <app-name> \
  --resource-group <rg-name> \
  --https-only true
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg/providers/Microsoft.Web/sites/myapp-prod",
  "name": "myapp-prod",
  "type": "Microsoft.Web/sites",
  "location": "eastus",
  "tags": {},
  "kind": "app,linux",
  "properties": {
    "serverFarmId": "/subscriptions/a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p/resourceGroups/prod-rg/providers/Microsoft.Web/serverfarms/myapp-plan",
    "minTlsVersion": "1.2",
    "httpsOnly": true,
    "state": "Running"
  }
}
```

!!! warning "Common errors"
    **`The specified resource group '<rg-name>' could not be found.`** — Verify the resource group name with `az group list` and ensure you are in the correct subscription.
    **`The specified App Service '<app-name>' does not exist in the specified resource group.`** — Confirm the app name matches exactly with `az webapp list --resource-group <rg-name>` and check for typos.
    **`AuthorizationFailed: The client 'user@example.com' with object id 'xxx' does not have authorization to perform action 'Microsoft.Web/sites/write' over scope '/subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.Web/sites/xxx'.`** — Ensure your Azure account has Contributor or Web Plan Contributor role on the resource group.
---

## Private Endpoints for Key Vault

Key Vault should only be accessible from private endpoints — no public network access.

```bash
# Disable public network access on Key Vault
az keyvault update \
  --name <kv-name> \
  --resource-group <rg-name> \
  --public-network-access Disabled

# Create a private endpoint
az network private-endpoint create \
  --name pe-keyvault \
  --resource-group <rg-name> \
  --vnet-name <vnet-name> \
  --subnet <subnet-name> \
  --private-connection-resource-id <kv-resource-id> \
  --group-id vault \
  --connection-name pec-keyvault

# Create DNS record for private endpoint resolution
az network private-dns zone create \
  --resource-group <rg-name> \
  --name "privatelink.vaultcore.azure.net"

az network private-endpoint dns-zone-group create \
  --resource-group <rg-name> \
  --endpoint-name pe-keyvault \
  --name keyvault-dns-group \
  --private-dns-zone "privatelink.vaultcore.azure.net" \
  --zone-name keyvault
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cd2/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/prod-kv-001",
  "name": "prod-kv-001",
  "publicNetworkAccess": "Disabled",
  "properties": {
    "tenantId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "sku": {
      "family": "A",
      "name": "standard"
    }
  }
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cd2/resourceGroups/prod-rg/providers/Microsoft.Network/privateEndpoints/pe-keyvault",
  "name": "pe-keyvault",
  "location": "eastus",
  "privateLinkServiceConnections": [
    {
      "name": "pec-keyvault",
      "privateLinkServiceId": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cd2/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/prod-kv-001",
      "groupIds": ["vault"],
      "requestMessage": "",
      "privateLinkServiceConnectionState": {
        "status": "Approved",
        "description": "Auto-approved",
        "actionsRequired": "None"
      }
    }
  ]
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cd2/resourceGroups/prod-rg/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net",
  "name": "privatelink.vaultcore.azure.net",
  "type": "Microsoft.Network/privateDnsZones",
  "location": "global"
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cd2/resourceGroups/prod-rg/providers/Microsoft.Network/privateEndpoints/pe-keyvault/privateDnsZoneGroups/keyvault-dns-group",
  "name": "keyvault-dns-group",
  "privateDnsZoneConfigs": [
    {
      "name": "keyvault",
      "privateDnsZoneId": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cd2/resourceGroups/prod-rg/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net"
    }
  ]
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.KeyVault/vaults/<kv-name>' under resource group '<rg-name>' was not found.`** — Verify the Key Vault name and resource group name are correct and exist in your subscription.
    **`(InvalidResourceId) The provided resource ID is invalid or does not exist.`** — Ensure the `<kv-
---

## Key Vault Diagnostics

```bash
# Enable audit logging to Log Analytics
az monitor diagnostic-settings create \
  --name kv-diagnostics \
  --resource <kv-resource-id> \
  --workspace <log-analytics-workspace-id> \
  --logs '[{"category": "AuditEvent", "enabled": true}]'

# Query Key Vault access logs in Log Analytics
# AzureDiagnostics
# | where ResourceType == "VAULTS"
# | where OperationName in ("SecretGet", "KeyUnwrap", "KeyWrap")
# | project TimeGenerated, CallerIPAddress, identity_claim_oid_g, OperationName, ResultType
# | order by TimeGenerated desc

# Alert on Key Vault secret access by unexpected principals
# Create a scheduled query rule in Azure Monitor targeting the above query
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/rg-security/providers/microsoft.insights/diagnosticsettings/kv-diagnostics",
  "identity": null,
  "kind": null,
  "location": null,
  "name": "kv-diagnostics",
  "resourceGroup": "rg-security",
  "tags": null,
  "type": "Microsoft.Insights/diagnosticSettings",
  "properties": {
    "logs": [
      {
        "category": "AuditEvent",
        "categoryGroup": null,
        "enabled": true,
        "retentionPolicy": {
          "days": 0,
          "enabled": false
        }
      }
    ],
    "metrics": [],
    "workspaceId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/rg-security/providers/microsoft.operationalinsights/workspaces/law-audit",
    "storageAccountId": null,
    "serviceBusRuleId": null,
    "eventHubAuthorizationRuleId": null,
    "eventHubName": null,
    "logAnalyticsDestinationType": null
  }
}
```

!!! warning "Common errors"
    **`ResourceNotFound : The resource '/subscriptions/.../providers/Microsoft.KeyVault/vaults/kv-prod' could not be found.`** — Verify the Key Vault resource ID is correct and exists in the specified subscription using `az keyvault show --name <vault-name> --query id`.
    **`AuthorizationFailed : The client 'user@contoso.com' with object id '...' does not have authorization to perform action 'microsoft.insights/diagnosticsettings/write' on resource '...'.`** — Grant the user or service principal the "Monitoring Contributor" role on the Key Vault resource using `az role assignment create --role "Monitoring Contributor" --assignee <principal-id> --scope <kv-resource-id>`.
---

## See also

- [Azure — Hardening](../hardening/)
- [Azure — Authentication](../authentication/)
- [Azure — Access Control](../access-control/)
