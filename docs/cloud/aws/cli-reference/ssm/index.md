---
tags:
  - aws
---
# Systems Manager (SSM)


<div class="kb-summary">
Systems Manager (SSM) reference covering Run Command, Parameter Store, Maintenance Windows, Patch Management, Inventory and 2 more sections.
</div>

```text
┌──────────────────────────────────────────── AWS CLI — SSM ────────────────────────────────────────────┐
│                                                                                                       │
│  Systems Manager CLI for session manager, run command, parameter store, and patching.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Session Manager                │  │                 Run Command                 │   │
│   │         start-session: shell access          │  │         send-command: execute script        │   │
│   │         terminate-session: end shell         │  │            list-commands: history           │   │
│   │            list-sessions: active             │  │            get-command-invocation           │   │
│   │              No SSH/RDP needed               │  │        describe-instance-information        │   │
│   │             Logs: CloudWatch/S3              │  │           list-command-invocations          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Session Manager replaces SSH bastion; run-command executes scripts fleet-wide                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Parameter Store                │  │                Patch Manager                │   │
│   │         put-parameter: store secret          │  │           describe-patch-baselines          │   │
│   │           get-parameter: retrieve            │  │         get-patch-baseline: details         │   │
│   │            get-parameters-by-path            │  │        describe-instance-patch-states       │   │
│   │           delete-parameter: remove           │  │          describe-patch-group-state         │   │
│   │         SecureString: KMS-encrypted          │  │      register-patch-baseline-for-group      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SSM Agent (on EC2) · SSM endpoints (VPC) · KMS · CloudWatch · S3 (session logs)                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Session Manager = Secure shell access via SSM without SSH port or key pair                           │
│  Run Command     = Execute scripts or documents on managed instances fleet-wide                       │
│  SSM Agent       = Lightweight agent installed on EC2; connects to SSM service                        │
│  Parameter Store = Hierarchical key-value store for config and secrets                                │
│  SecureString    = Parameter type encrypted with KMS key; for passwords/tokens                        │
│  get-parameters-by-path= Retrieves all parameters under a /path/ prefix                               │
│  Patch baseline  = Defines which patches are approved for auto-install                                │
│  Patch group     = Tag-based instance group assigned to a patch baseline                              │
│  describe-instance-patch-states= Shows patch compliance per instance                                  │
│  SSM document    = JSON/YAML runbook defining steps for Run Command                                   │
│  VPC endpoint    = Private SSM connectivity; no internet required for agent                           │
│  Managed instance= EC2 or on-prem server with SSM agent registered to account                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Parameter Store

```bash
# Read a parameter (decrypt SecureString)
aws ssm get-parameter --name /my/param --with-decryption

# Write a parameter
aws ssm put-parameter --name /my/param --value "value" --type SecureString

# Read all parameters under a path hierarchy
aws ssm get-parameters-by-path --path /my/
```

## Maintenance Windows

```bash
# List maintenance windows
aws ssm describe-maintenance-windows

# Create a maintenance window (runs Sundays 03:00 UTC, 2-hour cutoff, 4-hour duration)
aws ssm create-maintenance-window \
  --name "sunday-patching" \
  --schedule "cron(0 3 ? * SUN *)" \
  --duration 4 \
  --cutoff 2 \
  --allow-unassociated-targets

# Register a Run Command task against a window
aws ssm register-task-with-maintenance-window \
  --window-id <window_id> \
  --task-arn "AWS-RunShellScript" \
  --task-type RUN_COMMAND \
  --targets Key=InstanceIds,Values=<instance_id> \
  --service-role-arn arn:aws:iam::<account_id>:role/<MaintenanceWindowRole> \
  --max-concurrency 2 \
  --max-errors 1

# List tasks registered to a window
aws ssm describe-maintenance-window-tasks --window-id <window_id>
```

## Patch Management

```bash
# List available patch baselines
aws ssm describe-patch-baselines

# Describe a specific baseline
aws ssm get-patch-baseline --baseline-id <baseline_id>

# Scan instances for patch compliance (Scan only, no install)
aws ssm send-command \
  --instance-ids <id> \
  --document-name "AWS-RunPatchBaseline" \
  --parameters Operation=Scan

# Install patches on instances
aws ssm send-command \
  --instance-ids <id> \
  --document-name "AWS-RunPatchBaseline" \
  --parameters Operation=Install

# View patch compliance summary for an instance
aws ssm describe-instance-patch-states --instance-ids <id>
```

## Inventory

```bash
# List inventory entries for a specific type on an instance
aws ssm list-inventory-entries \
  --instance-id <instance_id> \
  --type-name AWS:Application

# Query inventory across all managed instances
aws ssm get-inventory \
  --filters Key=AWS:InstanceInformation.PlatformType,Values=Linux,Type=Equal

# List all inventory types collected
aws ssm get-inventory-schema
```

## OpsItems

```bash
# Create an OpsItem (e.g. from a CloudWatch alarm trigger)
aws ssm create-ops-item \
  --title "High CPU on prod-web-01" \
  --description "CPU exceeded 90% for 10 minutes" \
  --source "custom" \
  --severity "2" \
  --priority 2 \
  --operational-data '{"alarm":{"Value":"CPUUtilization","Type":"SearchableString"}}'

# Get details of an OpsItem
aws ssm get-ops-item --ops-item-id <ops_item_id>

# List open OpsItems
aws ssm describe-ops-items \
  --ops-item-filters Key=Status,Values=Open,Operator=Equal
```

## Automation Documents

```bash
# List available Automation runbooks
aws ssm list-documents \
  --document-filter-list key=DocumentType,value=Automation

# Start an automation execution
aws ssm start-automation-execution \
  --document-name "AWS-RestartEC2Instance" \
  --parameters InstanceId=<instance_id>

# List running or completed executions
aws ssm describe-automation-executions \
  --filters Key=DocumentNamePrefix,Values=AWS-RestartEC2Instance

# Get execution detail and step status
aws ssm get-automation-execution \
  --automation-execution-id <execution_id>

# Stop a running automation
aws ssm stop-automation-execution \
  --automation-execution-id <execution_id>
```
