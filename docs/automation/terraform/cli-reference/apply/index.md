# Apply & Destroy

> Part of the [Terraform CLI Reference](../).

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

## Destroy

```bash
# Destroy all resources
terraform destroy
terraform destroy -auto-approve
terraform destroy -target=resource_type.name
terraform destroy -var-file=prod.tfvars
```
