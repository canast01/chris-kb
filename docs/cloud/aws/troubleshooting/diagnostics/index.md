---
tags:
  - aws
  - troubleshooting
---
# AWS Diagnostics — Investigation Toolset

```bash
aws sts get-caller-identity
# Returns: UserId, Account, Arn — confirm you are in the correct account and role

# Check profile in use
aws configure list
```
```text
┌─────────────────────────────── AWS Diagnostics — Investigation Toolset ───────────────────────────────┐
│                                                                                                       │
│  Diagnostic tools and investigation procedures for AWS infrastructure and application issues.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Log Sources                  │  │               Metrics & Traces              │   │
│   │      CloudTrail: who did what and when       │  │         CloudWatch: CPU/mem/disk/net        │   │
│   │        VPC Flow Logs: network traffic        │  │         Enhanced Monitoring: RDS OS         │   │
│   │       CloudWatch Logs: app/system logs       │  │        X-Ray: distributed service map       │   │
│   │      ELB access logs: per-request data       │  │        Performance Insights: RDS SQL        │   │
│   │      S3 server access logs: object ops       │  │        CloudWatch Logs Insights query       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  CloudTrail is the first stop for any "who changed what" investigation.                               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Diagnostic CLI Commands            │  │             Network Diagnostics             │   │
│   │         aws cloudtrail lookup-events         │  │          VPC Reachability Analyzer          │   │
│   │          aws logs filter-log-events          │  │           Network Access Analyzer           │   │
│   │       aws ec2 describe-instance-status       │  │        Flow Logs: find REJECT entries       │   │
│   │      aws iam simulate-principal-policy       │  │        Traceroute via SSM Session Mgr       │   │
│   │           aws support create-case            │  │        ELB access logs: Athena query        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  CloudTrail storage infrastructure · CloudWatch Logs backend · X-Ray sampling plane                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CloudTrail lookup= API returning recent management events for an account and region                  │
│  filter-log-events= CLI command searching CloudWatch Logs for a pattern in a time range               │
│  Reachability Analyzer= VPC tool that traces the network path between two resources                   │
│  Network Access Analyzer= Identifies unintended network access paths to resources                     │
│  simulate-principal-policy= IAM CLI command checking if a principal can perform an action             │
│  X-Ray service map= Visual graph of microservices and latency between them                            │
│  ELB access log  = Per-request record with response time, backend, status, client IP                  │
│  Flow Log REJECT = Indicates SG or NACL denied the packet; starting point for firewall debug          │
│  SSM Session Manager= Browser/CLI shell to instance without SSH; useful for diagnostics               │
│  Athena on logs  = SQL queries over ELB or S3 access logs stored in S3                                │
│  Logs Insights   = CloudWatch Logs query engine; supports time-series and aggregation                 │
│  aws support     = Open AWS support case via CLI with describe-trusted-advisor-checks                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Check VPC Reachability Analyzer (path analysis)
aws ec2 create-network-insights-path \
  --source i-0abc123 \
  --destination sg-0def456 \
  --protocol TCP \
  --destination-port 443 \
  --query 'NetworkInsightsPath.NetworkInsightsPathId' --output text

PATH_ID=<path-id>
aws ec2 start-network-insights-analysis \
  --network-insights-path-id $PATH_ID \
  --query 'NetworkInsightsAnalysis.NetworkInsightsAnalysisId' --output text

ANALYSIS_ID=<analysis-id>
aws ec2 describe-network-insights-analyses \
  --network-insights-analysis-ids $ANALYSIS_ID \
  --query 'NetworkInsightsAnalyses[0].[NetworkPathFound,Explanations]'

# VPC Flow Logs — find dropped traffic
aws logs filter-log-events \
  --log-group-name /aws/vpc/flowlogs \
  --filter-pattern '[version, account, eni, source, dest, srcport, destport, protocol, packets, bytes, start, end, action="REJECT", log_status]' \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' --output text
```
```bash
# Check recent RDS events (errors, failovers)
aws rds describe-events \
  --source-identifier prod-mysql \
  --source-type db-instance \
  --duration 60 \
  --query 'Events[*].[Date,Message]' \
  --output table

# Enhanced Monitoring — check OS metrics (requires enhanced monitoring enabled)
aws rds describe-db-instances \
  --db-instance-identifier prod-mysql \
  --query 'DBInstances[0].[MonitoringInterval,MonitoringRoleArn]'

# CloudWatch — check RDS CPU, connections, free storage
for METRIC in CPUUtilization DatabaseConnections FreeStorageSpace; do
  echo "--- $METRIC ---"
  aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS \
    --metric-name $METRIC \
    --dimensions Name=DBInstanceIdentifier,Value=prod-mysql \
    --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
    --period 300 --statistics Average \
    --query 'sort_by(Datapoints, &Timestamp)[-1].Average' --output text
done

# Check slow query log (if enabled via parameter group)
aws logs filter-log-events \
  --log-group-name /aws/rds/instance/prod-mysql/slowquery \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' --output text | head -50
```
```bash
# List recent invocation errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "ERROR" \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' --output text

# Get last N log streams (invocations)
aws logs describe-log-streams \
  --log-group-name /aws/lambda/my-function \
  --order-by LastEventTime \
  --descending \
  --max-items 5 \
  --query 'logStreams[*].[logStreamName,lastEventTimestamp]' \
  --output table

# Invoke function manually and capture response
aws lambda invoke \
  --function-name my-function \
  --payload '{"key":"value"}' \
  --log-type Tail \
  --query 'LogResult' --output text \
  /tmp/lambda-output.json | base64 -d
cat /tmp/lambda-output.json

# Check function concurrency throttling
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Throttles \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 --statistics Sum \
  --query 'sort_by(Datapoints, &Timestamp)[-1].Sum' --output text
```
```bash
# Cluster control plane logs (requires logging enabled)
aws eks update-cluster-config \
  --name my-cluster \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'

# View API server audit logs
aws logs filter-log-events \
  --log-group-name /aws/eks/my-cluster/cluster \
  --log-stream-name-prefix kube-apiserver-audit \
  --filter-pattern '{$.user.username="system:serviceaccount:*"}' \
  --start-time $(($(date +%s) - 3600))000 \
  --query 'events[*].message' --output text | python3 -m json.tool | head -100

# Describe node group for issues
aws eks describe-nodegroup \
  --cluster-name my-cluster \
  --nodegroup-name workers \
  --query 'nodegroup.[status,health.issues,scalingConfig]'

# Node and pod state (after kubeconfig update)
kubectl get nodes -o wide
kubectl describe node <node-name> | grep -A 20 "Conditions:"
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
```
```bash
# Simulate a specific action to find why it's denied
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<account>:role/MyRole \
  --action-names s3:PutObject \
  --resource-arns "arn:aws:s3:::my-bucket/key" \
  --context-entries 'ContextKeyName=aws:RequestedRegion,ContextKeyValues=eu-west-1,ContextKeyType=string' \
  --query 'EvaluationResults[*].[EvalActionName,EvalDecision,MatchedStatements[*].SourcePolicyId]' \
  --output table

# List all policies attached to a role
aws iam list-attached-role-policies --role-name MyRole --output table
aws iam list-role-policies --role-name MyRole  # Inline policies

# View the trust policy
aws iam get-role --role-name MyRole \
  --query 'Role.AssumeRolePolicyDocument' | python3 -m json.tool
```
```bash
# Show stack events ordered by time (most recent first)
aws cloudformation describe-stack-events \
  --stack-name my-stack \
  --query 'sort_by(StackEvents, &Timestamp)[-20:].[LogicalResourceId,ResourceStatus,ResourceStatusReason,Timestamp]' \
  --output table

# Show stack drift (resources that changed outside CloudFormation)
aws cloudformation detect-stack-drift --stack-name my-stack
DRIFT_ID=$(aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id $DRIFT_ID \
  --query 'StackDriftDetectionId' --output text)

aws cloudformation describe-stack-resource-drifts \
  --stack-name my-stack \
  --stack-resource-drift-status-filters MODIFIED DELETED \
  --query 'StackResourceDrifts[*].[LogicalResourceId,ResourceType,StackResourceDriftStatus]' \
  --output table
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

