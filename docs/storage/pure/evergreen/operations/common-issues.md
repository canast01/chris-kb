---
tags:
  - operations
  - pure
---
# Evergreen — Common Issues


<div class="kb-summary">
Common Issues reference covering Incident Triage Checklist, Common Issues Reference, Controller Upgrade Issues in Detail, Capacity Management Issues, Subscription and Lifecycle Issues and 2 more sections.
</div>

```text
Evergreen Common Issues — Triage
  Issue type
       │
   ┌────────────────────────────────────────────────── ┴ ──────────────────────────────────────────────────┐
   ▼                                           ▼
Capacity / subscription                 Hardware / performance
Pure1 subscription dashboard            purealert + puredrive
  │                                       │
  ▼                                       ▼
Contact account team                   Open support case
True Forward amendment                 Pure1 auto-monitors
   │
   ▼
Controller refresh missed:
  Contact Pure account team immediately
  Operating past support window voids Ever Modern guarantee
```

> Part of the [Evergreen Operations](index.md) reference.

---

This page covers the most common operational issues encountered with arrays running under an Evergreen subscription — covering controller upgrade problems, host path failures, capacity concerns, subscription management issues, and replication incidents.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Incident Triage Checklist

Before diving into specific issues, run the following sequence to establish the failure domain:

- [ ] Check Pure1 for any open hardware or software alerts — Pure1 often has context on incidents before the customer is aware
- [ ] Run `purealert list` on the affected array — identify whether the alert is hardware, software, or capacity
- [ ] Run `purearray list --controller` — confirm both controllers are online and running the same Purity version
- [ ] Run `puredrive list` — check for failed or evacuating drives
- [ ] Run `purepod list` — check ActiveCluster pod status if replication is involved
- [ ] Run `purehostconnection list` — confirm host path states; single-path hosts are a risk factor
- [ ] Check the Pure1 subscription dashboard — confirm capacity consumed vs. entitled and that phonehome is active

| Question | Where to Find the Answer |
|---|---|
| Is this a hardware or software failure? | `purealert list` and Pure1 > Arrays |
| Are both controllers healthy? | `purearray list --controller` |
| Are any drives failed? | `puredrive list` |
| Is this capacity-related? | `purearray list --space` |
| Is this replication-related? | `purepod list` |
| Is phonehome active? | Pure1 > Arrays > select array > Support > Phone Home |

---

## Common Issues Reference

