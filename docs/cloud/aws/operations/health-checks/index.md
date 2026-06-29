---
tags:
  - aws
  - operations
---
# AWS — Health Checks

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
network_health: "Network Health" {shape: rectangle}
storage_health: "Storage Health" {shape: rectangle}
iam_and_security: "IAM and Security" {shape: rectangle}
cost_and_billing_alerts: "Cost and Billing Alerts" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> network_health
network_health -> storage_health
storage_health -> iam_and_security
iam_and_security -> cost_and_billing_alerts
cost_and_billing_alerts -> verify
verify -> generate_report
```

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


```text title="Expected output"
# 1. Account-level health events
Service    Type                Region      Status    Start
---------  ------------------  ----------  --------  --------------------------
EC2        EC2_INSTANCE_STORE  us-east-1   open      2024-01-15T09:23:45Z
RDS        RDS_MAINTENANCE     eu-west-1  open      2024-01-15T14:00:00Z

# 2. EC2 instances with failing status checks
ID                    System      Instance    AZ
--------------------  ----------  ----------  -----------
i-0a7f2c9e1b4d5f8a2  impaired    ok          us-east-1a
i-1b8g3d0f2c5e6g9b3  ok          impaired    us-east-1b

# 3. Unhealthy ELB targets
ID                    Port    State       Reason
--------------------  ------  ----------  ----------------------
10.0.1.45             8080    unhealthy   Health checks failed
10.0.2.67             8080    draining    Connection limit exceeded

# 4. RDS instance status
ID                  Class           Engine    Status      MultiAZ
------------------  --------------  --------  ----------  ---------
prod-mysql-01       db.r5.2xlarge   mysql     available   True
staging-postgres    db.t3.medium     postgres  available   False

# 5. S3 buckets without server-side encryption
NO ENCRYPTION: legacy-logs-bucket-2019
NO ENCRYPTION: temp-uploads-dev

# 6. IAM access keys older than 90 days
Key age > 90d: alice.johnson 120
Key age > 90d: svc-deploy-user 156

# 7. CloudWatch alarms in ALARM state
Name                          State    Namespace            Metric                Reason
------------------------------  -------  -------------------  --------------------  -------------------------
prod-api-cpu-high             ALARM    AWS/EC2              CPUUtilization        Threshold Crossed: 1 datapoint [85.2]
db-connection-pool-exhausted   ALARM    AWS/RDS              DatabaseConnections   Threshold Crossed: 1 datapoint [450]

# 8. Trusted Advisor check summaries
Name                                    Status
--------------------------------------  --------
Security Groups - Specific Ports        warning
IAM Access Key Rotation                 warning
MFA on Root Account                     ok
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the DescribeEvents operation: Invalid filter value`** — Verify the filter syntax matches AWS Health API documentation; use `--filter eventStatusCodes=OPEN` (uppercase) instead.
    **`An error occurred (InvalidParameterValue) when calling the DescribeTargetHealth operation: Target group arn '<arn>' does not exist`** — Replace `<arn>` with an actual target group ARN from your account (e.g., `arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-targets/abc123def456`).
    **`An error occurred (AccessDenied) when calling the DescribeTrustedAdvisorCheckSummaries operation: User is not authorized to perform: support:DescribeTrustedAdvisorCheckSummaries`
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


```text title="Expected output"
----------------------------------------------------------------------------------
|                          LoadBalancers                                        |
|----------------------------------------------------------------------------------
|  DNS                                      |  Name          |  State  |  Type  |
|----------------------------------------------------------------------------------
|  app-lb-1234567890.us-east-1.elb.amazonaws.com  |  app-lb-prod   |  active |  application |
|  nlb-prod-9876543210.us-east-1.elb.amazonaws.com |  nlb-prod      |  active |  network     |
|  clb-legacy-1122334455.us-east-1.elb.amazonaws.com |  clb-legacy    |  active |  classic     |
----------------------------------------------------------------------------------

----------------------------------------------------------------------------------
|                          TargetGroups                                         |
|----------------------------------------------------------------------------------
|  LBType  |  Name              |  Port  |  Protocol  |
|----------------------------------------------------------------------------------
|  ip      |  tg-api-prod       |  8080  |  HTTP      |
|  instance |  tg-web-prod      |  443   |  HTTPS     |
|  ip      |  tg-backend-staging |  5432 |  TCP       |
----------------------------------------------------------------------------------

