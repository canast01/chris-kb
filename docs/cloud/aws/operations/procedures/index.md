# AWS Operations — Procedures & Runbooks

```bash
# List RDS instances
aws rds describe-db-instances \
  --query 'DBInstances[*].{ID:DBInstanceIdentifier,Engine:Engine,Class:DBInstanceClass,Status:DBInstanceStatus,AZ:AvailabilityZone,MultiAZ:MultiAZ,Endpoint:Endpoint.Address}' \
  --output table

# Describe a specific instance
aws rds describe-db-instances --db-instance-identifier <db-id>

# Create a snapshot
aws rds create-db-snapshot \
  --db-instance-identifier <db-id> \
  --db-snapshot-identifier <snap-name>

# List snapshots
aws rds describe-db-snapshots \
  --db-instance-identifier <db-id> \
  --query 'DBSnapshots[*].{ID:DBSnapshotIdentifier,Status:Status,Created:SnapshotCreateTime,Size:AllocatedStorage}' \
  --output table

# Reboot instance
aws rds reboot-db-instance --db-instance-identifier <db-id>

# Modify instance (example: enable Multi-AZ)
aws rds modify-db-instance \
  --db-instance-identifier <db-id> \
  --multi-az \
  --apply-immediately

# Start / stop instance (for dev/test)
aws rds stop-db-instance --db-instance-identifier <db-id>
aws rds start-db-instance --db-instance-identifier <db-id>
```text
┌─────────────────────────────── AWS Operations — Procedures & Runbooks ────────────────────────────────┐
│                                                                                                       │
│  Standard operating procedures for AWS change management, incident response, and routine ops.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Change Management               │  │              Incident Response              │   │
│   │       RFC: document scope and rollback       │  │        Detect: CloudWatch alarm fires       │   │
│   │        CAB approval for prod changes         │  │      Acknowledge: on-call via PagerDuty     │   │
│   │      Change window: low-traffic period       │  │      Investigate: CloudTrail + CW Logs      │   │
│   │     Pre-change: snapshot + health check      │  │      Contain: isolate affected resource     │   │
│   │      Post-change: validate + close RFC       │  │       Recover: restore from backup/AMI      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SSM Automation documents codify runbooks; OpsCenter tracks operational issues.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Routine Operations              │  │             Post-Incident Review            │   │
│   │     Daily: review CloudWatch dashboards      │  │      Timeline: reconstruct from CT logs     │   │
│   │      Weekly: cost anomaly report review      │  │          Root cause: 5-why analysis         │   │
│   │       Monthly: patch compliance report       │  │      Action items: preventive controls      │   │
│   │         Quarterly: IAM access review         │  │       Document: PIR in Confluence/Jira      │   │
│   │    Annual: DR test + architecture review     │  │     Share: distribute learnings to team     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS regional infrastructure · Multi-AZ service endpoints · CloudTrail audit data                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RFC             = Request for Change; documents scope, risk, and rollback plan                       │
│  CAB             = Change Advisory Board; approves high-risk changes before execution                 │
│  Change window   = Pre-approved time slot for making infrastructure changes                           │
│  Rollback plan   = Documented steps to revert changes if post-change validation fails                 │
│  OpsCenter       = SSM feature that aggregates operational issues with context                        │
│  SSM Automation  = Document-based runbook executed against AWS resources                              │
│  PIR             = Post-Incident Review; blameless analysis after an incident                         │
│  5-why analysis  = Root cause technique: ask why 5 times to find the true cause                       │
│  On-call rotation= Schedule assigning primary/secondary responders for incident alerts                │
│  Runbook         = Step-by-step procedure for a repeatable operational task                           │
│  IAM access review= Periodic audit of unused permissions and inactive access keys                     │
│  DR test         = Disaster recovery test validating RTO/RPO targets are achievable                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Launch an EC2 Instance (AWS CLI)

