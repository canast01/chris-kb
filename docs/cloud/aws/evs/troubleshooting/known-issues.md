---
tags:
  - troubleshooting
  - aws-evs
  - aws
  - vmware
  - known-issues
---
# AWS Elastic VMware Service (EVS) — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known AWS EVS bugs and workarounds. EVS runs VMware vSphere, vSAN, and NSX on AWS bare-metal — issues may be at the AWS control plane layer or within the VMware layer running on top.

*Applies to: AWS EVS (GA 2025)*
</div>

```text
┌───────────────────────────────────── AWS Elastic VMware Service ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                   VCF running on AWS bare-metal hosts inside a customer VPC                   │   │
│   │              Protocols: HTTPS (AWS API) · vSphere/NSX mgmt protocols on EVS hosts             │   │
│   │             Management: AWS Console/CLI (EVS) + vCenter/NSX Manager (VMware layer)            │   │
│   │              AWS API provision -> Bare-metal hosts -> VCF bring-up -> vCenter/NSX             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │        Control (AWS)        │  │       EVS service API       │  │   Bare-metal+VPC provision  │   │
│   │        Control (VMw)        │  │      vCenter / NSX Mgr      │  │     Runs inside EVS env     │   │
│   │           Compute           │  │     i4i bare-metal hosts    │  │    Dedicated, not shared    │   │
│   │           Network           │  │         VPC + DX/VPN        │  │     Connects to on-prem     │   │
│   │           Storage           │  │      vSAN on EVS hosts      │  │     Same vSAN as on-prem    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │     EVS API      │Cluster lifecycle │       HTTPS       │       IAM        │AWS-native control│   │
│   │  vCenter (EVS)   │   VMware mgmt    │       HTTPS       │       SSO        │ Same as on-prem  │   │
│   │  NSX Mgr (EVS)   │Net. virtualizatn │       HTTPS       │    Local/LDAP    │ Same as on-prem  │   │
│   │      DX/VPN      │  Connect to EVS  │   IPsec/private   │       N/A        │Needed for hybrid │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: AWS i4i.metal hosts in an AWS AZ - customer VPC - Direct Connect/VPN                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  EVS            = Elastic VMware Service; AWS-managed bare-metal hosts running VCF                    │
│  i4i.metal      = AWS bare-metal instance type used as EVS host hardware                              │
│  VCF            = VMware Cloud Foundation; the SDDC stack EVS deploys on AWS                          │
│  VPC            = Virtual Private Cloud; the AWS network EVS hosts live in                            │
│  Direct Connect = dedicated private network link from on-prem to AWS                                  │
│  AWS Health Dash.= service status page; check before assuming a bug                                   │
│  Bring-up       = initial VCF deployment process onto EVS bare-metal hosts                            │
│  Workload domain= VCF logical grouping of clusters for a given purpose                                │
│  SDDC Manager   = VCF lifecycle/orchestration component, present on EVS too                           │
│  Security group = AWS-level firewall controlling traffic to/from EVS hosts                            │
│  vSAN ports     = UDP 12345/12346 used for vSAN traffic between ESXi hosts                            │
│  GA (2025)      = EVS reached General Availability in 2025                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- AWS EVS control plane issues: check AWS Health Dashboard and `evs.<region>.amazonaws.com` API.
- VMware layer issues (vCenter, vSAN, NSX errors): refer to respective VMware known-issues pages.
- EVS security group misconfigurations are the most common networking issue.

## AWS Control Plane

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| EVS cluster creation failing: `InsufficientCapacity` | EVS GA | i4i bare-metal capacity unavailable in requested AZ | Try different AZ; contact AWS sales for reserved capacity | N/A |
| EVS API returning `ServiceUnavailableException` | EVS GA | Transient AWS EVS control plane issue | Retry with exponential backoff; check AWS Health Dashboard | N/A |

## Networking

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Cannot reach vCenter after EVS deployment | EVS GA | VPN/Direct Connect not established; or security group blocking 443 | Verify DX/VPN connectivity; check EVS management VPC security group allows 443 from admin IPs | N/A |
| vSAN traffic degraded in EVS | EVS GA | EVS security group not allowing UDP 12345/12346 between ESXi hosts | Update EVS security group to allow vSAN ports between ESXi management IPs | N/A |

## VMware Layer

For VMware-specific issues within EVS, refer to:
- [VMware vCenter — Known Issues](../../../../virtualization/vmware/vcenter/troubleshooting/known-issues/)
- [VMware vSAN — Known Issues](../../../../virtualization/vmware/vsan/troubleshooting/known-issues/)
- [VMware NSX — Known Issues](../../../../virtualization/vmware/nsx/troubleshooting/known-issues/)

## See also

- [AWS EVS — Common Issues](common-issues/)
- [AWS — Known Issues](../../troubleshooting/known-issues.md)
