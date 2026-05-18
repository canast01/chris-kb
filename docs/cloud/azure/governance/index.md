# Azure Governance

<div class="kb-summary">
Azure Governance articles, operational checks, troubleshooting notes, and references.
</div>

```
┌────────────────────────────────────────────────────────────┐
│                  Azure Governance Hierarchy                │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Management Group  (tenant root / custom hierarchy)  │  │
│  └──────────────────────────┬─────────────────────────┘  │
│                             │ Policy + RBAC inherit ▼     │
│  ┌──────────────────────────┴─────────────────────────┐   │
│  │  Subscription  (billing + access boundary)         │   │
│  └──────────────────────────┬───────────────────────┘    │
│                             │ Policy + RBAC inherit ▼     │
│  ┌──────────────────────────┴────────────────────────┐    │
│  │  Resource Group  (lifecycle container)            │    │
│  └──────────────────────────┬──────────────────────┘     │
│                             │                             │
│  ┌──────────────────────────┴──────────────────────────┐  │
│  │  Resources  (VMs, Storage, Network, etc.)           │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                            │
│  Azure Policy ──► audit / deny / modify at any scope      │
│  RBAC         ──► role assignments inherit downward       │
└────────────────────────────────────────────────────────────┘
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
