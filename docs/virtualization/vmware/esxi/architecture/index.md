---
tags:
  - architecture
  - esxi
  - vmware
  - vsphere-8
---
# ESXi — Architecture

<div class="kb-summary">
ESXi is VMware's Type-1 hypervisor. It is deployed in standalone, standard cluster, vSAN cluster, or stretched cluster configurations depending on resilience, storage, and scale requirements.

*Applies to: vSphere 7.x · 8.x*
</div>

```text
┌────────────────────────────── Virtualization Vmware Esxi — Architecture ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Vmware architecture overview: Virtualization Vmware Esxi platform               │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │         Key components: Virtualization Vmware Esxi, Management, Monitoring, Automation        │   │
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
│    Physical: Virtualization Vmware Esxi infrastructure · management network · monitoring              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Esxi platform overview and core concepts                │
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


![ESXi Cluster Deployment Models](../../../../assets/esxi-architecture-overview.svg)

| Cluster Type | Min Hosts | Storage | HA / DRS |
|---|---|---|---|
| Standalone | 1 | Local / external | No |
| Standard Cluster | 3+ | Shared SAN or NAS | Yes |
| vSAN Cluster | 3+ | Pooled from hosts (HCI) | Yes |
| Stretched Cluster | 4+ (2 per site) | vSAN stretched | Yes (site-level) |

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>VMkernel, networking, storage paths, CPU/memory scheduling, HA/DRS, and boot architecture.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>vCenter, storage, network, backup, and monitoring integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Host naming, BIOS baseline, vmkernel layout, NTP, VIB policy, and cluster sizing.</span></a>
</div>

