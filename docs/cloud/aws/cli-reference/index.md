---
tags:
  - aws
description: "AWS CLI Reference reference covering EC2 — Instances, EC2 — Images, Volumes & Snapshots, S3, VPC & Networking, CloudWatch and 5 more sections."
---
# AWS CLI Reference

<div class="kb-summary">
AWS CLI Reference reference covering EC2 — Instances, EC2 — Images, Volumes & Snapshots, S3, VPC & Networking, CloudWatch and 5 more sections.

*Applies to: AWS*
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="ec2-instances/">
  <strong>EC2 Instances</strong>
  <span>Instance lifecycle, describe, start, stop, and run commands.</span>
</a>

<a class="kb-card" href="ec2-storage/">
  <strong>EC2 Storage</strong>
  <span>EBS volumes, snapshots, and AMI management.</span>
</a>

<a class="kb-card" href="s3/">
  <strong>S3</strong>
  <span>Bucket and object operations, sync, and S3 API commands.</span>
</a>

<a class="kb-card" href="iam/">
  <strong>IAM</strong>
  <span>Users, roles, policies, and STS assume-role commands.</span>
</a>

<a class="kb-card" href="vpc/">
  <strong>VPC & Networking</strong>
  <span>VPC, subnets, route tables, security groups, and gateways.</span>
</a>

<a class="kb-card" href="cloudwatch/">
  <strong>CloudWatch</strong>
  <span>Alarms, metrics, and log group commands.</span>
</a>

<a class="kb-card" href="cloudformation/">
  <strong>CloudFormation</strong>
  <span>Stack lifecycle, events, and template validation.</span>
</a>

<a class="kb-card" href="rds/">
  <strong>RDS</strong>
  <span>Database instance management and snapshot commands.</span>
</a>

<a class="kb-card" href="eks/">
  <strong>EKS</strong>
  <span>Cluster management, kubeconfig, and node group commands.</span>
</a>

<a class="kb-card" href="ssm/">
  <strong>SSM</strong>
  <span>Session Manager, Run Command, and Parameter Store.</span>
</a>

<a class="kb-card" href="lambda/">
  <strong>Lambda</strong>
  <span>Function management, invocation, and deployment commands.</span>
</a>

</div>

---

## S3

S3 (Simple Storage Service) is AWS's object storage — it stores files (objects) in containers (buckets). Unlike a filesystem, there are no folders — just keys (paths) that look like folder structures. S3 is extremely durable and cheap.

```bash
# Buckets
aws s3 ls                          # list all your buckets
aws s3 ls s3://<bucket>/           # list contents of a bucket
aws s3 mb s3://<bucket>            # make bucket
aws s3 rb s3://<bucket> --force    # remove bucket (and all contents)

# Objects (files)
aws s3 cp <local_file> s3://<bucket>/<key>       # upload
aws s3 cp s3://<bucket>/<key> <local_file>       # download
aws s3 mv s3://<bucket>/<key> s3://<bucket>/<new_key>
aws s3 rm s3://<bucket>/<key>
aws s3 rm s3://<bucket>/<prefix>/ --recursive    # delete all objects under a path

# Sync (like rsync for S3 — only copies changed files)
aws s3 sync <local_dir> s3://<bucket>/<prefix>
aws s3 sync s3://<bucket>/<prefix> <local_dir>
aws s3 sync --delete s3://<source> s3://<dest>   # mirror — deletes files not in source

# S3 API (for versioning, policies, lifecycle rules)
aws s3api get-bucket-versioning --bucket <bucket>
aws s3api put-bucket-versioning --bucket <bucket> --versioning-configuration Status=Enabled
aws s3api get-bucket-policy --bucket <bucket>
aws s3api list-object-versions --bucket <bucket>
aws s3api put-bucket-lifecycle-configuration --bucket <bucket> --lifecycle-configuration file://lifecycle.json
```


