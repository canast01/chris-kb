# AWS Operations — Install & Upgrade

```bash
# View patch compliance status
aws ssm describe-instance-patch-states --instance-ids <i-xxxx>

# Run patching on a specific instance now (ad-hoc)
aws ssm send-command \
    --document-name "AWS-RunPatchBaseline" \
    --instance-ids <i-xxxx> \
    --parameters "Operation=Install" \
    --comment "Manual patch run $(date)"

# List instances with missing patches
aws ssm describe-instance-patches --instance-id <i-xxxx> \
    --filters "Key=State,Values=Missing"
```
```text
┌───────────────────────────────── AWS Operations — Install & Upgrade ──────────────────────────────────┐
│                                                                                                       │
│  Patching, agent upgrades, AMI refresh, and service version management procedures.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 EC2 Patching                 │  │                Agent Upgrades               │   │
│   │      SSM Patch Manager: baseline + scan      │  │      CloudWatch agent: SSM distributor      │   │
│   │      Patch groups: tag-based targeting       │  │        SSM agent: auto-update setting       │   │
│   │      Maintenance window: scheduled run       │  │          X-Ray daemon: via userdata         │   │
│   │        Pre-patch: snapshot AMI first         │  │      CodeDeploy agent: SSM distributor      │   │
│   │     Post-patch: compliance report in CW      │  │        Inspector agent: auto-managed        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  AMI refresh strategy: build new AMI with Packer, replace instances via Auto Scaling.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             RDS & Other Services             │  │            Blue/Green & Immutable           │   │
│   │          RDS: modify engine version          │  │        Auto Scaling: instance refresh       │   │
│   │     RDS: apply during maintenance window     │  │      CodeDeploy: blue/green deployment      │   │
│   │        EKS: managed node group update        │  │      Elastic Beanstalk: rolling update      │   │
│   │      Lambda: version + alias promotion       │  │        CloudFormation: rolling update       │   │
│   │     ElastiCache: cluster version update      │  │      Bake new AMI: never patch in place     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS EC2 host fleet · RDS managed hardware · EKS control plane infrastructure                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Patch baseline  = SSM policy defining which patches to install; OS and severity filters              │
│  Patch group     = Tag value (Patch Group) used to associate instances with a baseline                │
│  Maintenance window= SSM scheduled time window for patch and other automation tasks                   │
│  Distributor     = SSM feature for installing and updating agent packages on instances                │
│  Instance refresh= Auto Scaling feature replacing instances with updated launch template              │
│  AMI bake        = Build a new AMI with all patches baked in; replace running instances               │
│  Blue/green      = New environment deployed alongside old; traffic switched at cutover                │
│  Rolling update  = Update subset of instances at a time; maintains partial availability               │
│  RDS apply-immediately= Forces maintenance change immediately vs next window                          │
│  Lambda alias    = Pointer to a function version; shift traffic between versions                      │
│  Compliance report= SSM Patch Manager scan result: compliant/non-compliant per instance               │
│  Immutable upgrade= Never patch in place; always replace with pre-patched AMI                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# List Lambda functions by runtime
aws lambda list-functions --query 'Functions[*].[FunctionName,Runtime]' --output table | sort

# Update runtime (requires testing)
aws lambda update-function-configuration --function-name <name> --runtime python3.12
```
```bash
# Check current EKS version
aws eks describe-cluster --name <cluster-name> --query 'cluster.version'

# List available upgrade versions
aws eks describe-addon-versions --kubernetes-version 1.30

# Upgrade cluster control plane
aws eks update-cluster-version --name <cluster-name> --kubernetes-version 1.30

# Upgrade node groups after control plane
aws eks update-nodegroup-version --cluster-name <cluster-name> \
    --nodegroup-name <nodegroup-name> --kubernetes-version 1.30
```
```bash
# Check RI utilisation
aws ce get-reservation-utilization --time-period Start=2026-01-01,End=2026-01-31

# List expiring RIs
aws ec2 describe-reserved-instances --filters "Name=state,Values=active" \
    --query "ReservedInstances[?End<='$(date -d '+90 days' +%Y-%m-%d)T23:59:59'].[ReservedInstancesId,InstanceType,End]"
```
