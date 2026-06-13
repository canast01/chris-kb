---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# PowerStore — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Diagnostic Data Collection, Component-Level Diagnostics, Event Log Analysis, Replication Diagnostics, Log Locations and 1 more sections.
</div>
```text
┌──────────────────────────────────── Dell PowerStore — Diagnostics ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerStore diagnostics: log collection, health checks, and performance analysis        │   │
│   │          Tools: management CLI, REST API, vendor support bundle, and system event log         │   │
│   │          Performance: check I/O latency, throughput, queue depth, and cache hit rate          │   │
│   │       Collect support bundle before contacting vendor support to reduce time-to-resolve       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify issue → collect logs → run diagnostics → analyse → resolve                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   Volume group   │ Logical containe │      iSCSI/FC     │    Host group    │  Shared policy   │   │
│   │Protection policy │ Snapshot/repl ru │      Internal     │    Admin role    │    Per volume    │   │
│   │   Metro volume   │ Sync replication │    Internal RPC   │   Certificate    │     Zero RPO     │   │
│   │     Snapshot     │     PiT copy     │      Internal     │    Admin role    │ Space-efficient  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
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

## Diagnostic Data Collection

Before contacting Dell Support or performing deep troubleshooting, collect the standard diagnostic dataset. This avoids repeated back-and-forth with support and establishes a timestamped baseline.

### Generate a Support Package (Log Bundle)

PowerStore's support package collects system logs, hardware health dumps, configuration state, and event history into a single archive. This is the primary diagnostic deliverable for Dell Support.

```bash
# Request a support package via REST API
curl -k -X POST "https://<mgmt-ip>/api/rest/gather_support_materials" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "node_ids": ["<node-a-id>", "<node-b-id>"],
    "include_logs": true
  }'

# Monitor the job until complete
JOB_ID="<job-id from response>"
curl -k -X GET "https://<mgmt-ip>/api/rest/job/${JOB_ID}" \
  -H "DELL-EMC-TOKEN: <token>"

# Download the support package when the job state is 'Completed'
# PowerStore Manager → Settings → Support → Support Packages → Download
```

Alternatively, initiate from the UI: **PowerStore Manager → Help → Collect Support Materials**.

### System State Snapshot

```bash
# Collect the full diagnostic state in a single script run
# Save output to a timestamped file for reference

OUTFILE="pstore_diag_$(date '+%Y%m%d_%H%M%S').txt"
MGMT_IP="192.168.10.50"

echo "PowerStore Diagnostics: ${MGMT_IP}" > "$OUTFILE"
echo "Timestamp: $(date)" >> "$OUTFILE"

# Authenticate
TOKEN=$(curl -ks -X POST "https://${MGMT_IP}/api/rest/login_session" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' \
  | jq -r '.token')

AUTH=(-H "DELL-EMC-TOKEN: ${TOKEN}" -H "Accept: application/json")

collect() {
  echo "" >> "$OUTFILE"
  echo "=== $1 ===" >> "$OUTFILE"
  curl -ks -X GET "https://${MGMT_IP}/api/rest/${2}" "${AUTH[@]}" \
    | python3 -m json.tool >> "$OUTFILE" 2>&1
}

collect "SOFTWARE_INSTALLED" "software_installed"
collect "ALERTS_ACTIVE" "alert?state=active"
collect "HARDWARE" "hardware"
collect "DRIVES" "drive?select=name,health.state,life_remaining,drive_type,size"
collect "NODES" "node?select=name,health.state,node_id"
collect "POOLS" "pool?select=name,size_free,size_used,size_total,percent_used"
collect "VOLUMES" "volume?select=name,size,health.state,type"
collect "REPLICATION_SESSIONS" "replication_session?select=name,state,last_sync_time"
collect "NAS_SERVERS" "nas_server?select=name,health.state,current_node_id"
collect "HOSTS" "host?select=name,health.state,os_type"

echo "Diagnostics written to: $OUTFILE"
```

## Component-Level Diagnostics

### Drive Diagnostics

```bash
# Full drive inventory with health state and remaining life
curl -k -X GET "https://<mgmt-ip>/api/rest/drive?select=name,health.state,life_remaining,drive_type,size,firmware_version,model_number,serial_number" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -m json.tool

# Identify drives with low remaining life (< 10%)
curl -k -X GET "https://<mgmt-ip>/api/rest/drive?select=name,life_remaining" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for d in data:
    lr = d.get('life_remaining')
    if lr is not None and lr < 10:
        print(f'LOW LIFE: {d[\"name\"]} — {lr}% remaining')
"

# Get SMART data equivalent for a specific drive
curl -k -X GET "https://<mgmt-ip>/api/rest/drive/<drive-id>?select=name,health,life_remaining,model_number,serial_number,firmware_version" \
  -H "DELL-EMC-TOKEN: <token>"
```

### Node Diagnostics

```bash
# Node health summary
curl -k -X GET "https://<mgmt-ip>/api/rest/node?select=name,health,node_id,model,firmware_version" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -m json.tool

# Hardware component health (fans, PSUs, memory)
curl -k -X GET "https://<mgmt-ip>/api/rest/hardware" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -m json.tool

# Fan status
curl -k -X GET "https://<mgmt-ip>/api/rest/fan?select=name,health.state" \
  -H "DELL-EMC-TOKEN: <token>"

# Power supply status
curl -k -X GET "https://<mgmt-ip>/api/rest/power_supply?select=name,health.state" \
  -H "DELL-EMC-TOKEN: <token>"
```

### Network Port Diagnostics

```bash
# FC port status and statistics
curl -k -X GET "https://<mgmt-ip>/api/rest/fc_port?select=name,wwn,current_speed,health.state,node_id" \
  -H "DELL-EMC-TOKEN: <token>"

# Ethernet port status (management and iSCSI)
curl -k -X GET "https://<mgmt-ip>/api/rest/eth_port?select=name,mac_address,link_speed,health.state,node_id" \
  -H "DELL-EMC-TOKEN: <token>"

# iSCSI portal status
curl -k -X GET "https://<mgmt-ip>/api/rest/iscsi_portal?select=name,ip_address,iscsi_target_name,health.state" \
  -H "DELL-EMC-TOKEN: <token>"
```

### Performance Metrics Diagnostics

```bash
# Get real-time appliance-level performance metrics
curl -k -X GET "https://<mgmt-ip>/api/rest/appliance_metrics/query" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "entity": "appliance",
    "entity_id": "<appliance-id>",
    "metrics": ["avg_read_latency_ms", "avg_write_latency_ms", "total_iops", "read_iops", "write_iops", "avg_read_bandwidth_mb", "avg_write_bandwidth_mb"],
    "interval": "last_5_minutes"
  }'

