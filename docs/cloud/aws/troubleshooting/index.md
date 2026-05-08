# AWS — Troubleshooting

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known failure modes, symptoms, causes, and fixes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>What to collect before opening a support case and how to engage AWS support.</span>
</a>

</div>

## EC2 Connectivity Issues

```bash
# 1. Check security group effective rules
aws ec2 describe-security-groups --group-ids <sg-id> \
    --query 'SecurityGroups[*].IpPermissions'

# 2. Check effective routes on instance NIC
aws ec2 describe-route-tables --filters "Name=association.subnet-id,Values=<subnet-id>"

# 3. Check NACLs
aws ec2 describe-network-acls --filters "Name=association.subnet-id,Values=<subnet-id>"

# 4. Check source/destination check (must be disabled for NAT instances)
aws ec2 describe-network-interfaces --network-interface-ids <eni-id> \
    --query 'NetworkInterfaces[*].SourceDestCheck'

# 5. Test connectivity with Network Reachability Analyser
aws ec2 start-network-insights-analysis \
    --network-insights-path-id <path-id>
```

Common causes:
- Security group missing inbound rule for source CIDR
- Route table missing route to internet gateway (for public subnet instances)
- NACL denying traffic (check both inbound and outbound — NACLs are stateless)

## S3 Access Denied

```bash
# Check bucket policy
aws s3api get-bucket-policy --bucket <bucket-name>

# Check block public access settings
aws s3api get-public-access-block --bucket <bucket-name>

# Check caller's effective permissions
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::<account>:role/<role-name> \
    --action-names s3:GetObject \
    --resource-arns arn:aws:s3:::<bucket-name>/path/to/object

# Check bucket ACL
aws s3api get-bucket-acl --bucket <bucket-name>
```

Common causes:
- Bucket policy explicit `Deny` overrides IAM `Allow`
- Block Public Access enabled at account level overrides bucket policy
- SCP in Organizations denying the action
- Missing `s3:GetObject` in the caller's IAM policy

## IAM Permission Denied

```bash
# Run IAM Policy Simulator for a specific role
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::<account>:role/<role> \
    --action-names ec2:DescribeInstances \
    --resource-arns "*"

# Check if SCP is blocking
# (only accessible from the management account)
aws organizations list-policies-for-target --target-id <account-id> --filter SERVICE_CONTROL_POLICY

# Decode access denied error message
aws sts decode-authorization-message --encoded-message <encoded-msg>
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

## VPC Flow Logs — Analysing Traffic

```bash
# Query Flow Logs in CloudWatch Insights
# CloudWatch → Logs Insights → select flow log group
fields @timestamp, srcAddr, dstAddr, dstPort, action
| filter dstAddr = "<target-ip>" and action = "REJECT"
| sort @timestamp desc
| limit 50
```

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
