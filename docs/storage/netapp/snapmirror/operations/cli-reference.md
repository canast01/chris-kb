---
tags:
  - netapp
  - operations
---
# SnapMirror — CLI Reference


<div class="kb-summary">
Part of the [SnapMirror Operations](index.md) reference.

*Applies to: SnapMirror*
</div>
```text
┌────────────────────────────────── NetApp SnapMirror — CLI Reference ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        SnapMirror CLI: command-line interface for all management and operational tasks        │   │
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
│   │            Async            │  │        Periodic sync        │  │         RPO: minutes        │   │
│   │             Sync            │  │           Zero RPO          │  │          Sub-ms lag         │   │
│   │            SM-BC            │  │        Active-active        │  │        Transparent FO       │   │
│   │            Vault            │  │        Long retention       │  │         Backup copy         │   │
│   │            Cloud            │  │         ONTAP → CVO         │  │       Cloud DR/backup       │   │
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
│    Physical: Source ONTAP cluster · destination ONTAP cluster · intercluster LIFs · WAN link          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapMirror         = ONTAP replication; transfers only changed blocks after initial baseline sync  │
│    Intercluster LIF   = dedicated logical interface for SnapMirror traffic between clusters           │
│    SnapMirror policy  = defines schedule, retention, and transfer type (async/sync/vault)             │
│    Baseline transfer  = first full snapshot transfer establishing the SnapMirror relationship         │
│    Update             = incremental transfer; only sends new or changed blocks since last successfu...│
│    Snapmirror break   = breaks the DR relationship; activates destination volume for read-write       │
│    Resync             = re-establishes a broken SnapMirror relationship from the last common snapshot │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN volumes│
│    Mediator           = ONTAP Mediator; quorum service for SM-BC running on Linux VM at third site    │
│    SnapVault          = SnapMirror variant for backup retention; destination has independent schedule │
│    MirrorAndVault     = policy combining SnapMirror DR and SnapVault backup retention copies          │
│    Fanout             = single source volume replicating to multiple destination clusters simultane...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## ONTAP CLI

All commands are run from the ONTAP cluster shell. Use `cluster1::>` prompt notation.

| Command | Purpose |
|---|---|
| `snapmirror show` | Display all SnapMirror relationships |
| `snapmirror status` | High-level status of all relationships |
| `snapmirror update` | Trigger an incremental transfer |
| `snapmirror initialize` | Baseline transfer for a new relationship |
| `snapmirror resync` | Re-establish a broken relationship |
| `snapmirror break` | Quiesce and break the mirror (R/W at destination) |
| `snapmirror quiesce` | Pause transfers without breaking the relationship |
| `snapmirror abort` | Stop an in-progress transfer |
| `snapmirror delete` | Remove a relationship |
| `snapmirror create` | Define a new SnapMirror relationship |

### Status and Inspection

```bash
# Show all relationships with key fields
snapmirror show -fields source-path,destination-path,relationship-status,mirror-state,lag-time,healthy

# Show only unhealthy relationships
snapmirror show -fields source-path,destination-path,lag-time,unhealthy-reason -healthy false

# Show a specific relationship
snapmirror show -destination-path svm_dr:vol_data

# Verbose relationship detail
snapmirror show -destination-path svm_dr:vol_data -instance

# Lag time and health for threshold alerting
snapmirror show -fields lag-time,healthy | grep -v true
```

### Create and Initialize

```bash
# Create an async SnapMirror relationship (XDP — preferred for SVM-DR and volume DR)
snapmirror create -source-path svm_prod:vol_data \
  -destination-path svm_dr:vol_data \
  -policy MirrorAllSnapshots -schedule hourly

# Create with a custom throttle (KB/s)
snapmirror create -source-path svm_prod:vol_data \
  -destination-path svm_dr:vol_data \
  -policy MirrorAllSnapshots -max-transfer-rate 51200

# Initialize (baseline copy — can take hours for large volumes)
snapmirror initialize -destination-path svm_dr:vol_data

# Initialize all relationships on a specific destination SVM
snapmirror initialize -destination-path svm_dr:*

# Check initialization progress
snapmirror show -destination-path svm_dr:vol_data -fields transfer-progress,bytes-transferred
```

### Updates and Quiesce

```bash
# Manual incremental update
snapmirror update -destination-path svm_dr:vol_data

# Update all volumes on a destination SVM
snapmirror update -destination-path svm_dr:*

