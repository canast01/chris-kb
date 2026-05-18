# AWS Compute

<div class="kb-summary">
AWS compute spans EC2 virtual machines, Auto Scaling groups, Lambda serverless functions, and ECS/EKS containers. Fleet management runs through Systems Manager — no bastion hosts required. AMI standardisation and Patch Manager enforce OS hygiene across the fleet.
</div>

```
┌─────────────────────────────────────────────────────────┐
│                  AWS Compute Overview                   │
│                                                         │
│  AMI (snapshot + launch config)                         │
│   │                                                     │
│   ▼                                                     │
│  Instance Type (family: t/m/c/r/x) + size              │
│   │                                                     │
│   ▼                                                     │
│  EC2 Instance ── EBS root disk ── Security Group        │
│   │                                                     │
│   ├── Auto Scaling Group (min / desired / max)          │
│   ├── Systems Manager Agent (patch · session · run)     │
│   └── Lambda (event-driven · no server · scale to 0)   │
└─────────────────────────────────────────────────────────┘
```

![AWS Compute Architecture](../../../assets/aws-compute-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="ec2/">
  <strong>EC2</strong>
  <span>Virtual machines, instance lifecycle, access, sizing, and operations.</span>
</a>

<a class="kb-card" href="auto-scaling/">
  <strong>Auto Scaling</strong>
  <span>Scaling groups, launch templates, desired capacity, and health checks.</span>
</a>

<a class="kb-card" href="lambda/">
  <strong>Lambda</strong>
  <span>Serverless functions, triggers, logs, permissions, and runtime checks.</span>
</a>

<a class="kb-card" href="systems-manager/">
  <strong>Systems Manager</strong>
  <span>Fleet operations, inventory, session access, and automation.</span>
</a>

<a class="kb-card" href="amis/">
  <strong>AMIs</strong>
  <span>Image standards, lifecycle, patch baselines, and recovery use cases.</span>
</a>

<a class="kb-card" href="patch-manager/">
  <strong>Patch Manager</strong>
  <span>Patch baselines, maintenance windows, compliance, and reporting.</span>
</a>

<a class="kb-card" href="instance-recovery/">
  <strong>Instance Recovery</strong>
  <span>Recovery alarms, instance checks, and workload recovery steps.</span>
</a>

</div>
