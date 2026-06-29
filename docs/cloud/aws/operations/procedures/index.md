---
tags:
  - aws
  - operations
---
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
```


```text title="Expected output"
| ID                    | Engine   | Class          | Status    | AZ            | MultiAZ | Endpoint                                    |
|-----------------------|----------|----------------|-----------|---------------|---------|---------------------------------------------|
| prod-mysql-01         | mysql    | db.r5.2xlarge  | available | us-east-1a    | True    | prod-mysql-01.c9akciq32.us-east-1.rds.a... |
| dev-postgres-02       | postgres | db.t3.medium   | available | us-east-1b    | False   | dev-postgres-02.c9akciq32.us-east-1.rds.a... |
| staging-aurora-03     | aurora   | db.r5.large    | available | us-east-1c    | True    | staging-aurora-03.c9akciq32.us-east-1.rds... |
...

{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-mysql-01",
        "DBInstanceClass": "db.r5.2xlarge",
        "Engine": "mysql",
        "DBInstanceStatus": "available",
        "AllocatedStorage": 500,
        "AvailabilityZone": "us-east-1a",
        "MultiAZ": true,
        "Endpoint": {
            "Address": "prod-mysql-01.c9akciq32.us-east-1.rds.amazonaws.com",
            "Port": 3306
        }
    }
}

{
    "DBSnapshot": {
        "DBSnapshotIdentifier": "prod-mysql-01-snap-20240115",
        "DBInstanceIdentifier": "prod-mysql-01",
        "SnapshotCreateTime": "2024-01-15T14:32:00+00:00",
        "Status": "available",
        "AllocatedStorage": 500,
        "Engine": "mysql"
    }
}

| ID                           | Status    | Created                      | Size |
|------------------------------|-----------|------------------------------|------|
| prod-mysql-01-snap-20240115  | available | 2024-01-15T14:32:00+00:00    | 500  |
| prod-mysql-01-snap-20240114  | available | 2024-01-14T02:15:00+00:00    | 500  |
...

{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-mysql-01",
        "DBInstanceStatus": "rebooting"
    }
}

{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-mysql-01",
        "DBInstanceStatus": "modifying",
        "PendingModifiedValues": {
            "MultiAZ": true
        }
    }
}

{
    "DBInstance": {
        "DBInstanceIdentifier": "dev-postgres-02",
        "DBInstanceStatus": "stopping"
    }
}

{
    "DBInstance": {
        "DBInstanceIdentifier": "dev-postgres-02",
        "DBInstanceStatus": "starting"
    }
}
```

!!! warning "Common errors"
    **`An error occurred (DBInstanceNotFound) when calling the DescribeDBInstances operation: DBInstance
---

```d2
direction: right

launch_an_ec2_instance_aws_cli: "Launch an EC2 Instance (AWS CLI)" {shape: rectangle}
create_and_attach_an_ebs_volume: "Create and Attach an EBS Volume" {shape: rectangle}
create_an_s3_bucket_and_set_policy: "Create an S3 Bucket and Set Policy" {shape: rectangle}
create_a_security_group_rule: "Create a Security Group Rule" {shape: rectangle}
create_a_vpc_peering_connection: "Create a VPC Peering Connection" {shape: rectangle}
configure_an_iam_role_and_policy: "Configure an IAM Role and Policy" {shape: rectangle}

launch_an_ec2_instance_aws_cli -> create_and_attach_an_ebs_volume
create_and_attach_an_ebs_volume -> create_an_s3_bucket_and_set_policy
create_an_s3_bucket_and_set_policy -> create_a_security_group_rule
create_a_security_group_rule -> create_a_vpc_peering_connection
create_a_vpc_peering_connection -> configure_an_iam_role_and_policy
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

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


```text title="Expected output"
-------------------------------------
|          ID          |  State   |        IP         |
|----------------------+----------+-------------------|
| i-0a1b2c3d4e5f6g7h8  | pending  | 10.0.1.42         |
-------------------------------------

Waiting, this may take a few minutes...

{
    "System": "initializing",
    "Instance": "initializing"
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidKeyPair.Duplicate) when calling the CreateKeyPair operation: The key pair 'my-keypair' already exists.`** — Remove the create-key-pair command or use a different `--key-name` value if reusing an existing key.
    
    **`An error occurred (InvalidAMIID.NotFound) when calling the RunInstances operation: The image id '[ami-0abcdef1234567890]' does not exist`** — Verify the AMI ID is correct for your region by running `aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*"`.
    
    **`An error occurred (InvalidParameterValue) when calling the RunInstances operation: Invalid id: "<instance-id>" (MalformedParameterValue)`** — Replace the literal string `<instance-id>` with the actual instance ID from the run-instances output (e.g., `i-0a1b2c3d4e5f6g7h8`).
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


