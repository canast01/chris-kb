---
tags:
  - aws
description: "Lambda reference covering Environment Variables, Event Source Mappings (SQS / Kinesis triggers), Layers, Versions and Aliases, Concurrency and 2 more..."
---
# Lambda

<div class="kb-summary">
Lambda reference covering Environment Variables, Event Source Mappings (SQS / Kinesis triggers), Layers, Versions and Aliases, Concurrency and 2 more sections.

*Applies to: AWS*
</div>

```d2
direction: down

event_source_mappings_sqs_kinesis_tr: "Event Source Mappings (SQS / Kinesis triggers)" {shape: rectangle}
layers: "Layers" {shape: rectangle}
versions_and_aliases: "Versions and Aliases" {shape: rectangle}
concurrency: "Concurrency" {shape: rectangle}
function_urls: "Function URLs" {shape: rectangle}
logs: "Logs" {shape: rectangle}

event_source_mappings_sqs_kinesis_tr -> layers: uses
layers -> versions_and_aliases: uses
versions_and_aliases -> concurrency: uses
concurrency -> function_urls: uses
function_urls -> logs: uses
```

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


```text title="Expected output"
{
    "EventSourceMappings": [
        {
            "UUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "EventSourceArn": "arn:aws:sqs:us-east-1:123456789012:my-queue",
            "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor",
            "State": "Enabled",
            "BatchSize": 10,
            "LastProcessingResult": "OK"
        },
        {
            "UUID": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
            "EventSourceArn": "arn:aws:kinesis:us-east-1:123456789012:stream/my-stream",
            "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor",
            "State": "Enabled",
            "BatchSize": 100,
            "StartingPosition": "LATEST"
        }
    ]
}
{
    "UUID": "c3d4e5f6-a7b8-9012-cdef-123456789012",
    "EventSourceArn": "arn:aws:sqs:us-east-1:123456789012:my-queue",
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor",
    "State": "Creating",
    "BatchSize": 10,
    "Enabled": true
}
{
    "UUID": "d4e5f6a7-b8c9-0123-def1-234567890123",
    "EventSourceArn": "arn:aws:kinesis:us-east-1:123456789012:stream/my-stream",
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor",
    "State": "Creating",
    "BatchSize": 100,
    "StartingPosition": "LATEST"
}
{
    "UUID": "c3d4e5f6-a7b8-9012-cdef-123456789012",
    "EventSourceArn": "arn:aws:sqs:us-east-1:123456789012:my-queue",
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor",
    "State": "Enabled",
    "BatchSize": 10,
    "Enabled": true,
    "LastUpdateStatus": "Successful"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFoundException: Event source mapping not found` | Verify the UUID is correct and the mapping exists using `aws lambda list-event-source-mappings --function-name <name>`. |
    | `InvalidParameterValueException: The role is invalid or does not have permission to access the event source` | Ensure the Lambda execution role has `sqs:ReceiveMessage` or `kinesis:GetRecords` permissions for the event source ARN. |
    **`Resource
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


```text title="Expected output"
{
    "Layers": [
        {
            "LayerArn": "arn:aws:lambda:us-east-1:123456789012:layer:numpy-scipy",
            "LayerVersionArn": "arn:aws:lambda:us-east-1:123456789012:layer:numpy-scipy:5",
            "Version": 5,
            "Description": "NumPy and SciPy for data processing",
            "CreatedDate": "2024-01-15T10:32:44.000+0000",
            "CompatibleRuntimes": ["python3.12", "python3.11"]
        },
        {
            "LayerArn": "arn:aws:lambda:us-east-1:123456789012:layer:requests-lib",
            "LayerVersionArn": "arn:aws:lambda:us-east-1:123456789012:layer:requests-lib:3",
            "Version": 3,
            "Description": "HTTP requests library",
            "CreatedDate": "2024-01-10T14:22:11.000+0000",
            "CompatibleRuntimes": ["python3.12"]
        }
    ]
}
{
    "LayerVersions": [
        {
            "LayerVersionArn": "arn:aws:lambda:us-east-1:123456789012:layer:custom-deps:8",
            "Version": 8,
            "Description": "My runtime deps",
            "CreatedDate": "2024-01-16T09:45:22.000+0000",
            "CompatibleRuntimes": ["python3.12"]
        },
        {
            "LayerVersionArn": "arn:aws:lambda:us-east-1:123456789012:layer:custom-deps:7",
            "Version": 7,
            "CreatedDate": "2024-01-14T16:18:55.000+0000",
            "CompatibleRuntimes": ["python3.12"]
        }
    ]
}
{
    "LayerVersionArn": "arn:aws:lambda:us-east-1:123456789012:layer:custom-deps:9",
    "Version": 9,
    "Description": "My runtime deps",
    "CreatedDate": "2024-01-16T11:02:33.000+0000",
    "CompatibleRuntimes": ["python3.12"],
    "Content": {
        "Location": "https://awslambda-us-east-1-tasks.s3.us-east-1.amazonaws.com/...",
        "CodeSha256": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
    }
}
{
    "Statement": "{\"Sid\":\"AllowAccount123\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::987654321098:root\"},\"Action\":\"lambda:GetLayerVersion\",\"Resource\":\"arn:aws:lambda:us-east-1:123456789012:layer:custom-deps:9\"}"
}
{
    "Function
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


```text title="Expected output"
{
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor:7",
    "Version": "7",
    "CodeSha256": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "LastModified": "2024-01-15T14:32:18.000+0000"
}
{
    "Versions": [
        {
            "Version": "$LATEST",
            "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor:$LATEST"
        },
        {
            "Version": "1",
            "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor:1"
        },
        {
            "Version": "5",
            "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor:5"
        },
        {
            "Version": "7",
            "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor:7"
        }
    ]
}
{
    "AliasArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor:alias/prod",
    "Name": "prod",
    "FunctionVersion": "7",
    "Description": ""
}
{
    "AliasArn": "arn:aws:lambda:us-east-1:123456789012:function:my-processor:alias/prod",
    "Name": "prod",
    "FunctionVersion": "8",
    "RoutingConfig": {
        "AdditionalVersionWeights": {
            "7": 0.1
        }
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the PublishVersion operation: The resource you requested does not exist.` | Verify the function name matches exactly and the function exists in the current AWS region. |
    | `An error occurred (InvalidParameterValueException) when calling the UpdateAlias operation: The function version 8 does not exist.` | Publish version 8 first using `aws lambda publish-version --function-name <name>` before updating the alias to point to it. |
    | `An error occurred (ResourceConflictException) when calling the CreateAlias operation: Cannot create Alias for this function. The Alias prod already exists.` | Use `update-alias` instead of `create-alias` if the alias already exists, or delete it first with `aws lambda delete-alias`. |
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


```text title="Expected output"
{
    "ReservedConcurrentExecutions": 100
}
{
    "Requested": 10,
    "Allocated": 10,
    "Status": "InProgress",
    "LastModified": "2024-01-15T14:32:47.123000+00:00"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the PutReservedConcurrency operation: The resource you requested does not exist.` | Verify the function name exists in the current AWS region using `aws lambda list-functions`. |
    | `An error occurred (InvalidParameterValueException) when calling the PutProvisionedConcurrencyConfig operation: The qualifier does not exist.` | Ensure the alias or version (e.g., `prod`) exists; list versions with `aws lambda list-versions-by-function --function-name <name>`. |
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


```text title="Expected output"
{
    "FunctionUrl": "https://abcdefg1234567890.lambda-url.us-east-1.amazonaws.com/",
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-function",
    "CreationTime": "2024-01-15T10:23:45.123456+00:00",
    "AuthType": "NONE"
}
{
    "FunctionUrl": "https://hijklmn9876543210.lambda-url.us-east-1.amazonaws.com/",
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-function",
    "CreationTime": "2024-01-15T10:24:12.654321+00:00",
    "AuthType": "AWS_IAM"
}
{
    "FunctionUrl": "https://abcdefg1234567890.lambda-url.us-east-1.amazonaws.com/",
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:my-function",
    "CreationTime": "2024-01-15T10:23:45.123456+00:00",
    "AuthType": "NONE",
    "LastModifiedTime": "2024-01-15T10:24:12.654321+00:00"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceConflictException) when calling the CreateFunctionUrlConfig operation: The resource already exists.` | Delete the existing URL config with `aws lambda delete-function-url-config --function-name <name>` before creating a new one. |
    | `An error occurred (ResourceNotFoundException) when calling the GetFunctionUrlConfig operation: The resource you requested does not exist.` | Verify the function name is correct and a URL config has been created for this function. |
    | `An error occurred (InvalidParameterValueException) when calling the CreateFunctionUrlConfig operation: Invalid auth type specified.` | Use only `NONE` or `AWS_IAM` as the `--auth-type` value. |
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


```text title="Expected output"
2024-01-15T14:32:18.456Z	REQUEST	RequestId: a1b2c3d4-e5f6-7890-abcd-ef1234567890	Duration: 245.32 ms	Billed Duration: 246 ms	Memory Size: 128 MB	Max Memory Used: 87 MB	Init Duration: 523.41 ms
2024-01-15T14:32:19.123Z	ERROR	Traceback (most recent call last):
2024-01-15T14:32:19.124Z	ERROR	  File "/var/task/lambda_function.py", line 42, in handler
2024-01-15T14:32:19.125Z	ERROR	    response = db.query(sql_statement)
2024-01-15T14:32:19.126Z	ERROR	ConnectionError: Unable to connect to database endpoint rds-prod.c9akciq32.us-east-1.rds.amazonaws.com:5432
2024-01-15T14:32:20.789Z	END	RequestId: a1b2c3d4-e5f6-7890-abcd-ef1234567890	Runtime: python3.11

{
    "events": [
        {
            "logStreamName": "2024/01/15/[$LATEST]a1b2c3d4e5f6",
            "timestamp": 1705329139123,
            "message": "ERROR\tConnectionError: Unable to connect to database endpoint",
            "eventId": "37405409649205249650529284057344"
        }
    ],
    "searchedLogStreams": 8
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFoundException: The specified log group does not exist.` | Verify the function name is correct and the Lambda function has CloudWatch Logs permissions in its execution role. |
    | `InvalidParameterException: Invalid filter pattern syntax` | Ensure filter patterns use valid CloudWatch Logs syntax (e.g., `[ERROR]` for bracketed terms or quoted strings for exact matches). |
## See also

- [AWS CLI Reference](../index.md)
- [AWS Compute](../../compute/index.md)
