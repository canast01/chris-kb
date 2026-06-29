---
tags:
  - dell
  - troubleshooting
  - powerstore
search:
  boost: 1.5
---
# PowerStore — Diagnostics

<div class="kb-summary">
Dell PowerStore diagnostic commands: query cluster and hardware health via the REST API, list critical events, check volume and host connectivity, inspect per-appliance alert status, and generate a SupportAssist support bundle from PowerStore Manager for Dell cases.

*Applies to: Dell PowerStore OS 3.x / 4.x*
</div>
![PowerStore — Diagnostics](../../../../assets/storage-dell-powerstore-troubleshooting-diagnostics.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "GET /api/rest/cluster\nGET /api/rest/hardware select=name,type,lifecycle_state" {shape: rectangle}
D: "GET /api/rest/volume select=name,state\nGET /api/rest/host_volume_mapping" {shape: rectangle}
E: "GET /api/rest/event filter=severity=Critical\nPowerStore Manager Alerts page" {shape: rectangle}
F: "GET /api/rest/fc_port select=name,current_speed,link_state\nGET /api/rest/eth_port" {shape: rectangle}
G: "GET /api/rest/nas_server select=name,operational_status\nGET /api/rest/file_system" {shape: rectangle}
H: "GET /api/rest/replication_session\nCheck replication network path between appliances" {shape: rectangle}
I: "I" {shape: rectangle}
J: "GET /api/rest/appliance select=name,model,service_tag,health\nCheck hardware component health" {shape: rectangle}
K: "GET /api/rest/hardware filter failing components\nCheck physical drive or node LED" {shape: rectangle}
L: "GET /api/rest/host select=name,os_type,initiators\nVerify host is logged in to correct target ports" {shape: rectangle}
M: "GET /api/rest/event filter=severity=in.Critical.Major limit=50\nIdentify affected component from event description" {shape: rectangle}
N: "Check cable and SFP physical state\nVerify FC zone contains both initiator and target WWPNs" {shape: rectangle}
O: "GET /api/rest/nas_server\nCheck NTP sync: NAS depends on accurate time for Kerberos" {shape: rectangle}
P: "GET /api/rest/replication_session\nCheck replication Ethernet port and MTU" {shape: rectangle}
Q: "Collect SupportAssist bundle\nOpen Dell support case" {shape: rectangle}
R: "Provide: PowerStore OS version, appliance serial\nEvent log export and support bundle" {shape: rectangle}
A: "PowerStore Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> K
D -> L
E -> M
F -> N
G -> O
H -> P
J -> Q
K -> Q
L -> Q
M -> Q
N -> Q
O -> Q
P -> Q
Q -> R
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_cluster_and_appliance_h: "Step 1 — Check cluster and appliance health via REST API" {shape: rectangle}
step_2_check_recent_critical_events: "Step 2 — Check recent critical events" {shape: rectangle}
step_3_check_volume_and_host_connect: "Step 3 — Check volume and host connectivity" {shape: rectangle}
step_4_check_fc_and_ethernet_port_he: "Step 4 — Check FC and Ethernet port health" {shape: rectangle}
step_5_check_nas_server_and_file_sys: "Step 5 — Check NAS server and file system health" {shape: rectangle}
step_6_check_replication_sessions: "Step 6 — Check replication sessions" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_cluster_and_appliance_h: investigate
symptom -> step_2_check_recent_critical_events: investigate
symptom -> step_3_check_volume_and_host_connect: investigate
symptom -> step_4_check_fc_and_ethernet_port_he: investigate
symptom -> step_5_check_nas_server_and_file_sys: investigate
symptom -> step_6_check_replication_sessions: investigate
step_1_check_cluster_and_appliance_h -> resolution
step_2_check_recent_critical_events -> resolution
step_3_check_volume_and_host_connect -> resolution
step_4_check_fc_and_ethernet_port_he -> resolution
step_5_check_nas_server_and_file_sys -> resolution
step_6_check_replication_sessions -> resolution
```

## Before you begin

- **Access:** PowerStore Manager admin credentials (HTTPS on port 443); SSH access requires Dell service account and is only used by Dell Support
- **Gather first:** the specific symptom (volume not visible, performance degradation, hardware alert), the affected appliance serial, and when the issue started
- **Scope:** confirm whether the issue affects one appliance, one volume/host, one protocol (FC/iSCSI/NAS), or the entire cluster

---

## Step 1 — Check cluster and appliance health via REST API

```bash
# Authenticate — PowerStore REST API uses cookie-based sessions
curl -sk -c /tmp/ps-cookie.txt \
  -X POST "https://<powerstore-mgmt-ip>/api/rest/login_session" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' > /dev/null
echo "Login complete"

# Cluster state (overall health)
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/cluster?select=name,state,management_address,master_appliance_id" | \
  python3 -m json.tool
# Expected: "state": "Configured"

# Per-appliance health (each physical unit in the cluster)
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/appliance?select=name,model,service_tag,drive_failure_tolerance_level,health" | \
  python3 -m json.tool
# Expected: health values all in OK state

# Hardware component health (drives, PSU, fans, nodes)
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/hardware?select=name,model,type,lifecycle_state,slot" | \
  python3 -c "
import json,sys
for h in json.load(sys.stdin):
    if h.get('lifecycle_state') not in ['Healthy','Empty','']:
        print(f\"{h['type']} {h['name']}: {h.get('lifecycle_state','?')}\")
" 2>/dev/null || \
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/hardware?select=name,model,type,lifecycle_state,slot" | \
  python3 -m json.tool
```

---

## Step 2 — Check recent critical events

```bash
# All Critical and Major events (most recent first)
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/event?select=created_timestamp,description,severity,category&order=created_timestamp.desc&limit=50" | \
  python3 -c "
import json,sys
for e in json.load(sys.stdin):
    sev = e.get('severity','?')
    if sev in ('Critical','Major','Warning'):
        ts  = e.get('created_timestamp','?')
        msg = e.get('description','?')
        print(f'[{sev}] {ts}: {msg}')
"

# Events for a specific time window (ISO 8601)
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/event?select=created_timestamp,description,severity&filter=created_timestamp.gt.2026-06-15T00:00:00.000Z&order=created_timestamp.desc" | \
  python3 -m json.tool
```

---

## Step 3 — Check volume and host connectivity

```bash
# List all volumes and their state
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/volume?select=name,state,size,wwn,appliance_id" | \
  python3 -c "
import json,sys
for v in json.load(sys.stdin):
    if v.get('state') != 'Ready':
        print(f\"PROBLEM: {v['name']} state={v.get('state','?')}\")
"

# Registered hosts
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/host?select=name,os_type,description" | \
  python3 -m json.tool

# Host-to-volume mappings
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/host_volume_mapping?select=host_id,volume_id,logical_unit_number" | \
  python3 -m json.tool
# Look for: expected host-to-volume mappings present
```

---

## Step 4 — Check FC and Ethernet port health

```bash
# FC port health (Fibre Channel host-facing ports)
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/fc_port?select=name,current_speed,link_state,appliance_id,wwn" | \
  python3 -c "
import json,sys
for p in json.load(sys.stdin):
    link = p.get('link_state','?')
    if link not in ('Up',''):
        print(f\"FC port {p['name']}: link_state={link}, speed={p.get('current_speed','?')}\")
"
# Expected: all host-facing FC ports link_state = Up

# Ethernet ports (iSCSI, NAS, replication)
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/eth_port?select=name,link_state,current_speed,mac_address,appliance_id" | \
  python3 -m json.tool
# Expected: all enabled ports link_state = Up
```

---

## Step 5 — Check NAS server and file system health

```bash
# NAS server status
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/nas_server?select=name,operational_status,current_node_id,health" | \
  python3 -m json.tool
# Expected: operational_status = Started

# File systems
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/file_system?select=name,size_total,size_used,health" | \
  python3 -m json.tool

# NFS exports
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/nfs_export?select=name,path,export_hosts" | \
  python3 -m json.tool

# SMB shares
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/smb_share?select=name,path,file_system_id" | \
  python3 -m json.tool
```

---

## Step 6 — Check replication sessions

```bash
# Replication sessions (MetroSync or async replication)
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/replication_session?select=name,state,last_sync_timestamp,estimated_completion_timestamp,lag_time" | \
  python3 -c "
import json,sys
for r in json.load(sys.stdin):
    state = r.get('state','?')
    lag   = r.get('lag_time','?')
    ts    = r.get('last_sync_timestamp','?')
    print(f\"{r['name']}: state={state}, lag={lag}, last_sync={ts}\")
"
# Expected: state = Synchronizing or Synchronized
# Problem: state = Failed, Paused, or lag increasing

# Replication remote system connectivity
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/remote_system?select=name,management_address,connection_state" | \
  python3 -m json.tool
# Expected: connection_state = Connected
```

---

## Step 7 — Collect SupportAssist bundle for Dell case

```bash
# Via PowerStore Manager (recommended):
# Settings → Support → SupportAssist → Collect Support Materials
# Download the bundle ZIP

# Via REST API (trigger bundle collection):
curl -sk -b /tmp/ps-cookie.txt \
  -X POST "https://<powerstore-mgmt-ip>/api/rest/support_instance?action=collect" \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool

# Prepare for Dell SR:
# PowerStore OS version: Settings → Software → Installed Software
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/software_installed?select=release_version" | \
  python3 -m json.tool

# Appliance serial numbers
curl -sk -b /tmp/ps-cookie.txt \
  "https://<powerstore-mgmt-ip>/api/rest/appliance?select=name,service_tag" | \
  python3 -m json.tool

# Include in Dell SR:
# - SupportAssist support bundle ZIP
# - PowerStore OS version
# - Appliance service tag(s)
# - Affected volume name, host name, or NAS server name
# - Event log export (REST event query output)
# - Time window of the issue
```

---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| Events | `GET /api/rest/event?filter=severity=in.Critical.Major` | Hardware faults, volume errors |
| Hardware | `GET /api/rest/hardware` | Component lifecycle state |
| Volumes | `GET /api/rest/volume` | Volume state (Ready vs. Offline) |
| FC ports | `GET /api/rest/fc_port` | Link state for host-facing ports |
| Replication | `GET /api/rest/replication_session` | State and lag time |
| Full bundle | SupportAssist via PowerStore Manager | All logs — required for Dell SR |

---

## See also

- [PowerStore — Common Issues](../common-issues/)
- [PowerStore — Escalation](../escalation/)

## Verify resolution

- `GET /api/rest/cluster` returns `"state": "Configured"` with no health alerts
- `GET /api/rest/hardware` shows no components with degraded lifecycle state
- `GET /api/rest/event?filter=severity=in.Critical.Major` shows no new events since the fix
- Host I/O test succeeds: mount the volume from the host and run a read/write test
- `GET /api/rest/replication_session` shows all sessions Synchronizing with lag decreasing
