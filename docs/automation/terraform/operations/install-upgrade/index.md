---
tags:
  - operations
  - terraform
---
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


```text title="Expected output"
Get:1 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
Get:2 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
Reading package lists... Done
Setting up gnupg (2.2.27-3ubuntu2.1) ...
Setting up software-properties-common (0.99.30.2) ...
Setting up curl (7.81.0-1ubuntu1.13) ...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3662  100  3662    0     0  18456      0 --:--:-- -- 0:00:00 --:--:-- 0:00:00
deb [arch=amd64 signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com jammy main
Hit:1 https://apt.releases.hashicorp.com jammy InRelease
Reading package lists... Done
Setting up terraform (1.6.4-1) ...
Terraform v1.6.4
on linux_amd64
+ provider registry.terraform.io/hashicorp/aws v5.31.0
+ provider registry.terraform.io/hashicorp/null v3.2.2
```

!!! warning "Common errors"
    **`E: Could not resolve 'apt.releases.hashicorp.com'`** — Verify internet connectivity and DNS resolution with `nslookup apt.releases.hashicorp.com`.
    **`gpg: can't connect to the GPG agent: IPC connect call failed`** — Run `gpg-connect-agent reloadagent /bye` or restart the gpg-agent service.
    **`E: Unable to locate package terraform`** — Ensure the HashiCorp repository was added correctly by running `grep hashicorp /etc/apt/sources.list.d/*.list` and verify the GPG key import succeeded.
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

```text title="Expected output"
Terraform v1.5.7
on linux_amd64

Your version of Terraform is out of date! The newest version
is 1.6.4. You can update by downloading from https://www.terraform.io/downloads.html

Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
Reading package lists... Done
Setting up terraform (1.6.4-1) ...
Processing triggers for man-db (2.10.2-1) ...

Upgrading hashicorp/tap/terraform
==> Upgrading 1 outdated package:
hashicorp/tap/terraform 1.5.7 -> 1.6.4
==> Upgrading hashicorp/tap/terraform
🍺  /usr/local/Cellar/hashicorp/tap/terraform/1.6.4: 5 files, 95.2MB

Initializing the backend...
Initializing provider plugins...
Upgrading hashicorp/aws to version 5.31.0...
Terraform has been successfully initialized!
```

!!! warning "Common errors"
    **`Error: Failed to query available provider packages`** — Ensure your network connectivity is stable and check that your Terraform registry credentials are valid if using a private registry.
    **`Error: Incompatible provider version`** — Run `terraform init -upgrade` to fetch compatible provider versions matching your configuration.
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

```d2
direction: right

plan: "Plan" {shape: oval}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> verify
verify -> validate
```

## Before you begin

- **Access:** Provider credentials configured (`terraform login` or env vars)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Terraform — Deploy](../../deploy/)
