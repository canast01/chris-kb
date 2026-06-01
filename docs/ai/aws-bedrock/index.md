# AWS Bedrock

<div class="kb-summary">
AWS Bedrock is a fully managed serverless service for invoking foundation models (Anthropic, Meta, Mistral, Amazon) without managing inference infrastructure. Coverage includes model access enablement, IAM policy design, Provisioned Throughput vs on-demand pricing, Knowledge Bases (RAG), Agents, and monitoring.
</div>
```text
┌─────────────────────────────────────────── Ai Aws Bedrock ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Aws Bedrock: Ai Aws Bedrock platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                         Management: Ai Aws Bedrock management console                         │   │
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
│    Physical: Ai Aws Bedrock infrastructure · management network · monitoring                          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Aws Bedrock        = Ai Aws Bedrock platform overview and core concepts                            │
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

<a class="kb-card" href="model-access/">
  <strong>Model Access</strong>
  <span>Requesting model access in the Bedrock console, supported model providers, regional availability, and model IDs for API calls.</span>
</a>

<a class="kb-card" href="knowledge-bases/">
  <strong>Knowledge Bases</strong>
  <span>RAG pipeline setup — S3 data source, chunking strategy, embedding models, OpenSearch Serverless vector store, and retrieval configuration.</span>
</a>

<a class="kb-card" href="agents/">
  <strong>Agents</strong>
  <span>Multi-step reasoning with tool use — action groups, Lambda function integration, knowledge base attachment, and session management.</span>
</a>

<a class="kb-card" href="monitoring/">
  <strong>Monitoring</strong>
  <span>CloudWatch metrics for invocation counts, latency, and errors; CloudTrail for API audit; model invocation logging to S3 or CloudWatch Logs.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>IAM resource-based policies, VPC endpoints for private access, CloudTrail logging, guardrails for content filtering, and data encryption.</span>
</a>

</div>

## Quick Reference

### Supported Model Providers and Model IDs

| Provider | Model | Model ID |
|---|---|---|
| Anthropic | Claude 3.5 Sonnet | `anthropic.claude-3-5-sonnet-20241022-v2:0` |
| Anthropic | Claude 3 Haiku | `anthropic.claude-3-haiku-20240307-v1:0` |
| Anthropic | Claude 3 Opus | `anthropic.claude-3-opus-20240229-v1:0` |
| Meta | Llama 3.1 70B Instruct | `meta.llama3-1-70b-instruct-v1:0` |
| Mistral | Mistral Large | `mistral.mistral-large-2402-v1:0` |
| Amazon | Titan Text G1 Express | `amazon.titan-text-express-v1` |
| Amazon | Titan Embeddings V2 | `amazon.titan-embed-text-v2:0` |
| Stability AI | Stable Diffusion XL | `stability.stable-diffusion-xl-v1` |

### Pricing Models

| Mode | Billing | Use Case |
|---|---|---|
| On-demand | Per input/output token | Variable workloads, development |
| Provisioned Throughput | Model units, hourly commitment | Consistent high-volume inference |
| Batch inference | Per token, async | Large offline processing jobs |

## Common Operations

```python
import boto3
import json

# Client uses IAM credentials from environment / instance role
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Invoke Claude 3.5 Sonnet (Messages API format)
response = bedrock.invoke_model(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    contentType="application/json",
    accept="application/json",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Explain AWS Bedrock Provisioned Throughput."}
        ]
    })
)
result = json.loads(response["body"].read())
print(result["content"][0]["text"])

# Streaming response
response = bedrock.invoke_model_with_response_stream(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "Hello"}]
    })
)
for event in response["body"]:
    chunk = json.loads(event["chunk"]["bytes"])
    if chunk.get("type") == "content_block_delta":
        print(chunk["delta"]["text"], end="", flush=True)
```

```bash
# Check which models you have access to
aws bedrock list-foundation-models \
  --region us-east-1 \
  --query 'modelSummaries[?modelLifecycle.status==`ACTIVE`].[modelId,modelName]' \
  --output table

# Request model access (opens browser — do this in console, not CLI)
# AWS Console → Bedrock → Model access → Request access

# Invoke a model via AWS CLI
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-haiku-20240307-v1:0 \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":256,"messages":[{"role":"user","content":"Hello"}]}' \
  --cli-binary-format raw-in-base64-out \
  response.json && cat response.json

# List Knowledge Bases
aws bedrock-agent list-knowledge-bases --region us-east-1 --output table

# List Bedrock Agents
aws bedrock-agent list-agents --region us-east-1 --output table

# Enable model invocation logging (sends logs to CloudWatch)
aws bedrock put-model-invocation-logging-configuration \
  --logging-config '{"cloudWatchConfig":{"logGroupName":"/aws/bedrock/invocations","roleArn":"arn:aws:iam::123456789012:role/BedrockLoggingRole"}}'
```

## Key Considerations

- **Model access is not automatic:** Each model must be individually enabled in the Bedrock console per AWS account per region. Access requests are usually approved instantly for most models, but some (e.g., Llama) may require a brief wait. Automation pipelines will fail with `AccessDeniedException` if model access is not enabled.
- **IAM is the only auth mechanism:** There are no API keys. All calls are SigV4-signed using an IAM identity. Scope permissions using `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` with resource ARN conditions to restrict which models a role can call.
- **Regional availability varies:** Not all models are available in all regions. Claude models are typically available in `us-east-1`, `us-west-2`, and `eu-west-1`. Verify availability before designing a multi-region architecture.
- **On-demand vs Provisioned Throughput:** On-demand is subject to service quotas and burst limits — use Provisioned Throughput (model units) for production workloads with predictable traffic patterns. PTU is billed per hour even at zero usage, so right-size before committing.
- **Knowledge Base chunking strategy matters:** Default fixed-size chunking (300 tokens, 20% overlap) works for general text. For structured documents or code, consider hierarchical chunking or semantic chunking to improve retrieval quality.
- **CloudTrail for compliance:** Enable CloudTrail in all regions where Bedrock is used. Model invocation logging (separate from CloudTrail) captures the actual prompts and responses — route these to S3 with appropriate bucket policies and retention rules if required for audit.
