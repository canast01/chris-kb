# Automation

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Automation Overview                              │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Scripting   │  │   REST API   │  │  CI/CD       │              │
│  │  PowerShell  │  │  Pure REST   │  │  GitHub      │              │
│  │  Python      │  │  vSphere API │  │  Actions     │              │
│  │  Ansible     │  │  AWS/Azure   │  │  Workflows   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                      │
│  ┌──────▼─────────────────▼─────────────────▼────────────────────┐  │
│  │              Automation Targets                               │  │
│  │   vSphere · NSX · FlashArray · PowerMax · Linux · Windows    │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  IaC (Terraform)                                           │     │
│  │  Plan ──► Apply ──► State ──► Drift detect ──► Destroy    │     │
│  └────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="ansible/"><strong>Ansible</strong><span>Inventory, playbooks, roles, variables, vault, and infrastructure automation.</span></a>
<a class="kb-card" href="powershell/"><strong>PowerShell</strong><span>Scripts, modules, remoting, reporting, and Windows/VMware automation.</span></a>
<a class="kb-card" href="python/"><strong>Python</strong><span>Scripts, REST API clients, parsing, reporting, and cross-platform automation.</span></a>
<a class="kb-card" href="terraform/"><strong>Terraform</strong><span>State management, modules, plans, applies, drift detection, and provider config.</span></a>
<a class="kb-card" href="github-actions/"><strong>GitHub Actions</strong><span>Workflows, CI/CD pipelines, validation, publishing, and secret management.</span></a>
</div>
