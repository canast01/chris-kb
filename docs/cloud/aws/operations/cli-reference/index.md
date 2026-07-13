---
tags:
  - aws
  - operations
description: "CLI Reference reference covering EC2, S3, IAM, RDS, CloudWatch and 3 more sections."
---
# AWS — CLI Reference

<div class="kb-summary">
CLI Reference reference covering EC2, S3, IAM, RDS, CloudWatch and 3 more sections.

*Applies to: AWS*
</div>

---

```d2
direction: down

s3: "S3" {shape: rectangle}
iam: "IAM" {shape: rectangle}
rds: "RDS" {shape: rectangle}
cloudwatch: "CloudWatch" {shape: rectangle}
vpc_networking: "VPC / Networking" {shape: rectangle}
eks: "EKS" {shape: rectangle}

s3 -> iam: uses
iam -> rds: uses
rds -> cloudwatch: uses
cloudwatch -> vpc_networking: uses
vpc_networking -> eks: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## S3

```bash
# List buckets
aws s3 ls

# List contents of a bucket
aws s3 ls s3://my-bucket/ --recursive --human-readable

# Copy files
aws s3 cp file.txt s3://my-bucket/path/
aws s3 cp s3://my-bucket/path/file.txt ./

# Sync directory
aws s3 sync ./local-dir s3://my-bucket/prefix/ --delete

# Remove object
aws s3 rm s3://my-bucket/path/file.txt

# Check bucket policy
aws s3api get-bucket-policy --bucket my-bucket

# Get bucket size
aws s3api list-objects-v2 --bucket my-bucket \
  --query 'sum(Contents[*].Size)' --output text | \
  awk '{printf "%.2f GB\n", $1/1024/1024/1024}'
```


```text title="Expected output"
2024-01-15 10:23:45 my-bucket
2024-01-15 10:24:12 my-bucket-backups
2024-01-15 10:25:33 my-bucket-logs

2024-01-10 14:22:15    4.2 KiB logs/app.log
2024-01-10 14:22:16    1.8 MiB data/export.csv
2024-01-10 14:22:17  256.5 MiB archive/backup.tar.gz
2024-01-10 14:22:18   12.3 KiB config/settings.json
...

upload: ./file.txt to s3://my-bucket/path/file.txt
download: s3://my-bucket/path/file.txt to ./file.txt

upload: ./local-dir/config.yaml to s3://my-bucket/prefix/config.yaml
upload: ./local-dir/data.json to s3://my-bucket/prefix/data.json
delete: s3://my-bucket/prefix/old-file.txt
delete: s3://my-bucket/prefix/temp.log

delete: s3://my-bucket/path/file.txt

{
    "Policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":\"*\",\"Action\":\"s3:GetObject\",\"Resource\":\"arn:aws:s3:::my-bucket/*\"}]}"
}

487.65 GB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (NoSuchBucket) when calling the ListObjects operation: The specified bucket does not exist` | Verify the bucket name is correct and exists in your AWS account with `aws s3 ls`. |
    | `An error occurred (AccessDenied) when calling the GetBucketPolicy operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: s3:GetBucketPolicy on resource` | Ensure your IAM user has `s3:GetBucketPolicy` permission in their policy document. |
    | `fatal error: An error occurred (InvalidAccessKeyId) when calling the ListBuckets operation: The AWS Access Key Id you provided does not exist in our records.` | Run `aws configure` to verify your AWS credentials are correct and current. |
---

## IAM

```bash
# List users
aws iam list-users --query 'Users[*].[UserName,CreateDate,PasswordLastUsed]' --output table

# List roles
aws iam list-roles --query 'Roles[*].[RoleName,RoleId,CreateDate]' --output table

# Get effective policies for a user
aws iam list-attached-user-policies --user-name myuser
aws iam list-user-policies --user-name myuser  # inline policies

# Simulate policy evaluation
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<account>:user/myuser \
  --action-names s3:GetObject ec2:DescribeInstances \
  --query 'EvaluationResults[*].[EvalActionName,EvalDecision]' \
  --output table

# Rotate access key
aws iam create-access-key --user-name myuser
aws iam delete-access-key --user-name myuser --access-key-id AKIA...
```


```text title="Expected output"
# List users
---------------------------------------------------------------------------
|                             ListUsers                                  |
+-----------+---------------------------+---------------------------+
| UserName  |       CreateDate           |    PasswordLastUsed       |
+-----------+---------------------------+---------------------------+
| alice     | 2023-01-15T10:22:33+00:00 | 2024-11-20T14:05:12+00:00 |
| bob       | 2023-03-22T08:15:47+00:00 | 2024-11-18T09:33:44+00:00 |
| myuser    | 2023-06-10T16:44:21+00:00 | None                      |
| svc-app   | 2024-02-01T12:00:00+00:00 | None                      |
+-----------+---------------------------+---------------------------+

