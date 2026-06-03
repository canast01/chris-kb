# AWS — Health Checks


<div class="kb-summary">
Health Checks reference covering Quick Account Health Overview, RDS Health, EKS Cluster Health, Load Balancer Health, CloudWatch Alarms in ALARM State and 5 more sections.
</div>

---

## Quick Account Health Overview

```bash
# Check AWS Health for active issues affecting your account
aws health describe-events \
  --filter '{"eventStatusCodes":["open","upcoming"]}' \
  --query 'events[*].[service,eventTypeCode,region,statusCode,startTime]' \
  --output table

# Current caller identity (confirm correct account/role)
aws sts get-caller-identity
```text
┌─────────────────────────────────── AWS Operations — Health Checks ────────────────────────────────────┐
│                                                                                                       │
│  Health verification procedures for EC2 instances, load balancers, RDS, and services.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              EC2 Health Checks               │  │              ELB Health Checks              │   │
│   │      System status: hardware + network       │  │       HTTP path + expected status code      │   │
│   │        Instance status: OS + software        │  │        Interval: 5s or 30s (ALB/NLB)        │   │
│   │      Auto-recovery on system check fail      │  │       Healthy threshold: N consecutive      │   │
│   │     CloudWatch: StatusCheckFailed alarm      │  │       Unhealthy: removed from rotation      │   │
│   │        SSM: run command to verify app        │  │      Route 53 health check: DNS remove      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Failed health checks trigger alarm actions and Auto Scaling replacement of instances.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Database Health                │  │             Service-Level Checks            │   │
│   │       RDS: Enhanced Monitoring metrics       │  │       CloudWatch alarms: CPU/mem/disk       │   │
│   │      RDS: describe-db-instances status       │  │        CloudWatch Synthetics canaries       │   │
│   │      RDS: Performance Insights queries       │  │       Route 53: endpoint health checks      │   │
│   │        DynamoDB: ConsumedCapacity CW         │  │       AWS Health: account event status      │   │
│   │       ElastiCache: cluster node status       │  │       Systems Manager OpsCenter items       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS EC2 host hardware · ELB infrastructure per AZ · CloudWatch data collection agents                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  System status check= EC2 check for AWS hardware and network issues under the instance                │
│  Instance status check= EC2 check for OS-level software and network configuration                     │
│  Auto-recovery   = EC2 action that migrates instance to healthy host on system failure                │
│  ELB health check= Load balancer probe that marks targets healthy or unhealthy                        │
│  Healthy threshold= Number of consecutive successful checks to mark target healthy                    │
│  Unhealthy threshold= Consecutive failures before target removed from load balancer                   │
│  Synthetics canary= Scripted check that simulates user actions against an endpoint                    │
│  Enhanced Monitoring= Per-second RDS OS metrics via CloudWatch agent on the host                      │
│  Performance Insights= RDS query-level analysis tool showing wait states and top SQL                  │
│  OpsCenter item  = Systems Manager work item created from CloudWatch alarm or event                   │
│  StatusCheckFailed= CloudWatch metric: 1 if either EC2 status check is failing                        │
│  Route 53 health = External probe; fails DNS failover if endpoint unreachable                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## EKS Cluster Health

```bash
# Cluster status
aws eks describe-cluster --name my-cluster \
  --query 'cluster.[name,status,version,endpoint]' --output table

# Node group status
aws eks list-nodegroups --cluster-name my-cluster --output text | \
  xargs -I{} aws eks describe-nodegroup \
    --cluster-name my-cluster \
    --nodegroup-name {} \
    --query 'nodegroup.[nodegroupName,status,scalingConfig.desiredSize,health.issues]'

# After kubeconfig update — node and pod health
aws eks update-kubeconfig --name my-cluster --region eu-west-1
kubectl get nodes -o wide
kubectl get pods -A | grep -v Running | grep -v Completed
```

---

## Load Balancer Health

