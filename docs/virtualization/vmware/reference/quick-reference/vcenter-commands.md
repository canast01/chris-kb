---
tags:
  - reference
  - vcenter
  - vsphere-8
---
# vCenter Service Commands


<div class="kb-summary">
vCenter SSH command reference: `service-control --status/--start/--stop`, `vmon-cli`, appliance health checks, DB vacuum, and certificate status — run from the VCSA shell.

*Applies to: vSphere 7.x / 8.x*
</div>
```text
┌────────────────────────────── Virtualization Reference Quick Reference ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Reference: Virtualization Reference Quick Reference platform                 │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │            Management: Virtualization Reference Quick Reference management console            │   │
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
│    Physical: Virtualization Reference Quick Reference infrastructure · management network · monitoring│
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Reference          = Virtualization Reference Quick Reference platform overview and core concepts  │
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


## Check All Services

```bash
service-control --status
```

## Start All Services

```bash
service-control --start --all
```

## Stop All Services

```bash
service-control --stop --all
```

## Restart All Services

```bash
service-control --stop --all && service-control --start --all
```

## Restart a Single Service

```bash
service-control --restart vmware-vpxd
service-control --restart vmware-sts
service-control --restart vmware-lookupsvc
```

## Check Disk Space

```bash
df -h
```

## Check Uptime

```bash
uptime
```

## Check Certificate Status

Access VAMI at `https://<vcenter>:5480` → **Certificate Management**

## When Not to Restart Services

- If disk partitions are full — free space first
- If a restore is needed — restarting services will not fix a corrupt database
- During active vMotion or vSAN resync operations without change approval

## Escalation

If services do not recover after a restart, collect a support bundle from VAMI and open a VMware support case.