=== Target Group: arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/tg-api-prod/a1b2c3d4e5f6g7h8 ===
----------------------------------------------------------------------------------
|                          TargetHealth                                         |
|----------------------------------------------------------------------------------
|  Reason  |  State  |  Target           |
|----------------------------------------------------------------------------------
|  N/A     |  healthy |  10.0.1.42        |
|  N/A     |  healthy |  10.0.2.88        |
|  Connection limit exceeded |  unhealthy |  10.0.3.15 |
----------------------------------------------------------------------------------

----------------------------------------------------------------------------------
|                          VpcPeeringConnections                                |
|----------------------------------------------------------------------------------
|  Accepter          |  ID                    |  Requester        |  Status    |
|----------------------------------------------------------------------------------
|  vpc-0987654321abcdef |  pcx-1a2b3c4d5e6f7g8h |  vpc-abcdef123456 |  active    |
|  vpc-fedcba987654321 |  pcx-9z8y7x6w5v4u3t2s |  vpc-123456abcdef |  pending-acceptance |
----------------------------------------------------------------------------------

----------------------------------------------------------------------------------
|                          NatGateways                                          |
|----------------------------------------------------------------------------------
|  ID                 |  State      |  SubnetId              |  VPC           |
|----------------------------------------------------------------------------------
|  nat-0a1b2c3d4e5f6g7 |  available  |  subnet-1a2b3c4d5e6f7 |  vpc-abcdef123456 |
|  nat-9z8y7x6w5v4u3t2 |  available  |  subnet-8f7e6d5c4b3a2 |  vpc-fedcba987654 |
----------------------------------------------------------------------------------

----------------------------------------------------------------------------------
|                          VpnConnections                                       |
|----------------------------------------------------------------------------------
|  ID                    |  State  |  Type  |
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


```text title="Expected output"
---------------------------------------------------------------------------
|                              DescribeVolumes                            |
---------------------------------------------------------------------------
|  ID           |  State   |  Size  |  Type  |  AZ            |
|---------------|----------|--------|--------|----------------|
|  vol-0a8f2c1b |  error   |  100   |  gp3   |  us-east-1a    |
|  vol-1d4e9f7a |  deleting|  50    |  io1   |  us-west-2b    |
---------------------------------------------------------------------------

---------------------------------------------------------------------------
|                        DescribeVolumesModifications                     |
---------------------------------------------------------------------------
|  ID           |  State     |  Progress  |
|---------------|------------|------------|
|  vol-2b5c8e3d |  modifying |  45%       |
|  vol-3f9a1c6e |  failed    |  0%        |
---------------------------------------------------------------------------

prod-app-logs: Enabled
prod-backups: Suspended
staging-data: Unknown
dev-temp: Enabled

---------------------------------------------------------------------------
|                         DescribeFileSystems                            |
---------------------------------------------------------------------------
|  ID                    |  State      |  Size       |  Throughput    |
|------------------------|-------------|-------------|----------------|
|  fs-0c7d2a1f8b9e4k3m   |  available  |  1099511627 |  bursting      |
|  fs-1a9e3b2f7c8d5k6m   |  creating   |  0          |  provisioned   |
---------------------------------------------------------------------------

---------------------------------------------------------------------------
|                          ListBackupJobs                                |
---------------------------------------------------------------------------
|  ID                    |  Resource                    |  State  |  Error         |
|------------------------|------------------------------|---------|----------------|
|  backup-job-abc123def  |  arn:aws:rds:us-east-1:...  |  FAILED |  Timeout       |
|  backup-job-xyz789ghi  |  arn:aws:ec2:us-west-2:...  |  FAILED |  Access Denied |
---------------------------------------------------------------------------

---------------------------------------------------------------------------
|                        DescribeDBInstances                             |
---------------------------------------------------------------------------
|  ID              |  Engine  |  StorageGB  |  FreeStorageSpace      |  MultiAZ |
|------------------|----------|------------|------------------------|----------|
|  prod-mysql-01   |  mysql8.0|  500       |  prod-mysql-01.c9akciq |  true    |
|  staging-postgres|  postgres|  200       |  staging-postgres.c9ak |  false   |
---------------------------------------------------------------------------
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the DescribeVolumes operation: The filter 'status' does not exist`** — Use `--filters Name=status,Values=error` without the `status` prefix in the filter name, or verify the correct filter name for your AWS CLI version.
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
    **`(InvalidParameterValue) when calling the ListBackupJobs operation: 1 validation error detected: Value at '
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


```text title="Expected output"
{
    "CredentialReportId": "12a34b5c-6789-0def-1234-567890abcdef"
}

