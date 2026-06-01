# Terraform — Integrations


<div class="kb-summary">
Terraform integrates with cloud providers, secrets management, source control, and CI/CD systems. This page covers the major integrations used in enterprise environments.
</div>

---

## AWS Provider

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
  }
}

provider "aws" {
  region = var.aws_region
  # Authentication (in order of preference for CI):
  # 1. OIDC role assumption (GitHub Actions / GitLab CI)
  # 2. Instance profile / ECS task role
  # 3. AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY env vars
  # Never: hardcoded credentials in .tf files
}
```
┌────────────────────────────────────── Terraform — Integrations ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Terraform integrates with CI/CD, secret managers, monitoring, and ITSM via providers and APIs │   │
│   │          GitHub Actions: terraform plan in PR check; terraform apply on merge to main         │   │
│   │Secrets: provider auth via env vars or OIDC; Vault provider for secret injection into resources│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            CI/CD            │  │           Secrets           │  │          Platforms          │   │
│   │    GitHub Actions (OIDC)    │  │        Vault provider       │  │       AWS, Azure, GCP       │   │
│   │    GitLab CI: plan/apply    │  │      env var: TF_VAR_x      │  │        VMware vSphere       │   │
│   │   Atlantis (PR automation)  │  │   AWS SSM Parameter Store   │  │      NetApp, Pure, Dell     │   │
│   │  Terraform Cloud/Enterprise │  │ No secrets in .tfvars in git│  │       Kubernetes, Helm      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Atlantis    = Terraform PR automation; runs plan on PR, apply on merge; self-hosted      │   │
│   │    TF Cloud    = HashiCorp SaaS; remote execution, Sentinel policies, team RBAC, audit log    │   │
│   │  Vault provider= reads secrets from Vault at apply time; writes dynamic credentials to state  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

```bash
# GitHub Actions OIDC for Azure
# Requires federated credential on the app registration:
# Entity: GitHub Actions deployment → repo:my-org/infra:ref:refs/heads/main
export ARM_USE_OIDC=true
export ARM_CLIENT_ID="..."
export ARM_TENANT_ID="..."
export ARM_SUBSCRIPTION_ID="..."
```

---

## GCP Provider (`google`)

```hcl
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  # Workload Identity Federation for CI — no service account keys
}

provider "google-beta" {
  project = var.gcp_project_id
  region  = var.gcp_region
}
```

```bash
# Workload Identity Federation
gcloud iam workload-identity-pools create "github-pool" \
  --project="${PROJECT_ID}" \
  --location="global"

gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository"
```

---

## VMware vSphere Provider

```hcl
terraform {
  required_providers {
    vsphere = {
      source  = "hashicorp/vsphere"
      version = "~> 2.7"
    }
  }
}

provider "vsphere" {
  vsphere_server       = var.vsphere_server        # e.g. "vcenter.example.com"
  user                 = var.vsphere_user           # From Vault / env var
  password             = var.vsphere_password       # From Vault / env var
  allow_unverified_ssl = var.vsphere_insecure       # false in production
}

# Data sources for existing infrastructure
data "vsphere_datacenter"    "dc"    { name = "DC-PROD" }
data "vsphere_datastore"     "ds"    { name = "VSAN-PROD-01"; datacenter_id = data.vsphere_datacenter.dc.id }
data "vsphere_compute_cluster" "cls" { name = "Cluster-PROD"; datacenter_id = data.vsphere_datacenter.dc.id }
data "vsphere_network"       "net"   { name = "VLAN-100-App"; datacenter_id = data.vsphere_datacenter.dc.id }
data "vsphere_virtual_machine" "tmpl" {
  name          = "rhel-9-template"
  datacenter_id = data.vsphere_datacenter.dc.id
}

# Deploy a VM from template
resource "vsphere_virtual_machine" "app" {
  name             = "app-prod-01"
  resource_pool_id = data.vsphere_compute_cluster.cls.resource_pool_id
  datastore_id     = data.vsphere_datastore.ds.id

  num_cpus = 4
  memory   = 8192
  firmware = "efi"

  network_interface {
    network_id   = data.vsphere_network.net.id
    adapter_type = data.vsphere_virtual_machine.tmpl.network_interface_types[0]
  }

  disk {
    label            = "disk0"
    size             = data.vsphere_virtual_machine.tmpl.disks[0].size
    thin_provisioned = false
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.tmpl.id
    customize {
      linux_options {
        host_name = "app-prod-01"
        domain    = "example.com"
      }
      network_interface {
        ipv4_address = "10.100.0.11"
        ipv4_netmask = 24
      }
      ipv4_gateway = "10.100.0.1"
    }
  }
}
```

---

## HashiCorp Vault Integration

Retrieve dynamic credentials and secrets at plan/apply time without storing them in state.

```hcl
terraform {
  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "~> 4.2"
    }
  }
}

provider "vault" {
  address = "https://vault.example.com"
  # Auth via VAULT_TOKEN env var, or AWS IAM auth, or AppRole
}

# Read a static secret
data "vault_kv_secret_v2" "db_creds" {
  mount = "secret"
  name  = "platform/postgres"
}

# Use in a resource
resource "aws_db_instance" "app" {
  identifier     = "app-prod"
  engine         = "postgres"
  engine_version = "16.2"
  username       = data.vault_kv_secret_v2.db_creds.data["username"]
  password       = data.vault_kv_secret_v2.db_creds.data["password"]
  instance_class = "db.t4g.medium"
}

