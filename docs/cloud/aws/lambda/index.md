# Lambda

AWS Lambda — serverless function deployment, invocation, monitoring, and troubleshooting.

## Key Concepts

| Concept | Description |
|---|---|
| Function | Code + configuration (runtime, memory, timeout, env vars) |
| Trigger / Event source | What invokes the function (API GW, S3, SQS, EventBridge, etc.) |
| Execution environment | Isolated runtime container; reused across invocations (warm start) |
| Concurrency | Simultaneous executions; default account limit: 1,000 |
| Reserved concurrency | Hard cap for a function (protects downstream systems) |
| Provisioned concurrency | Pre-warmed environments (eliminates cold starts) |
| Layer | Shared library or dependency package added to functions |

## Common CLI Commands

```bash
# List functions
aws lambda list-functions \
  --query 'Functions[*].{Name:FunctionName,Runtime:Runtime,Memory:MemorySize,Timeout:Timeout,Modified:LastModified}' \
  --output table

# Invoke a function synchronously
aws lambda invoke \
  --function-name <function-name> \
  --payload '{"key":"value"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
cat response.json

# Invoke asynchronously
aws lambda invoke \
  --function-name <function-name> \
  --invocation-type Event \
  --payload '{"key":"value"}' \
  --cli-binary-format raw-in-base64-out \
  /dev/null

# Get function configuration
aws lambda get-function-configuration --function-name <function-name>

# Update function code (from S3)
aws lambda update-function-code \
  --function-name <function-name> \
  --s3-bucket <bucket> \
  --s3-key <key>

# Update environment variables
aws lambda update-function-configuration \
  --function-name <function-name> \
  --environment Variables={DB_HOST=<host>,DB_PORT=5432}

# Publish a version and create alias
aws lambda publish-version --function-name <function-name>
aws lambda create-alias \
  --function-name <function-name> \
  --name prod \
  --function-version <version-number>
```

## Monitoring and Logs

```bash
# Tail function logs (CloudWatch Logs)
aws logs tail /aws/lambda/<function-name> --follow

# Get recent log events
aws logs get-log-events \
  --log-group-name /aws/lambda/<function-name> \
  --log-stream-name <stream-name> \
  --limit 50

# CloudWatch Insights — find errors in last 1 hour
aws logs start-query \
  --log-group-name /aws/lambda/<function-name> \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 50'
```

## Key CloudWatch Metrics

| Metric | Threshold to Watch |
|---|---|
| Errors | Any increase |
| Duration (P99) | Approaching timeout |
| Throttles | >0 — increase reserved concurrency |
| ConcurrentExecutions | Approaching account limit |
| IteratorAge (for streams) | Increasing — function falling behind |

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Function timing out | Duration vs timeout config | Increase timeout; optimise code or add concurrency |
| Throttling errors | ConcurrentExecutions limit | Request limit increase; add SQS queue for buffering |
| `AccessDeniedException` | Execution role IAM | Add required permissions to Lambda execution role |
| Cold start latency | First invocation or after idle | Use provisioned concurrency for latency-sensitive functions |
| OOM (out of memory) | MemorySize | Increase memory; check for memory leaks in code |
| VPC function can't reach internet | NAT Gateway | Lambda in private subnet needs NAT GW for outbound internet |
