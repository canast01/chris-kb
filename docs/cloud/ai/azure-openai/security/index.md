---
tags:
  - security
---
# Azure OpenAI Security

<div class="kb-summary">
Azure OpenAI security covers authentication methods, role-based access control (RBAC), managed identity, customer-managed keys (CMK), and content filtering configuration.

*Applies to: Azure OpenAI*
</div>

```d2
direction: down

external: External / Untrusted {shape: rectangle}
rbac_roles: "RBAC Roles" {shape: rectangle}
managed_identity_authentication: "Managed Identity Authentication" {shape: rectangle}
customermanaged_keys: "Customer-Managed Keys" {shape: rectangle}
content_filters: "Content Filters" {shape: rectangle}
disabling_api_keys: "Disabling API Keys" {shape: rectangle}
security_checklist: "Security Checklist" {shape: rectangle}
core: "Azure OpenAI Core" {shape: hexagon}

external -> rbac_roles: traffic in
rbac_roles -> managed_identity_authentication
managed_identity_authentication -> customermanaged_keys
customermanaged_keys -> content_filters
content_filters -> disabling_api_keys
disabling_api_keys -> security_checklist
security_checklist -> core: secured path
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## RBAC Roles

Azure RBAC roles control who can manage the resource and who can call the API. API keys are an alternative but managed identity is preferred in production.

| Role | Scope | Can Call API | Can Manage Resource |
|---|---|---|---|
| `Cognitive Services OpenAI User` | Resource | Yes (data plane) | No |
| `Cognitive Services OpenAI Contributor` | Resource | Yes | Yes (limited) |
| `Cognitive Services Contributor` | Resource/RG | Yes | Yes (full) |
| `Owner` / `Contributor` | Subscription/RG | Yes | Yes |

```bash
# Assign OpenAI User role to a service principal
az role assignment create \
  --assignee "APP_CLIENT_ID" \
  --role "Cognitive Services OpenAI User" \
  --scope "/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource"
```


```text title="Expected output"
{
  "canDelegate": false,
  "id": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource/providers/Microsoft.Authorization/roleAssignments/a1b2c3d4-e5f6-4a7b-8c9d-e0f1a2b3c4d5",
  "principalId": "f7e6d5c4-b3a2-1098-7654-3210fedcba98",
  "principalType": "ServicePrincipal",
  "roleDefinitionId": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/providers/Microsoft.Authorization/roleDefinitions/5e0bd9bd-7b93-4f28-af87-19fc36ad61ae",
  "scope": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource",
  "type": "Microsoft.Authorization/roleAssignments"
}
```

!!! warning "Common errors"
    **`The provided information does not map to a valid role.`** — Verify the role name is exactly "Cognitive Services OpenAI User" and run `az role definition list --query "[?contains(roleName, 'OpenAI')]"` to confirm availability in your subscription.
    **`The service principal with id <id> does not exist in the directory.`** — Ensure the APP_CLIENT_ID is the correct application (client) ID from the service principal's Azure AD registration, not the object ID.
    **`Authorization failed: User does not have permission to perform action 'Microsoft.Authorization/roleAssignments/write'.`** — Confirm your user account has Owner or User Access Administrator role on the subscription or resource group scope.
## Managed Identity Authentication

Prefer managed identity over API keys — no secrets to rotate or leak.

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential, "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint="https://my-aoai-resource.openai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-02-01"
)

response = client.chat.completions.create(
    model="gpt4o-prod",
    messages=[{"role": "user", "content": "Hello"}]
)
```

`DefaultAzureCredential` automatically uses the system-assigned or user-assigned managed identity when running on Azure, and falls back to developer credentials locally.

## Customer-Managed Keys

CMK encrypts the resource's stored data (fine-tuning datasets, conversation history) with a key you control in Azure Key Vault.

