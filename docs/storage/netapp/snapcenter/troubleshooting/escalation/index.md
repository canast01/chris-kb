# SnapCenter — Escalation


<div class="kb-summary">
> Part of the [SnapCenter Troubleshooting](../index.md) reference.
</div>
```
┌─────────────────────────────────── NetApp SnapCenter — Escalation ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     SnapCenter escalation: severity triage, vendor support contact, and required artifacts    │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │          Windows VM         │  │       Central control       │   │
│   │           Plug-in           │  │          Host agent         │  │        App-consistent       │   │
│   │            Policy           │  │       Schedule/retain       │  │         Backup rule         │   │
│   │        Resource group       │  │       Grouped targets       │  │        Shared policy        │   │
│   │           Recovery          │  │       Volume/LUN/file       │  │       Granular restore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapCenter         = NetApp backup orchestration; coordinates app-consistent snapshots via plug-ins│
│    Plug-in            = host-side agent; quiesces application before snapshot: SQL, Oracle, VMware    │
│    Resource group     = set of resources sharing a backup policy and schedule in SnapCenter           │
│    Policy             = SnapCenter object defining snapshot frequency, retention, and replication t...│
│    App-consistent     = snapshot taken after DB quiesce; guarantees crash-consistent recovery         │
│    Clone lifecycle    = SnapCenter clone: create from snapshot, provision to host, then delete        │
│    FlexClone          = underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone      │
│    Vault policy       = SnapCenter policy that also replicates snapshots to SnapVault destination     │
│    Mirror policy      = SnapCenter policy that replicates snapshots via SnapMirror to DR cluster      │
│    RBAC               = SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles  │
│    SMF                = SnapCenter MySQL database storing job history, policies, and resource configs │
│    SnapCenter API     = REST API on port 8143; full feature coverage for automation workflows         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Support Portal

[https://mysupport.netapp.com](https://mysupport.netapp.com)

Open SnapCenter cases under: Storage Software → SnapCenter. Cases are handled by NetApp support engineers specialising in SnapCenter and its application plugins.

## Information to Collect

Before opening a case or during initial triage, collect:

| Item | Source |
|---|---|
| SnapCenter Server version | Help → About in GUI; or `Get-SmHost -HostType SnapCenter` |
| Plugin versions on affected hosts | Settings → Hosts → view plug-in version column |
| ONTAP version of registered storage systems | `Get-SmStorageConnection` then `system image show` on ONTAP |
| Job ID and error message | Jobs → Monitor → select failed job → View Logs |
| SnapCenter support bundle | Help → Support → Generate Support Bundle (all logs + config) |
| Windows Event Log from SnapCenter Server | Application log, System log, export as .evtx |
| Plugin host OS logs | Windows Event Log or `/var/opt/snapcenter/spl/logs/` on Linux |
| ONTAP EMS logs (for snapshot/SnapMirror failures) | `event log show -severity error -time-range 24h` |

```powershell
# Generate SnapCenter support bundle via PowerShell
Get-SmSupportBundle -Path C:\temp\snapcenter-support-bundle

# Collect version info
Get-SmHost | Select HostName, HostType, PlugInVersion, SnapCenterVersion | Format-Table
```

## SLA Tiers — NetApp SupportEdge

| Priority | Response Time | Criteria |
|---|---|---|
| P1 — Critical | 1 hour | All backups failing; active data loss risk; production DR blocked |
| P2 — High | 2 hours | Most backup jobs failing; restore capability impaired |
| P3 — Medium | 4 hours | Individual resource group failing; workaround available |
| P4 — Low | Next business day | Configuration questions, feature requests, non-urgent issues |

For P1 SnapCenter cases, call the NetApp support line after opening the web case to ensure immediate assignment: +1-888-463-8277.

## Escalation Path

1. **Initial case**: Assigned to a SnapCenter Technical Support Engineer (TSE) via [mysupport.netapp.com](https://mysupport.netapp.com)
2. **Application specialist escalation**: TSE escalates to an Oracle/SQL/VMware application plugin specialist if the issue is in the plugin layer
3. **Development escalation**: For confirmed bugs, the TSE opens a bug report (BUG ID) and escalates to SnapCenter engineering; you receive a tracking ID
4. **Duty Manager escalation**: If response SLA is breached or the issue is unresolved after reasonable time, request escalation to the Support Duty Manager — state your case number and SLA breach
5. **Account team**: Engage your NetApp Account Manager for persistent P1 issues or SLA disputes
