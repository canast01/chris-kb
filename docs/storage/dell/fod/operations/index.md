# FOD — Operations

┌──────────────────────────────────────── Dell FoD — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FoD operations: feature request handling, key purchase, application, and quarterly audit   │   │
│   │    Request: app team requests new feature; storage team validates need and firmware prereq    │   │
│   │     Purchase: raise CR, get approval, buy key from portal, store in vault, apply to array     │   │
│   │       Audit: quarterly review of all active FoD features per array; CMDB reconciliation       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Feature request → prereq check → CR → purchase → apply → verify → CMDB → quarterly audit           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Request Ops         │  │           Key Ops           │  │          Audit Ops          │   │
│   │        Feature intake       │  │           Raise CR          │  │       Quarterly review      │   │
│   │       Need validation       │  │         Purchase key        │  │        CMDB reconcile       │   │
│   │       FW prereq check       │  │          Apply key          │  │        Key inventory        │   │
│   │       Budget sign-off       │  │        Verify feature       │  │      Unused key review      │   │
│   │       Test in non-prod      │  │         Update CMDB         │  │       Portal reconcile      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All FoD key applications require approved CR and documented business justification                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Frequency     │       Task       │       Owner       │       Tool       │      Output      │   │
│   │    On-demand     │   Key purchase   │    Storage lead   │ Licensing portal │   Key applied    │   │
│   │    On-demand     │    Key apply     │    Storage eng.   │  Array GUI/CLI   │  Feature active  │   │
│   │    Quarterly     │    Key audit     │    Storage lead   │  CMDB + portal   │   Audit report   │   │
│   │      Annual      │ FW compat check  │    Storage eng.   │Dell compat matrix│   Upgrade plan   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FoD application is online; no downtime; feature available across all array nodes         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Feature intake = Formal request from app or business team; documented in ITSM ticket               │
│    Need validation = Storage team confirms requested feature is not already active or available       │
│    FW prereq check = Verify array firmware meets minimum version required for the FoD key             │
│    Budget sign-off = Finance approval for FoD key cost before purchase; include in request            │
│    Test in non-prod = Apply identical FoD key on non-production array first; validate feature         │
│    Verify feature  = After apply, confirm feature appears active in array management UI               │
│    CMDB reconcile = Compare array license list to CMDB records; update discrepancies                  │
│    Key inventory  = Maintained list of all FoD keys: SN, feature, purchase date, applied date         │
│    Unused key review = Check for purchased but unapplied keys; ensure stored in vault securely        │
│    Portal reconcile = Compare licensing portal order history to key inventory; gaps indicate lost keys│
│    FW compat check = Annual review of FoD keys against latest firmware; ensure no incompatibility     │
│    CR             = Change Request; ITSM ticket documenting reason and approver for FoD apply         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌──────────────────────────────────────── Dell FoD — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FoD operations: feature request handling, key purchase, application, and quarterly audit   │   │
│   │    Request: app team requests new feature; storage team validates need and firmware prereq    │   │
│   │     Purchase: raise CR, get approval, buy key from portal, store in vault, apply to array     │   │
│   │       Audit: quarterly review of all active FoD features per array; CMDB reconciliation       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Feature request → prereq check → CR → purchase → apply → verify → CMDB → quarterly audit           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Request Ops         │  │           Key Ops           │  │          Audit Ops          │   │
│   │        Feature intake       │  │           Raise CR          │  │       Quarterly review      │   │
│   │       Need validation       │  │         Purchase key        │  │        CMDB reconcile       │   │
│   │       FW prereq check       │  │          Apply key          │  │        Key inventory        │   │
│   │       Budget sign-off       │  │        Verify feature       │  │      Unused key review      │   │
│   │       Test in non-prod      │  │         Update CMDB         │  │       Portal reconcile      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All FoD key applications require approved CR and documented business justification                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Frequency     │       Task       │       Owner       │       Tool       │      Output      │   │
│   │    On-demand     │   Key purchase   │    Storage lead   │ Licensing portal │   Key applied    │   │
│   │    On-demand     │    Key apply     │    Storage eng.   │  Array GUI/CLI   │  Feature active  │   │
│   │    Quarterly     │    Key audit     │    Storage lead   │  CMDB + portal   │   Audit report   │   │
│   │      Annual      │ FW compat check  │    Storage eng.   │Dell compat matrix│   Upgrade plan   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FoD application is online; no downtime; feature available across all array nodes         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Feature intake = Formal request from app or business team; documented in ITSM ticket               │
│    Need validation = Storage team confirms requested feature is not already active or available       │
│    FW prereq check = Verify array firmware meets minimum version required for the FoD key             │
│    Budget sign-off = Finance approval for FoD key cost before purchase; include in request            │
│    Test in non-prod = Apply identical FoD key on non-production array first; validate feature         │
│    Verify feature  = After apply, confirm feature appears active in array management UI               │
│    CMDB reconcile = Compare array license list to CMDB records; update discrepancies                  │
│    Key inventory  = Maintained list of all FoD keys: SN, feature, purchase date, applied date         │
│    Unused key review = Check for purchased but unapplied keys; ensure stored in vault securely        │
│    Portal reconcile = Compare licensing portal order history to key inventory; gaps indicate lost keys│
│    FW compat check = Annual review of FoD keys against latest firmware; ensure no incompatibility     │
│    CR             = Change Request; ITSM ticket documenting reason and approver for FoD apply         │
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
