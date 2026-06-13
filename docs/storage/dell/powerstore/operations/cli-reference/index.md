---
tags:
  - dell
  - operations
---
# Dell PowerStore CLI Reference


<div class="kb-summary">
PowerStore management uses the PowerStore Manager web UI, REST API, and the `pstcli` command-line interface. `pstcli` connects to the PowerStore management IP and supports scripting and automation for all array operations.
</div>
```text
┌─────────────────────────────────── Dell PowerStore — CLI Reference ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerStore CLI: command-line interface for all management and operational tasks        │   │
│   │            Access: SSH or REST client to management IP; authenticate as admin role            │   │
│   │        Commands: status, list, create, modify, delete, show, and diagnostic operations        │   │
│   │          Scripting: use REST API or CLI in automation for provisioning and reporting          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH → authenticate → show status → configure → verify → log output                                 │
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
│   │     Category     │     Command      │      Purpose      │      Output      │      Notes       │   │
│   │      Status      │   show status    │    Health check   │   State/alerts   │    Daily run     │   │
│   │       List       │     list all     │     Inventory     │   Name/ID/size   │    Read-only     │   │
│   │      Create      │  create volume   │     Provision     │    New object    │    Change req    │   │
│   │      Delete      │ delete resource  │    Decommission   │   Confirmation   │   Irreversible   │   │
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


---

## Connection

```bash
# Connect to PowerStore CLI
pstcli -d <management-ip> -u admin

# Or set environment variables
export PSTCLI_HOST=<management-ip>
export PSTCLI_USER=admin
```

---

## Array & System Management

```bash
# Show system info and software version
pstcli -d <ip> -u admin "show /sys/primary_model"

# List all appliances
pstcli -d <ip> -u admin "show /appliance"

# Show hardware component status
pstcli -d <ip> -u admin "show /hardware"

# Show software version
pstcli -d <ip> -u admin "show /software_installed"

# Show active alerts
pstcli -d <ip> -u admin "show /alert?state=active"
```

---

## Volume Operations

```bash
# List all volumes
pstcli -d <ip> -u admin "show /volume"

# Show volume details
pstcli -d <ip> -u admin "show /volume/<id>"

# Create a volume
pstcli -d <ip> -u admin "create /volume name=<name> size=<size_bytes>"

# Delete a volume
pstcli -d <ip> -u admin "delete /volume/<id>"

# Map volume to host
pstcli -d <ip> -u admin "create /volume/<id>/host_volume_mapping host_id=<host_id>"
```

---

## Host Management

```bash
# List hosts
pstcli -d <ip> -u admin "show /host"

# Create a host
pstcli -d <ip> -u admin "create /host name=<name> os_type=<ESXi|Windows|Linux>"

# Add initiator to host
pstcli -d <ip> -u admin "create /host_initiator host_id=<id> port_name=<wwn_or_iqn>"

# List host groups
pstcli -d <ip> -u admin "show /host_group"
```

---

## Snapshots & Protection

```bash
# List all snapshots
pstcli -d <ip> -u admin "show /volume_snapshot"

# Take a snapshot
pstcli -d <ip> -u admin "create /volume_snapshot volume_id=<id> name=<snap_name>"

# Delete a snapshot
pstcli -d <ip> -u admin "delete /volume_snapshot/<id>"

# List replication sessions
pstcli -d <ip> -u admin "show /replication_session"
```

---

## Capacity & Performance

```bash
# Show capacity summary
pstcli -d <ip> -u admin "show /appliance/<id>/metrics/capacity"

# Show performance metrics
pstcli -d <ip> -u admin "show /appliance/<id>/metrics/performance"

# Show drive health
pstcli -d <ip> -u admin "show /drive"
```

---

## REST API (Alternative)

```bash
# Authenticate and get token
curl -k -X POST https://<ip>/api/rest/login_session \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}'

# List volumes (use token from login)
curl -k -X GET https://<ip>/api/rest/volume \
  -H "DELL-EMC-TOKEN: <token>"

# List alerts
curl -k -X GET https://<ip>/api/rest/alert \
  -H "DELL-EMC-TOKEN: <token>"
```

---

## Common Patterns

```bash
# Full health check sequence
pstcli -d <ip> -u admin "show /alert?state=active"
pstcli -d <ip> -u admin "show /hardware"
pstcli -d <ip> -u admin "show /drive"
pstcli -d <ip> -u admin "show /replication_session"
```
