---
tags:
  - architecture
  - aria-automation
  - vmware
---
# Aria Automation — Standards


<div class="kb-summary">
Standards reference covering Naming Conventions, Build Baseline, Configuration Checklist, Blueprint / Template Standards, Project Standards and 1 more sections.
</div>

```text
┌───────────────────────────────── Aria Automation — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│  Design patterns for projects, templates, naming, and governance in Aria Automation.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Project & Naming Standards          │  │          Template Design Standards          │   │
│   │       One project per team/BU/env tier       │  │     Inputs: only required params exposed    │   │
│   │       Naming: env-team-purpose pattern       │  │      Constraints: machine.count limits      │   │
│   │        Cloud zones linked per project        │  │    Versioning: major for breaking changes   │   │
│   │       Quotas: CPU/memory/storage caps        │  │       No hardcoded IPs or credentials       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Governance standards enforce consistent tagging, approvals, and lifecycle management.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Governance Standards             │  │           Extensibility Standards           │   │
│   │     Approval policies for all prod items     │  │     ABX actions in version control (Git)    │   │
│   │    Cost policies: budget alerts per proj     │  │     Orchestrator workflows tested in dev    │   │
│   │       Lease policies: auto-expire VMs        │  │     No inline scripts in cloud templates    │   │
│   │        Mandatory tags: env/owner/team        │  │      ABX: separate actions per concern      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance cluster · vCenter · NSX-T · AD · Git for IaC and action source control                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cloud zone        = Placement policy linking a project to a vCenter cluster or cloud region          │
│  Quota             = Resource limit (CPU/mem/storage count) enforced per project in vRA               │
│  Lease policy      = Expiry rule: deployments auto-deleted or sent for approval after N days          │
│  Approval policy   = Governance workflow requiring authoriser sign-off before provisioning            │
│  Cost policy       = Budget threshold triggering alert or block when project spend exceeds limit      │
│  Template version  = Immutable snapshot of a cloud template; major versions break consumers           │
│  Constraint tag    = vRA tag applied to a resource (cluster/datastore) to control placement           │
│  Input property    = Template parameter exposed to consumer at request time (dropdown/free text)      │
│  ABX source control= Git repo storing ABX action code; imported via vRA integration setting           │
│  No inline scripts = Design rule: scripts belong in ABX actions, not cloudConfig/customisation        │
│  Naming convention = Consistent env-team-role-seq pattern for VMs, networks, and deployments          │
│  Mandatory tag     = Tag enforced by lease/approval policy; deployment blocked without it             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Naming Conventions

| Object | Convention | Example |
|--------|-----------|---------|
| Appliance node | `aria-auto-<site>-<nn>` | `aria-auto-dc1-01` |
| Load balancer VIP | `aria-auto-<site>-vip` | `aria-auto-dc1-vip` |
| Cloud account (vCenter) | `<vcenter-shortname>` | `vcsa-prod` |
| Cloud account (cloud) | `<provider>-<account>-<region>` | `aws-prod-eu-west-1` |
| Project | `<team>-<env>` | `platform-prod` |
| Blueprint / template | `<service>-<os>-<version>` | `web-ubuntu22-v1` |

---

## Build Baseline

### Appliance Requirements

| Deployment | Nodes | vCPU | RAM | Disk |
|-----------|-------|------|-----|------|
| Single-node (non-prod) | 1 | 8 | 32 GB | 300 GB |
| 3-node cluster (prod) | 3 | 8 | 32 GB | 300 GB each |

### Required Infrastructure

- DNS A records and reverse PTR for all nodes and VIP
- NTP configured (drift < 1 second within cluster)
- Load balancer VIP (production 3-node only)
- CA-signed TLS certificate for VIP/FQDN
- vCenter service account with appropriate cloud account permissions
- NSX service account with manager role (if NSX cloud account used)
- AD/LDAP group mapped to Aria Automation roles

---

## Configuration Checklist

### Pre-deployment

- [ ] DNS and NTP verified
- [ ] vCenter service account created
- [ ] NSX service account created (if NSX cloud account required)
- [ ] Load balancer VIP configured (3-node)
- [ ] TLS certificate issued for VIP FQDN
- [ ] AD groups documented for role mapping

### Post-deployment

- [ ] Cloud accounts healthy (vCenter, NSX) — green status in Infrastructure > Connections
- [ ] Projects created with correct cloud zones and naming prefixes
- [ ] AD/LDAP auth configured and tested
- [ ] At minimum one blueprint/template deployed end-to-end
- [ ] Approval policies configured for production project
- [ ] Pipeline integration (GitHub/GitLab) tested if Pipelines is in use
- [ ] Backup of appliance VMs configured

---

## Blueprint / Template Standards

- Use **Cloud Agnostic machine** type where possible to maintain portability.
- Store blueprint YAML in Git and use Pipelines or sync to Assembler.
- Version blueprints using semantic versioning in the name: `v1`, `v2`.
- Use **input variables** for all environment-specific values (CPU, memory, network, storage).
- Apply **constraints** (tag-based) to control placement rather than hardcoding cloud zones.

---

## Project Standards

- Each team/BU owns one or more **Projects**.
- Cloud zones are assigned per project to enforce placement boundaries.
- Apply a **naming prefix** in the project to enforce VM naming convention.
- Set memory and CPU **quota limits** per project for cost control.

---

## Related Sections

- [Architecture](index.md) — cluster topology
- [Security](../security/index.md) — RBAC and project-based access
- [Operations](../operations/index.md) — health checks

## See also

- [Aria Automation — How It Works](how-it-works/)
- [Aria Automation — Deploy](../deploy/)
