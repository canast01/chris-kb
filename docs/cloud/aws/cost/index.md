# AWS Cost

<div class="kb-summary">
AWS cost management combines visibility tools (Cost Explorer, Anomaly Detection) with spend optimisation (Reserved Instances, Savings Plans) and governance via Budgets and cost allocation tags. Coverage includes chargeback tagging, RI/Savings Plan planning, and anomaly investigation workflows.
</div>

```text
┌───────────────────────────────────────── AWS Cost Management ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 AWS Cost Management — Visibility, Optimisation, and Governance                │   │
│   │      Cost Explorer: historical and forecasted spend by service, account, region, and tag      │   │
│   │     Budgets: threshold alerts via email or SNS; action budgets can auto-apply IAM policies    │   │
│   │  Reserved Instances + Savings Plans: commit to 1 or 3 years for up to 72% discount on EC2/RDS │   │
│   │   Cost Anomaly Detection: ML-based; detects unexpected spend spikes and notifies immediately  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Visibility (Explorer/CUR) feeds optimisation (RI/SP) and governance (Budgets/Anomaly/Tags)         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Cost Explorer        │  │           Budgets           │  │         Optimisation        │   │
│   │  Service breakdowns: daily  │  │   Cost threshold: $+alert   │  │  Reserved Instances: 1/3yr  │   │
│   │   Account + region filters  │  │   Usage budget: unit+alert  │  │    Savings Plans: compute   │   │
│   │     Tag-based chargeback    │  │   Action budget: IAM deny   │  │  Spot Instances: -90% cost  │   │
│   │ Rightsizing: recommendations│  │    Forecast: alert at 80%   │  │    Anomaly Detection: ML    │   │
│   │   CUR: hourly cost detail   │  │   SNS: alert notification   │  │   Cost alloc tags: billing  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Cost Explorer provides visibility · Budgets alert on thresholds · Optimisation reduces total spend │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Cost Explorer   │     Budgets      │    RI / Savings   │     Anomaly      │       Tags       │   │
│   │ By service: EC2  │  Monthly limit   │   RI coverage %   │ ML alert: spike  │  Activate tags   │   │
│   │ By account: all  │  Forecast alert  │   SP utilisation  │ Investigate: who │  Cost alloc tag  │   │
│   │ Rightsizing recs │  Action budget   │  RI renewal: when │  Anomaly report  │ Chargeback: team │   │
│   │  Forecast: 3mo   │    SNS notify    │   Spot: savings   │ Suppress: known  │  Tagging policy  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS billing infrastructure · CUR data in S3 · Cost Explorer API · Budget notifications via SNS/email │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cost Explorer   = AWS console and API tool for analysing spend trends by service, account, tag,      │
│  CUR             = Cost and Usage Report; detailed hourly billing data exported to S3 for FinOps tools│
│  Budget          = Spend threshold with alert and optional action; types: cost, usage, RI, Savings    │
│  Action budget   = Budget that auto-applies SCPs or IAM policies when spend threshold is crossed      │
│  Reserved Instance= 1 or 3-year commitment to EC2/RDS capacity; up to 72% discount vs on-demand       │
│  Savings Plan    = Flexible commitment to $/hr compute spend; applies to EC2, Fargate, Lambda         │
│  Spot Instance   = Unused EC2 capacity at up to 90% discount; can be reclaimed with 2-min notice      │
│  RI Coverage     = Percentage of eligible usage hours covered by Reserved Instances; target >80%      │
│  Cost alloc tag  = Resource tag activated in billing console; appears as column in Cost Explorer/CUR  │
│  Chargeback      = Attributing AWS costs to business units or teams using cost allocation tags        │
│  Anomaly Detection= ML model that learns normal spend patterns and alerts on statistically unexpected │
│  Rightsizing     = Cost Explorer recommendation to downsize underutilised EC2 or RDS instances        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

![AWS Cost Architecture](../../../assets/aws-cost-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cost-explorer-billing/">
  <strong>Cost Explorer / Billing</strong>
  <span>Billing review, trends, service cost, and chargeback notes.</span>
</a>

<a class="kb-card" href="budgets/">
  <strong>Budgets</strong>
  <span>Budget alerts, thresholds, owners, and review cadence.</span>
</a>

<a class="kb-card" href="cost-anomaly-detection/">
  <strong>Cost Anomaly Detection</strong>
  <span>Unexpected spend detection and investigation workflow.</span>
</a>

<a class="kb-card" href="reserved-instances/">
  <strong>Reserved Instances</strong>
  <span>RI planning, coverage, utilization, and renewal notes.</span>
</a>

<a class="kb-card" href="savings-plans/">
  <strong>Savings Plans</strong>
  <span>Savings Plan coverage, commitments, utilization, and review.</span>
</a>

<a class="kb-card" href="cost-allocation-tags/">
  <strong>Cost Allocation Tags</strong>
  <span>Cost tag activation, reporting, and ownership mapping.</span>
</a>

</div>
