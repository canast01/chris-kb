---
tags:
  - architecture
  - aria-automation
  - vmware
---
# Aria Automation — Architecture

<div class="kb-summary">
Kubernetes-based microservices platform for infrastructure self-service automation. Cloud templates (YAML IaC) define resources declaratively; Aria Automation resolves placement and orchestrates provisioning across vSphere, NSX, and public cloud.

*Applies to: Aria Automation 8.x*
</div>

```text
┌─────────────────────────── Aria Automation Architecture — Self-Service IaC ───────────────────────────┐
│                                                                                                       │
│  Kubernetes-based microservices; cloud templates (YAML IaC) declaratively define                      │
│  resources; Aria Automation resolves placement across vSphere, NSX, public cloud.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Platform Architecture             │  │             Cloud Template (IaC)            │   │
│   │         K8s microservices in vSphere         │  │         YAML declarative definition         │   │
│   │      Services: catalog, blueprint, k8s       │  │    Resource types: Cloud.vSphere.Machine    │   │
│   │           Embedded NSX integration           │  │        Constraints: tag/cloud/region        │   │
│   │         PostgreSQL + MinIO for data          │  │         Versioned in Service Catalog        │   │
│   │        Multi-tenant: projects + orgs         │  │        Input params: consumer choices       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cloud templates compile to deployments; day-2 actions run via Action-Based Ext.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Integrations                 │  │                Orchestration                │   │
│   │           vCenter: VM provisioning           │  │        ABX: serverless action scripts       │   │
│   │            NSX: network on-demand            │  │       Orchestrator: complex workflows       │   │
│   │         AWS/Azure/GCP: public cloud          │  │         Pipelines: CI/CD integration        │   │
│   │        ServiceNow: ITSM ticket-driven        │  │        Git: template version control        │   │
│   │          IPAM: Infoblox or internal          │  │       Notification: Slack/email hooks       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  3–4 VM cluster running embedded Kubernetes; vSphere 7+ required; 16 vCPU                             │
│  / 40 GB RAM per node minimum; PostgreSQL data on shared storage.                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cloud template  = YAML IaC file defining a deployable set of resources                               │
│  Deployment      = running instance created from a cloud template                                     │
│  Service Catalog = portal where users request templates; RBAC-gated                                   │
│  Project         = multi-tenancy unit; controls which clouds + users can access                       │
│  ABX             = Action-Based Extensibility; serverless scripts (Python/JS/PS)                      │
│  Orchestrator    = workflow engine; complex multi-step automation                                     │
│  Constraint      = placement rule; tag, cloud, or availability zone filter                            │
│  Day-2 action    = post-deployment operation; resize, snapshot, power actions                         │
│  Pipeline        = CI/CD; build-test-deploy chain triggered by Git events                             │
│  IPAM            = IP Address Manager; external integration for IP allocation                         │
│  Input param     = consumer-visible variable in template; dropdown or text                            │
│  MinIO           = S3-compatible object store; artifact storage in Aria Automation                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Aria Automation Architecture](../../../../assets/aria-automation-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with vCenter, NSX, cloud providers, and external tools.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, HA design, and configuration best practices.</span></a>
</div>

## Deployment Models

| Model | Description |
|---|---|
| SaaS (Cloud) | VMware-hosted; no infrastructure to manage; connected via cloud extensibility proxy |
| On-Premises | 1 or 3 appliance cluster; self-managed; supports air-gap environments |

