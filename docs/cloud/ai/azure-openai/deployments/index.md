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
```text
┌───────────────────────────────────── Ai Azure Openai Deployments ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                       Azure Openai: Ai Azure Openai Deployments platform                      │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Ai Azure Openai Deployments management console                  │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Ai Azure Openai Deployments infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure Openai       = Ai Azure Openai Deployments platform overview and core concepts               │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

## Common Deployment Issues

| Issue | Cause | Fix |
|---|---|---|
| `DeploymentNotFound` | Wrong deployment name in code | Check exact name via portal or CLI |
| Quota exceeded on creation | Insufficient regional TPM quota | Request quota increase in Azure Portal |
| PTU commitment not available | Region doesn't support PTU for that model | Check model availability matrix |
| 429 on Standard deployment | Shared quota exhausted | Add retry with exponential backoff or use PTU |
