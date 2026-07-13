---
tags:
  - aws
  - ai
description: "AWS Bedrock Agents enable multi-step reasoning and action execution using foundation models. Agents can call APIs, query knowledge bases, and orchestrate..."
---
# Bedrock Agents

<div class="kb-summary">
AWS Bedrock Agents enable multi-step reasoning and action execution using foundation models. Agents can call APIs, query knowledge bases, and orchestrate complex workflows autonomously without custom orchestration code.

*Applies to: AWS Bedrock*
</div>

```d2
direction: down

creating_an_agent: "Creating an Agent" {shape: rectangle}
action_groups: "Action Groups" {shape: rectangle}
lambda_integration: "Lambda Integration" {shape: rectangle}
testing_agents: "Testing Agents" {shape: rectangle}
agent_aliases_and_versioning: "Agent Aliases and Versioning" {shape: rectangle}
troubleshooting: "Troubleshooting" {shape: rectangle}

creating_an_agent -> action_groups: uses
action_groups -> lambda_integration: uses
lambda_integration -> testing_agents: uses
testing_agents -> agent_aliases_and_versioning: uses
agent_aliases_and_versioning -> troubleshooting: uses
```

## Creating an Agent

Each agent requires a foundation model, an instruction prompt, an IAM execution role, and optionally action groups and knowledge bases.

```bash
aws bedrock-agent create-agent \
  --agent-name "support-agent" \
  --agent-resource-role-arn "arn:aws:iam::123456789012:role/AmazonBedrockExecutionRoleForAgents" \
  --foundation-model "anthropic.claude-3-sonnet-20240229-v1:0" \
  --instruction "You are a support agent. Use tools to look up orders, accounts, and tickets." \
  --region us-east-1

# Prepare a working draft after every config change
aws bedrock-agent prepare-agent --agent-id "AGENTID123" --region us-east-1
```


```text title="Expected output"
{
    "agent": {
        "agentId": "AGENTID123",
        "agentName": "support-agent",
        "agentStatus": "CREATING",
        "agentArn": "arn:aws:bedrock:us-east-1:123456789012:agent/AGENTID123",
        "foundationModel": "anthropic.claude-3-sonnet-20240229-v1:0",
        "instruction": "You are a support agent. Use tools to look up orders, accounts, and tickets.",
        "agentResourceRoleArn": "arn:aws:iam::123456789012:role/AmazonBedrockExecutionRoleForAgents",
        "createdAt": "2024-01-15T14:32:18.456Z",
        "updatedAt": "2024-01-15T14:32:18.456Z"
    }
}
{
    "agentId": "AGENTID123",
    "agentStatus": "DRAFT",
    "draftVersion": "DRAFT_V1",
    "preparedAt": "2024-01-15T14:32:45.123Z"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationException) when calling the CreateAgent operation: Invalid IAM role ARN format` | Verify the IAM role ARN exists and matches the pattern `arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME`. |
    | `An error occurred (ResourceNotFoundException) when calling the PrepareAgent operation: Agent not found: AGENTID123` | Use the actual agent ID returned from the create-agent command instead of the placeholder "AGENTID123". |
    | `An error occurred (AccessDenied) when calling the CreateAgent operation: User is not authorized to perform: bedrock:CreateAgent` | Add the `bedrock:CreateAgent` permission to your IAM user or role policy. |
The execution role must trust `bedrock.amazonaws.com` and have `bedrock:InvokeModel` on the chosen model ARN.

## Action Groups

Action groups map the API operations an agent can call to an OpenAPI schema and a Lambda function. Keep schemas focused — overly broad schemas cause the model to hallucinate tool calls.

```bash
aws bedrock-agent create-agent-action-group \
  --agent-id "AGENTID123" \
  --agent-version "DRAFT" \
  --action-group-name "OrderActions" \
  --action-group-executor '{"lambda":"arn:aws:lambda:us-east-1:123456789012:function:order-actions"}' \
  --api-schema '{"s3":{"s3BucketName":"my-schemas","s3ObjectKey":"order-actions.json"}}' \
  --region us-east-1
```


```text title="Expected output"
{
    "agentActionGroupId": "AAGID9f7c2e1b",
    "agentId": "AGENTID123",
    "agentVersion": "DRAFT",
    "actionGroupName": "OrderActions",
    "actionGroupExecutor": {
        "lambda": "arn:aws:lambda:us-east-1:123456789012:function:order-actions"
    },
    "apiSchema": {
        "s3": {
            "s3BucketName": "my-schemas",
            "s3ObjectKey": "order-actions.json"
        }
    },
    "createdAt": "2024-01-15T14:32:47.123Z",
    "updatedAt": "2024-01-15T14:32:47.123Z"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the CreateAgentActionGroup operation: Agent not found` | Verify the agent ID exists with `aws bedrock-agent get-agent --agent-id AGENTID123 --region us-east-1`. |
    | `An error occurred (AccessDeniedException) when calling the CreateAgentActionGroup operation: User is not authorized to perform bedrock-agent:CreateAgentActionGroup` | Add the `bedrock-agent:CreateAgentActionGroup` permission to your IAM role or user policy. |
    | `An error occurred (ValidationException) when calling the CreateAgentActionGroup operation: S3 object not found` | Confirm the schema file exists at `s3://my-schemas/order-actions.json` and your credentials have `s3:GetObject` permission. |
## Lambda Integration

The Lambda receives a structured event and must return a response in the Bedrock-expected format.