# List roles
---------------------------------------------------------------------------
|                           ListRoles                                    |
+------------------+------------------+---------------------------+
|    RoleName      |      RoleId      |       CreateDate          |
+------------------+------------------+---------------------------+
| EC2-Admin        | AIDA2K7X9M2Q5P8R | 2023-02-14T11:30:22+00:00 |
| Lambda-Exec      | AIDA3N8Y0L4S6T9V | 2023-05-20T13:45:10+00:00 |
| CrossAccount     | AIDA1J2K3L4M5N6O | 2024-01-08T09:12:55+00:00 |
+------------------+------------------+---------------------------+

{
    "AttachedPolicies": [
        {
            "PolicyName": "AmazonS3ReadOnlyAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
        },
        {
            "PolicyName": "CloudWatchLogsFullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
        }
    ]
}
{
    "UserPolicyList": []
}

---------------------------------------------------------------------------
|                      SimulatePrincipalPolicy                           |
+---------------------+---------------+
|   EvalActionName    |  EvalDecision |
+---------------------+---------------+
| s3:GetObject        | allowed       |
| ec2:DescribeInstances | denied      |
+---------------------+---------------+

{
    "AccessKey": {
        "UserName": "myuser",
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "Status": "Active",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "CreateDate": "2024-11-21T10:15:33+00:00"
    }
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`An error occurred (NoSuchEntity) when calling the ListAttachedUserPolicies operation: The user with name myuser cannot
---

## RDS

```bash
# List instances
aws rds describe-db-instances \
  --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus,Engine,DBInstanceClass,Endpoint.Address]' \
  --output table

# Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier prod-mysql \
  --db-snapshot-identifier prod-mysql-manual-$(date +%Y-%m-%d)

# Modify instance (apply immediately or at maintenance window)
aws rds modify-db-instance \
  --db-instance-identifier prod-mysql \
  --db-instance-class db.r6g.xlarge \
  --apply-immediately

# List pending maintenance
aws rds describe-pending-maintenance-actions \
  --query 'PendingMaintenanceActions[*].[ResourceIdentifier,PendingMaintenanceActionDetails[0].Action]' \
  --output table
```


```text title="Expected output"
DBInstanceIdentifier    | DBInstanceStatus | Engine | DBInstanceClass | Endpoint.Address
------------------------+-----------------+--------+-----------------+----------------------------------
prod-mysql              | available       | mysql  | db.t3.medium    | prod-mysql.c9akciq32.us-east-1.rds.amazonaws.com
staging-postgres        | available       | postgres| db.t3.small     | staging-postgres.c9akciq32.us-east-1.rds.amazonaws.com
analytics-aurora        | available       | aurora-mysql| db.r6g.large | analytics-aurora.cluster-c9akciq32.us-east-1.rds.amazonaws.com

{
    "DBSnapshotIdentifier": "prod-mysql-manual-2024-01-15",
    "DBInstanceIdentifier": "prod-mysql",
    "SnapshotCreateTime": "2024-01-15T14:32:18.123000+00:00",
    "SnapshotType": "manual",
    "Status": "creating",
    "Engine": "mysql"
}

{
    "DBInstanceIdentifier": "prod-mysql",
    "PendingModifiedValues": {
        "DBInstanceClass": "db.r6g.xlarge"
    },
    "ApplyImmediately": true
}

ResourceIdentifier      | Action
------------------------+------------------------------------------
arn:aws:rds:us-east-1:123456789012:db:prod-mysql | system-update
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (DBInstanceNotFound) when calling the DescribeDBInstances operation: DBInstance not found` | Verify the DB instance identifier exists in your region using `aws rds describe-db-instances --region <region>`. |
    | `An error occurred (InvalidDBInstanceState) when calling the ModifyDBInstance operation: Invalid DB instance state` | Wait for the instance to reach "available" status before modifying; check current status with `aws rds describe-db-instances --db-instance-identifier prod-mysql`. |
    | `An error occurred (AccessDenied) when calling the CreateDBSnapshot operation: User is not authorized to perform: rds:CreateDBSnapshot` | Ensure your IAM user/role has the `rds:CreateDBSnapshot` permission attached in your AWS account. |
---

## CloudWatch

```bash
# List alarms in ALARM state
aws cloudwatch describe-alarms \
  --state-value ALARM \
  --query 'MetricAlarms[*].[AlarmName,StateReason,MetricName]' \
  --output table

# Get metric statistics (EC2 CPU last hour)
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-0abc123 \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average \
  --query 'Datapoints[*].[Timestamp,Average]' \
  --output table

# Get CloudWatch Logs
aws logs get-log-events \
  --log-group-name /aws/lambda/my-function \
  --log-stream-name <stream-name> \
  --start-from-head \
  --query 'events[*].[timestamp,message]' \
  --output text

