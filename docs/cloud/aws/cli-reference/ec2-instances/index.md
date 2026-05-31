# EC2 — Instances

```text
EC2 Instance CLI: State Management
──────────────────────────────────────────────────────────────

  describe-instances (filter by tag / ID)
          │
          ▼
  ┌───────────────────────────────────────────┐
  │         Instance States                   │
  │                                           │
  │  stopped ──► start-instances ──► running  │
  │  running ──► stop-instances  ──► stopped  │
  │  running ──► reboot-instances             │
  │  any     ──► terminate-instances──► term. │
  └───────────────────────────────────────────┘

  ┌─────────────────┐    ┌──────────────────────────┐
  │  Key Pairs      │    │  Security Groups          │
  │                 │    │                           │
  │ describe-key-   │    │ describe-security-groups  │
  │   pairs         │    │ authorize-sg-ingress      │
  │ create-key-pair │    │ revoke-sg-ingress         │
  │  → key.pem      │    │                           │
  └─────────────────┘    └──────────────────────────┘
```
```text
┌─────────────────────────────────────── AWS CLI — EC2 Instances ───────────────────────────────────────┐
│                                                                                                       │
│  EC2 instance CLI commands for lifecycle, metadata, connect, and troubleshooting.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Instance Lifecycle              │  │             Instance Inspection             │   │
│   │            run-instances: launch             │  │           describe-instances: list          │   │
│   │          start-instances: power on           │  │           describe-instance-status          │   │
│   │           stop-instances: graceful           │  │         describe-instance-attribute         │   │
│   │          reboot-instances: restart           │  │           get-console-output: log           │   │
│   │         terminate-instances: delete          │  │            get-console-screenshot           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  run-instances launches; describe-instances filters by state, tag, or instance ID                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Connect and Manage              │  │              Metadata and Tags              │   │
│   │           ssm start-session: shell           │  │           describe-tags: list tags          │   │
│   │          ec2-instance-connect: SSH           │  │             create-tags: add tag            │   │
│   │          send-ssh-public-key: temp           │  │             delete-tags: remove             │   │
│   │          modify-instance-attribute           │  │           describe-instance-types           │   │
│   │          monitor-instances: enable           │  │         describe-availability-zones         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  EC2 host hardware · Nitro hypervisor · VPC network · EBS storage · SSM service                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  run-instances   = Launches one or more EC2 instances from an AMI                                     │
│  ssm start-session= Opens interactive shell via SSM without SSH or key pair                           │
│  ec2-instance-connect= Pushes temporary SSH public key and opens SSH session                          │
│  get-console-output= Retrieves serial console log; useful when instance unreachable                   │
│  get-console-screenshot= Screenshot of instance display; diagnose stuck boot                          │
│  describe-instance-status= Shows system and instance reachability check results                       │
│  modify-instance-attribute= Changes instance type, user data, or termination protection               │
│  monitor-instances= Enables detailed 1-minute CloudWatch monitoring                                   │
│  Nitro hypervisor= AWS-built hypervisor providing performance and security isolation                  │
│  Termination protection= Setting preventing accidental terminate-instances call                       │
│  Instance metadata= EC2 service at 169.254.169.254 providing IAM role credentials                     │
│  User data       = Script or cloud-init config executed on first boot                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
