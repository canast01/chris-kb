# AWS — Diagnostics

---

## Identify Current Identity and Account

```bash
aws sts get-caller-identity
# Returns: UserId, Account, Arn — confirm you are in the correct account and role

# Check profile in use
aws configure list
```

---

## CloudTrail — Find Who Did What

```bash
# Look up events for a specific resource or user (last 90 days, management events only)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=my-bucket \
  --start-time $(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ) \
  --query 'Events[*].[EventTime,Username,EventName,Resources[0].ResourceName]' \
  --output table

# Find who deleted a resource
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteBucket \
  --start-time $(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ) \
  --query 'Events[*].[EventTime,Username,CloudTrailEvent]' \
  --output table

# Filter CloudWatch Logs (CloudTrail) for sensitive actions
aws logs filter-log-events \
  --log-group-name CloudTrail \
  --filter-pattern '{$.eventName="DeleteBucket" || $.eventName="TerminateInstances" || $.eventName="DeleteDBInstance"}' \
  --start-time $(($(date +%s) - 86400))000 \
  --query 'events[*].message' --output text | python3 -m json.tool
```

---

## EC2 — Instance Diagnostics

```bash
# Status checks
aws ec2 describe-instance-status --instance-ids i-0abc123 \
  --query 'InstanceStatuses[0].[SystemStatus.Status,InstanceStatus.Status,Events]'

# Console output (boot log — useful when unreachable)
aws ec2 get-console-output --instance-id i-0abc123 --output text

# Console screenshot (GUI instances)
aws ec2 get-console-screenshot --instance-id i-0abc123 \
  --query 'ImageData' --output text | base64 -d > screenshot.jpg

# Connect via SSM Session Manager (no SSH key needed)
aws ssm start-session --target i-0abc123

# Run diagnostic command via SSM
COMMAND_ID=$(aws ssm send-command \
  --instance-ids i-0abc123 \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["df -h","free -h","netstat -tlnp","ps aux --sort=-%cpu | head -20"]' \
  --query 'Command.CommandId' --output text)
sleep 5
aws ssm get-command-invocation \
  --command-id $COMMAND_ID --instance-id i-0abc123 \
  --query 'StandardOutputContent' --output text
```

---

## EC2 — Network Diagnostics

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

---

## RDS — Diagnostics

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

---

## Lambda — Diagnostics

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

---

## EKS — Cluster Diagnostics

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

---

## IAM — Policy Debugging

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

---

## CloudFormation — Stack Diagnostics

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