```text title="Expected output"
us-east-1a
Creating volume...
---------------------------------------------------------------------------
|                          CreateVolume                                  |
+---------------------------------------------------------------------------+
| VolumeId   | vol-0a7f2c8e9b1d4f6c2                                      |
| State      | creating                                                    |
| Size       | 100                                                         |
+---------------------------------------------------------------------------+
Waiting for volume to become available...
{
    "Attachments": [],
    "AvailabilityZone": "us-east-1a",
    "CreateTime": "2024-01-15T14:32:18.000000+00:00",
    "Encrypted": true,
    "VolumeId": "vol-0a7f2c8e9b1d4f6c2",
    "State": "available"
}
{
    "AttachTime": "2024-01-15T14:32:45.000000+00:00",
    "Device": "/dev/sdf",
    "InstanceId": "i-0c5a9e2f7b1d8a3c6",
    "State": "attached",
    "VolumeId": "vol-0a7f2c8e9b1d4f6c2"
}
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
xvda        202:0    0   30G  0 disk
├─xvda1     202:1    0    1M  0 part
└─xvda2     202:2    0   30G  0 part /
nvme1n1     259:0    0  100G  0 disk
meta-data=isize=512    agcount=4, agsize=1638400 blks
data        =                       bsize=4096   blocks=6553600, imaxpct=25
naming   =version 2              bsize=4096   crcs=1            finobt=1
log      =internal               bsize=4096   blocks=3200, version=2
realtime =none                   exts=4, nextents=1
/dev/nvme1n1 /data xfs defaults,nofail 0 2
```

!!! warning "Common errors"
    **`An error occurred (InvalidInstanceID.NotFound) when calling the DescribeInstances operation: The instance ID '<instance-id>' does not exist`** — Replace `<instance-id>` with a valid EC2 instance ID from your account and region.
    **`An error occurred (InvalidParameterValue) when calling the AttachVolume operation: Invalid device name /dev/sdf`** — Use `/dev/sdf` through `/dev/sdp` for EBS volumes; NVMe device names like `/dev/nvme1n1` are assigned by the OS after attachment.
    **`mount: /data: unknown filesystem type 'xfs'`** — Install XFS tools on the instance with `sudo yum install xfsprogs` (Amazon Linux/RHEL) or `sudo apt install xfsprogs` (Ubuntu) before formatting.
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


```text title="Expected output"
make_bucket: my-prod-bucket-20240601
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
{
    "Status": "Enabled",
    "MFADelete": "Disabled"
}
{
    "Rules": [
        {
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            },
            "BucketKeyEnabled": true
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (BucketAlreadyExists) when calling the MakeBucket operation: The requested bucket name is not available. The bucket namespace is shared by all AWS accounts.`** — Choose a globally unique bucket name with a timestamp or random suffix, as S3 bucket names must be unique across all AWS accounts.
    **`An error occurred (NoSuchBucket) when calling the PutBucketPolicy operation: The specified bucket does not exist`** — Verify the bucket was created successfully by running `aws s3 ls` and ensure the BUCKET variable is set correctly before applying the policy.
    **`An error occurred (MalformedPolicy) when calling the PutBucketPolicy operation: Policy has invalid resource`** — Replace `<account-id>` in the policy JSON with your actual AWS account ID (12-digit number).
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


```text title="Expected output"
{
    "Return": true
}
{
    "Return": true
}
{
    "Return": true
}
{
    "Return": true
}
{
    "Name": "web-tier-sg",
    "Ingress": [
        {
            "IpProtocol": "tcp",
            "FromPort": 443,
            "ToPort": 443,
            "IpRanges": [
                {
                    "CidrIp": "0.0.0.0/0",
                    "Description": ""
                }
            ]
        },
        {
            "IpProtocol": "tcp",
            "FromPort": 8080,
            "ToPort": 8080,
            "UserIdGroupPairs": [
                {
                    "GroupId": "sg-0alb1234",
                    "Description": ""
                }
            ]
        }
    ],
    "Egress": [
        {
            "IpProtocol": "udp",
            "FromPort": 53,
            "ToPort": 53,
            "IpRanges": [
                {
                    "CidrIp": "0.0.0.0/0"
                }
            ]
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidGroupId.NotFound) when calling the AuthorizeSecurityGroupIngress operation: The security group 'sg-0abc1234' does not exist`** — Verify the security group ID exists in the correct AWS region using `aws ec2 describe-security-groups --region <region>`.
    **`An error occurred (InvalidPermission.Duplicate) when calling the AuthorizeSecurityGroupIngress operation: The specified rule already exists`** — Remove the duplicate rule first with `revoke-security-group-ingress` or check existing rules with `describe-security-groups`.
    **`An error occurred (UnauthorizedOperation) when calling the AuthorizeSecurityGroupIngress operation: You are not authorized to perform this operation`** — Ensure your IAM user/role has `ec2:AuthorizeSecurityGroupIngress` and `ec2:AuthorizeSecurityGroupEgress` permissions.
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