NO MFA: alice.johnson
NO MFA: svc-deploy-bot
Old key (156d): bob.smith 2024-07-15T09:22:00Z
Old key (203d): legacy-app-user 2024-05-20T14:11:33Z

|                           Title                            | Severity |      Product      |              Resource              |
|------------------------------------------------------------+----------+-------------------+------------------------------------|
| EC2 instance i-0a1b2c3d4e5f6g7h8 has unrestricted SSH    | HIGH     | AWS GuardDuty     | arn:aws:ec2:us-east-1:123456789:i |
| S3 bucket prod-data-backup has public read access         | CRITICAL | AWS Config        | arn:aws:s3:::prod-data-backup     |
| IAM policy allows s3:* on all resources                   | HIGH     | AWS Access Analyzer | arn:aws:iam::123456789:policy/Ad |
| RDS instance db-prod-01 encryption disabled              | CRITICAL | AWS Security Hub  | arn:aws:rds:us-east-1:123456789: |

finding-id-001a2b3c4d5e6f7g8h9i0j1k2l3m4n5o finding-id-002b3c4d5e6f7g8h9i0j1k2l3m4n5o6 finding-id-003c4d5e6f7g8h9i0j1k2l3m4n5o6p

|           Time            |      Event      |                    IP                    |
|---------------------------+-----------------+------------------------------------------|
| 2025-01-10T14:32:15Z      | ConsoleLogin    | {"sourceIPAddress":"203.0.113.42"}       |
| 2025-01-09T08:19:47Z      | CreateAccessKey | {"sourceIPAddress":"203.0.113.42"}       |
| 2025-01-05T22:11:22Z      | DeleteUser      | {"sourceIPAddress":"198.51.100.89"}      |
```

!!! warning "Common errors"
    **`An error occurred (AccessDenied) when calling the GenerateCredentialReport operation: User: arn:aws:iam::123456789:user/ops-user is not authorized to perform: iam:GenerateCredentialReport`** — Add `iam:GenerateCredentialReport` and `iam:GetCredentialReport` permissions to the IAM user or role running this script.
    **`date: invalid date '2024-07-15T09:22:00Z'`** — Use `date -d "2024-07-15T09:22:00Z" +%s` (with quotes around the date string) or install GNU coreutils if on macOS.
    **`An error occurred (InvalidParameterException) when calling the GetFindings operation: 1 validation error detected`** — Ensure the `--filters` JSON is valid; use `--filters file://filters.json` if the filter structure is complex, or verify SeverityLabel values match AWS documentation exactly.
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


```text title="Expected output"
---------------------------------------------------------------------------------------------------------
|                                    Service                                    |        Cost         |
---------------------------------------------------------------------------------------------------------
| Amazon Elastic Compute Cloud - Compute                                        |     1847.32         |
| Amazon Simple Storage Service                                                 |      892.15         |
| AWS Lambda                                                                    |      445.67         |
| Amazon Relational Database Service                                            |      334.89         |
| Amazon DynamoDB                                                               |      156.23         |
| AWS CloudTrail                                                                |       89.45         |
| Amazon CloudWatch                                                             |       67.12         |
...

-----------------------------------------  Anomalies  ------------------------------------------
|                Service                |    MaxImpact    |      StartDate      |
-----------------------------------------  Anomalies  ------------------------------------------
| Amazon Elastic Compute Cloud - Compute |     234.56      | 2024-01-15T08:30:00Z|
| Amazon Simple Storage Service          |      67.89      | 2024-01-18T14:22:00Z|

-----------------------------------  Budgets  -----------------------------------
|              Name              |    Limit    |   Actual    |  Forecast   |
|-----------------------------------  Budgets  ---|
| Production-Monthly-Budget      |   5000.00   |  3847.32    |  4156.78    |
| Development-Monthly-Budget     |   1500.00   |   892.15    |  1023.45    |
| Data-Transfer-Budget           |    800.00   |   445.67    |   567.89    |

-----------  AnomalyMonitors  -----------
|           Name            |    Type    |         Spec         |
|--------  AnomalyMonitors  --------|
| Production-Monitor        | DIMENSIONAL| SERVICE              |
| Cost-Spike-Monitor        | CUSTOM     | EC2,RDS,Lambda       |
```

