---
tags:
  - aws
  - troubleshooting
search:
  boost: 1.5
description: "Troubleshooting reference covering S3 Access Denied, IAM Permission Denied, RDS Connection Issues, VPC Flow Logs — Analysing Traffic, Lambda Timeout..."
---
# AWS — Troubleshooting

<div class="kb-summary">
Troubleshooting reference covering S3 Access Denied, IAM Permission Denied, RDS Connection Issues, VPC Flow Logs — Analysing Traffic, Lambda Timeout Issues.

*Applies to: AWS*
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known problems, symptoms, and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to AWS Support with the right data.</span>
</a>

</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
rds_connection_issues: "RDS Connection Issues" {shape: rectangle}
vpc_flow_logs_analysing_traffic: "VPC Flow Logs — Analysing Traffic" {shape: rectangle}
lambda_timeout_issues: "Lambda Timeout Issues" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> rds_connection_issues: investigate
symptom -> vpc_flow_logs_analysing_traffic: investigate
symptom -> lambda_timeout_issues: investigate
rds_connection_issues -> resolution
vpc_flow_logs_analysing_traffic -> resolution
lambda_timeout_issues -> resolution
```

## RDS Connection Issues

```bash
# Check RDS security group
aws rds describe-db-instances --db-instance-identifier <db-id> \
    --query 'DBInstances[*].VpcSecurityGroups'

# Verify security group allows inbound on DB port from app subnet
aws ec2 describe-security-groups --group-ids <rds-sg-id>

# Check RDS status
aws rds describe-db-instances --db-instance-identifier <db-id> \
    --query 'DBInstances[*].[DBInstanceStatus,Endpoint]'

# If connection refused after failover:
aws rds describe-events --source-identifier <db-id> --duration 60
```


```text title="Expected output"
[
    {
        "GroupId": "sg-0a7f2c8e9d1b4f6c2",
        "Status": "active",
        "VpcSecurityGroupMemberships": [
            {
                "VpcSecurityGroupId": "sg-0a7f2c8e9d1b4f6c2",
                "Status": "active"
            }
        ]
    }
]

GROUP ID                DESCRIPTION                    VPC ID
sg-0a7f2c8e9d1b4f6c2   rds-mysql-prod-sg             vpc-0e3f8a2b1c9d7e4f5

INBOUND RULES:
IpProtocol    FromPort    ToPort    IpRange              Description
tcp           3306        3306      10.2.0.0/16          Allow MySQL from app subnet
tcp           3306        3306      10.3.0.0/16          Allow MySQL from backup subnet

[
    [
        "available",
        {
            "Address": "prod-mysql-01.c9akciq32.us-east-1.rds.amazonaws.com",
            "Port": 3306
        }
    ]
]