```bash
# Create a key pair (skip if reusing an existing one)
aws ec2 create-key-pair \
  --key-name my-keypair \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/my-keypair.pem
chmod 400 ~/.ssh/my-keypair.pem

# Launch instance
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.medium \
  --key-name my-keypair \
  --subnet-id subnet-0abc1234 \
  --security-group-ids sg-0abc1234 \
  --user-data file://userdata.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-instance},{Key=Env,Value=prod}]' \
  --query 'Instances[0].{ID:InstanceId,State:State.Name,IP:PrivateIpAddress}' \
  --output table

# Wait for the instance to reach running state
aws ec2 wait instance-running --instance-ids <instance-id>

# Confirm status checks pass
aws ec2 describe-instance-status \
  --instance-ids <instance-id> \
  --query 'InstanceStatuses[0].{System:SystemStatus.Status,Instance:InstanceStatus.Status}'
```

Parameters to confirm before running:

| Parameter | Value |
|---|---|
| AMI ID | Region-specific; check `aws ec2 describe-images` or SSM Public Parameters |
| Instance type | Match workload: t3 (burstable), m6i (general), c6i (compute), r6i (memory) |
| Subnet | Determines AZ and VPC; use private subnet for non-public workloads |
| Security group | Must allow required ingress (SSH/RDP) and application ports |
| User data | Optional bootstrap script (install packages, configure app) |

---

## Create and Attach an EBS Volume

```bash
# Get the AZ of the target instance (volume must be in the same AZ)
AZ=$(aws ec2 describe-instances \
  --instance-ids <instance-id> \
  --query 'Reservations[0].Instances[0].Placement.AvailabilityZone' \
  --output text)

# Create volume
aws ec2 create-volume \
  --availability-zone "$AZ" \
  --size 100 \
  --volume-type gp3 \
  --iops 3000 \
  --throughput 125 \
  --encrypted \
  --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=data-vol-01}]' \
  --query '{VolumeId:VolumeId,State:State,Size:Size}' \
  --output table

# Wait for volume to become available
aws ec2 wait volume-available --volume-ids <volume-id>

# Attach volume to instance
aws ec2 attach-volume \
  --volume-id <volume-id> \
  --instance-id <instance-id> \
  --device /dev/sdf

# --- In-guest: mount the volume (SSH into the instance) ---
# List block devices to confirm attachment
lsblk

# Format the volume (first time only — skip if restoring data)
sudo mkfs -t xfs /dev/nvme1n1

# Create mount point and mount
sudo mkdir -p /data
sudo mount /dev/nvme1n1 /data

# Persist mount across reboots
echo '/dev/nvme1n1 /data xfs defaults,nofail 0 2' | sudo tee -a /etc/fstab
```

---

## Create an S3 Bucket and Set Policy

```bash
BUCKET=my-prod-bucket-20240601
REGION=eu-west-1

# Create bucket (us-east-1 does not use --create-bucket-configuration)
aws s3 mb s3://$BUCKET --region $REGION \
  --create-bucket-configuration LocationConstraint=$REGION

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket $BUCKET \
  --versioning-configuration Status=Enabled

# Enable default server-side encryption (SSE-S3)
aws s3api put-bucket-encryption \
  --bucket $BUCKET \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      },
      "BucketKeyEnabled": true
    }]
  }'

# Block all public access
aws s3api put-public-access-block \
  --bucket $BUCKET \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Apply a resource-based bucket policy (example: restrict to specific IAM role)
cat > /tmp/bucket-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRoleAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:role/my-app-role"
      },
      "Action": ["s3:GetObject","s3:PutObject","s3:DeleteObject"],
      "Resource": "arn:aws:s3:::my-prod-bucket-20240601/*"
    },
    {
      "Sid": "DenyNonSSL",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-prod-bucket-20240601",
        "arn:aws:s3:::my-prod-bucket-20240601/*"
      ],
      "Condition": {"Bool": {"aws:SecureTransport": "false"}}
    }
  ]
}
EOF

aws s3api put-bucket-policy --bucket $BUCKET --policy file:///tmp/bucket-policy.json

# Verify
aws s3api get-bucket-versioning --bucket $BUCKET
aws s3api get-bucket-encryption --bucket $BUCKET
```