# Quiesce (stop new transfers, allow current to finish)
snapmirror quiesce -destination-path svm_dr:vol_data

# Abort an in-progress transfer
snapmirror abort -destination-path svm_dr:vol_data -h
```

### DR Failover Procedure

```bash
# Step 1: Quiesce (allow final transfer to finish if possible)
snapmirror quiesce -destination-path svm_dr:vol_data

# Step 2: Update to minimise RPO
snapmirror update -destination-path svm_dr:vol_data

# Step 3: Break the mirror (destination becomes read-write)
snapmirror break -destination-path svm_dr:vol_data

# Step 4: Mount the destination volume
volume mount -vserver svm_dr -volume vol_data -junction-path /vol_data

# Step 5: Create/update NFS export or CIFS share on DR SVM as needed
# Update DNS to point to DR SVM LIF
vserver services name-service dns hosts create -vserver svm_dr \
  -address 10.10.20.50 -hostname app.example.com
```

### Failback Sequence

```bash
# After source is recovered — re-establish reverse mirror from DR back to source

# Step 1: Resync (source becomes destination, DR stays R/W)
snapmirror resync -source-path svm_dr:vol_data \
  -destination-path svm_prod:vol_data

# Step 2: Wait for sync, then quiesce DR side
snapmirror update -destination-path svm_prod:vol_data
snapmirror quiesce -destination-path svm_prod:vol_data

# Step 3: Break from DR back to prod
snapmirror break -destination-path svm_prod:vol_data

# Step 4: Re-establish original direction
snapmirror resync -destination-path svm_dr:vol_data

# Step 5: Verify
snapmirror show -destination-path svm_dr:vol_data -fields mirror-state,lag-time
```

### Delete a Relationship

```bash
# Must quiesce/break first if Snapmirrored
snapmirror quiesce -destination-path svm_dr:vol_data
snapmirror break  -destination-path svm_dr:vol_data
snapmirror delete -destination-path svm_dr:vol_data

# Remove destination volume snapshots left behind
snapshot delete -vserver svm_dr -volume vol_data -snapshot "snapmirror*" -force
```

---

## Lag Monitoring and Alerts

```bash
# List all relationships with lag over 2 hours (manual check)
snapmirror show -fields source-path,destination-path,lag-time | \
  awk '$3 > "0:2:0:0"'

# Show RDF group / policy schedule (to cross-check expected lag)
snapmirror policy show -policy MirrorAllSnapshots
snapmirror schedule show

# EMS-based alert (set threshold at 4 hours)
event notification destination create -name snap-lag-email \
  -mail admin@example.com
event notification create -filter-name SnapMirrorLag \
  -destinations snap-lag-email
```

---

## REST API

Base URL: `https://<cluster-mgmt-ip>/api`

```bash
# Authenticate (basic auth inline — use stored creds in production)
BASEURL="https://ontap-cluster.example.com/api"
AUTH="-u admin:password"

# List all SnapMirror relationships
curl -sk $AUTH "$BASEURL/snapmirror/relationships" | \
  python3 -m json.tool

# Filter by state (broken-off)
curl -sk $AUTH "$BASEURL/snapmirror/relationships?mirror_state=broken_off" | \
  python3 -m json.tool

# Get a single relationship by UUID
curl -sk $AUTH "$BASEURL/snapmirror/relationships/<uuid>" | python3 -m json.tool

# Trigger an update (PATCH state to snapmirrored)
curl -sk -X PATCH $AUTH "$BASEURL/snapmirror/relationships/<uuid>" \
  -H "Content-Type: application/json" \
  -d '{"state":"snapmirrored"}' | python3 -m json.tool

# Break a relationship (PATCH state to broken_off)
curl -sk -X PATCH $AUTH "$BASEURL/snapmirror/relationships/<uuid>" \
  -H "Content-Type: application/json" \
  -d '{"state":"broken_off"}' | python3 -m json.tool

# Initialize a new relationship
curl -sk -X POST $AUTH "$BASEURL/snapmirror/relationships/<uuid>/transfers" \
  -H "Content-Type: application/json" -d '{}' | python3 -m json.tool

# Check active transfers
curl -sk $AUTH "$BASEURL/snapmirror/relationships/<uuid>/transfers" | python3 -m json.tool
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Snapmirror — Procedures](procedures/)
- [Snapmirror — Scripts](scripts/)
- [Snapmirror — Health Checks](health-checks/)
