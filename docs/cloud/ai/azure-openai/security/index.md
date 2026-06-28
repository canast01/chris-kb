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
