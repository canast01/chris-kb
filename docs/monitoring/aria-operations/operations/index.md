# Aria Operations Operations
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

## Remote Collector Connectivity

Check remote collector health from each distributed site:

```text
Admin > Environment > Remote Collectors
- Status: Online / Offline
- Last heartbeat timestamp
- Assigned adapters
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