# Dynamic AWS credentials from Vault (avoids long-lived IAM keys)
data "vault_aws_access_credentials" "ci" {
  backend = "aws"
  role    = "terraform-deployer"
  type    = "sts"
}
```

> Secrets fetched via `data` sources are stored in Terraform state. Ensure state is encrypted at rest and access is restricted.

---

## GitHub Provider

Manage repositories, teams, and branch protection as code.

```hcl
terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.2"
    }
  }
}

provider "github" {
  owner = "my-org"
  # GITHUB_TOKEN env var — use a GitHub App token in production
}

resource "github_repository" "infra" {
  name        = "platform-infra"
  description = "Platform infrastructure as code"
  visibility  = "private"

  has_issues   = true
  has_projects = false
  has_wiki     = false

  delete_branch_on_merge = true
  allow_squash_merge      = true
  allow_merge_commit      = false
  allow_rebase_merge      = false
}

resource "github_branch_protection" "main" {
  repository_id = github_repository.infra.node_id
  pattern       = "main"

  required_pull_request_reviews {
    required_approving_review_count = 2
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = true
  }

  required_status_checks {
    strict   = true
    contexts = ["terraform-validate", "terraform-plan"]
  }

  enforce_admins = true
}

resource "github_team" "platform" {
  name    = "platform-engineering"
  privacy = "closed"
}

resource "github_team_repository" "platform_infra" {
  team_id    = github_team.platform.id
  repository = github_repository.infra.name
  permission = "maintain"
}
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/terraform.yml
name: Terraform
on:
  pull_request:
    paths: ['infra/**']
  push:
    branches: [main]
    paths: ['infra/**']

permissions:
  id-token: write   # Required for OIDC
  contents: read
  pull-requests: write

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: infra/

    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/TerraformCIRole
          aws-region: eu-west-1

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.7.5"

      - name: Init
        run: terraform init

      - name: Validate
        run: terraform validate

      - name: Plan
        id: plan
        run: terraform plan -no-color -out=tfplan
        continue-on-error: true

      - name: Post plan to PR
        uses: actions/github-script@v7
        if: github.event_name == 'pull_request'
        with:
          script: |
            const output = `### Terraform Plan
            \`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\``;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });

      - name: Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply tfplan
```

### GitLab CI

```yaml
# .gitlab-ci.yml
variables:
  TF_ROOT: ${CI_PROJECT_DIR}/infra
  TF_STATE_NAME: ${CI_PROJECT_NAME}

stages: [validate, plan, apply]

.terraform:
  image: hashicorp/terraform:1.7.5
  before_script:
    - cd ${TF_ROOT}
    - terraform init
      -backend-config="address=${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/${TF_STATE_NAME}"
      -backend-config="lock_address=${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/${TF_STATE_NAME}/lock"
      -backend-config="unlock_address=${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/${TF_STATE_NAME}/lock"
      -backend-config="username=gitlab-ci-token"
      -backend-config="password=${CI_JOB_TOKEN}"

validate:
  extends: .terraform
  stage: validate
  script:
    - terraform validate
    - terraform fmt -check

plan:
  extends: .terraform
  stage: plan
  script:
    - terraform plan -out=tfplan
  artifacts:
    paths: [infra/tfplan]

apply:
  extends: .terraform
  stage: apply
  script:
    - terraform apply tfplan
  dependencies: [plan]
  when: manual
  only: [main]
```

---

## Atlantis (Pull Request Automation)

Atlantis runs `terraform plan` on PR open/update and `terraform apply` on PR merge approval. It provides an audit trail in PR comments.

```yaml
# atlantis.yaml — repository configuration
version: 3
automerge: false
delete_source_branch_on_merge: false

projects:
  - name: platform-networking
    dir: infra/networking
    workspace: default
    terraform_version: v1.7.5
    autoplan:
      when_modified: ["**/*.tf", "**/*.tfvars", "../../modules/**/*.tf"]
      enabled: true
    apply_requirements:
      - approved
      - mergeable

  - name: platform-compute
    dir: infra/compute
    workspace: default
    terraform_version: v1.7.5
    autoplan:
      when_modified: ["**/*.tf", "**/*.tfvars"]
    apply_requirements:
      - approved
      - mergeable
```

PR workflow with Atlantis:

1. Open PR → Atlantis runs `terraform plan` → posts plan output as comment
2. Team reviews plan in PR
3. Reviewer approves: `atlantis apply` comment triggers apply
4. Apply output posted as PR comment
5. PR merged

---

## Terraform Cloud / Enterprise API

```bash
# Trigger a run via API (CI pipeline integration)
curl -s \
  --header "Authorization: Bearer $TFC_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST \
  --data '{
    "data": {
      "attributes": {
        "is-destroy": false,
        "message": "Triggered by CI pipeline - commit abc123"
      },
      "type": "runs",
      "relationships": {
        "workspace": {
          "data": { "type": "workspaces", "id": "ws-XXXXXXXXXXXXXXXXX" }
        }
      }
    }
  }' \
  "https://app.terraform.io/api/v2/runs"
```

```hcl
# Terraform Cloud backend
terraform {
  cloud {
    organization = "my-org"
    workspaces {
      name = "platform-networking-prod"
    }
  }
}
```