# Tail logs (filter)
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "ERROR" \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' \
  --output text
```


```text title="Expected output"
------------------------------------------------------------------------------------------
|                                    MetricAlarms                                       |
|------------------------------------------------------------------------------------------
|  web-api-high-cpu                 |  Threshold Crossed: 1 datapoint [85.2 (12/15/2024 14:32:00 UTC)] was greater than the threshold (80.0).  |  CPUUtilization  |
|  rds-db-connections               |  Threshold Crossed: 1 datapoint [450 (12/15/2024 14:28:00 UTC)] was greater than the threshold (400.0).  |  DatabaseConnections  |
|  elb-unhealthy-hosts              |  Threshold Crossed: 1 datapoint [2 (12/15/2024 14:25:00 UTC)] was greater than the threshold (0.0).  |  UnHealthyHostCount  |
------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------
|                              Datapoints                                               |
|------------------------------------------------------------------------------------------
|  2024-12-15T14:55:00Z             |  72.4  |
|  2024-12-15T14:50:00Z             |  68.9  |
|  2024-12-15T14:45:00Z             |  75.1  |
|  2024-12-15T14:40:00Z             |  71.3  |
------------------------------------------------------------------------------------------

2024-12-15T14:32:15.123Z	[INFO] Lambda function invoked with requestId: a1b2c3d4-e5f6-7890-abcd-ef1234567890
2024-12-15T14:32:16.456Z	[INFO] Processing event from SQS queue
2024-12-15T14:32:17.789Z	[DEBUG] Payload size: 2048 bytes

2024-12-15T14:31:42.234Z	[ERROR] Database connection timeout after 30s
2024-12-15T14:31:43.567Z	[ERROR] Retry attempt 1 of 3 failed
2024-12-15T14:31:44.890Z	[ERROR] Max retries exceeded, aborting request
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the DescribeAlarms operation: The alarm does not exist.` | Verify the alarm name exists in your region with `aws cloudwatch describe-alarms --alarm-names <name>`. |
    | `An error occurred (InvalidParameterValue) when calling the GetMetricStatistics operation: 1 validation error detected: Value '<stream-name>' at 'logStreamName' failed to satisfy constraint` | Replace `<stream-name>` with an actual log stream name from `aws logs describe-log-streams --log-group-name /aws/lambda/my-function`. |
---

## VPC / Networking

```bash
# List VPCs
aws ec2 describe-vpcs \
  --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0],IsDefault]' \
  --output table

# List subnets
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=vpc-0abc123" \
  --query 'Subnets[*].[SubnetId,CidrBlock,AvailabilityZone,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# List security groups
aws ec2 describe-security-groups \
  --filters "Name=vpc-id,Values=vpc-0abc123" \
  --query 'SecurityGroups[*].[GroupId,GroupName,Description]' \
  --output table

# Show security group rules
aws ec2 describe-security-group-rules \
  --filters "Name=group-id,Values=sg-0abc123" \
  --query 'SecurityGroupRules[*].[IsEgress,IpProtocol,FromPort,ToPort,CidrIpv4,Description]' \
  --output table
```


```text title="Expected output"
---------------------------------------------------------------------------
|                              DescribeVpcs                              |
+-----------+------------------+---------------+------------+
| VpcId     | CidrBlock        | Name          | IsDefault  |
+-----------+------------------+---------------+------------+
| vpc-0abc123 | 10.0.0.0/16    | production    | False      |
| vpc-1def456 | 10.1.0.0/16    | staging       | False      |
| vpc-2ghi789 | 172.31.0.0/16  | None          | True       |
+-----------+------------------+---------------+------------+

---------------------------------------------------------------------------
|                           DescribeSubnets                              |
+-----------+------------------+------------------+---------------+
| SubnetId  | CidrBlock        | AvailabilityZone | Name          |
+-----------+------------------+------------------+---------------+
| subnet-0a1b2c3d | 10.0.1.0/24  | us-east-1a       | prod-public-1a |
| subnet-0d4e5f6g | 10.0.2.0/24  | us-east-1b       | prod-public-1b |
| subnet-0h7i8j9k | 10.0.11.0/24 | us-east-1a       | prod-private-1a |
+-----------+------------------+------------------+---------------+

---------------------------------------------------------------------------
|                      DescribeSecurityGroups                            |
+-----------+------------------+----------------------------------+
| GroupId   | GroupName        | Description                      |
+-----------+------------------+----------------------------------+
| sg-0abc123 | prod-web-sg     | Security group for web tier      |
| sg-0def456 | prod-db-sg      | Security group for RDS MySQL     |
| sg-0ghi789 | prod-alb-sg     | ALB ingress security group       |
+-----------+------------------+----------------------------------+

