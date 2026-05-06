# State & Output

> Part of the [Terraform CLI Reference](../).

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

## Import

```bash
# Import existing resource into state
terraform import resource_type.name <resource_id>
terraform import -var-file=prod.tfvars resource_type.name <id>

# Generate config from existing resources (1.5+)
terraform plan -generate-config-out=generated.tf
```

## Output

```bash
# Show outputs
terraform output
terraform output <output_name>
terraform output -json
terraform output -raw <output_name>
```
