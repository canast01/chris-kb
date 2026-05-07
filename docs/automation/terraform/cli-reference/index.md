# Terraform CLI Reference

Terraform is HashiCorp's infrastructure-as-code tool. You describe your desired infrastructure in `.tf` files, and Terraform figures out what to create, change, or delete to reach that state. State is stored in a `.tfstate` file — it's Terraform's record of what it has actually deployed.

> Install with `brew install terraform` (macOS), `apt install terraform` (Debian), or download from terraform.io. Run `terraform init` in any new working directory before other commands.
---

## Init & Setup

Initialize a Terraform working directory — downloads providers, configures the backend (where state is stored), and prepares modules. Always run this first in a new directory or after changing provider/backend configuration.

```bash
# Initialize working directory
terraform init
terraform init -reconfigure          # force re-initialization (clears cached backend config)
terraform init -upgrade              # upgrade providers to the latest allowed version
terraform init -backend=false        # skip backend init (use local state only)

# Show installed Terraform version and provider versions
terraform version
```

---

## Plan

Preview what Terraform will do before making any changes. Always run `plan` before `apply`. Save the plan to a file to guarantee that `apply` runs exactly what you reviewed.

```bash
# Preview changes
terraform plan
terraform plan -out=tfplan           # save plan to file (apply this file to guarantee exact changes)
terraform plan -var 'env=prod'       # pass a variable
terraform plan -var-file=prod.tfvars # load variables from file
terraform plan -target=resource_type.name   # only plan a specific resource

# Destroy plan (preview what would be deleted)
terraform plan -destroy

# Detailed exit codes (useful in CI/CD scripts)
terraform plan -detailed-exitcode
# Exit code: 0 = no changes, 1 = error, 2 = changes present
```

---

## Apply & Destroy

Apply makes the changes from a plan. Destroy removes all resources managed by Terraform. Use `-target` to operate on a specific resource instead of everything.

```bash
# Apply changes
terraform apply
terraform apply tfplan               # apply a saved plan (recommended — no surprises)
terraform apply -auto-approve        # skip confirmation prompt (for CI/CD)
terraform apply -var 'env=prod'
terraform apply -var-file=prod.tfvars
terraform apply -target=resource_type.name
terraform apply -parallelism=10      # concurrent operations (default: 10)

# Replace a specific resource (force recreation)
terraform apply -replace=resource_type.name

# Destroy all resources
terraform destroy
terraform destroy -auto-approve
terraform destroy -target=resource_type.name
terraform destroy -var-file=prod.tfvars
```

---

## Validate, Format & Providers

Check syntax, auto-format code, and inspect provider dependencies. Run `validate` and `fmt -check` in CI before planning.

```bash
# Validate configuration syntax
terraform validate

# Auto-format code to canonical style
terraform fmt
terraform fmt -recursive            # format all subdirectories
terraform fmt -check                # exit non-zero if any files need formatting (CI use)
terraform fmt -diff                 # show what would change without writing

# Provider management
terraform providers                 # list required providers and their versions
terraform providers lock            # lock provider versions in .terraform.lock.hcl
terraform get                       # download modules referenced in configuration
terraform get -update               # update modules to latest allowed version

# Dependency graph (requires graphviz)
terraform graph | dot -Tsvg > graph.svg
terraform graph -type=plan | dot -Tpng > plan.png
```

---

## State & Output

State is Terraform's source of truth about what's deployed. Use `state` commands carefully — modifying state incorrectly can cause Terraform to recreate resources or lose track of existing ones.

```bash
# List all resources tracked in state
terraform state list
terraform state list module.name    # resources in a specific module

# Show a resource's current state
terraform state show resource_type.name
terraform state show 'resource_type.name["key"]'

# Move a resource (rename without destroying)
terraform state mv resource_type.old resource_type.new

# Remove a resource from state (without deleting the real resource)
terraform state rm resource_type.name

# Backup and restore state
terraform state pull > backup.tfstate
terraform state push backup.tfstate

# Release a stuck state lock
terraform force-unlock <lock_id>

# Import an existing resource into Terraform management
terraform import resource_type.name <resource_id>
terraform import -var-file=prod.tfvars resource_type.name <id>

# Generate config from existing resources (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf

# Outputs
terraform output
terraform output <output_name>
terraform output -json
terraform output -raw <output_name>   # plain string without quotes
```

---

## Workspaces

Workspaces let you manage multiple independent deployments (e.g., dev, staging, prod) from the same configuration with separate state files. Not available with all backends.

```bash
# List workspaces
terraform workspace list

# Create and switch
terraform workspace new <name>
terraform workspace select <name>

# Show current workspace
terraform workspace show

# Delete (must switch away first)
terraform workspace delete <name>
```

---

## Console, Debug & Patterns

The interactive console evaluates expressions against your current state. Debug logging helps trace provider API calls when something isn't working.

```bash
# Interactive console (evaluate expressions against current state)
terraform console
# > module.name.output_value
# > var.my_var
# > length(var.list)

# Debug logging
TF_LOG=DEBUG terraform plan
TF_LOG=TRACE terraform apply
TF_LOG_PATH=./debug.log terraform plan

# Common workflow patterns
# Full cycle (plan → save → apply saved plan)
terraform init && terraform plan -out=tfplan && terraform apply tfplan

# Refresh-only (sync state with reality without changing resources)
terraform apply -refresh-only

# Import an existing resource then verify nothing would change
terraform import resource_type.name <id> && terraform plan

# CI/CD pattern (non-interactive)
terraform init -input=false
terraform plan -input=false -out=tfplan
terraform apply -input=false tfplan
```
