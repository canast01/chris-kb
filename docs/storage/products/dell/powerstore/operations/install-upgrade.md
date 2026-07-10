---
tags:
  - dell
  - operations
---
# PowerStore — Install & Upgrade

<div class="kb-summary">
Install & Upgrade reference covering Initial Setup, Software Upgrade, Appliance Lifecycle.

*Applies to: PowerStore 3.x*
</div>
![PowerStore — Install & Upgrade](../../../../../assets/storage-dell-powerstore-operations-install-upgrade.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Initial Setup

### Pre-Installation Requirements

Before racking and initialising a new PowerStore appliance:

| Requirement | Details |
|---|---|
| Rack space | 2U per appliance (standard); cable management arm optional |
| Power | Dual power feeds (A and B circuit) per PSU set |
| Management network | 1 GbE switch port (dedicated management VLAN) |
| Data network | FC: 16/32 Gb switch ports per fabric; iSCSI: 10/25/100 GbE switch ports |
| IP addresses | Management IP (floating VIP), Node A mgmt, Node B mgmt, optional iSCSI data IPs |
| DNS | Forward and reverse DNS entries for the management FQDN |
| NTP | NTP server reachable from management network |
| SMTP relay | For alert email notifications (optional but recommended) |
| Laptop / management host | For initial configuration via the PowerStore Initial Configuration wizard |

### Initial Configuration Wizard

Dell ships PowerStore with a default management IP pre-configured. Connect a laptop to the management switch and access the Initial Configuration Wizard:

1. Navigate to `https://192.168.1.20` (default initial IP — verify with the Dell shipping documentation for the specific order)
2. Log in with the default credentials (`admin` / `Password123!` — change immediately)
3. Complete the Initial Configuration Wizard:
   - Set the management FQDN and IP address
   - Configure NTP servers
   - Configure DNS servers
   - Set the admin password (minimum 12 characters, at least one uppercase, one digit, one special character)
   - Configure SupportAssist (ESRS) if permitted
   - Optional: configure SMTP for email alerts
4. After the wizard completes, the array reboots with the new management IP
5. Access the production management IP and verify the Dashboard shows all hardware healthy

### Post-Installation Baseline

Complete these steps before onboarding the first workloads:

```bash
# Verify software version
curl -k -X GET "https://<mgmt-ip>/api/rest/software_installed" \
  -H "DELL-EMC-TOKEN: <token>"

# Verify hardware health (all components should be 'OK')
curl -k -X GET "https://<mgmt-ip>/api/rest/hardware" \
  -H "DELL-EMC-TOKEN: <token>"

# Set NTP configuration (if not done in wizard)
curl -k -X POST "https://<mgmt-ip>/api/rest/ntp_server" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"addresses": ["192.168.1.252", "192.168.1.253"]}'

# Configure LDAP/AD authentication
# PowerStore Manager → Settings → Security → LDAP Configuration

# Register with Secure Connect Gateway for CloudIQ
# SCG web UI → Devices → Add Device → enter PowerStore management IP
```


```text title="Expected output"
{
  "id": "software_installed_1",
  "version": "3.0.0.0",
  "release_date": "2024-01-15T00:00:00Z",
  "build": "Build 1234.5"
}
{
  "id": "hardware_1",
  "status": "OK",
  "components": [
    {
      "name": "SSD_1",
      "status": "OK",
      "health_score": 100
    },
    {
      "name": "PSU_A",
      "status": "OK",
      "health_score": 100
    },
    {
      "name": "PSU_B",
      "status": "OK",
      "health_score": 100
    },
    {
      "name": "FAN_MODULE_1",
      "status": "OK",
      "health_score": 98
    },
    {
      "name": "CTRL_A",
      "status": "OK",
      "health_score": 100
    }
  ]
}
{
  "id": "ntp_server_1",
  "addresses": ["192.168.1.252", "192.168.1.253"],
  "status": "configured"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to bypass certificate verification, or import the PowerStore management certificate into your system's trust store.
    **`{"error_code": 401, "message": "Invalid or expired token"}`** — Regenerate the authentication token via the PowerStore Manager UI or re-authenticate using valid credentials.
    **`curl: (7) Failed to connect to <mgmt-ip> port 443: Connection refused`** — Verify the management IP address is correct and reachable, and confirm the PowerStore REST API service is running.
## Software Upgrade

PowerStore software upgrades are non-disruptive to host I/O. The upgrade orchestrates a rolling restart of both nodes, maintaining continuous availability throughout.

### Upgrade Preparation

Before beginning an upgrade, complete a full pre-upgrade health check:

```bash
# 1. Verify no active alerts (clear all before upgrading)
curl -k -X GET "https://<mgmt-ip>/api/rest/alert?state=active&severity=CRITICAL" \
  -H "DELL-EMC-TOKEN: <token>"

# 2. Confirm all drives are healthy (no reconstructing or failed)
curl -k -X GET "https://<mgmt-ip>/api/rest/drive?select=name,health_state" \
  -H "DELL-EMC-TOKEN: <token>"

# 3. Confirm all replication sessions are synchronised
curl -k -X GET "https://<mgmt-ip>/api/rest/replication_session?select=name,state" \
  -H "DELL-EMC-TOKEN: <token>"

# 4. Check available capacity — upgrade staging requires temporary disk space
# Pool utilisation should be below 75% before upgrade
curl -k -X GET "https://<mgmt-ip>/api/rest/pool?select=name,percent_used" \
  -H "DELL-EMC-TOKEN: <token>"
```


```text title="Expected output"
{
  "entries": []
}
{
  "entries": [
    {
      "id": "drive_1",
      "name": "drive_1",
      "health_state": "Healthy"
    },
    {
      "id": "drive_2",
      "name": "drive_2",
      "health_state": "Healthy"
    },
    {
      "id": "drive_3",
      "name": "drive_3",
      "health_state": "Healthy"
    },
    {
      "id": "drive_4",
      "name": "drive_4",
      "health_state": "Healthy"
    }
  ]
}
{
  "entries": [
    {
      "id": "repl_session_prod_dr",
      "name": "prod_dr",
      "state": "Synchronized"
    },
    {
      "id": "repl_session_backup",
      "name": "backup",
      "state": "Synchronized"
    }
  ]
}
{
  "entries": [
    {
      "id": "pool_ssd_tier",
      "name": "SSD_Tier",
      "percent_used": 62.4
    },
    {
      "id": "pool_capacity",
      "name": "Capacity_Pool",
      "percent_used": 71.8
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip certificate verification, or import the management node's CA certificate into your system trust store.
    **`{"error_code":"401","message":"Invalid or expired token"}`** — Regenerate the DELL-EMC-TOKEN by authenticating to the management API and ensure the token has not exceeded its 24-hour expiration window.
    **`curl: (7) Failed to connect to <mgmt-ip> port 443: Connection refused`** — Verify the management IP address is correct, the PowerStore cluster is online, and port 443 is accessible from your client (check firewall rules and network connectivity).
**Additional pre-upgrade checks:**

- [ ] Check Dell PowerStore Interoperability Matrix for the target version against all connected components (vSphere, vCenter, SRA, Veeam)
- [ ] Review the PowerStoreOS Release Notes for the target version — note any upgrade sequencing requirements or known issues
- [ ] Take manual snapshots of critical volumes as a rollback option (snapshots are automatically taken by the upgrade process but taking manual pre-upgrade snapshots is belt-and-suspenders)
- [ ] Notify application teams of the maintenance window (even though host I/O is uninterrupted, management access may be briefly unavailable during node restart)

### PowerStoreOS Version Matrix

| From Version | To Version | Path | Notes |
|---|---|---|---|
| 3.x | 3.5.x | Direct | Single upgrade |
| 3.x | 4.x | Via 3.5.x | Must upgrade to 3.5.x first |
| 3.5.x | 4.0.x | Direct | Single upgrade |
| 4.0.x | 4.5.x | Direct | Single upgrade |
| Any version | Any version 2+ major versions ahead | Multi-hop | Follow the upgrade path in release notes |

> Always verify the specific upgrade path in the current PowerStoreOS Release Notes for the target version.

### Download and Apply the Upgrade

```bash
# Step 1: Download the upgrade package from Dell Support
# Portal: https://www.dell.com/support → Products → PowerStore → Downloads
# File: PowerStoreOS_4.5.x.x.bin (approximately 2–5 GB)

# Step 2: Upload to PowerStore via the Manager UI
# Settings → Software → Upload Software Package → browse to .bin file
# Or upload via REST API (multipart form upload)
curl -k -X POST "https://<mgmt-ip>/api/rest/software_package/upload" \
  -H "DELL-EMC-TOKEN: <token>" \
  -F "file=@/path/to/PowerStoreOS_4.5.x.x.bin"

# Step 3: Verify the package was uploaded and is valid
curl -k -X GET "https://<mgmt-ip>/api/rest/software_package" \
  -H "DELL-EMC-TOKEN: <token>"

# Step 4: Initiate the upgrade
curl -k -X POST "https://<mgmt-ip>/api/rest/software_package/<package-id>/install" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"appliance_ids": ["<appliance-id>"]}'
```


```text title="Expected output"
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 2.4G  100 2.4G    0     0  45.2M      0 --:--:--  0:00:54 --:--:-- 0:00:54

{
  "id": "pkg-4f8c2a1b-9e3d-47c2-b1a2-8f5c3d2e1a9b",
  "name": "PowerStoreOS_4.5.2.1.bin",
  "version": "4.5.2.1",
  "size": 2576980992,
  "status": "Valid",
  "upload_date": "2024-01-15T14:32:18Z",
  "checksum": "a7f3c9e2b1d4f8a5c3e2b1d4f8a5c3e2"
}

{
  "id": "job-5a2c8f1e-3b9d-42c1-a5d2-7e4c1f3a8b2d",
  "status": "In Progress",
  "appliance_id": "Appliance-1",
  "package_id": "pkg-4f8c2a1b-9e3d-47c2-b1a2-8f5c3d2e1a9b",
  "progress_percentage": 0,
  "estimated_time_remaining": 1800,
  "message": "Upgrade job initiated. System will reboot during upgrade."
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification, or import the PowerStore management certificate into your system's CA bundle.
    **`{"error": "Invalid or expired token"}`** — Regenerate the DELL-EMC-TOKEN via the Manager UI (Settings → API → Generate Token) and ensure it has not expired.
    **`{"error": "Package not found or invalid checksum"}`** — Re-download the .bin file from Dell Support Portal and verify the SHA256 checksum matches the published value before uploading.
### Upgrade Timeline

Typical upgrade durations:

| Appliance Model | Upgrade Duration |
|---|---|
| 500T / 500X | 45–90 minutes |
| 3000T / 3000X | 60–120 minutes |
| 9000T | 90–150 minutes |
| Cluster (4 appliances) | 3–6 hours (sequential per appliance) |

During the upgrade:

- Host I/O continues uninterrupted (paths temporarily shift during node restart)
- Management UI may be briefly unavailable (2–5 minutes per node restart)
- Replication sessions automatically pause and resume
- Do not manually intervene; the upgrade orchestration handles node sequencing

### Monitor Upgrade Progress

```bash
# Poll upgrade job status (run every few minutes during upgrade)
curl -k -X GET "https://<mgmt-ip>/api/rest/job?type=upgrade&state=running" \
  -H "DELL-EMC-TOKEN: <token>"

# Alternatively, monitor via PowerStore Manager
# Settings → Software → Current Upgrade → shows percentage complete and current step
```


```text title="Expected output"
{
  "entries": [
    {
      "id": "job-upgrade-20240115-001",
      "type": "upgrade",
      "state": "running",
      "progress_percentage": 67,
      "current_step": "Updating appliance firmware on node-2",
      "estimated_completion_time": "2024-01-15T14:32:00Z",
      "start_time": "2024-01-15T13:15:00Z",
      "nodes_completed": 1,
      "nodes_total": 3
    }
  ],
  "page": 1,
  "per_page": 100,
  "total": 1
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification (already present in the example, but ensure it's not removed).
    **`{"error": "Unauthorized", "error_code": 401}`** — Verify the DELL-EMC-TOKEN is valid and not expired by requesting a fresh token via the login endpoint.
    **`curl: (7) Failed to connect to <mgmt-ip> port 443: Connection refused`** — Confirm the management IP is correct and the PowerStore cluster is accessible on the network; check firewall rules allowing HTTPS to the management interface.
### Post-Upgrade Validation

```bash
# 1. Confirm new software version is running
curl -k -X GET "https://<mgmt-ip>/api/rest/software_installed" \
  -H "DELL-EMC-TOKEN: <token>"

# 2. Check for new alerts introduced by the upgrade
curl -k -X GET "https://<mgmt-ip>/api/rest/alert?state=active" \
  -H "DELL-EMC-TOKEN: <token>"

# 3. Verify replication sessions resumed
curl -k -X GET "https://<mgmt-ip>/api/rest/replication_session?select=name,state" \
  -H "DELL-EMC-TOKEN: <token>"

# 4. Verify host I/O paths are healthy on all hosts
# ESXi: esxcli storage nmp device list | grep PathSelectionPolicy
# Linux: multipath -ll | grep status

# 5. Verify CloudIQ is still receiving telemetry
# Log into cloudiq.dell.com; confirm system health score is visible
```


```text title="Expected output"
{
  "software_installed": [
    {
      "id": "sw_installed_001",
      "version": "3.2.1.0",
      "release_date": "2024-01-15T00:00:00Z",
      "build": "4567",
      "status": "Installed"
    }
  ]
}

{
  "alerts": [
    {
      "id": "alert_2847",
      "severity": "Warning",
      "message": "Replication session lag detected on session-prod-dr",
      "state": "active",
      "created_at": "2024-01-16T14:32:10Z"
    },
    {
      "id": "alert_2851",
      "severity": "Info",
      "message": "Software upgrade completed successfully",
      "state": "active",
      "created_at": "2024-01-16T13:45:22Z"
    }
  ]
}

{
  "replication_sessions": [
    {
      "name": "prod-to-dr-sync",
      "state": "Running"
    },
    {
      "name": "backup-async-session",
      "state": "Running"
    },
    {
      "name": "archive-weekly",
      "state": "Paused"
    }
  ]
}

name                                    policy
naa.6006016b8d0234a5c8e4f2a1b9c7d5e3f  service-time
naa.6006016b8d0234a5c8e4f2a1b9c7d5e3g  service-time

mpatha (36006016b8d0234a5c8e4f2a1b9c7d5) dm-0 DELL,PowerStore
size=500G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 2:0:0:1 sda 8:0  active ready running
  `- 3:0:0:1 sdb 8:16 active ready running
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to bypass certificate validation, or import the PowerStore management certificate into your system trust store.
    **`{"error": "Invalid or expired token"}`** — Regenerate the authentication token via the PowerStore management UI or API and update the DELL-EMC-TOKEN header value.
    **`Connection refused on <mgmt-ip>:443`** — Verify the management IP is correct and reachable; confirm the PowerStore management interface is online and the network path is not blocked by firewalls.
## Appliance Lifecycle

### Adding a Second Appliance to a Cluster (PowerStore T only)

```bash
# Step 1: Rack and cable the new appliance
# Step 2: Complete the Initial Configuration Wizard on the new appliance
# Step 3: Join the new appliance to the existing cluster
# PowerStore Manager → Settings → Appliances → Add Appliance → enter management IP of new appliance
# Or via REST API:
curl -k -X POST "https://<mgmt-ip>/api/rest/appliance/join" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"management_address": "<new-appliance-mgmt-ip>"}'
```


```text title="Expected output"
{
  "id": "A1234567890BCDEF",
  "name": "powerstore-node-03",
  "management_address": "192.168.1.45",
  "data_address": "192.168.2.45",
  "status": "Joining",
  "cluster_id": "cluster-prod-001",
  "join_progress": 45,
  "estimated_time_remaining": "8 minutes"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification, or import the appliance's CA certificate into your trust store.
    **`{"error": "Invalid or expired token", "error_code": 401}`** — Regenerate a valid DELL-EMC-TOKEN via PowerStore Manager or ensure the token has not expired.
    **`{"error": "Appliance already part of cluster", "error_code": 409}`** — Verify the management IP is correct and the appliance has not already been joined to this or another cluster.
After joining, the new appliance appears in the cluster and its capacity is immediately available. Existing volumes can be migrated to the new appliance non-disruptively via the Data Migration feature in PowerStore Manager.

### Decommissioning an Appliance

Before decommissioning:

1. Migrate all volumes off the appliance being removed (PowerStore Manager → Storage → Migrate)
2. Confirm no volumes or NAS servers remain on the appliance
3. Remove the appliance from the cluster via PowerStore Manager → Settings → Appliances → Remove
4. Wipe the appliance before physical disposal (Dell provides a Secure Erase option under Settings → Security → Secure Erase)

### Drive Replacement

PowerStore drives are hot-swappable. When a drive failure alert fires:

1. Confirm the failed drive slot in PowerStore Manager → Hardware → Drives
2. Engage Dell Support for a replacement drive if under ProSupport
3. Remove the failed drive (the drive slot LED will be lit amber to identify it)
4. Insert the replacement drive; reconstruction begins automatically
5. Monitor reconstruction progress in PowerStore Manager → Hardware → Drives (state will show `reconstructing` then return to `healthy`)

Reconstruction time: approximately 1 hour per TB under moderate workload. During reconstruction, the pool remains operational but with reduced fault tolerance.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powerstore — Procedures](../procedures/)
- [Powerstore — Health Checks](../health-checks/)
- [Powerstore — Deploy](../../deploy/)
