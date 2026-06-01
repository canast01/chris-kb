# VMware Snapshot Quick Reference


<div class="kb-summary">
VMware Snapshot Quick Reference reference covering Find All Snapshots, Check Snapshot Age and Size, Identify Snapshot Owner, Remove a Snapshot Safely, Consolidation Warning and 2 more sections.
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


## Find All Snapshots

In vCenter: **Menu** → **Global Views** → **VMs and Templates** → Filter by snapshot state

Or use Aria Operations: **Environment** → **VMs** → filter by snapshot count > 0

## Check Snapshot Age and Size

In vSphere Client: Right-click VM → **Snapshots** → **Manage Snapshots**

- Review snapshot creation date
- Review snapshot size on disk

## Identify Snapshot Owner

- Check if the snapshot was created by a backup product (name will include backup job name)
- Check if it was a manual change-related snapshot

## Remove a Snapshot Safely

1. Confirm the VM is healthy and the snapshot is no longer needed
2. Right-click VM → **Snapshots** → **Manage Snapshots**
3. Select the snapshot → **Delete**
4. Monitor the consolidation task — it may take several minutes

## Consolidation Warning

If vCenter shows a consolidation needed warning:
- Right-click VM → **Snapshots** → **Consolidate**
- Monitor the task and confirm completion

## Check Datastore Free Space After Cleanup

- Confirm datastore free space has recovered after snapshot removal

## Escalate Locked or Stuck Snapshots

- Do not force-delete stuck snapshots without VMware support guidance
- Collect the snapshot delta file list and vCenter events before escalating
