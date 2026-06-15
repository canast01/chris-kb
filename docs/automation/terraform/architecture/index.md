---
tags:
  - architecture
  - terraform
---
# Terraform — Architecture

<div class="kb-summary">
Declarative IaC tool with Go provider plugins for 1000+ APIs; single CLI binary drives init/plan/apply/destroy workflow; remote state backend with locking prevents concurrent mutations; modules package reusable infrastructure components.

*Applies to: Terraform 1.x*
</div>

```text
┌────────────────────────────── Terraform Architecture — Declarative IaC ───────────────────────────────┐
│                                                                                                       │
│  Declarative IaC: Go provider plugins wrap 1000+ APIs; single CLI binary drives                       │
│  init/plan/apply/destroy; remote state + locking prevents concurrent mutations.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Core Workflow                 │  │               Provider Plugins              │   │
│   │      init: download providers + modules      │  │            Go binary per provider           │   │
│   │         plan: diff desired vs state          │  │       Registry: registry.terraform.io       │   │
│   │         apply: create/update/delete          │  │          Pinned: required_providers         │   │
│   │        destroy: tear down all managed        │  │        aws, azurerm, google, vsphere        │   │
│   │         fmt + validate: code hygiene         │  │        Custom: internal provider SDK        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Plan shows additions/changes/deletions before apply; review before confirming.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               State Management               │  │                   Modules                   │   │
│   │       terraform.tfstate: resource map        │  │       Package reusable infra patterns       │   │
│   │        Remote backend: S3, GCS, Azure        │  │        source: local or registry URL        │   │
│   │         Locking: DynamoDB / S3 lease         │  │        version: pinned in module call       │   │
│   │       Workspaces: isolated state sets        │  │          Input vars + output values         │   │
│   │      import: onboard existing resources      │  │           for_each/count: fan-out           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Workstation or CI runner with terraform binary; remote backend: cloud storage                        │
│  bucket + DynamoDB table for locking; network to target API endpoints.                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HCL           = HashiCorp Configuration Language; declarative config syntax                          │
│  Provider      = Go plugin wrapping a target API; versioned independently                             │
│  Resource      = managed infra object; tracked in state file                                          │
│  Data source   = read-only query of external data; not managed in state                               │
│  State file    = JSON map of real resource IDs to Terraform config                                    │
│  Remote backend= cloud storage for state; enables team collaboration                                  │
│  Workspace     = isolated state within one config; dev/staging/prod                                   │
│  Module        = reusable .tf files with input vars and output values                                 │
│  for_each      = create multiple resource instances from a map/set                                    │
│  depends_on    = explicit dependency override; use when implicit fails                                │
│  Locking       = prevents concurrent apply; DynamoDB with S3 backend                                  │
│  import        = bring existing resource under Terraform management                                   │
│                                                                                                       │
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

