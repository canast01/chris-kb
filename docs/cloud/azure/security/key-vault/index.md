---
tags:
  - azure
  - security
---
# Azure — Key Vault

<div class="kb-summary">
Azure Key Vault is a managed service for storing and controlling access to secrets, encryption keys, and certificates. It provides hardware security module (HSM) backing, RBAC-based access control, soft-delete protection, and audit logging.

*Applies to: Azure*
</div>

```d2
direction: down

vault_vs_managed_hsm: "Vault vs Managed HSM" {shape: rectangle}
access_model: "Access Model" {shape: rectangle}
creating_a_key_vault: "Creating a Key Vault" {shape: rectangle}
managing_secrets: "Managing Secrets" {shape: rectangle}
soft_delete_and_purge_protection: "Soft Delete and Purge Protection" {shape: rectangle}
networking_private_endpoint: "Networking — Private Endpoint" {shape: rectangle}

vault_vs_managed_hsm -> access_model: uses
access_model -> creating_a_key_vault: uses
creating_a_key_vault -> managing_secrets: uses
managing_secrets -> soft_delete_and_purge_protection: uses
soft_delete_and_purge_protection -> networking_private_endpoint: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Vault vs Managed HSM

| Feature | Key Vault (Standard) | Key Vault (Premium) | Managed HSM |
|---|---|---|---|
| Secrets / Certs | Yes | Yes | No |
| Keys (software) | Yes | Yes | No |
| Keys (HSM-backed) | No | Yes | Yes |
| FIPS 140-2 level | Level 1 | Level 2 | Level 3 |
| Dedicated HSM | No | No | Yes |
| Use case | General secrets and certs | HSM-backed keys alongside secrets | High-security key material only |

## Access Model

Key Vault supports two permission models (set at vault creation; cannot be changed):

| Model | How access is granted | Recommended |
|---|---|---|
| **Vault access policy** | Legacy; per-vault principal-based permissions | No |
| **Azure RBAC** | Standard Azure RBAC via role assignments | Yes |

**Use RBAC.** It enables centralized access management, PIM eligibility, and Conditional Access.

Key RBAC roles for Key Vault:

| Role | Scope | Actions |
|---|---|---|
| Key Vault Administrator | Control + data plane | Full access to all object types |
| Key Vault Secrets Officer | Data plane | Create, delete, manage secrets |
| Key Vault Secrets User | Data plane | Read secret values |
| Key Vault Crypto Officer | Data plane | Create, delete, manage keys |
| Key Vault Crypto User | Data plane | Use keys for crypto operations |
| Key Vault Certificates Officer | Data plane | Create, manage certificates |
| Key Vault Reader | Control plane | Read vault metadata (not values) |

## Creating a Key Vault

```bash
# Create vault (RBAC model, soft-delete 90 days, purge protection)
az keyvault create \
  --name <vault-name> \
  --resource-group <rg> \
  --location <region> \
  --enable-rbac-authorization true \
  --soft-delete-retention-days 90 \
  --enable-purge-protection true

