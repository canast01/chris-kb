# Azure Runbook Template

A standard structure for Azure operational runbooks. Copy this template for any planned change, maintenance window, or incident response procedure.

---

## Runbook Metadata

Fill in this section before every runbook is executed.

| Field | Value |
|---|---|
| **Runbook Title** | |
| **Owner** | |
| **Secondary Contact** | |
| **Date / Change Window** | |
| **Change Request ID** | |
| **Risk Level** | Low / Medium / High |
| **Estimated Duration** | |
| **Rollback Possible?** | Yes / No |
| **Approval Sign-off** | |

```bash
# Confirm current subscription before starting
az account show --query "{Subscription:name, ID:id}" --output table

# Confirm operator identity
az ad signed-in-user show --query "userPrincipalName" --output tsv
```

---

## Pre-Checks

Validate the environment is in the expected state before making any changes.

```bash
# Verify resource group exists
az group show --name <rg-name> --query "properties.provisioningState" --output tsv

# Check current VM power state
az vm show \
  --resource-group <rg-name> \
  --name <vm-name> \
  --show-details \
  --query "powerState" --output tsv

# Verify disk is not currently attached to another VM
az disk show \
  --resource-group <rg-name> \
  --name <disk-name> \
  --query "diskState" --output tsv

# Check resource locks that might block the operation
az lock list --resource-group <rg-name> --output table

# Take a snapshot before destructive operations
az snapshot create \
  --resource-group <rg-name> \
  --name <snapshot-name> \
  --source <disk-id>
```

Pre-check checklist:

| Check | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|
| Subscription active | Enabled | | |
| Target resource exists | Present | | |
| No conflicting resource locks | None | | |
| Snapshot/backup taken | Completed | | |
| Downstream dependencies notified | Confirmed | | |

---

## Step-by-Step Procedure

Number each step. Record the actual command run and its output.

### Step 1 — Stop the workload (if required)

```bash
az vm deallocate \
  --resource-group <rg-name> \
  --name <vm-name> \
  --no-wait

# Wait for deallocated state
az vm wait \
  --resource-group <rg-name> \
  --name <vm-name> \
  --custom "instanceView.statuses[?code=='PowerState/deallocated']"
```

### Step 2 — Apply the change

```bash
# Example: resize a VM
az vm resize \
  --resource-group <rg-name> \
  --name <vm-name> \
  --size Standard_D4s_v3

# Example: update a tag
az resource update \
  --ids <resource-id> \
  --set tags.env=prod

# Example: attach a new managed disk
az vm disk attach \
  --resource-group <rg-name> \
  --vm-name <vm-name> \
  --name <disk-name>
```

### Step 3 — Restart and verify

```bash
az vm start \
  --resource-group <rg-name> \
  --name <vm-name>

az vm show \
  --resource-group <rg-name> \
  --name <vm-name> \
  --show-details \
  --query "powerState" --output tsv
```

---

## Rollback Procedure

Document the exact reversal steps. If rollback is not possible, state the reason.

```bash
# Example: revert VM size
az vm resize \
  --resource-group <rg-name> \
  --name <vm-name> \
  --size Standard_D2s_v3

# Example: restore disk from snapshot
az disk create \
  --resource-group <rg-name> \
  --name <restored-disk-name> \
  --source <snapshot-id>

# Example: delete a newly created resource
az resource delete --ids <resource-id> --yes
```

Rollback decision criteria:

| Condition | Action |
|---|---|
| VM fails to start after resize | Revert to original SKU |
| Application health check fails | Restore from snapshot |
| Performance degradation > 20% | Rollback and escalate |
| Change window exceeded | Stop, rollback, reschedule |

---

## Validation

Run these checks after the procedure to confirm success.

```bash
# Confirm new VM size
az vm show \
  --resource-group <rg-name> \
  --name <vm-name> \
  --query "hardwareProfile.vmSize" --output tsv

# Confirm VM is running
az vm get-instance-view \
  --resource-group <rg-name> \
  --name <vm-name> \
  --query "instanceView.statuses[1].displayStatus" --output tsv

# Check activity log for errors in the last hour
az monitor activity-log list \
  --resource-group <rg-name> \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --query "[?level=='Error'].{Time:eventTimestamp, Op:operationName.value, Status:status.value}" \
  --output table
```

---

## Sign-Off Checklist

| Item | Confirmed By | Time |
|---|---|---|
| Change applied successfully | | |
| Validation checks passed | | |
| Monitoring confirms no alerts | | |
| Snapshot/backup cleaned up (if temp) | | |
| Change request closed | | |
| Stakeholders notified | | |
