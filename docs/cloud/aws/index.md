# AWS

<div class="kb-summary">
Amazon Web Services knowledge base covering compute, storage, networking, identity, monitoring, backup, security, governance, and cost management. Includes architecture references, operational procedures, CLI commands, and troubleshooting guides.
</div>

```
┌───────────────────────────────────────── AWS Platform Stack ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                         AWS Management                                        │   │
│   │       Console · CloudWatch · CloudTrail · Organizations · Control Tower · Cost Explorer       │   │
│   │       AWS Config: resource compliance rules · SCPs: account-level permission guardrails       │   │
│   │             Trusted Advisor: cost, security, and performance best-practice checks             │   │
│   │              AWS CLI · SDK (boto3) · CloudFormation · CDK: infrastructure as code             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Governance and automation span all AWS services and accounts                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           AWS IAM           │  │           Compute           │  │          Networking         │   │
│   │    Users · groups · roles   │  │   EC2: on-demand/reserved   │  │    VPC: subnets · routing   │   │
│   │     Policies: allow/deny    │  │    Auto Scaling · ALB/NLB   │  │    SG · NACL: stateful FW   │   │
│   │    STS: temp credentials    │  │    ECS · EKS: containers    │  │     Route53: DNS service    │   │
│   │    AssumeRole: delegation   │  │   Lambda: serverless FaaS   │  │    CloudFront: global CDN   │   │
│   │    SAML 2.0 · OIDC · SSO    │  │     Spot: spare capacity    │  │      WAF · Shield: DDoS     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    IAM controls access · EC2 runs inside VPCs · networking isolates workloads                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Storage           │  │           Database          │  │    Security & Monitoring    │   │
│   │   S3: object + versioning   │  │   RDS: managed relational   │  │   GuardDuty: threat detect  │   │
│   │   EBS: block volumes (EC2)  │  │   Aurora: MySQL/PostgreSQL  │  │    Security Hub: findings   │   │
│   │    EFS: managed NFS share   │  │   DynamoDB: serverless KV   │  │  CloudTrail: API audit log  │   │
│   │  FSx: Windows/Lustre/ONTAP  │  │   ElastiCache: Redis/Memcd  │  │   Config: compliance rules  │   │
│   │   Glacier: archive storage  │  │   Redshift: data warehouse  │  │     KMS: key management     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Storage, databases, and security services consumed as fully managed APIs                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Hybrid & Multi-Account Connectivity                              │   │
│   │         Direct Connect: dedicated private circuit from on-premises to AWS (1/10 Gbps)         │   │
│   │           Site-to-Site VPN: IPsec tunnel over the public internet to a VPC endpoint           │   │
│   │           Transit Gateway: hub-and-spoke router connecting VPCs and on-prem networks          │   │
│   │             VPC Peering: private routing between two VPCs within or across regions            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS global regions and availability zones; data centres owned and operated by Amazon                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IAM           = Identity and Access Management; controls which API actions a principal can call      │
│  STS           = Security Token Service; issues temporary credentials via AssumeRole                  │
│  EC2           = Elastic Compute Cloud; virtual machines with hundreds of instance type families      │
│  ECS           = Elastic Container Service; managed container orchestration on EC2 or Fargate         │
│  EKS           = Elastic Kubernetes Service; AWS managed Kubernetes control plane                     │
│  Lambda        = Serverless function execution; event-driven, no server provisioning required         │
│  VPC           = Virtual Private Cloud; isolated network with subnets, route tables, and gateways     │
│  SG            = Security Group; stateful firewall applied to EC2 instances and ENIs                  │
│  S3            = Simple Storage Service; object store with 11 nines durability guarantee              │
│  EBS           = Elastic Block Store; persistent block volumes for EC2; gp3 and io2 Block Express     │
│  RDS           = Relational Database Service; managed MySQL, PostgreSQL, SQL Server, Oracle           │
│  Route53       = AWS managed DNS; latency routing, geo-routing, and health-check failover             │
│  CloudFront    = AWS CDN; caches content at 400+ global edge locations; integrates with WAF           │
│  GuardDuty     = ML threat detection; analyses VPC Flow Logs, CloudTrail, and DNS logs                │
│  Direct Connect= Dedicated private circuit from on-premises to AWS — bypasses public internet         │
│  Transit Gateway= Hub-and-spoke router connecting multiple VPCs and Direct Connect/VPN links          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
