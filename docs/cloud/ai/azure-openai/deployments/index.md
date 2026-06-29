---
tags:
  - azure
  - ai
---
# Azure OpenAI Deployments

<div class="kb-summary">
Azure OpenAI requires you to deploy a model before use — the model version, deployment name, and capacity all affect availability and cost. This page covers creating deployments, capacity planning, and PTU vs consumption billing.

*Applies to: Azure OpenAI*
</div>

```d2
direction: down

creating_a_deployment: "Creating a Deployment" {shape: rectangle}
deployment_types_consumption_vs_ptu: "Deployment Types: Consumption vs PTU" {shape: rectangle}
capacity_planning: "Capacity Planning" {shape: rectangle}
deployment_names: "Deployment Names" {shape: rectangle}
updating_and_deleting_deployments: "Updating and Deleting Deployments" {shape: rectangle}
common_deployment_issues: "Common Deployment Issues" {shape: rectangle}

creating_a_deployment -> deployment_types_consumption_vs_ptu: uses
deployment_types_consumption_vs_ptu -> capacity_planning: uses
capacity_planning -> deployment_names: uses
deployment_names -> updating_and_deleting_deployments: uses
updating_and_deleting_deployments -> common_deployment_issues: uses
```

## Creating a Deployment

Deployments are created per Azure OpenAI resource (which is region-scoped). The deployment name is what your application references in API calls.

```bash
# Using the Azure CLI with the cognitive services extension
az cognitiveservices account deployment create \
  --name my-aoai-resource \
  --resource-group my-rg \
  --deployment-name gpt4o-prod \
  --model-name gpt-4o \
  --model-version "2024-11-20" \
  --model-format OpenAI \
  --sku-capacity 100 \
  --sku-name "Standard"
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource/deployments/gpt4o-prod",
  "name": "gpt4o-prod",
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "gpt-4o",
      "version": "2024-11-20"
    },
    "provisioningState": "Succeeded",
    "raiPolicyId": null,
    "scaleSettings": {
      "capacity": 100,
      "scaleType": "Standard"
    }
  },
  "systemData": {
    "createdAt": "2024-12-19T14:32:18.456789+00:00",
    "createdBy": "user@example.com",
    "createdByType": "User",
    "lastModifiedAt": "2024-12-19T14:32:18.456789+00:00"
  },
  "type": "Microsoft.CognitiveServices/accounts/deployments"
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The resource 'Microsoft.CognitiveServices/accounts/my-aoai-resource' under resource group 'my-rg' was not found.`** — Verify the resource name and resource group exist with `az cognitiveservices account show --name my-aoai-resource --resource-group my-rg`.
    **`(InvalidParameter) The model version '2024-11-20' is not available for model 'gpt-4o'.`** — Check available versions with `az cognitiveservices model list --location eastus` and use a supported version.
    **`(QuotaExceeded) Quota exceeded for deployment capacity. Current quota: 50, requested: 100.`** — Reduce `--sku-capacity` to a value within your quota or request a quota increase in the Azure portal.
Or via the REST API:

```bash
curl -X PUT \
  "https://management.azure.com/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource/deployments/gpt4o-prod?api-version=2023-05-01" \
  -H "Authorization: Bearer $(az account get-access-token --query accessToken -o tsv)" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": {"name": "Standard", "capacity": 100},
    "properties": {
      "model": {"format": "OpenAI", "name": "gpt-4o", "version": "2024-11-20"}
    }
  }'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource/deployments/gpt4o-prod",
  "name": "gpt4o-prod",
  "type": "Microsoft.CognitiveServices/accounts/deployments",
  "sku": {
    "name": "Standard",
    "capacity": 100
  },
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "gpt-4o",
      "version": "2024-11-20"
    },
    "provisioningState": "Succeeded",
    "capabilities": {
      "chat_completion": true,
      "embeddings": false
    }
  }
}
```

!!! warning "Common errors"
    **`"error":{"code":"InvalidAuthenticationTokenTenant","message":"The access token is from the wrong tenant."}`** — Ensure your Azure CLI is logged into the correct tenant with `az account set --subscription SUB_ID`.
    **`"error":{"code":"DeploymentQuotaExceeded","message":"Quota exceeded for deployment capacity in this region."}`** — Reduce the capacity value or request a quota increase through the Azure portal for your cognitive services account.
    **`"error":{"code":"ModelNotFound","message":"The model 'gpt-4o' version '2024-11-20' is not available in this region."}`** — Verify model availability in your region and use a supported version with `az cognitiveservices account deployment create --help`.
