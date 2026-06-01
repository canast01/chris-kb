# Superna Eyeglass — CLI Reference


<div class="kb-summary">
Eyeglass provides the `igls` CLI accessible from the appliance shell via SSH and a REST API for automation. OneFS SyncIQ CLI commands are used alongside Eyeglass operations to verify the underlying replication state. SSH to the Eyeglass appliance as the `admin` user.
</div>

```mermaid
flowchart LR
    operator(["Operator /\nAutomation"])
    ssh["SSH\nadmin@eyeglass-ip"]
    iglsCLI["igls CLI\n(Eyeglass appliance)"]
    restAPI["REST API\nhttps://eyeglass-ip/eca/api/v1"]
    eyeglassSvc["Eyeglass Services\nDR orchestration"]
    psApi["PowerScale\nOneFS REST API"]
    synciq["SyncIQ\nReplication engine"]

    operator --> ssh --> iglsCLI --> eyeglassSvc
    operator --> restAPI --> eyeglassSvc
    eyeglassSvc --> psApi --> synciq
```
┌────────────────────────────────── Superna Eyeglass — CLI Reference ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Superna Eyeglass — Command Reference                             │   │
│   │           Use these commands for routine operations, scripting, and troubleshooting           │   │
│   │                                         igls quota list                                       │   │
│   │                                         igls dr runbook                                       │   │
│   │                                         igls sync status                                      │   │
│   │                                         igls rapa status                                      │   │
│   │                                       igls failover start                                     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Ports: 443 (Eyeglass web UI) · 8080 (REST API) · 8116 (Isilon/PowerScale mgmt)                     │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Command Categories                                      │   │
│   │                  Status / Query  — check current state, list jobs, show config                │   │
│   │                  Operations      — start, stop, failover, restore, sync, expire               │   │
│   │                Configuration   — add/modify policies, schedules, storage targets              │   │
│   │               Diagnostics     — collect logs, run health checks, test connectivity            │   │
│   │                  Scripting       — REST API or CLI for automation and reporting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link   │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection            │
│  RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats       │
│  SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies         │
│  DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS        │
│  Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster              │
│  Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product       │
│  Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits            │
│  Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site            │
│  Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team                  │
│  Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha       │
│  Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation      │
│  igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations                         │
│  SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation         │
│  Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

---

## Failback

Failback restores the original source cluster as the active side after a failover.

```bash
# List available failback jobs
igls failback list

# Run a failback
igls failback run --job <job_name>

# Monitor failback progress
igls failback status --job <job_name>
```

---

## OneFS SyncIQ (Supporting Commands)

Run these on the PowerScale/Isilon cluster to verify the underlying replication state that Eyeglass monitors.

```bash
# List all SyncIQ policies and their status
isi sync policies list

# Show detail for a policy
isi sync policies view <policy_name>

# List recent sync reports
isi sync reports list

# Start a manual SyncIQ sync
isi sync policies start <policy_name>

# Check SyncIQ service status
isi sync settings view
```

---

## REST API

The Eyeglass REST API is available at `https://<eyeglass_ip>/eca/api/v1`.

```bash
# Authenticate
curl -k -X POST https://<eyeglass_ip>/eca/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<pass>"}'

# List sync jobs
curl -k -X GET https://<eyeglass_ip>/eca/api/v1/jobs/sync \
  -H "Authorization: Bearer <token>"

# List failover jobs
curl -k -X GET https://<eyeglass_ip>/eca/api/v1/jobs/failover \
  -H "Authorization: Bearer <token>"
```
