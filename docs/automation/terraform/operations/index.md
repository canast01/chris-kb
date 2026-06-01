# Terraform — Operations



<div class="kb-summary">
Terraform — Operations reference.
</div>

```
┌─────────────────────────────────────── Terraform — Operations ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Terraform operations: init, plan, apply, state management, workspace management, import    │   │
│   │            Day-to-day: create branch → modify .tf → plan → review → apply → commit            │   │
│   │    State ops: terraform state list/show/mv/rm — use with caution; always backup state first   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Core Operations                │  │               State Operations              │   │
│   │                terraform init                │  │             terraform state list            │   │
│   │          terraform plan -out=tfplan          │  │       terraform state show <resource>       │   │
│   │            terraform apply tfplan            │  │            terraform state mv A B           │   │
│   │         terraform destroy -target=X          │  │        terraform state rm <resource>        │   │
│   │       terraform workspace select prod        │  │           terraform import addr ID          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    terraform import = bring existing resource under Terraform management; writes state only   │   │
│   │  terraform state rm= removes resource from state without destroying it; orphans the resource  │   │
│   │        -target       = apply/destroy specific resource; use sparingly; state can drift        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────── Terraform — Operations ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Terraform operations: init, plan, apply, state management, workspace management, import    │   │
│   │            Day-to-day: create branch → modify .tf → plan → review → apply → commit            │   │
│   │    State ops: terraform state list/show/mv/rm — use with caution; always backup state first   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Core Operations                │  │               State Operations              │   │
│   │                terraform init                │  │             terraform state list            │   │
│   │          terraform plan -out=tfplan          │  │       terraform state show <resource>       │   │
│   │            terraform apply tfplan            │  │            terraform state mv A B           │   │
│   │         terraform destroy -target=X          │  │        terraform state rm <resource>        │   │
│   │       terraform workspace select prod        │  │           terraform import addr ID          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    terraform import = bring existing resource under Terraform management; writes state only   │   │
│   │  terraform state rm= removes resource from state without destroying it; orphans the resource  │   │
│   │        -target       = apply/destroy specific resource; use sparingly; state can drift        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>init, plan, apply, destroy, state, workspace, import, and output commands.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Drift detection, state validation, and resource health.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Plan review, apply workflows, and operational procedures.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install &amp; Upgrade</strong>
  <span>Terraform version management and provider upgrades.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup &amp; Restore</strong>
  <span>State file backup and disaster recovery procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for Terraform operations.</span>
</a>

</div>