---

## Create a Security Group Rule

```bash
# Authorize inbound (ingress) rule — allow HTTPS from anywhere
aws ec2 authorize-security-group-ingress \
  --group-id sg-0abc1234 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# Authorize ingress from another security group (e.g., ALB → app servers)
aws ec2 authorize-security-group-ingress \
  --group-id sg-0app1234 \
  --ip-permissions '[{
    "IpProtocol": "tcp",
    "FromPort": 8080,
    "ToPort": 8080,
    "UserIdGroupPairs": [{"GroupId": "sg-0alb1234"}]
  }]'

# Authorize outbound (egress) rule — allow DNS from instances
aws ec2 authorize-security-group-egress \
  --group-id sg-0abc1234 \
  --protocol udp \
  --port 53 \
  --cidr 0.0.0.0/0

# Revoke a rule (same syntax as authorize, different sub-command)
aws ec2 revoke-security-group-ingress \
  --group-id sg-0abc1234 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Verify current rules
aws ec2 describe-security-groups \
  --group-ids sg-0abc1234 \
  --query 'SecurityGroups[0].{Name:GroupName,Ingress:IpPermissions,Egress:IpPermissionsEgress}'
```

Rule parameters:

| Parameter | Notes |
|---|---|
| `--protocol` | `tcp`, `udp`, `icmp`, or `-1` (all) |
| `--port` | Single port or range `8080-8090`; `-1` for all |
| `--cidr` | IPv4 CIDR or use `--source-group` for SG-to-SG rules |

---

## Create a VPC Peering Connection

```bash
# --- Step 1: Requester account creates the peering request ---
aws ec2 create-vpc-peering-connection \
  --vpc-id vpc-0requester \
  --peer-vpc-id vpc-0accepter \
  --peer-region eu-central-1 \
  --peer-owner-id <accepter-account-id> \
  --tag-specifications 'ResourceType=vpc-peering-connection,Tags=[{Key=Name,Value=peer-prod-to-dr}]'

# Note the PeeringConnectionId returned (pcx-0abc1234)

# --- Step 2: Accepter account accepts the request ---
aws ec2 accept-vpc-peering-connection \
  --vpc-peering-connection-id pcx-0abc1234

# Wait for active state
aws ec2 describe-vpc-peering-connections \
  --vpc-peering-connection-ids pcx-0abc1234 \
  --query 'VpcPeeringConnections[0].Status.Code'

# --- Step 3: Update route tables on BOTH sides ---
# Requester: add route pointing to accepter CIDR via the peering connection
aws ec2 create-route \
  --route-table-id rtb-0requester \
  --destination-cidr-block 10.1.0.0/16 \
  --vpc-peering-connection-id pcx-0abc1234

# Accepter: add route pointing to requester CIDR via the peering connection
aws ec2 create-route \
  --route-table-id rtb-0accepter \
  --destination-cidr-block 10.0.0.0/16 \
  --vpc-peering-connection-id pcx-0abc1234

# Verify connectivity from an EC2 instance in each VPC
ping <peer-instance-private-ip>
```

> Note: VPC peering does not support transitive routing. If VPC-A peers with VPC-B and VPC-B peers with VPC-C, VPC-A cannot reach VPC-C through VPC-B. Use AWS Transit Gateway for hub-and-spoke topologies.

---

## Configure an IAM Role and Policy

