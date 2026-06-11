# Amazon EVS — Access Control

<div class="kb-summary">
AWS IAM permissions for EVS cluster management, vSphere RBAC roles for VMs and infrastructure, SDDC Manager roles, and least-privilege design principles.
</div>

```text
┌───────────────────────────────────── Amazon EVS — Access Control ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Two separate RBAC planes: AWS IAM (cluster/host lifecycle) + vSphere RBAC (VM operations)   │   │
│   │   AWS IAM: use managed policy AmazonEVSFullAccess or AmazonEVSReadOnlyAccess + custom         │   │
│   │   vSphere RBAC: no-permissions root role; assign custom roles scoped to inventory objects     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IAM role     = AWS identity with attached policies; grants evs:* API permissions                     │
│  AmazonEVSFullAccess = AWS managed policy; full EVS cluster and host lifecycle management             │
│  AmazonEVSReadOnlyAccess = Read-only EVS policy; safe for monitoring and compliance roles             │
│  vSphere RBAC = Binds a role to a user/group on a vCenter inventory object                            │
│  SDDC Manager role = Built-in VCF roles: ADMIN, OPERATOR, VIEWER for lifecycle management             │
│  SSO domain   = vSphere auth domain; vsphere.local default or AD-backed identity source               │
│  Privilege    = Atomic vCenter permission (~400+ available; e.g., VirtualMachine.Config.*)            │
│  Custom role  = User-defined set of vCenter privileges; assign at datacenter or cluster scope         │
│  Least privilege = Grant only minimum permissions; read-only roles where write is not needed          │
│  Service account = Non-human identity for CI/CD or monitoring; assign minimum required roles          │
│  CloudTrail   = AWS audit log capturing all evs:* API calls with actor, time, and IP address          │
│  SCP          = Service Control Policy; AWS Organizations guardrail restricting evs:* actions         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## AWS IAM for EVS

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EVSReadOnly",
      "Effect": "Allow",
      "Action": [
        "evs:ListEnvironments",
        "evs:GetEnvironment",
        "evs:ListEnvironmentHosts",
        "evs:ListEnvironmentVlans"
      ],
      "Resource": "*"
    }
  ]
}
```

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EVSAdminScoped",
      "Effect": "Allow",
      "Action": [
        "evs:CreateEnvironmentHost",
        "evs:DeleteEnvironmentHost",
        "evs:UpdateEnvironment"
      ],
      "Resource": "arn:aws:evs:us-east-1:123456789:environment/env-xxx"
    }
  ]
}
```

```bash
# Check IAM role used for EVS operations
aws sts get-caller-identity

# Verify access to EVS
aws evs list-environments

# Create IAM role for EVS read-only access (for monitoring/ops team)
aws iam create-role --role-name EVS-ReadOnly \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"arn:aws:iam::123456789012:root"},"Action":"sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name EVS-ReadOnly \
  --policy-arn arn:aws:iam::aws:policy/AmazonEVSReadOnlyAccess
```

## vSphere RBAC

```powershell
# Connect to vCenter
Connect-VIServer -Server $VCENTER -User administrator@vsphere.local -Password $PASS

# List existing roles
Get-VIRole | Select Name, Description

# Create a scoped operator role (VM power operations only)
New-VIRole -Name "VM-Operator" -Privilege (Get-VIPrivilege -Id "VirtualMachine.Interact.PowerOn",
  "VirtualMachine.Interact.PowerOff", "VirtualMachine.Interact.Suspend",
  "VirtualMachine.State.CreateSnapshot", "VirtualMachine.State.RemoveSnapshot",
  "System.View", "System.Anonymous", "System.Read")

# Assign role to AD group on a specific folder (scoped, not global)
$folder = Get-Folder -Name "Production"
$principal = "DOMAIN\vsphere-operators"
New-VIPermission -Entity $folder -Principal $principal -Role "VM-Operator" -Propagate $true

# List current permissions on cluster
Get-VIPermission -Entity (Get-Cluster) | Select Principal, Role, Propagate
```

## SDDC Manager Roles

| Role | Access Level | Typical User |
|---|---|---|
| ADMIN | Full SDDC Manager access; cluster management | Platform team lead |
| OPERATOR | Read + workflow execution; no destructive operations | Platform engineer |
| VIEWER | Read-only; dashboard and inventory | Monitoring, security |
| AUDITOR | Read-only + audit log access | Compliance team |

```bash
# Add user to SDDC Manager role via API
curl -sk -u "$SDDC_USER:$SDDC_PASS" \
  -X POST "https://sddc-manager.vcf.internal/v1/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "ops-user@domain.com", "role": {"name": "OPERATOR"}, "type": "USER"}'
```
