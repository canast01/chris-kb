# AWS Architecture

AWS account structure is built on AWS Organizations with a management account at the root, Service Control Policies (SCPs) enforcing guardrails, and member accounts segregated by environment (dev, staging, production). Core services include VPC for network isolation, EC2 for compute workloads, S3 for object storage, RDS for managed relational databases, and IAM for identity and access management. High availability is achieved through Multi-AZ deployments within a region, while disaster recovery leverages multi-region replication and failover patterns.

- **Management account**: root of the Organization, hosts SCPs and consolidated billing only — no workloads
- **Member accounts**: one per environment (dev, staging, prod) plus shared-services and log-archive accounts
- **Networking**: hub-and-spoke via Transit Gateway; each VPC has public, private, and isolated subnet tiers
- **HA pattern**: Multi-AZ for all stateful services (RDS, ElastiCache, EFS); ALB across AZs for compute
- **DR pattern**: S3 cross-region replication, RDS automated backups to secondary region, Route 53 health-check failover
