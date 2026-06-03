# Terraform — Install & Upgrade

```bash
# Ubuntu / Debian — via HashiCorp apt repo
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
  https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update && sudo apt-get install terraform

# Verify
terraform version
```

```text
┌──────────────────────────────────── Terraform — Install & Upgrade ────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Install Terraform: tfenv for version management; or direct binary from releases.hashicorp.com │   │
│   │        Upgrade: tfenv install 1.8.0; tfenv use 1.8.0; test with terraform init -upgrade       │   │
│   │    Provider upgrade: update required_providers version constraint; terraform init -upgrade    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Terraform Install (tfenv)           │  │               Provider Upgrade              │   │
│   │              brew install tfenv              │  │        Update versions.tf constraint        │   │
│   │             tfenv install 1.8.0              │  │           terraform init -upgrade           │   │
│   │               tfenv use 1.8.0                │  │       Review .terraform.lock.hcl diff       │   │
│   │      echo "1.8.0" > .terraform-version       │  │       terraform plan (check no issues)      │   │
│   │          terraform version (verify)          │  │           Commit updated lock file          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ tfenv           = Terraform version manager; .terraform-version file pins version per project │   │
│   │   -upgrade        = init flag; re-downloads providers to latest matching version constraint   │   │
│   │     required_version= constraint in versions.tf; prevents running wrong Terraform version     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Check current version
terraform version

# Linux — upgrade via apt
sudo apt-get update && sudo apt-get install terraform

# macOS
brew upgrade hashicorp/tap/terraform

# After upgrade — re-init existing workspaces
terraform init -upgrade
```
```bash
# Upgrade all providers to latest allowed by version constraints
terraform init -upgrade

# Check what changed
terraform providers
```
```hcl
terraform {
  required_version = ">= 1.6, < 2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    vsphere = {
      source  = "hashicorp/vsphere"
      version = ">= 2.5"
    }
  }
}
```
