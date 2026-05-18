# Azure Cost

<div class="kb-summary">
Azure Cost articles, operational checks, troubleshooting notes, and references.
</div>

```
┌──────────────────────────────────────────────────────────────┐
│                   Azure Cost Overview                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │  Subscriptions  (billing boundary)                  │     │
│  └────────────────────────────┬────────────────────────┘     │
│                               │                              │
│                               ▼                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Cost Management                           │  │
│  │                                                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │  │
│  │  │  Budgets     │  │  Cost        │  │  Advisor    │  │  │
│  │  │  (thresholds)│  │  Analysis    │  │  Recomm.    │  │  │
│  │  └──────┬───────┘  └──────────────┘  └─────────────┘  │  │
│  └─────────┼──────────────────────────────────────────────┘  │
│            │ threshold breach                                 │
│            ▼                                                  │
│  ┌─────────────────┐    ┌─────────────────────────────────┐   │
│  │  Budget Alert   │──► │  Action Group (email/webhook)   │   │
│  └─────────────────┘    └─────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="advisor-recommendations/">
  <strong>Advisor Recommendations</strong>
  <span>Right-sizing, reserved instance, and idle resource recommendations from Azure Advisor.</span>
</a>

<a class="kb-card" href="budgets/">
  <strong>Budgets</strong>
  <span>Spending thresholds with email or action group alerts when costs approach or exceed budget.</span>
</a>

<a class="kb-card" href="cost-alerts/">
  <strong>Cost Alerts</strong>
  <span>Anomaly detection and budget breach alerts for subscriptions, resource groups, or services.</span>
</a>

<a class="kb-card" href="cost-allocation-tags/">
  <strong>Cost Allocation Tags</strong>
  <span>Tagging strategy to split and attribute costs by team, environment, or application.</span>
</a>

<a class="kb-card" href="cost-management/">
  <strong>Cost Management</strong>
  <span>Usage analysis, cost breakdowns by service, and trend reports across subscriptions.</span>
</a>

<a class="kb-card" href="cost-management-billing/">
  <strong>Cost Management Billing</strong>
  <span>Invoice review, payment methods, subscription billing details, and EA enrollment management.</span>
</a>

<a class="kb-card" href="reservations/">
  <strong>Reservations</strong>
  <span>1- or 3-year compute reservations for VMs, SQL, and other services to reduce costs up to 72%.</span>
</a>

<a class="kb-card" href="savings-plans/">
  <strong>Savings Plans</strong>
  <span>Flexible hourly spend commitments for compute (VMs, AKS, App Service) with up to 65% savings.</span>
</a>
</div>
