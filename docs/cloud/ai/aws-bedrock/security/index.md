---
tags:
  - security
description: "Security for Bedrock spans IAM access control, network isolation with VPC endpoints, encryption at rest and in transit, and content guardrails. Apply all..."
---
# Bedrock Security

<div class="kb-summary">
Security for Bedrock spans IAM access control, network isolation with VPC endpoints, encryption at rest and in transit, and content guardrails. Apply all layers for production deployments handling sensitive data.

*Applies to: AWS Bedrock*
</div>

```d2
direction: down

external: External / Untrusted {shape: rectangle}
iam_policies: "IAM Policies" {shape: rectangle}
vpc_endpoints: "VPC Endpoints" {shape: rectangle}
encryption: "Encryption" {shape: rectangle}
guardrails: "Guardrails" {shape: rectangle}
audit_and_compliance: "Audit and Compliance" {shape: rectangle}
core: "AWS Bedrock Core" {shape: hexagon}

external -> iam_policies: traffic in
iam_policies -> vpc_endpoints
vpc_endpoints -> encryption
encryption -> guardrails
guardrails -> audit_and_compliance
audit_and_compliance -> core: secured path
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

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


```text title="Expected output"
{
    "VpcEndpoint": {
        "VpcEndpointId": "vpce-0a1b2c3d4e5f6g7h8",
        "VpcId": "vpc-0abc1234",
        "ServiceName": "com.amazonaws.us-east-1.bedrock-runtime",
        "State": "pending",
        "VpcEndpointType": "Interface",
        "CreationTimestamp": "2024-01-15T14:32:18.000Z",
        "SubnetIds": ["subnet-0abc1234", "subnet-0def5678"],
        "Groups": [{"GroupId": "sg-0abc1234", "GroupName": "bedrock-vpc-endpoint"}],
        "PrivateDnsEnabled": true,
        "PrivateDnsNameOptions": {"PrivateDnsHostnameType": "ip-name"}
    }
}
{
    "VpcEndpoint": {
        "VpcEndpointId": "vpce-0i9j8k7l6m5n4o3p2",
        "VpcId": "vpc-0abc1234",
        "ServiceName": "com.amazonaws.us-east-1.bedrock",
        "State": "pending",
        "VpcEndpointType": "Interface",
        "CreationTimestamp": "2024-01-15T14:32:21.000Z",
        "SubnetIds": ["subnet-0abc1234"],
        "Groups": [{"GroupId": "sg-default", "GroupName": "default"}],
        "PrivateDnsEnabled": true
    }
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidVpcID.NotFound) when calling the CreateVpcEndpoint operation: The VPC ID 'vpc-0abc1234' does not exist`** — Verify the VPC ID exists in your region with `aws ec2 describe-vpcs --region us-east-1`.
    **`An error occurred (InvalidSubnetID.NotFound) when calling the CreateVpcEndpoint operation: The subnet ID 'subnet-0abc1234' does not exist`** — Confirm the subnet IDs belong to the specified VPC and region using `aws ec2 describe-subnets --subnet-ids subnet-0abc1234 --region us-east-1`.
    **`An error occurred (InvalidGroup.NotFound) when calling the CreateVpcEndpoint operation: The security group 'sg-0abc1234' does not exist`** — Ensure the security group exists in the same VPC with `aws ec2 describe-security-groups --group-ids sg-0abc1234 --region us-east-1`.
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`An error occurred (NoSuchBucket) when calling the PutBucketEncryption operation: The specified bucket does not exist`** — Verify the bucket name is correct and exists in the same AWS region by running `aws s3 ls | grep my-bedrock-logs`.
    **`An error occurred (AccessDenied) when calling the PutBucketEncryption operation: User: arn:aws:iam::123456789012:user/USERNAME is not authorized to perform: s3:PutEncryptionConfiguration`** — Add the `s3:PutEncryptionConfiguration` permission to your IAM user or role's policy.
    **`An error occurred (InvalidArgument) when calling the PutBucketEncryption operation: The KMS key ARN provided is invalid or the key does not exist`** — Confirm the KMS key ARN is correct and the key exists in the same region using `aws kms describe-key --key-id arn:aws:kms:us-east-1:123456789012:key/KEY_ID`.
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


```text title="Expected output"
{
    "guardrailId": "gdrail-7f4a2c9e1b5d8a3f",
    "guardrailArn": "arn:aws:bedrock:us-east-1:123456789012:guardrail/gdrail-7f4a2c9e1b5d8a3f",
    "createdAt": "2024-01-15T14:32:47.123Z",
    "version": "1",
    "name": "production-guardrail",
    "status": "ACTIVE",
    "contentPolicyConfig": {
        "filtersConfig": [
            {"type": "SEXUAL", "inputStrength": "HIGH", "outputStrength": "HIGH"},
            {"type": "VIOLENCE", "inputStrength": "MEDIUM", "outputStrength": "HIGH"},
            {"type": "PROMPT_ATTACK", "inputStrength": "HIGH", "outputStrength": "NONE"}
        ]
    },
    "sensitiveInformationPolicyConfig": {
        "piiEntitiesConfig": [
            {"type": "EMAIL", "action": "ANONYMIZE"},
            {"type": "CREDIT_DEBIT_CARD_NUMBER", "action": "BLOCK"}
        ]
    },
    "blockedInputMessaging": "I cannot process this request.",
    "blockedOutputsMessaging": "The response was blocked by policy."
}
```

!!! warning "Common errors"
    **`An error occurred (ValidationException) when calling the CreateGuardrail operation: Invalid filter type 'SEXUAL'. Valid types are: PROFANITY, HATE, VIOLENCE, SEXUAL_CONTENT, PROMPT_INJECTION`** — Replace `"SEXUAL"` with `"SEXUAL_CONTENT"` in the filtersConfig.
    **`An error occurred (AccessDeniedException) when calling the CreateGuardrail operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: bedrock:CreateGuardrail`** — Add the `bedrock:CreateGuardrail` permission to the IAM user or role's policy.
    **`An error occurred (ValidationException) when calling the CreateGuardrail operation: Invalid action 'ANONYMIZE' for PII type 'EMAIL'. Valid actions are: BLOCK, REDACT`** — Change the EMAIL action from `"ANONYMIZE"` to `"REDACT"`.
Apply the guardrail ARN when invoking a model:

```bash
aws bedrock-runtime invoke-model \
  --model-id "anthropic.claude-3-sonnet-20240229-v1:0" \
  --guardrail-identifier "arn:aws:bedrock:us-east-1:123456789012:guardrail/GUARD_ID" \
  --guardrail-version "1" \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":512,"messages":[{"role":"user","content":"Hello"}]}' \
  output.json