```text title="Expected output"
2024-01-15 10:23:45 prod-app-backups
2024-01-14 16:47:12 staging-logs
2024-01-12 09:15:33 dev-scratch
2024-01-10 14:22:01 archive-2023

PRE logs/
PRE config/
2024-01-15T08:30:22.000Z       4521 app.log
2024-01-15T07:45:11.000Z     156234 metrics.json
2024-01-14T23:12:05.000Z      89012 backup.tar.gz

upload: ./data.csv to s3://prod-app-backups/exports/data.csv
download: s3://prod-app-backups/exports/data.csv to ./data.csv

{
    "Status": "Enabled",
    "MFADelete": "Disabled"
}

{
    "Rules": [
        {
            "ID": "archive-old-logs",
            "Status": "Enabled",
            "Prefix": "logs/",
            "Transitions": [
                {
                    "Days": 30,
                    "StorageClass": "GLACIER"
                }
            ]
        }
    ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (NoSuchBucket) when calling the ListObjects operation: The specified bucket does not exist` | Verify the bucket name is correct and exists in your AWS account with `aws s3 ls`. |
    | `An error occurred (AccessDenied) when calling the PutObject operation: Access Denied` | Ensure your IAM user/role has `s3:PutObject` permission for that bucket in the bucket policy or IAM policy. |
    | `fatal error: An error occurred (InvalidArgument) when calling the PutBucketLifecycleConfiguration operation: Invalid lifecycle configuration` | Validate the JSON syntax in your lifecycle.json file and ensure it contains required fields like `Rules` and `Status`. |
---

## VPC & Networking

VPC (Virtual Private Cloud) is your private network in AWS. Subnets divide the VPC into segments. Route tables control where traffic goes. Internet gateways provide internet access. Elastic IPs are static public IP addresses.

```bash
# VPCs (your isolated private network in AWS)
aws ec2 describe-vpcs
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 delete-vpc --vpc-id <id>

# Subnets (segments of a VPC — typically split by AZ and public/private)
aws ec2 describe-subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc_id>"
aws ec2 create-subnet --vpc-id <id> --cidr-block 10.0.1.0/24 --availability-zone us-east-1a

# Route tables (rules for where network traffic should go)
aws ec2 describe-route-tables
aws ec2 create-route --route-table-id <rt_id> --destination-cidr-block 0.0.0.0/0 --gateway-id <igw_id>

# Internet gateways (connects your VPC to the public internet)
aws ec2 describe-internet-gateways
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --internet-gateway-id <igw_id> --vpc-id <vpc_id>

# Elastic IPs (static public IP addresses that persist independent of instances)
aws ec2 describe-addresses
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id <id> --allocation-id <eip_id>
aws ec2 release-address --allocation-id <eip_id>
```


```text title="Expected output"
{
    "Vpcs": [
        {
            "VpcId": "vpc-0a1b2c3d4e5f6g7h8",
            "CidrBlock": "10.0.0.0/16",
            "State": "available",
            "OwnerId": "123456789012"
        },
        {
            "VpcId": "vpc-1x2y3z4a5b6c7d8e9",
            "CidrBlock": "172.31.0.0/16",
            "State": "available",
            "OwnerId": "123456789012"
        }
    ]
}

{
    "Vpc": {
        "VpcId": "vpc-9f8e7d6c5b4a3z2y1",
        "CidrBlock": "10.0.0.0/16",
        "State": "pending",
        "OwnerId": "123456789012"
    }
}

{
    "Subnets": [
        {
            "SubnetId": "subnet-0a1b2c3d4e5f6g7h8",
            "VpcId": "vpc-0a1b2c3d4e5f6g7h8",
            "CidrBlock": "10.0.1.0/24",
            "AvailabilityZone": "us-east-1a",
            "State": "available"
        }
    ]
}

{
    "RouteTables": [
        {
            "RouteTableId": "rtb-0a1b2c3d4e5f6g7h8",
            "VpcId": "vpc-0a1b2c3d4e5f6g7h8",
            "Routes": [
                {
                    "DestinationCidrBlock": "10.0.0.0/16",
                    "GatewayId": "local",
                    "State": "active"
                }
            ]
        }
    ]
}

{
    "InternetGateways": [
        {
            "InternetGatewayId": "igw-0a1b2c3d4e5f6g7h8",
            "Attachments": [
                {
                    "VpcId": "vpc-0a1b2c3d4e5f6g7h8",
                    "State": "available"
                }
            ]
        }
    ]
}

{
    "Addresses": [
        {
            "InstanceId": "i-0a1b2c3d4e5f6g7h8",
            "PublicIp": "203.0.113.45",
            "AllocationId": "eipalloc-0a1b2c3d4e5f6g7h8",
            "Domain": "vpc",
            "AssociationId": "eipassoc-2bsum4arq"
        }
    ]
}

{
    "PublicIp": "198.51.100.72",
    "AllocationId": "eipalloc-1x2y3z4a5b6c7d8e9",
```
---

## CloudWatch

CloudWatch is AWS's monitoring and observability service. Metrics are numeric measurements (e.g., CPU %). Alarms trigger actions when metrics cross thresholds. Log groups store application and service logs.

