# AWS — Install & Upgrade

> Part of the [Operations](../index.md) section.

```
┌──────────────────────────────────────────────────────────┐
│            AWS Patch Manager — Patching Flow             │
└──────────────────────────────────────────────────────────┘

  ┌──────────────────────┐
  │  Patch Baseline      │  (OS family, severity, auto-approve rules)
  └──────────┬───────────┘
             │ assigned to
             ▼
  ┌──────────────────────┐
  │  Patch Group         │  (tag: Patch Group = prod / staging / dev)
  └──────────┬───────────┘
             │ triggered by
             ▼
  ┌──────────────────────┐
  │  Maintenance Window  │  (schedule: 2nd week, rolling waves)
  └──────────┬───────────┘
             │ runs
             ▼
  ┌──────────────────────┐
  │  AWS-RunPatchBaseline│  (SSM Document — Operation=Install)
  └──────────┬───────────┘
             │ executes on
     ┌───────┴──────────┐
     ▼                  ▼
┌─────────┐       ┌──────────────────┐
│  EC2    │       │  ASG — Instance                        │
│ Targets │       │  Refresh (blue/                        │
│ (SSM)   │       │  green replace)                        │
└────┬────┘       └────────┬─────────┘
     │                     │
     └──────────┬──────────┘
                ▼
  ┌──────────────────────┐
  │  Patch Compliance    │  (describe-instance-patch-states)
  │  Report              │
  └──────────────────────┘
```

---

## EC2 Patching

EC2 instances patched monthly via AWS Systems Manager Patch Manager:

```bash
# View patch compliance status
aws ssm describe-instance-patch-states --instance-ids <i-xxxx>

# Run patching on a specific instance now (ad-hoc)
aws ssm send-command \
    --document-name "AWS-RunPatchBaseline" \
    --instance-ids <i-xxxx> \
    --parameters "Operation=Install" \
    --comment "Manual patch run $(date)"

# List instances with missing patches
aws ssm describe-instance-patches --instance-id <i-xxxx> \
    --filters "Key=State,Values=Missing"
```

Patching schedule:
- Second week of each month (aligned to Patch Tuesday + 1 week)
- Dev → Staging → Production in rolling waves separated by 3 days
- Auto Scaling Groups: replace instances with updated launch template (blue/green via Instance Refresh)

## RDS Version Management

```bash
# Check current RDS engine version
aws rds describe-db-instances --db-instance-identifier <db-id> \
    --query 'DBInstances[*].[DBInstanceIdentifier,EngineVersion,PendingModifiedValues]'

# List available upgrade targets
aws rds describe-db-engine-versions --engine postgres \
    --query "DBEngineVersions[?ValidUpgradeTarget != null].[EngineVersion]" --output text

# Apply minor version upgrade immediately
aws rds modify-db-instance --db-instance-identifier <db-id> \
    --engine-version <new-version> --apply-immediately
```

Major version upgrades require:
1. Test in staging environment first
2. Create final snapshot before upgrade
3. Schedule change record with agreed rollback window
4. Run application validation suite post-upgrade

## AMI Lifecycle

```bash
# Create AMI from running instance
aws ec2 create-image --instance-id <i-xxxx> --name "prod-app-$(date +%Y%m%d)" --no-reboot

# List old AMIs (older than 90 days)
aws ec2 describe-images --owners self --query "Images[?CreationDate<='$(date -d '90 days ago' +%Y-%m-%dT%H:%M:%S)'].[ImageId,Name,CreationDate]"

# Deregister old AMI (after confirming no launch templates reference it)
aws ec2 deregister-image --image-id <ami-xxxx>
aws ec2 delete-snapshot --snapshot-id <snap-xxxx>
```

## Lambda Runtime Deprecation

```bash
# List Lambda functions by runtime
aws lambda list-functions --query 'Functions[*].[FunctionName,Runtime]' --output table | sort

# Update runtime (requires testing)
aws lambda update-function-configuration --function-name <name> --runtime python3.12
```

Check deprecation dates: [AWS Lambda runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html) — review quarterly.

## EKS Upgrade

```bash
# Check current EKS version
aws eks describe-cluster --name <cluster-name> --query 'cluster.version'

# List available upgrade versions
aws eks describe-addon-versions --kubernetes-version 1.30

# Upgrade cluster control plane
aws eks update-cluster-version --name <cluster-name> --kubernetes-version 1.30

# Upgrade node groups after control plane
aws eks update-nodegroup-version --cluster-name <cluster-name> \
    --nodegroup-name <nodegroup-name> --kubernetes-version 1.30
```

EKS support policy: N-2 minor versions. Cluster running unsupported version → no patches or support.

## Account Decommissioning

1. Disable IAM users and access keys in the account
2. Suspend account workloads (stop EC2, scale down ECS)
3. Export data and close active services
4. Move account to Suspended OU in Organizations
5. After 90-day hold: close account via Billing Console
6. Update CMDB; remove from monitoring inventory

## Reserved Instance Management

```bash
# Check RI utilisation
aws ce get-reservation-utilization --time-period Start=2026-01-01,End=2026-01-31

# List expiring RIs
aws ec2 describe-reserved-instances --filters "Name=state,Values=active" \
    --query "ReservedInstances[?End<='$(date -d '+90 days' +%Y-%m-%d)T23:59:59'].[ReservedInstancesId,InstanceType,End]"
```

Alert 90 days before RI expiry — initiate renewal or Savings Plan conversion.
