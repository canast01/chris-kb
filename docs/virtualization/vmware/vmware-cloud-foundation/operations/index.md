# VCF — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware Cloud Foundation. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```
┌────────────────────────────────────────── VCF — Operations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   SDDC Manager dashboard for domain health; LCM upgrade orchestration across all components   │   │
│   │  SoS health check tool validates VCF component state; reports failures per domain and service │   │
│   │  Password rotation for all components via SDDC Manager; certificate status monitoring across  │   │
│   │  LCM upgrade sequence: Management domain first; VI domains staged after; pre-checks mandatory │   │
│   │            Automation: SDDC REST API, LCM API, PowerCLI VCF, Terraform VCF provider           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch drift · lifecycle orchestrates upgrades safely · automation scales VCF management  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │        SDDC dashboard       │  │       SDDC LCM upgrade      │  │        SDDC REST API        │   │
│   │      Domain health chk      │  │       Bundle download       │  │           LCM API           │   │
│   │          LCM status         │  │        Pre-check run        │  │         PowerCLI VCF        │   │
│   │      Password rotation      │  │       Upg: mgmt first       │  │        Terraform VCF        │   │
│   │         Cert status         │  │        Aria upgrades        │  │      Cloud Builder API      │   │
│   │         SoS tool run        │  │          BOM update         │  │       Tag-based policy      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops keep domains healthy · lifecycle upgrades safely in sequence                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  SDDC REST API   │ Domain: healthy  │   Add VI domain   │  LCM bundle dl   │  Config backup   │   │
│   │  SoS tool cmds   │   LCM: current   │      Add host     │  Pre-check run   │   SFTP target    │   │
│   │   PowerCLI VCF   │   Certs: valid   │    Add cluster    │   Mgmt upg 1st   │   SDDC restore   │   │
│   │     LCM API      │  Passwords: ok   │   Expand domain   │   Post-upg val   │  Domain backup   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers (mgmt + workload) · PCIe NICs · ToR switches · vSAN/SAN · OOB management                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager  = VCF control plane; dashboard shows domain health, alerts, and LCM upgrade status     │
│  LCM           = Lifecycle Manager; orchestrates upgrades for vSphere, vSAN, NSX, and SDDC Manager    │
│  SoS (Support and Service Guidance tool) = Health check CLI; validates all VCF component states       │
│  Workload domain = Isolated VCF unit; add hosts, clusters, or expand via SDDC Manager workflow        │
│  BOM           = Bill of Materials; defines validated component versions for each VCF release         │
│  Cloud Builder = Bring-up appliance used for initial Management domain deployment; retired post-deploy│
│  SDDC REST API = VCF programmatic interface; manage domains, hosts, clusters, and lifecycle tasks     │
│  Password rotation = SDDC Manager rotates credentials for vCenter, NSX, ESXi, and SDDC components     │
│  vCenter per domain = Dedicated vCenter in each domain; upgraded as part of LCM domain upgrade        │
│  NSX per domain = NSX Manager cluster per VCF domain; upgraded after vCenter in LCM sequence          │
│  Certificate rotation = SDDC Manager renews certificates for all VCF components on schedule           │
│  VCF upgrade sequence = Mgmt domain first; VI domains after; never upgrade VI before Management       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────────── VCF — Operations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   SDDC Manager dashboard for domain health; LCM upgrade orchestration across all components   │   │
│   │  SoS health check tool validates VCF component state; reports failures per domain and service │   │
│   │  Password rotation for all components via SDDC Manager; certificate status monitoring across  │   │
│   │  LCM upgrade sequence: Management domain first; VI domains staged after; pre-checks mandatory │   │
│   │            Automation: SDDC REST API, LCM API, PowerCLI VCF, Terraform VCF provider           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch drift · lifecycle orchestrates upgrades safely · automation scales VCF management  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │        SDDC dashboard       │  │       SDDC LCM upgrade      │  │        SDDC REST API        │   │
│   │      Domain health chk      │  │       Bundle download       │  │           LCM API           │   │
│   │          LCM status         │  │        Pre-check run        │  │         PowerCLI VCF        │   │
│   │      Password rotation      │  │       Upg: mgmt first       │  │        Terraform VCF        │   │
│   │         Cert status         │  │        Aria upgrades        │  │      Cloud Builder API      │   │
│   │         SoS tool run        │  │          BOM update         │  │       Tag-based policy      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops keep domains healthy · lifecycle upgrades safely in sequence                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  SDDC REST API   │ Domain: healthy  │   Add VI domain   │  LCM bundle dl   │  Config backup   │   │
│   │  SoS tool cmds   │   LCM: current   │      Add host     │  Pre-check run   │   SFTP target    │   │
│   │   PowerCLI VCF   │   Certs: valid   │    Add cluster    │   Mgmt upg 1st   │   SDDC restore   │   │
│   │     LCM API      │  Passwords: ok   │   Expand domain   │   Post-upg val   │  Domain backup   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers (mgmt + workload) · PCIe NICs · ToR switches · vSAN/SAN · OOB management                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager  = VCF control plane; dashboard shows domain health, alerts, and LCM upgrade status     │
│  LCM           = Lifecycle Manager; orchestrates upgrades for vSphere, vSAN, NSX, and SDDC Manager    │
│  SoS (Support and Service Guidance tool) = Health check CLI; validates all VCF component states       │
│  Workload domain = Isolated VCF unit; add hosts, clusters, or expand via SDDC Manager workflow        │
│  BOM           = Bill of Materials; defines validated component versions for each VCF release         │
│  Cloud Builder = Bring-up appliance used for initial Management domain deployment; retired post-deploy│
│  SDDC REST API = VCF programmatic interface; manage domains, hosts, clusters, and lifecycle tasks     │
│  Password rotation = SDDC Manager rotates credentials for vCenter, NSX, ESXi, and SDDC components     │
│  vCenter per domain = Dedicated vCenter in each domain; upgraded as part of LCM domain upgrade        │
│  NSX per domain = NSX Manager cluster per VCF domain; upgraded after vCenter in LCM sequence          │
│  Certificate rotation = SDDC Manager renews certificates for all VCF components on schedule           │
│  VCF upgrade sequence = Mgmt domain first; VI domains after; never upgrade VI before Management       │
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
