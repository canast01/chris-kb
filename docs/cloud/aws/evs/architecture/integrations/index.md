# Amazon EVS — Integrations

<div class="kb-summary">
EVS integration with on-premises infrastructure via HCX and Direct Connect, AWS native services (S3, Route 53, IAM), and cross-account VPC connectivity via Transit Gateway.
</div>

```text
┌────────────────────────────────────── Amazon EVS — Integrations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   HCX: live migration and cold migration between on-prem vSphere and EVS; no re-IP required   │   │
│   │   Direct Connect: private link; required for HCX vMotion; 1 Gbps min for production           │   │
│   │   Transit Gateway: connect EVS VPC to workload VPCs and on-premises; hub-and-spoke routing    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       HCX Migration         │  │      AWS Native Services     │  │     Direct Connect / TGW    │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  vMotion (live, no downtime)│  │  S3: backup/cold storage     │  │  DX: private connectivity   │  │
│   │  Cold migration (offline)   │  │  Route 53: DNS resolution    │  │  TGW: VPC-to-VPC routing   │   │
│   │  Bulk migration (WAN opt.)  │  │  IAM: EVS service roles      │  │  VPN: fallback only         │  │
│   │  No re-IP of VMs during mig │  │  CloudWatch: metrics via CW  │  │  BGP on T0 router to VPC   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## HCX (VMware Hybrid Cloud Extension)

HCX is the primary migration tool for moving VMs from on-premises vSphere to EVS.

```text
HCX components:
  HCX Manager (on-premises): deployed as OVA on on-prem vCenter; manages HCX service mesh
  HCX Cloud (EVS side):      auto-deployed by EVS; mirrors on-prem HCX Manager
  Service Mesh:              Interconnect (IX) + WAN Opt + Network Extension (NE) appliances

Migration types:
  vMotion         Live migration, no downtime. Requires 1 Gbps DX or sufficient bandwidth.
  Cold migration  Powered-off VM copy. Faster bulk data transfer.
  Bulk migration  Background copy with final vMotion switchover. Uses WAN optimization.
  OS-assisted     P2V or cross-hypervisor (requires HCX Enterprise license)

Network Extension (NE):
  Stretches on-prem L2 networks to EVS; VMs keep their IP addresses during migration.
  Remove NE after migration is complete (routing optimization).
```

```bash
# Verify HCX connectivity (run from HCX Manager UI or API)
# Check: HCX Manager → Interconnect → Service Mesh → Status = Green

# HCX vMotion requires port 443 and 8301 open between on-prem and EVS HCX Cloud
# Direct Connect private VIF or VPN must have these ports allowed
```

## Direct Connect

```text
Connection types:
  Dedicated: 1G or 10G physical port; request via AWS console; ~15-45 day lead time
  Hosted:    Sub-1G via AWS partner; faster provisioning; shared infrastructure

VIF types for EVS:
  Private VIF: access VPC resources (management subnet, EVS hosts); required for HCX
  Transit VIF: attach to Transit Gateway; recommended for multi-VPC or hybrid architectures

BGP peering:
  AWS side: ASN 64512 (default) or custom
  On-prem:  your router ASN
  Advertise: on-prem prefixes to AWS; AWS advertises VPC CIDRs back
```

## Transit Gateway (TGW)

```text
Use TGW when you need:
  EVS → other AWS VPCs (workload VPCs, shared services)
  On-premises → multiple AWS VPCs via single DX attachment
  East-west between multiple EVS clusters in same region

Architecture:
  DX → Transit VIF → TGW
  EVS VPC → TGW attachment (VPC route table points to TGW)
  Spoke VPCs → TGW attachments
  TGW route table: propagate EVS CIDR, on-prem CIDR, spoke VPC CIDRs

Note: EVS T0 router advertises workload VM prefixes via BGP to VPC ENI.
The VPC route table entry for those prefixes points to the T0 uplink ENI.
TGW then propagates those routes to connected spoke VPCs.
```

## AWS Native Service Integration

```bash
# S3 — object storage for backups and cold data
# Access from EVS VMs: via VPC Endpoint (Gateway) or NAT Gateway
# Recommended: S3 Gateway VPC Endpoint (no cost, stays in VPC)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-evs-xxx \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-evs-workload

# Route 53 — DNS for VCF components
# Create private hosted zone for vcf.internal
# Associate with EVS VPC
aws route53 create-hosted-zone \
  --name vcf.internal \
  --vpc VPCRegion=us-east-1,VPCId=vpc-evs-xxx \
  --caller-reference $(date +%s)

# IAM — EVS service role
# EVS creates an IAM service-linked role: AWSServiceRoleForAmazonEVS
# Do not delete this role — EVS uses it for host lifecycle management

# CloudWatch — EVS publishes host metrics (CPU, memory, disk) to CloudWatch
# Namespace: AWS/EVS
# Useful metric: HostCount, HostStatus
aws cloudwatch get-metric-statistics \
  --namespace AWS/EVS \
  --metric-name HostStatus \
  --dimensions Name=ClusterId,Value=evs-cluster-id \
  --period 300 --statistics Average \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ)
```
