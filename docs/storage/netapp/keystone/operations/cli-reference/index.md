# NetApp Keystone — CLI Reference


<div class="kb-summary">
CLI Reference reference covering Keystone Collector CLI, NetApp ONTAP REST API (Keystone Collector Bootstrap), Keystone Portal API, Quick Reference.
</div>

## Keystone Collector CLI

The Keystone Collector is managed via SSH and a dedicated CLI on the collector VM.

```bash
# Show Collector status and version
keystone-collector status
keystone-collector version

# Validate configuration
keystone-config validate

# Force data collection (triggers immediate usage push to Keystone portal)
keystone-collector collect --force

# Show last collection result
keystone-collector show-last-collection

# List managed arrays
keystone-collector list-arrays

# Update Collector software
keystone-collector upgrade --check     # dry-run
keystone-collector upgrade --apply
```
┌───────────────────────────── NetApp Keystone — Operations: CLI Reference ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           CLI reference: ONTAP admin commands for daily Keystone storage operations           │   │
│   │           Health: storage failover show, system health alert show, disk show -broken          │   │
│   │             Capacity: volume show -space, aggr show -space, df -h (NFS from host)             │   │
│   │           Performance: statistics show, qos statistics show, network interface show           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH cluster LIF -> ONTAP CLI; set -priv advanced for extended commands                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Health Commands       │  │      Capacity Commands      │  │        Perf Commands        │   │
│   │      storage fail show      │  │       volume show -sp       │  │       statistics show       │   │
│   │      system health show     │  │       aggr show -space      │  │        qos stat show        │   │
│   │      disk show -broken      │  │          snap list          │  │          nfsstat -l         │   │
│   │        event log show       │  │        vol efficiency       │  │        net stat show        │   │
│   │       system node show      │  │         quota report        │  │        lun stats show       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Collector CLI Linux: sudo keystone-collector status | logs | collect | upload                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Command      │      Output      │      Use When     │      Level       │      Notes       │   │
│   │storage fail show │     HA state     │       Daily       │      admin       │  Both Connected  │   │
│   │ aggr show -space │  Aggr capacity   │       Weekly      │      admin       │    <85% used     │   │
│   │  qos stat show   │  IOPS throttle   │      On alert     │      admin       │    Throttled?    │   │
│   │  event log show  │    EMS events    │      On alert     │      admin       │    Last 24 h     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SSH from jump host port 22 to cluster management LIF IP                                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    storage failover show    = Lists HA pair state; both nodes must be Connected                       │
│    system health alert show = Active system health alarms; review daily                               │
│    disk show -broken        = Lists failed/predictive-fail disks; action: replace                     │
│    event log show -sev err  = EMS errors; filter last 24 h                                            │
│    volume show -space       = Per-volume used/avail; check thin overcommit                            │
│    aggr show -space         = Aggregate physical capacity; key Keystone metric                        │
│    statistics show          = Live performance counters: latency, IOPS, throughput                    │
│    qos statistics show      = QoS policy hit rate; check if volumes are throttled                     │
│    volume efficiency show   = Dedup/compress savings; verify efficiency enabled                       │
│    quota report             = Displays qtree and user quotas; check for overages                      │
│    ks status                = Collector service; last upload time; upload backlog                     │
│    set -priv advanced       = Enable advanced CLI; required for diag-level cmds                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## NetApp ONTAP REST API (Keystone Collector Bootstrap)

```bash
# Test API connectivity from Collector VM to ONTAP
curl -s -u admin:<password> \
    "https://<ontap-mgmt-ip>/api/cluster" | jq '.name, .version.full'

# List SVMs via REST
curl -s -u admin:<password> \
    "https://<ontap-mgmt-ip>/api/svm/svms" | jq '.records[].name'

# Volume list via REST
curl -s -u admin:<password> \
    "https://<ontap-mgmt-ip>/api/storage/volumes?svm.name=<keystone-svm>" | \
    jq '.records[] | "\(.name) \(.space.used) / \(.space.size)"'
```

## Keystone Portal API

NetApp exposes Keystone subscription data via API for reporting and integration.

```python
import requests

PORTAL = "https://keystone.netapp.com/api/v1"
TOKEN  = "<keystone-api-token>"
HDR    = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Get subscription details
resp = requests.get(f"{PORTAL}/subscriptions", headers=HDR)
for sub in resp.json().get("subscriptions", []):
    print(f"{sub['subscriptionNumber']}  committed={sub['committedCapacity']} consumed={sub['consumedCapacity']}")
```

## Quick Reference

| Task | Command |
|---|---|
| Check Collector status | `keystone-collector status` |
| Force usage collection | `keystone-collector collect --force` |
| List managed arrays | `keystone-collector list-arrays` |
| Validate config | `keystone-config validate` |
| ONTAP volume list | `volume show -vserver <svm>` |
| ONTAP SnapMirror status | `snapmirror show` |
| Test ONTAP API | `curl -u admin:pass https://<ip>/api/cluster` |