| Symptom | Likely Cause | Action |
|---|---|---|
| Controller upgrade window missed | Subscription renewal not tracked with sufficient lead time | Contact Pure account team immediately — operating past the controller support window risks voiding the Ever Modern guarantee; the Pure account team can assess options for rescheduling |
| Host path goes offline during controller upgrade | Host multipathing not validated before upgrade; single-path hosts | Identify affected hosts with `purehostconnection list`; rescan HBAs or iSCSI initiators on affected hosts; contact Pure Support for guidance on path recovery |
| ActiveCluster mediator unreachable during upgrade | Network change or mediator misconfiguration; mediator IP changed | Verify mediator connectivity: `curl -sk https://<mediator-ip>/mediator/version`; update mediator IP in pod configuration if it has changed |
| Replication pod not replicating after upgrade | Network interruption during upgrade; pod paused or lag too high | Run `purepod list` to identify pod status; resume a paused pod: `purepod resume --name <pod_name>`; allow time for the pod to re-sync — lag reduces as replication catches up |
| Pure1 phonehome offline | Proxy change, firewall rule update, or network reconfiguration | Confirm outbound HTTPS port 443 to `*.purestorage.com` from the management interface; check proxy settings in the array GUI under System > Support |
| Capacity alert at upgrade time | Snapshot growth or volume provisioning without corresponding cleanup | Review snapshot space with `puresnap list --space`; eradicate old destroyed snapshots: `purevol eradicate --destroyed`; review and clean protection group snapshots before the upgrade |
| Purity software version outside supported range | Upgrade deferred too long; now outside N-2 support window | Contact Pure account team and support to plan an expedited upgrade path; some version gaps require intermediate upgrades — do not attempt to skip without guidance |
| Data reduction ratio below contracted guarantee | Workload mix changed; incompressible data (video, encrypted files) now dominant | Run `purearray list --space` to confirm the current effective data reduction ratio; contact Pure account team — if the ratio is below the contracted guarantee, Pure should provide additional capacity at no charge |
| Volume not visible to host after provisioning | Host group membership not configured; HBA not logged in; fabric zoning missing | Confirm the volume is connected to the correct host group: `purevol list --connection`; verify the host IQN or WWPN is registered in Purity: `purehost list`; check SAN fabric zoning |
| Snapshot retention growing unexpectedly | Protection group schedule creating more snapshots than the retention policy expires | Audit protection group schedules: `purepgroup list --schedule`; confirm retention policy settings match intent; eradicate accumulated expired snapshots |
| Performance below SLA for specific volumes | QoS limit not set; wrong array series for workload type; noisy neighbour | Review QoS settings on the affected volumes: `purevol list --space`; run a Pure1 workload assessment; engage the Pure account team to assess whether the array series (//X vs //C) is appropriate |
| ActiveCluster pod in `degraded` state | One array of the pair is unreachable from the pod perspective | Run `purepod list` on both arrays; verify network connectivity between the two arrays and to the mediator; Pure Support should be engaged for pod degraded events on production |

---

## Controller Upgrade Issues in Detail

### Pre-Upgrade Validation Failures

Run the following before any controller upgrade window to identify blockers early:

```bash
# Confirm all drives are healthy — no rebuilding or failed drives
puredrive list
puredrive list --filter "status!='healthy'"

# Confirm both controllers are online
purearray list --controller

# Confirm no active critical alerts
purealert list --severity error

# Confirm all pods are online (if ActiveCluster is deployed)
purepod list

# Confirm all hosts have redundant paths (no single-path hosts)
purehostconnection list
# Look for any host with only 1 path shown
```

**Common blockers and resolutions:**

| Blocker | Resolution |
|---|---|
| Drive rebuild in progress | Wait for the rebuild to complete before starting the upgrade window — `puredrive list` shows progress |
| Single-path host detected | Add a second path to the host before proceeding — do not upgrade with single-path hosts |
| Pod not online | Investigate and resolve pod health before upgrade — a degraded pod during upgrade may result in an extended outage |
| Snapshot count very high | Eradicate old destroyed snapshots to reduce upgrade duration: `puresnap eradicate --destroyed` |

### Path Recovery After Controller Upgrade

If host paths do not recover automatically after a controller swap:

**Linux (multipath):**

```bash
# On the affected Linux host
# Rescan the SCSI bus to detect new paths
for host in /sys/class/scsi_host/host*; do echo "- - -" > $host/scan; done

# Reload multipath to pick up new paths
multipathd reconfigure

# Confirm all expected paths are visible
multipath -ll
```

**VMware ESXi:**

```bash
# Rescan storage adapters in ESXi
esxcli storage core adapter rescan --all

# Confirm paths are active for each device
esxcli storage nmp device list | grep -A 5 <device_naa>
```

**Windows (MPIO):**

```powershell
# Rescan MPIO paths in PowerShell
mpclaim -r

# Confirm path state
mpclaim -s -d
```

---

## Capacity Management Issues

### Identifying Top Capacity Consumers

When capacity alerts fire or the subscription True Forward review is approaching:

```bash
# Overall capacity summary
purearray list --space

# Volume-level space usage — identify top consumers
purevol list --space | sort -k 2 -rh | head -20

# Snapshot space usage — identify snapshots consuming unexpected space
puresnap list --space | sort -k 3 -rh | head -20

# Protection group snapshot totals
purepgroup list --space

# Show space used by destroyed but not yet eradicated volumes
purevol list --destroyed --space
```

### Freeing Capacity Before a True Forward Review

```bash
# Eradicate destroyed volumes that are past the eradication timer
purevol eradicate --destroyed

# Eradicate old destroyed snapshots
puresnap eradicate --destroyed

# Review and trim snapshot retention on protection groups that have excessive history
purepgroup list --schedule
# Use the GUI or CLI to reduce the retention period for non-critical protection groups
```

### Confirming the Data Reduction Guarantee

```bash
# Check current effective data reduction ratio
purearray list --space
# Look for 'data_reduction' field — this is the current achieved ratio

# If the ratio is below the contracted guarantee:
# 1. Note the current ratio and contracted ratio
# 2. Contact the Pure account team — Pure should provide additional capacity at no charge
# 3. Identify the cause: incompressible data types, deduplication disabled on volumes
```

---

## Subscription and Lifecycle Issues

### Scheduling a Missed Ever Modern Controller Upgrade

If the controller upgrade window has been missed or is approaching its deadline:

1. Log into Pure1 and navigate to **Subscription > Lifecycle** to see the current controller generation and upgrade window status
2. Contact the Pure account team directly — do not wait for Pure to initiate contact
3. Provide the Pure account team with available maintenance windows (at least 3 options, 4+ hours each)
4. Confirm Purity software version is within the supported range for the new controller generation before scheduling — Pure will validate, but confirm independently using the compatibility matrix

### Checking Subscription Status

```bash
# Confirm phonehome is active (prerequisite for subscription monitoring)
purearray phonehome --status

# Confirm the array is registered in Pure1 (array must appear in Pure1 portal)
# Pure1 > Arrays — the array should appear with a green health score

# Subscription tier, renewal date, and controller generation
# Pure1 > Subscription > Dashboard
```

---

## Diagnostic Commands Summary

```bash
# Array health and version
purearray list
purearray list --controller
purearray list --hardware
purearray list --space

# All alerts
purealert list
purealert list --severity error

# Drive status
puredrive list
puredrive list --filter "status!='healthy'"

# Replication
purepod list
purepod list --replicating
purepod list --failover-preference

# Host paths
purehostconnection list
purehost list

# Snapshot space
puresnap list --space
purepgroup list --space

# Diagnostic bundle for Pure Support
purediag
```

---

## Before Calling Pure Support

Gather the following before opening a case to reduce time to resolution:

1. **Array serial number and Purity version** — `purearray list`
2. **Full alert output** — `purealert list`; copy the complete output
3. **Drive status** — `puredrive list`; copy the complete output
4. **Controller status** — `purearray list --controller`
5. **Pod status** (if replication is involved) — `purepod list`
6. **Host connection status** (if host I/O is affected) — `purehostconnection list`
7. **Diagnostic bundle** — `purediag`; Pure Support can pull this via phonehome if the support tunnel is active
8. **Symptom description** — what changed before the issue, when it started, and business impact
9. **Pure1 health score screenshot** — captures the fleet view context at time of incident

For controller upgrade or subscription issues, also have the Pure1 subscription dashboard available and the CSM contact details ready.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
