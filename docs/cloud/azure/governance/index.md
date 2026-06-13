---
tags:
  - azure
---
# Azure Governance

<div class="kb-summary">
Azure Governance articles, operational checks, troubleshooting notes, and references.
</div>

```text
┌────────────────────────────────────── Azure Governance Overview ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Azure Governance — Policy, Initiatives, Compliance, and Management Groups           │   │
│   │   Management Groups: policy and RBAC applied at MG scope cascade to all subscriptions below   │   │
│   │    Azure Policy: define rules for resource configs; effects: Audit, Deny, DeployIfNotExists   │   │
│   │ Initiatives: group multiple policy definitions; assign as one unit (e.g. CIS Azure Benchmark) │   │
│   │     Compliance review: policy state dashboard; non-compliant resources; remediation tasks     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Management Groups scope policies · Policy defines rules · Initiatives bundle them                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Management Groups      │  │         Azure Policy        │  │          Compliance         │   │
│   │     Root: tenant root MG    │  │   Effect: Audit/Deny/DINE   │  │    Dashboard: compliant %   │   │
│   │     Custom MG hierarchy     │  │     Scope: MG/sub/RG/res    │  │   Non-compliant: list/fix   │   │
│   │    Inheritance: sub → RG    │  │    Initiatives: CIS/NIST    │  │    Remediation: auto task   │   │
│   │   Policy scope: inherited   │  │   Parameters: reuse policy  │  │    Exemption: time-bound    │   │
│   │     Tag policy: org-wide    │  │     Assignment: + params    │  │   Audit log: activity log   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Management Groups establish hierarchy · Policy defines rules · Compliance validates and remediates │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Mgmt Groups    │   Azure Policy   │    Initiatives    │    Compliance    │    Exemptions    │   │
│   │    Create MG     │  New definition  │    Assign init    │   View %: pass   │   Create exemp   │   │
│   │  Move sub to MG  │  Assign policy   │     CIS Az 1.4    │  Non-compliant   │  Waiver: reason  │   │
│   │ Policy: inherit  │   Effect: Deny   │   NIST SP800-53   │   Remediation    │   Expiry: date   │   │
│   │    RBAC at MG    │  DeployIfNotEx   │   Custom bundled  │  Mitigate task   │  Scope: RG/res   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure Resource Manager · Policy engine · Management Group hierarchy · Activity Log infrastructure    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Management Group   = Container above subscriptions; scoping boundary for policy and RBAC             │
│  Azure Policy       = Service for defining, assigning, and evaluating compliance rules on resources   │
│  Policy definition  = JSON rule with conditions and effects; built-in or custom; parameterised        │
│  Policy assignment  = Applies a definition or initiative to a scope with specific parameter values    │
│  Effect: Audit      = Logs non-compliant resources without blocking; compliance reporting only        │
│  Effect: Deny       = Blocks creation or update of non-compliant resources; hard enforcement          │
│  Effect: DINE       = DeployIfNotExists; deploys remediation resource when policy condition is met    │
│  Initiative         = Collection of policy definitions assigned together; simplifies compliance sets  │
│  Remediation task   = Auto-runs the DINE effect on existing non-compliant resources in scope          │
│  Exemption          = Excludes a resource or scope from a policy assignment; time-bound or permanent  │
│  Compliance state   = Per-resource evaluation result: Compliant / Non-compliant / Not started / Exempt│
│  Tagging policy     = Policy enforcing required tags (e.g. Owner, Environment) on all resource        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="assignments/">
  <strong>Assignments</strong>
  <span>Policy and initiative assignments scoped to management groups, subscriptions, or resource groups.</span>
</a>

<a class="kb-card" href="azure-policy/">
  <strong>Azure Policy</strong>
  <span>Define and enforce compliance rules for resource configuration, tagging, and allowed SKUs.</span>
</a>

<a class="kb-card" href="compliance-review/">
  <strong>Compliance Review</strong>
  <span>Policy compliance state review, non-compliant resource enumeration, and remediation tracking.</span>
</a>

<a class="kb-card" href="exemptions/">
  <strong>Exemptions</strong>
  <span>Time-bound or permanent exclusions from policy effects for justified non-compliant resources.</span>
</a>

<a class="kb-card" href="initiatives/">
  <strong>Initiatives</strong>
  <span>Collections of related policies deployed together as a compliance or security benchmark.</span>
</a>

<a class="kb-card" href="management-groups/">
  <strong>Management Groups</strong>
  <span>Hierarchy above subscriptions for applying policy and RBAC across multiple subscriptions.</span>
</a>

<a class="kb-card" href="subscriptions/">
  <strong>Subscriptions</strong>
  <span>Billing and access boundary; subscription layout, ownership, and governance standards.</span>
</a>

<a class="kb-card" href="tagging-standards/">
  <strong>Tagging Standards</strong>
  <span>Required and recommended tag keys, allowed values, and enforcement policy definitions.</span>
</a>
</div>