!!! warning "Common errors"
    **`An error occurred (AccessDenied) when calling the GetCostAndUsage operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: ce:GetCostAndUsage`** — Attach the `CE_ReadOnly` or `Billing` IAM policy to the user or role executing the command.
    **`An error occurred (ValidationException) when calling the DescribeBudgets operation: Invalid account id`** — Verify the AWS account ID is correct and the IAM principal has `budgets:DescribeBudgets` permission.
    **`date: invalid date 'TZ=UTC0 7 days ago'`** — Use `date -d '7 days ago' +%Y-%m-%d` (without `-u` flag) or ensure GNU coreutils is installed on macOS by using `brew install coreutils` and calling `gdate` instead.
> Billing alarms require the CloudWatch region set to `us-east-1` (global billing metrics are only published there). Use Cost Explorer anomaly detection for multi-service monitoring.

```bash
# Check existing billing alarms (must run in us-east-1)
aws cloudwatch describe-alarms \
  --namespace AWS/Billing \
  --region us-east-1 \
  --query 'MetricAlarms[*].{Name:AlarmName,Threshold:Threshold,State:StateValue}' \
  --output table
```


```text title="Expected output"
-------------------------------------------------------------------------------------------------
|                                    DescribeAlarms                                            |
+---------------------------------+---------------+---------------+
|             Name                |   Threshold   |     State     |
+---------------------------------+---------------+---------------+
|  monthly-spend-500-usd          |  500.0        |  OK           |
|  daily-spend-100-usd            |  100.0        |  ALARM        |
|  forecast-1000-usd              |  1000.0       |  OK           |
|  critical-spend-2000-usd        |  2000.0       |  INSUFFICIENT_DATA |
+---------------------------------+---------------+---------------+
```

!!! warning "Common errors"
    **`An error occurred (UnauthorizedOperation) when calling the DescribeAlarms operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: cloudwatch:DescribeAlarms`** — Add `cloudwatch:DescribeAlarms` permission to the IAM user/role policy.
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
    **`The Billing namespace does not have any alarms configured`** — Create billing alarms first using `aws cloudwatch put-metric-alarm` with `--namespace AWS/Billing`.
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

```text title="Expected output"
┌─────────────────┬──────────────────────────────┬────────────┬──────────┬──────────────────────────────┐
│ service         │ eventTypeCode                │ region     │ statusCode │ startTime                  │
├─────────────────┼──────────────────────────────┼────────────┼──────────┼─────────────────────────┤
│ EC2             │ AWS_EC2_INSTANCE_STORE_DRIVE │ us-east-1  │ open     │ 2024-01-15T09:23:45Z         │
│ RDS             │ AWS_RDS_MAINTENANCE_SCHEDULED│ eu-west-1  │ upcoming │ 2024-01-20T02:00:00Z         │
└─────────────────┴──────────────────────────────┴────────────┴──────────┴──────────────────────────────┘

{
    "UserId": "AIDAI7X3Z4K9MPLQ5N2B",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/ops-admin"
}
```

!!! warning "Common errors"
    **`An error occurred (AccessDenied) when calling the DescribeEvents operation: User: arn:aws:iam::123456789012:user/ops-admin is not authorized to perform: health:DescribeEvents`** — Add `health:DescribeEvents` permission to the IAM user/role policy.
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
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

