# AWS CLI Reference

Commonly used AWS CLI commands for managing compute, storage, networking, identity, and monitoring.

> Requires `aws configure` or environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`).

---

## Identity & Access (IAM / STS)

```bash
# Current identity
aws sts get-caller-identity

# IAM users
aws iam list-users
aws iam get-user --user-name <user>
aws iam create-user --user-name <user>
aws iam delete-user --user-name <user>

# IAM groups
aws iam list-groups
aws iam add-user-to-group --user-name <user> --group-name <group>

# IAM roles
aws iam list-roles
aws iam get-role --role-name <role>
aws iam create-role --role-name <role> --assume-role-policy-document file://trust.json
aws iam attach-role-policy --role-name <role> --policy-arn <arn>

# Access keys
aws iam list-access-keys --user-name <user>
aws iam create-access-key --user-name <user>
aws iam delete-access-key --user-name <user> --access-key-id <id>

# Assume role
aws sts assume-role --role-arn <arn> --role-session-name session1
```

---

## EC2 — Instances

```bash
# List instances
aws ec2 describe-instances
aws ec2 describe-instances --filters "Name=tag:Name,Values=<name>"
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table

# Start / stop / reboot
aws ec2 start-instances --instance-ids <id>
aws ec2 stop-instances --instance-ids <id>
aws ec2 reboot-instances --instance-ids <id>
aws ec2 terminate-instances --instance-ids <id>

# Instance types
aws ec2 describe-instance-types --instance-types t3.medium

# Key pairs
aws ec2 describe-key-pairs
aws ec2 create-key-pair --key-name <name> --query 'KeyMaterial' --output text > key.pem

# Security groups
aws ec2 describe-security-groups
aws ec2 authorize-security-group-ingress --group-id <sg_id> --protocol tcp --port 22 --cidr 10.0.0.0/8
aws ec2 revoke-security-group-ingress --group-id <sg_id> --protocol tcp --port 22 --cidr 10.0.0.0/8
```

---

## EC2 — Images, Volumes & Snapshots

```bash
# AMIs
aws ec2 describe-images --owners self
aws ec2 create-image --instance-id <id> --name "snapshot-$(date +%F)" --no-reboot

# EBS volumes
aws ec2 describe-volumes
aws ec2 describe-volumes --filters "Name=attachment.instance-id,Values=<id>"
aws ec2 create-volume --availability-zone us-east-1a --size 100 --volume-type gp3
aws ec2 attach-volume --device /dev/xvdf --instance-id <id> --volume-id <vol_id>
aws ec2 detach-volume --volume-id <vol_id>
aws ec2 delete-volume --volume-id <vol_id>

# EBS snapshots
aws ec2 describe-snapshots --owner-ids self
aws ec2 create-snapshot --volume-id <vol_id> --description "backup"
aws ec2 delete-snapshot --snapshot-id <snap_id>
aws ec2 copy-snapshot --source-snapshot-id <snap_id> --source-region us-east-1 --destination-region eu-west-1
```

---

## S3

```bash
# Buckets
aws s3 ls
aws s3 ls s3://<bucket>/
aws s3 mb s3://<bucket>
aws s3 rb s3://<bucket> --force

# Objects
aws s3 cp <local_file> s3://<bucket>/<key>
aws s3 cp s3://<bucket>/<key> <local_file>
aws s3 mv s3://<bucket>/<key> s3://<bucket>/<new_key>
aws s3 rm s3://<bucket>/<key>
aws s3 rm s3://<bucket>/<prefix>/ --recursive

# Sync
aws s3 sync <local_dir> s3://<bucket>/<prefix>
aws s3 sync s3://<bucket>/<prefix> <local_dir>
aws s3 sync --delete s3://<source> s3://<dest>

# S3 API (for policy/lifecycle/versioning)
aws s3api get-bucket-versioning --bucket <bucket>
aws s3api put-bucket-versioning --bucket <bucket> --versioning-configuration Status=Enabled
aws s3api get-bucket-policy --bucket <bucket>
aws s3api list-object-versions --bucket <bucket>
aws s3api put-bucket-lifecycle-configuration --bucket <bucket> --lifecycle-configuration file://lifecycle.json
```

---

## VPC & Networking

```bash
# VPCs
aws ec2 describe-vpcs
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 delete-vpc --vpc-id <id>

