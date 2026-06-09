# Horizon (VDI) — Operations

<div class="kb-summary">
Horizon day-2 operations — Connection Server health monitoring, active session management, desktop pool recompose and instant clone image push, App Volumes and DEM assignment, event database review, lifecycle upgrade sequencing (Connection Server first, then UAG, then agent via recompose), and PowerCLI Horizon module and REST API automation.
</div>

```text
┌──────────────────────────────────────── Horizon — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Connection Server health monitoring; active session count and session management daily    │   │
│   │   Desktop pool provisioning and recompose; image management and push to instant clone pools   │   │
│   │    App Volumes assignment per user or group; log review and event DB monitoring for errors    │   │
│   │    Lifecycle: upgrade Connection Server first, then UAG, then push agent via pool recompose   │   │
│   │  Automation: PowerCLI Horizon module, REST API, Provisioning API for at-scale pool management │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops track sessions and pool health · lifecycle upgrades CS first                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │       CS health check       │  │       Horizon upgrades      │  │       PowerCLI Horizon      │   │
│   │       Active sessions       │  │        CS upgrade 1st       │  │           REST API          │   │
│   │        Pool provision       │  │         UAG upgrade         │  │       Provisioning API      │   │
│   │       Composer status       │  │       Agent via recomp      │  │        Connection API       │   │
│   │          Image push         │  │       App Vol upgrade       │  │          LDAP query         │   │
│   │          Log review         │  │          Add new CS         │  │        Dashboard API        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch session and pool issues · lifecycle upgrades in order                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │     REST API     │   CS: running    │   Pool recompose  │  CS upgrade 1st  │   Event DB bkp   │   │
│   │   PowerCLI Hor   │   Sessions: ok   │     Image push    │   UAG upgrade    │  Config export   │   │
│   │    LDAP query    │   UAG: healthy   │   App Vol assign  │   Agent recomp   │   CS config bk   │   │
│   │  Event DB query  │   Pool: ready    │     User reset    │   Post-upg val   │  Restore config  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · vCenter · AD domain                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server  = Horizon broker; health monitored via vCenter plugin and Horizon Admin console   │
│  UAG                = Unified Access Gateway; DMZ proxy; upgrade after Connection Server upgrade      │
│  Desktop pool       = Group of Horizon desktops provisioned from a parent image or template           │
│  Recompose          = Horizon operation pushing a new parent image to all instant clone pool desktops │
│  Instant clone      = Pool type where desktops are forked from a live parent VM snapshot              │
│  App Volumes        = Application delivery layer; AppStacks assigned per user, group, or OU           │
│  Dynamic Environment Manager = User environment and settings roaming for Horizon virtual desktops     │
│  vGPU profile       = NVIDIA vGPU slice assigned to a VM; profile determines VRAM allocation          │
│  Event database     = Horizon SQL database logging all session, admin, and provisioning events        │
│  REST API           = Horizon REST API for pool, session, and entitlement management at scale         │
│  Horizon agent      = Software installed in guest OS; communicates with Connection Server             │
│  Image management   = Process of updating parent VM, taking snapshot, and recomposing pool            │
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
