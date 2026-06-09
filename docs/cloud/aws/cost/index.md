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

```text
┌───────────────────────────── EC2 Pricing Models — Commitment vs Discount ─────────────────────────────┐
│                                                                                                       │
│    Longer commitment = larger discount; Spot gives biggest saving with interruption risk.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      Model                                   │  │      Key Facts                              │   │
│   │  On-Demand                                   │  │  No commitment; full price; per second      │   │
│   │  Standard Reserved (1 year)                  │  │  Up to 72% off; same config only            │   │
│   │  Standard Reserved (3 year)                  │  │  Maximum RI discount; locked config         │   │
│   │  Convertible Reserved (1/3 yr)               │  │  Up to 66% off; can exchange family         │   │
│   │  Compute Savings Plan                        │  │  Up to 66% off; EC2+Fargate+Lambda          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Reserved and Savings Plans are billed whether you use the capacity or not.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      Model (continued)                       │  │      Key Facts                              │   │
│   │  EC2 Instance Savings Plan                   │  │  Up to 72% off; same family + Region        │   │
│   │  Spot Instances                              │  │  Up to 90% off; 2-min interruption          │   │
│   │  Dedicated Host                              │  │  Physical server; BYOL; compliance          │   │
│   │  Dedicated Instance                          │  │  On dedicated HW; per-instance charge       │   │
│   │  Free Tier (12 months new accounts)          │  │  750 hrs/mo t2/t3.micro; then billed        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    EC2 billing infrastructure · AWS Cost Explorer API · CUR exported to S3                            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    On-Demand     = No commitment; highest per-unit cost; most flexible                                │
│    Reserved RI   = 1 or 3-year commitment to capacity; up to 72% discount                             │
│    Savings Plan  = $/hr flexible commitment; applies across instance families                         │
│    Spot          = Unused EC2 capacity auction; up to 90% off; interruptible                          │
│    Dedicated Host= Physical server commitment; BYOL compliant; socket/core visibility                 │
│    Free Tier     = 750 hrs/mo t2.micro or t3.micro for 12 months on new accounts                      │
│    RI Marketplace= Sell unused Standard RIs to other AWS customers                                    │
│    Utilisation   = Percentage of purchased Reserved/Savings Plan capacity actually used               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌─────────────────────────── AWS Support Plans — Features and Response Times ───────────────────────────┐
│                                                                                                       │
│    Five support tiers; higher tiers add TAMs, faster response, and architectural guidance.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Basic / Developer Plans                  │  │      Business / Enterprise On-Ramp          │   │
│   │  Basic: free; documentation only             │  │  Business: $100/mo or 10% of charges        │   │
│   │  Basic: AWS Health Dashboard + forums        │  │  Business: all contacts; 24/7 phone         │   │
│   │  Developer: $29/mo or 3% of charges          │  │  Business: <1h critical response            │   │
│   │  Developer: 1 contact; biz-hours email       │  │  Enterprise On-Ramp: $5500/mo min           │   │
│   │  Developer: general guidance + sandbox       │  │  Ent On-Ramp: TAM pool; <30 min crit        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Business adds 24/7 support + full Trusted Advisor; Enterprise adds dedicated TAM.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Enterprise Plan                          │  │      Trusted Advisor Checks by Tier         │   │
│   │  Enterprise: $15000/mo or % of charges       │  │  Basic: 6 core security checks only         │   │
│   │  Enterprise: dedicated Technical Acct        │  │  Developer: same 6 checks as Basic          │   │
│   │  Enterprise: <15 min business-critical       │  │  Business: ALL ~500+ Trusted Advisor        │   │
│   │  Enterprise: Well-Architected Reviews        │  │  Enterprise: ALL checks + API access        │   │
│   │  Enterprise: Concierge; billing review       │  │  Proactive recommendations: Ent only        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    AWS Support infrastructure · TAM communication channels · Trusted Advisor service                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    TAM            = Technical Account Manager; dedicated expert in Enterprise plan                    │
│    Trusted Advisor= Automated checks across cost, performance, security, fault tolerance              │
│    Basic          = Free; 7 Trusted Advisor checks; Health Dashboard; community forums                │
│    Developer      = $29/mo or 3% of monthly charges; 1 primary contact; 12-24h response               │
│    Business       = $100+/mo; unlimited contacts; 24/7 phone+chat; <1h prod-down response             │
│    Enterprise On-Ramp= $5500/mo; TAM pool; 30-min critical response; WAR reviews                      │
│    Enterprise     = $15000/mo; dedicated TAM; 15-min critical; Concierge team access                  │
│    Infrastructure Event Mgmt = Enterprise only; AWS support during launches/migrations                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

<a class="kb-card" href="cost-allocation-tags/"><strong>Cost Allocation Tags</strong><span>Cost tag activation, reporting, and ownership mapping.</span></a>
<a class="kb-card" href="cost-explorer/"><strong>Cost Explorer</strong><span>Interactive cost analysis, filter views, usage patterns, and historical trend exploration.</span></a>

</div>

