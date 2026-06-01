# Automation

<div class="kb-summary">
Automation reference: Ansible, PowerShell, Python, Terraform, and 1 more.
</div>

```
┌──────────────────────────── Automation — Infrastructure Automation Tools ─────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Automation: codifying repeatable infra operations into executable, version-controlled logic  │   │
│   │     Goals: eliminate manual error, enforce consistency, accelerate delivery, self-service     │   │
│   │   Tools: Ansible (config mgmt), Terraform (IaC), GitHub Actions (CI/CD), PowerShell, Python   │   │
│   │    Maturity path: manual → scripted → idempotent config mgmt → full IaC with pipeline gates   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Configuration Management           │  │            Infrastructure as Code           │   │
│   │         Ansible: agentless SSH/WinRM         │  │          Terraform: declarative HCL         │   │
│   │       Playbooks → roles → collections        │  │        Plan → apply → state tracking        │   │
│   │      AWX/AAP: enterprise control plane       │  │      Multi-cloud and on-prem providers      │   │
│   │          Idempotent: safe to re-run          │  │      Remote state: S3, Terraform Cloud      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               CI/CD Pipelines                │  │             Scripting Languages             │   │
│   │      GitHub Actions: event-driven jobs       │  │     PowerShell: Windows + cross-platform    │   │
│   │    Runners: GitHub-hosted or self-hosted     │  │        Python: scripting, APIs, SDKs        │   │
│   │       Secrets, environments, approvals       │  │          Virtual envs, pip, Poetry          │   │
│   │      Marketplace actions + custom steps      │  │      boto3, paramiko, ansible, requests     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                       Physical Infrastructure (what automation manages):                      │   │
│   │      Bare-metal servers · VMs · containers · cloud VMs · network devices · storage arrays     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Ansible         = agentless configuration management; SSH/WinRM transport; YAML playbooks   │   │
│   │       Terraform       = HashiCorp IaC tool; provider plugins; declarative resource graph      │   │
│   │           GitHub Actions  = native GitHub CI/CD; workflow YAML in .github/workflows/          │   │
│   │    PowerShell      = Microsoft shell and scripting language; .ps1 files; PS7 cross-platform   │   │
│   │  Python          = general-purpose language; dominant for infra scripting and API automation  │   │
│   │     Idempotent      = running the same automation multiple times produces the same result     │   │
│   │     AWX / AAP       = Ansible Automation Platform; web UI + API + RBAC over Ansible Engine    │   │
│   │     IaC             = Infrastructure as Code; resources declared in files, tracked in git     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="ansible/"><strong>Ansible</strong><span>Inventory, playbooks, roles, variables, vault, and infrastructure automation.</span></a>
<a class="kb-card" href="powershell/"><strong>PowerShell</strong><span>Scripts, modules, remoting, reporting, and Windows/VMware automation.</span></a>
<a class="kb-card" href="python/"><strong>Python</strong><span>Scripts, REST API clients, parsing, reporting, and cross-platform automation.</span></a>
<a class="kb-card" href="terraform/"><strong>Terraform</strong><span>State management, modules, plans, applies, drift detection, and provider config.</span></a>
<a class="kb-card" href="github-actions/"><strong>GitHub Actions</strong><span>Workflows, CI/CD pipelines, validation, publishing, and secret management.</span></a>
</div>
