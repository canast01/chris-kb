# Auto Scaling

AWS Auto Scaling — EC2 Auto Scaling groups, scaling policies, and lifecycle management.

## Key Concepts

| Concept | Description |
|---|---|
| Auto Scaling Group (ASG) | Fleet of EC2 instances with min/max/desired capacity |
| Launch Template | Configuration for new instances (AMI, type, SG, user data) |
| Scaling Policy | Target tracking, step, or scheduled scaling |
| Lifecycle hook | Pause instances during launch/terminate for custom actions |
| Warm pool | Pre-initialised instances ready to scale out faster |

## Common CLI Commands

```bash
# List Auto Scaling groups
aws autoscaling describe-auto-scaling-groups \
  --query 'AutoScalingGroups[*].{Name:AutoScalingGroupName,Min:MinSize,Max:MaxSize,Desired:DesiredCapacity,Instances:length(Instances)}' \
  --output table

# List instances in an ASG
aws autoscaling describe-auto-scaling-instances \
  --query 'AutoScalingInstances[?AutoScalingGroupName==`<asg-name>`].{ID:InstanceId,State:LifecycleState,Health:HealthStatus,AZ:AvailabilityZone}' \
  --output table

# Update desired capacity manually
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name <asg-name> \
  --desired-capacity 5

# Suspend scaling processes (for maintenance)
aws autoscaling suspend-processes \
  --auto-scaling-group-name <asg-name> \
  --scaling-processes Launch Terminate HealthCheck

# Resume after maintenance
aws autoscaling resume-processes \
  --auto-scaling-group-name <asg-name> \
  --scaling-processes Launch Terminate HealthCheck

# Detach an instance (remove without terminating — useful for debugging)
aws autoscaling detach-instances \
  --auto-scaling-group-name <asg-name> \
  --instance-ids <i-id> \
  --should-decrement-desired-capacity

# Terminate an instance and replace it
aws autoscaling terminate-instance-in-auto-scaling-group \
  --instance-id <i-id> \
  --should-decrement-desired-capacity false
```

## Scaling Policies

```bash
# Target tracking — keep CPU at 60%
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name <asg-name> \
  --policy-name cpu-target-tracking \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {"PredefinedMetricType": "ASGAverageCPUUtilization"},
    "TargetValue": 60.0,
    "DisableScaleIn": false
  }'

# Scheduled action — scale up before business hours
aws autoscaling put-scheduled-update-group-action \
  --auto-scaling-group-name <asg-name> \
  --scheduled-action-name morning-scale-up \
  --recurrence "0 7 * * 1-5" \
  --min-size 4 \
  --desired-capacity 6
```

## Instance Refresh (rolling replacement)

```bash
# Replace all instances gradually with new launch template version
aws autoscaling start-instance-refresh \
  --auto-scaling-group-name <asg-name> \
  --preferences '{"MinHealthyPercentage": 90, "InstanceWarmup": 300}'

# Check refresh status
aws autoscaling describe-instance-refreshes \
  --auto-scaling-group-name <asg-name> \
  --query 'InstanceRefreshes[0].{Status:Status,Progress:PercentageComplete,Reason:StatusReason}'
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| ASG not scaling out | Activity history | `describe-scaling-activities` — check for launch errors |
| Instances immediately terminating | Health checks | Confirm LB health check path returns 200 within `HealthCheckGracePeriod` |
| ASG stuck at 0 instances | Launch Template valid? | Check AMI exists; verify security groups and subnet are valid |
| Uneven AZ distribution | Rebalancing suspended? | `resume-processes` for `AZRebalance` |
| Instance refresh stuck | Healthy percentage | Reduce `MinHealthyPercentage` or fix the health check issue first |
