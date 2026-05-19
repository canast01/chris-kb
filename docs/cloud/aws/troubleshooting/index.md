# AWS — Troubleshooting

```
┌──────────────────────────────────── AWS Troubleshooting Overview ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                AWS Troubleshooting — Common Issues, Diagnostics, and Escalation               │   │
│   │   Common issues: IAM permission denied · SG/NACL blocking traffic · EC2 instance unreachable  │   │
│   │  Diagnostics: CloudWatch Logs · CloudTrail event history · VPC Flow Logs · EC2 serial console │   │
│   │    Tools: AWS CLI describe commands · Policy Simulator · Reachability Analyzer · CloudShell   │   │
│   │ Escalation: AWS Support cases; collect account ID, region, resource ARN, error message + time │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide investigation · Diagnostics locate root cause · Escalation engages AWS support │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │     EC2: 2/2 status fail    │  │     CW Logs: app errors     │  │     Account ID + region     │   │
│   │      SG: port not open      │  │   CloudTrail: API history   │  │    Resource ARN: include    │   │
│   │      IAM: Access Denied     │  │    VPC Flow Logs: traffic   │  │     Error message + time    │   │
│   │      RDS: conn refused      │  │    Policy Simulator: test   │  │       Severity: P1-P4       │   │
│   │      S3: 403 on object      │  │    Reachability Analyzer    │  │    TAM: strategic issues    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Identify issue category → gather diagnostics (logs + trail + flow) → resolve or escalate with data │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │     Escalation    │    CLI Tools     │  Console Tools   │   │
│   │ EC2 unreachable  │ CW Logs: filter  │   P1: 24/7 phone  │   describe-sgs   │ Policy Simulator │   │
│   │ SG: missing rule │ CloudTrail: who? │   Case: open now  │  flow-logs: get  │  Reach Analyzer  │   │
│   │   IAM: denied    │  VPC Flow Logs   │  ARN + error msg  │  sts get-caller  │  EC2 serial con  │   │
│   │  S3: bucket ACL  │  Serial console  │  Trusted Advisor  │   ec2 describe   │  AWS Health evt  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  EC2 Nitro hosts · VPC network fabric · AWS Support infrastructure · CloudTrail S3 log delivery       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  EC2 status check = System check (infra) + instance check (OS); failure triggers alarm or auto-recover│
│  Policy Simulator = IAM console tool; tests IAM policies to check if an action would be allowed/denied│
│  Reachability Analyzer= VPC tool; traces packet path between source and destination; finds blocking ru│
│  VPC Flow Logs   = Captures accepted/rejected traffic metadata for subnets, VPCs, or ENIs             │
│  CloudTrail      = Records every AWS API call; start with event history for the last 90 days in consol│
│  EC2 Serial Console= Out-of-band console access; useful when SSH/SSM unreachable; OS-level triage     │
│  Trusted Advisor  = AWS checks across cost, security, performance, fault tolerance, and service limits│
│  P1 case          = Production down; 24/7 response; call +1-800-xxx alongside opening console case    │
│  TAM              = Technical Account Manager; named AWS contact for strategic and critical escalation│
│  sts get-caller-identity= CLI command returning current identity; first step when debugging IAM issues│
│  Session Manager  = SSM feature; connect to EC2 without SSH when networking is broken but SSM agent wo│
│  Access Denied    = IAM error; check CloudTrail for the denied call; use Policy Simulator to trace    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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
