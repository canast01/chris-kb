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

## Capacity Review (Weekly)

1. Navigate to **Dashboards > INFRA-Capacity-Overview**
2. Review time-remaining forecasts for CPU, memory, and datastore capacity
3. Flag any cluster or datastore showing < 60 days remaining to the capacity planning team
4. Download the weekly Capacity Overview report (Reports > Scheduled Reports)
5. Share report in the weekly infrastructure review meeting

## Top-N VM Review (Weekly)

Navigate to **Dashboards > INFRA-Performance-TopN** or run the Top-N VMs report:

- Top 10 VMs by CPU contention (> 5% sustained)
- Top 10 VMs by memory balloon/swap
- Top 10 VMs by disk latency

Escalate to application teams for VMs showing sustained contention above threshold.

## Adapter Health Checks

If an adapter shows **Not Receiving Data** or **Error**:

```text
1. Admin > Solutions > [Adapter] > Test Connection
2. Review adapter logs: Admin > Solutions > [Adapter] > Logs > Download
3. Common causes:
   - Credential expired or password rotated: update under Admin > Credentials
   - vCenter certificate changed: re-trust certificate in adapter settings
   - Network connectivity: verify TCP 443 from collector to target
4. If persistent: restart the adapter collection cycle under Solutions > [Adapter] > Start Collection
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