```bash
# Alarms (trigger notifications or auto-scaling when a metric threshold is breached)
aws cloudwatch describe-alarms
aws cloudwatch describe-alarms --state-value ALARM
aws cloudwatch set-alarm-state --alarm-name <name> --state-value OK --state-reason "manual reset"

# Metrics (numeric measurements for AWS services and custom apps)
aws cloudwatch list-metrics --namespace AWS/EC2
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=<id> \
  --start-time $(date -u -d '1 hour ago' +%FT%TZ) \
  --end-time $(date -u +%FT%TZ) \
  --period 300 --statistics Average

# Logs (centralized log storage for applications and AWS services)
aws logs describe-log-groups
aws logs describe-log-streams --log-group-name <group>
aws logs get-log-events --log-group-name <group> --log-stream-name <stream>
aws logs tail <log_group> --follow             # live tail (like tail -f for cloud logs)
aws logs filter-log-events --log-group-name <group> --filter-pattern "ERROR"
```


```text title="Expected output"
{
    "MetricAlarms": [
        {
            "AlarmName": "prod-api-cpu-high",
            "MetricName": "CPUUtilization",
            "Namespace": "AWS/EC2",
            "Statistic": "Average",
            "Period": 300,
            "EvaluationPeriods": 2,
            "Threshold": 80.0,
            "ComparisonOperator": "GreaterThanThreshold",
            "StateValue": "OK",
            "StateUpdatedTimestamp": "2024-01-15T14:32:10.000Z"
        },
        {
            "AlarmName": "rds-connections-warning",
            "MetricName": "DatabaseConnections",
            "Namespace": "AWS/RDS",
            "StateValue": "ALARM",
            "StateUpdatedTimestamp": "2024-01-15T13:45:22.000Z"
        }
    ]
}

{
    "MetricAlarms": [
        {
            "AlarmName": "rds-connections-warning",
            "StateValue": "ALARM",
            "StateReason": "Threshold Crossed: 1 out of 1 datapoints was greater than the threshold (85.0)."
        }
    ]
}

(no output — command completes silently)

{
    "Metrics": [
        {
            "Namespace": "AWS/EC2",
            "MetricName": "CPUUtilization",
            "Dimensions": [{"Name": "InstanceId", "Value": "i-0a1b2c3d4e5f6g7h8"}]
        },
        {
            "Namespace": "AWS/EC2",
            "MetricName": "NetworkIn",
            "Dimensions": [{"Name": "InstanceId", "Value": "i-0a1b2c3d4e5f6g7h8"}]
        }
    ]
}

{
    "Label": "CPUUtilization",
    "Datapoints": [
        {"Timestamp": "2024-01-15T14:00:00Z", "Average": 42.5},
        {"Timestamp": "2024-01-15T14:05:00Z", "Average": 38.2},
        {"Timestamp": "2024-01-15T14:10:00Z", "Average": 45.1}
    ]
}

{
    "logGroups": [
        {"logGroupName": "/aws/lambda/auth-service", "creationTime": 1705334400000, "retentionInDays": 7},
        {"logGroupName": "/aws/ecs/prod-api", "creationTime": 1705248000000, "retentionInDays": 30},
        {"logGroupName": "/aws/rds/mysql-prod", "creationTime": 1704988800000}
    ]
}

{
    "logStreams": [
        {"logStreamName": "2024/01/15/[$LATEST]a1b2c3d4e5f6g7h8", "creationTime": 1705334410000, "firstEventTimestamp": 1705334415000, "
```
---

## CloudFormation

CloudFormation is AWS's Infrastructure as Code service. You define your infrastructure in a YAML or JSON template, and CloudFormation creates, updates, or deletes the resources. A stack is one deployment of a template.

```bash
# Stacks (a running deployment of a CloudFormation template)
aws cloudformation list-stacks
aws cloudformation describe-stacks --stack-name <name>
aws cloudformation create-stack \
  --stack-name <name> \
  --template-body file://template.yaml \
  --parameters ParameterKey=Env,ParameterValue=prod
aws cloudformation update-stack --stack-name <name> --template-body file://template.yaml
aws cloudformation delete-stack --stack-name <name>

# Stack status and events (useful for debugging failed deployments)
aws cloudformation describe-stack-events --stack-name <name>
aws cloudformation wait stack-create-complete --stack-name <name>

# Validate a template before deploying (catches syntax errors)
aws cloudformation validate-template --template-body file://template.yaml
```