```text title="Expected output"
{
    "VpcPeeringConnection": {
        "VpcPeeringConnectionId": "pcx-0abc1234def5",
        "RequesterVpcInfo": {
            "VpcId": "vpc-0requester",
            "OwnerId": "123456789012",
            "CidrBlock": "10.0.0.0/16"
        },
        "AccepterVpcInfo": {
            "VpcId": "vpc-0accepter",
            "OwnerId": "987654321098",
            "CidrBlock": "10.1.0.0/16",
            "Region": "eu-central-1"
        },
        "Status": {
            "Code": "initiating-request",
            "Message": "Initiating Request to 987654321098"
        },
        "Tags": [
            {
                "Key": "Name",
                "Value": "peer-prod-to-dr"
            }
        ]
    }
}
{
    "VpcPeeringConnection": {
        "VpcPeeringConnectionId": "pcx-0abc1234def5",
        "Status": {
            "Code": "active",
            "Message": "Active"
        }
    }
}
active
{
    "Return": true
}
{
    "Return": true
}
PING 10.1.5.42 (10.1.5.42) 56(84) bytes of data.
64 bytes from 10.1.5.42: icmp_seq=1 ttl=64 time=15.3 ms
64 bytes from 10.1.5.42: icmp_seq=2 ttl=64 time=14.8 ms
64 bytes from 10.1.5.42: icmp_seq=3 ttl=64 time=15.1 ms
--- 10.1.5.42 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
```

!!! warning "Common errors"
    **`An error occurred (InvalidVpcID.NotFound) when calling the CreateVpcPeeringConnection operation: The vpc ID 'vpc-0requester' does not exist`** — Verify both VPC IDs exist in the requester account and use correct region context.
    **`An error occurred (InvalidParameterValue) when calling the AcceptVpcPeeringConnection operation: The vpc peering connection 'pcx-0abc1234' does not exist`** — Ensure the peering connection ID from Step 1 output is copied exactly and the accepter account has permissions to accept it.
    **`An error occurred (RouteAlreadyExists) when calling the CreateRoute operation: The route identified by destination CIDR 10.1.0.0/16 already exists in route table rtb-0requester`** — Delete the existing route first with `aws ec2 delete-route` or use a different destination CIDR block.
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


```text title="Expected output"
{
    "Role": {
        "Path": "/",
        "RoleName": "MyAppRole",
        "RoleId": "AIDAQ7EXAMPLE2K5QZXYZ",
        "Arn": "arn:aws:iam::123456789012:role/MyAppRole",
        "CreateDate": "2024-01-15T14:32:18+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    }
}
{
    "InstanceProfile": {
        "Path": "/",
        "InstanceProfileName": "MyAppProfile",
        "InstanceProfileId": "AIPAQ7EXAMPLE9K2MNOP",
        "Arn": "arn:aws:iam::123456789012:instance-profile/MyAppProfile",
        "CreateDate": "2024-01-15T14:32:22+00:00",
        "Roles": []
    }
}
{
    "IamInstanceProfile": {
        "Arn": "arn:aws:iam::123456789012:instance-profile/MyAppProfile",
        "Id": "AIPAQ7EXAMPLE9K2MNOP"
    }
}
---------------------------------------------------------------------------------------
AttachmentCount    PolicyName                      PolicyType
---------------------------------------------------------------------------------------
1                  AmazonS3ReadOnlyAccess          Managed
1                  MyAppInlinePolicy               Inline
---------------------------------------------------------------------------------------
```

