# Amazon EVS — Deploy

<!-- diagram:evs-deploy -->

<div class="kb-summary">
EVS cluster deployment: prerequisites, VPC setup, cluster creation via AWS console or CLI, initial VCF configuration, HCX deployment, and post-deploy validation checklist.
</div>

```text
┌──────────────────────────────────────── Amazon EVS Deployment ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    EVS Deployment Sequence                                    │   │
│   │            Pre-requisites: VPC, subnets, SGs, IAM service-linked role, key pair, DX           │   │
│   │                 Cluster creation via AWS console or CLI; takes 90-120 minutes                 │   │
│   │         Post-deploy: retrieve secrets, configure SDDC Manager, deploy HCX service mesh        │   │
│   │         Validation: cluster CREATED + vSAN green + NSX-T stable + HCX service mesh Up         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│    SDDC Manager = VCF control plane; manages hosts, domains, upgrades, credentials                    │
│    VTEP subnet  = NSX-T tunnel endpoint traffic; separate from management subnet                      │
│    Service mesh = HCX Interconnect + WAN Opt + Network Extension appliance pair                       │
│                                                                                                       │
```

## Prerequisites

```bash
# 1. VPC and subnets
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=evs-vpc}]'

# Required subnets (minimum):
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.0.0/20 --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=evs-management}]'
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.16.0/20 --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=evs-vtep}]'

# 2. Security groups for EVS
# EVS requires specific ports — check current AWS documentation for full list
# Minimum: 443 (vCenter/NSX API), 902 (ESXi), 5671 (vSphere messaging), 8301 (HCX)
aws ec2 create-security-group --group-name evs-management-sg \
  --description "EVS Management Security Group" --vpc-id vpc-xxx

# 3. IAM service-linked role (created automatically on first EVS cluster, or manually)
aws iam create-service-linked-role --aws-service-name elasticvmwareservice.amazonaws.com

# 4. SSH key pair (used for initial ESXi DCUI access if needed)
aws ec2 create-key-pair --key-name evs-cluster-key --output text > evs-cluster-key.pem
chmod 400 evs-cluster-key.pem
```

## Create EVS Cluster (AWS CLI)

```bash
# Create EVS cluster — replaces the AWS console flow
aws evs create-environment \
  --environment-name prod-evs-cluster-01 \
  --vcf-version VCF-5.1 \
  --connectivity-info '{
    "privateRouteServerPeerings": [],
    "vpcId": "vpc-xxx"
  }' \
  --initial-vlan-subnet-tags '[
    {"key": "Name", "value": "evs-management"},
    {"key": "Name", "value": "evs-vtep"}
  ]' \
  --hosts '[
    {"instanceType": "i4i.metal", "keyName": "evs-cluster-key"},
    {"instanceType": "i4i.metal", "keyName": "evs-cluster-key"},
    {"instanceType": "i4i.metal", "keyName": "evs-cluster-key"}
  ]'

# Monitor creation status
aws evs get-environment --environment-id env-xxx
# Status: CREATING → CREATED (takes 90-120 min)
```

## Post-Deploy VCF Configuration

```bash
# After cluster is in CREATED state:
# 1. Retrieve SDDC Manager credentials from AWS Secrets Manager
aws secretsmanager get-secret-value \
  --secret-id /evs/prod-evs-cluster-01/sddc-manager-credentials \
  --query SecretString --output text | jq .

# 2. Access SDDC Manager UI
# URL shown in EVS environment details
# Login with retrieved credentials → change default passwords

# 3. Access vCenter
# vCenter URL from SDDC Manager → vCenters
# Login: administrator@vsphere.local + password from Secrets Manager

# 4. Verify vSAN cluster health
# vCenter → Cluster → vSAN → Skyline Health
# All checks should pass before deploying workloads
```

## HCX Deployment (On-Premises Side)

```bash
# 1. Download HCX OVA from EVS console → HCX tab
# 2. Deploy HCX Manager OVA on on-premises vCenter
#    - Assign management IP, DNS, NTP
#    - Activate with HCX license key from EVS console

# 3. Pair on-prem HCX Manager with EVS HCX Cloud
#    - HCX Manager UI → Site Pairing → Add Site
#    - URL: https://<evs-hcx-cloud-ip>
#    - Credentials from EVS Secrets Manager

# 4. Create Service Mesh (compute profile + service mesh)
#    - Compute profile: select on-prem hosts and datastores
#    - Service mesh: pair with EVS site → deploys IX, WAN opt, NE appliances

# 5. Extend L2 network (Network Extension)
#    - HCX UI → Network Extension → Extend a network
#    - Select on-prem dvPortGroup to extend to EVS
#    - Provides same L2 segment on both sides (no re-IP during migration)
```

## Post-Deploy Validation Checklist

```bash
# EVS cluster health
aws evs get-environment --environment-id env-xxx --query 'environment.state'
# Expected: CREATED

# vSAN health (run from vCenter API or PowerCLI)
# All clusters should show Green in vSAN Skyline Health

# NSX-T health
# NSX Manager → System → Overview → All components Green

# HCX connectivity
# HCX Manager → Interconnect → Service Mesh → Status = Green

# DNS resolution
# From a VM in EVS: nslookup vcenter.vcf.internal
# Should resolve to vCenter IP in management subnet

# vCenter reachability from on-prem
curl -k -o /dev/null -w "%{http_code}" https://vcenter.vcf.internal/ui/
# Expected: 200
```
