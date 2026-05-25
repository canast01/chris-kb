# AWS Governance

<div class="kb-summary">
AWS governance is structured around AWS Organizations with SCPs enforcing preventive guardrails at the OU level and AWS Config handling detective compliance. Coverage includes account structure, Service Control Policies, tagging standards, and compliance review.
</div>

```text
┌─────────────────────────────────────── AWS Governance Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  AWS Governance — Organizations, SCPs, Config, and Compliance                 │   │
│   │    AWS Organizations: root account > OUs > member accounts; SCPs enforced at each OU level    │   │
│   │  Service Control Policies: preventive guardrails; deny actions before IAM even evaluates them │   │
│   │    AWS Config: detective compliance; records every resource config change; evaluates rules    │   │
│   │    Tagging standards: mandatory tags enforced by Config rules; used for cost and compliance   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Organizations provides structure · SCPs prevent violations · Config detects drift                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      AWS Organizations      │  │   Service Control Policies  │  │          AWS Config         │   │
│   │    Root: management acct    │  │   JSON policy: allow/deny   │  │  Config recorder: all types │   │
│   │    OUs: env / team / app    │  │     OU-level attachment     │  │   Rules: managed + custom   │   │
│   │  Member accounts: isolated  │  │   Deny: regions, services   │  │  Compliance: pass/fail/N/A  │   │
│   │     Consolidated billing    │  │   Allow-list pattern: safe  │  │   Remediation: auto/manual  │   │
│   │    Account structure std.   │  │    Guardrail: no root key   │  │   Config: S3 delivery dest  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Organizations structures accounts · SCPs prevent bad actions                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Organizations   │       SCPs       │     AWS Config    │     Tagging      │    Compliance    │   │
│   │  Create account  │   Attach to OU   │  Enable recorder  │  Mandatory tags  │  Audit reports   │   │
│   │    Move to OU    │  Deny: eu-west   │  Add managed rule │ Tag policy: org  │  Non-compliant?  │   │
│   │ Invite accounts  │  Test: SCP sim   │  Remediation auto │ Tagging standard │   Security Hub   │   │
│   │Consolidated bill │ Exception: allow │  Delivery: S3+SNS │ Cost alloc tags  │ Frameworks: CIS  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS global infrastructure · Organizations API · Config delivery to S3 · CloudTrail audit trail       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Organizations   = AWS multi-account management service; enforces billing and governance hierarchy    │
│  OU              = Organisational Unit; logical account grouping; SCPs attach at this level           │
│  SCP             = Service Control Policy; max permission boundary for all IAM in attached accounts   │
│  Preventive guardrail= SCP that blocks actions before IAM policy is evaluated; hard boundary          │
│  Detective guardrail = Config rule that detects non-compliant resources after they exist              │
│  Config recorder = Tracks configuration snapshots and changes for all or selected resource types      │
│  Config rule     = Evaluates resource configs against defined conditions; managed or custom Lambda    │
│  Remediation action= Auto-fix triggered by Config rule non-compliance; e.g. delete public S3 bucket   │
│  Tag policy      = Organizations policy enforcing consistent tag keys/values across accounts          │
│  Consolidated billing= Single bill for all accounts in org; volume discounts and RI sharing applies   │
│  Account structure = Pattern of management/audit/log-archive/workload accounts following landing zone │
│  SCP allow-list   = Deny-all-except pattern; safer than deny-list; only permits explicitly listed     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

![AWS Governance Architecture](../../../assets/aws-governance-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="aws-config/">
  <strong>AWS Config</strong>
  <span>Resource inventory, compliance rules, and drift review.</span>
</a>

<a class="kb-card" href="aws-organizations/">
  <strong>AWS Organizations</strong>
  <span>Accounts, OUs, policies, and governance boundaries.</span>
</a>

<a class="kb-card" href="service-control-policies/">
  <strong>Service Control Policies</strong>
  <span>SCP design, guardrails, testing, and exceptions.</span>
</a>

<a class="kb-card" href="account-structure/">
  <strong>Account Structure</strong>
  <span>Account layout, ownership, environment separation, and standards.</span>
</a>

<a class="kb-card" href="tagging-standards/">
  <strong>Tagging Standards</strong>
  <span>Required tags, cost tags, ownership, and compliance.</span>
</a>

<a class="kb-card" href="compliance-review/">
  <strong>Compliance Review</strong>
  <span>Control review, evidence, drift, and remediation tracking.</span>
</a>

</div>
