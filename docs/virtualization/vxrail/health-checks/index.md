# VxRail Health Checks

<div class="kb-summary">
VxRail Health Checks reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>
```text
┌───────────────────────── Virtualization Vxrail Health Checks — Health Checks ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Vxrail health checks: routine verification of operational status and performance       │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
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
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vxrail Health Checks infrastructure · management network · monitoring     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vxrail             = Virtualization Vxrail Health Checks platform overview and core concepts       │
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

## Run This Routine

Run these steps in order for every daily check, pre-change validation, or post-incident review of the VxRail cluster.

1. **VxRail Manager cluster status** — Log in to VxRail Manager UI → Dashboard. Confirm cluster health indicator is green. Any non-green status requires investigation before proceeding with changes.
2. **vSAN health** — In vCenter, select the VxRail cluster → Monitor → vSAN → Health. All health checks must show green. Investigate and resolve any failing checks; common culprits are clock skew, capacity imbalance, and network connectivity failures.
3. **Node inventory status** — In VxRail Manager → Inventory → Nodes, confirm all nodes show status `Healthy`. A node in `Degraded` or `Unknown` state needs immediate triage — check iDRAC events and ESXi host logs.
4. **LCM compliance** — In VxRail Manager → Lifecycle Management, verify all nodes are listed as `Compliant` against the current baseline. Non-compliant nodes must be remediated before the next change window.
5. **iDRAC connectivity** — From the management host, ping each node's iDRAC IP (`ping <idrac-ip>`). All pings must succeed. An unreachable iDRAC means out-of-band management is unavailable for that node.
6. **NTP time synchronisation** — SSH to each ESXi host and run `esxcli system time get`. Compare timestamps across all hosts — skew must be less than 5 seconds. Time drift causes vSAN and vCenter authentication failures.
7. **vCenter connectivity** — In VxRail Manager → Settings → vCenter Server, confirm the connection status shows `Connected`. A disconnected vCenter stops all VxRail management operations.
8. **Open alerts review** — In VxRail Manager → Alerts, review all open alerts. Resolve or acknowledge any `Critical` or `Warning` alerts, assigning owner and due date for each unresolved item before closing the check.

## Overview

VxRail Health Checks notes for infrastructure operations, support, health checks, and troubleshooting.

## Where It Fits

Use this page for daily, pre-change, and post-change VxRail cluster validation.

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review active alerts. |  |  |
| Confirm management access. |  |  |
| Check capacity, health, and recent task failures. |  |  |
| Review backup, replication, or protection status where applicable. |  |  |
| Confirm recent changes did not create new warnings. |  |  |

## Health Commands

```bash
# Add environment-specific commands here
```

## Common Issues

- Certificate or authentication problems.
- Capacity pressure.
- Failed or stuck tasks.
- Version mismatch after upgrades.
- Alert noise without clear ownership.
- Configuration drift from standards.

## Operational Tasks

| Task | Command |
|---|---|
| Check service health. |  |
| Review inventory and ownership. |  |
| Validate monitoring coverage. |  |
| Confirm backup or recovery posture. |  |
| Document changes after maintenance work. |  |

## Upgrade Notes

- Confirm compatibility before upgrade.
- Review release notes and known issues.
- Validate backups and rollback options.
- Confirm maintenance window.
- Run post-upgrade health checks.

## Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Document ownership and support boundaries. | Document ownership and support boundaries. |
| Use least privilege access. | Use least privilege access. |
| Keep versions aligned. | Keep versions aligned. |
| Validate changes after implementation. | Validate changes after implementation. |
