# Terraform Plans

## terraform plan Basics

`terraform plan` generates an execution plan showing what changes Terraform will make.

```bash
# Basic plan — shows changes, does not apply
terraform plan

# Plan with variable file
terraform plan -var-file="envs/prod.tfvars"

# Plan with inline variable
terraform plan -var="instance_count=3"

# Plan with exit codes (useful in scripts)
terraform plan -detailed-exitcode
# 0 = no changes, 1 = error, 2 = changes pending
```

## Saving Plan Files

Saving a plan guarantees the apply step executes exactly what was reviewed.

```bash
# Save plan to a binary file
terraform plan -out=tfplan

# View a saved plan in human-readable form
terraform show tfplan

# View as JSON for scripting / audit
terraform show -json tfplan > plan.json

# Extract resource changes from JSON plan
terraform show -json tfplan | \
  jq '.resource_changes[] | {address, actions: .change.actions}'

# Apply from a saved plan (no confirmation prompt)
terraform apply tfplan
```

## Reading Plan Output

Understanding the plan output symbols:

| Symbol | Meaning |
|---|---|
| `+` green | Resource will be created |
| `-` red | Resource will be destroyed |
| `~` yellow | Resource will be updated in-place |
| `-/+` | Resource must be destroyed and recreated |
| `<=` | Data source will be read |

```
# Example plan output snippet
  # aws_instance.web will be updated in-place
  ~ resource "aws_instance" "web" {
        id            = "i-0abc12345def"
      ~ instance_type = "t3.small" -> "t3.medium"
        # (all other attributes unchanged)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

## Plan Review Checklist

Before approving and applying a plan, verify:

- No unexpected destroys (`-` or `-/+` on production resources)
- Resource counts match expectations
- No sensitive variable values exposed in plain text
- `instance_type`, `ami`, `cidr_block` changes are intentional
- Dependencies between resources are reflected correctly
- Module outputs used by other resources are still valid

```bash
# Highlight destroy operations in a saved JSON plan
terraform show -json tfplan | \
  jq '.resource_changes[] | select(.change.actions[] == "delete") | .address'
```

## Plan in CI/CD

```yaml
# GitHub Actions — post plan output to PR comment
- name: Terraform Plan
  id: plan
  run: terraform plan -no-color -out=tfplan 2>&1 | tee plan_output.txt
  working-directory: infra/
  continue-on-error: true

- name: Post Plan to PR
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const plan = fs.readFileSync('infra/plan_output.txt', 'utf8');
      const output = `#### Terraform Plan\n\`\`\`\n${plan.slice(0, 60000)}\n\`\`\``;
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: output
      });
```

## Useful Plan Flags

```bash
# Limit plan to specific resources
terraform plan -target=module.database

# Skip refreshing state (faster, use when you know state is current)
terraform plan -refresh=false

# Show only the plan, no preceding status messages
terraform plan -no-color 2>&1 | grep -E '^\s*(#|\+|~|-|Plan)'

# Generate a graph of the plan
terraform graph | dot -Tsvg > plan.svg
```
