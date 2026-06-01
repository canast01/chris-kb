# COD — Operations

<div class="kb-summary">
COD — Operations reference: CLI Reference, Health Checks, Procedures, Install & Upgrade, and 2 more.
</div>

```text
┌──────────────────────────────────────── Dell CoD — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   CoD operations: monitor dark capacity levels, plan key purchases, apply keys, audit usage   │   │
│   │      Monitoring: CloudIQ tracks used vs locked capacity; alerts at configurable threshold     │   │
│   │     Planning: forecast capacity needs 3-6 months ahead; pre-purchase keys to avoid delays     │   │
│   │    Key application: import key file via array management UI or CLI; instant capacity unlock   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Monitor usage → hit threshold → raise change request → purchase key → apply → verify               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Monitoring         │  │           Planning          │  │        Key Operations       │   │
│   │      CloudIQ dashboard      │  │       Forecast review       │  │         Purchase key        │   │
│   │       Capacity alerts       │  │         Pre-buy keys        │  │         Download key        │   │
│   │       Threshold config      │  │           Raise CR          │  │        Apply to array       │   │
│   │        Dark cap view        │  │        Lead time plan       │  │        Verify unlock        │   │
│   │        Monthly audit        │  │       Budget approval       │  │         Update CMDB         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Monthly review: check dark capacity remaining, update forecast, ensure pre-purchased keys ready    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Frequency     │       Task       │       Owner       │       Tool       │      Output      │   │
│   │      Daily       │   Alert triage   │    Storage ops    │     CloudIQ      │    Alert log     │   │
│   │     Monthly      │  Capacity audit  │    Storage lead   │ CloudIQ + portal │ Forecast report  │   │
│   │    Quarterly     │ Key pre-purchase │    Storage lead   │ Licensing portal │   Keys on hand   │   │
│   │    On-demand     │ Key application  │    Storage eng.   │  Array GUI/CLI   │  Capacity live   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: dark drives/nodes on array already installed; key activates firmware to expose them      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dark capacity  = Installed but locked drives or nodes; appear as locked in array management        │
│    Threshold alert = CloudIQ fires when used capacity / total CoD capacity exceeds set percentage     │
│    Pre-buy key    = Purchasing CoD keys before threshold is hit; avoids procurement delay             │
│    Lead time      = Procurement approval plus Dell order processing; typically 1-5 business days      │
│    Change request = ITSM CR raised before CoD key application; documents capacity change reason       │
│    Capacity audit = Monthly review of all arrays: dark remaining, used, forecast, keys on hand        │
│    CMDB update    = After key applied, update CMDB with new licensed capacity per array               │
│    Verify unlock  = After key application, confirm in array GUI that new capacity is visible          │
│    Budget approval = Finance sign-off required for CoD key purchase; include in capacity plan         │
│    Keys on hand   = Purchased but unapplied CoD keys stored in licensing portal for quick use         │
│    Monthly audit  = Formal review; compare used vs dark vs keys on hand across all CoD arrays         │
│    Forecast review = Projecting when next CoD key will be needed based on growth trend                │
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