```bash
# Enable CMK on an existing resource
az cognitiveservices account update \
  --name my-aoai-resource \
  --resource-group my-rg \
  --encryption '{
    "keySource": "Microsoft.KeyVault",
    "keyVaultProperties": {
      "keyName": "aoai-cmk",
      "keyVersion": "KEY_VERSION_ID",
      "keyVaultUri": "https://my-keyvault.vault.azure.net"
    }
  }'
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource",
  "name": "my-aoai-resource",
  "type": "Microsoft.CognitiveServices/accounts",
  "location": "eastus",
  "sku": {
    "name": "S0"
  },
  "kind": "OpenAI",
  "properties": {
    "encryption": {
      "keySource": "Microsoft.KeyVault",
      "keyVaultProperties": {
        "keyName": "aoai-cmk",
        "keyVersion": "KEY_VERSION_ID",
        "keyVaultUri": "https://my-keyvault.vault.azure.net"
      }
    },
    "provisioningState": "Succeeded",
    "publicNetworkAccess": "Enabled"
  }
}
```

!!! warning "Common errors"
    **`(InvalidKeyVaultKeyReference) The key vault key reference is invalid.`** — Verify the keyVaultUri, keyName, and keyVersion exist in the specified Key Vault and the Cognitive Services account has "Get", "Wrap Key", and "Unwrap Key" permissions on the key.
    **`(AuthorizationFailed) The client 'user@example.com' with object id '...' does not have authorization to perform action 'Microsoft.CognitiveServices/accounts/write' over scope '...'`** — Ensure your Azure account has the Contributor or Cognitive Services Contributor role on the resource group or subscription.
    **`(KeyVaultAccessDenied) The user, group or application does not have the required permissions to access the key vault.`** — Grant the Cognitive Services account's managed identity access to the Key Vault using `az keyvault set-policy` with key permissions for get, wrapKey, and unwrapKey.
The resource's managed identity must have `Key Vault Crypto User` role on the key vault. CMK cannot be removed once enabled without recreating the resource.

## Content Filters

Content filters are applied automatically but can be customised for specific use cases with an approved configuration request.

```python
# Check content filter results in the response
response = client.chat.completions.create(
    model="gpt4o-prod",
    messages=[{"role": "user", "content": "Write a story about a robot."}]
)

choice = response.choices[0]
if hasattr(choice, "content_filter_results"):
    filters = choice.content_filter_results
    for category, result in filters.items():
        print(f"{category}: filtered={result.filtered}, severity={result.severity}")
```

Default filter thresholds:

| Category | Default Block Threshold |
|---|---|
| Hate | Medium and above |
| Violence | Medium and above |
| Sexual | Medium and above |
| Self-harm | Medium and above |
| Prompt injection | High |

## Disabling API Keys

For maximum security, disable API key authentication entirely and require AAD tokens:

```bash
az cognitiveservices account update \
  --name my-aoai-resource \
  --resource-group my-rg \
  --api-properties disableLocalAuth=true
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource",
  "identity": null,
  "kind": "OpenAI",
  "location": "eastus",
  "name": "my-aoai-resource",
  "properties": {
    "apiProperties": {
      "disableLocalAuth": true
    },
    "callRateLimit": {
      "count": 60,
      "renewalPeriod": 60
    },
    "customSubDomainName": "my-aoai-resource",
    "endpoint": "https://my-aoai-resource.openai.azure.com/",
    "provisioningState": "Succeeded",
    "publicNetworkAccess": "Enabled"
  },
  "resourceGroup": "my-rg",
  "sku": {
    "name": "S0"
  },
  "type": "Microsoft.CognitiveServices/accounts"
}
```

!!! warning "Common errors"
    **`The resource 'my-aoai-resource' under resource group 'my-rg' was not found.`** — Verify the resource name and resource group name are correct using `az cognitiveservices account list --resource-group my-rg`.
    **`InvalidApiProperties: The value of 'disableLocalAuth' must be a boolean.`** — Use `true` or `false` (lowercase, unquoted) in the `--api-properties` parameter.
    **`AuthorizationFailed: The client 'user@example.com' with object id '...' does not have authorization to perform action 'Microsoft.CognitiveServices/accounts/write' over scope '...'.`** — Ensure your user account has the Contributor or Cognitive Services Contributor role on the resource group.
After this change, all callers must use an AAD token — API keys will return 401.

## Security Checklist

| Control | Recommended Setting |
|---|---|
| Authentication | Managed identity (disable API keys) |
| Network | Private endpoint + public access disabled |
| Encryption | CMK for regulated data |
| Audit logging | Diagnostic settings to Log Analytics |
| RBAC | Least-privilege per team/service |
| Content filters | Tuned per use case, never fully disabled |
