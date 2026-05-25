# Nexus Dashboard — Operations


```text
┌───────────────────────────────── Cisco Nexus Dashboard — Operations ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       ND operations: app lifecycle management, cluster health, site onboarding, backups       │   │
│   │     App lifecycle: install from AppStore or upload image; upgrade, enable, disable, delete    │   │
│   │       Cluster health: monitor node status, pod health, resource utilisation in Admin UI       │   │
│   │          Site onboarding: add ACI APIC or NX-OS switch credentials to ND for app use          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    App install → site add → policy configure → health monitor → backup → upgrade                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           App Ops           │  │         Cluster Ops         │  │           Site Ops          │   │
│   │         Install app         │  │         Node health         │  │         Add ACI site        │   │
│   │         Upgrade app         │  │          Pod status         │  │        Add NX-OS site       │   │
│   │        Enable/disable       │  │        Resource usage       │  │          Site creds         │   │
│   │          Delete app         │  │          Event log          │  │        Fabric verify        │   │
│   │        Backup cluster       │  │          Cert renew         │  │         Site health         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Backup: Admin > System Settings > System Backup; schedule daily; copy off-cluster                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │    ND UI path    │     Key field     │      Verify      │      Notes       │   │
│   │   Install app    │  Services>Apps   │    AppStore/img   │   App running    │   Compat check   │   │
│   │     Add site     │   Admin>Sites    │    APIC/SNMP IP   │   Site healthy   │   Creds stored   │   │
│   │   Node health    │   Admin>Nodes    │       Status      │   All healthy    │   Pod details    │   │
│   │      Backup      │   Admin>Backup   │      Schedule     │    File saved    │   Off-cluster    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ND VM datastores · OOB switch mgmt ports · fabric switches in Data VLAN                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    AppStore       = ND built-in catalogue; downloads and installs app images from Cisco CDN           │
│    App lifecycle  = Install → enable → configure → upgrade → disable → delete workflow                │
│    Node health    = ND Admin UI node view; shows CPU/RAM/disk per node and pod counts                 │
│    Pod status     = Kubernetes pod state for each app service; Running = healthy                      │
│    Site           = ND term for a managed fabric (ACI cluster or NX-OS fabric)                        │
│    ACI site       = APIC cluster onboarded to ND; NDI and NDO use it for assurance                    │
│    NX-OS site     = NDFC-managed Nexus/MDS fabric registered as ND site                               │
│    Backup         = ND config snapshot including cluster config and app state                         │
│    Cert renew     = ND TLS certs expire; renew before expiry via Admin > Security                     │
│    Event log      = ND system event log; shows node join/leave, app state changes                     │
│    Resource usage = ND node CPU/RAM/disk utilisation; add workers if consistently >70%                │
│    Compat check   = Verify app version is listed as compatible with installed ND version              │
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

```text
┌───────────────────────────────── Cisco Nexus Dashboard — Operations ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       ND operations: app lifecycle management, cluster health, site onboarding, backups       │   │
│   │     App lifecycle: install from AppStore or upload image; upgrade, enable, disable, delete    │   │
│   │       Cluster health: monitor node status, pod health, resource utilisation in Admin UI       │   │
│   │          Site onboarding: add ACI APIC or NX-OS switch credentials to ND for app use          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    App install → site add → policy configure → health monitor → backup → upgrade                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           App Ops           │  │         Cluster Ops         │  │           Site Ops          │   │
│   │         Install app         │  │         Node health         │  │         Add ACI site        │   │
│   │         Upgrade app         │  │          Pod status         │  │        Add NX-OS site       │   │
│   │        Enable/disable       │  │        Resource usage       │  │          Site creds         │   │
│   │          Delete app         │  │          Event log          │  │        Fabric verify        │   │
│   │        Backup cluster       │  │          Cert renew         │  │         Site health         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Backup: Admin > System Settings > System Backup; schedule daily; copy off-cluster                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │    ND UI path    │     Key field     │      Verify      │      Notes       │   │
│   │   Install app    │  Services>Apps   │    AppStore/img   │   App running    │   Compat check   │   │
│   │     Add site     │   Admin>Sites    │    APIC/SNMP IP   │   Site healthy   │   Creds stored   │   │
│   │   Node health    │   Admin>Nodes    │       Status      │   All healthy    │   Pod details    │   │
│   │      Backup      │   Admin>Backup   │      Schedule     │    File saved    │   Off-cluster    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ND VM datastores · OOB switch mgmt ports · fabric switches in Data VLAN                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    AppStore       = ND built-in catalogue; downloads and installs app images from Cisco CDN           │
│    App lifecycle  = Install → enable → configure → upgrade → disable → delete workflow                │
│    Node health    = ND Admin UI node view; shows CPU/RAM/disk per node and pod counts                 │
│    Pod status     = Kubernetes pod state for each app service; Running = healthy                      │
│    Site           = ND term for a managed fabric (ACI cluster or NX-OS fabric)                        │
│    ACI site       = APIC cluster onboarded to ND; NDI and NDO use it for assurance                    │
│    NX-OS site     = NDFC-managed Nexus/MDS fabric registered as ND site                               │
│    Backup         = ND config snapshot including cluster config and app state                         │
│    Cert renew     = ND TLS certs expire; renew before expiry via Admin > Security                     │
│    Event log      = ND system event log; shows node join/leave, app state changes                     │
│    Resource usage = ND node CPU/RAM/disk utilisation; add workers if consistently >70%                │
│    Compat check   = Verify app version is listed as compatible with installed ND version              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
