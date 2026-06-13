---
tags:
  - aws
  - troubleshooting
---
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
│  Key terms:                                                                                           │
│                                                                                                       │
│  AWS Business/Enterprise Support = Required tier for EVS production; includes TAM and SLA             │
│  TAM          = Technical Account Manager; AWS named escalation contact for production issues         │
│  P1 case      = Severity 1 support case; production system down; 15-minute initial response           │
│  P2 case      = Severity 2; significant impairment; 1-hour initial response SLA                       │
│  Broadcom GSS = Global Support Services; VMware/Broadcom portal for VCF software issues               │
│  Joint case   = AWS and VMware/Broadcom cases raised in parallel for EVS platform issues              │
│  SOS report   = SDDC Manager → Support → SOS Report; captures full VCF platform state                 │
│  vm-support   = ESXi support bundle; required for VMware/Broadcom case submission                     │
│  NSX support bundle = NSX Manager → Troubleshoot → Support Bundle; required for NSX cases             │
│  CR           = Change Request; formal process for non-urgent production modifications                │
│  SLA          = Service Level Agreement; defines response and resolution time per severity level      │
│  aws re:Post  = AWS community support forum; search before raising a P2/P3 support case               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Case Routing Matrix

Use this matrix to determine who to contact first and when to open joint cases.

| Issue Type | First Contact | Escalation | Joint Case? |
|---|---|---|---|
| Host FAILED or CREATE_FAILED | AWS Support | AWS TAM after 2 hours with no progress | No — AWS owns host infrastructure |
| vSAN data loss risk (object inaccessible) | VMware/Broadcom GSS | VMware TAM / Duty Manager | Yes if EVS host or ENI is also failed |
| NSX-T control plane down (Manager VMs unreachable) | VMware/Broadcom GSS | VMware TAM | Yes if vSAN or host failure contributed |
| HCX migration failure | AWS Support (DX/network layer) + VMware GSS (HCX layer) | Both TAMs | Always — HCX spans both |
| EVS API error (InternalServerException) | AWS Support | AWS TAM after 1 hour | No |
| DX connectivity loss affecting EVS management | AWS Support | AWS TAM immediately (P1 scope) | No |
| SDDC Manager workflow stuck | VMware/Broadcom GSS | VMware TAM | No |
| vCenter unreachable (not vSAN-related) | VMware/Broadcom GSS | VMware TAM | No |

When an issue involves both infrastructure and software (e.g., a host failure that triggered vSAN degradation which then caused NSX-T Manager VMs to lose storage), open cases with both vendors simultaneously and share case IDs between them. AWS and VMware/Broadcom have a joint escalation process for EVS specifically.

## Severity Levels

| Severity | Definition | AWS Response SLA |
|---|---|---|
| Critical | Production cluster down; business-critical workloads unavailable | 15 min (Business/Enterprise) |
| High | Production degraded; significant function impaired | 1 hour |
| Medium | Non-critical failure; workaround available | 4 hours |
| Low | General question or guidance needed | 1 business day |

Enterprise Support plan required for Critical SLA. Business Support provides High = 4 hours.

## AWS Support Case Requirements

Always include this data when opening an EVS case with AWS. Missing information causes round-trip delays averaging 4-6 hours per exchange.

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

For networking issues (HCX tunnel down, BGP failure), also include:

```bash
# VPC route tables
aws ec2 describe-route-tables \
  --filters Name=vpc-id,Values=$EVS_VPC_ID --output json > vpc-route-tables.json

# ENI status for EVS management subnet
aws ec2 describe-network-interfaces \
  --filters Name=subnet-id,Values=$EVS_MGMT_SUBNET_ID \
  --output json > eni-status.json

# DX connection state
aws directconnect describe-connections \
  --query 'connections[*].[connectionId,connectionName,connectionState,bandwidth]' \
  --output table
```

## VMware Support Case Requirements

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

Additional data for VMware support cases:

