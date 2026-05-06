# AWS Lifecycle

EC2 AMIs are patched monthly via Systems Manager Patch Manager using maintenance windows scheduled in the second week of each month; instances are restarted in rolling fashion per Auto Scaling group. RDS minor version upgrades are applied automatically during the defined maintenance window, while major version upgrades require a planned change with a pre-tested snapshot. Lambda runtime deprecation dates are tracked against the AWS Lambda runtime support policy, and deprecated runtimes are remediated before the enforcement date.

| Component | Lifecycle Event | Cadence / Policy |
|---|---|---|
| EC2 AMIs | Patch via SSM Patch Manager | Monthly, second week |
| RDS minor versions | Auto-upgrade enabled | Applied during maintenance window |
| RDS major versions | Manual upgrade with snapshot | Planned change, tested in staging first |
| Lambda runtimes | Deprecation tracking | Reviewed quarterly; remediate before enforcement date |
| EKS clusters | Supported versions (N-2) | Upgrade within 12-month support window |
| AWS accounts | Decommissioning | Disable IAM users → move to suspended OU → close after 90 days |