```text title="Expected output"
|  name      |  status  | version |                    endpoint                     |
|------------|----------|---------|--------------------------------------------------|
|  my-cluster|  ACTIVE  |  1.28   | https://ABC123DEF456.eks.eu-west-1.amazonaws.com |

nodegroup-1	ACTIVE	3	[]
nodegroup-2	ACTIVE	2	[]
nodegroup-3	UPDATING	2	[{'message': 'Ec2LaunchTemplateIdMismatch', 'resourceIds': ['i-0a1b2c3d4e5f6g7h8']}]

Added new context arn:aws:eks:eu-west-1:123456789012:cluster/my-cluster to /home/user/.kube/config
NAME                          STATUS   ROLES    AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE
ip-10-0-1-45.ec2.internal    Ready    <none>   45d   v1.28.1   10.0.1.45        <none>        Amazon Linux 2
ip-10-0-2-67.ec2.internal    Ready    <none>   45d   v1.28.1   10.0.2.67        <none>        Amazon Linux 2
ip-10-0-3-89.ec2.internal    NotReady <none>   12d   v1.28.1   10.0.3.89        <none>        Amazon Linux 2

NAMESPACE     NAME                                    READY   STATUS             RESTARTS   AGE
kube-system   coredns-558bd4d5db-7x9kl               0/1     CrashLoopBackOff   8          2h
monitoring    prometheus-operator-5d4f8c9b2-m4lkj    1/2     ImagePullBackOff   0          1h
default       app-deployment-6f7g8h9i0-9j2k3l4m5     0/3     Pending            0          45m
```

!!! warning "Common errors"
    **`An error occurred (ResourceNotFoundException) when calling the DescribeCluster operation: No cluster found for name: my-cluster.`** — Verify the cluster name matches exactly and you are querying the correct AWS region with `--region`.
    **`error: You must be logged in to the server (Unauthorized)`** — Run `aws eks update-kubeconfig --name my-cluster --region eu-west-1` to refresh your kubeconfig credentials.
    **`error: exec plugin: invalid apiVersion "client.authentication.k8s.io/v1alpha1"`** — Update your AWS CLI to the latest version with `pip install --upgrade awscli` to fix kubeconfig authentication plugin version mismatch.
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

```text title="Expected output"
-------------------------------------------------------------------------------------------------
|                                    TargetHealthDescriptions                                  |
+---------------------------+----------+----------------------------------------------------------+
|  i-0a7f2c9d4e1b5f3a2    |  healthy |  N/A                                                     |
|  i-0b3e1f8c9a2d7e4f5    |  healthy |  N/A                                                     |
|  i-0c5d9a2f1e8b3c7g6    |  unhealthy |  Target.ResponseCodeMismatch                            |
|  i-0d2e4b7f9c1a6d8h3    |  draining |  Connection draining in progress                        |
+---------------------------+----------+----------------------------------------------------------+

---

-------------------------------------------------------------------------------------------------
|                                      LoadBalancers                                           |
+---------------------+----------+-------+--------------------------------------------------+
|  my-app-alb         |  active  |  application |  my-app-alb-1234567890.eu-west-1.elb.amazonaws.com |
|  my-nlb-prod        |  active  |  network     |  my-nlb-prod-9876543210.eu-west-1.elb.amazonaws.com |
|  legacy-alb-old     |  provisioning |  application |  legacy-alb-old-5555555555.eu-west-1.elb.amazonaws.com |
+---------------------+----------+-------+--------------------------------------------------+
```

!!! warning "Common errors"
    **`An error occurred (LoadBalancerNotFound) when calling the DescribeTargetHealth operation: There is no target group found for arn`** — Verify the target group ARN is correct and exists in the current AWS region and account.
    **`An error occurred (AccessDenied) when calling the DescribeLoadBalancers operation: User: arn:aws:iam::<account>:user/<user> is not authorized`** — Add `elasticloadbalancing:Describe*` permissions to the IAM user or role policy.
```bash
aws cloudwatch describe-alarms \
  --state-value ALARM \
  --query 'MetricAlarms[*].[AlarmName,StateReason,Namespace,MetricName]' \
  --output table
```

