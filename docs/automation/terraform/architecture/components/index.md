# Terraform — Components

## Modules

### Module Directory Structure

A module is any directory containing `.tf` files. The convention for reusable modules:

```
modules/
  network/
    main.tf         # resources
    variables.tf    # input variables
    outputs.tf      # output values
    versions.tf     # required providers and Terraform version
    README.md
```

```hcl
# modules/network/variables.tf
variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, prod)"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# modules/network/outputs.tf
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}
```

### Calling a Local Module

```hcl
# root/main.tf
module "network" {
  source = "./modules/network"

  vpc_cidr    = "10.1.0.0/16"
  environment = var.environment
}

# Use module outputs in other resources
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.small"
  subnet_id     = module.network.private_subnet_ids[0]
}
```

### Terraform Registry Modules

```hcl
# Use a module from the Terraform Registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
}
```

### Version Constraints

| Constraint | Meaning |
|---|---|
| `version = "5.0.0"` | Exact version only |
| `version = "~> 5.0"` | Any 5.x release (patch updates allowed) |
| `version = "~> 5.0.0"` | Any 5.0.x release (patch only) |
| `version = ">= 5.0, < 6.0"` | Range constraint |
| `version = ">= 5.0"` | Minimum version, no upper bound |

### Module Sources

```hcl
# Local path
source = "./modules/network"

# Terraform Registry
source  = "hashicorp/consul/aws"
version = "~> 0.10"

# GitHub
source = "github.com/hashicorp/example"

# GitHub with specific ref
source = "git::https://github.com/myorg/modules.git//network?ref=v2.1.0"

# Private registry
source  = "app.terraform.io/myorg/network/aws"
version = "~> 1.0"
```

### Module Management Commands

```bash
# Download and install all modules referenced in configuration
terraform init

# Upgrade modules to latest allowed version
terraform init -upgrade

# Show the full module call tree
terraform providers

# Inspect a specific module's outputs after apply
terraform output -module=network

# List all resources managed by a module
terraform state list | grep module.network
```

---

## State Management

### Remote State Configuration

Remote state stores the `terraform.tfstate` file in a shared backend instead of locally.

```hcl
# backend.tf — AWS S3 backend with DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/network/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

```hcl
# backend.tf — Azure blob storage backend
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstateaccount"
    container_name       = "tfstate"
    key                  = "prod.network.tfstate"
  }
}
```

```bash
# Migrate local state to a remote backend
terraform init -migrate-state

# Reconfigure backend without migrating (use with care)
terraform init -reconfigure
```

### State Locking

State locking prevents concurrent operations from corrupting state.

| Backend | Locking mechanism |
|---|---|
| S3 | DynamoDB table (`LockID` primary key) |
| Azure blob | Blob lease |
| GCS | Object lock |
| Terraform Cloud | Built-in |
| Local | `.terraform.lock.hcl` |

```bash
# Force-unlock if a lock is stuck (use with care — only when the locking process is dead)
terraform force-unlock LOCK_ID
```

### terraform state Commands

```bash
# List all resources tracked in state
terraform state list

# List resources in a module
terraform state list module.network

# Show the state for a specific resource
terraform state show aws_instance.web01

# Remove a resource from state (does NOT destroy the real resource)
terraform state rm aws_instance.old_server

# Move/rename a resource in state
terraform state mv aws_instance.web aws_instance.web01

# Move a resource into a module
terraform state mv aws_security_group.web module.network.aws_security_group.web

# Pull remote state to stdout
terraform state pull

# Push local state to remote backend (use with extreme care)
terraform state push terraform.tfstate
```

### Importing Existing Resources

```bash
# Import a real resource into Terraform management
terraform import aws_instance.web01 i-0abc1234def56789

# After import, add the resource block to match the real resource
# Then verify with plan
terraform plan
# Expected: 0 to add, 0 to change, 0 to destroy

# Generate configuration from imported state (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf
```

### State File Best Practices

```bash
# Never edit terraform.tfstate manually
# Always use terraform state subcommands

# Back up state before destructive operations
terraform state pull > backup-$(date +%Y%m%d-%H%M%S).tfstate

# Use workspaces to separate environments with the same config
terraform workspace new production
terraform workspace select production
terraform workspace list
terraform workspace show
```
