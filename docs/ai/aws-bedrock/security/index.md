# Bedrock Security


<div class="kb-summary">
Security for Bedrock spans IAM access control, network isolation with VPC endpoints, encryption at rest and in transit, and content guardrails. Apply all layers for production deployments handling sensitive data.
</div>

## IAM Policies

Follow least-privilege: grant only the model IDs and actions required for each workload.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificModelInvoke",
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
      ]
    },
    {
      "Sid": "DenyAllOtherModels",
      "Effect": "Deny",
      "Action": "bedrock:InvokeModel",
      "NotResource": [
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
      ]
    }
  ]
}
```

Agent execution roles additionally need `bedrock:InvokeAgent` and permissions for any downstream services (Lambda, S3, DynamoDB).

## VPC Endpoints

Use interface VPC endpoints to keep traffic off the public internet.

```bash
# Create a Bedrock VPC endpoint
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0abc1234 \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-0abc1234 subnet-0def5678 \
  --security-group-ids sg-0abc1234 \
  --private-dns-enabled \
  --region us-east-1

# Also create endpoint for the bedrock (control plane) service
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0abc1234 \
  --service-name com.amazonaws.us-east-1.bedrock \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-0abc1234 \
  --private-dns-enabled
```

Attach an endpoint policy to restrict which principals and models can be accessed via the endpoint.

## Encryption

| Layer | Default | Customer-Managed Key |
|---|---|---|
| Data in transit | TLS 1.2+ always on | Not configurable |
| Invocation log data at rest (S3) | SSE-S3 | SSE-KMS with CMK |
| Provisioned Throughput model copies | AWS-managed key | CMK via `--customModelKmsKeyId` |
| Knowledge Base vector store | Depends on store | Configure CMK in OpenSearch/Aurora |

```bash
# Enable CMK on invocation logs S3 bucket
aws s3api put-bucket-encryption \
  --bucket my-bedrock-logs \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "arn:aws:kms:us-east-1:123456789012:key/KEY_ID"
      }
    }]
  }'
```

## Guardrails

Guardrails enforce content policies on both input prompts and model responses.

```bash
aws bedrock create-guardrail \
  --name "production-guardrail" \
  --content-policy-config '{
    "filtersConfig": [
      {"type": "SEXUAL", "inputStrength": "HIGH", "outputStrength": "HIGH"},
      {"type": "VIOLENCE", "inputStrength": "MEDIUM", "outputStrength": "HIGH"},
      {"type": "PROMPT_ATTACK", "inputStrength": "HIGH", "outputStrength": "NONE"}
    ]
  }' \
  --sensitive-information-policy-config '{
    "piiEntitiesConfig": [
      {"type": "EMAIL", "action": "ANONYMIZE"},
      {"type": "CREDIT_DEBIT_CARD_NUMBER", "action": "BLOCK"}
    ]
  }' \
  --blocked-input-messaging "I cannot process this request." \
  --blocked-outputs-messaging "The response was blocked by policy."
```

Apply the guardrail ARN when invoking a model:

```bash
aws bedrock-runtime invoke-model \
  --model-id "anthropic.claude-3-sonnet-20240229-v1:0" \
  --guardrail-identifier "arn:aws:bedrock:us-east-1:123456789012:guardrail/GUARD_ID" \
  --guardrail-version "1" \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":512,"messages":[{"role":"user","content":"Hello"}]}' \
  output.json
```

## Audit and Compliance

```bash
# Enable CloudTrail for Bedrock API calls
aws cloudtrail create-trail \
  --name bedrock-audit-trail \
  --s3-bucket-name my-cloudtrail-bucket \
  --is-multi-region-trail \
  --enable-log-file-validation

# Search for Bedrock invocation events
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=bedrock.amazonaws.com \
  --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ) \
  --query 'Events[*].{Time:EventTime,User:Username,Event:EventName}'
```
