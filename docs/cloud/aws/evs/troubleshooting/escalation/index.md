# Amazon EVS — Escalation

<div class="kb-summary">
AWS support escalation for EVS: severity levels, required data for support cases, joint VMware/AWS ticket coordination, and TAM escalation for production-critical issues.
</div>

```text
┌─────────────────────────────────── Amazon EVS — Support Escalation ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   EVS issues span two vendors: AWS (host/infrastructure) and VMware/Broadcom (VCF software)   │   │
│   │   AWS support: required for host failures, ENI issues, and AWS-layer networking problems      │   │
│   │   VMware support: required for vSAN, NSX-T, vCenter, and SDDC Manager software issues        │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Severity Levels

| Severity | Definition | AWS Response SLA |
|---|---|---|
| Critical | Production cluster down; business-critical workloads unavailable | 15 min (Business/Enterprise) |
| High | Production degraded; significant function impaired | 1 hour |
| Medium | Non-critical failure; workaround available | 4 hours |
| Low | General question or guidance needed | 1 business day |

Enterprise Support plan required for Critical SLA. Business Support provides High = 4 hours.

## Required Data for AWS Support Case

```bash
# 1. EVS environment and host IDs
aws evs get-environment --environment-id $ENV_ID \
  --query '[environment.environmentName, environment.state]' --output text

aws evs list-environment-hosts --environment-id $ENV_ID \
  --query 'hostSummaries[*].[hostId,instanceType,state]' --output table

# 2. CloudTrail export (last 24 hours of EVS events)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=evs.amazonaws.com \
  --start-time $(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ) \
  --output json > cloudtrail-evs-24h.json

# 3. EC2 instance status for EVS hosts
aws ec2 describe-instance-status \
  --instance-ids $(aws evs list-environment-hosts --environment-id $ENV_ID \
    --query 'hostSummaries[*].hostId' --output text) \
  --output json > ec2-instance-status.json

# 4. VPC and subnet configuration
aws ec2 describe-subnets \
  --filters Name=vpc-id,Values=$EVS_VPC_ID --output json > vpc-subnets.json

# 5. Symptom timeline: when did the issue start? what changed?
# Include: last successful operation timestamp, first error observed, any DX/VPN changes
```

## Escalation Path

```text
EVS Infrastructure Issue (host, ENI, VPC, DX):
  1. Open AWS support case (severity Critical or High)
  2. Phone: available for Business/Enterprise support plans
     Enterprise: 24×7 phone access; Business: 24×7 for Critical
  3. Provide: environment ID, host ID, CloudTrail export, EC2 status
  4. If no progress in 1-2 hours: request TAM (Technical Account Manager)

VCF Software Issue (vSAN, NSX-T, vCenter, SDDC Manager):
  1. Open VMware support case (Broadcom Support portal)
  2. Provide: vSAN/NSX support bundle, VCF version, SDDC Manager logs
  3. For joint issues (e.g., NSX-T can't communicate over EVS ENI):
     Open both AWS and VMware cases and reference each other's case ID

Both vendors involved (most common for HCX issues):
  1. Open AWS case for network layer (ENI, SG, DX, VPC routing)
  2. Open VMware case for HCX application layer
  3. Note: AWS and VMware have joint escalation process for EVS
```

## VMware Support Data Collection

```bash
# Always gather before calling VMware support

# 1. NSX-T support bundle
curl -sk -u "admin:$NSX_PASSWORD" \
  -X POST "$NSX_URL/api/v1/support-bundles?action=collect" \
  -H "Content-Type: application/json" -d '{}' | python3 -m json.tool

# 2. vCenter log bundle
# vCenter UI → Administration → Support → Create Support Bundle
# Or SFTP: /var/log/vmware/support/*.zip on vCenter appliance

# 3. SDDC Manager bundle
curl -sk -u "$SDDC_USER:$SDDC_PASS" \
  -X POST "https://sddc-manager.vcf.internal/v1/support-bundles" \
  -H "Content-Type: application/json" | python3 -m json.tool

# 4. vSAN Health XML export
# vCenter → Cluster → vSAN → Skyline Health → Export Health Data
```
