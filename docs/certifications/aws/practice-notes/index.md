# AWS Practice Notes


<div class="kb-summary">
AWS Practice Notes reference covering Service Comparison Tables, Common Gotchas, Architecture Patterns, IAM Quick Reference, Study Checklist.
</div>
```
┌────────────────────────────────── Certifications Aws Practice Notes ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Aws: Certifications Aws Practice Notes platform                        │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                Management: Certifications Aws Practice Notes management console               │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Certifications Aws Practice Notes infrastructure · management network · monitoring       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Aws                = Certifications Aws Practice Notes platform overview and core concepts         │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Service Comparison Tables

### Compute

| Service | Use Case | Key Differentiator |
|---|---|---|
| EC2 | Full VM control, lift-and-shift | Choose instance type, AMI, OS |
| Lambda | Event-driven, short-duration functions | No server management; 15-min max |
| ECS (Fargate) | Container workloads, serverless containers | No EC2 nodes to manage |
| EKS | Kubernetes workloads | Managed control plane; you manage worker nodes or use Fargate |
| Elastic Beanstalk | PaaS for web apps | Managed platform; less control than EC2 |

### Storage

| Service | Type | Use Case |
|---|---|---|
| S3 | Object | Unstructured data, backups, static assets |
| EBS | Block | EC2 boot volumes, databases |
| EFS | File (NFS) | Shared file system across multiple EC2 instances |
| FSx for Windows | File (SMB) | Windows workloads requiring NTFS/AD integration |
| FSx for Lustre | HPC File | High-throughput parallel processing |

### Database

| Service | Engine | Best For |
|---|---|---|
| RDS | MySQL, PostgreSQL, Oracle, MSSQL, MariaDB | Managed relational, OLTP |
| Aurora | MySQL/PostgreSQL-compatible | High performance, global databases |
| DynamoDB | NoSQL (key-value + document) | Low-latency at any scale |
| ElastiCache | Redis / Memcached | Caching, session store |
| Redshift | Column-store SQL | Data warehouse, OLAP |
| Neptune | Graph | Social networks, fraud detection |

## Common Gotchas

- **S3 bucket policy vs ACL**: Bucket policies are the recommended approach; ACLs are legacy and disabled by default on new buckets
- **Security Group vs NACL**: SGs are stateful (return traffic automatic); NACLs are stateless (explicit allow both directions required)
- **ALB vs NLB vs CLB**: ALB = Layer 7 (HTTP/HTTPS, path-based routing); NLB = Layer 4 (TCP/UDP, ultra-low latency, static IP); CLB = legacy
- **SQS vs SNS**: SQS is a pull-based queue (consumers poll); SNS is push-based pub/sub (fan-out to subscribers)
- **CloudWatch vs CloudTrail**: CloudWatch = metrics, logs, alarms; CloudTrail = API call audit log

## Architecture Patterns

| Pattern | Services Involved | Exam Trigger Words |
|---|---|---|
| Serverless web app | API Gateway + Lambda + DynamoDB + S3 | "No server management", "scale to zero" |
| Highly available web tier | ALB + Auto Scaling Group + Multi-AZ RDS | "Fault tolerant", "AZ failure" |
| Event-driven processing | S3 → SQS/SNS → Lambda | "Decoupled", "async processing" |
| Static content delivery | S3 + CloudFront + Route 53 | "Global", "low latency", "cache" |
| Hybrid connectivity | Direct Connect + VPN backup | "Consistent bandwidth", "on-premises" |

## IAM Quick Reference

- **Policy types**: Identity-based, Resource-based, SCP (org-level), Permission boundary
- **Evaluation order**: Explicit Deny → SCP → Permission boundary → Identity policy → Resource policy
- **Roles vs Users**: Roles for applications/services and cross-account; Users for humans (prefer SSO)
- **Least privilege**: Start with no permissions; grant minimum required

## Study Checklist

- [ ] Memorize compute service decision tree (EC2 / Lambda / ECS / EKS)
- [ ] Know S3 storage class use cases and transition rules
- [ ] Understand Security Group vs NACL statefulness
- [ ] Practice 5 IAM policy evaluation scenarios
- [ ] Review ALB vs NLB differences for exam scenarios
- [ ] Know RDS Multi-AZ vs Read Replica purposes
- [ ] Practice 3 architecture design questions with cost optimization constraint
