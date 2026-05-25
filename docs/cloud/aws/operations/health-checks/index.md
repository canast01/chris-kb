# AWS — Health Checks

```text
┌─────────────────────────────────────────────────────────┐
│              AWS Health Check Flow                      │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────┼──────────────┐
         ▼             ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐
│   Personal   │ │  CloudWatch  │ │   Trusted Advisor     │
│   Health     │ │   Alarms     │ │   (Cost / Security /  │
│  Dashboard   │ │              │ │    Fault Tolerance)   │
└──────┬───────┘ └──────┬───────┘ └──────────┬───────────┘
       │                │                    │
       ▼                ▼                    ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐
│  AWS Health  │ │  EC2/RDS/EKS │ │   Security Hub        │
│  Events API  │ │   Metrics    │ │   Findings Summary    │
└──────┬───────┘ └──────┬───────┘ └──────────┬───────────┘
       │                │                    │
       └────────────────┴────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Daily Health   │
              │  Check Script   │
              │  (pass / fail)  │
              └─────────────────┘
```

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
```

---

## EC2 Instance Health

```bash
# Instance status checks
aws ec2 describe-instance-status \
  --query 'InstanceStatuses[*].[InstanceId,InstanceState.Name,SystemStatus.Status,InstanceStatus.Status]' \
  --output table

# Instances failing status checks
aws ec2 describe-instance-status \
  --filters "Name=system-status.status,Values=impaired" \
  --query 'InstanceStatuses[*].[InstanceId,SystemStatus.Details[0].Status]' \
  --output table

# CPU utilization — last 5 minutes (single instance)
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-0abc123 \
  --start-time $(date -u -v-5M +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average Maximum \
  --query 'Datapoints[*].[Timestamp,Average,Maximum]' \
  --output table
```

---

## RDS Health

```bash
# List RDS instances and status
aws rds describe-db-instances \
  --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus,Engine,MultiAZ,Endpoint.Address]' \
  --output table

# Check for pending maintenance
aws rds describe-pending-maintenance-actions \
  --query 'PendingMaintenanceActions[*].[ResourceIdentifier,PendingMaintenanceActionDetails[0].Action,PendingMaintenanceActionDetails[0].ForcedApplyDate]' \
  --output table

# RDS FreeStorageSpace (last hour, GB)
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name FreeStorageSpace \
  --dimensions Name=DBInstanceIdentifier,Value=prod-mysql \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 3600 \
  --statistics Minimum \
  --query 'Datapoints[0].Minimum' \
  --output text | awk '{printf "%.2f GB\n", $1/1024/1024/1024}'
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
