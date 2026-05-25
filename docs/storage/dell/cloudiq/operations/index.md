# CloudIQ — Operations


```text
┌────────────────────────────────────── Dell CloudIQ — Operations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ CloudIQ operations: daily health review, alert triage, capacity planning, and platform upkeep │   │
│   │   Health Ops: review scores, acknowledge alerts, apply recommendations, tune alert policies   │   │
│   │  Capacity Ops: review forecasts, expand pools, rebalance tiers, update quotas, export reports │   │
│   │      Platform Ops: update SCG firmware, rotate API tokens, audit users, review audit log      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily health → weekly capacity → monthly platform review → on-demand incident response             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Health Ops         │  │         Capacity Ops        │  │         Platform Ops        │   │
│   │        Review scores        │  │       Review forecasts      │  │          Update SCG         │   │
│   │      Acknowledge alerts     │  │         Expand pools        │  │      Rotate API tokens      │   │
│   │          Apply recs         │  │       Rebalance tiers       │  │         Audit users         │   │
│   │        Tune policies        │  │        Update quotas        │  │       Review audit log      │   │
│   │       Schedule reports      │  │        Export reports       │  │        Update alerts        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    CloudIQ web portal for all tasks; SCG management UI for relay health and array registration        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Frequency     │       Task       │       Owner       │       Tool       │      Output      │   │
│   │      Daily       │  Health review   │    Storage ops    │  CloudIQ portal  │    Alert log     │   │
│   │      Weekly      │ Capacity review  │    Storage ops    │  Forecast view   │  Expansion plan  │   │
│   │     Monthly      │ Platform review  │    Storage lead   │    Audit log     │  Review report   │   │
│   │    On-demand     │ Incident triage  │    On-call eng.   │   Diagnostics    │     SR / RCA     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: all operations via CloudIQ web portal and SCG management UI; no CLI required             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Health Ops     = Daily task of reviewing array health scores and acting on alerts or recs          │
│    Capacity Ops   = Weekly review of space forecasts; triggers pool expansion or data migration       │
│    Platform Ops   = Monthly review of SCG firmware, API tokens, user access, and audit log            │
│    Recommendation = CloudIQ actionable suggestion; ops team reviews and applies or dismisses          │
│    Alert policy   = Rule set defining which conditions generate CloudIQ alerts and at what threshold  │
│    Acknowledgment = Marking an alert as seen; does not resolve; audit trail records who and when      │
│    Pool expansion = Adding drives or nodes to a storage pool to extend capacity                       │
│    Tier rebalance = Moving data between performance tiers (NVMe/SAS/NL-SAS) based on activity         │
│    Audit log      = CloudIQ record of all user actions in portal; exported for compliance review      │
│    SCG update     = Applying new SCG firmware/software via CloudIQ-initiated remote update            │
│    Token rotation = Generating new API tokens and invalidating old ones on a scheduled cycle          │
│    Forecast view  = CloudIQ capacity trend graph showing projected full date per pool/volume          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
</div>
