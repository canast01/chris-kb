---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# ONTAP — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, AutoSupport, Information to Collect, SLA Tiers — NetApp SupportEdge, Escalation Path.

*Applies to: ONTAP 9.x*
</div>
```text
┌────────────────────────────────────── NetApp ONTAP — Escalation ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       ONTAP escalation: severity triage, vendor support contact, and required artifacts       │   │
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
│   │           Cluster           │  │        HA node pairs        │  │          Scale-out          │   │
│   │             SVM             │  │        Virtual server       │  │       Protocol access       │   │
│   │          Aggregate          │  │         RAID groups         │  │         Storage pool        │   │
│   │           FlexVol           │  │         Thin volume         │  │        Data container       │   │
│   │          SnapMirror         │  │         Replication         │  │          Async/Sync         │   │
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
│    Physical: AFF/FAS HA node pairs · cluster network · client access network · MetroCluster           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ONTAP              = NetApp storage OS; unified NAS, SAN, and object across AFF, FAS, ONTAP Select │
│    SVM                = Storage Virtual Machine; logical storage server with protocols, IP, and vol...│
│    Aggregate          = RAID group of disks; underpins FlexVols and FlexGroups within a node          │
│    FlexVol            = flexible thin-provisioned volume within an aggregate; most common container   │
│    FlexGroup          = scale-out volume spanning multiple aggregates; for very large NAS workloads   │
│    SnapMirror         = async or synchronous replication between ONTAP systems for DR and backup      │
│    SnapVault          = backup-oriented SnapMirror variant; independent retention at destination      │
│    FlexClone          = instant space-efficient writable clone of a volume or LUN from snapshot       │
│    Snapshot           = ONTAP space-efficient PiT copy; stored in .snapshot directory on NFS          │
│    ONTAP Mediator     = third-site quorum for SnapMirror SM-BC; prevents split-brain scenarios        │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN repl...│
│    vserver            = ONTAP CLI name for SVM; vserver show and vserver nfs show are common commands │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Support Portal

[https://support.netapp.com](https://support.netapp.com)

- Case management, knowledge base, downloads, and compatibility tools
- Login with NetApp SSO credentials tied to your support contract serial numbers
- Active IQ / BlueXP dashboard: [https://bluexp.netapp.com](https://bluexp.netapp.com)

## AutoSupport

AutoSupport is the primary mechanism for NetApp support engineers to diagnose your system remotely. Ensure it is configured and delivering before opening a case.

```bash
# Verify AutoSupport configuration
system node autosupport show

# Test AutoSupport delivery
system node autosupport invoke -node * -type test

# Generate a support AutoSupport tied to an open case
system node autosupport invoke -node * -type all -message "case <number> - <brief description>"

# Show AutoSupport delivery history
system node autosupport history show -node * -most-recent 10
```

## Information to Collect

Before opening a case or during initial triage, collect:

| Item | Command / Source |
|---|---|
| ONTAP version and platform | `system node show -fields model,ontap-version,serial-number` |
| Cluster health summary | `cluster show`; `storage failover show` |
| Active health alerts | `system health alert show` |
| EMS event log (last 24h) | `event log show -severity error -time-range 24h` |
| AutoSupport bundle | `system node autosupport invoke -node * -type all -message "case <number>"` |
| Aggregate and volume status | `storage aggregate show`; `volume show -fields used-percent` |
| SnapMirror relationship health | `snapmirror show -fields lag-time,healthy,relationship-status` |
| Network interface status | `network interface show`; `network port show -fields health-status` |
| Storage disk broken list | `storage disk show -broken` |
| Node sysconfig | `system node run -node <node> sysconfig -a` |

For performance issues, also collect:
```bash
# QoS statistics
qos statistics performance show

# Network interface statistics
network interface statistics show

# Disk latency histogram (node shell)
system node run -node <node> sysstat -c 5 -x 2
```

## SLA Tiers — NetApp SupportEdge

| Priority | Response Time | Criteria |
|---|---|---|
| P1 — Critical | 1 hour | Production system down; no workaround; data at risk |
| P2 — High | 2 hours | Significant degradation; workaround exists but impractical |
| P3 — Medium | 4 hours | Partial degradation; workaround available; non-urgent issues |
| P4 — Low | Next business day | General questions, planning, non-impacting issues |

SLA clock starts from case creation and first engineer acknowledgment. For P1, call the NetApp support line directly after opening the case online to ensure immediate pickup — do not rely on the web portal alone for critical cases.

**NetApp support phone (US/Global)**: +1-888-463-8277 (SupportEdge 24×7 required for P1/P2 after-hours)

## Escalation Path

1. **Initial case**: Open via [mysupport.netapp.com](https://support.netapp.com) or phone; assigned to a Technical Support Engineer (TSE)
2. **Escalation to specialist**: TSE escalates to a product specialist or escalation engineer if the issue requires deeper expertise — typically within the same business day for P1/P2
3. **Duty Manager escalation**: If response is inadequate, request escalation to the Support Duty Manager via the support portal or phone; state the case number and the escalation reason
4. **Account team escalation**: Engage your NetApp Account Manager and Systems Engineer for persistent P1 issues, commercial disputes, or SLA breach claims
5. **Executive escalation**: NetApp has a formal executive escalation process for critical accounts — initiated by your Account Manager

When escalating, always reference:
- Case number
- System serial number(s)
- Business impact (applications affected, data at risk, revenue impact)
- Timeline of events and actions already taken

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
