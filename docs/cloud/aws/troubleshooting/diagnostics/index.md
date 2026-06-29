---
tags:
  - aws
  - troubleshooting
search:
  boost: 1.5
---
# AWS — Diagnostics

<div class="kb-summary">
AWS diagnostic commands: confirm account and role identity with aws sts, query CloudTrail for recent API changes, use VPC Reachability Analyzer and Flow Logs to trace connectivity, simulate IAM policy decisions, check RDS and Lambda CloudWatch metrics, inspect EKS node and pod state, and detect CloudFormation stack drift.

*Applies to: AWS CLI v2 · all regions*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "CloudTrail lookup-events --lookup-attributes\nFilter by resource type or time window" {shape: rectangle}
D: "VPC Reachability Analyzer\nCheck SG rules and NACL for REJECT" {shape: rectangle}
E: "aws iam simulate-principal-policy\nFind which policy statement denies the action" {shape: rectangle}
F: "aws ec2 describe-instance-status\nCheck system and instance status checks" {shape: rectangle}
G: "CloudWatch metrics: CPUUtilization / DBConnections\nCheck enhanced monitoring and slow query log" {shape: rectangle}
H: "aws logs filter-log-events /aws/lambda/function\nCheck throttling CloudWatch metric" {shape: rectangle}
I: "kubectl get nodes -o wide\nkubectl get pods -A --field-selector=status.phase!=Running" {shape: rectangle}
J: "aws cloudformation describe-stack-events\nRead ResourceStatusReason column" {shape: rectangle}
K: "aws cloudtrail lookup-events --max-results 50\nFilter for ErrorCode or specific resource" {shape: rectangle}
L: "L" {shape: rectangle}
M: "Identify SG rule or NACL blocking port\nCheck SG for source IP / CIDR" {shape: rectangle}
N: "Check route table: aws ec2 describe-route-tables\nCheck internet gateway and NAT gateway" {shape: rectangle}
O: "simulate-principal-policy output: implicitDeny or explicitDeny\nImplicit = no allow; Explicit = Deny statement present" {shape: rectangle}
P: "aws ec2 get-console-output to read serial console\nConnect via SSM Session Manager if SSH fails" {shape: rectangle}
Q: "Enable Performance Insights\nCheck slow query log /aws/rds/instance/id/slowquery" {shape: rectangle}
R: "Check ReservedConcurrentExecutions limit\nReview function timeout vs actual execution time" {shape: rectangle}
S: "kubectl describe node node-name\naws eks describe-nodegroup for health.issues" {shape: rectangle}
T: "Review ROLLBACK events\nFix the specific resource that caused ROLLBACK_IN_PROGRESS" {shape: rectangle}
U: "Collect diagnostics for AWS Support\naws support create-case" {shape: rectangle}
A: "AWS Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
B -> I
B -> J
C -> K
L -> M
L -> N
E -> O
F -> P
G -> Q
H -> R
I -> S
J -> T
K -> U
M -> U
N -> U
O -> U
P -> U
Q -> U
R -> U
S -> U
T -> U
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_confirm_identity_and_recent_c: "Step 1 — Confirm identity and recent changes" {shape: rectangle}
step_2_diagnose_vpc_connectivity_wit: "Step 2 — Diagnose VPC connectivity with Flow Logs and Reacha" {shape: rectangle}
step_3_diagnose_iam_access_denied_er: "Step 3 — Diagnose IAM access denied errors" {shape: rectangle}
step_4_diagnose_ec2_instance_health: "Step 4 — Diagnose EC2 instance health" {shape: rectangle}
step_5_diagnose_rds_performance_and_: "Step 5 — Diagnose RDS performance and connectivity" {shape: rectangle}
step_6_diagnose_lambda_and_eks_failu: "Step 6 — Diagnose Lambda and EKS failures" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_confirm_identity_and_recent_c: investigate
symptom -> step_2_diagnose_vpc_connectivity_wit: investigate
symptom -> step_3_diagnose_iam_access_denied_er: investigate
symptom -> step_4_diagnose_ec2_instance_health: investigate
symptom -> step_5_diagnose_rds_performance_and_: investigate
symptom -> step_6_diagnose_lambda_and_eks_failu: investigate
step_1_confirm_identity_and_recent_c -> resolution
step_2_diagnose_vpc_connectivity_wit -> resolution
step_3_diagnose_iam_access_denied_er -> resolution
step_4_diagnose_ec2_instance_health -> resolution
step_5_diagnose_rds_performance_and_ -> resolution
step_6_diagnose_lambda_and_eks_failu -> resolution
```

## Before you begin

- **Access:** AWS CLI configured with the correct profile and region; confirm with `aws sts get-caller-identity`; IAM permissions to read CloudTrail, CloudWatch Logs, and VPC Reachability
- **Gather first:** the specific error message (from the console, API response, or application log), the affected resource ARN or name, the AWS account and region, and the time the issue started
- **Scope:** confirm whether the issue affects one resource, one service, one VPC, or multiple accounts (AWS Organizations)

---

## Step 1 — Confirm identity and recent changes

```bash
# Confirm you are in the correct account and role
aws sts get-caller-identity
# Returns: UserId, Account, Arn — verify against expected account number and role

