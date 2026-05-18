# AWS

<div class="kb-summary">
Amazon Web Services knowledge base covering compute, storage, networking, identity, monitoring, backup, security, governance, and cost management. Includes architecture references, operational procedures, CLI commands, and troubleshooting guides.
</div>

```
┌─────────────────────────────────────────────────────────┐
│                  AWS Service Hierarchy                  │
│                                                         │
│  Management Account (Organizations / SCPs)              │
│        │                                                │
│        ▼                                                │
│  Member Account (workload)                              │
│  ├── IAM (users · roles · policies)                     │
│  └── VPC (10.x.0.0/16)                                  │
│       ├── Public Subnet  → EC2 · ALB · NAT GW           │
│       ├── Private Subnet → EC2 · ECS · Lambda           │
│       └── Isolated Subnet→ RDS · ElastiCache            │
│                                                         │
│  Storage: EBS (block) · S3 (object) · EFS (file)        │
└─────────────────────────────────────────────────────────┘
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
