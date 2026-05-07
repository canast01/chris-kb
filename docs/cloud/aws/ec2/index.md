# AWS EC2

## Overview

AWS EC2 provides virtual machine compute capacity in AWS. It supports application hosting, batch processing, automation workers, jump hosts, and infrastructure services.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review instance status checks |  |  |
| Check CPU, memory, and disk trends |  |  |
| Validate backups and AMIs |  |  |
| Review security groups |  |  |
| Confirm patch compliance |  |  |

## Health Commands

```bash
aws ec2 describe-instances
aws ec2 describe-instance-status
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization
aws ssm describe-instance-information
```

## Upgrade Workflow

1. Create AMI or snapshot
2. Confirm application owner approval
3. Patch through SSM or maintenance process
4. Reboot if required
5. Validate instance and application health
