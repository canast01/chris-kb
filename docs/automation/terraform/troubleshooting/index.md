# Terraform — Troubleshooting


```
┌───────────────────────────────────── Terraform — Troubleshooting ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Terraform troubleshooting: state errors, provider errors, plan/apply failures, lock errors  │   │
│   │               Enable debug: TF_LOG=DEBUG terraform plan 2>&1 | tee tf-debug.log               │   │
│   │           Provider errors: TF_LOG_PROVIDER=DEBUG for provider-level API call logging          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Common Issues                 │  │             Diagnostic Commands             │   │
│   │          Error acquiring state lock          │  │       terraform plan (verbose output)       │   │
│   │        Provider authentication error         │  │             TF_LOG=DEBUG tf plan            │   │
│   │           Resource already exists            │  │       terraform state show <resource>       │   │
│   │       Cycle error in dependency graph        │  │         terraform graph | dot -Tpng         │   │
│   │       State drift: plan shows changes        │  │         terraform refresh then plan         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           TF_LOG=DEBUG   = environment var; levels: TRACE, DEBUG, INFO, WARN, ERROR           │   │
│   │        Cycle error    = circular dependency between resources; use depends_on carefully       │   │
│   │         Already exists = resource in provider but not in state; fix: terraform import         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Provider errors, state conflicts, and workspace problems.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Debug logging, plan inspection, and validation tools.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate unresolved issues.</span>
</a>

</div>
