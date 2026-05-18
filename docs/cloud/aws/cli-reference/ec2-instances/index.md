# EC2 — Instances

```
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

> Part of the AWS CLI Reference.

---

```bash
# List instances
aws ec2 describe-instances
aws ec2 describe-instances --filters "Name=tag:Name,Values=<name>"
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table

# Start / stop / reboot
aws ec2 start-instances --instance-ids <id>
aws ec2 stop-instances --instance-ids <id>
aws ec2 reboot-instances --instance-ids <id>
aws ec2 terminate-instances --instance-ids <id>

# Instance types
aws ec2 describe-instance-types --instance-types t3.medium

# Key pairs
aws ec2 describe-key-pairs
aws ec2 create-key-pair --key-name <name> --query 'KeyMaterial' --output text > key.pem

# Security groups
aws ec2 describe-security-groups
aws ec2 authorize-security-group-ingress --group-id <sg_id> --protocol tcp --port 22 --cidr 10.0.0.0/8
aws ec2 revoke-security-group-ingress --group-id <sg_id> --protocol tcp --port 22 --cidr 10.0.0.0/8
```
