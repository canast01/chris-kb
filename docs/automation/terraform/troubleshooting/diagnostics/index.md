# Terraform — Diagnostics

## Terraform Diagnostics Workflow

```mermaid
graph LR
    symptom["Symptom /\nUnexpected Output"]
    validate["terraform validate\n(syntax check)"]
    fmtCheck["terraform fmt -check\n(formatting)"]
    planJSON["terraform plan -out=tfplan\nterraform show -json tfplan"]
    jqFilter["jq filter:\nresource_changes"]
    graph["terraform graph\n| dot -Tsvg"]
    stateList["terraform state list"]
    stateShow["terraform state show\n<resource>"]
    debugLog["TF_LOG=TRACE\nTF_LOG_PATH=debug.log"]
    resolved["Root cause\nidentified"]

    symptom --> validate
    validate --> fmtCheck
    fmtCheck --> planJSON
    planJSON --> jqFilter
    jqFilter --> resolved
    symptom --> stateList
    stateList --> stateShow
    stateShow --> resolved
    symptom --> graph
    graph --> resolved
    symptom --> debugLog
    debugLog --> resolved
```
```

## Validation and Syntax Checks

```bash
# Validate configuration without connecting to provider
terraform validate

# Format and check for syntax errors
terraform fmt -check -recursive
echo $?   # non-zero means formatting issues found

# Use -json output for easier scripted inspection
terraform plan -json 2>/dev/null | jq '.diagnostics'
```

## Plan Inspection

```bash
# Graph the dependency tree to identify cycles
terraform graph | dot -Tsvg > graph.svg

# Inspect a saved plan in JSON format
terraform plan -out=tfplan
terraform show -json tfplan | jq '.resource_changes[] | {address, actions: .change.actions}'

# Highlight destroy operations
terraform show -json tfplan | \
  jq '.resource_changes[] | select(.change.actions[] == "delete") | .address'

# Check exit code for scripted drift detection
terraform plan -detailed-exitcode
# 0 = no changes, 1 = error, 2 = changes present
```

## State Inspection

```bash
# List all resources in state
terraform state list

# Show details for a specific resource
terraform state show aws_instance.web01

# Pull remote state for inspection
terraform state pull | jq '.resources[] | {type, name}'

# Show all outputs
terraform output
terraform output -json
```

## Diagnostics Reference

| Tool | Command | Use case |
|---|---|---|
| Debug logging | `TF_LOG=DEBUG terraform plan` | Trace provider API calls |
| Validate | `terraform validate` | Check configuration syntax |
| fmt check | `terraform fmt -check -recursive` | Find formatting issues |
| Graph | `terraform graph \| dot -Tsvg > graph.svg` | Visualise dependency cycles |
| State list | `terraform state list` | Confirm resources tracked in state |
| State show | `terraform state show <resource>` | Inspect a specific resource's attributes |
| Plan JSON | `terraform show -json tfplan` | Parse plan output in scripts |
