# MDS — Operations


<div class="kb-summary">
MDS — Operations reference.
</div>

```text
┌───────────────────────────────────── Cisco MDS 9000 — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          MDS 9000 day-2 operations: VSAN management, zoning, ISL, port channels, ISSU         │   │
│   │        VSAN: create VSAN, assign ports, verify VSAN membership; VSAN 1 default — avoid        │   │
│   │                 Zoning: device aliases → zones → zone sets → activate per VSAN                │   │
│   │         ISSU: In-Service Software Upgrade; minimises disruption on dual-supervisor MDS        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VSAN create → port assign → zone build → zone activate → health verify                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        VSAN / ISL Ops       │  │          Zoning Ops         │  │        Health Checks        │   │
│   │         Create VSAN         │  │         Create alias        │  │        show interface       │   │
│   │       Assign VSAN port      │  │         Create zone         │  │          show vsan          │   │
│   │       Trunk ISL ports       │  │       Add to zone set       │  │         show zoneset        │   │
│   │       Port channel ISL      │  │        Activate zone        │  │        show flogi db        │   │
│   │        ISSU firmware        │  │        Verify members       │  │        show port-ch.        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Always backup config before zone changes: copy running-config startup-config                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │  NX-OS command   │     Key output    │      Verify      │      Notes       │   │
│   │   Create VSAN    │  vsan database   │       vsan N      │   show vsan N    │     Name it      │   │
│   │   Zone create    │  zone name Z vN  │    member pwwn    │    show zone     │   Alias better   │   │
│   │     Activate     │ zoneset activate │      Changes#     │ show zoneset act │  No disruption   │   │
│   │       ISSU       │   install all    │    Superv check   │   show version   │  Dual-sup req.   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: MDS 9000 line cards · FC SFP transceivers (SW/LW/CWDM) · ISL fibre paths                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VSAN          = Virtual SAN; logical fabric partition on MDS; isolates devices and zones           │
│    Device alias  = Named alias for a port WWN; recommended over raw WWN in zone membership            │
│    Zone set      = Container for zones in a VSAN; activate to enforce; only one active                │
│    Activate      = Deploy zone set to all switches in VSAN; non-disruptive if correctly done          │
│    FLOGI         = Fabric Login; device procedure to join FC fabric and receive FC address            │
│    FCNS          = FC Name Server; VSAN-scoped directory of all logged-in devices                     │
│    ISSU          = In-Service Software Upgrade; upgrades NX-OS without disrupting traffic             │
│    Trunk ISL     = ISL configured to carry multiple VSANs; uses E_port/TE_port mode                   │
│    Port channel  = Bundle of ISL ports for higher bandwidth and link redundancy                       │
│    show flogi db = Displays all devices that have logged into the fabric on this switch               │
│    show zoneset  = Shows active zone set for a VSAN; use active keyword for enforced config           │
│    copy run start = Saves running configuration to startup; always run after changes                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Step-by-step operational procedures and runbooks.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Proactive MDS health monitoring and validation routines.</span>
</a>

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known problems, symptoms, and resolution steps.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>MDS NX-OS installation, upgrade procedures, and version management.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Configuration backup, restore operations, and recovery validation.</span>
</a>

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>MDS NX-OS command reference for day-to-day operations.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for common operational tasks.</span>
</a>

</div>
