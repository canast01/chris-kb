---
tags:
  - aws
---
# Systems Manager (SSM)

<div class="kb-summary">
Systems Manager (SSM) reference covering Run Command, Parameter Store, Maintenance Windows, Patch Management, Inventory and 2 more sections.

*Applies to: AWS*
</div>

```d2
direction: down

parameter_store: "Parameter Store" {shape: rectangle}
maintenance_windows: "Maintenance Windows" {shape: rectangle}
patch_management: "Patch Management" {shape: rectangle}
inventory: "Inventory" {shape: rectangle}
opsitems: "OpsItems" {shape: rectangle}
automation_documents: "Automation Documents" {shape: rectangle}

parameter_store -> maintenance_windows: uses
maintenance_windows -> patch_management: uses
patch_management -> inventory: uses
inventory -> opsitems: uses
opsitems -> automation_documents: uses
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


```text title="Expected output"
{
    "Parameter": {
        "Name": "/my/param",
        "Type": "SecureString",
        "Value": "super-secret-database-password",
        "Version": 3,
        "Selector": null,
        "SourceResult": null,
        "LastModifiedDate": "2024-01-15T14:32:18.456000+00:00",
        "ARN": "arn:aws:ssm:us-east-1:123456789012:parameter/my/param"
    }
}
{
    "Version": 4,
    "Tier": "Standard"
}
{
    "Parameters": [
        {
            "Name": "/my/param",
            "Type": "SecureString",
            "Value": "super-secret-database-password",
            "Version": 3,
            "LastModifiedDate": "2024-01-15T14:32:18.456000+00:00",
            "ARN": "arn:aws:ssm:us-east-1:123456789012:parameter/my/param"
        },
        {
            "Name": "/my/param/db-host",
            "Type": "String",
            "Value": "db.example.com",
            "Version": 1,
            "LastModifiedDate": "2024-01-10T09:15:22.123000+00:00",
            "ARN": "arn:aws:ssm:us-east-1:123456789012:parameter/my/param/db-host"
        }
    ],
    "NextToken": null
}
```

!!! warning "Common errors"
    **`An error occurred (ParameterNotFound) when calling the GetParameter operation: Parameter /my/param not found.`** — Verify the parameter name exists in Parameter Store using `aws ssm describe-parameters --filters "Key=Name,Values=/my/param"`.
    **`An error occurred (AccessDeniedException) when calling the GetParameter operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: ssm:GetParameter on resource: arn:aws:ssm:us-east-1:123456789012:parameter/my/param`** — Add `ssm:GetParameter` and `kms:Decrypt` permissions to the IAM user/role policy.
    **`An error occurred (InvalidParameterType) when calling the PutParameter operation: Invalid parameter type specified.`** — Use a valid type: `String`, `StringList`, or `SecureString`.
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


```text title="Expected output"
{
    "MaintenanceWindowIdentifiers": [
        {
            "WindowId": "mw-0a1b2c3d4e5f6g7h8",
            "Name": "sunday-patching",
            "Enabled": true,
            "Duration": 4,
            "Cutoff": 2,
            "Schedule": "cron(0 3 ? * SUN *)"
        },
        {
            "WindowId": "mw-9i8j7k6l5m4n3o2p1",
            "Name": "monthly-maintenance",
            "Enabled": true,
            "Duration": 3,
            "Cutoff": 1,
            "Schedule": "cron(0 2 ? * MON#1 *)"
        }
    ]
}
{
    "WindowId": "mw-0a1b2c3d4e5f6g7h8"
}
{
    "WindowTaskId": "task-1a2b3c4d5e6f7g8h9"
}
{
    "Tasks": [
        {
            "WindowId": "mw-0a1b2c3d4e5f6g7h8",
            "WindowTaskId": "task-1a2b3c4d5e6f7g8h9",
            "TaskArn": "AWS-RunShellScript",
            "Type": "RUN_COMMAND",
            "Targets": [
                {
                    "Key": "InstanceIds",
                    "Values": ["i-0123456789abcdef0"]
                }
            ],
            "ServiceRoleArn": "arn:aws:iam::123456789012:role/MaintenanceWindowRole",
            "MaxConcurrency": "2",
            "MaxErrors": "1"
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidWindowId) when calling the DescribeMaintenanceWindowTasks operation: The maintenance window ID 'mw-invalid' does not exist.`** — Verify the window ID exists by running `aws ssm describe-maintenance-windows` and copy the correct WindowId value.
    **`An error occurred (InvalidParameterValue) when calling the RegisterTaskWithMaintenanceWindow operation: The service role ARN is invalid.`** — Ensure the IAM role exists and the ARN format is correct: `arn:aws:iam::<account_id>:role/<RoleName>`, and the role has SSM maintenance window trust permissions.
    **`An error occurred (InvalidParameterValue) when calling the CreateMaintenanceWindow operation: The schedule expression is invalid.`** — Verify the cron expression syntax; use `cron(minute hour day month day-of-week year)` format, e.g., `cron(0 3 ? * SUN *)` for 3 AM Sundays.
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


```text title="Expected output"
{
    "PatchBaselines": [
        {
            "BaselineId": "pb-0a1b2c3d4e5f6g7h8",
            "BaselineName": "AWS-DefaultPatchBaseline",
            "OperatingSystemType": "WINDOWS",
            "BaselineDescription": "Default patch baseline for Windows",
            "DefaultBaseline": true
        },
        {
            "BaselineId": "pb-9i8j7k6l5m4n3o2p1",
            "BaselineName": "custom-linux-baseline",
            "OperatingSystemType": "AMAZON_LINUX_2",
            "BaselineDescription": "Custom baseline for AL2 instances",
            "DefaultBaseline": false
        }
    ]
}
{
    "BaselineId": "pb-0a1b2c3d4e5f6g7h8",
    "BaselineName": "AWS-DefaultPatchBaseline",
    "OperatingSystemType": "WINDOWS",
    "ApprovedPatches": ["KB5012345", "KB5012346"],
    "RejectedPatches": [],
    "PatchGroups": ["production-servers", "dev-servers"]
}
{
    "Command": {
        "CommandId": "cmd-0123456789abcdef0",
        "DocumentName": "AWS-RunPatchBaseline",
        "DocumentVersion": "$DEFAULT",
        "Content": "...",
        "TargetCount": 1,
        "CompletedCount": 0,
        "ErrorCount": 0,
        "Status": "Pending",
        "StatusDetails": "Pending",
        "OutputS3BucketName": "",
        "OutputS3KeyPrefix": "",
        "Parameters": {
            "Operation": ["Scan"]
        },
        "InstanceIds": ["i-0a1b2c3d4e5f6g7h8"],
        "CreatedDate": 1699564800.0,
        "ExpiresAfter": 1699651200.0
    }
}
{
    "Command": {
        "CommandId": "cmd-1a2b3c4d5e6f7g8h9",
        "DocumentName": "AWS-RunPatchBaseline",
        "Status": "InProgress",
        "TargetCount": 1,
        "CompletedCount": 0,
        "ErrorCount": 0
    }
}
{
    "InstancePatchStates": [
        {
            "InstanceId": "i-0a1b2c3d4e5f6g7h8",
            "PatchGroup": "production-servers",
            "BaselineId": "pb-0a1b2c3d4e5f6g7h8",
            "OperationStartTime": 1699564800.0,
            "OperationEndTime": 1699565400.0,
            "LastNoRebootInstallOperationTime": 1699565400.0,
            "RebootOption": "RebootIfNeeded",
            "FailedCount": 0,
            "InstalledCount": 3,
            "InstalledOtherCount": 0,
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


```text title="Expected output"
# List inventory entries for a specific type on an instance
{
    "Entries": {
        "aws:application": [
            {
                "Name": "amazon-cloudwatch-agent",
                "Version": "1.247018.0",
                "InstalledTime": "2024-01-15T09:23:44Z"
            },
            {
                "Name": "aws-cli",
                "Version": "2.13.27",
                "InstalledTime": "2024-01-10T14:12:18Z"
            },
            {
                "Name": "ssm-agent",
                "Version": "3.2.1630.0",
                "InstalledTime": "2023-12-20T08:45:22Z"
            }
        ]
    },
    "TypeName": "AWS:Application",
    "InstanceId": "i-0a1b2c3d4e5f6g7h8"
}

# Query inventory across all managed instances
{
    "Entities": [
        {
            "Id": "i-0a1b2c3d4e5f6g7h8",
            "Data": {
                "AWS:InstanceInformation": {
                    "Content": [
                        {
                            "PlatformType": "Linux",
                            "PlatformName": "Ubuntu",
                            "PlatformVersion": "22.04 LTS"
                        }
                    ]
                }
            }
        },
        {
            "Id": "i-0x9y8z7w6v5u4t3s2",
            "Data": {
                "AWS:InstanceInformation": {
                    "Content": [
                        {
                            "PlatformType": "Linux",
                            "PlatformName": "Amazon Linux 2",
                            "PlatformVersion": "5.10.184-175.749.amzn2.x86_64"
                        }
                    ]
                }
            }
        }
    ]
}

# List all inventory types collected
{
    "Schemas": [
        {
            "TypeName": "AWS:Application",
            "Version": "1.0",
            "Attributes": [
                {
                    "Name": "Name",
                    "Type": "String"
                },
                {
                    "Name": "Version",
                    "Type": "String"
                }
            ]
        },
        {
            "TypeName": "AWS:InstanceInformation",
            "Version": "1.0",
            "Attributes": [
                {
                    "Name": "PlatformType",
                    "Type": "String"
                },
                {
                    "Name": "PlatformName",
                    "Type": "String"
                }
            ]
        },
        {
            "TypeName": "AWS:Network",
            "Version": "1.0",
            "Attributes": [
                {
                    "Name": "IpAddress",
                    "Type": "String"
                }
            ]
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidInstanceId) when calling the ListInventoryEntries operation: The instance ID
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


```text title="Expected output"
{
    "OpsItemId": "oi-0a1b2c3d4e5f6g7h8",
    "OpsItemArn": "arn:aws:ssm:us-east-1:123456789012:opsitem/oi-0a1b2c3d4e5f6g7h8"
}
{
    "OpsItem": {
        "CreatedTime": "2024-01-15T14:32:18.456000+00:00",
        "Title": "High CPU on prod-web-01",
        "Description": "CPU exceeded 90% for 10 minutes",
        "Source": "custom",
        "Status": "Open",
        "Priority": 2,
        "Severity": "2",
        "OpsItemId": "oi-0a1b2c3d4e5f6g7h8",
        "LastModifiedTime": "2024-01-15T14:32:18.456000+00:00",
        "OperationalData": {
            "alarm": {
                "Value": "CPUUtilization",
                "Type": "SearchableString"
            }
        }
    }
}
{
    "OpsItemSummaries": [
        {
            "CreatedTime": "2024-01-15T14:32:18.456000+00:00",
            "Title": "High CPU on prod-web-01",
            "OpsItemId": "oi-0a1b2c3d4e5f6g7h8",
            "Status": "Open",
            "Priority": 2,
            "Source": "custom",
            "LastModifiedTime": "2024-01-15T14:32:18.456000+00:00"
        },
        {
            "CreatedTime": "2024-01-14T09:15:42.123000+00:00",
            "Title": "Database replication lag detected",
            "OpsItemId": "oi-1x2y3z4a5b6c7d8e",
            "Status": "Open",
            "Priority": 3,
            "Source": "aws:ec2",
            "LastModifiedTime": "2024-01-14T10:22:05.789000+00:00"
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the CreateOpsItem operation: Invalid severity value. Valid values are: 1, 2, 3, 4`** — Ensure severity is a string between "1" and "4", not an integer.
    **`An error occurred (AccessDenied) when calling the CreateOpsItem operation: User: arn:aws:iam::123456789012:user/ops-user is not authorized to perform: ssm:CreateOpsItem`** — Add the `ssm:CreateOpsItem` permission to the IAM user or role's policy.
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


```text title="Expected output"
{
    "DocumentIdentifiers": [
        {
            "Name": "AWS-RestartEC2Instance",
            "DocumentVersion": "$DEFAULT",
            "DocumentType": "Automation",
            "Owner": "Amazon",
            "PlatformTypes": ["Windows", "Linux"]
        },
        {
            "Name": "AWS-RunPatchBaseline",
            "DocumentVersion": "$DEFAULT",
            "DocumentType": "Automation",
            "Owner": "Amazon",
            "PlatformTypes": ["Windows", "Linux"]
        },
        {
            "Name": "AWS-StopEC2Instance",
            "DocumentVersion": "$DEFAULT",
            "DocumentType": "Automation",
            "Owner": "Amazon",
            "PlatformTypes": ["Windows", "Linux"]
        }
    ]
}
{
    "AutomationExecutionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
{
    "AutomationExecutionMetadataList": [
        {
            "AutomationExecutionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "DocumentName": "AWS-RestartEC2Instance",
            "ExecutionStatus": "Success",
            "ExecutionStartTime": 1699564800.0,
            "ExecutionEndTime": 1699564920.0
        }
    ]
}
{
    "AutomationExecution": {
        "AutomationExecutionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "DocumentName": "AWS-RestartEC2Instance",
        "ExecutionStatus": "Success",
        "StepExecutions": [
            {
                "StepName": "RestartInstances",
                "ExecutionStatus": "Success",
                "ExecutionStartTime": 1699564800.0,
                "ExecutionEndTime": 1699564920.0
            }
        ]
    }
}
{
    "AutomationExecutionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidDocument) when calling the ListDocuments operation: Document name cannot be blank.`** — Ensure the `--document-filter-list` parameter is correctly formatted with both `key=` and `value=` specified.
    **`An error occurred (ValidationException) when calling the StartAutomationExecution operation: 1 validation error detected: Value null at 'parameters.InstanceId' failed to satisfy constraint: Member must not be null`** — Replace `<instance_id>` with an actual EC2 instance ID (e.g., `i-0abcd1234efgh5678`).
    **`An error occurred (AutomationExecutionNotFoundException) when calling the GetAutomationExecution operation: Execution does not exist.`** — Verify the `<execution_id>` is correct and the execution has not been purged (SSM retains execution history for 30 days).
## See also

- [AWS CLI Reference](../index.md)
- [AWS Operations](../../operations/index.md)
- [AWS Compute](../../compute/index.md)
