# Terraform State

## Remote State Configuration

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

## State Locking

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

## terraform state Commands

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

## Importing Existing Resources

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

## State File Best Practices

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
