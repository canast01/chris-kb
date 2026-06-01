# AWS Services Reference


<div class="kb-summary">
AWS Services Reference reference covering Compute Services, Storage Services, Networking Services, Security Services, Database Services and 1 more sections.
</div>
```
┌───────────────────────────────────── Certifications Aws Services ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           Aws: Certifications Aws Services platform                           │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Certifications Aws Services management console                  │   │
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
│    Physical: Certifications Aws Services infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Aws                = Certifications Aws Services platform overview and core concepts               │
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


## Compute Services

| Service | Category | Key Facts |
|---|---|---|
| EC2 | IaaS VM | Instance families: General (M/T), Compute (C), Memory (R/X), Storage (I/D), GPU (P/G) |
| Lambda | Serverless | Event-driven; max 15 min timeout; 1M free requests/month |
| ECS | Container | Supports EC2 launch type (self-managed nodes) and Fargate (serverless) |
| EKS | Kubernetes | Managed control plane; supports Fargate node groups |
| Elastic Beanstalk | PaaS | Manages EC2, ASG, ELB; deploys code packages |
| Lightsail | Simple VPS | Fixed monthly pricing; for simple apps and dev/test |
| Batch | Batch processing | Runs containerized batch jobs; auto-provisions compute |

## Storage Services

| Service | Type | Durability / SLA | Notes |
|---|---|---|---|
| S3 Standard | Object | 99.999999999% (11 9s) | General purpose; frequent access |
| S3 IA | Object | 11 9s | Lower cost; minimum 30-day charge |
| S3 Glacier Instant | Archive | 11 9s | ms retrieval; 90-day minimum |
| S3 Glacier Flexible | Archive | 11 9s | Minutes to hours retrieval |
| S3 Glacier Deep Archive | Archive | 11 9s | 12-hour retrieval; lowest cost |
| EBS gp3 | Block | 99.999% | Default volume type; separate IOPS/throughput |
| EFS Standard | File | — | NFS; multi-AZ by default |
| FSx for Windows | File | — | SMB; Active Directory integration |

## Networking Services

| Service | Purpose | Exam Points |
|---|---|---|
| VPC | Virtual network | Spans one region; subnets in one AZ |
| Internet Gateway | Public internet access | One per VPC; attached to VPC not subnet |
| NAT Gateway | Outbound internet for private subnets | Deployed in public subnet; per-AZ for HA |
| VPC Peering | VPC-to-VPC connectivity | Non-transitive; no overlapping CIDRs |
| Transit Gateway | Hub-and-spoke VPC connectivity | Transitive routing; supports VPN and Direct Connect |
| PrivateLink | Private service endpoint | Avoids public internet; no CIDR overlap requirement |
| Direct Connect | Dedicated private line to AWS | Consistent bandwidth, low latency; not encrypted by default |
| Route 53 | DNS + health checks | Routing policies: Simple, Weighted, Latency, Failover, Geolocation, Multivalue |

## Security Services

| Service | Function |
|---|---|
| IAM | Identity and access management; users, roles, policies |
| KMS | Managed encryption key service; CMK, AWS-managed, AWS-owned keys |
| Secrets Manager | Store and rotate secrets; RDS native integration |
| SSM Parameter Store | Config and secrets; free tier with SecureString via KMS |
| WAF | Layer 7 firewall; rate limiting, IP rules, managed rule groups |
| Shield Standard | DDoS protection; free, automatic for all AWS customers |
| Shield Advanced | Enhanced DDoS; 24/7 DRT access; $3,000/month |
| GuardDuty | Threat detection; analyzes CloudTrail, VPC Flow Logs, DNS |
| Security Hub | Aggregated security findings across services and accounts |

## Database Services

| Service | Type | Multi-AZ HA | Read Scaling |
|---|---|---|---|
| RDS | Relational | Multi-AZ standby (sync) | Read Replicas (async) |
| Aurora | MySQL/PG-compatible | Automatic (6 copies, 3 AZs) | Up to 15 Read Replicas |
| DynamoDB | NoSQL | Global Tables for multi-region | DAX in-memory cache |
| ElastiCache Redis | In-memory | Multi-AZ with auto-failover | Read replicas |
| Redshift | Data warehouse | Multi-AZ cluster option | Concurrency Scaling |

## Study Checklist

- [ ] Know all S3 storage classes, retrieval times, and minimum storage durations
- [ ] Understand the difference between VPC Peering, Transit Gateway, and PrivateLink
- [ ] Memorize Route 53 routing policy types and use cases
- [ ] Know RDS Multi-AZ (sync standby) vs Read Replica (async scale-out)
- [ ] List five IAM best practices from memory
- [ ] Distinguish Shield Standard vs Advanced protection scope
- [ ] Know which services are regional vs global (IAM, Route 53, CloudFront are global)
