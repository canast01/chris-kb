---
tags:
  - aws
  - ai
description: "AWS Bedrock requires explicit model access to be enabled per AWS account and region. Models are not available by default. This page covers enabling..."
---
# Bedrock Model Access

<div class="kb-summary">
AWS Bedrock requires explicit model access to be enabled per AWS account and region. Models are not available by default. This page covers enabling models, throughput modes, and quota management.

*Applies to: AWS Bedrock*
</div>

```d2
direction: down

enabling_model_access: "Enabling Model Access" {shape: rectangle}
ondemand_vs_provisioned_throughput: "On-Demand vs Provisioned Throughput" {shape: rectangle}
provisioned_throughput_setup: "Provisioned Throughput Setup" {shape: rectangle}
invoking_models: "Invoking Models" {shape: rectangle}
service_quotas: "Service Quotas" {shape: rectangle}
crossregion_inference_profiles: "Cross-Region Inference Profiles" {shape: rectangle}

enabling_model_access -> ondemand_vs_provisioned_throughput: uses
ondemand_vs_provisioned_throughput -> provisioned_throughput_setup: uses
provisioned_throughput_setup -> invoking_models: uses
invoking_models -> service_quotas: uses
service_quotas -> crossregion_inference_profiles: uses
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


```text title="Expected output"
---------------------------------------------------------------------------------------------------------
|                                    modelSummaries                                                    |
|-----------|-----------------------------------------------------|------------|
| id        | provider                                              | status     |
|-----------|-----------------------------------------------------|------------|
| anthropic.claude-3-5-sonnet-20241022-v2:0 | Anthropic                                             | ACTIVE     |
| anthropic.claude-3-opus-20250219-v1:0     | Anthropic                                             | ACTIVE     |
| meta.llama3-1-405b-instruct-v1:0           | Meta                                                  | ACTIVE     |
| mistral.mistral-7b-instruct-v0:2            | Mistral AI                                            | ACTIVE     |
| cohere.command-r-plus-v1:0                 | Cohere                                                | ACTIVE     |
---------------------------------------------------------------------------------------------------------

{
    "modelDetails": {
        "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "modelName": "Claude 3.5 Sonnet",
        "providerName": "Anthropic",
        "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
        "inputTokenCount": 200000,
        "outputTokenCount": 4096,
        "modelLifecycle": {
            "status": "ACTIVE"
        }
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (AccessDeniedException) when calling the ListFoundationModels operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: bedrock:ListFoundationModels` | Add `bedrock:ListFoundationModels` permission to the IAM user or role policy. |
    | `An error occurred (ValidationException) when calling the GetFoundationModel operation: Could not find model with identifier anthropic.claude-3-5-sonnet-20241022-v2:0` | Verify the exact model identifier using `list-foundation-models` and ensure the model is available in your region. |
    | `An error occurred (ThrottlingException) when calling the ListFoundationModels operation: Rate exceeded` | Wait a few seconds before retrying the command, or implement exponential backoff in automation scripts. |
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


```text title="Expected output"
{
    "provisionedModelArn": "arn:aws:bedrock:us-east-1:123456789012:provisioned-model/prod-claude-sonnet",
    "provisionedModelName": "prod-claude-sonnet",
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "modelUnits": 2,
    "commitmentDuration": "SixMonths",
    "creationTime": "2024-01-15T14:32:47.123Z",
    "status": "Creating"
}
"arn:aws:bedrock:us-east-1:123456789012:provisioned-model/prod-claude-sonnet"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationException) when calling the CreateProvisionedModelThroughput operation: Model anthropic.claude-3-sonnet-20240229-v1:0 is not available in region us-east-1` | Verify the model ID is available in your region using `aws bedrock list-foundation-models --region us-east-1` and update the model-id parameter. |
    | `An error occurred (AccessDeniedException) when calling the CreateProvisionedModelThroughput operation: User is not authorized to perform bedrock:CreateProvisionedModelThroughput` | Add the `bedrock:CreateProvisionedModelThroughput` permission to your IAM user or role policy. |
    | `An error occurred (ResourceNotFoundException) when calling the GetProvisionedModelThroughput operation: Could not find provisioned model with id prod-claude-sonnet` | Wait 30-60 seconds for the provisioned model creation to complete before querying it, or verify the provisioned-model-id matches the provisioned-model-name from creation. |
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


```text title="Expected output"
---------------------------------------------------------------------------------------------------------
|                                          ListServiceQuotas                                            |
+----------------------------------------+----------------------------------------------------------+
| Name                                   | Value                                                    |
+----------------------------------------+----------------------------------------------------------+
| Batch inference jobs per account       | 100                                                      |
| Concurrent inference units (on-demand) | 1                                                        |
| Model invocations per second           | 100                                                      |
| Custom models per account              | 10                                                       |
| Provisioned throughput per account     | 0                                                        |
+----------------------------------------+----------------------------------------------------------+

{
    "RequestedQuotaChangeInfo": {
        "Id": "qr-1a2b3c4d5e6f7g8h9",
        "ServiceCode": "bedrock",
        "QuotaCode": "L-XXXXXXXX",
        "QuotaName": "Model invocations per second",
        "DesiredValue": 100000.0,
        "Status": "PENDING",
        "CreatedDate": "2024-01-15T14:32:18.456000+00:00"
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (AccessDenied) when calling the ListServiceQuotas operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: servicequotas:ListServiceQuotas` | Add the `servicequotas:ListServiceQuotas` and `servicequotas:RequestServiceQuotaIncrease` permissions to the IAM user or role. |
    | `An error occurred (InvalidParameterException) when calling the RequestServiceQuotaIncrease operation: Invalid quota code: L-XXXXXXXX` | Replace `L-XXXXXXXX` with the actual quota code from the list output (e.g., `L-4B902E5D`). |
    | `An error occurred (QuotaExceededException) when calling the RequestServiceQuotaIncrease operation: You have reached the maximum number of quota increase requests` | Wait for pending quota requests to complete or be denied before submitting new ones. |
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


```text title="Expected output"
{
    "body": {
        "type": "text",
        "text": "Hello! I'm Claude, an AI assistant made by Anthropic. How can I help you today?"
    },
    "contentType": "application/json",
    "httpStatusCode": 200
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationException) when calling the InvokeModel operation: Could not validate the provided model identifier` | Verify the model ID is correct and available in your region with `aws bedrock list-foundation-models --region us-east-1`. |
    | `An error occurred (AccessDeniedException) when calling the InvokeModel operation: User is not authorized to perform: bedrock:InvokeModel` | Add the `bedrock:InvokeModel` permission to your IAM user or role policy. |
The `us.` prefix denotes the US cross-region inference profile. Use `eu.` for Europe and `ap.` for Asia-Pacific.