```text title="Expected output"
---------------------------------------------------------------------------------------------------------
|                                    DescribeAlarms                                                   |
+----------------------------------------+---------------------------+---------------+----------------+
| AlarmName                              | StateReason               | Namespace     | MetricName     |
+----------------------------------------+---------------------------+---------------+----------------+
| prod-api-high-cpu                      | Threshold Crossed: 87.3% > 80.0%  | AWS/EC2       | CPUUtilization |
| rds-db-connection-pool-exhausted       | Threshold Crossed: 156 > 150      | AWS/RDS       | DatabaseConnections |
| elb-unhealthy-host-count               | Threshold Crossed: 2 > 0          | AWS/ELB       | UnHealthyHostCount |
| lambda-error-rate-spike                | Threshold Crossed: 12.5% > 5.0%   | AWS/Lambda    | Errors         |
| s3-replication-lag-critical            | Threshold Crossed: 4521ms > 3000ms| AWS/S3        | ReplicationLatency |
+----------------------------------------+---------------------------+---------------+----------------+
```
```text

!!! warning "Common errors"
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
    **`An error occurred (UnauthorizedOperation) when calling the DescribeAlarms operation: User is not authorized to perform: cloudwatch:DescribeAlarms`** — Add the `cloudwatch:DescribeAlarms` permission to your IAM user or role policy.
    **`An error occurred (InvalidParameterValue) when calling the DescribeAlarms operation: Invalid value for parameter StateValue: ALARM`** — Use valid state values: `ALARM`, `INSUFFICIENT_DATA`, or `OK` (case-sensitive).
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

```text title="Expected output"
{
    "Status": "Enabled",
    "MFADelete": "Disabled"
}
---------------------------------------------------------------------------
|                         ReplicationConfiguration                        |
|---------------------------------------------------------------------------|
|  ID                    |  Status  |  Destination.Bucket                |
|---------------------------------------------------------------------------|
|  replicate-to-dr       |  Enabled |  arn:aws:s3:::my-prod-bucket-dr    |
|  replicate-to-archive  |  Enabled |  arn:aws:s3:::my-prod-archive     |
|---------------------------------------------------------------------------|

[
    [
        "expire-old-logs",
        "Enabled",
        {
            "Days": 90
        }
    ],
    [
        "archive-after-30d",
        "Enabled",
        {
            "Days": 30
        }
    ]
]
```

!!! warning "Common errors"
    **`An error occurred (NoSuchBucket) when calling the GetBucketVersioning operation: The specified bucket does not exist`** — Verify the bucket name is correct and exists in your current AWS region using `aws s3 ls`.
    **`An error occurred (ReplicationConfigurationNotFoundError) when calling the GetBucketReplication operation: The replication configuration was not found`** — Replication has not been configured for this bucket; use `aws s3api put-bucket-replication` to set it up if needed.
    **`An error occurred (NoSuchLifecycleConfiguration) when calling the GetBucketLifecycleConfiguration operation: The lifecycle configuration does not exist`** — No lifecycle rules are configured; this is expected if lifecycle management is not in use for this bucket.
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

```text title="Expected output"
---------------------------------------------------------------------------------------------------------
|                                    ListCertificates                                                  |
+---------------------------------------------------------------------------------------------------------+
|  DomainName                          |  CertificateArn                                    |  Status     |
+---------------------------------------------------------------------------------------------------------+
|  api.example.com                     |  arn:aws:acm:eu-west-1:123456789012:certificate/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6  |  ISSUED     |
|  *.internal.example.com              |  arn:aws:acm:eu-west-1:123456789012:certificate/b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7  |  ISSUED     |
|  web.example.com                     |  arn:aws:acm:eu-west-1:123456789012:certificate/c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8  |  PENDING_VALIDATION  |
|  mail.example.com                    |  arn:aws:acm:eu-west-1:123456789012:certificate/d4e5f6g7-h8i9-40j0-k1l2-m3n4o5p6q7r8  |  ISSUED     |
+---------------------------------------------------------------------------------------------------------+

[
    "api.example.com",
    "2026-03-15T23:59:59+00:00",
    "ISSUED",
    null
]
```

!!! warning "Common errors"
    **`An error occurred (ValidationException) when calling the ListCertificates operation: 1 validation error detected: value at 'certificateArn' failed to match pattern`** — Verify the certificate ARN format matches `arn:aws:acm:region:account-id:certificate/id` exactly.
    **`An error occurred (ResourceNotFoundException) when calling the DescribeCertificate operation: Certificate not found`** — Confirm the certificate exists in the specified region by running `aws acm list-certificates --region <region>`.
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

```text title="Expected output"
{
    "Content": "AQpDcmVkZW50aWFsUmVwb3J0VmVyc2lvbjox...",
    "GeneratedTime": "2024-01-15T14:32:18+00:00",
    "ReportFormat": "text/csv"
}
user                    arn                                              mfa_active  access_key_1_active  password_last_used
root_account            arn:aws:iam::123456789012:root                   true        false                2024-01-10T09:22:15+00:00
alice.chen              arn:aws:iam::123456789012:user/alice.chen        true        true                 2024-01-14T16:45:32+00:00
bob.martinez            arn:aws:iam::123456789012:user/bob.martinez      false       true                 2023-12-28T11:18:09+00:00
svc-deploy              arn:aws:iam::123456789012:user/svc-deploy        false       true                 N/A
```

!!! warning "Common errors"
    **`An error occurred (AccessDenied) when calling the GenerateCredentialReport operation: User: arn:aws:iam::123456789012:user/alice is not authorized to perform: iam:GenerateCredentialReport`** — Attach the `IAMReadOnlyAccess` policy or `iam:GenerateCredentialReport` permission to the calling user's IAM role.
    **`base64: invalid input`** — Wait the full 10 seconds before calling `get-credential-report`; the report may not be ready immediately after generation.
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

```text title="Expected output"
42