# Volume-level performance (identify hot volumes)
curl -k -X GET "https://<mgmt-ip>/api/rest/volume_metrics/query" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "entity": "volume",
    "metrics": ["avg_read_latency_ms", "avg_write_latency_ms", "read_iops", "write_iops"],
    "interval": "last_1_hour",
    "order_by": "write_iops desc",
    "limit": 10
  }'
```

## Event Log Analysis

```bash
# Retrieve all events from the last 24 hours
curl -k -X GET "https://<mgmt-ip>/api/rest/event?select=created_timestamp,severity,message_key,arguments&order=created_timestamp desc" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -m json.tool

# Filter events by severity
curl -k -X GET "https://<mgmt-ip>/api/rest/event?severity=Critical&order=created_timestamp desc" \
  -H "DELL-EMC-TOKEN: <token>"

# Filter events by type (e.g., drive events)
curl -k -X GET "https://<mgmt-ip>/api/rest/event?resource_type=drive&order=created_timestamp desc" \
  -H "DELL-EMC-TOKEN: <token>"
```

## Replication Diagnostics

```bash
# Full replication session detail including error reason
curl -k -X GET "https://<mgmt-ip>/api/rest/replication_session?select=name,state,sync_state,last_sync_time,remaining_capacity_to_sync,failed_reason,role" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -m json.tool

# Check remote system connectivity state
curl -k -X GET "https://<mgmt-ip>/api/rest/remote_system?select=name,management_address,connection_state,data_connection_state" \
  -H "DELL-EMC-TOKEN: <token>"

# Metro Volume mediator status
curl -k -X GET "https://<mgmt-ip>/api/rest/remote_system?select=name,metro_sync_status,mediator_address" \
  -H "DELL-EMC-TOKEN: <token>"
```

## Log Locations

PowerStore does not expose its internal OS logs directly to users — all diagnostic data is collected via the support package or REST API. Key log locations within the support package:

| Log | Location in Support Package | Contents |
|---|---|---|
| System event log | `events/events.json` | All system events with timestamps and severity |
| Hardware fault log | `hardware/faults.json` | Drive and component faults |
| Replication log | `replication/sessions.json` | Replication session history and errors |
| Upgrade log | `upgrade/upgrade.log` | Software upgrade history and errors |
| Node service log | `nodes/node_<id>/service.log` | Node-level service events |
| NAS server log | `nas/nas_server_<id>/logs/` | NAS server event and protocol logs |

## Before Calling Dell Support

Collect the following before opening a support case to minimise time to resolution:

| Item | How to Collect |
|---|---|
| System serial number | PowerStore Manager → Hardware → Appliance → Serial Number |
| PowerStoreOS version | `GET /api/rest/software_installed` |
| Active alerts dump | `GET /api/rest/alert?state=active` (JSON output) |
| Hardware health dump | `GET /api/rest/hardware` (JSON output) |
| Replication session state | `GET /api/rest/replication_session` (JSON output) |
| Support package | Initiate from PowerStore Manager → Help → Collect Support Materials |
| Timeline of events | Note when the issue started and what changed immediately before |
| Error messages | Exact text from PowerStore Manager alerts or REST API error responses |
| Affected hosts | List of hosts experiencing I/O issues (if connectivity problem) |

When opening the case:

- **Product**: Dell PowerStore
- **Serial number**: from hardware view
- **Software version**: from software_installed API
- **Problem description**: describe the symptom, when it started, and the impact on hosts and workloads
- **Attach**: the support package and the system state JSON dump collected above

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
