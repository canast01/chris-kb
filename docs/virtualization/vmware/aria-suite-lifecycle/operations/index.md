# Aria Suite Lifecycle — Operations
```text
┌──────────────────────────────────────── Aria LCM — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Environment health dashboard for all Aria products; upgrade wizard for orchestrated upgrades │   │
│   │  Certificate rotation via Certificate Locker; password rotation via Password Locker workflows │   │
│   │      Content management for environments; request monitoring for all LCM background jobs      │   │
│   │   Upgrade wizard validates BOM compatibility and runs pre-checks before any product upgrade   │   │
│   │    LCM REST API for day-2 automation; vIDM integration API for identity and SSO management    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor all Aria products · lifecycle wizard orchestrates upgrades                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │       Env health dash       │  │        Upgrade wizard       │  │         LCM REST API        │   │
│   │       Product versions      │  │       Pre-chk validate      │  │        Day-2 actions        │   │
│   │         Cert expiry         │  │        BOM compat chk       │  │           Cert API          │   │
│   │        Request status       │  │      Product upg order      │  │        Pwd Locker API       │   │
│   │       Locker inventory      │  │         Post-upg val        │  │         Content mgmt        │   │
│   │       Download catalog      │  │        Cert rotation        │  │        vIDM intg API        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch cert expiry and version drift · upgrade wizard enforces order                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │   LCM REST API   │   Env: healthy   │   Cert rotation   │  Upgrade wizard  │  Config export   │   │
│   │    Day-2 API     │   Products: ok   │    Pwd rotation   │   Pre-chk run    │  Locker backup   │   │
│   │     Cert API     │   Certs: valid   │    Add product    │    BOM compat    │   Restore LCM    │   │
│   │  Pwd Locker API  │   Downloads ok   │    Env snapshot   │   Post-upg val   │   DR failover    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter (deploy target) · Internet (My VMware)   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Upgrade wizard    = LCM UI workflow that orchestrates Aria product upgrades in correct dependency    │
│  Pre-check validation = Automated checks run before upgrade; verifies disk space, connectivity, and   │
│  Certificate Locker = LCM component for managing TLS certificates; used for cert rotation workflows   │
│  Password Locker   = LCM encrypted credential store; used for password rotation day-2 operations      │
│  BOM compatibility = Verification that all Aria products in an Environment are on a supported version │
│  Day-2 operations  = Post-install LCM tasks: cert rotation, password rotation, environment snapshots  │
│  Environment health = Dashboard view showing status of all Aria products in each LCM Environment      │
│  Product version   = Currently installed Aria product version tracked by LCM in each Environment      │
│  Request monitoring = LCM job tracker for all background operations; shows progress and error details │
│  DR replication    = LCM configuration backup replicated to DR site for failover capability           │
│  Content management = LCM workflow for managing Aria Automation content packs and blueprints          │
│  LCM REST API      = REST API for automating LCM day-2 operations: cert rotation, upgrades, locker    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Commands, syntax, and quick reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Routine checks, service validation, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Day-to-day operational tasks and how-to guides.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation, upgrade, patching, and decommission.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup configuration, restore procedures, and validation.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and reusable code.</span>
</a>

</div>
