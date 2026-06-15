---
tags:
  - architecture
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Architecture

<div class="kb-summary">
vSAN pools local NVMe and SSD disks across ESXi hosts into a shared distributed datastore. Storage policies (RAID-1/5/6, FTT) define per-VM resilience. vSAN ESA eliminates the separate cache tier on supported hardware.

*Applies to: vSAN 7.x · 8.x*
</div>

```text
┌────────────────────────────── Virtualization Vmware Vsan — Architecture ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Vmware architecture overview: Virtualization Vmware Vsan platform               │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │         Key components: Virtualization Vmware Vsan, Management, Monitoring, Automation        │   │
│   │          Design principles: HA, scalability, non-disruptive operations, and security          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Design → deploy → configure → validate → monitor → optimise                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Vsan infrastructure · management network · monitoring              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Vsan platform overview and core concepts                │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


![vSAN Architecture Models](../../../../assets/vsan-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Disk groups, RAID tiers, dedup/compression, vSAN ESA, and stretched cluster mechanics.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>vCenter, vSphere HA/DRS, NSX, file services, Aria Ops, and HCL compatibility.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Cluster sizing, host requirements, storage policy baseline, naming conventions, and capacity rules.</span>
</a>

<a class="kb-card" href="component-states/">
  <strong>Component States</strong>
  <span>ABSENT, DEGRADED, STALE, REBUILDING — what each state means and how to respond.</span>
</a>

<a class="kb-card" href="resync-mechanics/">
  <strong>Resync Mechanics</strong>
  <span>Why resyncs trigger, how CLOM places rebuilds, throttle settings, and the 30% headroom rule.</span>
</a>

</div>

