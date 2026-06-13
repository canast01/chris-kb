---
tags:
  - aws
  - operations
---
# AWS — Health Checks

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Run these eight commands in sequence at the start of every operational shift to get an immediate picture of account health.

```bash
# 1. Account-level health events (open incidents affecting your services)
aws health describe-events \
  --filter eventStatusCodes=open \
  --query 'events[*].{Service:service,Type:eventTypeCode,Region:region,Status:statusCode,Start:startTime}' \
  --output table

# 2. EC2 instances with failing system or instance status checks
aws ec2 describe-instance-status \
  --query 'InstanceStatuses[?InstanceStatus.Status!=`ok` || SystemStatus.Status!=`ok`].{ID:InstanceId,System:SystemStatus.Status,Instance:InstanceStatus.Status,AZ:AvailabilityZone}' \
  --output table

# 3. Unhealthy ELB targets
aws elbv2 describe-target-health \
  --target-group-arn <arn> \
  --query 'TargetHealthDescriptions[?TargetHealth.State!=`healthy`].{ID:Target.Id,Port:Target.Port,State:TargetHealth.State,Reason:TargetHealth.Reason}' \
  --output table

# 4. RDS instance status
aws rds describe-db-instances \
  --query 'DBInstances[].{ID:DBInstanceIdentifier,Class:DBInstanceClass,Engine:Engine,Status:DBInstanceStatus,MultiAZ:MultiAZ}' \
  --output table

# 5. S3 buckets without server-side encryption configured
aws s3api list-buckets --query 'Buckets[].Name' --output text | \
  xargs -I{} sh -c 'aws s3api get-bucket-encryption --bucket {} 2>&1 | grep -q "ServerSideEncryptionConfigurationNotFoundError" && echo "NO ENCRYPTION: {}"'

# 6. IAM access keys older than 90 days
aws iam generate-credential-report
sleep 5
aws iam get-credential-report \
  --query 'Content' --output text | \
  base64 -d | \
  awk -F',' 'NR>1 && $10!="N/A" && $10>90 {print "Key age > 90d:", $1, "last_rotated:", $10}'

# 7. CloudWatch alarms currently in ALARM state
aws cloudwatch describe-alarms \
  --state-value ALARM \
  --query 'MetricAlarms[].{Name:AlarmName,State:StateValue,Namespace:Namespace,Metric:MetricName,Reason:StateReason}' \
  --output table

# 8. Trusted Advisor check summaries (Business/Enterprise support required)
aws support describe-trusted-advisor-check-summaries \
  --check-ids \
    Pfx0RwqBli \
    1iG5NDGVre \
    R365s2Qddf \
    ePs02jT06w \
    Ti39halfu8 \
  --query 'summaries[].{Name:categorySpecificSummary,Status:status}' \
  --output table
```
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

| Status | Meaning | Action |
|---|---|---|
| `ok` / `ok` | Both checks passing | No action required |
| `impaired` / `ok` | AWS hardware/network issue | Open AWS support case; consider stop/start to migrate host |
| `ok` / `impaired` | OS or application issue | SSH in; check kernel, disk, network; review `/var/log/messages` |
| `initializing` | Check not yet complete | Wait 5–10 minutes after instance start |

---

## Network Health

Verify load balancers, VPC connectivity, and DNS resolution.

```bash
# List all load balancers and their state
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[*].{Name:LoadBalancerName,Type:Type,State:State.Code,DNS:DNSName}' \
  --output table

# All target groups and health summary
aws elbv2 describe-target-groups \
  --query 'TargetGroups[*].{Name:TargetGroupName,Protocol:Protocol,Port:Port,LBType:TargetType}' \
  --output table

# Check all target health for a given load balancer
LB_ARN=$(aws elbv2 describe-load-balancers \
  --names <lb-name> --query 'LoadBalancers[0].LoadBalancerArn' --output text)

for TG_ARN in $(aws elbv2 describe-target-groups \
  --load-balancer-arn $LB_ARN \
  --query 'TargetGroups[*].TargetGroupArn' --output text); do
  echo "=== Target Group: $TG_ARN ==="
  aws elbv2 describe-target-health \
    --target-group-arn $TG_ARN \
    --query 'TargetHealthDescriptions[*].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason}' \
    --output table
done

# VPC peering connection states
aws ec2 describe-vpc-peering-connections \
  --query 'VpcPeeringConnections[*].{ID:VpcPeeringConnectionId,Status:Status.Code,Requester:RequesterVpcInfo.VpcId,Accepter:AccepterVpcInfo.VpcId}' \
  --output table

# NAT Gateway status
aws ec2 describe-nat-gateways \
  --query 'NatGateways[*].{ID:NatGatewayId,State:State,VPC:VpcId,SubnetId:SubnetId}' \
  --output table

# VPN connection status
aws ec2 describe-vpn-connections \
  --query 'VpnConnections[*].{ID:VpnConnectionId,State:State,Type:Type,Tunnels:VgwTelemetry[*].Status}' \
  --output table
```

---

## Storage Health

Verify S3, EBS, EFS, and backup integrity.

