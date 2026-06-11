# Amazon EVS — Hardening

<div class="kb-summary">
EVS hardening: NSX-T micro-segmentation default deny, VPC security groups, AWS VPC flow logs, disabling unnecessary services on ESXi, and CIS hardening controls for VCF.
</div>

```text
┌─────────────────────────────────────── Amazon EVS — Hardening ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   NSX-T DFW: default deny + explicit allow; isolate tenants and workload tiers by policy       │  │
│   │   VPC security groups: limit inbound to management subnet CIDRs only; deny internet by default  │ │
│   │   ESXi hardening: disable SSH after setup, enable lockdown mode, NTP sync required             │  │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NSX-T DFW    = Distributed Firewall; enforces rules at each VM vNIC; default deny posture            │
│  Micro-segmentation = Zero-trust network model; workloads only talk to explicitly allowed peers       │
│  VPC security group = AWS stateful firewall at ENI level; restrict inbound to management CIDRs        │
│  VPC Flow Logs = Captured ENI-level traffic metadata; stored in CloudWatch or S3 for audit            │
│  Lockdown mode = ESXi feature restricting direct host access; API/UI only via vCenter                 │
│  CIS benchmark = Center for Internet Security hardening guide for VMware ESXi and VCF                 │
│  NTP          = Network Time Protocol; required for SSO and cert validity; use AWS NTP                │
│  SSH          = Access to ESXi hosts; disable after initial setup; re-enable only when needed         │
│  CloudTrail   = AWS audit service; all evs:* API calls recorded with actor and timestamp              │
│  GuardDuty    = AWS threat detection; monitors VPC traffic and CloudTrail for anomalies               │
│  Security Hub = AWS aggregator for CIS benchmark findings across the account                          │
│  Normal lockdown = ESXi lockdown mode allowing DCUI + vCenter access (not Strict)                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## NSX-T Micro-segmentation

```bash
# Create security groups for workload tiers
curl -sk -u "admin:$NSX_PASSWORD" \
  -X POST "$NSX_URL/api/v1/ns-groups" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "web-tier",
    "members": [{"resource_type": "NSGroupTagExpression",
                 "tag": "tier", "scope": "app", "op": "CONTAINS", "tag_op": "EQUALS"}]
  }'

# Create default-deny firewall section at bottom of rule list
curl -sk -u "admin:$NSX_PASSWORD" \
  -X POST "$NSX_URL/api/v1/firewall/sections?operation=insert_bottom" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "Default Deny All",
    "section_type": "LAYER3",
    "stateful": true,
    "rules": [{
      "display_name": "Deny All",
      "action": "DROP",
      "logged": true,
      "sources_excluded": false,
      "destinations_excluded": false,
      "ip_protocol": "IPV4_IPV6",
      "direction": "IN_OUT"
    }]
  }'

# Create explicit allow rule above the default-deny section
# NSX-T UI → Security → Distributed Firewall → Add rule above "Default Deny All"
```

## VPC Security Groups

```bash
# Restrict EVS management SG — only allow from management bastion or Direct Connect CIDR
aws ec2 authorize-security-group-ingress \
  --group-id sg-evs-management \
  --protocol tcp --port 443 --cidr 10.0.0.0/8  # corporate range via DX

aws ec2 authorize-security-group-ingress \
  --group-id sg-evs-management \
  --protocol tcp --port 902 --cidr 10.0.0.0/8  # ESXi host access

# Deny internet-bound traffic from EVS VPC (no IGW attached by default)
# Verify: no Internet Gateway attached to EVS VPC
aws ec2 describe-internet-gateways \
  --filters Name=attachment.vpc-id,Values=$EVS_VPC_ID

# Enable VPC Flow Logs for EVS VPC (security audit requirement)
aws ec2 create-flow-logs \
  --resource-ids $EVS_VPC_ID \
  --resource-type VPC \
  --traffic-type ALL \
  --log-destination-type s3 \
  --log-destination "arn:aws:s3:::evs-flow-logs-bucket"
```

## ESXi Hardening

```bash
# Disable SSH after deployment (SSH should only be enabled during maintenance)
# Via PowerCLI:
Get-VMHost | ForEach-Object {
    Get-VMHostService -VMHost $_ | Where-Object {$_.Key -eq "TSM-SSH"} | Stop-VMHostService -Confirm:$false
    Set-VMHostService -HostService (Get-VMHostService -VMHost $_ | Where-Object {$_.Key -eq "TSM-SSH"}) -Policy "off"
}

# Enable Lockdown Mode (Normal) — prevents direct ESXi access, requires vCenter
Get-VMHost | Foreach { $_.ExtensionData.EnterLockdownMode() }

# Verify NTP sync on all hosts
Get-VMHost | Get-VMHostNtpServer
Get-VMHost | ForEach-Object { (Get-View $_.Id).Runtime.DasHostState }
```

## CIS VCF Hardening Checklist

| Control | Action |
|---|---|
| Disable ESXi SSH after setup | Set TSM-SSH service to off; use vCenter for management |
| Enable ESXi Lockdown Mode | Normal lockdown: vCenter-managed access only |
| Enforce NTP sync | All hosts synchronized; etcd requires < 500ms drift |
| Remove default admin account aliases | Rename or disable default accounts after initial setup |
| Enable vCenter SSO password policy | Minimum 12 chars, complexity, 90-day rotation |
| Enable vSAN encryption at rest | Encrypt data at rest using NKP or external KMS |
| Enable VPC Flow Logs | Capture all traffic for audit trail |
| NSX-T default deny DFW | Explicit-allow model; log all deny hits |
| MFA for AWS console | Enforce MFA policy for all IAM users |
| Rotate Secrets Manager credentials | Rotate SDDC Manager + vCenter passwords quarterly |