---------------------------------------------------------------------------
|                    DescribeSecurityGroupRules                          |
+----------+----------+----------+--------+-----------+------------------+
| IsEgress | IpProtocol | FromPort | ToPort | CidrIpv4  | Description      |
+----------+----------+----------+--------+-----------+------------------+
| False    | tcp      | 80       | 80     | 0.0.0.0/0 | Allow HTTP       |
| False    | tcp      | 443      | 443    | 0.0.0.0/0 | Allow HTTPS      |
| False    | tcp      | 3306     | 3306   | 10.0.0.0/16 | MySQL from app |
| True     | -1       | -1       | -1     | 0.0.0.0/0 | Allow all egress |
+----------+----------+----------+--------+-----------+------------------+
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (UnauthorizedOperation) when calling the DescribeVpcs operation: You are not authorized to perform: ec2:DescribeVpcs on resource` | Ensure your IAM user/role has the `ec2:Describe*` permissions attached via an appropriate policy. |
    **`An error occurred (InvalidParameterValue
---

## EKS

```bash
# List clusters
aws eks list-clusters

# Update kubeconfig
aws eks update-kubeconfig --name my-cluster --region eu-west-1

# List node groups
aws eks list-nodegroups --cluster-name my-cluster

# Describe node group
aws eks describe-nodegroup --cluster-name my-cluster --nodegroup-name workers \
  --query 'nodegroup.[nodegroupName,status,scalingConfig,instanceTypes]'

# Update node group scaling
aws eks update-nodegroup-config \
  --cluster-name my-cluster \
  --nodegroup-name workers \
  --scaling-config minSize=2,maxSize=10,desiredSize=4
```


```text title="Expected output"
{
    "clusters": [
        "my-cluster",
        "staging-cluster",
        "prod-eu-cluster"
    ]
}
Added new context arn:aws:eks:eu-west-1:123456789012:cluster/my-cluster to /home/user/.kube/config
{
    "nodegroups": [
        "workers",
        "gpu-nodes",
        "spot-instances"
    ]
}
[
    "workers",
    "ACTIVE",
    {
        "minSize": 2,
        "maxSize": 8,
        "desiredSize": 3
    },
    [
        "t3.large",
        "t3.xlarge"
    ]
]
{
    "nodegroup": {
        "nodegroupName": "workers",
        "status": "UPDATING",
        "scalingConfig": {
            "minSize": 2,
            "maxSize": 10,
            "desiredSize": 4
        }
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the ListClusters operation: No clusters found in region eu-west-1` | Verify the AWS region is correct with `aws configure get region` or explicitly set `--region` in the command. |
    | `An error occurred (InvalidParameterException) when calling the UpdateNodegroupConfig operation: Desired size must be between minSize and maxSize` | Ensure desiredSize (4) is within the range of minSize (2) and maxSize (10). |
    | `Unable to locate credentials` | Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. |
---

## SSM — Session Manager

```bash
# Start SSM session to an EC2 instance (no SSH/bastion needed)
aws ssm start-session --target i-0abc123def456789

# Run command on instance(s)
aws ssm send-command \
  --instance-ids i-0abc123 \
  --document-name "AWS-RunShellScript" \
  --parameters commands='["df -h","free -h"]' \
  --query 'Command.CommandId' --output text

# Get command result
aws ssm get-command-invocation \
  --command-id <command-id> \
  --instance-id i-0abc123 \
  --query '[Status,StandardOutputContent]' \
  --output text
```


```text title="Expected output"
Starting session with SSM Agent v3.1.1060.0
Connected to instance i-0abc123def456789

d4f8c2a1-9e7b-4c3d-b1a2-5f6e7d8c9b0a

Success  Filesystem     Size  Used Avail Use% Mounted on
/dev/xvda1      20G  4.2G   15G  22% /
tmpfs           1.9G     0  1.9G   0% /dev/shm
              total        used        free      shared  buff/cache   available
              1953Mi       287Mi      1401Mi        0Mi       264Mi      1548Mi
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidInstanceID.NotFound) when calling the StartSession operation: The instance ID 'i-0abc123def456789' does not exist or you do not have permission to access it.` | Verify the instance ID is correct and the IAM role has `ssm:StartSession` permissions. |
    | `An error occurred (InvalidDocument) when calling the SendCommand operation: The document 'AWS-RunShellScript' does not exist in the account.` | Use `aws ssm describe-document --name AWS-RunShellScript` to confirm the document exists in your region. |
    | `An error occurred (InvalidCommandId.NotFound) when calling the GetCommandInvocation operation: The command ID 'd4f8c2a1-9e7b-4c3d-b1a2-5f6e7d8c9b0a' does not exist.` | Replace `<command-id>` with the actual command ID from the send-command output and wait 2-3 seconds for the command to execute. |
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Aws — Procedures](../procedures/)
- [Aws — Scripts](../scripts/)
- [Aws — Health Checks](../health-checks/)