```python
def lambda_handler(event, context):
    action_group = event["actionGroup"]
    api_path      = event["apiPath"]
    http_method   = event["httpMethod"]
    params        = {p["name"]: p["value"] for p in event.get("parameters", [])}

    if api_path == "/get-order":
        order = fetch_order(params["orderId"])
        body  = {"orderId": order["id"], "status": order["status"]}
    else:
        body = {"error": "unknown path"}

    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "apiPath": api_path,
            "httpMethod": http_method,
            "httpStatusCode": 200,
            "responseBody": {"application/json": {"body": str(body)}}
        }
    }
```

Set Lambda timeout to at least 60 seconds — agent orchestration adds latency before Lambda is invoked.

## Testing Agents

Use a unique `sessionId` per conversation. The built-in `TSTALIASID` alias always points to the DRAFT version.

```bash
aws bedrock-agent-runtime invoke-agent \
  --agent-id "AGENTID123" \
  --agent-alias-id "TSTALIASID" \
  --session-id "test-$(date +%s)" \
  --input-text "What is the status of order 98765?" \
  --enable-trace \
  --region us-east-1
```


```text title="Expected output"
{
    "sessionState": {
        "sessionAttributes": {},
        "invocationId": "invoke-a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6"
    },
    "output": "Order 98765 is currently in transit. Expected delivery: 2024-01-15. Last scanned at distribution center in Atlanta, GA at 2024-01-12 14:32 UTC.",
    "trace": {
        "trace": [
            {
                "agentAliasId": "TSTALIASID",
                "agentId": "AGENTID123",
                "sessionId": "test-1705084532",
                "timestamp": "2024-01-12T15:42:12.456Z",
                "type": "ModelInvocationRequest",
                "modelInvocationInput": {
                    "text": "What is the status of order 98765?"
                }
            },
            {
                "type": "ActionGroupInvocation",
                "actionGroupName": "OrderLookup",
                "actionName": "getOrderStatus",
                "invocationId": "invoke-xyz789",
                "timestamp": "2024-01-12T15:42:13.891Z"
            }
        ]
    },
    "responseMetadata": {
        "RequestId": "req-9f8e7d6c-5b4a-3c2b-1a09-f8e7d6c5b4a3",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "date": "Fri, 12 Jan 2024 15:42:14 GMT",
            "x-amzn-requestid": "req-9f8e7d6c-5b4a-3c2b-1a09-f8e7d6c5b4a3"
        }
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the InvokeAgent operation: Could not find agent with ID AGENTID123` | Verify the agent ID exists in your AWS account and region by running `aws bedrock-agent list-agents --region us-east-1`. |
    | `An error occurred (ValidationException) when calling the InvokeAgent operation: Agent alias TSTALIASID is not in PREPARED state` | Check the alias status with `aws bedrock-agent get-agent-alias --agent-id AGENTID123 --agent-alias-id TSTALIASID --region us-east-1` and ensure it has been prepared. |
    | `An error occurred (AccessDeniedException) when calling the InvokeAgent operation: User is not authorized to perform bedrock-agent-runtime:InvokeAgent` | Add the `bedrock-agent:InvokeAgent` permission to your IAM user or role policy. |
`--enable-trace` returns orchestration steps showing how the model reasoned, which tools it considered, and what it returned.

## Agent Aliases and Versioning

| Concept | Description |
|---|---|
| DRAFT | Mutable working version, always reflects latest config |
| Version | Immutable numbered snapshot (1, 2, 3…) |
| Alias | Named pointer to a version, used in application code |
| TSTALIASID | Built-in alias pointing to DRAFT |

```bash
# Create an immutable version from the current DRAFT
aws bedrock-agent create-agent-version --agent-id "AGENTID123"

# Create a production alias pointing to version 2
aws bedrock-agent create-agent-alias \
  --agent-id "AGENTID123" \
  --agent-alias-name "production" \
  --routing-configuration '[{"agentVersion":"2"}]'
```


```text title="Expected output"
{
    "agentVersion": {
        "agentId": "AGENTID123",
        "agentVersion": "2",
        "agentStatus": "NOT_PREPARED",
        "createdAt": "2024-01-15T14:32:47.123Z",
        "updatedAt": "2024-01-15T14:32:47.123Z"
    }
}
{
    "agentAliasId": "ALIA5K9M2X",
    "agentId": "AGENTID123",
    "agentAliasName": "production",
    "agentAliasStatus": "CREATED",
    "routingConfiguration": [
        {
            "agentVersion": "2"
        }
    ],
    "createdAt": "2024-01-15T14:32:52.456Z",
    "updatedAt": "2024-01-15T14:32:52.456Z"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationException) when calling the CreateAgentVersion operation: Agent AGENTID123 is in FAILED state and cannot be versioned` | Ensure the agent is in a PREPARED or DRAFT state by running `aws bedrock-agent get-agent --agent-id AGENTID123` to check status, then fix any preparation errors before retrying. |
    | `An error occurred (ResourceNotFoundException) when calling the CreateAgentAlias operation: Could not find agent with id AGENTID123` | Verify the agent ID is correct and exists in your account by listing agents with `aws bedrock-agent list-agents`. |
## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `AccessDeniedException` on invoke | Missing `bedrock:InvokeModel` on execution role | Update IAM policy |
| Lambda not called | OpenAPI schema mismatch | Validate schema against Lambda paths |
| Agent loops without completing | Unclear instruction or missing tool | Refine system prompt, add explicit stop condition |
| Trace shows no tool calls | Model does not recognise need for tool | Add few-shot examples to instruction |

Check CloudWatch Logs under `/aws/lambda/<function-name>` and the Bedrock agent invocation logs for detailed error messages.
