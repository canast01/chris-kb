# Terraform

<div class="kb-summary">
Terraform infrastructure-as-code knowledge base covering provider plugin architecture, state backend configuration, workspace model, module design, CI/CD integration, and troubleshooting for multi-cloud and on-premises environments.
</div>

```
┌───────────────────────────────── Terraform — Infrastructure as Code ──────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Terraform: HashiCorp IaC tool; declares resources in HCL; plan → apply workflow        │   │
│   │    Provider plugins: AWS, Azure, GCP, VMware, NetApp, Kubernetes — one binary per provider    │   │
│   │  State: JSON file tracking actual resource state; stored in S3 + DynamoDB or Terraform Cloud  │   │
│   │      Modules: reusable resource groups; internal registry or Terraform Registry (public)      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │       HCL + providers       │  │    Plan / apply / destroy   │  │       State encryption      │   │
│   │        State backend        │  │     Workspace management    │  │        Remote backend       │   │
│   │        Module design        │  │    Import existing infra    │  │      Sentinel policies      │   │
│   │       Dependency graph      │  │       State operations      │  │     Least-privilege auth    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    HCL         = HashiCorp Configuration Language; declarative, JSON-compatible; .tf files    │   │
│   │   Provider    = plugin implementing CRUD operations for a platform API (AWS, vSphere, etc.)   │   │
│   │       State file  = terraform.tfstate; maps resource configs to real-world resource IDs       │   │
│   │  Plan        = terraform plan; shows what will be created/modified/destroyed; no changes made │   │
│   │      Apply       = terraform apply; executes the plan after confirmation or -auto-approve     │   │
│   │     Module      = encapsulated resource group with inputs/outputs; reusable across configs    │   │
│   │         Workspace   = isolated state environment; prod/staging/dev within same config         │   │
│   │  Backend     = remote state storage; S3+DynamoDB (locking), GCS, Terraform Cloud, Azure Blob  │   │
│   │ Sentinel    = policy-as-code; Terraform Cloud/Enterprise; enforce tagging, region, cost limits│   │
│   │     Data source = reads existing infrastructure without managing it; e.g. aws_ami, aws_vpc    │   │
│   │      Output      = exported values from a module or root config; passed to other configs      │   │
│   │       Variable    = parameterised input; .tfvars file, env var TF_VAR_name, or -var flag      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────── Terraform — Infrastructure as Code ──────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Terraform: HashiCorp IaC tool; declares resources in HCL; plan → apply workflow        │   │
│   │    Provider plugins: AWS, Azure, GCP, VMware, NetApp, Kubernetes — one binary per provider    │   │
│   │  State: JSON file tracking actual resource state; stored in S3 + DynamoDB or Terraform Cloud  │   │
│   │      Modules: reusable resource groups; internal registry or Terraform Registry (public)      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │       HCL + providers       │  │    Plan / apply / destroy   │  │       State encryption      │   │
│   │        State backend        │  │     Workspace management    │  │        Remote backend       │   │
│   │        Module design        │  │    Import existing infra    │  │      Sentinel policies      │   │
│   │       Dependency graph      │  │       State operations      │  │     Least-privilege auth    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    HCL         = HashiCorp Configuration Language; declarative, JSON-compatible; .tf files    │   │
│   │   Provider    = plugin implementing CRUD operations for a platform API (AWS, vSphere, etc.)   │   │
│   │       State file  = terraform.tfstate; maps resource configs to real-world resource IDs       │   │
│   │  Plan        = terraform plan; shows what will be created/modified/destroyed; no changes made │   │
│   │      Apply       = terraform apply; executes the plan after confirmation or -auto-approve     │   │
│   │     Module      = encapsulated resource group with inputs/outputs; reusable across configs    │   │
│   │         Workspace   = isolated state environment; prod/staging/dev within same config         │   │
│   │  Backend     = remote state storage; S3+DynamoDB (locking), GCS, Terraform Cloud, Azure Blob  │   │
│   │ Sentinel    = policy-as-code; Terraform Cloud/Enterprise; enforce tagging, region, cost limits│   │
│   │     Data source = reads existing infrastructure without managing it; e.g. aws_ami, aws_vpc    │   │
│   │      Output      = exported values from a module or root config; passed to other configs      │   │
│   │       Variable    = parameterised input; .tfvars file, env var TF_VAR_name, or -var flag      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, scripts, procedures, and state management.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, secrets, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