```text title="Expected output"
{
    "StackSummaries": [
        {
            "StackName": "prod-api-stack",
            "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/prod-api-stack/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "StackStatus": "CREATE_COMPLETE",
            "CreationTime": "2024-01-15T10:32:45.123Z"
        },
        {
            "StackName": "dev-database-stack",
            "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/dev-database-stack/f9e8d7c6-b5a4-3210-fedc-ba9876543210",
            "StackStatus": "UPDATE_IN_PROGRESS",
            "CreationTime": "2024-01-10T14:22:10.456Z"
        }
    ]
}

{
    "Stacks": [
        {
            "StackName": "prod-api-stack",
            "StackStatus": "CREATE_COMPLETE",
            "Parameters": [
                {
                    "ParameterKey": "Env",
                    "ParameterValue": "prod"
                }
            ],
            "CreationTime": "2024-01-15T10:32:45.123Z"
        }
    ]
}

{
    "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/prod-api-stack/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}

{
    "StackEvents": [
        {
            "EventId": "prod-api-stack-CREATE_COMPLETE-2024-01-15T10:35:22.123Z",
            "StackName": "prod-api-stack",
            "LogicalResourceId": "prod-api-stack",
            "ResourceStatus": "CREATE_COMPLETE",
            "Timestamp": "2024-01-15T10:35:22.123Z"
        },
        {
            "EventId": "ApiGateway-CREATE_COMPLETE-2024-01-15T10:35:10.456Z",
            "LogicalResourceId": "ApiGateway",
            "ResourceStatus": "CREATE_COMPLETE",
            "Timestamp": "2024-01-15T10:35:10.456Z"
        }
    ]
}

{
    "Parameters": [
        {
            "ParameterKey": "Env",
            "DefaultValue": "dev"
        }
    ],
    "Description": "API deployment stack"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Template format error: Every Mappings object member must contain a String key and an object value.` | Validate your YAML syntax, especially in the Mappings section, using `aws cloudformation validate-template` before deployment. |
    | `User: arn:aws:iam::123456789012:user/admin is not authorized to perform: cloudformation:CreateStack` | Ensure your IAM user or role has the `cloudformation:* |
---

## RDS

RDS (Relational Database Service) is AWS's managed database service. It runs PostgreSQL, MySQL, SQL Server, and other engines on instances that AWS manages — you get a database endpoint without managing the OS or database software.

```bash
# Instances
aws rds describe-db-instances
aws rds describe-db-instances --db-instance-identifier <id>

# Start / stop / reboot
aws rds start-db-instance --db-instance-identifier <id>
aws rds stop-db-instance --db-instance-identifier <id>
aws rds reboot-db-instance --db-instance-identifier <id>

# Snapshots (automated point-in-time backups)
aws rds describe-db-snapshots
aws rds create-db-snapshot --db-instance-identifier <id> --db-snapshot-identifier <snap_name>
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier <new_id> \
  --db-snapshot-identifier <snap_name>
```


```text title="Expected output"
{
    "DBInstances": [
        {
            "DBInstanceIdentifier": "prod-mysql-01",
            "DBInstanceClass": "db.t3.medium",
            "Engine": "mysql",
            "DBInstanceStatus": "available",
            "MasterUsername": "admin",
            "AllocatedStorage": 100,
            "EngineVersion": "8.0.35",
            "DBInstanceArn": "arn:aws:rds:us-east-1:123456789012:db:prod-mysql-01"
        },
        {
            "DBInstanceIdentifier": "staging-postgres-02",
            "DBInstanceClass": "db.t3.small",
            "Engine": "postgres",
            "DBInstanceStatus": "available",
            "MasterUsername": "postgres",
            "AllocatedStorage": 50,
            "EngineVersion": "15.3",
            "DBInstanceArn": "arn:aws:rds:us-east-1:123456789012:db:staging-postgres-02"
        }
    ]
}

{
    "DBSnapshots": [
        {
            "DBSnapshotIdentifier": "prod-mysql-01-snap-20240115",
            "DBInstanceIdentifier": "prod-mysql-01",
            "SnapshotCreateTime": "2024-01-15T02:30:00.000Z",
            "Engine": "mysql",
            "Status": "available",
            "AllocatedStorage": 100,
            "DBSnapshotArn": "arn:aws:rds:us-east-1:123456789012:snapshot:prod-mysql-01-snap-20240115"
        }
    ]
}