!!! warning "Common errors"
    **`An error occurred (EntityAlreadyExists) when calling the CreateRole operation: Role with name MyAppRole already exists`** — Delete the existing role with `aws iam delete-role --role-name MyAppRole` first, or use a different role name.
    **`An error occurred (NoSuchEntity) when calling the AssociateIamInstanceProfile operation: The instance profile with name MyAppProfile cannot be found`** — Ensure the instance profile was created successfully and the name matches exactly; wait a few seconds for eventual consistency.
    **`An error occurred (InvalidParameterValue) when calling the AssociateIamInstanceProfile operation: The specified instance does not exist`** — Verify the instance ID is correct and the instance is in a running or stopped state (not terminated).
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


```text title="Expected output"
{
    "TopicArn": "arn:aws:sns:eu-west-1:123456789012:ops-alerts"
}
{
    "SubscriptionArn": "arn:aws:sns:eu-west-1:123456789012:ops-alerts:12a3b4c5-d6e7-8f9a-0b1c-2d3e4f5a6b7c"
}
(no output — command completes silently)
(no output — command completes silently)
{
    "State": "INSUFFICIENT_DATA",
    "Reason": "Insufficient Data: 1 datapoint [2024-01-15 14:32:00.0 (Average: 45.2)] was received for the metric."
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the CreateTopic operation: Topic names must be made up of only uppercase and lowercase ASCII letters, numbers, underscores, and hyphens, and must be between 1 and 256 characters long`** — Replace hyphens in the topic name with underscores (e.g., `ops_alerts`).
    **`An error occurred (InvalidParameterValue) when calling the PutMetricAlarm operation: Invalid alarm action: arn:aws:sns:eu-west-1:<account>:ops-alerts`** — Verify the SNS topic ARN exists and replace `<account>` with your actual AWS account ID.
    **`An error occurred (ValidationError) when calling the DescribeAlarms operation: 1 validation error detected: Value '<instance-id>' at 'alarmNames' failed a validation constraint: Member must satisfy regular expression pattern: [\x20-\x7E]*`** — Replace `<instance-id>` with the actual EC2 instance ID (e.g., `i-0a1b2c3d4e5f6g7h8`).
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


```text title="Expected output"
{
    "ImageId": "ami-0a7f3d8c9e2b1f4d6"
}

Waiting for image-available with max attempts 40 and delay 15 seconds...
(no output — command completes silently)

{
    "Return": true
}

---------------------------------------------------------------------------
|                             DescribeImages                              |
---------------------------------------------------------------------------
||                          ID                    |  Name  |  State  | Created           ||
|+----------------------------------------------+--------+---------+-------------------+|
||  ami-0a7f3d8c9e2b1f4d6                       |  my-instance-baseline  |  available  |  2024-01-15T09:42:18.000Z  ||
||  ami-087b2c5f3e9d1a4b2                       |  my-instance-20240114  |  available  |  2024-01-14T14:22:05.000Z  ||
||  ami-0f2e8b1c3d9a5f7e4                       |  prod-baseline-v2      |  available  |  2024-01-10T11:33:42.000Z  ||
---------------------------------------------------------------------------

{
    "Instances": [
        {
            "InstanceId": "i-0d4e9f2c8a1b3e5f7",
            "ImageId": "ami-0a7f3d8c9e2b1f4d6",
            "State": {
                "Code": 0,
                "Name": "pending"
            },
            "InstanceType": "t3.medium",
            "LaunchTime": "2024-01-15T09:47:22.000Z",
            "SubnetId": "subnet-0c8f2e1d9a3b5f7e4",
            "SecurityGroups": [
                {
                    "GroupId": "sg-0a9f2e1c8d3b5f7e4",
                    "GroupName": "prod-app-sg"
                }
            ]
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidInstanceID.NotFound) when calling the CreateImage operation: The instance ID '<instance-id>' does not exist`** — Replace `<instance-id>` with a valid running or stopped instance ID from your account and region.
    **`An error occurred (InvalidAMIID.NotFound) when calling the WaitImageAvailable operation: The image id '[<ami-id>]' does not exist`** — Verify the AMI ID from the create-image output matches the wait command, or check that the image exists in your current AWS region.
    **`An error occurred (InvalidKeyPair.NotFound) when calling the RunInstances operation: The key pair '<keypair>' does not exist`** — Confirm the EC2 key pair name exists in your region using `aws ec2 describe-key-pairs` and update the `--key-name` parameter.
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


