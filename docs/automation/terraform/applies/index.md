# Terraform Apply

## Standard Apply Workflow

The normal workflow is init → plan → review → apply.

```bash
# Initialise the working directory
terraform init

# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Generate and display a plan
terraform plan

# Apply the changes (prompts for confirmation)
terraform apply

# Apply without interactive prompt (CI/CD)
terraform apply -auto-approve
```

## Saving and Applying Plan Files

Using saved plan files ensures the apply executes exactly the reviewed plan.

```bash
# Save plan to a file
terraform plan -out=tfplan

# Review the plan (human-readable)
terraform show tfplan

# Review as JSON for scripting
terraform show -json tfplan | jq '.resource_changes[] | {resource: .address, action: .change.actions}'

# Apply from saved plan (no second prompt)
terraform apply tfplan

# Clean up plan file after apply
rm tfplan
```

## Targeted Apply

Apply only specific resources without touching the rest of the configuration.

```bash
# Apply a single resource
terraform apply -target=aws_instance.web01

# Apply a module
terraform apply -target=module.network

# Apply multiple targets
terraform apply \
  -target=aws_security_group.web \
  -target=aws_instance.web01

# Destroy a specific resource
terraform destroy -target=aws_instance.old_server -auto-approve
```

Use `-target` sparingly — it creates drift between the plan and real state if overused.

## Passing Variables at Apply Time

```bash
# Inline variable values
terraform apply -var="instance_type=t3.medium" -var="region=eu-west-1"

# From a var file
terraform apply -var-file="envs/production.tfvars"

# From environment variables (TF_VAR_ prefix)
export TF_VAR_db_password="s3cretpassword"
terraform apply
```

## Apply in CI/CD Pipelines

```yaml
# GitHub Actions example
- name: Terraform Init
  run: terraform init
  working-directory: infra/

- name: Terraform Plan
  id: plan
  run: terraform plan -out=tfplan -no-color
  working-directory: infra/
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

- name: Terraform Apply
  if: github.ref == 'refs/heads/main'
  run: terraform apply -auto-approve tfplan
  working-directory: infra/
```

## Apply Behaviour Reference

| Flag | Effect |
|---|---|
| `-auto-approve` | Skip interactive confirmation |
| `-target=resource` | Limit apply to specific resource(s) |
| `-var="key=val"` | Pass a variable inline |
| `-var-file=file.tfvars` | Load variables from a file |
| `-parallelism=N` | Concurrent resource operations (default 10) |
| `-refresh=false` | Skip state refresh (faster, less safe) |
| `-compact-warnings` | Summarise warnings instead of full detail |
