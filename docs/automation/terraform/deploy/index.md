---
tags:
  - deployment
  - terraform
search:
  boost: 1.5
---

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
install_terraform: "Install Terraform" {shape: rectangle}
configure_backend_remote_state: "Configure Backend (Remote State)" {shape: rectangle}
configure_provider_credentials: "Configure Provider Credentials" {shape: rectangle}
initialise_a_new_module: "Initialise a New Module" {shape: rectangle}
configure_workspace_per_environment: "Configure Workspace per Environment" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> install_terraform
install_terraform -> configure_backend_remote_state
configure_backend_remote_state -> configure_provider_credentials
configure_provider_credentials -> initialise_a_new_module
initialise_a_new_module -> configure_workspace_per_environment
configure_workspace_per_environment -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: Learn Terraform (and AWS) by Building a Dev Environment — Full Course for Beginners](https://www.youtube.com/watch?v=iRaai1IBlB0){ .md-button }
<!-- /video-link -->

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# Terraform — Environment Setup

This guide covers setting up a production-ready Terraform environment: installation, remote state backend, provider credentials, module structure, workspaces per environment, CI/CD integration, and drift detection.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Terraform | 1.6+ recommended |
| Cloud CLI | `aws`, `az`, or both — for provider authentication |
| Git | Version-controlled root module |
| Backend storage | S3 bucket (AWS) or Azure Storage Account (Azure) — created before `terraform init` |
| CI/CD system | GitHub Actions, GitLab CI, or Jenkins |

---

## Install Terraform

**macOS (Homebrew):**

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```


```text title="Expected output"
==> Tapping hashicorp/tap
Cloning into '/opt/homebrew/Library/Taps/hashicorp/homebrew-tap'...
remote: Enumerating objects: 1247, done.
remote: Counting objects: 100% (1247/1247), done.
remote: Compressing objects: 100% (892/892), done.
remote: Receiving objects: 100% (1247/1247), done.
==> Cloned successfully
==> Installing terraform from hashicorp/tap
==> Downloading https://releases.hashicorp.com/terraform/1.7.4/terraform_1.7.4_darwin_arm64.zip
==> Downloading from https://releases.hashicorp.com/terraform/1.7.4/terraform_1.7.4_darwin_arm64.zip
######################################################################## 100.0%
==> Installing hashicorp/tap/terraform
==> Pouring terraform--1.7.4.arm64_monterey.bottle.tar.gz
🍺  /opt/homebrew/Cellar/terraform/1.7.4: 6 files, 89.2MB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: hashicorp/tap/terraform: no bottle found for the requested macOS version` | Upgrade Homebrew with `brew update` and try again, or install from the official HashiCorp releases page. |
    | `Error: Failed to download resource "terraform_resource"` | Check your internet connection and verify HashiCorp's download servers are accessible; try `brew install terraform` from the core tap instead. |
**Linux (apt):**

```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```


```text title="Expected output"
--2024-01-15 14:32:18--  https://apt.releases.hashicorp.com/gpg
Resolving apt.releases.hashicorp.com (apt.releases.hashicorp.com)... 151.101.1.140, 151.101.65.140
Connecting to apt.releases.hashicorp.com (apt.releases.hashicorp.com)|151.101.1.140|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3149 (3.1K) [application/octet-stream]
Saving to: 'STDOUT'
deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com jammy main
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Hit:2 http://security.ubuntu.com/ubuntu jammy-security InRelease
Get:3 https://apt.releases.hashicorp.com jammy InRelease [7,234 B]
Get:4 https://apt.releases.hashicorp.com jammy/main amd64 Packages [32.5 kB]
Fetched 39.8 kB in 2s (18.2 kB/s)
Reading package lists... Done
Setting up terraform (1.7.4-1) ...
Processing triggers for man-db (2.10.2-1) ...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `gpg: can't connect to the agent: IPC connect call failed` | Run `gpg-connect-agent /bye` to reset the GPG agent, then retry the command. |
    | `E: Could not get lock /var/lib/apt/lists/lock - open (11: Resource temporarily unavailable)` | Wait for any running `apt` or `apt-get` processes to complete, or run `sudo lsof /var/lib/apt/lists/lock` to identify blocking processes. |
**Linux (binary download):**

```bash
curl -fsSL https://releases.hashicorp.com/terraform/1.8.5/terraform_1.8.5_linux_amd64.zip -o terraform.zip
unzip terraform.zip && sudo mv terraform /usr/local/bin/
```


```text title="Expected output"
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   102M  100   102M    0     0  8.2M      0  0:00:12 0:00:12 --:--:--  0:00:12
Archive:  terraform.zip
  inflating: terraform
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: unable to get local issuer certificate` | Update your CA certificates with `sudo update-ca-certificates` or use `curl -k` to skip verification (not recommended for production). |
    | `unzip: command not found` | Install unzip with `sudo apt-get install unzip` (Debian/Ubuntu) or `sudo yum install unzip` (RHEL/CentOS). |
    | `sudo: no password is available` | Run the commands without `sudo` if your user has write permissions to `/usr/local/bin/`, or configure passwordless sudo for this command. |
Verify installation:

```bash
terraform version
```


```text title="Expected output"
Terraform v1.5.7
on linux_amd64

Your version of Terraform is out of date! The newest version
is 1.6.4. You can update by downloading from https://www.terraform.io/downloads.html
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `command not found: terraform` | Install Terraform or add its binary directory to your PATH environment variable. |
    | `Error: Failed to query available provider packages` | Ensure you have internet connectivity and that your firewall allows access to registry.terraform.io. |
Expected output: `Terraform v1.8.x` or higher.

Install `tfenv` if you need to manage multiple Terraform versions across projects:

```bash
brew install tfenv
tfenv install 1.8.5
tfenv use 1.8.5
```


```text title="Expected output"
==> Downloading https://github.com/tfutils/tfenv/releases/download/v3.0.1/tfenv-v3.0.1.tar.gz
==> Downloading https://mirrors.aliyun.com/homebrew/bottles/tfenv-3.0.1.arm64_macos.bottle.tar.gz
==> Installing tfenv
==> Pouring tfenv-3.0.1.arm64_macos.bottle.tar.gz
🍺  /opt/homebrew/Cellar/tfenv/3.0.1: 47 files, 398KB
Installing Terraform v1.8.5
Downloading release notes from https://releases.hashicorp.com/terraform/1.8.5/
######################################################################## 100.0%
Downloading Terraform v1.8.5 for darwin_arm64
######################################################################## 100.0%
Unzipping /Users/admin/.tfenv/versions/1.8.5/terraform
Installing v1.8.5
Switching to v1.8.5
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `tfenv: command not found` | Add `/opt/homebrew/bin` to your `$PATH` or restart your shell after installation. |
    | `Error: terraform v1.8.5 not found in remote` | Verify the version exists on releases.hashicorp.com or use `tfenv list-remote` to see available versions. |
    | `permission denied: /Users/admin/.tfenv/versions` | Run `mkdir -p ~/.tfenv/versions` and ensure your user owns the directory with `chmod 755`. |
---

## Configure Backend (Remote State)

Remote state enables team collaboration, state locking, and auditability. Never use local state in shared environments.

**AWS S3 backend:**

First, create the S3 bucket and DynamoDB lock table (one-time setup):

```bash
aws s3api create-bucket \
    --bucket tf-state-prod-<account-id> \
    --region us-east-1

aws s3api put-bucket-versioning \
    --bucket tf-state-prod-<account-id> \
    --versioning-configuration Status=Enabled

aws dynamodb create-table \
    --table-name tf-state-lock \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```


```text title="Expected output"
{
    "Location": "http://tf-state-prod-123456789012.s3.amazonaws.com/"
}
(no output — command completes silently)
{
    "TableDescription": {
        "TableName": "tf-state-lock",
        "TableStatus": "CREATING",
        "TableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/tf-state-lock",
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "BillingModeSummary": {
            "BillingMode": "PAY_PER_REQUEST"
        },
        "CreationDateTime": "2024-01-15T14:32:47.123000+00:00"
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (BucketAlreadyExists) when calling the CreateBucket operation: The requested bucket name is not available. The bucket namespace is shared by all AWS accounts.` | Choose a globally unique bucket name by appending a timestamp or random suffix (e.g., `tf-state-prod-<account-id>-$(date +%s)`). |
    | `An error occurred (AccessDenied) when calling the CreateBucket operation: User: arn:aws:iam::123456789012:user/terraform is not authorized to perform: s3:CreateBucket` | Attach the `AmazonS3FullAccess` policy (or a custom S3 policy) to the IAM user/role running these commands. |
    | `An error occurred (ResourceInUseException) when calling the CreateTable operation: Requested resource already exists` | Delete the existing DynamoDB table with `aws dynamodb delete-table --table-name tf-state-lock` before rerunning, or skip creation if the table is already in use. |
In `main.tf`:

```hcl
terraform {
  backend "s3" {
    bucket         = "tf-state-prod-<account-id>"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-state-lock"
    encrypt        = true
  }
}
```

**Azure Storage Account backend:**

```bash
az storage account create \
    --name tfstateprod<suffix> \
    --resource-group rg-platform-terraform \
    --sku Standard_LRS \
    --kind StorageV2

az storage container create \
    --name tfstate \
    --account-name tfstateprod<suffix>
```


```text title="Expected output"
{
  "accessTier": "Hot",
  "allowBlobPublicAccess": true,
  "azureFilesIdentityBasedAuthentication": null,
  "creationTime": "2024-01-15T09:42:17.123456+00:00",
  "customDomain": null,
  "enableHttpsTrafficOnly": true,
  "encryption": {
    "keySource": "Microsoft.Storage",
    "keyVaultProperties": null,
    "services": {
      "blob": {
        "enabled": true,
        "lastEnabledTime": "2024-01-15T09:42:17.123456+00:00"
      },
      "file": {
        "enabled": true,
        "lastEnabledTime": "2024-01-15T09:42:17.123456+00:00"
      }
    }
  },
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-platform-terraform/providers/Microsoft.Storage/storageAccounts/tfstateprod2847",
  "identity": null,
  "kind": "StorageV2",
  "location": "eastus",
  "name": "tfstateprod2847",
  "primaryEndpoints": {
    "blob": "https://tfstateprod2847.blob.core.windows.net/",
    "dfs": "https://tfstateprod2847.dfs.core.windows.net/",
    "file": "https://tfstateprod2847.file.core.windows.net/",
    "queue": "https://tfstateprod2847.queue.core.windows.net/",
    "table": "https://tfstateprod2847.table.core.windows.net/",
    "web": "https://tfstateprod2847.web.core.windows.net/"
  },
  "primaryLocation": "eastus",
  "provisioningState": "Succeeded",
  "resourceGroup": "rg-platform-terraform",
  "sku": {
    "name": "Standard_LRS",
    "tier": "Standard"
  },
  "statusOfPrimary": "available",
  "tags": null,
  "type": "Microsoft.Storage/storageAccounts"
}
{
  "created": true,
  "metadata": {},
  "name": "tfstate",
  "publicAccess": null
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound: Resource group 'rg-platform-terraform' could not be found.` | Create the resource group first with `az group create --name rg-platform-terraform --location eastus`. |
    | `StorageAccountAlreadyTaken: The storage account named 'tfstateprod<suffix>' is already taken.` | Replace `<suffix>` with a unique numeric or alphanumeric string (storage account names must be globally unique). |
    **`AuthorizationFailed: The client 'user@example.com' with object id 'xxx' does not have authorization to perform action 'Microsoft.Storage/storageAccounts/write' over scope '/subscriptions/xxx/resourceGroups/
In `main.tf`:

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-platform-terraform"
    storage_account_name = "tfstateprod<suffix>"
    container_name       = "tfstate"
    key                  = "infra/terraform.tfstate"
  }
}
```

Initialise the backend:

```bash
terraform init
```


```text title="Expected output"
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/aws...
- Installing hashicorp/aws v5.42.0...
- Installed hashicorp/aws v5.42.0 (signed by HashiCorp)

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" next.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: error reading the backend configuration: unsupported argument "region"` | Remove or correct the invalid argument in your backend block in the Terraform configuration. |
    | `Error: Failed to download module: error downloading "git::https://github.com/org/repo.git": git not found in PATH` | Install git on your system or add it to your PATH environment variable. |
On success: `Backend "s3" (or "azurerm") initialised successfully.`

---

## Configure Provider Credentials

Providers authenticate using environment variables or credential files. Never hard-code credentials in `.tf` files.

**AWS:**

```bash
# Option 1 — AWS CLI (interactive)
aws configure

# Option 2 — Environment variables (CI/CD)
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"
```


```text title="Expected output"
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: json
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unable to locate credentials` | Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are exported before running Terraform, or run `aws configure` to store credentials in `~/.aws/credentials`. |
    | `The security token included in the request is invalid` | Verify the AWS_SECRET_ACCESS_KEY value is correct and not truncated; regenerate credentials in the AWS IAM console if needed. |
    | `InvalidParameterValue: Invalid region` | Set AWS_DEFAULT_REGION to a valid AWS region name such as `us-east-1`, `eu-west-1`, or `ap-southeast-1`. |
In `providers.tf`:

```hcl
provider "aws" {
  region = var.aws_region
}
```

**Azure:**

```bash
# Interactive login
az login

# Service principal (CI/CD)
export ARM_CLIENT_ID="..."
export ARM_CLIENT_SECRET="..."
export ARM_TENANT_ID="..."
export ARM_SUBSCRIPTION_ID="..."
```


```text title="Expected output"
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ABC123DEF456 to authenticate.

[
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "12345678-1234-1234-1234-123456789012",
    "id": "87654321-4321-4321-4321-210987654321",
    "isDefault": true,
    "name": "Production",
    "state": "Enabled",
    "tenantId": "12345678-1234-1234-1234-123456789012",
    "user": {
      "name": "admin@contoso.com",
      "type": "user"
    }
  }
]
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: AADSTS700016: Application with identifier 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' was not found in the directory` | Verify the ARM_CLIENT_ID is correct and the service principal exists in the target Azure AD tenant. |
    | `ERROR: AADSTS7000215: Invalid client secret is provided` | Regenerate the service principal secret in Azure Portal and update ARM_CLIENT_SECRET with the new value. |
In `providers.tf`:

```hcl
provider "azurerm" {
  features {}
}
```

**VMware vSphere:**

```bash
export VSPHERE_USER="administrator@vsphere.local"
export VSPHERE_PASSWORD="..."
export VSPHERE_SERVER="vcenter.corp.local"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bash: export: `administrator@vsphere.local': not a valid identifier` | Remove or escape the `@` symbol in the username, or use quotes: `export VSPHERE_USER="administrator@vsphere.local"` (ensure the entire string is quoted). |
    | `bash: VSPHERE_PASSWORD: command not found` | Ensure the password value is not left empty or contains unquoted special characters; use `export VSPHERE_PASSWORD="your_actual_password"` with proper quoting. |
In `providers.tf`:

```hcl
provider "vsphere" {
  allow_unverified_ssl = false
}
```

Verify provider configuration:

```bash
terraform providers
```


```text title="Expected output"
Providers required by the current configuration:

.
├── provider[registry.terraform.io/hashicorp/aws]
│   └── ~> 5.0
├── provider[registry.terraform.io/hashicorp/azurerm]
│   └── ~> 3.85
└── provider[registry.terraform.io/hashicorp/kubernetes]
    └── ~> 2.23

Providers required by the state:

.
├── provider[registry.terraform.io/hashicorp/aws] 5.12.0
├── provider[registry.terraform.io/hashicorp/azurerm] 3.87.0
└── provider[registry.terraform.io/hashicorp/kubernetes] 2.23.1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: No configuration files` | Run `terraform init` first to initialize the working directory and create the `.terraform` folder. |
    | `Error: Incompatible provider version` | Update your provider constraints in the configuration or run `terraform init -upgrade` to fetch compatible versions. |
All required providers should be listed with their versions.

---

## Initialise a New Module

Structure a root module before writing resources.

```bash
mkdir infra && cd infra
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `mkdir: cannot create directory 'infra': File exists` | Remove or rename the existing `infra` directory with `rm -rf infra` before running the command again. |
    | `mkdir: cannot create directory 'infra': Permission denied` | Ensure you have write permissions in the current directory by checking with `ls -ld .` and requesting access from your administrator if needed. |
Create the standard file layout:

![Terraform — Environment Setup — Diagram](../../../assets/automation-terraform-deploy-diagram.svg)

`versions.tf` — pin provider versions to avoid unexpected upgrades:

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
```

Initialise the module:

```bash
terraform init
terraform providers
terraform validate
```


```text title="Expected output"
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/aws...
- Installing hashicorp/aws v5.38.0...
- Installed hashicorp/aws v5.38.0 (signed by HashiCorp)

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" next.

Providers required by configuration:

Provider                  Version
--------                  -------
hashicorp/aws             5.38.0

Terraform v1.7.2
on linux_amd64

Your configuration is valid.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Terraform Core does not support this state file format` | Delete the `.terraform` directory and re-run `terraform init` to reinitialize with the current Terraform version. |
    | `Error: Failed to query available provider packages` | Verify internet connectivity and check that your Terraform provider registry is accessible (or configure a private registry in `.terraformrc`). |
    | `Error: Error reading schema from remote state` | Run `terraform state pull > backup.tfstate` to backup state, then `terraform state rm` to clear problematic resources before re-initializing. |
`terraform validate` should return `Success! The configuration is valid.`

---

## Configure Workspace per Environment

Workspaces keep state files separate for each environment while sharing the same root module and backend bucket.

```bash
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod
```


```text title="Expected output"
Created and switched to workspace "dev"
Created and switched to workspace "staging"
Created and switched to workspace "prod"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Workspace "dev" already exists` | Delete the existing workspace with `terraform workspace delete dev` or use `terraform workspace select dev` to switch to it instead. |
    | `Error: Invalid workspace name "dev-test"` | Use only alphanumeric characters, hyphens, and underscores in workspace names; rename to a valid format like `dev_test`. |
List workspaces:

```bash
terraform workspace list
```


```text title="Expected output"
default
* prod
  staging
  dev
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Not a valid terraform directory` | Run `terraform init` in the directory containing your Terraform configuration files first. |
    | `Error: workspace not found` | Ensure you are in the correct Terraform working directory where `.terraform/` exists. |
Switch to an environment:

```bash
terraform workspace select prod
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: workspace "prod" does not exist` | Run `terraform workspace new prod` to create the workspace before selecting it. |
    | `Error: No default backend configured` | Initialize the Terraform working directory with `terraform init` first to configure the backend. |
Reference the workspace name in resource names to avoid collisions:

```hcl
resource "aws_s3_bucket" "app_data" {
  bucket = "app-data-${terraform.workspace}-${var.account_id}"
}
```

Use a `terraform.tfvars` file per workspace or use `-var-file`:

```bash
terraform plan -var-file="envs/prod.tfvars"
terraform apply -var-file="envs/prod.tfvars"
```


```text title="Expected output"
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create
  ~ update in-place
  - destroy

Terraform will perform the following actions:

  # aws_instance.web_server will be created
  + resource "aws_instance" "web_server" {
      + ami           = "ami-0c55b159cbfafe1f0"
      + instance_type = "t3.medium"
      + tags          = {
          + "Environment" = "prod"
          + "Name"        = "web-server-01"
        }
    }

Plan: 3 to add, 1 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_instance.web_server: Creating...
aws_instance.web_server: Still creating... [10s elapsed]
aws_instance.web_server: Creation complete after 15s [id=i-0a7f3c8d9e2b1f4a6]

Apply complete! Resources: 3 added, 1 changed, 0 destroyed.

Outputs:

instance_id = "i-0a7f3c8d9e2b1f4a6"
instance_ip = "10.42.8.15"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: error reading envs/prod.tfvars: open envs/prod.tfvars: no such file or directory` | Verify the tfvars file path is correct and the file exists in the working directory. |
    | `Error: Insufficient IAM permissions to perform: ec2:RunInstances` | Ensure the AWS credentials in use have the required IAM policies attached for the resources being created. |
    | `Error: resource already exists in state` | Run `terraform refresh` to sync the state file with actual infrastructure, or manually remove the conflicting resource from state. |
---

## Set Up CI/CD Integration

Automate plan on pull request and apply on merge. The example below uses GitHub Actions.

Create `.github/workflows/terraform.yml`:

```yaml
name: Terraform

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  AWS_DEFAULT_REGION: us-east-1

jobs:
  plan:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.8.5
      - run: terraform init
        working-directory: infra
      - run: terraform plan -out=tfplan
        working-directory: infra

  apply:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.8.5
      - run: terraform init
        working-directory: infra
      - run: terraform apply -auto-approve
        working-directory: infra
```

Store credentials as GitHub Actions secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

For Azure, set `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_TENANT_ID`, `ARM_SUBSCRIPTION_ID` as secrets.

---

## Enable Drift Detection (Scheduled Plan)

Drift occurs when infrastructure changes outside Terraform. A scheduled plan detects divergence between the state file and actual cloud resources.

Add a scheduled workflow in GitHub Actions:

```yaml
name: Terraform Drift Detection

on:
  schedule:
    - cron: '0 6 * * *'   # Daily at 06:00 UTC

env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  AWS_DEFAULT_REGION: us-east-1

jobs:
  drift-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.8.5
      - run: terraform init
        working-directory: infra
      - name: Check for drift
        working-directory: infra
        run: |
          terraform plan -detailed-exitcode -out=tfplan
          EXIT_CODE=$?
          if [ $EXIT_CODE -eq 2 ]; then
            echo "DRIFT DETECTED — infrastructure has changed outside Terraform"
            exit 1
          fi
```

Exit code meanings:
- `0` — no changes (no drift)
- `1` — error
- `2` — changes detected (drift)

The workflow fails on exit code 2, triggering a GitHub Actions alert. Connect the workflow failure to your alerting channel (Slack, PagerDuty, email) via GitHub notifications or a webhook step.

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation

---

## See also

- [Terraform — Procedures](../operations/procedures/)
- [Terraform — Common Issues](../troubleshooting/common-issues/)
- [Terraform — How It Works](../architecture/how-it-works/)
