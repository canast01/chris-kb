---
tags:
  - reference
---
# Command Cheat Sheet


<div class="kb-summary">
Command Cheat Sheet reference covering ESXi Host Commands, vSAN Commands, Network Checks, Log Locations.
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


## ESXi Host Commands

```bash
# Check ESXi version
vmware -v

# Check uptime
uptime

# Check services
services.sh status

# Restart management agents
/etc/init.d/hostd restart
/etc/init.d/vpxa restart

# Restart all management services
services.sh restart

# List network adapters
esxcli network nic list

# List VMkernel interfaces
esxcli network ip interface list

# List storage adapters
esxcli storage core adapter list

# List paths
esxcli storage core path list

# List mounted filesystems
esxcli storage filesystem list
```

## vSAN Commands

```bash
# Check vSAN cluster info
esxcli vsan cluster get

# Check vSAN network
esxcli vsan network list

# Check vSAN disks
esxcli vsan storage list

# Check resync summary
esxcli vsan debug resync summary get
```

## Network Checks

```bash
# Ping from ESXi
vmkping <target-ip>

# Ping using a specific VMkernel adapter
vmkping -I vmk1 <target-ip>

# Test jumbo frames
vmkping -I vmk1 -s 8972 -d <target-ip>

# List physical NICs
esxcli network nic list

# List standard switches
esxcli network vswitch standard list
```

## Log Locations

```bash
/var/log/hostd.log
/var/log/vpxa.log
/var/log/vmkernel.log
/var/log/vobd.log
/var/log/syslog.log
/var/log/auth.log
```
