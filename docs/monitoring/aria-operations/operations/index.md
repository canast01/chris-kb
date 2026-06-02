# Aria Operations Operations

<div class="kb-summary">
Aria Operations Operations reference covering Daily Checklist, Alert Triage Workflow, Monthly Tasks.
</div>

## Daily Checklist

Run through these checks each morning before the ops team stand-up.

| Check | Location | Pass Criteria |
|---|---|---|
| Active Alerts review | Dashboards > Active Alerts | No unacknowledged Critical/Immediate alerts |
| Cluster node health | Admin > Cluster Management | All nodes show Online |
| Adapter collection status | Admin > Solutions | All adapters in Collecting state |
| Disk usage — analytics nodes | Admin > Cluster Management > [Node] > Disk | Below 80% used |
| Remote Collector status | Admin > Environment > Remote Collectors | All collectors Online |

Any failed check should be raised in the team channel and tracked in the ops log before the stand-up.

## Alert Triage Workflow

```text
1. Open Active Alerts dashboard
2. Filter by Severity: Critical, Immediate
3. For each alert:
   a. Identify affected object (VM, host, cluster, datastore)
   b. Check Recent Events on the object for correlated changes
   c. Determine if alert is genuine, transient, or noise:
      - Genuine: raise incident in ServiceNow
      - Transient (resolved within threshold period): annotate and close
      - Noise: review alert definition and adjust threshold or suppression
4. Acknowledge all reviewed alerts
5. Add notes to ServiceNow ticket referencing the alert name and object
```
```
┌──────────────────────────────────── Aria Operations — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Aria Operations Day-2 Operations — Health, Maintenance, and Housekeeping Tasks        │   │
│   │         Daily checks: cluster health · adapter status · alert queue depth · disk usage        │   │
│   │       Weekly tasks: review capacity forecasts · compliance report · stale alert cleanup       │   │
│   │       Monthly: log rotation · user audit · MP version check · certificate expiry review       │   │
│   │         Emergency: vracli restart service · cluster rejoin · support bundle collection        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Log the support bundle path before engaging VMware TAM: /data/support_bundle/                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Daily Checks        │  │         Weekly Tasks        │  │        Monthly Tasks        │   │
│   │      Cluster health OK      │  │      Capacity forecast      │  │         Log rotation        │   │
│   │      Adapter status OK      │  │      Compliance report      │  │          User audit         │   │
│   │       Alert queue <500      │  │      Stale alert purge      │  │       MP version check      │   │
│   │        Disk <80% full       │  │       Dashboard review      │  │       Cert expiry scan      │   │
│   │     Collector reachable     │  │       Group membership      │  │        Backup verify        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Operations tasks performed via Aria Ops UI (HTTPS/443) or vracli SSH on master node                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vracli            = Aria Ops CLI: vracli cluster status · vracli services restart                    │
│  Cluster health    = UI indicator aggregating node status, service health, and Cassandra ring         │
│  Adapter status    = Green/Yellow/Red collector connectivity state in Administration > Adapters       │
│  Alert queue       = Count of active unacknowledged alerts; >500 requires triage                      │
│  Support bundle    = Compressed diagnostic archive: vracli support-bundle collect                     │
│  Log rotation      = Automated log file cycling to prevent disk exhaustion                            │
│  Stale alert purge = Cancelling alerts whose monitored object no longer exists                        │
│  Certificate expiry= TLS cert used by adapter or UI; must be renewed before expiry                    │
│  Compliance report = Scheduled export of policy violation counts per compliance pack                  │
│  MP version check  = Verifying Management Packs match vendor release notes                            │
│  User audit        = Review of local and AD-synced users for inactive or excessive roles              │
│  Cassandra ring    = Distributed DB health; vracli cassandra status shows ring state                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

If a Remote Collector goes Offline, check:
- VM power state
- Network connectivity (TCP 443 to analytics cluster VIP)
- Collector service status: log into collector VM and run `systemctl status vmware-casa`

## Monthly Tasks

- Generate Monthly Executive Capacity Summary report and distribute
- Review alert noise: identify alert definitions with the highest fire frequency and tune thresholds
- Audit user accounts: Admin > Access Control > User Accounts — remove stale accounts
- Verify management pack versions are current (Admin > Solutions > check each adapter version)
- Review data node disk usage trend — project growth against retention policy
