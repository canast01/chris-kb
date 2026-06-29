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
![Superna Eyeglass — CLI Reference](../../../../assets/storage-netapp-superna-eyeglass-operations-cli-reference.svg)

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
