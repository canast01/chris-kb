# Plan

> Part of the [Terraform CLI Reference](../).

---

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
