---
tags:
  - aws
  - ai
description: "AWS Bedrock emits CloudWatch metrics and optional invocation logs that cover latency, token usage, error rates, and throttling. Setting up monitoring..."
---
# Bedrock Monitoring

<div class="kb-summary">
AWS Bedrock emits CloudWatch metrics and optional invocation logs that cover latency, token usage, error rates, and throttling. Setting up monitoring early prevents blind spots in production.

*Applies to: AWS Bedrock*
</div>

```d2
direction: right

cloudwatch_metrics: "CloudWatch Metrics" {shape: rectangle}
key_metrics_reference: "Key Metrics Reference" {shape: rectangle}
invocation_logging: "Invocation Logging" {shape: rectangle}
cloudwatch_alarms: "CloudWatch Alarms" {shape: rectangle}
querying_logs_with_cloudwatch_insigh: "Querying Logs with CloudWatch Insights" {shape: rectangle}
latency_tracking_with_dashboards: "Latency Tracking with Dashboards" {shape: rectangle}

cloudwatch_metrics -> key_metrics_reference
key_metrics_reference -> invocation_logging
invocation_logging -> cloudwatch_alarms
cloudwatch_alarms -> querying_logs_with_cloudwatch_insigh
querying_logs_with_cloudwatch_insigh -> latency_tracking_with_dashboards
```

## CloudWatch Metrics

Bedrock publishes metrics to the `AWS/Bedrock` namespace automatically — no agent or configuration needed.

```bash
# Get invocation count for a model over the last hour
aws cloudwatch get-metric-statistics \
  --namespace AWS/Bedrock \
  --metric-name Invocations \
  --dimensions Name=ModelId,Value=anthropic.claude-3-sonnet-20240229-v1:0 \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Sum

# Get p99 latency
aws cloudwatch get-metric-statistics \
  --namespace AWS/Bedrock \
  --metric-name InvocationLatency \
  --dimensions Name=ModelId,Value=anthropic.claude-3-sonnet-20240229-v1:0 \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics p99
```


```text title="Expected output"
{
    "Label": "Invocations",
    "Datapoints": [
        {
            "Timestamp": "2024-01-15T14:00:00Z",
            "Sum": 342.0,
            "Unit": "Count"
        },
        {
            "Timestamp": "2024-01-15T14:05:00Z",
            "Sum": 387.0,
            "Unit": "Count"
        },
        {
            "Timestamp": "2024-01-15T14:10:00Z",
            "Sum": 421.0,
            "Unit": "Count"
        },
        {
            "Timestamp": "2024-01-15T14:15:00Z",
            "Sum": 356.0,
            "Unit": "Count"
        }
    ]
}
{
    "Label": "InvocationLatency",
    "Datapoints": [
        {
            "Timestamp": "2024-01-15T14:00:00Z",
            "Maximum": 2847.5,
            "Unit": "Milliseconds"
        },
        {
            "Timestamp": "2024-01-15T14:05:00Z",
            "Maximum": 3124.2,
            "Unit": "Milliseconds"
        },
        {
            "Timestamp": "2024-01-15T14:10:00Z",
            "Maximum": 2956.8,
            "Unit": "Milliseconds"
        },
        {
            "Timestamp": "2024-01-15T14:15:00Z",
            "Maximum": 3201.4,
            "Unit": "Milliseconds"
        }
    ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationException) when calling the GetMetricStatistics operation: The parameter MetricName is invalid.` | Verify the metric name is exactly `Invocations` or `InvocationLatency` and check AWS/Bedrock namespace documentation for available metrics. |
    | `An error occurred (InvalidParameterValue) when calling the GetMetricStatistics operation: The start time is after the end time.` | Ensure the `--start-time` is before `--end-time`; verify your system clock is synchronized with UTC. |
## Key Metrics Reference

| Metric | Namespace | Description |
|---|---|---|
| `Invocations` | AWS/Bedrock | Total model invocation count |
| `InvocationLatency` | AWS/Bedrock | End-to-end latency in ms |
| `InputTokenCount` | AWS/Bedrock | Input tokens consumed |
| `OutputTokenCount` | AWS/Bedrock | Output tokens generated |
| `ThrottledRequests` | AWS/Bedrock | Requests rejected due to rate limits |
| `InvocationClientErrors` | AWS/Bedrock | 4xx errors (bad input, auth) |
| `InvocationServerErrors` | AWS/Bedrock | 5xx errors (service side) |

## Invocation Logging

Enable invocation logs to capture full request/response payloads in S3 and/or CloudWatch Logs.

