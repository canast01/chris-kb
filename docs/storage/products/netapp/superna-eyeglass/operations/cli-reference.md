---
tags:
  - netapp
  - operations
---
# Superna Eyeglass — CLI Reference

<div class="kb-summary">
Eyeglass provides the `igls` CLI accessible from the appliance shell via SSH and a REST API for automation. OneFS SyncIQ CLI commands are used alongside Eyeglass operations to verify the underlying replication state. SSH to the Eyeglass appliance as the `admin` user.

*Applies to: Superna Eyeglass*
</div>
![Superna Eyeglass — CLI Reference](../../../../../assets/storage-netapp-superna-eyeglass-operations-cli-reference.svg)

```d2
direction: right

operator: "Operator /\nAutomation" {shape: rectangle}
ssh: "SSH\nadmin@eyeglass-ip" {shape: rectangle}
iglsCLI: "igls CLI\n(Eyeglass appliance" {shape: rectangle}
eyeglassSvc: "Eyeglass Services\nDR orchestration" {shape: rectangle}
restAPI: "REST API\nhttps://eyeglass-ip/eca/api/v1" {shape: rectangle}
psApi: "PowerScale\nOneFS REST API" {shape: rectangle}
synciq: "SyncIQ\nReplication engine" {shape: rectangle}

operator -> ssh
ssh -> iglsCLI
iglsCLI -> eyeglassSvc
operator -> restAPI
restAPI -> eyeglassSvc
eyeglassSvc -> psApi
psApi -> synciq
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

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


```text title="Expected output"
# igls failback list
Job Name                    Status      Last Run            Progress
dr-vault-sync-prod          completed   2024-01-15 14:32    100%
nfs-export-failback-01      idle        2024-01-10 09:15    —
san-lun-recovery-02         completed   2024-01-14 22:48    100%
cifs-share-restore-03       failed      2024-01-13 18:22    45%
iscsi-target-failback-04    idle        2024-01-12 11:05    —

# igls failback run --job dr-vault-sync-prod
Failback job 'dr-vault-sync-prod' started successfully
Job ID: fb-2024-01-15-847392
Estimated duration: 2 hours 15 minutes

# igls failback status --job dr-vault-sync-prod
Job ID:           fb-2024-01-15-847392
Job Name:         dr-vault-sync-prod
Status:           in_progress
Progress:         67%
Elapsed Time:     1 hour 32 minutes
Estimated Time:   45 minutes remaining
Data Transferred: 847.3 GB / 1.2 TB
```

!!! warning "Common errors"
    **`Error: Job '<job_name>' not found in failback queue`** — Verify the exact job name using `igls failback list` and ensure it exists before running.
    **`Error: Cannot start failback job - job already in progress`** — Wait for the current failback to complete or use `igls failback cancel --job <job_name>` to stop it first.
    **`Error: Authentication failed - invalid credentials`** — Ensure you are logged into the Eyeglass appliance with `igls login` and have appropriate failback permissions.
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


```text title="Expected output"
ID                                     Name                  Enabled  Target
b4a7c2f1-8e9d-4a2b-9f1c-3d5e6a7b8c9d   prod-to-dr-daily     true     192.168.50.42
a1f3e5d7-9c2b-4f6a-8e1d-2c3b4a5d6e7f   weekly-backup-sync   true     10.20.30.105
c8d2e4f6-1a3b-5c7d-9e0f-2a4b6c8d0e1f   archive-monthly      false    172.16.100.88

Policy: prod-to-dr-daily
  Target: 192.168.50.42
  Enabled: true
  Last Run: 2024-01-15T03:45:22Z
  Status: Completed
  Next Run: 2024-01-16T03:00:00Z

ID                          Policy Name           Status      Start Time              Duration
sync-rpt-20240115-034522    prod-to-dr-daily      Completed   2024-01-15T03:45:22Z   2h 14m
sync-rpt-20240114-030015    prod-to-dr-daily      Completed   2024-01-14T03:00:15Z   2h 8m
sync-rpt-20240113-025847    weekly-backup-sync    Completed   2024-01-13T02:58:47Z   45m

Starting SyncIQ policy: prod-to-dr-daily
Policy started successfully. Job ID: sync-job-20240115-142356

SyncIQ Service Status
  Service Enabled: true
  Service Running: true
  Max Concurrent Jobs: 4
  Current Active Jobs: 1
```

!!! warning "Common errors"
    **`Error: policy '<policy_name>' not found`** — Verify the policy name with `isi sync policies list` and use the exact ID or name from the output.
    **`Error: target cluster unreachable (192.168.x.x)`** — Confirm network connectivity to the target cluster and verify the target IP address is correct in the policy configuration.
    **`Error: SyncIQ service is not running`** — Start the SyncIQ service with `isi sync settings modify --service-enabled=true` and verify with `isi sync settings view`.
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


```text title="Expected output"
{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwOTMxNDU2MCwiZXhwIjoxNzA5MzE4MTYwfQ.k7mN9pQrXyZ2vL4wJhFgHbKcDmNoPqRsT5uVwXyZ1aA","expires_in":3600}
[
  {"id":"sync-job-001","name":"prod-to-dr-daily","status":"completed","last_run":"2024-03-01T14:32:00Z","next_run":"2024-03-02T14:00:00Z"},
  {"id":"sync-job-002","name":"backup-mirror","status":"running","progress":67,"last_run":"2024-03-01T10:15:00Z"},
  {"id":"sync-job-003","name":"archive-sync","status":"failed","error":"Connection timeout","last_run":"2024-03-01T08:00:00Z"}
]
[
  {"id":"failover-job-001","name":"prod-cluster-failover","status":"ready","last_tested":"2024-02-28T09:30:00Z","rpo_minutes":15},
  {"id":"failover-job-002","name":"secondary-failover","status":"ready","last_tested":"2024-02-25T16:45:00Z","rpo_minutes":30}
]
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or install the Eyeglass CA certificate in your system trust store.
    **`{"error":"Invalid token","code":401}`** — Ensure the Bearer token from the login response is current and correctly formatted in the Authorization header.
    **`curl: (7) Failed to connect to <eyeglass_ip> port 443: Connection refused`** — Verify the Eyeglass IP address is correct, the service is running, and port 443 is accessible from your network.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Superna Eyeglass — Procedures](../procedures/)
- [Superna Eyeglass — Scripts](../scripts/)
- [Superna Eyeglass — Health Checks](../health-checks/)
