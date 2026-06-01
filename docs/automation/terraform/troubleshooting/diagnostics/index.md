# Terraform — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Terraform Diagnostics Workflow, Plan Inspection, State Inspection, Diagnostics Reference.
</div>

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
┌─────────────────────────────────────── Terraform — Diagnostics ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Terraform diagnostic sequence: capture logs → inspect plan JSON → check state → verify auth  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Log Capture                  │  │                Plan Analysis                │   │
│   │       TF_LOG=DEBUG tf plan &>debug.log       │  │       tf plan -out=p; tf show -json p       │   │
│   │        TF_LOG_PROVIDER=DEBUG for API         │  │     cat plan.json | jq .resource_changes    │   │
│   │         TF_LOG_PATH=./terraform.log          │  │       terraform state show <resource>       │   │
│   │         terraform version (in logs)          │  │       terraform refresh (resync state)      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    TF_LOG_PATH    = write log to file instead of stderr; useful for CI artifact collection    │   │
│   │          Plan JSON      = machine-readable plan; jq to find specific resource changes         │   │
│   │       .resource_changes= JSON field listing all planned changes with before/after values      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

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