Title                                          SeverityLabel    ProductName                UpdatedAt
-------------------------------------------------  ---------------  -------------------------  --------------------------
IAM policy allows public access to S3 bucket     CRITICAL         AWS Security Hub           2024-01-15T09:42:18.000Z
Unrestricted SSH access detected                 HIGH             AWS Security Hub           2024-01-15T08:31:05.000Z
RDS database encryption not enabled              HIGH             AWS Security Hub           2024-01-15T07:18:42.000Z
Security group allows inbound from 0.0.0.0/0     CRITICAL         AWS Security Hub           2024-01-15T06:55:33.000Z
CloudTrail logging disabled on trail              HIGH             AWS Security Hub           2024-01-15T05:22:11.000Z
```

!!! warning "Common errors"
    **`An error occurred (InvalidInputException) when calling the GetFindings operation: 1 validation error detected: Value at 'filters' failed a custom validation constraint`** — Verify JSON syntax in the filters parameter; use single quotes around the entire filter object and ensure proper nesting of arrays.
    **`An error occurred (AccessDenied) when calling the GetFindings operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: securityhub:GetFindings`** — Add the `securityhub:GetFindings` permission to the IAM user or role's policy.
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


```text title="Expected output"
=== Thu Jan 16 09:42:15 UTC 2025 ===
--- EC2 Status Checks ---
|  InstanceId   | SystemStatus.Status | InstanceStatus.Status |
|---------------+---------------------+-----------------------|
| i-0a7f2c9e1b4 | ok                  | impaired              |
| i-1d3e5f8a2b9 | impaired            | ok                    |

--- CloudWatch Alarms ---
|         AlarmName          |    MetricName    |           StateReason            |
|----------------------------+------------------+----------------------------------|
| prod-api-cpu-high          | CPUUtilization   | Threshold Crossed: 87.3 > 80.0   |
| rds-connection-pool-alarm  | DatabaseConnections | Threshold Crossed: 245 > 200   |

--- RDS Status ---
|  DBInstanceIdentifier  | DBInstanceStatus |
|------------------------+------------------|
| prod-postgres-primary  | backing-up       |

--- AWS Health Events ---
|  service  | region     | statusCode | startTime              |
|-----------+------------+------------+------------------------|
| EC2       | eu-west-1 | open       | 2025-01-16T08:15:00Z  |
| RDS       | eu-west-1 | open       | 2025-01-16T07:42:00Z  |
```

!!! warning "Common errors"
    **`An error occurred (UnauthorizedOperation) when calling the DescribeInstanceStatus operation: You are not authorized to perform: ec2:DescribeInstanceStatus on resource`** — Ensure the IAM role or user has the `ec2:DescribeInstanceStatus`, `cloudwatch:DescribeAlarms`, `rds:DescribeDBInstances`, and `health:DescribeEvents` permissions attached.
    **`Unable to locate credentials. You can configure credentials by running "aws configure".`** — Set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION` environment variables or run `aws configure` to store credentials in `~/.aws/credentials`.
    **`An error occurred (InvalidParameterValue) when calling the DescribeAlarms operation: Invalid value for parameter StateValue`** — Verify the `--state-value` parameter accepts `ALARM` (not `alarm` or `ALARMED`); check AWS CLI version compatibility with the health API.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Aws — Procedures](../procedures/)
- [Aws — CLI Reference](../cli-reference/)
- [Aws — Common Issues](../../troubleshooting/common-issues/)
