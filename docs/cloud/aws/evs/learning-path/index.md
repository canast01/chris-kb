---
tags:
  - aws
  - learning-path
---
# Amazon EVS — Learning Path

<div class="kb-summary">
Recommended reading order for Amazon Elastic VMware Service (EVS). Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Amazon EVS*
</div>

```d2
direction: right

S1: "Architecture" {shape: rectangle}
S2: "Deploy" {shape: rectangle}
S3: "Operations" {shape: rectangle}
S4: "Security" {shape: rectangle}
S5: "Troubleshoot" {shape: rectangle}

S1 -> S2
S2 -> S3
S3 -> S4
S4 -> S5
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | Bare-metal host model, VPC integration, VCF stack | 4–6 h |
| 2 — Deployment | EVS provisioning, VCF bring-up | 3–4 h |
| 3 — Operations | Cluster health, workload management, CLI | ongoing |
| 4 — Security | IAM + vCenter SSO, encryption, hardening | 3 h |
| 5 — Troubleshooting | Multi-layer isolation, AWS + VMware tooling | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand how Amazon EVS maps VCF components onto dedicated i4i.metal hosts inside a customer VPC, and what that means for networking and control-plane access.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — dedicated bare-metal host model, ENI attachment for management and vSAN, and the full VCF software stack (vCenter, NSX, SDDC Manager) running on EVS
- [Design Standards](../architecture/design-standards/) — host sizing for i4i.metal, cluster topology and failure domains, NSX segment design for workload isolation, and SDDC Manager placement in the management cluster
- [Integrations](../architecture/integrations/) — Direct Connect for on-premises network extension, VPC peering to native AWS services (S3, RDS, EKS), and the AWS Console provisioning path via the EVS API

**Key concepts before moving on**:

- Each i4i.metal host runs ESXi and contributes CPU, RAM, and NVMe storage to vSAN — there is no shared SAN
- Management traffic (vCenter, NSX, SDDC Manager) flows over dedicated ENIs attached to the host; workload traffic uses a separate ENI
- EVS VPCs must not overlap with on-premises CIDRs extended via Direct Connect — plan IP addressing before provisioning
- NSX on EVS uses the same control plane as on-premises NSX; policy objects are compatible

**Why first**: EVS sits at the intersection of VMware and AWS networking. A clear architecture picture prevents misrouted traffic, misplaced VLANs, and broken vCenter access from day one.

---

## Stage 2 — Deployment

**Goal**: Follow the correct provisioning sequence for an EVS environment without breaking host connectivity or the VCF bring-up wizard.

**Read**:

- [Deploy](../deploy/) — EVS environment creation via the AWS console, initial host ordering and allocation, VPC subnet readiness checklist, and the VCF bring-up configuration file
- [Install & Upgrade](../operations/install-upgrade/) — VCF lifecycle manager (LCM) upgrade bundles, ESXi patch application via SDDC Manager, and NSX appliance upgrade sequence

**Deployment principles**:

- Pre-create all VPC subnets and route tables before requesting EVS hosts — the bring-up wizard validates connectivity at start
- Run the VCF bring-up checklist offline first; failed bring-ups require full re-provisioning
- Reserve a management CIDR that will not conflict with future Direct Connect or Transit Gateway attachments

---

## Stage 3 — Operations

**Goal**: Maintain EVS cluster health, manage workload placement, and keep the VCF control plane operational on every shift.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; vCenter cluster status, vSAN health summary, NSX transport node state, and host hardware alarms in ESXi
- [CLI Reference](../operations/cli-reference/) — `aws evs` CLI commands for environment management, PowerCLI for VM operations, NSX-T Policy API calls, and `esxcli` for host-level diagnostics
- [Procedures](../operations/procedures/) — host replacement (add new, evacuate, remove old), cluster scale-out, workload migration from EVS to native AWS services, and SDDC Manager task monitoring
- [Backup & Restore](../operations/backup-restore/) — vCenter VAMI scheduled backup to S3, NSX configuration export, SDDC Manager backup configuration, and restoration verification steps
- [Scripts](../operations/scripts/) — host health polling script, vSAN datastore capacity alerting, AWS tag synchronisation from VM attributes, and SDDC Manager task status reporter

**Daily rhythm**: vCenter health → vSAN health → NSX transport node status → EVS environment events in AWS console.

---

## Stage 4 — Security

**Goal**: Enforce access boundaries between the VMware control plane and the surrounding AWS account, and protect management traffic.

**Read**:

- [Access Control](../security/access-control/) — IAM roles for EVS API operations, vCenter SSO group mapping to roles, NSX role-based access (auditor vs operator vs admin), and SDDC Manager user permissions
- [Authentication](../security/authentication/) — vCenter SSO federation with IAM Identity Center (SAML), MFA enforcement for vCenter and SDDC Manager UIs, and certificate-based API authentication
- [Encryption](../security/encryption/) — vSAN data-at-rest encryption with HCI mesh key provider, TLS enforcement for vCenter and NSX API endpoints, and ESXi host certificate management
- [Hardening](../security/hardening/) — security group rules for management ENIs (limit to bastion/jump host CIDRs), ESXi lockdown mode configuration, audit log forwarding to CloudWatch Logs, and vCenter alarm on failed logins

---

## Stage 5 — Troubleshooting

**Goal**: Isolate failures in EVS across the AWS infrastructure layer, the VMware control plane, and the guest workload layer.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — host disconnected from vCenter (MTU mismatch or security group), NSX transport node degraded (BFD session loss), VPC routing broken for EVS management subnets, and vSAN health alarm
- [Diagnostics](../troubleshooting/diagnostics/) — VPC Flow Logs on EVS ENIs for dropped traffic, vCenter events and tasks view, NSX intelligence traceflow for East-West packet trace, and `esxcli network` for host-side NIC diagnostics
- [Escalation](../troubleshooting/escalation/) — AWS Support for EVS infrastructure issues (host hardware, ENI, VPC), VMware GSS engagement for VCF software bugs (routed through AWS Support for EVS customers), and severity criteria for both

**Why last**: Troubleshooting makes most sense once you know the expected data-plane topology and what healthy vCenter, vSAN, and NSX telemetry looks like.

---

## See also

- [Evs — Deploy](../../deploy/)
- [Evs — Procedures](../../operations/procedures/)
- [Evs — Common Issues](../../troubleshooting/common-issues/)
