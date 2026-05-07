# CloudTrail

AWS CloudTrail — API activity logging, audit trail, and event history.
## What CloudTrail Captures

- **Management events** — API calls that create, modify, or delete AWS resources (default: enabled)
- **Data events** — object-level operations (S3 GetObject, Lambda invocations) — must be explicitly enabled
- **Insights events** — anomaly detection on unusual API call rates

## Key Concepts

| Concept | Description |
|---|---|
| Trail | Configuration that delivers events to S3 (and optionally CloudWatch Logs / EventBridge) |
| Event history | 90-day read-only view in the console (no trail required) |
| Management event | Control plane API calls — EC2, IAM, S3 bucket ops, etc. |
| Data event | Data plane API calls — S3 GetObject, PutObject, Lambda Invoke |
| CloudTrail Lake | Managed query lake; store and query events in SQL-like format |

## Common CLI Commands

```bash
# List trails
aws cloudtrail describe-trails --output table

# Get trail status (is logging?)
aws cloudtrail get-trail-status --name <trail-name>

# Look up events by resource or user (last 90 days from Event History)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=Username,AttributeValue=<iam-user> \
  --start-time 2026-05-01 --end-time 2026-05-06 \
  --query 'Events[*].{Time:EventTime,Name:EventName,User:Username,Source:EventSource}' \
  --output table

# Look up events for a specific resource
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=<resource-id> \
  --output table

# Look up events by event name
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteBucket \
  --output table
```

## Query CloudTrail in S3 with Athena

```sql
-- Partition table by account/region/date
CREATE EXTERNAL TABLE cloudtrail_logs (
  eventVersion STRING, ...
)
PARTITIONED BY (region string, year string, month string, day string)
...

-- Find all failed API calls
SELECT eventTime, eventName, errorCode, errorMessage, userIdentity.arn
FROM cloudtrail_logs
WHERE errorCode IS NOT NULL
  AND year='2026' AND month='05'
ORDER BY eventTime DESC
LIMIT 100;

-- Who deleted a resource?
SELECT eventTime, userIdentity.arn, requestParameters
FROM cloudtrail_logs
WHERE eventName = 'DeleteSecurityGroup'
  AND year='2026' AND month='05';
```

## CloudTrail Lake Queries

```bash
# Run a query against CloudTrail Lake
aws cloudtrail start-query \
  --query-statement "SELECT eventTime, eventName, userIdentity.arn FROM <event-data-store-arn> WHERE errorCode IS NOT NULL LIMIT 100"

# Get query results
aws cloudtrail get-query-results --query-id <query-id>
```

## Monitoring with CloudWatch

```bash
# Create a metric filter for root account usage
aws logs put-metric-filter \
  --log-group-name <cloudtrail-log-group> \
  --filter-name RootUsage \
  --filter-pattern '{ $.userIdentity.type = "Root" && $.userIdentity.invokedBy NOT EXISTS && $.eventType != "AwsServiceEvent" }' \
  --metric-transformations metricName=RootUsageCount,metricNamespace=CloudTrailMetrics,metricValue=1
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Trail not logging | `get-trail-status` → `IsLogging: false` | `aws cloudtrail start-logging --name <trail>` |
| Events missing for a region | Multi-region trail disabled | Enable `--is-multi-region-trail` |
| S3 delivery failing | S3 bucket policy | Verify CloudTrail has `s3:PutObject` permission on the log bucket |
| Event history empty | Recent API calls? | Event history only shows last 90 days; older events need Athena query |
