# AWS Standards

All AWS resources must carry four mandatory tags — Environment, Owner, CostCentre, and Application — enforced via AWS Config rules and SCPs that deny resource creation on non-compliant requests. Resource naming follows the pattern `env-region-service-name` (e.g., `prod-euw1-rds-orders`), and default VPCs are deleted from every new account at provisioning time. CloudTrail must be enabled in all regions with logs centralised to the log-archive account, and every S3 bucket must have a deny-public-access bucket policy applied as a baseline.

| Standard | Requirement |
|---|---|
| Tagging | Environment, Owner, CostCentre, Application on all resources |
| Naming | `env-region-service-name` lowercase, hyphens only |
| Default VPC | Deleted from all regions on account creation |
| CloudTrail | All-regions trail, logs to centralised log-archive S3 bucket |
| S3 baseline | Block Public Access enabled; server-side encryption (SSE-S3 minimum) |
| AWS Config | Required rules: required-tags, restricted-ssh, s3-bucket-public-read-prohibited, root-mfa-enabled |