```bash
# --- Step 1: Define the trust policy (who can assume this role) ---
cat > /tmp/trust-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Service": "ec2.amazonaws.com"
    },
    "Action": "sts:AssumeRole"
  }]
}
EOF

# --- Step 2: Create the role ---
aws iam create-role \
  --role-name MyAppRole \
  --assume-role-policy-document file:///tmp/trust-policy.json \
  --description "Role for application EC2 instances"

# --- Step 3: Attach a managed policy ---
aws iam attach-role-policy \
  --role-name MyAppRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# --- Step 4: Optionally create and attach a custom inline policy ---
cat > /tmp/custom-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:PutObject","s3:GetObject"],
    "Resource": "arn:aws:s3:::my-prod-bucket/*"
  }]
}
EOF

aws iam put-role-policy \
  --role-name MyAppRole \
  --policy-name MyAppInlinePolicy \
  --policy-document file:///tmp/custom-policy.json

# --- Step 5: Create an instance profile and attach to EC2 ---
aws iam create-instance-profile --instance-profile-name MyAppProfile
aws iam add-role-to-instance-profile \
  --instance-profile-name MyAppProfile \
  --role-name MyAppRole

# Attach to a running EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id <instance-id> \
  --iam-instance-profile Name=MyAppProfile

# Verify
aws iam get-role --role-name MyAppRole \
  --query 'Role.{Name:RoleName,ARN:Arn,AssumeRolePolicyDocument:AssumeRolePolicyDocument}'
aws iam list-attached-role-policies --role-name MyAppRole --output table
```

For Lambda, change the trust principal to `"Service": "lambda.amazonaws.com"` and skip the instance profile steps.

---

## Set Up CloudWatch Alarms

```bash
# --- Create an SNS topic for notifications (if not already existing) ---
aws sns create-topic --name ops-alerts
aws sns subscribe \
  --topic-arn arn:aws:sns:eu-west-1:<account>:ops-alerts \
  --protocol email \
  --notification-endpoint ops-team@example.com

# --- CPU utilisation alarm on an EC2 instance ---
aws cloudwatch put-metric-alarm \
  --alarm-name "High-CPU-myinstance" \
  --alarm-description "CPU > 80% for 5 minutes" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=InstanceId,Value=<instance-id> \
  --alarm-actions arn:aws:sns:eu-west-1:<account>:ops-alerts \
  --ok-actions arn:aws:sns:eu-west-1:<account>:ops-alerts \
  --treat-missing-data notBreaching

# --- RDS storage alarm ---
aws cloudwatch put-metric-alarm \
  --alarm-name "Low-RDS-Storage" \
  --metric-name FreeStorageSpace \
  --namespace AWS/RDS \
  --statistic Minimum \
  --period 300 \
  --threshold 5368709120 \
  --comparison-operator LessThanThreshold \
  --evaluation-periods 1 \
  --dimensions Name=DBInstanceIdentifier,Value=<db-id> \
  --alarm-actions arn:aws:sns:eu-west-1:<account>:ops-alerts

# Verify alarm state
aws cloudwatch describe-alarms \
  --alarm-names "High-CPU-myinstance" \
  --query 'MetricAlarms[0].{State:StateValue,Reason:StateReason}'
```

Key parameters:

| Parameter | Notes |
|---|---|
| `--period` | Seconds per data point: 60, 300, 3600 |
| `--evaluation-periods` | How many periods must breach before alarm fires |
| `--threshold` | Value in the metric's native unit (%, bytes, count, etc.) |
| `--treat-missing-data` | `notBreaching` (safe), `breaching` (alert), `ignore`, `missing` |

---

## Create an AMI from a Running Instance

```bash
# Create the AMI (no-reboot avoids a brief instance outage but may produce a less consistent image)
aws ec2 create-image \
  --instance-id <instance-id> \
  --name "my-instance-$(date +%Y%m%d-%H%M)" \
  --description "Pre-patch baseline AMI" \
  --no-reboot \
  --query '{ImageId:ImageId}' \
  --output table

# Wait for the AMI to become available (can take several minutes)
aws ec2 wait image-available --image-ids <ami-id>

# Tag the AMI and its associated snapshots
aws ec2 create-tags \
  --resources <ami-id> \
  --tags Key=Name,Value=my-instance-baseline \
         Key=CreatedBy,Value=ops-runbook \
         Key=Env,Value=prod

# List your AMIs to confirm
aws ec2 describe-images \
  --owners self \
  --query 'Images[*].{ID:ImageId,Name:Name,State:State,Created:CreationDate}' \
  --output table

# After a rollback or migration, launch from the AMI
aws ec2 run-instances \
  --image-id <ami-id> \
  --instance-type <instance-type> \
  --key-name <keypair> \
  --subnet-id <subnet-id> \
  --security-group-ids <sg-id>
```