```bash
# EBS volumes not in "in-use" or "available" state
aws ec2 describe-volumes \
  --filters Name=status,Values=error,deleting,deleted \
  --query 'Volumes[*].{ID:VolumeId,State:State,Size:Size,Type:VolumeType,AZ:AvailabilityZone}' \
  --output table

# EBS volumes with I/O enabled (performance check)
aws ec2 describe-volumes-modifications \
  --filters Name=modification-state,Values=modifying,failed \
  --query 'VolumesModifications[*].{ID:VolumeId,State:ModificationState,Progress:Progress}' \
  --output table

# S3 bucket versioning status
for BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  STATUS=$(aws s3api get-bucket-versioning --bucket $BUCKET --query 'Status' --output text 2>/dev/null || echo "Unknown")
  echo "$BUCKET: $STATUS"
done

# EFS file system health
aws efs describe-file-systems \
  --query 'FileSystems[*].{ID:FileSystemId,State:LifeCycleState,Size:SizeInBytes.Value,Throughput:ThroughputMode}' \
  --output table

# AWS Backup — recent failed jobs
aws backup list-backup-jobs \
  --by-state FAILED \
  --by-created-after $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ) \
  --query 'BackupJobs[*].{ID:BackupJobId,Resource:ResourceArn,State:State,Start:CreationDate,Error:StatusMessage}' \
  --output table

# RDS storage near capacity
aws rds describe-db-instances \
  --query 'DBInstances[*].{ID:DBInstanceIdentifier,Engine:Engine,StorageGB:AllocatedStorage,FreeStorageSpace:Endpoint.Address,MultiAZ:MultiAZ}' \
  --output table
```

---

## IAM and Security

Review access keys, MFA status, Security Hub findings, and CloudTrail integrity.

```bash
# Generate and download IAM credential report
aws iam generate-credential-report
sleep 10
aws iam get-credential-report \
  --query 'Content' --output text | base64 -d > /tmp/iam-report.csv

# Users with MFA not enabled
awk -F',' 'NR>1 && $8=="false" {print "NO MFA:", $1}' /tmp/iam-report.csv

# Access keys unused for > 90 days
awk -F',' 'NR>1 && $10!="N/A" {
  cmd="date -d " $10 " +%s"; cmd | getline key_ts; close(cmd)
  now=systime(); age=int((now - key_ts) / 86400)
  if (age > 90) print "Old key (" age "d):", $1, $10
}' /tmp/iam-report.csv

# Security Hub: critical and high findings
aws securityhub get-findings \
  --filters '{
    "SeverityLabel":[
      {"Value":"CRITICAL","Comparison":"EQUALS"},
      {"Value":"HIGH","Comparison":"EQUALS"}
    ],
    "WorkflowStatus":[{"Value":"NEW","Comparison":"EQUALS"}]
  }' \
  --query 'Findings[*].{Title:Title,Severity:Severity.Label,Product:ProductName,Resource:Resources[0].Id}' \
  --output table

# GuardDuty findings
aws guardduty list-detectors --query 'DetectorIds' --output text | \
  xargs -I{} aws guardduty list-findings \
    --detector-id {} \
    --finding-criteria '{"Criterion":{"severity":{"Gte":7}}}' \
    --query 'FindingIds' --output text

# Recent root account activity (CloudTrail)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=Username,AttributeValue=root \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ) \
  --query 'Events[*].{Time:EventTime,Event:EventName,IP:CloudTrailEvent}' \
  --output table
```

---

## Cost and Billing Alerts

Monitor spend anomalies and budget thresholds to catch unexpected cost spikes early.

```bash
# Current month-to-date cost by service
aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[0].Groups[*].{Service:Keys[0],Cost:Metrics.BlendedCost.Amount}' \
  --output table | sort -k2 -rn | head -20

# Cost anomaly detections (last 7 days)
aws ce get-anomalies \
  --date-interval StartDate=$(date -u -d '7 days ago' +%Y-%m-%d),EndDate=$(date +%Y-%m-%d) \
  --query 'Anomalies[*].{Service:AnomalyScore.CurrentScore,MaxImpact:Impact.MaxImpact,StartDate:AnomalyStartDate}' \
  --output table

# Budget utilisation
aws budgets describe-budgets \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --query 'Budgets[*].{Name:BudgetName,Limit:BudgetLimit.Amount,Actual:CalculatedSpend.ActualSpend.Amount,Forecast:CalculatedSpend.ForecastedSpend.Amount}' \
  --output table

# List cost anomaly monitors
aws ce get-anomaly-monitors \
  --query 'AnomalyMonitors[*].{Name:MonitorName,Type:MonitorType,Spec:MonitorSpecification}' \
  --output table
```

> Billing alarms require the CloudWatch region set to `us-east-1` (global billing metrics are only published there). Use Cost Explorer anomaly detection for multi-service monitoring.

```bash
# Check existing billing alarms (must run in us-east-1)
aws cloudwatch describe-alarms \
  --namespace AWS/Billing \
  --region us-east-1 \
  --query 'MetricAlarms[*].{Name:AlarmName,Threshold:Threshold,State:StateValue}' \
  --output table
```

---

```bash
# Check AWS Health for active issues affecting your account
aws health describe-events \
  --filter '{"eventStatusCodes":["open","upcoming"]}' \
  --query 'events[*].[service,eventTypeCode,region,statusCode,startTime]' \
  --output table

# Current caller identity (confirm correct account/role)
aws sts get-caller-identity
```
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
```bash
aws cloudwatch describe-alarms \
  --state-value ALARM \
  --query 'MetricAlarms[*].[AlarmName,StateReason,Namespace,MetricName]' \
  --output table
```
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
