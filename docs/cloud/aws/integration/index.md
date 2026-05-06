# AWS Integration

On-premises connectivity to AWS is provided via AWS Direct Connect for dedicated private links or Site-to-Site VPN as a backup path, with BGP route propagation into Transit Gateway for hub-and-spoke routing. Active Directory integration is delivered either through AWS Managed Microsoft AD for a fully managed domain in AWS or AD Connector to proxy authentication to an on-premises domain without replicating the directory. CI/CD pipelines in GitHub Actions use OIDC federation to assume IAM roles without long-lived access keys, and AWS Backup integrates with centralised backup policies defined in AWS Organizations.

| Integration | Method | Notes |
|---|---|---|
| On-premises network | Direct Connect (primary) + VPN (failover) | BGP into Transit Gateway |
| Active Directory | AWS Managed Microsoft AD or AD Connector | Managed AD for new deployments; Connector for proxy-only |
| Monitoring | CloudWatch → Datadog / Splunk via Kinesis Firehose | Use CloudWatch metric streams for low-latency forwarding |
| Backup | AWS Backup with cross-account / cross-region vaults | Policies enforced via AWS Organizations |
| CI/CD | GitHub Actions + OIDC → IAM Role assumption | No static access keys; roles scoped per repo and branch |
| Terraform | Remote state in S3 + DynamoDB lock table | One state bucket per environment, versioning enabled |
