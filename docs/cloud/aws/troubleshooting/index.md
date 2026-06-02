# AWS — Troubleshooting


<div class="kb-summary">
Troubleshooting reference covering S3 Access Denied, IAM Permission Denied, RDS Connection Issues, VPC Flow Logs — Analysing Traffic, Lambda Timeout Issues.
</div>

```powershell
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
│  EC2 status check = System check (infra) + instance check (OS); failure triggers alarm or             │
│  Policy Simulator = IAM console tool; tests IAM policies to check if an action would be allowed/denied│
│  Reachability Analyzer= VPC tool; traces packet path between source and destination; finds blocking   │
│  VPC Flow Logs   = Captures accepted/rejected traffic metadata for subnets, VPCs, or ENIs             │
│  CloudTrail      = Records every AWS API call; start with event history for the last 90 days in       │
│  EC2 Serial Console= Out-of-band console access; useful when SSH/SSM unreachable; OS-level triage     │
│  Trusted Advisor  = AWS checks across cost, security, performance, fault tolerance, and service limits│
│  P1 case          = Production down; 24/7 response; call +1-800-xxx alongside opening console case    │
│  TAM              = Technical Account Manager; named AWS contact for strategic and critical escalation│
│  sts get-caller-identity= CLI command returning current identity; first step when debugging IAM issues│
│  Session Manager  = SSM feature; connect to EC2 without SSH when networking is broken but SSM agent   │
│  Access Denied    = IAM error; check CloudTrail for the denied call; use Policy Simulator to trace    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known problems, symptoms, and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to AWS Support with the right data.</span>
</a>

</div>

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