# Check active CLI profile
aws configure list

# Search CloudTrail for recent management events (last 1 hour)
aws cloudtrail lookup-events \
  --max-results 50 \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteSecurityGroup \
  --query 'Events[*].[EventTime,Username,EventName,Resources[0].ResourceName]' \
  --output table

# Find events by resource ARN (e.g., who modified a specific S3 bucket)
aws cloudtrail lookup-events \
  --max-results 50 \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=my-bucket \
  --query 'Events[*].[EventTime,Username,EventName,ErrorCode]' \
  --output table
# Look for: ErrorCode = AccessDenied or DeleteBucket events

# Last 1 hour of all error events in this region
aws cloudtrail lookup-events \
  --max-results 100 \
  --start-time $(date -u -d "1 hour ago" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || \
                date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --query 'Events[?ErrorCode!=null].[EventTime,Username,EventName,ErrorCode]' \
  --output table
```


```text title="Expected output"
{
    "UserId": "AIDAI45Q7LQVEXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/admin-user"
}

     Name                    Value             Type    Location
     ----                    -----             ----    --------
  profile                <not set>             None    None
  access_key     ****************ABCD      config-file    ~/.aws/config
  secret_key     ****************XyZ1      config-file    ~/.aws/config
     region              us-east-1      config-file    ~/.aws/config

-----------  ----------------  ---------------------  ------------------
EventTime    Username          EventName              ResourceName
-----------  ----------------  ---------------------  ------------------
2024-01-15T14:32:18Z  arn:aws:iam::123456789012:user/ops-team  DeleteSecurityGroup  sg-0a1b2c3d4e5f6g7h8
2024-01-15T13:47:05Z  arn:aws:iam::123456789012:user/dev-user  DeleteSecurityGroup  sg-0x9y8z7w6v5u4t3s2
-----------  ----------------  ---------------------  ------------------

-----------  ----------------  ---------------  -----------
EventTime    Username          EventName        ErrorCode
-----------  ----------------  ---------------  -----------
2024-01-15T14:18:22Z  arn:aws:iam::123456789012:user/jenkins  PutObject         None
2024-01-15T13:55:10Z  arn:aws:iam::123456789012:user/app-svc  GetObject         AccessDenied
-----------  ----------------  ---------------  -----------

-----------  ----------------  ---------------  -----------
EventTime    Username          EventName        ErrorCode
-----------  ----------------  ---------------  -----------
2024-01-15T14:22:33Z  arn:aws:iam::123456789012:user/admin-user  CreateDBInstance  None
2024-01-15T13:18:47Z  arn:aws:iam::123456789012:user/lambda-exec  AssumeRole       AccessDenied
2024-01-15T12:55:12Z  arn:aws:iam::123456789012:user/ci-deploy   ModifySecurityGroupRules  UnauthorizedOperation
-----------  ----------------  ---------------  -----------
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValueException) when calling the LookupEvents operation: Invalid start time`** — Use the correct date format `YYYY-MM-DDTHH:MM:SSZ` and ensure the start time is not older than 90 days.
    **`An error occurred (CloudTrailNotEnabledException) when calling the LookupEvents operation: CloudTrail is not enabled`** — Enable CloudTrail for your AWS account via the CloudTrail console or use `aws cloudtrail create-trail`.
    **`date: invalid date 'now'`** — Replace `date -d "1 hour ago"` with `date -v-1H` on macOS, or use `date --date="1 hour ago"` on Linux systems
---

## Step 2 — Diagnose VPC connectivity with Flow Logs and Reachability Analyzer

```bash
# Find REJECT entries in VPC Flow Logs (identifies blocked traffic)
aws logs filter-log-events \
  --log-group-name /aws/vpc/flowlogs \
  --filter-pattern '[version, account, eni, source, dest, srcport, destport, protocol, packets, bytes, start, end, action="REJECT", log_status]' \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' --output text
