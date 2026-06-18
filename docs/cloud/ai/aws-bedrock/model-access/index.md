---
tags:
  - aws
  - ai
---
# Bedrock Model Access


<div class="kb-summary">
AWS Bedrock requires explicit model access to be enabled per AWS account and region. Models are not available by default. This page covers enabling models, throughput modes, and quota management.

*Applies to: AWS Bedrock*
</div>
```text
┌───────────────────────────────────── Ai Aws Bedrock Model Access ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                       Aws Bedrock: Ai Aws Bedrock Model Access platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Ai Aws Bedrock Model Access management console                  │   │
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
│    Physical: Ai Aws Bedrock Model Access infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Aws Bedrock        = Ai Aws Bedrock Model Access platform overview and core concepts               │
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


## Enabling Model Access

Model access is granted through the Bedrock console under **Model access** or via the API. Access requests for third-party models (Anthropic, Meta, Mistral) may take minutes to hours depending on the provider.

```bash
# List models and their access status
aws bedrock list-foundation-models \
  --query 'modelSummaries[*].{id:modelId,provider:providerName,status:modelLifecycle.status}' \
  --output table \
  --region us-east-1

# Check access status for a specific model
aws bedrock get-foundation-model \
  --model-identifier "anthropic.claude-3-5-sonnet-20241022-v2:0" \
  --region us-east-1
```

Access is per-region. A model enabled in `us-east-1` is not automatically available in `eu-west-1`.

## On-Demand vs Provisioned Throughput

| Mode | Description | Billing | Use Case |
|---|---|---|---|
| On-Demand | Pay per input/output token, no commitment | Per token | Development, variable workloads |
| Provisioned Throughput | Reserved model units (MU), guaranteed capacity | Per hour (committed) | Production, latency-sensitive |
| Cross-Region Inference | Routes to nearest available region | Per token + small surcharge | High availability |

For production workloads with predictable traffic, Provisioned Throughput avoids throttling and provides consistent latency.

## Provisioned Throughput Setup

```bash
# Create a provisioned throughput commitment
aws bedrock create-provisioned-model-throughput \
  --provisioned-model-name "prod-claude-sonnet" \
  --model-id "anthropic.claude-3-sonnet-20240229-v1:0" \
  --model-units 2 \
  --commitment-duration "SixMonths" \
  --region us-east-1

# Get the provisioned model ARN for use in InvokeModel calls
aws bedrock get-provisioned-model-throughput \
  --provisioned-model-id "prod-claude-sonnet" \
  --region us-east-1 \
  --query 'provisionedModelArn'
```

Each Model Unit provides a defined tokens-per-minute (TPM) rate that varies by model. Check the Bedrock pricing page for current MU rates.

## Invoking Models

```python
import boto3, json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# On-demand invocation
response = bedrock.invoke_model(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Summarise this document."}]
    }),
    contentType="application/json",
    accept="application/json"
)

result = json.loads(response["body"].read())
print(result["content"][0]["text"])
```

## Service Quotas

Default quotas are conservative. Request increases through the Service Quotas console.

```bash
# List current Bedrock quotas
aws service-quotas list-service-quotas \
  --service-code bedrock \
  --query 'Quotas[*].{Name:QuotaName,Value:Value}' \
  --output table

# Request a quota increase
aws service-quotas request-service-quota-increase \
  --service-code bedrock \
  --quota-code L-XXXXXXXX \
  --desired-value 100000
```

Key quotas to monitor: `InvokeModel` requests per minute (RPM) and tokens per minute (TPM) per model.

## Cross-Region Inference Profiles

Use inference profiles to route to the nearest region automatically:

```bash
aws bedrock invoke-model \
  --model-id "us.anthropic.claude-3-5-sonnet-20241022-v2:0" \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":512,"messages":[{"role":"user","content":"Hello"}]}' \
  --region us-east-1 \
  output.json
```

The `us.` prefix denotes the US cross-region inference profile. Use `eu.` for Europe and `ap.` for Asia-Pacific.