> No-reboot note: `--no-reboot` does not guarantee crash-consistent images for all workloads. For databases, quiesce writes or take a reboot-based AMI during a maintenance window.

---

## Resize an EC2 Instance

```bash
# --- Step 1: Stop the instance ---
aws ec2 stop-instances --instance-ids <instance-id>
aws ec2 wait instance-stopped --instance-ids <instance-id>

# Confirm stopped state
aws ec2 describe-instances \
  --instance-ids <instance-id> \
  --query 'Reservations[0].Instances[0].State.Name'

# --- Step 2: Change the instance type ---
aws ec2 modify-instance-attribute \
  --instance-id <instance-id> \
  --instance-type '{"Value":"m6i.xlarge"}'

# Verify the attribute was updated
aws ec2 describe-instances \
  --instance-ids <instance-id> \
  --query 'Reservations[0].Instances[0].InstanceType'

# --- Step 3: Start the instance ---
aws ec2 start-instances --instance-ids <instance-id>
aws ec2 wait instance-running --instance-ids <instance-id>

# Confirm instance is healthy
aws ec2 describe-instance-status \
  --instance-ids <instance-id> \
  --query 'InstanceStatuses[0].{System:SystemStatus.Status,Instance:InstanceStatus.Status}'
```

Constraints:

| Consideration | Notes |
|---|---|
| Same family resize | Usually no additional validation needed |
| Cross-family resize | Verify CPU flags (e.g., AVX-512); re-test application after resize |
| Nitro vs. Xen | Switching from Xen-based types may require NVMe/ENA driver updates in the OS |
| ENA/EFA | Check `--ena-support` is enabled if moving to a network-intensive type |

---

## Configure VPC Flow Logs

```bash
# --- Option A: Flow logs to an S3 bucket ---
# Create S3 bucket for flow logs (if not existing)
aws s3 mb s3://my-vpc-flowlogs-<account-id> --region eu-west-1

# Enable flow logs on the VPC
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-0abc1234 \
  --traffic-type ALL \
  --log-destination-type s3 \
  --log-destination arn:aws:s3:::my-vpc-flowlogs-<account-id>/vpc/ \
  --log-format '${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status}'

# --- Option B: Flow logs to CloudWatch Logs ---
# IAM role for flow logs to write to CloudWatch
aws iam create-role \
  --role-name VPCFlowLogsRole \
  --assume-role-policy-document '{
    "Version":"2012-10-17",
    "Statement":[{"Effect":"Allow","Principal":{"Service":"vpc-flow-logs.amazonaws.com"},"Action":"sts:AssumeRole"}]
  }'

aws iam put-role-policy \
  --role-name VPCFlowLogsRole \
  --policy-name FlowLogsCWPolicy \
  --policy-document '{
    "Version":"2012-10-17",
    "Statement":[{"Effect":"Allow","Action":["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents","logs:DescribeLogGroups","logs:DescribeLogStreams"],"Resource":"*"}]
  }'

# Create CW log group
aws logs create-log-group --log-group-name /aws/vpc/flowlogs/vpc-0abc1234

# Enable flow logs to CloudWatch
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-0abc1234 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flowlogs/vpc-0abc1234 \
  --deliver-logs-permission-arn arn:aws:iam::<account-id>:role/VPCFlowLogsRole

# Verify flow log is active
aws ec2 describe-flow-logs \
  --filter Name=resource-id,Values=vpc-0abc1234 \
  --query 'FlowLogs[*].{ID:FlowLogId,Status:FlowLogStatus,Type:LogDestinationType,Destination:LogDestination}'
```

Traffic type options:

| `--traffic-type` | What is captured |
|---|---|
| `ALL` | Accepted and rejected traffic |
| `ACCEPT` | Only traffic allowed by security group and NACL rules |
| `REJECT` | Only traffic denied by security group or NACL rules |
