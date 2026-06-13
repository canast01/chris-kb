---
tags:
  - reference
---
# Virtualization Inventory


<div class="kb-summary">
Inventory references for clusters, hosts, datastores, networks, management tools, and versions.

*Applies to: vSphere 7.x / 8.x*
</div>
```text
┌───────────────────────────────── Virtualization Reference Inventory ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     Reference: Virtualization Reference Inventory platform                    │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │               Management: Virtualization Reference Inventory management console               │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│    Physical: Virtualization Reference Inventory infrastructure · management network · monitoring      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Reference          = Virtualization Reference Inventory platform overview and core concepts        │
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


<div class="kb-grid kb-grid-5">

<a class="kb-card" href="cluster-inventory/">
  <strong>Cluster Inventory</strong>
  <span>Cluster list, purpose, owner, version, capacity, and notes.</span>
</a>

<a class="kb-card" href="host-inventory/">
  <strong>Host Inventory</strong>
  <span>ESXi host list, hardware, version, cluster, warranty, and notes.</span>
</a>

<a class="kb-card" href="datastore-inventory/">
  <strong>Datastore Inventory</strong>
  <span>Datastore list, type, backing storage, capacity, owner, and usage.</span>
</a>

<a class="kb-card" href="network-inventory/">
  <strong>Network Inventory</strong>
  <span>Port groups, VLANs, segments, distributed switches, and uplinks.</span>
</a>

<a class="kb-card" href="management-tools/">
  <strong>Management Tools</strong>
  <span>vCenter, VxRail Manager, NSX, Aria, collectors, and URLs.</span>
</a>

<a class="kb-card" href="version-inventory/">
  <strong>Version Inventory</strong>
  <span>Current and target versions across VMware, VxRail, NSX, and Aria.</span>
</a>

<a class="kb-card" href="backup-coverage/">
  <strong>Backup Coverage</strong>
  <span>VM backup job coverage, schedules, retention policy, and gap identification.</span>
</a>

<a class="kb-card" href="certificate-inventory/">
  <strong>Certificate Inventory</strong>
  <span>Certificate thumbprints, expiry dates, issuer, and renewal tracking per component.</span>
</a>

<a class="kb-card" href="service-accounts/">
  <strong>Service Accounts</strong>
  <span>Service account list, permissions, owning team, and password rotation schedule.</span>
</a>
</div>