# Each line: source-ip destination-ip dest-port REJECT
# Find the port being rejected; match to SG inbound rule

# VPC Reachability Analyzer — trace path from EC2 to another resource
aws ec2 create-network-insights-path \
  --source i-0abc123def456 \
  --destination sg-0def456abc123 \
  --protocol TCP \
  --destination-port 443 \
  --query 'NetworkInsightsPath.NetworkInsightsPathId' --output text
# Returns: path ID

PATH_ID=nip-0abc123
aws ec2 start-network-insights-analysis \
  --network-insights-path-id $PATH_ID \
  --query 'NetworkInsightsAnalysis.NetworkInsightsAnalysisId' --output text

ANALYSIS_ID=nia-0def456
# Poll until status = succeeded (usually < 60 seconds)
aws ec2 describe-network-insights-analyses \
  --network-insights-analysis-ids $ANALYSIS_ID \
  --query 'NetworkInsightsAnalyses[0].[NetworkPathFound,Explanations]' \
  --output json
# NetworkPathFound: true = path exists; false = path blocked; Explanations shows why
```


```text title="Expected output"
10.45.23.18 10.200.5.44 443 REJECT
10.45.23.19 10.200.5.44 3306 REJECT
10.45.23.21 10.200.5.44 443 REJECT
nip-0a1b2c3d4e5f6g7h8
nia-0f1e2d3c4b5a6978
{
    "NetworkInsightsAnalyses": [
        {
            "NetworkPathFound": false,
            "Explanations": [
                {
                    "ExplanationCode": "SecurityGroupNotFound",
                    "NetworkInterfaceId": "eni-0abc123def456",
                    "SecurityGroupId": "sg-0def456abc123"
                }
            ]
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (ResourceNotFoundException) when calling the FilterLogEvents operation: The specified log group does not exist.`** — Verify the log group name with `aws logs describe-log-groups | grep flowlogs` and update `--log-group-name` to the correct path.
    **`An error occurred (InvalidParameterException) when calling the CreateNetworkInsightsPath operation: Invalid destination. Destination must be an ENI, VPC, or Internet Gateway.`** — Replace the security group ID with a valid destination resource type (e.g., `eni-xxxxx` or `igw-xxxxx`).
    **`An error occurred (InvalidParameterValue.NotFound) when calling the DescribeNetworkInsightsAnalyses operation: The network insights analysis ID 'nia-0f1e2d3c4b5a6978' does not exist.`** — Ensure the `ANALYSIS_ID` variable is set correctly from the previous command output and the analysis hasn't expired (analyses are retained for 35 days).
---

## Step 3 — Diagnose IAM access denied errors

```bash
# Simulate whether a role can perform a specific action
aws iam simulate-principal-policy \
  --policy-source-arn "arn:aws:iam::<account-id>:role/MyRole" \
  --action-names "s3:PutObject" \
  --resource-arns "arn:aws:s3:::my-bucket/key" \
  --query 'EvaluationResults[*].[EvalActionName,EvalDecision,MatchedStatements[*].SourcePolicyId]' \
  --output table
# EvalDecision: allowed = permitted; implicitDeny = no allow found; explicitDeny = Deny statement

# Add context entries for condition-based policies (e.g., region, MFA)
aws iam simulate-principal-policy \
  --policy-source-arn "arn:aws:iam::<account>:role/MyRole" \
  --action-names "s3:PutObject" \
  --resource-arns "arn:aws:s3:::my-bucket/key" \
  --context-entries \
    'ContextKeyName=aws:RequestedRegion,ContextKeyValues=eu-west-1,ContextKeyType=string' \
    'ContextKeyName=aws:MultiFactorAuthPresent,ContextKeyValues=true,ContextKeyType=bool' \
  --query 'EvaluationResults[*].[EvalDecision,MatchedStatements[*].SourcePolicyId]' \
  --output table

# List all policies attached to a role
aws iam list-attached-role-policies --role-name MyRole --output table
aws iam list-role-policies --role-name MyRole   # Inline policies

# View trust policy (which services/accounts can assume this role)
aws iam get-role --role-name MyRole \
  --query 'Role.AssumeRolePolicyDocument' | python3 -m json.tool
```


```text title="Expected output"
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          EvaluationResults                                                            │
├─────────────────────────────┬──────────────┬─────────────────────────────────┤
│ EvalActionName              │ EvalDecision │ MatchedStatements                                        │
├─────────────────────────────┼──────────────┼─────────────────────────────────┤
│ s3:PutObject                │ allowed      │ ['arn:aws:iam::123456789012:...                          │
└─────────────────────────────┴──────────────┴──────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          EvaluationResults                                                            │
├──────────────┬─────────────────────────────────────────────────────────────┤
│ EvalDecision │ MatchedStatements                                                                      │
├──────────────┼─────────────────────────────────────────────────────────────┤
│ implicitDeny │ []                                                                                     │
└──────────────┴────────────────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                      AttachedPolicies                                                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ PolicyName                           │ PolicyArn                                                      │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ S3ReadWritePolicy                    │ arn:aws:iam::123456789012:policy...                            │
│ CloudWatchLogsPolicy                 │ arn:aws:iam::123456789012:policy...                            │
└──────────────────────────────────────┴────────────────────────────────────────────────────────────────┘

RolePolicies:
[
    "MyRoleInlinePolicy"
]

{
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
```

!!! warning "Common errors"
    **`An error occurred (NoSuchEntity) when calling the SimulatePrincipalPolicy operation: The role with name MyRole cannot be found.`** — Verify the role name is correct and exists in the current AWS account using `aws iam list-roles`.
    **`An error occurred (InvalidInput) when calling the SimulatePrincipalPolicy operation: Invalid context key name: aws:RequestedRegion`** — Use valid context key names from AWS documentation (e.g., `aws:username`, `aws:SourceIp`) and ensure ContextKeyType matches the value format.
    **`An error occurred (AccessDenied) when calling the SimulatePrincipalPolicy operation: User: arn:aws:iam::123456789012:user/admin
---

## Step 4 — Diagnose EC2 instance health

```bash
# Check instance status checks (system = AWS infrastructure; instance = OS)
aws ec2 describe-instance-status \
  --instance-ids i-0abc123 \
  --query 'InstanceStatuses[0].[InstanceState.Name,SystemStatus.Status,InstanceStatus.Status]' \
  --output table
# Expected: running, ok, ok
# Problem: impaired = hardware or OS issue; initializing = just started

# Get serial console output (useful if SSH is unavailable)
aws ec2 get-console-output \
  --instance-id i-0abc123 \
  --output text | tail -50

# Connect without SSH via SSM Session Manager (requires SSM agent installed)
aws ssm start-session --target i-0abc123
# Opens interactive shell session in the browser or via CLI

# Check instance metadata from inside the instance
curl -s http://169.254.169.254/latest/meta-data/instance-id
curl -s http://169.254.169.254/latest/meta-data/local-ipv4

# Describe the effective SG rules for an instance
aws ec2 describe-security-groups \
  --group-ids $(aws ec2 describe-instances --instance-ids i-0abc123 \
    --query 'Reservations[0].Instances[0].SecurityGroups[*].GroupId' \
    --output text) \
  --query 'SecurityGroups[*].[GroupName,IpPermissions]' --output json
```


```text title="Expected output"
---------------------------------
|      InstanceStatuses      |
+---------------+-----+-----+
| running       | ok  | ok  |
+---------------+-----+-----+

[ec2-user@ip-10-0-45-123 ~]$ tail -50
...
[    0.245612] Linux version 5.10.205-195.807.amzn2.x86_64 (mockbuild@ip-10-0-1-88) (gcc (GCC) 7.3.1 20180712 (Red Hat 7.3.1-13), GNU ld version 2.29.1-31.amzn2) #1 SMP Fri Jan 10 12:34:56 UTC 2024
[    0.456789] Command line: root=/dev/xvda1 ro console=ttyS0
[    1.234567] systemd[1]: systemd 219 running in system mode
[    2.567890] systemd[1]: Started User Manager for UID 1000.
[    3.891234] cloud-init[2847]: Cloud-init v. 23.4.1 finished at Fri, 10 Jan 2024 12:45:23 +0000. Datasource DataSourceEc2Local. Up 3.21 seconds

Starting session with SSM agent...
sh-4.2$ 

i-0abc123
10.0.45.123

{
  "SecurityGroups": [
    {
      "GroupName": "web-tier-sg",
      "IpPermissions": [
        {
          "IpProtocol": "tcp",
          "FromPort": 22,
          "ToPort": 22,
          "IpRanges": [{"CidrIp": "10.0.0.0/8"}]
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 443,
          "ToPort": 443,
          "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
        }
      ]
    }
  ]
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidInstanceID.NotFound) when calling the DescribeInstanceStatus operation: The instance ID 'i-0abc123' does not exist`** — Verify the instance ID is correct and exists in the current region using `aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId'`.
    **`An error occurred (UnauthorizedOperation) when calling the StartSession operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: ssm:StartSession`** — Add the `AmazonSSMManagedInstanceCore` policy to the IAM role attached to the EC2 instance and ensure the SSM agent is running.
    **`curl: (7) Failed to connect to 169.254.169.254 port 80: Connection timed out`** — Verify the instance has an attached IAM instance profile and that the metadata service is enabled; check with `aws ec2 describe-instances --instance-ids i-0abc123 --query 'Reservations[0].Instances[0].MetadataOptions'`.
---

## Step 5 — Diagnose RDS performance and connectivity

```bash
# Check recent RDS events (failovers, restarts, storage full)
aws rds describe-events \
  --source-identifier prod-mysql \
  --source-type db-instance \
  --duration 60 \
  --query 'Events[*].[Date,Message]' \
  --output table

# CloudWatch metrics: CPU, connections, free storage (last 1 hour)
for METRIC in CPUUtilization DatabaseConnections FreeStorageSpace; do
  echo "--- $METRIC ---"
  aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS \
    --metric-name $METRIC \
    --dimensions Name=DBInstanceIdentifier,Value=prod-mysql \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || \
                  date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
    --period 300 --statistics Average \
    --query 'sort_by(Datapoints, &Timestamp)[-1].Average' --output text
done

# Slow query log (if enabled via parameter group)
aws logs filter-log-events \
  --log-group-name /aws/rds/instance/prod-mysql/slowquery \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' --output text | head -50
```


```text title="Expected output"
2024-01-15 14:32:15+00:00 | DB instance restarted
2024-01-15 13:18:42+00:00 | Failover event initiated
2024-01-15 12:05:09+00:00 | Storage space low (85% utilized)
2024-01-15 11:22:33+00:00 | Backup completed successfully

--- CPUUtilization ---
42.5

--- DatabaseConnections ---
127.0

--- FreeStorageSpace ---
5368709120.0

# User prod_app [15/Jan/2024 14:28:15] Query_time: 12.543 Lock_time: 0.002 Rows_sent: 45000 Rows_examined: 2100000 SELECT * FROM transactions WHERE status='pending' AND created_at > DATE_SUB(NOW(), INTERVAL 7 DAY);
# User prod_app [15/Jan/2024 14:15:22] Query_time: 8.127 Lock_time: 0.001 Rows_sent: 12 Rows_examined: 890000 SELECT COUNT(*) FROM audit_logs WHERE action='DELETE';
# User analytics [15/Jan/2024 13:52:08] Query_time: 5.634 Lock_time: 0.000 Rows_sent: 1 Rows_examined: 450000 SELECT AVG(amount) FROM orders WHERE region='US';
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the DescribeEvents operation: Invalid source identifier`** — Verify the DB instance name matches exactly with `aws rds describe-db-instances --query 'DBInstances[*].DBInstanceIdentifier'`.
    **`An error occurred (ResourceNotFoundException) when calling the FilterLogEvents operation: The specified log group does not exist`** — Enable slow query logging in the RDS parameter group and wait 5–10 minutes for the log group to be created, or check the actual log group name with `aws logs describe-log-groups --log-group-name-prefix /aws/rds`.
    **`date: invalid date 'now'`** — Replace `date -d` with `date -v-1H` on macOS, or use `date -u -d '1 hour ago'` on Linux systems only.
---

## Step 6 — Diagnose Lambda and EKS failures

```bash
# Lambda — recent error events
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "ERROR" \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' --output text

# Lambda — invoke manually and capture response + logs
aws lambda invoke \
  --function-name my-function \
  --payload '{"key":"value"}' \
  --log-type Tail \
  --query 'LogResult' --output text \
  /tmp/lambda-output.json | base64 -d
cat /tmp/lambda-output.json

# Lambda — check throttling (concurrent execution limit hit)
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Throttles \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || \
                date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 --statistics Sum \
  --query 'sort_by(Datapoints, &Timestamp)[-1].Sum' --output text

# EKS — node and pod health
kubectl get nodes -o wide
kubectl describe node <node-name> | grep -A 20 "Conditions:"
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

# EKS — control plane audit logs
aws logs filter-log-events \
  --log-group-name /aws/eks/my-cluster/cluster \
  --log-stream-name-prefix kube-apiserver-audit \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' --output text | python3 -m json.tool | head -100
```


```text title="Expected output"
2024-01-15T10:42:33.521Z	ERROR: Connection timeout after 30s	2024-01-15T10:41:12.089Z	ERROR: Invalid JSON payload	2024-01-15T10:39:45.203Z	ERROR: Permission denied accessing DynamoDB

{
  "StatusCode": 200,
  "FunctionVersion": "$LATEST",
  "ExecutedVersion": "$LATEST"
}
START RequestId: 550e8400-e29b-41d4-a716-446655440000 Version: $LATEST
END RequestId: 550e8400-e29b-41d4-a716-446655440000
REPORT RequestId: 550e8400-e29b-41d4-a716-446655440000 Duration: 245.67 ms Billed Duration: 246 ms Memory Used: 128 MB Init Duration: 523.45 ms

{"key":"value"}

None

NAME                          STATUS   ROLES    AGE   VERSION            INTERNAL-IP     EXTERNAL-IP      OS-IMAGE
ip-10-0-1-45.ec2.internal    Ready    <none>   89d   v1.27.6-eks-...    10.0.1.45       203.0.113.42     Amazon Linux 2
ip-10-0-2-78.ec2.internal    Ready    <none>   45d   v1.27.6-eks-...    10.0.2.78       203.0.113.51     Amazon Linux 2
ip-10-0-3-12.ec2.internal    Ready    <none>   12d   v1.27.6-eks-...    10.0.3.12       203.0.113.63     Amazon Linux 2

Conditions:
  Type                 Status  LastHeartbeatTime         LastTransitionTime        Reason                       Message
  Ready                True    Mon, 15 Jan 2024 10:45:22 +0000   Mon, 15 Jan 2024 10:45:22 +0000   KubeletReady                kubelet is posting ready status
  MemoryPressure       False   Mon, 15 Jan 2024 10:45:22 +0000   Mon, 15 Jan 2024 10:45:22 +0000   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         False   Mon, 15 Jan 2024 10:45:22 +0000   Mon, 15 Jan 2024 10:45:22 +0000   KubeletHasNoDiskPressure    kubelet has no disk pressure
  PIDPressure          False   Mon, 15 Jan 2024 10:45:22 +0000   Mon, 15 Jan 2024 10:45:22 +0000   KubeletHasSufficientPID     kubelet has sufficient PID available

NAMESPACE     NAME                                    READY   STATUS             RESTARTS   AGE
kube-system   coredns-558bd4d5db-7x9kl               0/1     CrashLoopBackOff   12         2h
monitoring    prometheus-operator-6d4f7c8b9f
```
---

## Step 7 — CloudFormation diagnostics and support case

```bash
# Show stack events (most recent first) — find the ROLLBACK trigger
aws cloudformation describe-stack-events \
  --stack-name my-stack \
  --query 'sort_by(StackEvents, &Timestamp)[-20:].[LogicalResourceId,ResourceStatus,ResourceStatusReason,Timestamp]' \
  --output table
# Look for: ROLLBACK_IN_PROGRESS and the ResourceStatusReason in the same block

# Detect drift (resources changed outside CloudFormation)
DRIFT_TOKEN=$(aws cloudformation detect-stack-drift \
  --stack-name my-stack \
  --query 'StackDriftDetectionId' --output text)

aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id $DRIFT_TOKEN \
  --query '[StackDriftStatus,DriftedStackResourceCount]'

aws cloudformation describe-stack-resource-drifts \
  --stack-name my-stack \
  --stack-resource-drift-status-filters MODIFIED DELETED \
  --query 'StackResourceDrifts[*].[LogicalResourceId,ResourceType,StackResourceDriftStatus]' \
  --output table

# Open an AWS Support case (requires Business or Enterprise Support plan)
aws support create-case \
  --subject "VPC connectivity issue - instance unreachable" \
  --service-code "virtual-private-cloud" \
  --severity-code "urgent" \
  --category-code "connectivity" \
  --communication-body "Instance i-0abc123 unreachable since 14:30 UTC. Flow Logs show REJECT on port 443."
```


```text title="Expected output"
|LogicalResourceId|ResourceStatus|ResourceStatusReason|Timestamp|
|-|-|-|-|
|my-stack|CREATE_IN_PROGRESS|User Initiated|2024-01-15T10:22:14.123Z|
|VPCSecurityGroup|CREATE_IN_PROGRESS||2024-01-15T10:22:15.456Z|
|VPCSecurityGroup|CREATE_COMPLETE||2024-01-15T10:22:18.789Z|
|IAMRole|CREATE_IN_PROGRESS||2024-01-15T10:22:19.012Z|
|IAMRole|CREATE_FAILED|User: arn:aws:iam::123456789012:user/admin is not authorized to perform: iam:CreateRole|2024-01-15T10:22:22.345Z|
|my-stack|ROLLBACK_IN_PROGRESS|The following resource(s) failed to create: [IAMRole].|2024-01-15T10:22:23.678Z|
|IAMRole|DELETE_IN_PROGRESS||2024-01-15T10:22:24.901Z|
|VPCSecurityGroup|DELETE_IN_PROGRESS||2024-01-15T10:22:25.234Z|
|VPCSecurityGroup|DELETE_COMPLETE||2024-01-15T10:22:27.567Z|
|my-stack|ROLLBACK_COMPLETE|The following resource(s) failed to create: [IAMRole].|2024-01-15T10:22:28.890Z|

DRIFTED
1

|LogicalResourceId|ResourceType|StackResourceDriftStatus|
|-|-|-|
|WebServerSecurityGroup|AWS::EC2::SecurityGroup|MODIFIED|
|InstanceProfile|AWS::IAM::InstanceProfile|DELETED|

{
    "CaseId": "case-123456789012-1234567890"
}
```

!!! warning "Common errors"
    **`An error occurred (ValidationError) when calling the DescribeStackEvents operation: Stack with id my-stack does not exist`** — Verify the stack name matches exactly and exists in the current AWS region using `aws cloudformation list-stacks --query 'StackSummaries[?StackName==\`my-stack\`]'`.
    **`An error occurred (AccessDenied) when calling the CreateCase operation: User is not authorized to perform: support:CreateCase`** — Ensure your IAM user has the `support:CreateCase` permission and that your AWS account has an active Business or Enterprise Support plan.
    **`An error occurred (ValidationError) when calling the DetectStackDrift operation: Stack [my-stack] does not have a status of CREATE_COMPLETE or UPDATE_COMPLETE`** — Wait for the stack to finish its current operation (CREATE/UPDATE/DELETE) before running drift detection.
---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| CloudTrail | `aws cloudtrail lookup-events` | Who changed what; API errors with ErrorCode |
| VPC Flow Logs | `aws logs filter-log-events /aws/vpc/flowlogs` | REJECT entries = SG or NACL blocking traffic |
| CloudWatch Logs | `aws logs filter-log-events /aws/lambda/name` | Application errors and Lambda cold starts |
| EKS audit | `/aws/eks/cluster-name/cluster` log group | Kubernetes API audit events |
| RDS slow query | `/aws/rds/instance/name/slowquery` log group | Queries exceeding the slow_query_time threshold |
| CloudFormation | `describe-stack-events` | ROLLBACK trigger, resource creation errors |

---

## See also

- [AWS — Common Issues](../common-issues/)
- [AWS — Escalation](../escalation/)

## Verify resolution

- `aws sts get-caller-identity` confirms the correct account and role
- VPC Reachability Analyzer analysis shows `NetworkPathFound: true` for the previously failing path
- `aws iam simulate-principal-policy` returns `allowed` for the previously denied action
- CloudWatch metrics for the affected service (CPU, error rate, latency) return to baseline
- The affected workload (EC2, RDS, Lambda, EKS pod) passes a functional smoke test
