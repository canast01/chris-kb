# Azure OpenAI Model Access


<div class="kb-summary">
Azure OpenAI model availability varies by region and subscription tier. Some models require explicit access approval. This page covers checking availability, requesting quota, and managing rate limits.

*Applies to: Azure OpenAI*
</div>
```text
┌──────────────────────────────────── Ai Azure Openai Model Access ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Azure Openai: Ai Azure Openai Model Access platform                      │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                  Management: Ai Azure Openai Model Access management console                  │   │
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
│    Physical: Ai Azure Openai Model Access infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure Openai       = Ai Azure Openai Model Access platform overview and core concepts              │
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


## Model Availability by Region

Not all models are available in all regions. Use the Azure portal or CLI to list available models for your resource's region.

```bash
# List models available in a region
az cognitiveservices account list-models \
  --name my-aoai-resource \
  --resource-group my-rg \
  --output table

# Or via REST
curl -s \
  "https://management.azure.com/subscriptions/SUB_ID/providers/Microsoft.CognitiveServices/locations/eastus/models?api-version=2023-05-01" \
  -H "Authorization: Bearer $(az account get-access-token --query accessToken -o tsv)" \
  | jq '.value[] | select(.kind=="OpenAI") | {name:.model.name, version:.model.version, capacity:.model.maxCapacity}'
```

Key models and typical regional availability (as of early 2026):

| Model | Generally Available Regions |
|---|---|
| gpt-4o (2024-11-20) | eastus, eastus2, swedencentral, westus, westus3 |
| gpt-4o-mini | eastus, eastus2, swedencentral, westeurope |
| o1 | eastus2, swedencentral |
| o3-mini | eastus, eastus2, swedencentral |
| text-embedding-3-large | Most regions |

## Requesting Access for Gated Models

Some models (e.g., o1, GPT-4o fine-tuning) require a request form. Submit via the Azure OpenAI Limited Access portal. Access is typically granted within 1–5 business days.

For standard models, access is automatic once you have an Azure OpenAI resource in a supported region.

## Quota and Rate Limits

Quota is expressed in Tokens Per Minute (TPM) per model per region, shared across all Standard deployments of that model in the region.

```bash
# Check current quota usage
az cognitiveservices usage list \
  --location eastus \
  --query "[?contains(name.value,'OpenAI')]" \
  --output table

# Request a quota increase via REST
curl -X PUT \
  "https://management.azure.com/subscriptions/SUB_ID/providers/Microsoft.CognitiveServices/locations/eastus/commitmentPlans/gpt-4o-quota?api-version=2023-05-01" \
  -H "Authorization: Bearer $(az account get-access-token --query accessToken -o tsv)" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"hostingModel":"Web","planType":"ProvisionedManaged","current":{"tier":"T1","count":1}}}'
```

## Rate Limit Headers

The API returns rate limit info in response headers. Log these to detect approaching limits before 429s occur.

```python
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-02-01"
)

# Access raw HTTP response to read headers
with client.chat.completions.with_raw_response.create(
    model="gpt4o-prod",
    messages=[{"role": "user", "content": "Hello"}]
) as response:
    print("Remaining requests:", response.headers.get("x-ratelimit-remaining-requests"))
    print("Remaining tokens:", response.headers.get("x-ratelimit-remaining-tokens"))
    print("Reset time:", response.headers.get("x-ratelimit-reset-requests"))
    completion = response.parse()
```

## Multi-Region Strategy

Distribute load across regions to increase effective quota and improve resilience.

```python
import random
from openai import AzureOpenAI

ENDPOINTS = [
    {"endpoint": "https://aoai-eastus.openai.azure.com", "key": "KEY_EASTUS"},
    {"endpoint": "https://aoai-swedencentral.openai.azure.com", "key": "KEY_SWEDEN"},
]

def get_client():
    ep = random.choice(ENDPOINTS)
    return AzureOpenAI(
        azure_endpoint=ep["endpoint"],
        api_key=ep["key"],
        api_version="2024-02-01"
    )
```

## Common Access Issues

| Error | Meaning | Resolution |
|---|---|---|
| `ResourceNotFound` | Model not deployed | Create deployment in the resource |
| `PermissionDenied` | No access to model family | Submit access request form |
| `QuotaExceeded` | Regional TPM limit reached | Request quota increase or add region |
| `ModelVersionRetired` | Using old API version | Update to a supported model version |