```bash
# ALB / NLB target group health
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:eu-west-1:<account>:targetgroup/my-tg/<id> \
  --query 'TargetHealthDescriptions[*].[Target.Id,TargetHealth.State,TargetHealth.Reason]' \
  --output table

# List load balancers and state
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[*].[LoadBalancerName,State.Code,Type,DNSName]' \
  --output table
```

---

## CloudWatch Alarms in ALARM State

```bash
aws cloudwatch describe-alarms \
  --state-value ALARM \
  --query 'MetricAlarms[*].[AlarmName,StateReason,Namespace,MetricName]' \
  --output table
```

---

## S3 Health

```bash
# Verify bucket versioning and replication status
aws s3api get-bucket-versioning --bucket my-prod-bucket
aws s3api get-bucket-replication --bucket my-prod-bucket \
  --query 'ReplicationConfiguration.Rules[*].[ID,Status,Destination.Bucket]' \
  --output table

# Lifecycle rules in place
aws s3api get-bucket-lifecycle-configuration --bucket my-prod-bucket \
  --query 'Rules[*].[ID,Status,Expiration]'
```

---

## Certificate Manager (ACM)

```bash
# List certificates and expiry
aws acm list-certificates \
  --query 'CertificateSummaryList[*].[DomainName,CertificateArn,Status]' \
  --output table

# Check expiry for a specific certificate
aws acm describe-certificate \
  --certificate-arn arn:aws:acm:eu-west-1:<account>:certificate/<id> \
  --query 'Certificate.[DomainName,NotAfter,Status,RenewalSummary.RenewalStatus]'
```

---

## IAM Credential Report

```bash
# Generate credential report (takes ~10s)
aws iam generate-credential-report
sleep 10
aws iam get-credential-report \
  --query 'Content' --output text | base64 -d | \
  awk -F',' 'NR==1 || $5=="true"' | \
  column -t -s','
# Shows: user, arn, mfa_active, access_key_1_active, password_last_used, etc.
```

---

## Security Hub Summary

```bash
# Active findings count by severity
aws securityhub get-findings \
  --filters '{"WorkflowStatus":[{"Value":"NEW","Comparison":"EQUALS"}]}' \
  --query 'length(Findings)' \
  --output text

# Critical + High findings
aws securityhub get-findings \
  --filters '{
    "SeverityLabel":[
      {"Value":"CRITICAL","Comparison":"EQUALS"},
      {"Value":"HIGH","Comparison":"EQUALS"}
    ],
    "WorkflowStatus":[{"Value":"NEW","Comparison":"EQUALS"}]
  }' \
  --query 'Findings[*].[Title,SeverityLabel,ProductName,UpdatedAt]' \
  --output table
```

---

## Daily Health Check Script

```bash
#!/bin/bash
# Quick daily AWS health summary
REGION=${AWS_DEFAULT_REGION:-eu-west-1}
echo "=== $(date) ==="
echo "--- EC2 Status Checks ---"
aws ec2 describe-instance-status \
  --query 'InstanceStatuses[?InstanceStatus.Status!=`ok` || SystemStatus.Status!=`ok`].[InstanceId,SystemStatus.Status,InstanceStatus.Status]' \
  --output table

echo "--- CloudWatch Alarms ---"
aws cloudwatch describe-alarms --state-value ALARM \
  --query 'MetricAlarms[*].[AlarmName,MetricName,StateReason]' --output table

echo "--- RDS Status ---"
aws rds describe-db-instances \
  --query 'DBInstances[?DBInstanceStatus!=`available`].[DBInstanceIdentifier,DBInstanceStatus]' \
  --output table

echo "--- AWS Health Events ---"
aws health describe-events \
  --filter '{"eventStatusCodes":["open"]}' \
  --query 'events[*].[service,region,statusCode,startTime]' \
  --output table 2>/dev/null || echo "(No active health events)"
```