```bash
aws bedrock put-model-invocation-logging-configuration \
  --logging-config '{
    "cloudWatchConfig": {
      "logGroupName": "/aws/bedrock/model-invocations",
      "roleArn": "arn:aws:iam::123456789012:role/BedrockCloudWatchRole",
      "largeDataDeliveryS3Config": {
        "bucketName": "my-bedrock-logs",
        "keyPrefix": "large-payloads/"
      }
    },
    "s3Config": {
      "bucketName": "my-bedrock-logs",
      "keyPrefix": "invocations/"
    },
    "textDataDeliveryEnabled": true,
    "imageDataDeliveryEnabled": false,
    "embeddingDataDeliveryEnabled": false
  }' \
  --region us-east-1
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationException) when calling the PutModelInvocationLoggingConfiguration operation: Invalid ARN format for roleArn` | Verify the IAM role ARN exists and follows the format `arn:aws:iam::ACCOUNT-ID:role/ROLE-NAME`. |
    | `An error occurred (AccessDeniedException) when calling the PutModelInvocationLoggingConfiguration operation: User is not authorized to perform: bedrock:PutModelInvocationLoggingConfiguration` | Add the `bedrock:PutModelInvocationLoggingConfiguration` permission to your IAM user or role policy. |
    | `An error occurred (ValidationException) when calling the PutModelInvocationLoggingConfiguration operation: S3 bucket does not exist or is not accessible` | Ensure both S3 buckets exist in the same region and the IAM role has `s3:PutObject` and `s3:GetObject` permissions. |
Payloads larger than 100 KB are written to S3 even if CloudWatch is the primary destination.

## CloudWatch Alarms

```bash
# Alarm when throttling exceeds 10 requests in 5 minutes
aws cloudwatch put-metric-alarm \
  --alarm-name "bedrock-throttling-high" \
  --namespace AWS/Bedrock \
  --metric-name ThrottledRequests \
  --dimensions Name=ModelId,Value=anthropic.claude-3-sonnet-20240229-v1:0 \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --alarm-actions "arn:aws:sns:us-east-1:123456789012:bedrock-alerts"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationError) when calling the PutMetricAlarm operation: Invalid SNS topic ARN` | Verify the SNS topic ARN exists in the specified region and your IAM user has `sns:Publish` permissions. |
    | `An error occurred (AccessDenied) when calling the PutMetricAlarm operation: User is not authorized to perform: cloudwatch:PutMetricAlarm` | Add the `cloudwatch:PutMetricAlarm` permission to your IAM policy or use an IAM role with CloudWatch full access. |
## Querying Logs with CloudWatch Insights

```bash
# Find slowest invocations in the last 24 hours
fields @timestamp, modelId, inputTokenCount, outputTokenCount, invocationLatency
| filter invocationLatency > 5000
| sort invocationLatency desc
| limit 20
```


```text title="Expected output"
@timestamp                    modelId                              inputTokenCount  outputTokenCount  invocationLatency
2024-01-15T14:32:18.456Z     anthropic.claude-3-sonnet-20240229   1247             892               8934
2024-01-15T13:18:45.123Z     anthropic.claude-3-opus-20240229     2156             1543              7821
2024-01-15T12:54:09.789Z     anthropic.claude-3-haiku-20240307    856              634               6745
2024-01-15T11:22:33.012Z     anthropic.claude-3-sonnet-20240229   3421             2187              6234
2024-01-15T10:45:17.654Z     anthropic.claude-3-opus-20240229     1834             1456              5678
2024-01-15T09:33:22.341Z     anthropic.claude-3-haiku-20240307    945              721               5432
2024-01-15T08:19:51.876Z     anthropic.claude-3-sonnet-20240229   2103             1678              5156
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Syntax error near 'filter': unexpected token` | Ensure this query is run within CloudWatch Logs Insights console or CLI with proper syntax; the pipe syntax shown is CloudWatch Logs Insights-specific and requires the correct query context. |
    | `No results found` | Verify the log group contains Bedrock invocation logs by checking that detailed monitoring is enabled on your Bedrock model invocations and logs are being sent to CloudWatch. |
    | `Field 'invocationLatency' does not exist` | Confirm the field name matches your log structure; use `fields @message | head 5` first to inspect actual field names in your Bedrock logs. |
Run in the CloudWatch Logs Insights console targeting the `/aws/bedrock/model-invocations` log group.

## Latency Tracking with Dashboards

Create a dashboard that combines latency percentiles with token throughput:

```python
import boto3, json

cw = boto3.client("cloudwatch", region_name="us-east-1")

dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "properties": {
                "metrics": [
                    ["AWS/Bedrock", "InvocationLatency", "ModelId",
                     "anthropic.claude-3-sonnet-20240229-v1:0",
                     {"stat": "p50", "label": "p50"}],
                    ["...", {"stat": "p99", "label": "p99"}]
                ],
                "period": 300,
                "title": "Bedrock Invocation Latency"
            }
        }
    ]
}

cw.put_dashboard(
    DashboardName="BedrockMonitoring",
    DashboardBody=json.dumps(dashboard_body)
)
```
