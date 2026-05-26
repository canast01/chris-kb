# AWS — Common Issues

---

## EC2 Instance Unreachable / Can't SSH

**Symptoms:** SSH times out; instance status checks show impaired; System Manager session fails

1. **Security group missing inbound rule**:
   ```bash
   aws ec2 describe-security-groups \
     --group-ids sg-0abc123 \
     --query 'SecurityGroups[*].IpPermissions[*].[IpProtocol,FromPort,ToPort,IpRanges[*].CidrIp]' \
     --output table
   # Add rule if missing:
   aws ec2 authorize-security-group-ingress \
     --group-id sg-0abc123 \
     --protocol tcp --port 22 --cidr 10.10.0.0/16
   ```

2. **Network ACL blocking**:
   ```bash
   # Check NACL on the subnet
   aws ec2 describe-network-acls \
     --filters "Name=association.subnet-id,Values=subnet-0abc123" \
     --query 'NetworkAcls[*].Entries[*].[RuleNumber,Protocol,RuleAction,CidrBlock,PortRange]'
   ```

3. **Instance failed system status check**:
   ```bash
   aws ec2 describe-instance-status --instance-ids i-0abc123 \
     --query 'InstanceStatuses[*].[SystemStatus.Status,InstanceStatus.Status]'
   # If system status impaired: stop + start (migrates to new host)
   aws ec2 stop-instances --instance-ids i-0abc123
   aws ec2 start-instances --instance-ids i-0abc123
   ```

4. **No route to instance** (private subnet, no NAT/bastion): use SSM Session Manager instead of SSH.

---

## S3 Access Denied

**Symptoms:** `AccessDenied` when reading or writing to a bucket

1. **Check bucket policy**:
   ```bash
   aws s3api get-bucket-policy --bucket my-bucket
   ```

2. **Check caller's effective permissions**:
   ```bash
   aws iam simulate-principal-policy \
     --policy-source-arn $(aws sts get-caller-identity --query Arn --output text) \
     --action-names s3:GetObject s3:PutObject \
     --resource-arns "arn:aws:s3:::my-bucket/*" \
     --query 'EvaluationResults[*].[EvalActionName,EvalDecision]' \
     --output table
   ```

3. **Block Public Access blocking cross-account access**: verify the bucket-level and account-level Block Public Access settings if the caller is from a different account.

4. **KMS key policy**: if bucket uses SSE-KMS, the caller's role must have `kms:GenerateDataKey` and `kms:Decrypt` permissions on the CMK.

---

## RDS — Cannot Connect

**Symptoms:** Application cannot connect to RDS endpoint; connection refused or timeout

1. **Security group**: RDS security group must allow inbound on port 3306 (MySQL) or 5432 (PostgreSQL) from the application's security group or IP range.
   ```bash
   aws rds describe-db-instances \
     --db-instance-identifier prod-mysql \
     --query 'DBInstances[0].VpcSecurityGroups'
   ```

2. **RDS is in a private subnet with no route**: application must be in the same VPC or connected via VPC peering/PrivateLink.

3. **RDS is stopped**: check instance status.
   ```bash
   aws rds describe-db-instances \
     --db-instance-identifier prod-mysql \
     --query 'DBInstances[0].DBInstanceStatus'
   ```

4. **Parameter group forcing SSL**: application must present SSL certificate when `require_secure_transport=1`.

---

## Lambda — Function Timing Out

**Symptoms:** Lambda invocations return `Task timed out after X seconds`

1. **Increase timeout** (max 900 seconds):
   ```bash
   aws lambda update-function-configuration \
     --function-name my-function \
     --timeout 300
   ```

2. **VPC Lambda cannot reach internet** (no NAT Gateway):
   ```bash
   aws lambda get-function-configuration \
     --function-name my-function \
     --query 'VpcConfig'
   # If VpcId set: function needs a NAT Gateway in the VPC for internet access
   ```

3. **Check CloudWatch logs for the actual error**:
   ```bash
   aws logs filter-log-events \
     --log-group-name /aws/lambda/my-function \
     --filter-pattern "Task timed out" \
     --start-time $(($(date +%s) - 3600))000 \
     --query 'events[*].message' --output text
   ```