# Subnets
aws ec2 describe-subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc_id>"
aws ec2 create-subnet --vpc-id <id> --cidr-block 10.0.1.0/24 --availability-zone us-east-1a

# Route tables
aws ec2 describe-route-tables
aws ec2 create-route --route-table-id <rt_id> --destination-cidr-block 0.0.0.0/0 --gateway-id <igw_id>

# Internet gateways
aws ec2 describe-internet-gateways
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --internet-gateway-id <igw_id> --vpc-id <vpc_id>

# Elastic IPs
aws ec2 describe-addresses
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id <id> --allocation-id <eip_id>
aws ec2 release-address --allocation-id <eip_id>
```

---

## CloudWatch

```bash
# Alarms
aws cloudwatch describe-alarms
aws cloudwatch describe-alarms --state-value ALARM
aws cloudwatch set-alarm-state --alarm-name <name> --state-value OK --state-reason "manual reset"

# Metrics
aws cloudwatch list-metrics --namespace AWS/EC2
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=<id> \
  --start-time $(date -u -d '1 hour ago' +%FT%TZ) \
  --end-time $(date -u +%FT%TZ) \
  --period 300 --statistics Average

# Logs
aws logs describe-log-groups
aws logs describe-log-streams --log-group-name <group>
aws logs get-log-events --log-group-name <group> --log-stream-name <stream>
aws logs tail <log_group> --follow
aws logs filter-log-events --log-group-name <group> --filter-pattern "ERROR"
```

---

## CloudFormation

```bash
# Stacks
aws cloudformation list-stacks
aws cloudformation describe-stacks --stack-name <name>
aws cloudformation create-stack --stack-name <name> --template-body file://template.yaml --parameters ParameterKey=Env,ParameterValue=prod
aws cloudformation update-stack --stack-name <name> --template-body file://template.yaml
aws cloudformation delete-stack --stack-name <name>

# Stack status
aws cloudformation describe-stack-events --stack-name <name>
aws cloudformation wait stack-create-complete --stack-name <name>

# Validate
aws cloudformation validate-template --template-body file://template.yaml
```

---

## RDS

```bash
# Instances
aws rds describe-db-instances
aws rds describe-db-instances --db-instance-identifier <id>

# Start / stop
aws rds start-db-instance --db-instance-identifier <id>
aws rds stop-db-instance --db-instance-identifier <id>
aws rds reboot-db-instance --db-instance-identifier <id>

# Snapshots
aws rds describe-db-snapshots
aws rds create-db-snapshot --db-instance-identifier <id> --db-snapshot-identifier <snap_name>
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier <new_id> --db-snapshot-identifier <snap_name>
```

---

## EKS

```bash
# Clusters
aws eks list-clusters
aws eks describe-cluster --name <cluster>

# Update kubeconfig
aws eks update-kubeconfig --name <cluster> --region <region>

# Node groups
aws eks list-nodegroups --cluster-name <cluster>
aws eks describe-nodegroup --cluster-name <cluster> --nodegroup-name <ng>
```

---

## Systems Manager (SSM)

```bash
# Session (no SSH needed)
aws ssm start-session --target <instance_id>

# Run command
aws ssm send-command --instance-ids <id> --document-name "AWS-RunShellScript" --parameters commands="uptime"
aws ssm list-command-invocations --command-id <cmd_id> --details

# Parameter Store
aws ssm get-parameter --name /my/param --with-decryption
aws ssm put-parameter --name /my/param --value "value" --type SecureString
aws ssm get-parameters-by-path --path /my/
```

---

## Lambda

```bash
# Functions
aws lambda list-functions
aws lambda get-function --function-name <name>
aws lambda invoke --function-name <name> --payload '{}' response.json

# Deploy
aws lambda update-function-code --function-name <name> --zip-file fileb://function.zip

# Logs
aws logs tail /aws/lambda/<function_name> --follow
```
