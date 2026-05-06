# Terraform CLI Reference

Commonly used Terraform commands for infrastructure provisioning and state management.

---

## Init & Setup

```bash
# Initialize working directory
terraform init
terraform init -reconfigure
terraform init -upgrade           # Upgrade providers to latest allowed version
terraform init -backend=false     # Skip backend init

# Show version
terraform version
```

---

## Plan

```bash
# Preview changes
terraform plan
terraform plan -out=tfplan        # Save plan to file
terraform plan -var 'env=prod'
terraform plan -var-file=prod.tfvars
terraform plan -target=resource_type.name

# Destroy plan
terraform plan -destroy

# Detailed exit codes (CI use)
terraform plan -detailed-exitcode
# Exit 0 = no changes, 1 = error, 2 = changes present
```

---

## Apply

```bash
# Apply changes
terraform apply
terraform apply tfplan            # Apply saved plan
terraform apply -auto-approve     # Skip confirmation prompt
terraform apply -var 'env=prod'
terraform apply -var-file=prod.tfvars
terraform apply -target=resource_type.name
terraform apply -parallelism=10   # Default is 10

# Replace a specific resource
terraform apply -replace=resource_type.name
```

---

## Destroy

```bash
# Destroy all resources
terraform destroy
terraform destroy -auto-approve
terraform destroy -target=resource_type.name
terraform destroy -var-file=prod.tfvars
```

---

## State

```bash
# List all resources in state
terraform state list
terraform state list module.name

# Show a resource
terraform state show resource_type.name
terraform state show 'resource_type.name["key"]'

# Move a resource (rename without recreate)
terraform state mv resource_type.old resource_type.new

# Remove from state (without deleting real resource)
terraform state rm resource_type.name

# Pull state
terraform state pull > backup.tfstate

# Push state
terraform state push backup.tfstate

# Force unlock state
terraform force-unlock <lock_id>
```

---

## Import

```bash
# Import existing resource into state
terraform import resource_type.name <resource_id>
terraform import -var-file=prod.tfvars resource_type.name <id>

# Generate config from existing resources (1.5+)
terraform plan -generate-config-out=generated.tf
```

---

## Output

```bash
# Show outputs
terraform output
terraform output <output_name>
terraform output -json
terraform output -raw <output_name>
```

---

## Workspaces

```bash
# List workspaces
terraform workspace list

# Create / switch
terraform workspace new <name>
terraform workspace select <name>

# Show current
terraform workspace show

# Delete
terraform workspace delete <name>
```

---

## Validate & Format

```bash
# Validate config syntax
terraform validate

# Format code
terraform fmt
terraform fmt -recursive
terraform fmt -check             # Exit non-zero if changes needed
terraform fmt -diff              # Show diffs
```

---

## Providers & Modules

```bash
# List required providers
terraform providers

# Lock provider versions
terraform providers lock

# Download modules
terraform get
terraform get -update

# Show module tree
terraform providers schema -json
```

---

## Graph

```bash
# Generate dependency graph (dot format)
terraform graph | dot -Tsvg > graph.svg
terraform graph -type=plan | dot -Tpng > plan.png
```

---

## Console & Debug

```bash
# Interactive console
terraform console
# > module.name.output_value
# > var.my_var

# Debug logging
TF_LOG=DEBUG terraform plan
TF_LOG=TRACE terraform apply
TF_LOG_PATH=./debug.log terraform plan
```

---

## Common Patterns

```bash
# Full cycle
terraform init && terraform plan -out=tfplan && terraform apply tfplan

# Targeted refresh
terraform apply -refresh-only

# Import + verify
terraform import resource_type.name <id> && terraform plan

# CI/CD pattern
terraform init -input=false
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
```