---

## EKS — Nodes Not Joining Cluster

**Symptoms:** Node group shows nodes in `NotReady` or nodegroup status `DEGRADED`

1. **aws-auth ConfigMap missing role**:
   ```bash
   kubectl describe configmap aws-auth -n kube-system
   # Must contain the node group IAM role in mapRoles
   ```

2. **IAM role missing required policies** (AmazonEKSWorkerNodePolicy, AmazonEKS_CNI_Policy, AmazonEC2ContainerRegistryReadOnly):
   ```bash
   aws iam list-attached-role-policies --role-name eksNodeRole \
     --query 'AttachedPolicies[*].PolicyName' --output table
   ```

3. **Security group not allowing node-to-control-plane communication**:
   ```bash
   aws eks describe-cluster --name my-cluster \
     --query 'cluster.resourcesVpcConfig.clusterSecurityGroupId'
   # Nodes must be in this security group or allowed by it
   ```

4. **Describe failing node**:
   ```bash
   kubectl describe node <node-name>
   # Look for: FailedMount, NetworkPlugin, KubeletNotReady
   ```

---

## CloudFormation — Stack Stuck in UPDATE_ROLLBACK_FAILED

**Symptoms:** Stack cannot update or roll back; stuck in `UPDATE_ROLLBACK_FAILED` state

```bash
# View the stack events to identify the failed resource
aws cloudformation describe-stack-events \
  --stack-name my-stack \
  --query 'StackEvents[?ResourceStatus==`UPDATE_FAILED`].[LogicalResourceId,ResourceStatusReason]' \
  --output table

# Continue rollback (skip specific resources if they're blocking)
aws cloudformation continue-update-rollback \
  --stack-name my-stack \
  --resources-to-skip LogicalResourceId1 LogicalResourceId2
```

---

## IAM — Access Denied Despite Correct Policy

**Symptoms:** Principal gets `AccessDenied` even though an IAM policy explicitly allows the action

1. **Explicit Deny elsewhere** — a Deny in any policy overrides any Allow:
   - Check attached policies, inline policies, resource-based policies, SCPs, permission boundaries, session policies

2. **SCP at the organization level** blocking the action:
   ```bash
   aws organizations list-policies-for-target \
     --target-id <ou-id> --filter SERVICE_CONTROL_POLICY
   ```

3. **S3 requires both bucket policy + IAM policy** for cross-account access.

4. **Simulate to identify the denial**:
   ```bash
   aws iam simulate-principal-policy \
     --policy-source-arn arn:aws:iam::<account>:role/MyRole \
     --action-names s3:GetObject \
     --resource-arns "arn:aws:s3:::my-bucket/path/file" \
     --query 'EvaluationResults[*].[EvalActionName,EvalDecision,MatchedStatements]'
   ```

---

## EBS Volume Stuck Detaching

**Symptoms:** Volume status shows `in-use` but instance was terminated; cannot attach elsewhere

```bash
# Force detach (may cause data loss if I/O was in progress)
aws ec2 detach-volume \
  --volume-id vol-0abc123 \
  --force

# Check volume status
aws ec2 describe-volumes \
  --volume-ids vol-0abc123 \
  --query 'Volumes[0].[State,Attachments]'
```

---

## Cost Spike — Unexpected Charges

**Symptoms:** Billing alert fires; cost significantly higher than baseline

1. **Identify top services**:
   ```bash
   aws ce get-cost-and-usage \
     --time-period Start=$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d),End=$(date +%Y-%m-%d) \
     --granularity DAILY \
     --metrics "UnblendedCost" \
     --group-by Type=DIMENSION,Key=SERVICE \
     --query 'ResultsByTime[-1].Groups[*].[Keys[0],Metrics.UnblendedCost.Amount]' \
     --output table
   ```

2. **Check for unintended resources** — large EC2/RDS instances, forgotten NAT Gateways, S3 data transfer:
   ```bash
   aws ec2 describe-instances \
     --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,Tags[?Key==`Name`].Value|[0]]' \
     --output table
   ```

3. **Check for data transfer** — GuardDuty or CloudTrail findings may reveal exfiltration patterns.
