# AWS — CLI Reference

```text
AWS CLI Daily Ops: Top Commands
──────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────┐
  │  Auth & Identity                                     │
  │  aws sts get-caller-identity  (confirm account/role) │
  │  aws sso login --profile prod                        │
  └──────────────────────────────────────────────────────┘
  ┌────────────────────┐  ┌───────────────────────────┐
  │  EC2               │  │  RDS                      │
  │  describe-instances│  │  describe-db-instances    │
  │  stop/start        │  │  create-db-snapshot       │
  │  get-console-output│  │  modify-db-instance       │
  └────────────────────┘  └───────────────────────────┘
  ┌────────────────────┐  ┌───────────────────────────┐
  │  S3                │  │  CloudWatch               │
  │  ls / cp / sync    │  │  describe-alarms ALARM    │
  │  s3api get-policy  │  │  get-metric-statistics    │
  └────────────────────┘  └───────────────────────────┘
  ┌────────────────────┐  ┌───────────────────────────┐
  │  EKS               │  │  SSM                      │
  │  update-kubeconfig │  │  start-session            │
  │  list-nodegroups   │  │  send-command             │
  └────────────────────┘  └───────────────────────────┘
```

---

## Setup and Authentication

```bash
# Configure a named profile
aws configure --profile prod
# Prompts for: Access Key ID, Secret Access Key, Region, Output format

# Use a profile
export AWS_PROFILE=prod
# Or: aws --profile prod <command>

# Assume a role (cross-account or elevated)
aws sts assume-role \
  --role-arn arn:aws:iam::<account-id>:role/MyRole \
  --role-session-name my-session

# Export temporary credentials
eval $(aws sts assume-role \
  --role-arn arn:aws:iam::<account-id>:role/MyRole \
  --role-session-name session \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text | awk '{print "export AWS_ACCESS_KEY_ID="$1"\nexport AWS_SECRET_ACCESS_KEY="$2"\nexport AWS_SESSION_TOKEN="$3}')

# Verify current identity
aws sts get-caller-identity
```

---

## EC2

```bash
# List instances
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,PrivateIpAddress,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# Filter by tag
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=prod" "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].[InstanceId,PrivateIpAddress,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# Start / stop / reboot
aws ec2 start-instances --instance-ids i-0abc123
aws ec2 stop-instances --instance-ids i-0abc123
aws ec2 reboot-instances --instance-ids i-0abc123

# Get console output (useful when instance unreachable)
aws ec2 get-console-output --instance-id i-0abc123 --output text
```

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