# Grant yourself Secrets Officer
az role assignment create \
  --assignee <your-object-id> \
  --role "Key Vault Secrets Officer" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name>
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/prod-security-rg/providers/Microsoft.KeyVault/vaults/prod-vault-001",
  "location": "eastus",
  "name": "prod-vault-001",
  "properties": {
    "accessPolicies": [],
    "enablePurgeProtection": true,
    "enableRbacAuthorization": true,
    "enableSoftDelete": true,
    "softDeleteRetentionInDays": 90,
    "tenantId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "sku": {
      "family": "A",
      "name": "standard"
    }
  },
  "resourceGroup": "prod-security-rg",
  "type": "Microsoft.KeyVault/vaults"
}
{
  "canDelegate": false,
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/prod-security-rg/providers/Microsoft.KeyVault/vaults/prod-vault-001/providers/Microsoft.Authorization/roleAssignments/a9f8e7d6-c5b4-a321-9876-543210fedcba",
  "principalId": "f1e2d3c4-b5a6-7890-1234-567890abcdef",
  "principalType": "User",
  "roleDefinitionId": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/providers/Microsoft.Authorization/roleDefinitions/4633458b-17de-408a-b874-0445c86300d1",
  "scope": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/prod-security-rg/providers/Microsoft.KeyVault/vaults/prod-vault-001",
  "type": "Microsoft.Authorization/roleAssignments"
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group exists with `az group list` and use the correct `--resource-group` name.
    **`InvalidObjectId`** — Retrieve your object ID with `az ad signed-in-user show --query id -o tsv` and pass it to `--assignee`.
    **`PrincipalNotFound`** — Wait 15–30 seconds for Azure AD replication to complete before assigning the role, or verify the user exists in your tenant.
## Managing Secrets

```bash
# Create/update a secret
az keyvault secret set \
  --vault-name <vault-name> \
  --name "db-password" \
  --value "S3cur3P@ss!"

# Get a secret value
az keyvault secret show \
  --vault-name <vault-name> \
  --name "db-password" \
  --query value --output tsv

# List all secrets (names only, not values)
az keyvault secret list --vault-name <vault-name> --output table

# Set an expiry date
az keyvault secret set-attributes \
  --vault-name <vault-name> \
  --name "db-password" \
  --expires "2027-01-01T00:00:00Z"

# Delete (soft-delete — recoverable within retention period)
az keyvault secret delete --vault-name <vault-name> --name "db-password"

# List deleted secrets
az keyvault secret list-deleted --vault-name <vault-name>

# Recover a deleted secret
az keyvault secret recover --vault-name <vault-name> --name "db-password"

# Purge permanently (only if purge protection is disabled)
az keyvault secret purge --vault-name <vault-name> --name "db-password"
```


```text title="Expected output"
{
  "attributes": {
    "created": 1704067200,
    "enabled": true,
    "expires": null,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": 1704067200
  },
  "id": "https://prod-vault-01.vault.azure.net/secrets/db-password/a7f2c9e1d4b8f3a6c2e9d1b4f7a3c6e9",
  "name": "db-password",
  "value": null
}
S3cur3P@ss!
Name                 Created On             Expires    Enabled
-------------------  ---------------------  ---------  ---------
db-password          2024-01-01T12:00:00Z   2027-01-01 True
api-key              2023-12-15T08:30:22Z   None       True
tls-cert             2023-11-20T14:15:45Z   2025-06-30 True
...
{
  "attributes": {
    "created": 1704067200,
    "enabled": true,
    "expires": 1799587200,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": 1704153600
  },
  "id": "https://prod-vault-01.vault.azure.net/secrets/db-password/a7f2c9e1d4b8f3a6c2e9d1b4f7a3c6e9",
  "name": "db-password"
}
Request had invalid parameters. (InvalidRequest) : The object is disabled.
Name                 DeletedDate            ScheduledPurgeDate
-------------------  ---------------------  ---------------------
db-password          2024-01-02T10:45:33Z   2024-04-02T10:45:33Z
old-secret           2024-01-01T09:22:11Z   2024-04-01T09:22:11Z
{
  "attributes": {
    "created": 1704067200,
    "enabled": true,
    "expires": 1799587200,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": 1704240000
  },
  "id": "https://prod-vault-01.vault.azure.net/secrets/db-password/a7f2c9e1d4b8f3a6c2e9d1b4f7a3c6e9",
  "name": "db-password"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Vault not found. (VaultNotFound)`** — Verify the vault name is correct and exists in your subscription with `az keyvault list`.
    **`The user, group or application does not have the 'get' permission on the object.`** — Ensure your user or service principal has Key Vault Secret User or Officer role assigned via `az role assignment create`.
    **`Purge is not allowed on this vault because purge protection is enabled.`** — Disable purge protection on the vault with `az keyvault update --name <vault-name> --enable-purge-protection false` before purging.
## Soft Delete and Purge Protection

**Soft delete** — deleted objects are retained for the configured period (7–90 days). The vault and all objects cannot be immediately destroyed; this prevents accidental loss.

**Purge protection** — prevents permanent deletion of soft-deleted objects during the retention period, even by administrators. Mandatory for vaults used with CMK (customer-managed keys) in Azure services.

```bash
# Show soft-delete state
az keyvault show --name <vault-name> --query properties.enableSoftDelete

# Show purge protection state
az keyvault show --name <vault-name> --query properties.enablePurgeProtection
```


```text title="Expected output"
true
true
```

!!! warning "Common errors"
    **`The specified vault does not exist in the specified subscription and resource group.`** — Verify the vault name is correct and you are authenticated to the correct Azure subscription with `az account show`.
    **`Authorization failed for template deployment. The client with object id does not have permission to perform action 'Microsoft.KeyVault/vaults/read' on scope.`** — Ensure your Azure user or service principal has at least Reader role on the Key Vault resource.
## Networking — Private Endpoint

Restrict Key Vault access to a private network:

```bash
# Disable public network access
az keyvault update \
  --name <vault-name> \
  --resource-group <rg> \
  --public-network-access Disabled

# Create private endpoint
az network private-endpoint create \
  --name "<vault-name>-pe" \
  --resource-group <rg> \
  --vnet-name <vnet> \
  --subnet <subnet> \
  --private-connection-resource-id \
    /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name> \
  --group-id vault \
  --connection-name "<vault-name>-connection"
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/prod-vault-kv",
  "name": "prod-vault-kv",
  "properties": {
    "publicNetworkAccess": "Disabled",
    "networkAcls": {
      "bypass": "AzureServices",
      "defaultAction": "Deny"
    }
  }
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.Network/privateEndpoints/prod-vault-kv-pe",
  "name": "prod-vault-kv-pe",
  "resourceGroup": "prod-rg",
  "location": "eastus",
  "privateLinkServiceConnections": [
    {
      "name": "prod-vault-kv-connection",
      "properties": {
        "privateLinkServiceId": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/prod-vault-kv",
        "groupIds": [
          "vault"
        ],
        "provisioningState": "Succeeded"
      }
    }
  ],
  "provisioningState": "Succeeded"
}
```

!!! warning "Common errors"
    **`(BadRequest) The resource with name '<vault-name>' does not exist in the resource group '<rg>'.`** — Verify the vault name and resource group name are correct and the vault exists in the specified region.
    **`(BadRequest) The subnet '<subnet>' does not exist in virtual network '<vnet>'.`** — Confirm the subnet name and virtual network name are spelled correctly and exist in the same resource group and region.
    **`(Conflict) The private endpoint '<vault-name>-pe' already exists in resource group '<rg>'.`** — Delete the existing private endpoint first using `az network private-endpoint delete --name <vault-name>-pe --resource-group <rg>` or use a different endpoint name.
After creating the private endpoint, add a DNS A record in the `privatelink.vaultcore.azure.net` private DNS zone pointing to the private endpoint IP.

## Audit Logging

Enable diagnostic settings to send Key Vault audit logs to Log Analytics:

```bash
az monitor diagnostic-settings create \
  --name "keyvault-audit" \
  --resource /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name> \
  --workspace <log-analytics-workspace-id> \
  --logs '[{"category":"AuditEvent","enabled":true}]'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourcegroups/prod-rg/providers/microsoft.insights/diagnosticsettings/keyvault-audit",
  "identity": null,
  "kind": null,
  "location": null,
  "name": "keyvault-audit",
  "resourceGroup": "prod-rg",
  "storageAccountId": null,
  "tags": null,
  "type": "Microsoft.Insights/diagnosticSettings",
  "workspaceId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourcegroups/prod-rg/providers/microsoft.operationalinsights/workspaces/prod-logs"
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name>' could not be found.`** — Verify the subscription ID, resource group name, and Key Vault name are correct and exist in your Azure account.
    **`InvalidResourceId: The provided resource ID is invalid or malformed.`** — Ensure the resource ID follows the exact format with correct casing for Microsoft.KeyVault and no trailing slashes.
    **`AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'microsoft.insights/diagnosticSettings/write' on resource '<vault-id>'.`** — Grant the user or service principal the "Monitoring Contributor" role on the Key Vault resource.
Query audit logs in Log Analytics:

```kusto
AzureDiagnostics
| where ResourceType == "VAULTS"
| where Category == "AuditEvent"
| project TimeGenerated, OperationName, CallerIPAddress, identity_claim_upn_s, ResultType
| order by TimeGenerated desc
```

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| `Forbidden` when reading a secret | Missing data-plane role (Key Vault Reader is control-plane only) | Assign `Key Vault Secrets User` at vault or secret scope |
| `VaultNotFound` | Vault deleted (soft-delete); or wrong subscription | Check `az keyvault list-deleted`; verify subscription context |
| Cannot purge deleted vault | Purge protection enabled | Wait out the retention period |
| Private endpoint — DNS resolution fails | Private DNS zone not linked to VNet or wrong A record | Verify DNS zone `privatelink.vaultcore.azure.net` is linked and has correct IP |
| Secret access works from VM but not from pipeline | Pipeline identity (SP/managed identity) lacks role assignment | Assign role to the pipeline service principal's object ID |