{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-mysql-01",
        "DBInstanceStatus": "started"
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (DBInstanceNotFound) when calling the DescribeDBInstances operation: DBInstance not found` | Verify the instance identifier is correct with `aws rds describe-db-instances` and check you're querying the correct AWS region. |
    | `An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: DB instance is not in stopped state` | Confirm the instance is stopped before attempting to start it using `aws rds describe-db-instances --db-instance-identifier <id>`. |
    | `An error occurred (DBSnapshotAlreadyExists) when calling the CreateDBSnapshot operation: DB Snapshot already exists` | Use a unique snapshot identifier or delete the existing snapshot with `aws rds delete-db-snapshot --db-snapshot-identifier <snap_name>`. |
---

## EKS

EKS (Elastic Kubernetes Service) is AWS's managed Kubernetes service. It runs the Kubernetes control plane for you. You interact with EKS using the AWS CLI to manage clusters and node groups, and `kubectl` to manage workloads.

```bash
# Clusters
aws eks list-clusters
aws eks describe-cluster --name <cluster>

# Update kubeconfig (configures kubectl to point to your EKS cluster)
aws eks update-kubeconfig --name <cluster> --region <region>

# Node groups (the EC2 instances that run your Kubernetes workloads)
aws eks list-nodegroups --cluster-name <cluster>
aws eks describe-nodegroup --cluster-name <cluster> --nodegroup-name <ng>
```


```text title="Expected output"
{
    "clusters": [
        "production-cluster",
        "staging-cluster",
        "dev-cluster"
    ]
}
{
    "cluster": {
        "name": "production-cluster",
        "arn": "arn:aws:eks:us-east-1:123456789012:cluster/production-cluster",
        "createdAt": "2024-01-15T10:32:45.000000+00:00",
        "version": "1.28.5",
        "endpoint": "https://ABC123DEF456.eks.us-east-1.amazonaws.com",
        "status": "ACTIVE"
    }
}
Added new context arn:aws:eks:us-east-1:123456789012:cluster/production-cluster to /home/user/.kube/config
{
    "nodegroups": [
        "worker-nodes-1",
        "worker-nodes-2",
        "gpu-nodes"
    ]
}
{
    "nodegroup": {
        "nodegroupName": "worker-nodes-1",
        "nodegroupArn": "arn:aws:eks:us-east-1:123456789012:nodegroup/production-cluster/worker-nodes-1/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "clusterName": "production-cluster",
        "status": "ACTIVE",
        "scalingConfig": {
            "minSize": 2,
            "maxSize": 10,
            "desiredSize": 5
        }
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the ListClusters operation: No cluster found` | Verify the cluster exists in your current AWS region with `aws eks list-clusters --region <region>`. |
    | `An error occurred (InvalidParameterException) when calling the UpdateKubeconfig operation: Cluster not found` | Ensure the cluster name is correct and you have permissions; verify with `aws eks describe-cluster --name <cluster> --region <region>`. |
---

## Systems Manager (SSM)

SSM lets you manage EC2 instances without SSH. Session Manager creates a shell session through the AWS API — no open ports needed. Run Command executes scripts on instances remotely. Parameter Store is a secure key-value store for configuration and secrets.

```bash
# Session (interactive shell — no SSH, no open port 22 required)
aws ssm start-session --target <instance_id>

# Run command (run a script on one or more instances)
aws ssm send-command \
  --instance-ids <id> \
  --document-name "AWS-RunShellScript" \
  --parameters commands="uptime"
aws ssm list-command-invocations --command-id <cmd_id> --details

# Parameter Store (secure key-value store for config and secrets)
aws ssm get-parameter --name /my/param --with-decryption
aws ssm put-parameter --name /my/param --value "value" --type SecureString
aws ssm get-parameters-by-path --path /my/
```


```text title="Expected output"
Starting session with i-0a7f2c9d4e1b5f3a2...
[ssm-user@ip-10-0-42-17 ~]$ 

Command ID is 12a34b56-78cd-90ef-ghij-1234567890ab
An error occurred (InvalidInstanceID.Malformed) when calling the SendCommand operation: The instance ID 'i-0a7f2c9d4e1b5f3a2' does not exist

CommandId                                          Status      TargetCount  CompletedCount
----------------------------------------------------  ---------   -----------  ---------------
12a34b56-78cd-90ef-ghij-1234567890ab               Success     1            1

InvocationId                                       CommandId                                        InstanceId             PluginName  DocumentName           DocumentVersion  CommandStatus  ExecutionStartDateTime  ExecutionElapsedTime
----------------------------------------------------  ----------------------------------------------------  ---------------------  ----------  ---------------------  ----------------  -------  -----------------------  --------------------
12a34b56-78cd-90ef-ghij-1234567890ab               12a34b56-78cd-90ef-ghij-1234567890ab               i-0a7f2c9d4e1b5f3a2    aws:runShellScript  AWS-RunShellScript     1.2.2          Success  2024-01-15T09:42:31Z    0.847

 10:42:31 up 18 days, 3:24, 2 users, load average: 0.12, 0.08, 0.05

Name: /my/param
Type: SecureString
Value: ****
Version: 3
LastModifiedDate: 2024-01-15T08:15:22.000000+00:00
ARN: arn:aws:ssm:us-east-1:123456789012:parameter/my/param

(no output — command completes silently)

Parameters:
- Name: /my/param
  Type: SecureString
  Value: ****
  Version: 3
- Name: /my/param/db-host
  Type: String
  Value: db.internal.example.com
  Version: 1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (TargetNotConnected) when calling the SendCommand operation: The following instances are not connected: i-0a7f2c9d4e1b5f3a2` | Verify the instance has the SSM agent running (`systemctl status amazon-ssm-agent`) and an IAM role with `AmazonSSMManagedInstanceCore` policy attached. |
    | `An error occurred (ParameterNotFound) when calling the GetParameter operation: Parameter /my/param not found.` | Confirm the parameter name and path are correct with `aws ssm describe-parameters --filters "Key=Name,Values=/my/param"`. |
    | `An error occurred (AccessDenied) when calling the StartSession operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: ssm:StartSession` | Add the `AmazonSSMFullAccess` policy or a custom policy with `ssm:StartSession` and `ssm:GetConnectionStatus` permissions to the IAM user/role. |
---

## Lambda

Lambda is AWS's serverless compute service. You upload code and Lambda runs it on demand without you managing any servers. Functions are invoked by events (HTTP requests, S3 events, schedules, etc.).

```bash
# Functions
aws lambda list-functions
aws lambda get-function --function-name <name>

# Invoke a function (synchronous — waits for result)
aws lambda invoke --function-name <name> --payload '{}' response.json

# Deploy updated code (zip your code and upload)
aws lambda update-function-code --function-name <name> --zip-file fileb://function.zip

# Logs (CloudWatch logs for Lambda executions)
aws logs tail /aws/lambda/<function_name> --follow
```


```text title="Expected output"
{
    "Functions": [
        {
            "FunctionName": "process-orders",
            "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:process-orders",
            "Runtime": "python3.11",
            "Handler": "index.handler",
            "CodeSize": 2048576,
            "MemorySize": 256,
            "Timeout": 60,
            "LastModified": "2024-01-15T10:32:45.000+0000"
        },
        {
            "FunctionName": "send-notifications",
            "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:send-notifications",
            "Runtime": "nodejs18.x",
            "Handler": "app.handler",
            "CodeSize": 1024000,
            "MemorySize": 512,
            "Timeout": 30,
            "LastModified": "2024-01-14T14:22:10.000+0000"
        }
    ]
}
{
    "Configuration": {
        "FunctionName": "process-orders",
        "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:process-orders",
        "Runtime": "python3.11",
        "Handler": "index.handler",
        "CodeSize": 2048576,
        "MemorySize": 256,
        "Timeout": 60,
        "LastModified": "2024-01-15T10:32:45.000+0000"
    }
}
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST",
    "LogResult": "U1RBUlQgUmVxdWVzdElkOiBhYzNkNDU2Yi1mZjg5LTQxZTItOGZkYS1jZjQ3ZjhhYzQ1ZTAgRHVyYXRpb246IDI4LjM2IG1zIEJpbGxlZCBEdXJhdGlvbjogMjkgbXMgTWVtb3J5IFVzZWQ6IDEyOCBNQiBFTkQ="
}
{
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:process-orders",
    "CodeSize": 2048576,
    "FunctionName": "process-orders",
    "LastModified": "2024-01-15T11:05:22.000+0000"
}
2024-01-15T11:05:45.123Z	ac3d456b-ff89-41e2-8fda-cf47f8ac45e0	INFO	Processing order #ORD-2024-001
2024-01-15T11:05:46.456Z	ac3d456b-ff89-41e2-8fda-cf47f8ac45e0	INFO	Order processed successfully
2024-01-15T11:05:47.789Z	ac3d456b-ff89
```