# Upgrade Sequence Reference


<div class="kb-summary">
Upgrade Sequence Reference reference covering Correct Upgrade Order, Why Order Matters, VCF (VMware Cloud Foundation) Sequence, Compatibility Matrix References, Key Version Constraints and 1 more sections.
</div>
```
┌──────────────────────────────────── Virtualization Vmware Topics ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Vmware: Virtualization Vmware Topics platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                  Management: Virtualization Vmware Topics management console                  │   │
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
│    Physical: Virtualization Vmware Topics infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Topics platform overview and core concepts              │
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


## Correct Upgrade Order

Upgrading VMware components in the wrong order causes compatibility failures, plugin breakage, and in worst cases requires rollback. Always follow this sequence:

```text
1. Aria Suite Lifecycle (LCM)        ← Always first if LCM is used
2. Workspace ONE Access (VIDM)       ← Must precede Aria product upgrades
3. vCenter Server                    ← Must precede ESXi upgrades
4. NSX Manager                       ← Before ESXi if NSX version requires new kernel modules
5. ESXi hosts                        ← One at a time, rolling through maintenance mode
6. vSAN (on-disk format)             ← After all ESXi hosts at target version
7. VM hardware / VMware Tools        ← After ESXi upgrades (non-disruptive, schedule separately)
8. Aria Operations                   ← After vCenter is at target version
9. Aria Automation                   ← After Aria Operations
10. Aria Log Insight                 ← After VIDM
11. VxRail Manager + LCM             ← Managed via VxRail LCM (separate from Aria LCM)
12. SRM + vSphere Replication        ← After vCenter
```

## Why Order Matters

| Wrong Order | Consequence |
|---|---|
| ESXi upgraded before vCenter | vCenter plugin API mismatch; host management may fail |
| NSX upgraded after ESXi | Kernel module incompatibility if NSX requires specific ESXi build |
| Aria Operations before vCenter | vCenter adapter may fail to connect post-vCenter upgrade |
| LCM not upgraded first | Product upgrade wizard blocked — LCM refuses to upgrade products without being current |
| vSAN format before all hosts upgraded | Mixed-version nodes during format upgrade may cause object inaccessibility |

## VCF (VMware Cloud Foundation) Sequence

In a VCF environment, SDDC Manager controls the upgrade sequence — do not manually upgrade components:

```text
1. SDDC Manager        ← Upgrade via SDDC Manager UI
2. VCF bundles downloaded
3. vCenter (orchestrated by SDDC Manager)
4. NSX (orchestrated by SDDC Manager)
5. ESXi (orchestrated by SDDC Manager — host-by-host)
6. vSAN (on-disk format, if applicable)
```

Follow the VCF LCM upgrade wizard — it enforces the correct order and blocks incorrect sequences.

## Compatibility Matrix References

| Scenario | Matrix to Check |
|---|---|
| vCenter + ESXi version pairing | [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com) |
| NSX + vCenter compatibility | [NSX-T Release Notes](https://docs.vmware.com/en/VMware-NSX) |
| ESXi + hardware (HBA, NIC) | [Broadcom Compatibility Guide](https://compatibilityguide.broadcom.com/) |
| Aria product compatibility | [Aria Interoperability Matrix](https://interopmatrix.vmware.com) |
| VxRail version support | [VxRail Support Docs](https://www.dell.com/support/home/en-us/product-support/product/vxrail-d-series/docs) |

## Key Version Constraints

- ESXi must be within N-2 of vCenter major version (e.g., vCenter 8.0 supports ESXi 7.0 and 8.0)
- NSX-T: each NSX release certifies specific vCenter and ESXi versions — check release notes
- SRM must match vCenter version exactly (same major.minor)
- VxRail LCM bundles are tested against specific VCF/vSphere versions — only upgrade via VxRail LCM

## Maintenance Window Planning

| Component | Estimated Downtime | Notes |
|---|---|---|
| vCenter | None (management plane only) | vCenter HA: < 5 minutes |
| NSX Manager | None (data plane survives) | Management plane unavailable during upgrade |
| ESXi host (each) | None (VMs migrated by DRS) | Allow 20–40 min per host for EVA migration + upgrade |
| vSAN on-disk format | None | Background operation; monitor with `esxcli vsan upgrade status` |
| Aria Operations | None (monitoring gap) | ~30 min collection gap per node |
