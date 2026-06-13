---
tags:
  - azure
---
# Azure Cost

<div class="kb-summary">
Azure Cost articles, operational checks, troubleshooting notes, and references.

*Applies to: Azure*
</div>

```text
┌──────────────────────────────────────── Azure Cost Management ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Azure Cost Management — Visibility, Budgets, Reservations, and Optimisation          │   │
│   │    Cost Management + Billing: analyse spend by subscription, RG, service, tag, and location   │   │
│   │    Budgets: cost or usage threshold alerts; linked to action groups for email or automation   │   │
│   │       Reservations: 1 or 3-year committed use for VMs, SQL, Storage; up to 72% discount       │   │
│   │  Azure Advisor: right-sizing, RI recommendations, idle resources, and cost savings estimates  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Cost visibility feeds budget alerts · Advisor finds savings · Reservations commit for discounts    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Cost Analysis        │  │           Budgets           │  │         Optimisation        │   │
│   │     By service: monthly     │  │      Threshold: $ alert     │  │     Reservations: 1/3yr     │   │
│   │       By tag: team/env      │  │     Forecast: 80% alert     │  │     Savings Plans: flex     │   │
│   │    By subscription: trend   │  │     Action group: email     │  │     Advisor: rightsizing    │   │
│   │   Export: storage account   │  │      Anomaly alerts: ML     │  │     Spot VMs: -90% cost     │   │
│   │   Cost alloc: tags billing  │  │    Budget: scope mgmt grp   │  │    Idle: deallocate + del   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Cost analysis provides visibility · Budgets alert on thresholds                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Cost Analysis   │     Budgets      │    Reservations   │  Savings Plans   │  Azure Advisor   │   │
│   │ By service view  │  Monthly limit   │   VM: 1yr save%   │   Compute flex   │   Resize: -30%   │   │
│   │ Tag: chargeback  │  Forecast alert  │    SQL: 3yr 72%   │   DB flexible    │ Idle: terminate  │   │
│   │  Export: daily   │    Action grp    │   Coverage: view  │   Storage flex   │  RI: recommend   │   │
│   │ Anomaly: detect  │  Scope: sub/RG   │   Utilise: >80%   │   Spend commit   │  Cost: estimate  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure billing infrastructure · Cost Management API · Export storage account · Action Group SNS/email │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cost Management + Billing= Azure portal blade for analysing and controlling Azure spend              │
│  Budget          = Spending threshold; types: cost (£/$) or usage; alerts at % of limit               │
│  Action Group    = Named set of actions (email, SMS, webhook, Logic App) triggered by alerts          │
│  Reservation     = 1 or 3-year committed use purchase; applies to specific VM size or service         │
│  Savings Plan    = Flexible spend commitment ($/hr); applies across regions and eligible services     │
│  Spot VM         = Low-priority VM using spare Azure capacity; up to 90% cheaper; can be evicted      │
│  Azure Advisor   = Personalised recommendations for cost, security, performance, and reliability      │
│  Cost allocation = Attributing Azure costs to teams/apps via resource tags; chargeback enablement     │
│  Cost export     = Scheduled export of usage data to Azure Blob Storage; feeds BI tools / Power BI    │
│  Anomaly alert   = AI-detected unexpected spend spike on subscription, resource group, or service     │
│  Reserved capacity= Azure Reservation; pre-purchase a discount for predictable workloads              │
│  Rightsizing     = Advisor recommendation to reduce VM SKU when CPU/memory consistently underused     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
