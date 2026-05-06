# Console, Debug & Patterns

> Part of the [Terraform CLI Reference](../).

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