```text title="Expected output"
{
    "StoppingInstances": [
        {
            "CurrentState": {
                "Code": 64,
                "Name": "stopping"
            },
            "InstanceId": "i-0a7f2c9e1b4d5f8a2",
            "PreviousState": {
                "Code": 16,
                "Name": "running"
            }
        }
    ]
}
"stopped"
{
    "ModifyInstanceAttributeResponse": {
        "Return": true
    }
}
"m6i.xlarge"
{
    "StartingInstances": [
        {
            "CurrentState": {
                "Code": 0,
                "Name": "pending"
            },
            "InstanceId": "i-0a7f2c9e1b4d5f8a2",
            "PreviousState": {
                "Code": 80,
                "Name": "stopped"
            }
        }
    ]
}
{
    "InstanceStatuses": [
        {
            "InstanceId": "i-0a7f2c9e1b4d5f8a2",
            "InstanceStatus": {
                "Status": "ok"
            },
            "SystemStatus": {
                "Status": "ok"
            }
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the ModifyInstanceAttribute operation: The instance type 'm6i.xlarge' is not compatible with the instance's current architecture or availability zone.`** — Verify the target instance type is available in the instance's AZ using `aws ec2 describe-instance-types --instance-types m6i.xlarge --query 'InstanceTypes[0].SupportedArchitectures'`.
    **`An error occurred (InvalidInstanceID.NotFound) when calling the StopInstances operation: The instance ID '<instance-id>' does not exist`** — Replace `<instance-id>` with a valid instance ID from your account, or verify the correct AWS region is configured.
    **`An error occurred (IncorrectInstanceState) when calling the ModifyInstanceAttribute operation: The instance 'i-0a7f2c9e1b4d5f8a2' is not in the stopped state.`** — Ensure the instance has fully transitioned to "stopped" state before modifying attributes; increase the wait time or manually verify with `aws ec2 describe-instances`.
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


```text title="Expected output"
make_bucket: my-vpc-flowlogs-123456789012
{
    "Unsuccessful": [],
    "Successful": [
        {
            "ResourceId": "vpc-0abc1234",
            "FlowLogId": "fl-0d1e2f3a4b5c6d7e8"
        }
    ]
}
{
    "Role": {
        "RoleName": "VPCFlowLogsRole",
        "Arn": "arn:aws:iam::123456789012:role/VPCFlowLogsRole",
        "CreateDate": "2024-01-15T10:42:33+00:00"
    }
}
(no output — command completes silently)
(no output — command completes silently)
{
    "LogGroups": [
        {
            "LogGroupName": "/aws/vpc/flowlogs/vpc-0abc1234",
            "CreationTime": 1705318953000,
            "RetentionInDays": 0,
            "MetricFilterCount": 0,
            "Arn": "arn:aws:logs:eu-west-1:123456789012:log-group:/aws/vpc/flowlogs/vpc-0abc1234"
        }
    ]
}
{
    "Unsuccessful": [],
    "Successful": [
        {
            "ResourceId": "vpc-0abc1234",
            "FlowLogId": "fl-0a9b8c7d6e5f4g3h2"
        }
    ]
}
FlowLogs:
- Destination: arn:aws:s3:::my-vpc-flowlogs-123456789012/vpc/
  ID: fl-0d1e2f3a4b5c6d7e8
  Status: ACTIVE
  Type: s3
- Destination: /aws/vpc/flowlogs/vpc-0abc1234
  ID: fl-0a9b8c7d6e5f4g3h2
  Status: ACTIVE
  Type: cloud-watch-logs
```

!!! warning "Common errors"
    **`An error occurred (BucketAlreadyExists) when calling the MakeBucket operation: The requested bucket name is not available.`** — Use a globally unique bucket name by appending a timestamp or UUID to the bucket name.
    **`An error occurred (InvalidParameterValue) when calling the CreateFlowLogs operation: Invalid log destination ARN.`** — Verify the S3 bucket exists and the ARN format is correct: `arn:aws:s3:::bucket-name/prefix/`.
    **`An error occurred (NoSuchEntity) when calling the PutRolePolicy operation: The role with name VPCFlowLogsRole cannot be found.`** — Ensure the IAM role creation completed successfully and wait a few seconds for IAM propagation before attaching the policy.
Traffic type options:

| `--traffic-type` | What is captured |
|---|---|
| `ALL` | Accepted and rejected traffic |
| `ACCEPT` | Only traffic allowed by security group and NACL rules |
| `REJECT` | Only traffic denied by security group or NACL rules |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Aws — Health Checks](../health-checks/)
- [Aws — CLI Reference](../cli-reference/)
- [Aws — Common Issues](../../troubleshooting/common-issues/)
