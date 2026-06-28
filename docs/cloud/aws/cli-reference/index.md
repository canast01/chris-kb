---
tags:
  - aws
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
