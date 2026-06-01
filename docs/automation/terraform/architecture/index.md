# Terraform — Architecture

<div class="kb-summary">
Declarative IaC tool with Go provider plugins for 1000+ APIs; single CLI binary drives init/plan/apply/destroy workflow; remote state backend with locking prevents concurrent mutations; modules package reusable infrastructure components.
</div>

```
┌────────────────────────────────────── Terraform — Architecture ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Terraform architecture: CLI + core + provider plugins + remote state backend + target API   │   │
│   │     Execution: CLI parses HCL → builds dependency graph → calls provider APIs in parallel     │   │
│   │   Remote state: S3 bucket (versioned) + DynamoDB table (state lock) is the standard pattern   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 How It Works                 │  │               Design Standards              │   │
│   │         HCL parsed → resource graph          │  │         One module per resource type        │   │
│   │      Provider downloaded (.terraform/)       │  │        Remote state always (no local)       │   │
│   │          State read + plan computed          │  │            Pin provider versions            │   │
│   │        Provider API calls in parallel        │  │         Separate state per workspace        │   │
│   │          State updated after apply           │  │       Approved plan before apply (CI)       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Physical: Terraform runs on CI runner or workstation; provider communicates with target APIs │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── Terraform — Architecture ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Terraform architecture: CLI + core + provider plugins + remote state backend + target API   │   │
│   │     Execution: CLI parses HCL → builds dependency graph → calls provider APIs in parallel     │   │
│   │   Remote state: S3 bucket (versioned) + DynamoDB table (state lock) is the standard pattern   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 How It Works                 │  │               Design Standards              │   │
│   │         HCL parsed → resource graph          │  │         One module per resource type        │   │
│   │      Provider downloaded (.terraform/)       │  │        Remote state always (no local)       │   │
│   │          State read + plan computed          │  │            Pin provider versions            │   │
│   │        Provider API calls in parallel        │  │         Separate state per workspace        │   │
│   │          State updated after apply           │  │       Approved plan before apply (CI)       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Physical: Terraform runs on CI runner or workstation; provider communicates with target APIs │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Terraform Architecture](../../../assets/terraform-architecture-overview.svg)

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


