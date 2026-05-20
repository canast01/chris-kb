# Aria Automation

<div class="kb-summary">
Technical and operational reference for VMware Aria Automation. Covers infrastructure automation, service catalogue, blueprint design, deployment management, and IaC pipeline integration across the vSphere and cloud platforms.
</div>

```
┌──────────────────────────────────────── Aria Automation Stack ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            VMware Aria Automation — Infrastructure Automation and Service Catalogue           │   │
│   │    Blueprints (templates): IaC definitions for VMs, networks, storage, and cloud resources    │   │
│   │      Service Catalogue: self-service portal for end-users to request approved deployments     │   │
│   │        CAS: Cloud Assembly; where blueprints are designed and cloud accounts connected        │   │
│   │      ABX: Action-Based eXtensibility; serverless functions triggered on deployment events     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Blueprints define desired state · Service Catalogue delivers self-service · ABX extends automation │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │     CAS: cloud accounts     │  │  Blueprint: design+version  │  │  RBAC: org + project roles  │   │
│   │   ABX: serverless actions   │  │  Deployment: manage+delete  │  │   Approval policies: gated  │   │
│   │  Service Broker: catalogue  │  │     Cloud account: sync     │  │  Secrets: integrated vault  │   │
│   │     Pipelines: CI/CD IaC    │  │   Content source: Git/vRO   │  │    Content trust: signed    │   │
│   │   Terraform: IaC provider   │  │   Approval: request+grant   │  │    Audit: deployment log    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines the platform · Operations manage deployments · Security controls access and ap│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │ Deployment fails │vra-support bundle│ Services: running?│   GSS + bundle   │  vra-cli login   │   │
│   │Approval not firin│cloud-account sync│Cloud acct: sync OK│  TAM escalation  │vra-cli get deploy│   │
│   │ Blueprint error  │ ABX action logs  │  ABX: runtime OK? │Collect service lo│vra-cli get bluepr│   │
│   │ Catalogue empty  │content-source syn│Catalogue: publish?│P1: automation dow│vra-cli get reques│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Aria Automation VMs on vSphere cluster · vPostgres DB · NSX network segments · Aria Suite LCM        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Blueprint     = YAML IaC template defining VMs, networks, storage, and cloud resources               │
│  CAS           = Cloud Assembly; blueprint designer and cloud account manager in Aria Automation      │
│  ABX           = Action-Based eXtensibility; serverless functions (Python/JS/PS) on deploy events     │
│  Service Broker= Catalogue front-end; users request approved items from published content sources     │
│  Deployment    = Running instance of a blueprint; tracks provisioned resources and lifecycle          │
│  Cloud Account = vSphere, AWS, Azure, or GCP connection supplying infrastructure endpoints            │
│  Project       = RBAC boundary; groups users and cloud zones; controls blueprint deployment targets   │
│  Content Source= Git repo or vRO connection feeding blueprint content into Service Catalogue          │
│  Approval Policy= Workflow gate before deployment; requires named approver or group sign-off          │
│  vRO           = vRealize Orchestrator; workflow engine integrated with Aria Automation               │
│  Pipeline      = CI/CD pipeline in Aria Automation Pipelines; integrates Git, test, and deploy        │
│  Terraform provider= Aria Automation Terraform service; manages Terraform state and runs plans        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
