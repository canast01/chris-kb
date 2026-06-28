---
tags:
  - netapp
  - ontap
  - quick-start
---
# ONTAP Day 1 — New Cluster Checklist

<div class="kb-summary">
What to do in your first hour with a new ONTAP cluster. Covers cluster orientation, health validation, key metrics to capture, and the first operational tasks.
</div>

![ONTAP Day 1](../../assets/reference-quick-start-ontap-day1.svg)

---

## 1. Orient

Establish the basic topology before anything else.

```bash
# Cluster identity
cluster show

# Node list with versions
system node show -fields node,model,serial-number,uptime

# ONTAP version per node
system image show

# SVM list
vserver show -fields vserver,type,state,allowed-protocols

# Aggregate layout
storage aggregate show -fields aggregate,node,state,size,used-size,percent-used
```

Record these facts:

| Item | Command | Note |
|------|---------|------|
| Cluster name | `cluster show` | Match DNS entry |
| Node count | `system node show` | Note HA pairs |
| ONTAP version | `system image show` | Flag if mixed versions exist |
| SVM count | `vserver show` | Note data vs. admin vs. system SVMs |
| Aggregate count | `storage aggregate show` | Check all aggregates are online |

---

## 2. First Health Checks

Run these checks in sequence. A failure at any step should be investigated before continuing.

### Cluster Health

```bash
cluster show
```

The `Health` column should show `true` for all nodes. Any `false` indicates an active problem.

### System Health

```bash
system health status show
system health alert show
```

`Status: ok` is the target. Review any open alerts — they map to specific subsystems (SAS, network, RAID).

### Aggregate Space

```bash
storage aggregate show-space -fields aggregate,size,used,available,percent-used
```

Flag aggregates above **80% used**. Above **90%** is a hard risk for volume guarantee failures and snapshot deletion cascades.

### Volume Space

```bash
volume show -fields volume,vserver,state,size,used,available,percent-used | sort -k6 -n
```

Note any volumes approaching their size limit or with autogrow disabled.

### SnapMirror Lag

```bash
snapmirror show -fields source-path,destination-path,lag-time,mirror-state,relationship-status
```

Expected lag depends on schedule — for hourly replication, anything over 2 hours is worth flagging. Broken relationships show `relationship-status: broken-off`.

### AutoSupport Last Sent

```bash
system node autosupport history show -node * -type all | head -5
```

If the last AutoSupport is more than 24 hours old, check connectivity and SMTP/HTTPS transport:

```bash
system node autosupport show -node * -fields transport,mail-hosts,state
```

---

## 3. Know the Numbers

Capture these metrics in a site record or handoff document.

| Metric | Command | Healthy Range |
|--------|---------|---------------|
| Aggregate used % | `storage aggregate show-space` | &lt; 80% |
| Volume count | `volume show -state online | wc -l` | Know your count |
| SnapMirror lag | `snapmirror show -fields lag-time` | &lt; 2× schedule interval |
| AutoSupport last sent | `system node autosupport history show` | &lt; 24 hours |
| Shelf/disk count | `storage disk show | wc -l` | Matches expected |
| Spare disks | `storage disk show -container-type spare` | At least 1 per shelf |

---

## 4. Common First Tasks

### Create a Volume

```bash
volume create -vserver <svm-name> -volume <vol-name> \
  -aggregate <aggr-name> -size 100G \
  -junction-path /<vol-name> \
  -snapshot-policy default \
  -space-guarantee none
```

Verify:

```bash
volume show -volume <vol-name> -fields state,size,junction-path
```

### Create a LIF

```bash
network interface create -vserver <svm-name> \
  -lif <lif-name> -role data \
  -data-protocol nfs,cifs \
  -home-node <node-name> -home-port <e0c> \
  -address <ip> -netmask <mask>
```

Verify:

```bash
network interface show -vserver <svm-name> -fields lif,address,status-oper,is-home
```

### Set Up a Snapshot Policy

Create or assign a policy to a volume:

```bash
# List existing policies
volume snapshot policy show

# Assign an existing policy to a volume
volume modify -vserver <svm-name> -volume <vol-name> -snapshot-policy <policy-name>

# Create a new policy
volume snapshot policy create -policy <policy-name> -enabled true \
  -schedule1 hourly -count1 24 \
  -schedule2 daily -count2 7 \
  -schedule3 weekly -count3 4
```

---

## See Also

- [ONTAP Cheat Sheet](../cheat-sheets/netapp/) — top CLI commands
- [NetApp ONTAP Architecture](../../../storage/netapp/ontap/architecture/)
- [ONTAP Health Check Runbook](../../storage/netapp/ontap/health-checks/)
- [Pure FlashArray Day 1](../pure-flasharray-day1/) — if Pure is also in the environment
