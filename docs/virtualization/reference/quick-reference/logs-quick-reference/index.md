---
tags:
  - reference
---
# VMware Logs Quick Reference


<div class="kb-summary">
VMware Logs Quick Reference reference covering ESXi Log Locations, vCenter Appliance Log Locations, Collecting a vCenter Support Bundle, Collecting an ESXi Support Bundle, Using Aria Operations for Logs.
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


## ESXi Log Locations

```bash
/var/log/hostd.log       # Host daemon — VM and host operations
/var/log/vpxa.log        # vCenter agent on the host
/var/log/vmkernel.log    # Kernel-level events — storage, network, hardware
/var/log/vobd.log        # Hardware and storage event observer
/var/log/syslog.log      # General system log
/var/log/auth.log        # Authentication events
```

## vCenter Appliance Log Locations

```bash
/var/log/vmware/vpxd/          # vCenter Server daemon logs
/var/log/vmware/sso/           # SSO and identity service logs
/var/log/vmware/vapi/          # vAPI endpoint logs
/var/log/vmware/applmgmt/      # Appliance management logs
```

## Collecting a vCenter Support Bundle

In vSphere Client: **Menu** → **Administration** → **Support** → **Export Support Bundle**

Or from VAMI at `https://<vcenter>:5480` → **Support**

## Collecting an ESXi Support Bundle

Via vSphere Client: Right-click host → **Export System Logs**

Or via SSH:
```bash
vm-support -n <bundle-name>
```

## Using Aria Operations for Logs

- Search by hostname, IP, or keyword
- Set a time range before searching
- Filter by log source (hostd, vpxa, vmkernel)
- Export results as CSV for evidence or support cases
