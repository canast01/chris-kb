# Terraform — Architecture

<div class="kb-summary">
Declarative IaC tool with Go provider plugins for 1000+ APIs; single CLI binary drives init/plan/apply/destroy workflow; remote state backend with locking prevents concurrent mutations; modules package reusable infrastructure components.
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>CLI workflow, state backend, provider plugins, workspace model, and module registry.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## State Backends

| Backend | State storage | Locking mechanism | Best for |
|---|---|---|---|
| S3 + DynamoDB | AWS S3 | DynamoDB item | AWS-primary organisations |
| GCS | Google Cloud Storage | GCS object lock | GCP-primary organisations |
| Azure Blob | Azure Storage Account | Blob lease | Azure-primary organisations |
| Terraform Cloud / Enterprise | Hosted | Native | Multi-cloud, managed service |

## High-Level Architecture

```mermaid
flowchart TD
    DEV([Developer / CI Pipeline]) --> CLI[Terraform CLI]
    CLI --> INIT[terraform init\nDownload providers & modules]
    CLI --> PLAN[terraform plan\nGenerate execution plan]
    CLI --> APPLY[terraform apply\nMutate infrastructure]

    INIT --> PR[Provider Registry\nregistry.terraform.io]
    INIT --> MR[Module Registry\nprivate or public]

    PLAN --> STATE[(State Backend\nS3 / GCS / Azure Blob\n/ Terraform Cloud)]
    APPLY --> STATE

    PLAN --> P1[AWS Provider]
    PLAN --> P2[Azure Provider]
    PLAN --> P3[vSphere Provider]

    P1 --> AWS[AWS APIs]
    P2 --> AZ[Azure ARM APIs]
    P3 --> VS[vSphere APIs]

    STATE --> LOCK[State Lock\nDynamoDB / Storage Account]

    style CLI fill:#5c35cc,color:#fff
    style STATE fill:#1565c0,color:#fff
    style LOCK fill:#c62828,color:#fff
```
