# Azure OpenAI

<div class="kb-summary">
Azure OpenAI Service hosts GPT-4o and other models within Azure regions with private endpoints, Entra ID auth, and regional data residency. Models must be explicitly deployed before use; coverage includes deployment quota, Standard vs PTU capacity, network isolation, content filtering, and monitoring.
</div>
```text
┌─────────────────────────────────────────── Ai Azure Openai ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Azure Openai: Ai Azure Openai platform                            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                         Management: Ai Azure Openai management console                        │   │
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
│    Physical: Ai Azure Openai infrastructure · management network · monitoring                         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure Openai       = Ai Azure Openai platform overview and core concepts                           │
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


<div class="kb-grid kb-grid-5">

<a class="kb-card" href="deployments/">
  <strong>Deployments</strong>
  <span>Creating and managing model deployments — Standard vs Provisioned Throughput Units (PTU), quota allocation, and deployment versioning.</span>
</a>

<a class="kb-card" href="model-access/">
  <strong>Model Access</strong>
  <span>Requesting model access per region, supported model versions, availability by geography, and capacity planning.</span>
</a>

<a class="kb-card" href="networking/">
  <strong>Networking</strong>
  <span>Private Endpoint configuration, VNet integration, disabling public network access, and DNS resolution for private endpoints.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Entra ID managed identity auth, API key rotation, content filtering policy, prompt shield, and RBAC role assignments.</span>
</a>

<a class="kb-card" href="monitoring/">
  <strong>Monitoring</strong>
  <span>Azure Monitor diagnostic settings, Log Analytics queries for token usage and latency, alerting on error rates and quota exhaustion.</span>
</a>

</div>

## Quick Reference

### Deployment Types

| Type | Capacity | Billing | Best For |
|---|---|---|---|
| Standard | Shared pool, auto-scaled | Per token | Variable workloads, dev/test |
| Provisioned (PTU) | Dedicated throughput units | Reserved hourly | Latency-sensitive, high-volume production |

### Key Configuration Values

| Parameter | Value / Notes |
|---|---|
| Base endpoint | `https://{resource-name}.openai.azure.com/` |
| API version (stable) | `2024-02-01` |
| Auth — API key | `api-key: {key}` header |
| Auth — Entra ID | Bearer token from `DefaultAzureCredential` |
| Deployment name | Set at resource creation; used in URL path |
| Quota unit | TPM (tokens per minute) per deployment |

### Content Filter Categories

| Category | Severities | Default Action |
|---|---|---|
| Violence | Low / Medium / High | Block at High |
| Sexual | Low / Medium / High | Block at High |
| Self-harm | Low / Medium / High | Block at High |
| Hate / Fairness | Low / Medium / High | Block at High |
| Prompt Shield | Jailbreak / Indirect attack | Block |

## Common Operations

```bash
# Set environment variables
export AZURE_OPENAI_ENDPOINT="https://my-resource.openai.azure.com/"
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"
export OPENAI_API_VERSION="2024-02-01"

# Chat completion via REST
curl "${AZURE_OPENAI_ENDPOINT}openai/deployments/${AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=${OPENAI_API_VERSION}" \
  -H "api-key: ${AZURE_OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Explain PTU deployments."}]
  }'

# List deployments via Azure CLI
az cognitiveservices account deployment list \
  --name my-resource \
  --resource-group my-rg \
  --output table

# Check quota usage
az cognitiveservices account list-usage \
  --name my-resource \
  --resource-group my-rg
```

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Option 1: API key auth
client = AzureOpenAI(
    azure_endpoint="https://my-resource.openai.azure.com/",
    api_key="...",
    api_version="2024-02-01"
)

# Option 2: Managed identity (preferred for production)
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)
client = AzureOpenAI(
    azure_endpoint="https://my-resource.openai.azure.com/",
    azure_ad_token_provider=token_provider,
    api_version="2024-02-01"
)

response = client.chat.completions.create(
    model="gpt-4o",          # deployment name, not model name
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

```python
# Log Analytics — KQL query for token usage over 1 hour
# Run in Azure Monitor > Logs against your Log Analytics workspace
AzureDiagnostics
| where ResourceType == "OPENAI"
| where TimeGenerated > ago(1h)
| summarize TotalTokens = sum(toint(promptTokens_d) + toint(completionTokens_d))
    by bin(TimeGenerated, 5m), deploymentId_s
| order by TimeGenerated desc
```

## Key Considerations

- **Deployment ≠ model:** You deploy a model version to a named deployment. API calls reference the deployment name, not the model name. Changing the underlying model version requires creating a new deployment or updating the existing one.
- **PTU vs Standard:** Standard is billed per token and scales automatically but can be rate-limited under burst load. PTU (Provisioned Throughput Units) gives consistent latency and throughput but requires capacity reservation — right-size carefully as PTU is billed hourly regardless of usage.
- **Network isolation:** For production, disable public network access and use Private Endpoints. Ensure DNS resolution is configured so workloads resolve the private endpoint IP, not the public Azure IP.
- **Managed identity over API keys:** Use `DefaultAzureCredential` with a managed identity assigned the `Cognitive Services OpenAI User` role. This eliminates key rotation overhead and reduces the risk of credential leakage.
- **Content filtering:** Default filters block high-severity content. Customising filters (e.g., lowering thresholds for certain categories) requires an approved use-case request to Microsoft. Enable Prompt Shield to detect jailbreak and indirect injection attempts.
- **Monitoring gaps:** Azure Monitor captures token counts and latency but not the full prompt/response content by default. Enable diagnostic logging to Log Analytics and build alerts on `4xx` error rates and TPM quota consumption to catch quota exhaustion before it impacts production.