```powershell
# VCF version and build numbers
Connect-VIServer -Server $VCENTER -User administrator@vsphere.local -Password $PASS
$vcenter = Get-View -Id "ServiceInstance"
Write-Host "vCenter build: $($vcenter.Content.About.Build)"
Write-Host "vCenter version: $($vcenter.Content.About.Version)"

# Host build info
Get-VMHost | Select Name, Build, Version

# vSAN cluster health summary for case description
$cluster = Get-Cluster
$vsanHealth = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$summary = $vsanHealth.QueryVsanClusterHealthSummary(
    $cluster.Id, $null, $null, $true, $null, $null, "defaultView")
Write-Host "Overall vSAN health: $($summary.OverallHealth)"
$summary.Groups | Where-Object { $_.GroupHealth -ne "green" } | ForEach-Object {
    Write-Host "DEGRADED: $($_.GroupName)"
}
```

For SR (Service Request) submission, include the VCF version (from SDDC Manager → Dashboard → Version), the support bundle file URLs, and the PowerCLI output above in the case description.

## TAM and Account Team Escalation

Escalate to your AWS TAM when:
- A P1 production outage has no progress after 4 hours with standard AWS Support.
- There is a risk of data loss (vSAN objects inaccessible, host with encrypted datastores unrecoverable).
- The issue spans both AWS and VMware and neither vendor is making progress.
- A scheduled maintenance window is at risk and business impact is imminent.

```bash
# Set severity to Critical via AWS Support console
# Support → Cases → Open case → Severity: Critical (Business-impacting)
# OR via AWS Support API:
aws support create-case \
  --subject "EVS Production Cluster Outage - Environment $ENV_ID" \
  --service-code "aws-elastic-vmware-service" \
  --severity-code "critical" \
  --category-code "general-guidance" \
  --communication-body "Environment ID: $ENV_ID
Host IDs: <list>
Issue: <description>
Impact: Production workloads unavailable since <timestamp>
Steps taken: <what has been tried>

CloudTrail export attached. EC2 instance status attached."
```

Expected response times by support tier:

| Plan | Critical | High | Medium |
|---|---|---|---|
| Enterprise | 15 minutes (24/7 phone) | 1 hour | 4 hours |
| Business | 1 hour (24/7 phone for critical) | 4 hours | 12 hours |
| Developer | Not available | Not available | 12 business hours |

Enterprise Support is required for EVS production. Business Support is the minimum for non-production. Developer Support has no SLA for infrastructure issues.

To request TAM engagement on an existing case, add a case correspondence explicitly asking for TAM review: "Requesting TAM review — P1 production outage with no resolution progress in 4 hours." Your TAM will join the case within 30 minutes during business hours or can be reached directly by phone.

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

## Post-Incident Review

After any P1 or P2 EVS incident, conduct a post-incident review before closing the support case.

Steps for post-incident review:
1. Document the full timeline: when the issue started, when it was detected, when each diagnostic step was taken, when resolution was achieved.
2. Identify the root cause using a 5-why analysis. Ask "why did this happen?" five times to reach the underlying systemic cause rather than the proximate cause.
3. Request the Root Cause Analysis (RCA) document from AWS and/or VMware. AWS Enterprise Support provides formal RCA documents for P1 incidents. VMware/Broadcom provides these for Critical SRs with data loss risk.
4. Document corrective actions: what changes to monitoring, runbooks, or architecture will prevent recurrence.
5. Add the timeline, root cause, and corrective actions to the team runbook for this issue category.

```text
RCA document request (add to support case correspondence):

"Please provide a formal Root Cause Analysis document for this incident.
Include:
- Timeline of events on the AWS/VMware infrastructure side
- Root cause of the failure
- AWS/VMware corrective actions taken or planned
- Recommended customer-side preventive measures

This is required for our internal post-incident review process."
```

For recurring issues (same root cause appearing more than once), escalate to your AWS TAM and request a Well-Architected Review for your EVS environment. AWS offers a focused EVS review that covers resiliency, networking, and operations best practices.
