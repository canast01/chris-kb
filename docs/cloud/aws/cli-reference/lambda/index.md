# Lambda


<div class="kb-summary">
Lambda reference covering Environment Variables, Event Source Mappings (SQS / Kinesis triggers), Layers, Versions and Aliases, Concurrency and 2 more sections.
</div>

```text
Lambda CLI: Deploy → Invoke → Monitor
──────────────────────────────────────────────────────────────

  function.zip
       │ update-function-code
       ▼
  ┌────────────────────────────────────────────────────┐
  │  Lambda Function                                   │
  │  list-functions / get-function                     │
  │  ┌──────────────────────────────────────────────┐  │
  │  │ Versions: publish-version ($LATEST → v1,v2)  │  │
  │  │ Aliases:  create-alias (prod → v7)            │  │
  │  │ Layers:   update-function-configuration       │  │
  │  └──────────────────────────────────────────────┘  │
  └────────────────────────────────────────────────────┘
          │ invoke (sync)          │ event source mapping
          ▼                        ▼
  ┌───────────────┐       ┌─────────────────────┐
  │  Response     │       │  SQS / Kinesis      │
  │  response.json│       │  create-event-      │
  │               │       │  source-mapping     │
  └───────────────┘       └─────────────────────┘
          │
          ▼ logs tail /aws/lambda/<fn> --follow
  ┌───────────────────────────────────┐
  │  CloudWatch Logs                  │
  │  filter-log-events "ERROR"        │
  └───────────────────────────────────┘
```
```
┌────────────────────────────────────────── AWS CLI — Lambda ───────────────────────────────────────────┐
│                                                                                                       │
│  Lambda CLI commands for function deploy, invoke, configuration, and log retrieval.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Function Management              │  │                  Invocation                 │   │
│   │           create-function: deploy            │  │           invoke: synchronous call          │   │
│   │        update-function-code: redeploy        │  │        invoke --invocation-type Event       │   │
│   │        update-function-configuration         │  │            invoke --log-type Tail           │   │
│   │           delete-function: remove            │  │          list-event-source-mappings         │   │
│   │          list-functions: all funcs           │  │         create-event-source-mapping         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  update-function-code deploys new zip/ECR; invoke tests synchronously or async                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Versions and Aliases             │  │                Configuration                │   │
│   │          publish-version: snapshot           │  │          get-function-configuration         │   │
│   │         create-alias: named pointer          │  │           put-function-concurrency          │   │
│   │         update-alias: shift traffic          │  │       put-function-event-invoke-config      │   │
│   │          list-versions-by-function           │  │       add-permission: resource policy       │   │
│   │        delete-function (--qualifier)         │  │         get-policy: show permissions        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Lambda execution environment · VPC (if configured) · CloudWatch Logs · SQS/SNS/S3                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  invoke          = Executes function synchronously; response returned in CLI output                   │
│  --invocation-type Event= Asynchronous invocation; no response body returned                          │
│  --log-type Tail = Returns last 4KB of execution log in Base64 in response                            │
│  publish-version = Creates immutable numbered version from current $LATEST code                       │
│  Alias           = Named pointer to specific version; used for blue/green traffic split               │
│  Event source mapping= Connects Lambda to SQS/Kinesis/DynamoDB stream as trigger                      │
│  Concurrency     = Max simultaneous Lambda executions; reserved or unreserved                         │
│  add-permission  = Grants another service (S3, SNS) permission to invoke function                     │
│  put-function-event-invoke-config= Sets max retries and DLQ for async invocations                     │
│  DLQ             = Dead Letter Queue; receives failed async events after retries                      │
│  $LATEST         = Mutable latest version; always updated by update-function-code                     │
│  ECR             = Elastic Container Registry; source for Lambda container image                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

## Event Source Mappings (SQS / Kinesis triggers)

```bash
# List all event source mappings for a function
aws lambda list-event-source-mappings --function-name <name>

# Create an SQS trigger
aws lambda create-event-source-mapping \
  --function-name <name> \
  --event-source-arn arn:aws:sqs:<region>:<account_id>:<queue-name> \
  --batch-size 10 \
  --enabled

# Create a Kinesis trigger
aws lambda create-event-source-mapping \
  --function-name <name> \
  --event-source-arn arn:aws:kinesis:<region>:<account_id>:stream/<stream-name> \
  --batch-size 100 \
  --starting-position LATEST

# Disable / enable an existing mapping
aws lambda update-event-source-mapping \
  --uuid <mapping-uuid> \
  --enabled     # use --no-enabled to disable

# Delete a mapping
aws lambda delete-event-source-mapping --uuid <mapping-uuid>
```

## Layers

```bash
# List available layers (latest version of each)
aws lambda list-layers

# List versions of a specific layer
aws lambda list-layer-versions --layer-name <layer-name>

# Publish a new layer version from a zip
aws lambda publish-layer-version \
  --layer-name <layer-name> \
  --description "My runtime deps" \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.12

# Grant another account permission to use a layer version
aws lambda add-layer-version-permission \
  --layer-name <layer-name> \
  --version-number <version> \
  --statement-id AllowAccount123 \
  --action lambda:GetLayerVersion \
  --principal <account_id>

# Attach a layer to a function
aws lambda update-function-configuration \
  --function-name <name> \
  --layers arn:aws:lambda:<region>:<account_id>:layer:<layer-name>:<version>
```

## Versions and Aliases

```bash
# Publish the current $LATEST code as a numbered version
aws lambda publish-version --function-name <name>

# List all published versions
aws lambda list-versions-by-function --function-name <name>

# Create an alias pointing to a specific version
aws lambda create-alias \
  --function-name <name> \
  --name prod \
  --function-version 7

# Shift alias traffic between two versions (weighted routing)
aws lambda update-alias \
  --function-name <name> \
  --name prod \
  --function-version 8 \
  --routing-config AdditionalVersionWeights={"7"=0.1}
```

## Concurrency

```bash
# Set reserved concurrency (hard cap; 0 throttles all invocations)
aws lambda put-reserved-concurrency \
  --function-name <name> \
  --reserved-concurrent-executions 100

# Configure provisioned concurrency for an alias or version
aws lambda put-provisioned-concurrency-config \
  --function-name <name> \
  --qualifier prod \
  --provisioned-concurrent-executions 10

# Remove reserved concurrency
aws lambda delete-reserved-concurrency-config --function-name <name>
```

## Function URLs

```bash
# Create a public function URL (no auth)
aws lambda create-function-url-config \
  --function-name <name> \
  --auth-type NONE

# Create a function URL restricted to IAM sigv4
aws lambda create-function-url-config \
  --function-name <name> \
  --auth-type AWS_IAM

# Get the URL for an existing config
aws lambda get-function-url-config --function-name <name>
```

## Logs

```bash
# Stream live logs
aws logs tail /aws/lambda/<function_name> --follow

# Filter recent log events by pattern (last 30 minutes)
aws logs filter-log-events \
  --log-group-name /aws/lambda/<function_name> \
  --start-time $(date -d '-30 minutes' +%s000) \
  --filter-pattern "ERROR"

# Filter logs for a specific request ID
aws logs filter-log-events \
  --log-group-name /aws/lambda/<function_name> \
  --filter-pattern "<request_id>"
```
