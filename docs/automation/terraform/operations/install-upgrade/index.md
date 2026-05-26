# Terraform — Install & Upgrade

## Install Terraform (Linux)

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
```

## Install Terraform (Windows)

```powershell
# Using winget
winget install --id Hashicorp.Terraform

# Or manually: download ZIP from releases.hashicorp.com/terraform/
# Extract terraform.exe to C:\Tools\terraform\ and add to PATH
```

## Version Management with tfenv

`tfenv` lets you switch Terraform versions per project — essential when managing multiple workspaces with different required versions.

```bash
# Install tfenv (Linux/macOS)
git clone --depth=1 https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# List available versions
tfenv list-remote

# Install a specific version
tfenv install 1.7.5
tfenv use 1.7.5

# Pin a project to a version (creates .terraform-version)
echo "1.7.5" > .terraform-version
```

## Upgrade Terraform In-Place

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

## Upgrade Providers

```bash
# Upgrade all providers to latest allowed by version constraints
terraform init -upgrade

# Check what changed
terraform providers
```

## Required Version Constraints

Pin versions in `terraform` block to prevent unexpected upgrades.

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

## Version Reference

| Release | Status | Notes |
|---|---|---|
| 1.9.x | Current stable | Recommended for new projects |
| 1.8.x | Supported | |
| 1.6.x | Supported | Min for test assertions |
| < 1.5 | EOL | Upgrade recommended |
