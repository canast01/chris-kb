# NetApp Operations


<div class="kb-summary">
Use this section for practical notes, checks, commands, troubleshooting, design references, and change validation.
</div>
```
┌─────────────────────────────────── NetApp Operations — Operations ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        NetApp Ops operations: day-2 procedures for administration and maintenance tasks       │   │
│   │          Covers: provisioning, health checks, upgrades, backup/restore, and scripting         │   │
│   │           All operations require approved change tickets in production environments           │   │
│   │         Runbooks available for common tasks; escalation path defined for all incidents        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Open change → pre-check → execute procedure → verify → close                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Monitoring         │  │           ActiveIQ          │  │       Risk assessment       │   │
│   │          Telemetry          │  │         AutoSupport         │  │       Call-home relay       │   │
│   │         Health check        │  │        Config Advisor       │  │        Best practice        │   │
│   │           Support           │  │     mysupport.netapp.com    │  │        SR management        │   │
│   │           Upgrade           │  │         NDO rolling         │  │        Non-disruptive       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │       Access      │       Auth       │      Notes       │   │
│   │     ActiveIQ     │  Health portal   │       HTTPS       │    NetApp SSO    │       SaaS       │   │
│   │   AutoSupport    │    Call-home     │    HTTPS/email    │   Certificate    │  Daily reports   │   │
│   │  Config Advisor  │  Best practice   │     Local tool    │   Local admin    │  Point-in-time   │   │
│   │  ONTAP Upgrade   │   Version mgmt   │   System Manager  │    Admin role    │   Rolling NDO    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NetApp AFF/FAS clusters · ActiveIQ SaaS · mysupport.netapp.com support portal            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ActiveIQ           = NetApp SaaS health portal; risk assessment, upgrade advisor, capacity planning│
│    AutoSupport        = ONTAP telemetry; sends daily health reports and call-home bundles to NetApp   │
│    Config Advisor     = NetApp best-practice checker; validates cabling, config, and firmware         │
│    NDO                = Non-Disruptive Operations; rolling upgrades without host I/O service disrup...│
│    Takeover           = HA failover; one node takes over partner storage on node failure event        │
│    Giveback           = return storage to original node after failover; completes HA pair recovery    │
│    Aggregate relocation = move aggregate between HA pair nodes without service disruption             │
│    LIF migration      = move logical interface to different node port during planned maintenance      │
│    System Manager     = ONTAP web GUI; unified management for cluster, SVMs, volumes, policies        │
│    ONTAP CLI          = SSH to cluster management IP; diag privilege required for low-level commands  │
│    mysupport          = mysupport.netapp.com; open SRs, download firmware, and access knowledge base  │
│    ASUP bundle        = AutoSupport bundle with logs, config, and core files for TAC case analysis    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-3">

<a class="kb-card" href="alerts/">
  <strong>Alerts</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Alerts.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Health Checks.</span>
</a>

<a class="kb-card" href="support-cases/">
  <strong>Support Cases</strong>
  <span>Notes, checks, runbooks, commands, troubleshooting, and operational references for Support Cases.</span>
</a>

</div>
