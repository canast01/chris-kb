---
tags:
  - aws
  - operations
---
# AWS Operations — Install & Upgrade

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


```text title="Expected output"
{
    "InstancePatchStates": [
        {
            "InstanceId": "i-0a7f3c2b9e1d4f5a",
            "PatchGroup": "prod-web-servers",
            "BaselineId": "pb-0123456789abcdef0",
            "OperationStartTime": "2024-01-15T09:30:00Z",
            "OperationEndTime": "2024-01-15T10:15:00Z",
            "LastNoRebootInstallOperationTime": "2024-01-15T10:15:00Z",
            "RebootOption": "RebootIfNeeded",
            "InstalledCount": 12,
            "InstalledPendingRebootCount": 3,
            "InstalledOtherCount": 0,
            "MissingCount": 2,
            "FailedCount": 0,
            "UnreachableCount": 0,
            "NotApplicableCount": 45,
            "ComplianceStatus": "NON_COMPLIANT"
        }
    ]
}

{
    "Command": {
        "CommandId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "DocumentName": "AWS-RunPatchBaseline",
        "DocumentVersion": "$DEFAULT",
        "Comment": "Manual patch run Mon Jan 15 14:22:33 UTC 2024",
        "ExpiresAfter": "2024-01-22T14:22:33.000Z",
        "Parameters": {
            "Operation": [
                "Install"
            ]
        },
        "InstanceIds": [
            "i-0a7f3c2b9e1d4f5a"
        ],
        "Targets": [],
        "RequestedDateTime": "2024-01-15T14:22:33.000Z",
        "Status": "InProgress",
        "StatusDetails": "Command execution in progress on 1 instance.",
        "OutputS3BucketName": "",
        "OutputS3KeyPrefix": "",
        "MaxConcurrency": "50",
        "MaxErrors": "0",
        "TargetCount": 1,
        "CompletedCount": 0,
        "ErrorCount": 0,
        "DeliveryTimedOutCount": 0,
        "ServiceRole": "arn:aws:iam::123456789012:role/aws-ssm-service-role",
        "NotificationConfig": {},
        "CloudWatchOutputConfig": {},
        "TimeoutSeconds": 3600
    }
}

{
    "Patches": [
        {
            "Title": "kernel-5.10.205-195.807.amzn2.x86_64",
            "KBId": "ALAS2-2024-2345",
            "Classification": "Security",
            "Severity": "Critical",
            "State": "Missing",
            "PublishedDate": "2024-01-10T00:00:00Z",
            "ContentUrl": "https://alas.aws.amazon.com/AL2/ALAS2-2024-2345.html
```
```bash
# List Lambda functions by runtime
aws lambda list-functions --query 'Functions[*].[FunctionName,Runtime]' --output table | sort

# Update runtime (requires testing)
aws lambda update-function-configuration --function-name <name> --runtime python3.12
```

```text title="Expected output"
FunctionName                          Runtime
------------------------------------  ---------------
data-processor-v2                     python3.11
email-notifier                        python3.9
legacy-batch-job                      python2.7
metrics-aggregator                    nodejs18.x
webhook-handler                       python3.12

FunctionName: webhook-handler
FunctionArn: arn:aws:lambda:us-east-1:123456789012:function:webhook-handler
Runtime: python3.12
LastModified: 2024-01-15T14:32:18.000+0000
CodeSha256: abcd1234efgh5678ijkl9012mnop3456qrst7890uv
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the ListFunctions operation: The resource you requested does not exist.` | Verify your AWS credentials and region are configured correctly with `aws configure`. |
    | `An error occurred (InvalidParameterValueException) when calling the UpdateFunctionConfiguration operation: The runtime parameter of python3.12 is not supported.` | Check the Lambda runtime is available in your region using `aws lambda list-runtimes` and ensure the function's architecture supports it. |
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

```text title="Expected output"
"1.29"
{
    "addons": [
        {
            "addonName": "vpc-cni",
            "addonVersions": [
                {
                    "addonVersion": "v1.16.0-eksbuild.1",
                    "created": "2024-01-15T10:22:33.000000+00:00",
                    "modified": "2024-01-15T10:22:33.000000+00:00",
                    "health": {
                        "issues": []
                    }
                }
            ]
        },
        {
            "addonName": "coredns",
            "addonVersions": [
                {
                    "addonVersion": "v1.10.1-eksbuild.2",
                    "created": "2024-01-10T08:15:12.000000+00:00"
                }
            ]
        }
    ]
}
{
    "update": {
        "id": "8a1b2c3d-4e5f-6g7h-8i9j-0k1l2m3n4o5p",
        "status": "InProgress",
        "type": "VersionUpdate",
        "params": [
            {
                "key": "version",
                "value": "1.30"
            }
        ],
        "createdAt": "2024-01-20T14:32:18.123456+00:00",
        "errors": []
    }
}
{
    "update": {
        "id": "9b2c3d4e-5f6g-7h8i-9j0k-1l2m3n4o5p6q",
        "status": "InProgress",
        "type": "VersionUpdate",
        "params": [
            {
                "key": "version",
                "value": "1.30"
            }
        ],
        "createdAt": "2024-01-20T14:35:42.654321+00:00",
        "errors": []
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceNotFoundException) when calling the DescribeCluster operation: No cluster found for name: <cluster-name>` | Replace `<cluster-name>` with your actual EKS cluster name and verify the cluster exists in the current AWS region. |
    | `An error occurred (InvalidParameterException) when calling the UpdateClusterVersion operation: Cluster version 1.30 is not available for upgrade from version 1.29` | Check available versions with `aws eks describe-addon-versions` and ensure you're upgrading to a version newer than your current version. |
    | `An error occurred (InvalidParameterException) when calling the UpdateNodegroupVersion operation: NodeGroup <nodegroup-name> not found` | Verify the nodegroup name matches exactly and exists in the cluster using `aws eks list-nodegroups --cluster-name <cluster-name>`. |
```bash
# Check RI utilisation
aws ce get-reservation-utilization --time-period Start=2026-01-01,End=2026-01-31

# List expiring RIs
aws ec2 describe-reserved-instances --filters "Name=state,Values=active" \
    --query "ReservedInstances[?End<='$(date -d '+90 days' +%Y-%m-%d)T23:59:59'].[ReservedInstancesId,InstanceType,End]"
```

```d2
direction: right

plan: "Plan" {shape: oval}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> verify
verify -> validate
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Aws — Deploy](../../deploy/)