[
    {
        "Message": "DB instance restarted",
        "EventCategories": ["failover"],
        "SourceType": "db-instance",
        "Timestamp": "2024-01-15T14:32:18.000Z"
    },
    {
        "Message": "Failover completed successfully",
        "EventCategories": ["failover"],
        "SourceType": "db-instance",
        "Timestamp": "2024-01-15T14:35:22.000Z"
    }
]
```

!!! warning "Common errors"
    **`An error occurred (InvalidDBInstanceIdentifier.NotFound) when calling the DescribeDBInstances operation: DBInstance not found`** — Verify the `<db-id>` parameter matches the actual RDS instance identifier shown in the AWS console.
    **`An error occurred (InvalidGroup.NotFound) when calling the DescribeSecurityGroups operation: The security group 'sg-xxxxxxxx' does not exist`** — Confirm the `<rds-sg-id>` is correct and exists in the same region as your RDS instance.
    **`An error occurred (UnauthorizedOperation) when calling the DescribeDBInstances operation: User is not authorized to perform: rds:DescribeDBInstances`** — Add the `rds:DescribeDBInstances` and `ec2:DescribeSecurityGroups` permissions to your IAM user or role policy.
**Expected output:** Status query returns `["available", {"Address": "<endpoint>", "Port": <port>}]`. If status is `modifying`, `rebooting`, or `failing-over`, connection refusal is expected — wait for status to return to `available`.

## VPC Flow Logs — Analysing Traffic

```bash
# Query Flow Logs in CloudWatch Insights
# CloudWatch → Logs Insights → select flow log group
fields @timestamp, srcAddr, dstAddr, dstPort, action
| filter dstAddr = "<target-ip>" and action = "REJECT"
| sort @timestamp desc
| limit 50
```


```text title="Expected output"
@timestamp                    | srcAddr      | dstAddr      | dstPort | action
2024-01-15T14:32:18.456Z     | 10.2.45.67   | 203.0.113.42 | 443     | REJECT
2024-01-15T14:31:52.123Z     | 10.2.45.68   | 203.0.113.42 | 443     | REJECT
2024-01-15T14:31:29.789Z     | 10.2.46.12   | 203.0.113.42 | 22      | REJECT
2024-01-15T14:30:44.567Z     | 10.2.45.67   | 203.0.113.42 | 3306    | REJECT
2024-01-15T14:29:15.234Z     | 10.3.12.88   | 203.0.113.42 | 443     | REJECT
2024-01-15T14:28:33.901Z     | 10.2.45.99   | 203.0.113.42 | 443     | REJECT
2024-01-15T14:27:11.645Z     | 10.2.47.33   | 203.0.113.42 | 80      | REJECT
...
(44 more results)
```

!!! warning "Common errors"
    **`The specified log group does not exist.`** — Verify the Flow Logs log group name exists in CloudWatch Logs and that the IAM principal has `logs:DescribeLogGroups` permission.
    **`Syntax error in query at position X`** — Check that the target IP in the filter is quoted as a string and that field names like `@timestamp` are correctly prefixed with `@`.
    **`Query returned no results`** — Confirm that Flow Logs are enabled on the VPC/subnet/ENI, that the log group is receiving data, and that the target IP and time range match actual traffic.
## Lambda Timeout Issues

```bash
# Check function configuration
aws lambda get-function-configuration --function-name <name> \
    --query '[Timeout, MemorySize, VpcConfig]'

# View X-Ray trace for a slow invocation
aws xray get-service-graph --start-time $(date -d '1 hour ago' +%s) --end-time $(date +%s)

# Check CloudWatch Logs for errors
aws logs get-log-events --log-group-name /aws/lambda/<name> \
    --log-stream-name <stream> --start-from-head
```


```text title="Expected output"
[
    300,
    256,
    {
        "SubnetIds": [
            "subnet-0a1b2c3d",
            "subnet-4e5f6g7h"
        ],
        "SecurityGroupIds": [
            "sg-0123456789abcdef0"
        ],
        "VpcId": "vpc-12345678"
    }
]
{
    "StartTime": 1699564800.0,
    "EndTime": 1699568400.0,
    "Services": [
        {
            "ReferenceId": 0,
            "Name": "lambda",
            "Names": ["my-function"],
            "State": "active",
            "Type": "aws::lambda::function"
        }
    ],
    "EdgeList": []
}
{
    "events": [
        {
            "timestamp": 1699568123456,
            "message": "START RequestId: a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        },
        {
            "timestamp": 1699568124123,
            "message": "Processing event: {\"key\": \"value\"}"
        },
        {
            "timestamp": 1699568125789,
            "message": "END RequestId: a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        }
    ],
    "nextForwardToken": "f/36028797018948608",
    "nextBackwardToken": "b/36028797018948608"
}
```

!!! warning "Common errors"
    **`An error occurred (ResourceNotFoundException) when calling the GetFunctionConfiguration operation: The resource you requested does not exist.`** — Verify the function name is correct and exists in the current AWS region with `aws lambda list-functions`.
    **`An error occurred (AccessDenied) when calling the GetLogEvents operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: logs:GetLogEvents`** — Add the `logs:GetLogEvents` permission to your IAM user or role policy.
    **`An error occurred (InvalidParameterException) when calling the GetServiceGraph operation: 1 validation error detected: Value at 'startTime' failed to satisfy constraint: Member must not be null`** — Ensure the `date` command is installed and working; on macOS use `date -v-1H +%s` instead of `date -d '1 hour ago' +%s`.