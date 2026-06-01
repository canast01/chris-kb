# Emergency Checks


<div class="kb-summary">
Use these when there is a major incident.
</div>
```
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


| Area | Check |
|---|---|
| vCenter | Can you log in? Are services running? |
| Hosts | Are hosts connected or not responding? |
| VMs | Are critical VMs powered on? |
| Storage | Are datastores mounted and not full? |
| vSAN | Are objects healthy? Any resyncs? |
| Network | Are management and VM networks reachable? |
| Hardware | Any failed disks, NICs, PSU, memory? |
| Backups | Are recent backups available? |
## Known Issue Tracking

| Field | Description |
|---|---|
| Issue | Short name of the problem |
| Impact | What it affects |
| Workaround | Temporary fix |
| Permanent Fix | Final fix |
| Owner | Team or person responsible |
| Status | Open, monitoring, fixed |
| Date Found | When it was identified |

## Escalation Quick Reference

| Issue | Escalate To |
|---|---|
| vSAN object inaccessible | VMware support |
| vCenter SSO failure | VMware support |
| VxRail upgrade failure | Dell support |
| Host hardware failure | Dell / hardware support |
| Datastore latency high | Storage team |
| vMotion network failure | Network team |
| Backup snapshot failure | Backup team |
| Certificate outage | VMware / security team |
| NSX control plane failure | VMware / NSX support |

## Fast Troubleshooting Map

| Problem | First Place to Look |
|---|---|
| VM slow | CPU ready, memory, datastore latency |
| VM cannot power on | Datastore space, host resources, locks |
| Host disconnected | Management network, DNS, hostd, vpxa |
| vMotion fails | VMkernel, VLAN, MTU, EVC |
| Datastore full | Snapshots, ISO files, orphaned disks |
| Login fails | SSO, AD/LDAP, locked account, certificates |
| vSAN warning | Skyline Health, disk groups, resyncs |
| VxRail upgrade fails | Pre-check results, VxRail Manager, support bundle |
