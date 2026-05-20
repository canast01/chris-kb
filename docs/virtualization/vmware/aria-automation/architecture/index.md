# Aria Automation — Architecture

<div class="kb-summary">
Kubernetes-based microservices platform for infrastructure self-service automation. Cloud templates (YAML IaC) define resources declaratively; Aria Automation resolves placement and orchestrates provisioning across vSphere, NSX, and public cloud.
</div>

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

## Cluster Topology

```
┌─────────────────────────────────── Aria Automation — Architecture ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Aria Automation = Automation appliance + Service Broker + Assembler + Extensibility (ABX +  │   │
│   │      Service Broker provides self-service catalog with entitlements and approval policies     │   │
│   │   Assembler manages blueprints, cloud accounts, and cloud zones for multi-cloud provisioning  │   │
│   │  ABX actions and embedded Orchestrator extend automation with custom functions and workflows  │   │
│   │ Connects to cloud accounts: vCenter, AWS, Azure, GCP; cloud proxy for on-premises connectivity│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines platform components · integrations connect cloud accounts                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │     Automation appliance    │  │      vCenter cloud acct     │  │       Org/project RBAC      │   │
│   │   Service Broker: catalog   │  │      GitHub/GitLab: IaC     │  │     Blueprint versioning    │   │
│   │    Assembler: blueprints    │  │       ServiceNow ITSM       │  │       Naming standards      │   │
│   │      ABX: extensibility     │  │         AD/LDAP auth        │  │      ABX action limits      │   │
│   │     Orchestrator: embed     │  │       Terraform plugin      │  │      Approval policies      │   │
│   │        Cloud accounts       │  │      Slack/Teams notify     │  │         Cloud zones         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    How-it-works covers platform components · integrations connect cloud and ITSM                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   How It Works   │   Integrations   │    Design Stds    │    Deployment    │     Key Stds     │   │
│   │  Service Broker  │   vCenter acct   │   Org/proj RBAC   │   Single-node    │  Blueprint std   │   │
│   │    Assembler     │    GitHub IaC    │   Blueprint ver   │    HA cluster    │   Naming conv    │   │
│   │   ABX actions    │    ServiceNow    │  Approval policy  │   Cloud proxy    │    ABX limits    │   │
│   │   Orchestrator   │    Terraform     │    Cloud zones    │   Multi-cloud    │  Secret policy   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (Automation appliance) · RAM DIMMs · Network NICs · vCenter/cloud provider targets            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Service Broker = Aria Automation self-service catalog; manages entitlements and approval workflows   │
│  Assembler     = Aria Automation design surface; creates blueprints and manages cloud accounts/zones  │
│  ABX (Action Based Extensibility) = FaaS runtime for Python/Node/PowerShell custom actions            │
│  Orchestrator  = vRO embedded in Aria Automation; runs complex multi-step workflows                   │
│  Blueprint     = IaC template in Aria YAML; defines cloud-agnostic infrastructure topology            │
│  Cloud account = Aria connection to a cloud endpoint: vCenter, AWS, Azure, or GCP                     │
│  Cloud zone    = Subset of a cloud account resources (clusters, regions) available for provisioning   │
│  Catalog item  = Published blueprint or Orchestrator workflow available in Service Broker             │
│  Entitlement   = Policy granting a project/user access to specific catalog items in Service Broker    │
│  Approval policy = Workflow requiring approver sign-off before catalog item request is fulfilled      │
│  Cloud proxy   = Lightweight VM deployed on-premises; routes Aria SaaS traffic to vCenter             │
│  Organization/Project = Org is top-level tenant; Project scopes users, cloud zones, and policies      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