```


```text title="Expected output"
{
  "content": [
    {
      "type": "text",
      "text": "Hello! I'm Claude, an AI assistant made by Anthropic. How can I help you today?"
    }
  ],
  "id": "msg_013xyz789abc",
  "model": "anthropic.claude-3-sonnet-20240229-v1:0",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 8,
    "output_tokens": 24
  }
}
```

!!! warning "Common errors"
    **`An error occurred (ValidationException) when calling the InvokeModel operation: Invalid guardrail ARN format`** — Verify the guardrail ARN matches the pattern `arn:aws:bedrock:region:account-id:guardrail/guardrail-id` and that the guardrail exists in the specified region.
    **`An error occurred (ResourceNotFoundException) when calling the InvokeModel operation: Could not find guardrail with id GUARD_ID`** — Confirm the guardrail identifier exists in your AWS account by running `aws bedrock list-guardrails --region us-east-1`.
    **`An error occurred (AccessDeniedException) when calling the InvokeModel operation: User is not authorized to perform bedrock:InvokeModel`** — Add the `bedrock:InvokeModel` and `bedrock:ApplyGuardrail` permissions to your IAM user or role policy.
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


```text title="Expected output"
{
    "TrailARN": "arn:aws:cloudtrail:us-east-1:123456789012:trail/bedrock-audit-trail",
    "S3BucketName": "my-cloudtrail-bucket",
    "IncludeGlobalServiceEvents": true,
    "IsMultiRegionTrail": true,
    "HomeRegion": "us-east-1",
    "TrailStatus": {
        "IsLogging": false,
        "LatestDeliveryTime": null,
        "LatestDeliveryAttemptTime": null
    },
    "HasCustomEventSelectors": false,
    "HasInsightSelectors": false,
    "IsOrganizationTrail": false
}
[
    {
        "Time": "2024-01-15T14:32:18Z",
        "User": "arn:aws:iam::123456789012:user/bedrock-admin",
        "Event": "InvokeModel"
    },
    {
        "Time": "2024-01-15T13:47:05Z",
        "User": "arn:aws:iam::123456789012:role/bedrock-lambda-role",
        "Event": "InvokeModel"
    },
    {
        "Time": "2024-01-15T12:19:42Z",
        "User": "arn:aws:iam::123456789012:user/data-scientist",
        "Event": "GetFoundationModelAvailability"
    }
]
```

!!! warning "Common errors"
    **`An error occurred (TrailAlreadyExists) when calling the CreateTrail operation: Trail already exists.`** — Use `aws cloudtrail describe-trails --trail-name bedrock-audit-trail` to verify the trail exists, or delete it first with `aws cloudtrail delete-trail --name bedrock-audit-trail`.
    **`An error occurred (S3BucketDoesNotExist) when calling the CreateTrail operation: S3 bucket does not exist.`** — Create the S3 bucket with `aws s3 mb s3://my-cloudtrail-bucket` before running the create-trail command.
    **`An error occurred (InvalidParameterException) when calling the LookupEvents operation: Start time is invalid.`** — Ensure the date command produces valid ISO 8601 format; test with `date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ` on your system first.