# vCenter — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware vCenter Server. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```
┌──────────────────────────────────────── vCenter — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     VCSA service health monitoring via VAMI; check all services green on start of each day    │   │
│   │     Certificate lifecycle management: monitor expiry in VAMI; renew via VMCA or custom CA     │   │
│   │   File-based backup to SFTP or NFS: schedule daily; retention of 3-7 restore points minimum   │   │
│   │    Update Planner checks compatibility and schedules upgrade; snapshot VCSA before upgrade    │   │
│   │     Automation: PowerCLI for vCenter management, REST API explorer, tag and attribute API     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor VCSA health · lifecycle keeps vCenter current                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │       VCSA services ok      │  │       Update appliance      │  │      REST API explorer      │   │
│   │       Cert expiry chk       │  │       Pre-check health      │  │       PowerCLI vCenter      │   │
│   │         Alarm review        │  │       Snapshot pre-upg      │  │         Tag/attr API        │   │
│   │        Storage tasks        │  │         Cert renewal        │  │      Automation scripts     │   │
│   │       HA cluster state      │  │       LCM integration       │  │         vCenter CLI         │   │
│   │        DB size check        │  │         PSC sync chk        │  │        API token auth       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch service drift · lifecycle upgrades vCenter safely                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │     REST API     │  Services green  │    Cert renewal   │  Update Planner  │  File-based bkp  │   │
│   │  PowerCLI conn   │   HA state ok    │    RBAC review    │  Pre-check run   │ SFTP/NFS target  │   │
│   │  Tag API calls   │ Backup: success  │      Add host     │   Snapshot pre   │  Restore: VCSA   │   │
│   │    Event API     │    Cert: 60d+    │    Add cluster    │   Post-upg chk   │  Config backup   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server (VCSA VM) · RAM DIMMs · Network NICs · Shared datastore (vSAN or SAN) · OOB management    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCSA          = vCenter Server Appliance; Linux-based VM; all vSphere management runs here           │
│  VAMI          = vCenter Appliance Management Interface; port 5480; monitors services and backup      │
│  File-based backup = Scheduled VCSA backup to SFTP or NFS; restores full appliance config and         │
│  Update Planner = vCenter tool checking compatibility matrix before scheduling an upgrade             │
│  PowerCLI      = VMware PowerShell module; connects to vCenter REST API for at-scale automation       │
│  REST API      = vCenter REST API (api/); supports hosts, VMs, tags, policies, and content library    │
│  Certificate lifecycle = VCSA certificate expiry monitored in VAMI; renew via VMCA or custom CA       │
│  VMCA          = VMware Certificate Authority; built-in CA for VCSA and ESXi host certificates        │
│  LCM           = Lifecycle Manager; integrated in vCenter for ESXi image-based upgrade management     │
│  vCenter HA    = Active/passive/witness VCSA cluster; failover automatic on host or network failure   │
│  SSO           = Single Sign-On; vSphere identity service; local and AD/LDAP sources                  │
│  PSC           = Platform Services Controller; embedded 7.0+; handles SSO tokens and certificates     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── vCenter — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     VCSA service health monitoring via VAMI; check all services green on start of each day    │   │
│   │     Certificate lifecycle management: monitor expiry in VAMI; renew via VMCA or custom CA     │   │
│   │   File-based backup to SFTP or NFS: schedule daily; retention of 3-7 restore points minimum   │   │
│   │    Update Planner checks compatibility and schedules upgrade; snapshot VCSA before upgrade    │   │
│   │     Automation: PowerCLI for vCenter management, REST API explorer, tag and attribute API     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops monitor VCSA health · lifecycle keeps vCenter current                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │       VCSA services ok      │  │       Update appliance      │  │      REST API explorer      │   │
│   │       Cert expiry chk       │  │       Pre-check health      │  │       PowerCLI vCenter      │   │
│   │         Alarm review        │  │       Snapshot pre-upg      │  │         Tag/attr API        │   │
│   │        Storage tasks        │  │         Cert renewal        │  │      Automation scripts     │   │
│   │       HA cluster state      │  │       LCM integration       │  │         vCenter CLI         │   │
│   │        DB size check        │  │         PSC sync chk        │  │        API token auth       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch service drift · lifecycle upgrades vCenter safely                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │     REST API     │  Services green  │    Cert renewal   │  Update Planner  │  File-based bkp  │   │
│   │  PowerCLI conn   │   HA state ok    │    RBAC review    │  Pre-check run   │ SFTP/NFS target  │   │
│   │  Tag API calls   │ Backup: success  │      Add host     │   Snapshot pre   │  Restore: VCSA   │   │
│   │    Event API     │    Cert: 60d+    │    Add cluster    │   Post-upg chk   │  Config backup   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server (VCSA VM) · RAM DIMMs · Network NICs · Shared datastore (vSAN or SAN) · OOB management    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCSA          = vCenter Server Appliance; Linux-based VM; all vSphere management runs here           │
│  VAMI          = vCenter Appliance Management Interface; port 5480; monitors services and backup      │
│  File-based backup = Scheduled VCSA backup to SFTP or NFS; restores full appliance config and         │
│  Update Planner = vCenter tool checking compatibility matrix before scheduling an upgrade             │
│  PowerCLI      = VMware PowerShell module; connects to vCenter REST API for at-scale automation       │
│  REST API      = vCenter REST API (api/); supports hosts, VMs, tags, policies, and content library    │
│  Certificate lifecycle = VCSA certificate expiry monitored in VAMI; renew via VMCA or custom CA       │
│  VMCA          = VMware Certificate Authority; built-in CA for VCSA and ESXi host certificates        │
│  LCM           = Lifecycle Manager; integrated in vCenter for ESXi image-based upgrade management     │
│  vCenter HA    = Active/passive/witness VCSA cluster; failover automatic on host or network failure   │
│  SSO           = Single Sign-On; vSphere identity service; local and AD/LDAP sources                  │
│  PSC           = Platform Services Controller; embedded 7.0+; handles SSO tokens and certificates     │
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
