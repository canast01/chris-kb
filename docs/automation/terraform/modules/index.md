# Terraform Modules

## Module Directory Structure

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

## Calling a Local Module

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

## Terraform Registry Modules

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

## Version Constraints

| Constraint | Meaning |
|---|---|
| `version = "5.0.0"` | Exact version only |
| `version = "~> 5.0"` | Any 5.x release (patch updates allowed) |
| `version = "~> 5.0.0"` | Any 5.0.x release (patch only) |
| `version = ">= 5.0, < 6.0"` | Range constraint |
| `version = ">= 5.0"` | Minimum version, no upper bound |

## Module Sources

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

## Module Management Commands

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