## Deployment Types: Consumption vs PTU

| Type | Billing | Latency | Quota | Best For |
|---|---|---|---|---|
| Standard (consumption) | Per 1K tokens | Variable | Shared regional pool | Dev, variable traffic |
| Provisioned (PTU) | Per PTU/hour | Consistent | Dedicated | Production, high volume |
| Global Standard | Per 1K tokens | Variable | Global pool | Burst capacity |
| Global Provisioned | Per PTU/hour | Consistent | Global | Global low-latency prod |

PTU (Provisioned Throughput Units) are purchased in increments and guarantee a tokens-per-minute rate that scales linearly with PTU count.

## Capacity Planning

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://my-aoai-resource.openai.azure.com",
    api_key="YOUR_API_KEY",
    api_version="2024-02-01"
)

# List existing deployments
import httpx, os

response = httpx.get(
    f"https://my-aoai-resource.openai.azure.com/openai/deployments?api-version=2024-02-01",
    headers={"api-key": os.environ["AZURE_OPENAI_API_KEY"]}
)
for dep in response.json()["data"]:
    print(dep["id"], dep["model"], dep["scale_settings"])
```

## Deployment Names

The deployment name is arbitrary and decoupled from the model name. Use descriptive names that include environment and purpose.

| Deployment Name Pattern | Example |
|---|---|
| `{model}-{env}` | `gpt4o-prod`, `gpt4o-dev` |
| `{purpose}-{env}` | `summariser-prod`, `classifier-staging` |
| `{team}-{model}-{version}` | `platform-gpt4o-nov24` |

Reference by deployment name in API calls:

```python
response = client.chat.completions.create(
    model="gpt4o-prod",   # deployment name, not model name
    messages=[{"role": "user", "content": "Summarise this text."}],
    max_tokens=512
)
```

## Updating and Deleting Deployments

```bash
# Scale capacity up
az cognitiveservices account deployment update \
  --name my-aoai-resource \
  --resource-group my-rg \
  --deployment-name gpt4o-prod \
  --capacity 200

# Delete a deployment (stops billing immediately)
az cognitiveservices account deployment delete \
  --name my-aoai-resource \
  --resource-group my-rg \
  --deployment-name gpt4o-old
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource/deployments/gpt4o-prod",
  "name": "gpt4o-prod",
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "gpt-4o",
      "version": "2024-08-06"
    },
    "scaleSettings": {
      "scaleType": "Standard",
      "capacity": 200
    },
    "raiPolicyName": null,
    "versionUpgradeOption": "OnceNewDefaultVersionAvailable"
  },
  "systemData": {
    "createdAt": "2024-01-15T10:22:33.456789Z",
    "lastModifiedAt": "2024-01-20T14:47:12.123456Z"
  }
}
Are you sure you want to perform this delete operation on deployment 'gpt4o-old'? (y/n): y
(Deployment deleted successfully)
```

!!! warning "Common errors"
    **`(ResourceNotFound) The resource 'gpt4o-prod' does not exist in resource group 'my-rg'.`** — Verify the deployment name matches exactly with `az cognitiveservices account deployment list --name my-aoai-resource --resource-group my-rg`.
    **`(AuthorizationFailed) The client 'user@example.com' with object id 'xxx' does not have authorization to perform action 'Microsoft.CognitiveServices/accounts/deployments/write' over scope '/subscriptions/xxx/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource'.`** — Ensure your Azure account has Contributor or Cognitive Services User role assigned on the resource group or subscription.
## Common Deployment Issues

| Issue | Cause | Fix |
|---|---|---|
| `DeploymentNotFound` | Wrong deployment name in code | Check exact name via portal or CLI |
| Quota exceeded on creation | Insufficient regional TPM quota | Request quota increase in Azure Portal |
| PTU commitment not available | Region doesn't support PTU for that model | Check model availability matrix |
| 429 on Standard deployment | Shared quota exhausted | Add retry with exponential backoff or use PTU |
