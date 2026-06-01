# Pure Storage Evergreen Troubleshooting


<div class="kb-summary">
Pure Storage Evergreen Troubleshooting reference covering Common Issues, Diagnostic Commands, Log Locations, Before Calling Support.
</div>

```text
Evergreen Troubleshooting Flow
  Symptom / alert
          │
          ▼
  Check Pure1 portal ──► fleet health + subscription status
          │
   ┌──────┴──────────────────────────────────────┐
   ▼                                             ▼
Capacity / subscription issue           Hardware / performance issue
Pure1 → subscription dashboard          purealert list
Contact account team                    puredrive list
Request True Forward amendment          purearray monitor
                                        Open support case if needed

Controller refresh issue:
  Contact Pure account team (90+ days lead time for scheduling)
```
## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Capacity utilisation exceeds subscription entitlement | Organic data growth, snapshot accumulation, or workload onboarding beyond plan | Review Pure1 capacity vs. subscription tier; identify top capacity consumers with `purearray list --space` and `puresnapshot list --space`; initiate a True Forward capacity upgrade if growth is sustained |
| Controller refresh notification missed | Pure1 lifecycle alert not actioned or subscription window not tracked | Check Pure1 lifecycle alerts and subscription dashboard; contact the Pure account team immediately to reschedule — operating past the controller support window voids the Ever Modern guarantee |
| Performance below SLA | Workload growth, QoS policy not set, or wrong array series for workload type | Run a Pure1 workload assessment; review QoS limits on affected volumes; engage Pure account team to assess whether tier (//X vs //C) is appropriate |
| Replication lag exceeds RPO | Network bandwidth insufficient for change rate, remote array degraded, or pod unhealthy | Run `purepod list` to check pod and ActiveCluster status; check replication network bandwidth; review `purealert list` on both source and target arrays |
| Snapshot retention growing unexpectedly | Protection group schedule creating more snapshots than retention policy expires | Audit protection group schedules with `purepgroup list --schedule`; confirm retention policy matches intent; eradicate accumulated expired snapshots |
| Host path offline after controller upgrade | Multipath failover not restored after Ever Modern controller swap | Run `purehostconnection list` to confirm all host path states; rescan HBAs or iSCSI sessions on affected hosts; contact Pure Support if paths do not restore |
| Pure1 phonehome offline | Proxy change, firewall rule update, or network reconfiguration blocked outbound 443 | Confirm outbound HTTPS to Pure1 endpoints; check proxy configuration in array GUI; restore phonehome before scheduling any maintenance — Pure Support visibility depends on it |
| Volume not visible to host after provisioning | Host group membership not set, or HBA/iSCSI initiator not logged in | Confirm volume is connected to the correct host group; verify host IQN or WWPN is registered in Purity; check SAN fabric zoning |

## Diagnostic Commands

```bash
# Capacity usage breakdown
purearray list --space

# Controller hardware status and generation
purearray list --controller

# All active alerts with severity
purealert list

# Replication pod status and ActiveCluster health
purepod list

# Recent snapshot inventory (first 20)
puresnap list | head -20

# Snapshot space consumption
puresnapshot list --space

# Host connection and path status
purehostconnection list

# Volume space and provisioned size
purevol list --space

# Protection group schedules and replication targets
purepgroup list --schedule

# Array hardware components
purearray list --hardware
```

## Log Locations

| Log Source | Location / Access |
|---|---|
| Pure1 phonehome logs | Pure1 portal > Arrays > select array > Support > Phone Home — history of phonehome sessions and any connectivity gaps |
| Array audit log | Purity GUI > Settings > Audit Log — all admin actions with user, timestamp, and IP; also forwarded to syslog if configured |
| `purediag` output | Run `purediag` on the array; generates a diagnostic bundle that Pure Support can pull via phonehome or download from the support portal |
| Array syslog | Forwarded to external syslog/SIEM if configured; contains hardware events, Purity OS messages, and audit entries |
| Pure1 alert history | Pure1 > Alerts — historical alert record for all arrays in the subscription including closed and auto-resolved alerts |

## Before Calling Support

Gather the following before opening a case to reduce time to resolution:

1. **Pure1 health score** — screenshot or note the current health score and any open alerts from Pure1 > Arrays
2. **`purediag` output** — run `purediag` and confirm the diagnostic bundle is available; Pure Support can pull it via phonehome if the tunnel is active
3. **Current Purity version** — `purearray list` — confirm exact Purity//FA version
4. **Subscription entitlement confirmation** — log into Pure1 and confirm the subscription tier, entitled capacity, and controller generation; this is needed if the issue relates to capacity, lifecycle, or controller refresh
5. **Alert history** — `purealert list` — all active and recent alerts
6. **Symptom timeline** — when did the issue start, what changed around that time, what has already been attempted

Having this information ready before calling significantly reduces time to first meaningful action from the support engineer.
