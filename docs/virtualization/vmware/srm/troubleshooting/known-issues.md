---
tags:
  - troubleshooting
  - srm
  - vmware
  - known-issues
---
# VMware Site Recovery Manager — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known SRM bugs, error codes, and workarounds covering protection groups, recovery plans, and vSphere Replication integration.

*Applies to: SRM 8.x / 9.x*
</div>

```text
┌────────────────────────────────────── Virtualization Vmware Srm ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           Vmware: Virtualization Vmware Srm platform                          │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Virtualization Vmware Srm management console                   │   │
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
│    Physical: Virtualization Vmware Srm infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Srm platform overview and core concepts                 │
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


## Before you begin

- SRM error codes appear in `Recovery Plan History` → view steps; expand failed step for detail.
- Collect `vmware-dr.log` from the SRM appliance for support escalation.
- Most recovery plan failures trace to network mapping, datastore mapping, or placeholder VM issues — check these before assuming a bug.

## Recovery Plan Failures

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Error: Cannot power on VM — network not found` | SRM 8.x | Network mapping not configured for recovery network | Configure network mappings in SRM → Mappings → Network Mappings | N/A |
| Recovery plan stuck at `Waiting for storage systems to complete failover` | SRM 8.x | Array-based replication (ABR) storage provider unresponsive | Check storage provider health; retest storage provider in SRM UI | N/A |
| `Placeholder VM not found` during recovery | SRM 8.x | Placeholder VM deleted or orphaned on recovery site vCenter | Re-synchronize protection group; placeholders are auto-recreated | N/A |
| Reprotect fails: `Cannot replicate — disk already exists` | SRM 8.x | Residual VMDK from previous failover test not cleaned up | Delete residual disk from recovery datastore manually; retry reprotect | N/A |

## vSphere Replication Integration

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| vSphere Replication RPO alarm despite healthy sync | SRM 8.x | vSphere Replication lag metric includes quiesce time for large VMs | Tune RPO threshold; or disable quiescing for high-change VMs | N/A |
| `VR appliance pairing failed — certificate mismatch` | SRM 8.x | VRMS certificates not trusted between sites | Resubmit VRMS certificate to vCenter trust on both sites | N/A |

## Site Pairing

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Site pairing fails: `SSL certificate verification failed` | SRM 8.x | Remote SRM appliance certificate not trusted | Accept remote site certificate in SRM Site Pairing wizard | N/A |
| `Lost connection to remote site` after network change | SRM 8.x | SRM inter-site port 9086 blocked after firewall change | Verify TCP 9086 open between both SRM appliances | N/A |

## See also

- [VMware SRM — Common Issues](common-issues.md)
- [VMware vSphere Replication — Known Issues](../../vsphere-replication/troubleshooting/known-issues/)
- [VMware vCenter — Known Issues](../../vcenter/troubleshooting/known-issues/)
