# Terraform — How It Works

Terraform is a declarative infrastructure-as-code tool that manages resources across hundreds of providers via a consistent workflow. All execution is driven by a single CLI binary — there are no separate agents.

---

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

    PLAN --> P1[AWS Provider\nterraform-provider-aws]
    PLAN --> P2[Azure Provider\nterraform-provider-azurerm]
    PLAN --> P3[vSphere Provider\nterraform-provider-vsphere]
    PLAN --> P4[Other Providers]

    P1 --> AWS[AWS APIs]
    P2 --> AZ[Azure ARM APIs]
    P3 --> VS[vSphere REST / SOAP APIs]
    P4 --> OTHER[Other Cloud/SaaS APIs]

    STATE --> LOCK[State Lock\nDynamoDB / Storage Account\n/ native backend lock]

    style CLI fill:#5c35cc,color:#fff
    style STATE fill:#1565c0,color:#fff
    style LOCK fill:#c62828,color:#fff
```

---

## Terraform CLI Commands

| Command | Purpose |
|---|---|
| `terraform init` | Initialise working directory: download providers, configure backend |
| `terraform validate` | Check configuration syntax and internal consistency |
| `terraform fmt` | Format `.tf` files to canonical style |
| `terraform plan` | Show changes required to reach desired state |
| `terraform apply` | Apply the plan; mutate real infrastructure |
| `terraform destroy` | Plan and apply deletion of all managed resources |
| `terraform state` | Inspect and manipulate state directly |
| `terraform import` | Import existing resources into state |
| `terraform output` | Print output values from state |
| `terraform workspace` | Manage workspaces |

---

## State Backend

The state file is Terraform's source of truth for what resources it manages. The backend determines where it is stored and how concurrent access is controlled.

| Backend | State storage | Locking mechanism | Best for |
|---|---|---|---|
| S3 + DynamoDB | AWS S3 | DynamoDB item | AWS-primary organisations |
| GCS | Google Cloud Storage | GCS object lock | GCP-primary organisations |
| Azure Blob | Azure Storage Account | Blob lease | Azure-primary organisations |
| Terraform Cloud / Enterprise | Hosted | Native | Multi-cloud, managed service |

```hcl
terraform {
  required_version = ">= 1.7.0"

  backend "s3" {
    bucket         = "my-org-terraform-state"
    key            = "platform/networking/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:eu-west-1:123456789012:key/mrk-abc123"
    dynamodb_table = "terraform-state-lock"
  }
}
```

---

## Workspace Model

Workspaces allow multiple independent state files within the same backend path. Suited for lightweight environment separation (dev/staging/prod).

```bash
terraform workspace list
terraform workspace new staging
terraform workspace select prod
```

For strict isolation (separate AWS accounts, different permissions), use separate root modules with separate backends rather than workspaces.

---

## Provider Plugin Architecture

Providers are separate binaries (Go plugins) downloaded by `terraform init`. Terraform communicates with providers over a local gRPC socket.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
    vsphere = {
      source  = "hashicorp/vsphere"
      version = "~> 2.7"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
  use_oidc = true
}
```

---

## Module Registry

| Source | Example |
|---|---|
| Terraform Registry (public) | `source = "terraform-aws-modules/vpc/aws"` |
| Private registry | `source = "app.terraform.io/myorg/vpc/aws"` |
| Git | `source = "git::https://github.com/org/tf-modules.git//vpc?ref=v2.0.0"` |
| Local path | `source = "../modules/vpc"` |

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.0"

  name = "prod-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false

  tags = local.common_tags
}
```

---

## Core Workflow

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
terraform state list
terraform state show aws_vpc.main
terraform import aws_s3_bucket.assets my-existing-bucket-name
```
