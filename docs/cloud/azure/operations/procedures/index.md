---
tags:
  - azure
  - operations
---
# Azure — Procedures

<div class="kb-summary">
Day-to-day operational tasks across compute, storage, and networking.

*Applies to: Azure*
</div>

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Azure Operations Change Flow

```d2
direction: right

changeReq: "Change Request\napproved in ITSM" {shape: rectangle}
preCheck: "Pre-change Checks\nResource health · backups · snapshots" {shape: rectangle}
mainWindow: "Maintenance Window\nnotify stakeholders" {shape: rectangle}
change: "Execute Change\nCLI / Portal / IaC" {shape: rectangle}
validate: "Post-change Validation\nhealth · connectivity · metrics" {shape: rectangle}
outcome: "outcome" {shape: rectangle}
rollback: "Rollback\nrestore snapshot · redeploy" {shape: rectangle}
closeChange: "Close Change Record\ndocument outcomes" {shape: rectangle}

changeReq -> preCheck
preCheck -> mainWindow
mainWindow -> change
change -> validate
validate -> outcome
rollback -> closeChange
```

## Runbook Templates

A standard structure for Azure operational runbooks. Copy this template for any planned change, maintenance window, or incident response procedure.

---

### Runbook Metadata

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


```text title="Expected output"
Subscription    ID
--------------  ------------------------------------
Production-Sub  a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6
user.admin@company.onmicrosoft.com
```

!!! warning "Common errors"
    **`ERROR: AADSTS65001: User or admin has not consented to use the application with ID...`** — Run `az login` to re-authenticate and grant consent to the Azure CLI application.
    **`ERROR: The subscription of type 'User' is not supported...`** — Switch to a supported subscription using `az account set --subscription <subscription-id>`.
---

### Pre-Checks

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


```text title="Expected output"
Succeeded
VM deallocated
Unattached
Name                             ResourceGroup    ResourceId                                                                                                    Level
-------------------------------  ---------------  ----------------------------------------------------------------------------------------------------------  -------
prod-rg-lock                     prod-rg          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Authorization/locks/prod-rg-lock  CanNotDelete
snapshot-prod-vm-disk-20240115  prod-rg          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Compute/snapshots/snapshot-prod-vm-disk-20240115  Succeeded
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name matches exactly and exists in the current subscription with `az group list`.
    **`The resource 'Microsoft.Compute/disks/<disk-name>' under resource group '<rg-name>' was not found`** — Confirm the disk name is correct and exists in the specified resource group using `az disk list --resource-group <rg-name>`.
Pre-check checklist:

| Check | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|
| Subscription active | Enabled | | |
| Target resource exists | Present | | |
| No conflicting resource locks | None | | |
| Snapshot/backup taken | Completed | | |
| Downstream dependencies notified | Confirmed | | |

---

### Step-by-Step Procedure

Number each step. Record the actual command run and its output.

#### Step 1 — Stop the workload (if required)

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


```text title="Expected output"
(no output — command completes silently)
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg-eastus/providers/Microsoft.Compute/virtualMachines/web-server-01",
  "name": "web-server-01",
  "resourceGroup": "prod-rg-eastus",
  "instanceView": {
    "statuses": [
      {
        "code": "PowerState/deallocated",
        "level": "Info",
        "displayStatus": "VM deallocated",
        "time": "2024-01-15T14:32:18.456789Z"
      }
    ]
  }
}
```

!!! warning "Common errors"
    **`The resource group '<rg-name>' could not be found.`** — Verify the resource group name with `az group list` and ensure you are authenticated to the correct subscription.
    **`The virtual machine '<vm-name>' does not exist in the specified resource group.`** — Confirm the VM name matches exactly with `az vm list --resource-group <rg-name>` and check for typos.
    **`Operation timed out waiting for condition.`** — Increase the wait timeout or check VM status with `az vm get-instance-view --resource-group <rg-name> --name <vm-name>` to diagnose stuck deallocations.
#### Step 2 — Apply the change

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


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
  "location": "eastus",
  "name": "web-vm-01",
  "hardwareProfile": {
    "vmSize": "Standard_D4s_v3"
  },
  "provisioningState": "Succeeded"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Compute/disks/data-disk-02",
  "tags": {
    "env": "prod"
  }
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01/dataDisks/0",
  "name": "data-disk-02",
  "createOption": "Attach",
  "managedDisk": {
    "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Compute/disks/data-disk-02"
  }
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg-name>' was not found.`** — Verify the VM name and resource group name are correct using `az vm list --resource-group <rg-name>`.
    **`InvalidParameter: The VM '<vm-name>' is in a failed provisioning state and cannot be resized.`** — Deallocate the VM first with `az vm deallocate --resource-group <rg-name> --name <vm-name>`, then retry the resize.
    **`ManagedDiskAlreadyAttached: Managed disk '<disk-name>' is already attached to another VM.`** — Detach the disk from its current VM using `az vm disk detach --resource-group <rg-name> --vm-name <current-vm> --name <disk-name>` before attaching it elsewhere.
#### Step 3 — Restart and verify

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


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg-eastus/providers/Microsoft.Compute/virtualMachines/web-server-01",
  "location": "eastus",
  "name": "web-server-01",
  "powerState": "VM running",
  "provisioningState": "Succeeded",
  "resourceGroup": "prod-rg-eastus",
  "vmId": "f7e6d5c4-b3a2-1098-7654-3210fedcba98"
}
VM running
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name with `az group list` and ensure you're using the correct subscription via `az account set --subscription <id>`.
    **`ResourceNotFound`** — Confirm the VM exists in the specified resource group using `az vm list --resource-group <rg-name>`.
---

### Rollback Procedure

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


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
  "name": "web-vm-01",
  "hardwareProfile": {
    "vmSize": "Standard_D2s_v3"
  },
  "provisioningState": "Succeeded"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/prod-rg/providers/Microsoft.Compute/disks/restored-disk-prod",
  "name": "restored-disk-prod",
  "diskSizeGB": 128,
  "provisioningState": "Succeeded",
  "creationData": {
    "sourceResourceId": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/prod-rg/providers/Microsoft.Compute/snapshots/snap-20240115"
  }
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg-name>' was not found.`** — Verify the VM name and resource group name are correct with `az vm list --resource-group <rg-name>`.
    **`InvalidParameter : The value of parameter 'source' is invalid. The source resource does not exist.`** — Confirm the snapshot ID exists and is in the same region as the target resource group using `az snapshot show --ids <snapshot-id>`.
    **`AuthorizationFailed : The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Resources/resources/delete' over scope '/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/...'.`** — Ensure your Azure account has Contributor or Owner role on the resource group with `az role assignment list --resource-group <rg-name>`.
Rollback decision criteria:

| Condition | Action |
|---|---|
| VM fails to start after resize | Revert to original SKU |
| Application health check fails | Restore from snapshot |
| Performance degradation > 20% | Rollback and escalate |
| Change window exceeded | Stop, rollback, reschedule |

---

### Validation

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


```text title="Expected output"
Standard_D4s_v3
VM running
Time                             Op                                          Status
---------------------------------  ------------------------------------------  ----------
2024-01-15T14:32:18.000000+00:00  Microsoft.Compute/virtualMachines/write     Failed
2024-01-15T14:28:45.000000+00:00  Microsoft.Compute/virtualMachines/restart   Succeeded
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg-name>' was not found.`** — Verify the resource group name and VM name are correct with `az vm list --resource-group <rg-name>`.
    
    **`InvalidDateTimeFormat: The value of parameter startTime is invalid.`** — Ensure the `date` command produces UTC format; on macOS use `date -u -v-1H +%Y-%m-%dT%H:%M:%SZ` instead of the GNU `date -d` syntax.
    
    **`AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Insights/eventtypes/values/read' over scope '/subscriptions/<sub-id>/resourcegroups/<rg-name>'.`** — Grant the user or service principal the "Monitoring Reader" role on the resource group.
---

### Sign-Off Checklist

| Item | Confirmed By | Time |
|---|---|---|
| Change applied successfully | | |
| Validation checks passed | | |
| Monitoring confirms no alerts | | |
| Snapshot/backup cleaned up (if temp) | | |
| Change request closed | | |
| Stakeholders notified | | |

---

## Azure Automation

Azure Automation — runbook automation, update management, configuration management (DSC), and change tracking.

### Key Capabilities

| Capability | Description |
|---|---|
| Runbooks | PowerShell, Python, or Graphical workflows |
| Update Management | Automated OS patching across Azure and on-premises VMs |
| Change Tracking | Track software, file, registry, and service changes |
| DSC (State Config) | Desired State Configuration for VM compliance |
| Shared resources | Credentials, variables, schedules, connections, modules |

### Common Azure CLI Commands

```bash
# List automation accounts
az automation account list \
  --query '[*].{Name:name,RG:resourceGroup,Location:location,State:state}' -o table

# List runbooks
az automation runbook list -g <rg> --automation-account-name <aa-name> \
  --query '[*].{Name:name,Type:runbookType,State:state,Modified:lastModifiedTime}' -o table

# Start a runbook job
az automation job create -g <rg> --automation-account-name <aa-name> \
  --runbook-name <runbook-name> \
  --parameters '{"param1":"value1"}'

# List recent jobs for a runbook
az automation job list -g <rg> --automation-account-name <aa-name> \
  --query '[?runbook.name==`<runbook-name>`].{ID:jobId,Status:status,Start:startTime,End:endTime}' -o table

# Get job output
az automation job get-output -g <rg> --automation-account-name <aa-name> \
  --id <job-id>

# List schedules
az automation schedule list -g <rg> --automation-account-name <aa-name> \
  --query '[*].{Name:name,Enabled:isEnabled,Frequency:frequency,NextRun:nextRun}' -o table
```


```text title="Expected output"
Name                          RG                Location    State
------------------------------  ----------------  ----------  -------
prod-automation-01            prod-infra         eastus      Enabled
dev-automation-account        dev-infra          westus2     Enabled
staging-auto-acct             staging-rg         eastus2     Enabled

Name                          Type              State    Modified
------------------------------  ----------------  -------  --------------------------
Patch-VMs-Weekly              PowerShell        Published  2024-01-15T09:23:45.123456Z
Backup-Storage-Daily          PowerShell        Published  2024-01-10T14:12:30.654321Z
Health-Check-Script           Python3           Published  2024-01-08T11:05:12.987654Z

{
  "jobId": "a7f2c9e1-4b6d-47e8-9f3a-2d8c5e1b4a9f",
  "runbookName": "Patch-VMs-Weekly",
  "creationTime": "2024-01-16T10:45:22.456789Z",
  "status": "New"
}

ID                                    Status      Start                          End
------------------------------------  ----------  ---------------------------  ---------------------------
a7f2c9e1-4b6d-47e8-9f3a-2d8c5e1b4a9f  Completed   2024-01-16T08:00:00.000000Z   2024-01-16T08:12:45.123456Z
b8e3d0f2-5c7e-48f9-0g4b-3e9d6f2c5b0g  Completed   2024-01-15T08:00:00.000000Z   2024-01-15T08:11:22.654321Z
c9f4e1g3-6d8f-49g0-1h5c-4f0e7g3d6c1h  Failed      2024-01-14T08:00:00.000000Z   2024-01-14T08:03:15.987654Z

Patch-VMs-Weekly output: Successfully patched 12 VMs in prod-infra resource group. 3 VMs required restart.

Name                          Enabled    Frequency      NextRun
------------------------------  ---------  --------  --------------------------
Weekly-Patch-Schedule         True       Week      2024-01-22T08:00:00.000000Z
Daily-Backup-Schedule         True       Day       2024-01-17T02:00:00.000000Z
Monthly-Health-Check          False      Month     2024-02-01T10:00:00.000000Z
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource 'Microsoft.Automation/automationAccounts/<aa-name>' was not found.`** — Verify the automation account name and resource group name are correct and exist in your subscription.
    **`BadRequest: Invalid runbook name '<runbook-name>'. The runbook does not exist.`** — Confirm the runbook name matches exactly (case-sensitive) and is published in the automation account.
    **`AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform
### Update Management

```bash
# List VMs onboarded to Update Management
az automation software-update-configuration list -g <rg> --automation-account-name <aa-name> \
  --query '[*].{Name:name,Schedule:scheduleInfo.frequency,Included:updateConfiguration.azureVirtualMachines}' -o table

# View update assessment results
az automation software-update-configuration machine-run list \
  -g <rg> --automation-account-name <aa-name> \
  --filter "status eq 'Failed'" \
  --query '[*].{VM:targetComputerId,Status:status,Failed:softwareUpdateConfigurationName}' -o table
```


```text title="Expected output"
Name                          Schedule    Included
------------------------------  ----------  -----------------------------------------------
Patch-Tuesday-Weekly          Week        ['/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01', '/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-02']
Critical-Hotfix-Monthly       Month       ['/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/db-vm-01']
Linux-Security-Biweekly      OneTime     ['/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/app-vm-03']

VM                                                                                                                                Status    Failed
--------------------------------------------------------------------------------------------------  ------  -----
/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-04  Failed    Patch-Tuesday-Weekly
/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/db-vm-02   Failed    Critical-Hotfix-Monthly
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name with `az group list` and ensure it exists in the correct subscription.
    **`AutomationAccountNotFound`** — Confirm the automation account name is correct and exists in the specified resource group using `az automation account list -g <rg>`.
### Runbook Example — Restart Azure VM

```powershell
param(
    [string]$ResourceGroupName,
    [string]$VMName
)

# Use system-assigned managed identity (no stored credentials needed)
Connect-AzAccount -Identity

$vm = Get-AzVM -ResourceGroupName $ResourceGroupName -Name $VMName
if ($vm.PowerState -eq "VM running") {
    Restart-AzVM -ResourceGroupName $ResourceGroupName -Name $VMName
    Write-Output "Restarted VM: $VMName"
} else {
    Write-Output "VM $VMName is not in running state: $($vm.PowerState)"
}
```

### Hybrid Runbook Worker

For running runbooks against on-premises systems:
```bash
# List hybrid worker groups
az automation hybrid-runbook-worker-group list -g <rg> --automation-account-name <aa-name> \
  --query '[*].{Name:name,Type:groupType}' -o table
```


```text title="Expected output"
Name                          Type
------------------------------  ----------------
prod-worker-group-01          User
staging-worker-group-02       User
hybrid-workers-east           System
backup-automation-workers     User
dev-test-workers              User
...
```

!!! warning "Common errors"
    **`ResourceGroupNotFound : The resource group '<rg>' could not be found.`** — Verify the resource group name with `az group list` and ensure you are logged into the correct Azure subscription.
    
    **`AutomationAccountNotFound : The automation account '<aa-name>' was not found in resource group '<rg>'.`** — Confirm the automation account name exists in the specified resource group using `az automation account list -g <rg>`.
    
    **`AuthorizationFailed : The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Automation/automationAccounts/hybridRunbookWorkerGroups/read'.`** — Assign the Automation Contributor or Reader role to your user account on the automation account resource.
### Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Runbook job failing | Job output / exception | `az automation job get-output` — check error details |
| Authentication failure in runbook | Managed identity assigned? | Assign automation account managed identity a role on the target resource |
| Scheduled job not running | Schedule enabled? | Verify schedule `isEnabled=true`; check next run time |
| Update Management not scanning VM | Log Analytics agent | Verify MMA/AMA agent is healthy and workspace matches automation account |
| Hybrid Runbook Worker offline | Worker process | Restart `HybridRunbookWorkerService` on the on-premises host |

---

## Create a Virtual Machine (Azure CLI)

```bash
# Set common variables
RG=my-resource-group
LOCATION=uksouth
VM=my-vm-01

# Create the resource group if it does not exist
az group create --name $RG --location $LOCATION

# Create the VM
az vm create \
  --resource-group $RG \
  --name $VM \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --vnet-name my-vnet \
  --subnet my-subnet \
  --nsg my-nsg \
  --public-ip-sku Standard \
  --tags Env=prod Owner=ops

# Verify the VM is running
az vm show -g $RG -n $VM \
  --show-details \
  --query '{Name:name,State:powerState,IP:publicIps,PrivateIP:privateIps}' \
  -o table
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-resource-group",
  "location": "uksouth",
  "managedBy": null,
  "name": "my-resource-group",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null
}
It is recommended to use '--public-ip-sku Standard' or '--public-ip-sku Basic' to specify the sku of the public ip. Defaulting to 'Standard' sku.
{
  "fqdns": "",
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-resource-group/providers/Microsoft.Compute/virtualMachines/my-vm-01",
  "location": "uksouth",
  "macAddress": "00:0D:3A:4F:2B:8C",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.42",
  "publicIpAddress": "20.108.45.67",
  "resourceGroup": "my-resource-group",
  "zones": ""
}
Name       State      IP             PrivateIP
---------  ---------  -------------  -----------
my-vm-01   VM running 20.108.45.67   10.0.1.42
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name is correct and exists in your subscription with `az group list`.
    **`InvalidImageName`** — Use `az vm image list --publisher Canonical --offer 0001-com-ubuntu-server-jammy --all` to find the correct image URN format (e.g., `UbuntuLTS` or `Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest`).
Common `--size` options:

| Series | Use case |
|---|---|
| Standard_B2s | Dev/test, burstable |
| Standard_D2s_v3 | General purpose |
| Standard_F4s_v2 | CPU-intensive |
| Standard_E4s_v3 | Memory-intensive |

---

## Resize a Virtual Machine

```bash
RG=my-resource-group
VM=my-vm-01

# --- Step 1: Check available sizes in the VM's current region/zone ---
az vm list-vm-resize-options \
  --resource-group $RG \
  --name $VM \
  --query '[].name' -o table

# --- Step 2: Deallocate (stop + release compute) ---
az vm deallocate \
  --resource-group $RG \
  --name $VM

# Wait for deallocated state
az vm wait \
  --resource-group $RG \
  --name $VM \
  --custom "instanceView.statuses[?code=='PowerState/deallocated']"

# --- Step 3: Resize ---
az vm resize \
  --resource-group $RG \
  --name $VM \
  --size Standard_D4s_v3

# --- Step 4: Start ---
az vm start \
  --resource-group $RG \
  --name $VM

# Confirm new size
az vm show \
  --resource-group $RG \
  --name $VM \
  --query "hardwareProfile.vmSize" -o tsv
```


```text title="Expected output"
Name
------------------
Standard_B2s
Standard_B2ms
Standard_B4ms
Standard_D2s_v3
Standard_D4s_v3
Standard_D8s_v3
Standard_E2s_v3
...

Standard_D4s_v3
```

!!! warning "Common errors"
    **`The VM 'my-vm-01' with id '/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-resource-group/providers/Microsoft.Compute/virtualMachines/my-vm-01' cannot be resized because it is still in a transitional state.`** — Wait for the deallocate operation to fully complete before attempting resize, or remove the custom wait condition if the VM is already deallocated.
    
    **`Operation failed with status: 'Bad Request'. Details: Code=InvalidParameter; Message=The requested VM size 'Standard_D4s_v3' is not available in zone 'Z1' for this subscription.`** — Choose a size from the list-vm-resize-options output that is available in your region/zone, or deallocate and move the VM to a different zone.
    
    **`The resource group 'my-resource-group' could not be found.`** — Verify the resource group name with `az group list` and update the RG variable to match an existing resource group.
> If the target size is unavailable in the current cluster, Azure may move the VM to a new host during resize. Confirm the application restarts cleanly after the resize.

---

## Create and Attach a Managed Disk

```bash
RG=my-resource-group
VM=my-vm-01
DISK=data-disk-01

# Get the AZ of the target VM (disk must match)
AZ=$(az vm show -g $RG -n $VM --query 'zones[0]' -o tsv)

# Create a Premium SSD managed disk
az disk create \
  --resource-group $RG \
  --name $DISK \
  --size-gb 256 \
  --sku Premium_LRS \
  --zone $AZ \
  --tags Purpose=data Owner=ops

# Attach to the VM
az vm disk attach \
  --resource-group $RG \
  --vm-name $VM \
  --name $DISK

# --- In-guest: extend partition (SSH into the VM) ---
# List block devices
lsblk

# Partition and format the new disk (example: /dev/sdc)
sudo parted /dev/sdc --script mklabel gpt mkpart primary xfs 0% 100%
sudo mkfs.xfs /dev/sdc1

# Mount
sudo mkdir -p /data
sudo mount /dev/sdc1 /data

# Persist across reboots
echo '/dev/sdc1 /data xfs defaults,nofail 0 2' | sudo tee -a /etc/fstab

# Verify disk is visible on the VM
az vm show -g $RG -n $VM \
  --query 'storageProfile.dataDisks[].{Name:name,LUN:lun,SizeGB:diskSizeGb,SKU:managedDisk.storageAccountType}' \
  -o table
```


```text title="Expected output"
1
NAME    MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda       8:0    0   128G  0 disk
├─sda1    8:1    0   512M  0 part /boot
├─sda2    8:2    0 127.5G  0 part /
sdb       8:16   0    32G  0 disk
└─sdb1    8:17   0    32G  0 part /mnt
sdc       8:32   0   256G  0 disk
mkpart primary xfs 0% 100%
mkfs.xfs 5.13.0
meta-data=/dev/sdc1              isize=512    agcount=4, agsize=16777216 blks
data     =                       bsize=4096   blocks=67108864, imaps=4
naming   =version 2              bsize=4096   ascii-ci=0, fxattr=0
log      =internal log           bsize=4096   blocks=32768, blks
realtime =none                   extrealtime blocks=0, blks
Name         LUN    SizeGB  SKU
data-disk-01  0     256     Premium_LRS
```

!!! warning "Common errors"
    **`ERROR: (BadRequest) The zone of the managed disk 'data-disk-01' does not match the zone of the virtual machine 'my-vm-01'.`** — Ensure the disk zone matches the VM's availability zone by verifying `az vm show` returns the correct zone before disk creation.
    **`Error: No such file or directory`** — Verify the correct device name (e.g., `/dev/sdc`) by running `lsblk` after attachment, as device naming varies by VM configuration.
    **`mount: /data: unknown filesystem type 'xfs'.`** — Install XFS tools on the VM with `sudo apt-get install xfsprogs` (Ubuntu/Debian) or `sudo yum install xfsprogs` (RHEL/CentOS) before formatting.
---

## Create a Network Security Group Rule

```bash
RG=my-resource-group
NSG=my-nsg

# Inbound rule — allow HTTPS from anywhere
az network nsg rule create \
  --resource-group $RG \
  --nsg-name $NSG \
  --name Allow-HTTPS-Inbound \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 443

# Inbound rule — allow SSH from a specific IP range
az network nsg rule create \
  --resource-group $RG \
  --nsg-name $NSG \
  --name Allow-SSH-CorpNet \
  --priority 110 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes 10.0.0.0/8 \
  --destination-port-ranges 22

# Outbound rule — deny internet egress for sensitive VMs
az network nsg rule create \
  --resource-group $RG \
  --nsg-name $NSG \
  --name Deny-Internet-Outbound \
  --priority 4000 \
  --direction Outbound \
  --access Deny \
  --protocol '*' \
  --source-address-prefixes 'VirtualNetwork' \
  --destination-address-prefixes Internet \
  --destination-port-ranges '*'

# Verify current rules
az network nsg rule list \
  --resource-group $RG \
  --nsg-name $NSG \
  --query '[].{Name:name,Priority:priority,Dir:direction,Access:access,Protocol:protocol,DestPort:destinationPortRange}' \
  -o table
```


```text title="Expected output"
{
  "name": "Allow-HTTPS-Inbound",
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/my-resource-group/providers/Microsoft.Network/networkSecurityGroups/my-nsg/securityRules/Allow-HTTPS-Inbound",
  "etag": "W/\"a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d\"",
  "type": "Microsoft.Network/networkSecurityGroups/securityRules",
  "properties": {
    "provisioningState": "Succeeded",
    "protocol": "Tcp",
    "sourcePortRange": "*",
    "destinationPortRange": "443",
    "sourceAddressPrefix": "*",
    "destinationAddressPrefix": "*",
    "access": "Allow",
    "priority": 100,
    "direction": "Inbound"
  }
}
{
  "name": "Allow-SSH-CorpNet",
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/my-resource-group/providers/Microsoft.Network/networkSecurityGroups/my-nsg/securityRules/Allow-SSH-CorpNet",
  "etag": "W/\"b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e\"",
  "type": "Microsoft.Network/networkSecurityGroups/securityRules",
  "properties": {
    "provisioningState": "Succeeded",
    "protocol": "Tcp",
    "sourcePortRange": "*",
    "destinationPortRange": "22",
    "sourceAddressPrefix": "10.0.0.0/8",
    "destinationAddressPrefix": "*",
    "access": "Allow",
    "priority": 110,
    "direction": "Inbound"
  }
}
{
  "name": "Deny-Internet-Outbound",
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/my-resource-group/providers/Microsoft.Network/networkSecurityGroups/my-nsg/securityRules/Deny-Internet-Outbound",
  "etag": "W/\"c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f\"",
  "type": "Microsoft.Network/networkSecurityGroups/securityRules",
  "properties": {
    "provisioningState": "Succeeded",
    "protocol": "*",
    "sourcePortRange": "*",
    "destinationPortRange": "*",
    "sourceAddressPrefix": "VirtualNetwork",
    "destinationAddressPrefix": "Internet",
    "access": "Deny",
    "priority": 4000,
    "direction": "Outbound"
  }
}
Name                        Priority    Dir        Access    Protocol
```
Priority rules: lower number = higher priority. Range is 100–4096. Azure evaluates rules in priority order and stops at the first match.

---

## Configure Azure Backup for a VM

```bash
VAULT=my-recovery-vault
RG=my-resource-group
VM=my-vm-01
POLICY=DefaultPolicy

# Create Recovery Services vault (if not existing)
az backup vault create \
  --resource-group $RG \
  --name $VAULT \
  --location uksouth

# List available backup policies
az backup policy list \
  --resource-group $RG \
  --vault-name $VAULT \
  --query '[].name' -o table

# Enable backup protection for the VM
az backup protection enable-for-vm \
  --resource-group $RG \
  --vault-name $VAULT \
  --vm $VM \
  --policy-name $POLICY

# Verify protection status
az backup item show \
  --resource-group $RG \
  --vault-name $VAULT \
  --container-name "iaasvmcontainerv2;$RG;$VM" \
  --name "vm;iaasvmcontainerv2;$RG;$VM" \
  --backup-management-type AzureIaasVM \
  --query '{VM:properties.friendlyName,Status:properties.protectionStatus,LastBackup:properties.lastBackupTime}' \
  -o table

# Trigger an on-demand backup
az backup protection backup-now \
  --resource-group $RG \
  --vault-name $VAULT \
  --container-name "iaasvmcontainerv2;$RG;$VM" \
  --item-name "vm;iaasvmcontainerv2;$RG;$VM" \
  --backup-management-type AzureIaasVM \
  --retain-until 2025-12-31
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/my-resource-group/providers/Microsoft.RecoveryServices/vaults/my-recovery-vault",
  "location": "uksouth",
  "name": "my-recovery-vault",
  "type": "Microsoft.RecoveryServices/vaults"
}
Name
-----------
DefaultPolicy
DailyPolicy
WeeklyPolicy
MonthlyPolicy

ProtectionState    : ProtectionConfigured
ProtectionStatus   : Healthy
VM                 : my-vm-01
Status             : Protected
LastBackup         : 2025-01-15T08:32:14.000000+00:00

JobID    : a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
Status   : InProgress
Operation: Backup
StartTime: 2025-01-15T09:45:22.123456+00:00
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.RecoveryServices/vaults/my-recovery-vault' under resource group 'my-resource-group' was not found.`** — Verify the vault name and resource group name are correct, or create the vault first with `az backup vault create`.
    **`InvalidParameterValue : Policy 'DefaultPolicy' not found in vault 'my-recovery-vault'.`** — List available policies with `az backup policy list` and use an existing policy name, or create a custom policy.
    **`ResourceNotFound : The container 'iaasvmcontainerv2;my-resource-group;my-vm-01' was not found.`** — Ensure the VM is registered with the vault by running `az backup protection enable-for-vm` first, or verify the VM exists in the resource group.
---

## Set Up Azure Monitor Alert

```bash
RG=my-resource-group
VM=my-vm-01

# Get the VM resource ID
VM_ID=$(az vm show -g $RG -n $VM --query id -o tsv)

# Create an action group (email notification target)
az monitor action-group create \
  --resource-group $RG \
  --name ops-email-group \
  --short-name opsalerts \
  --action email ops-lead ops-lead@example.com

# Get action group resource ID
AG_ID=$(az monitor action-group show -g $RG -n ops-email-group --query id -o tsv)

# Create a metrics alert — CPU > 80% for 5 minutes
az monitor metrics alert create \
  --name "High-CPU-$VM" \
  --resource-group $RG \
  --scopes $VM_ID \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --description "CPU utilisation exceeded 80% for 5 minutes" \
  --action $AG_ID

# Create a metrics alert — Available Memory < 1 GB
az monitor metrics alert create \
  --name "Low-Memory-$VM" \
  --resource-group $RG \
  --scopes $VM_ID \
  --condition "avg Available Memory Bytes < 1073741824" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --action $AG_ID

# Verify alerts
az monitor metrics alert list \
  --resource-group $RG \
  --query '[].{Name:name,Severity:severity,Enabled:enabled,Condition:criteria.allOf[0].metricName}' \
  -o table
```


```text title="Expected output"
/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/my-resource-group/providers/Microsoft.Compute/virtualMachines/my-vm-01
{
  "actionGroupId": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/my-resource-group/providers/Microsoft.Insights/actionGroups/ops-email-group",
  "enabled": true,
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/my-resource-group/providers/Microsoft.Insights/metricAlerts/High-CPU-my-vm-01",
  "name": "High-CPU-my-vm-01",
  "resourceGroup": "my-resource-group"
}
{
  "actionGroupId": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/my-resource-group/providers/Microsoft.Insights/actionGroups/ops-email-group",
  "enabled": true,
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/my-resource-group/providers/Microsoft.Insights/metricAlerts/Low-Memory-my-vm-01",
  "name": "Low-Memory-my-vm-01",
  "resourceGroup": "my-resource-group"
}
Name               Severity  Enabled  Condition
-----------------  ----------  ---------  ---------------------
High-CPU-my-vm-01           2  True       Percentage CPU
Low-Memory-my-vm-01         2  True       Available Memory Bytes
```

!!! warning "Common errors"
    **`ResourceNotFound : The resource 'Microsoft.Compute/virtualMachines/my-vm-01' under resource group 'my-resource-group' was not found.`** — Verify the resource group name and VM name are correct using `az vm list -g $RG`.
    **`InvalidTemplate : The action group resource ID is invalid or the action group does not exist in the specified resource group.`** — Ensure the action group was created successfully by running `az monitor action-group list -g $RG`.
    **`BadRequest : The condition syntax is invalid. Metric name 'Percentage CPU' not found for resource type 'Microsoft.Compute/virtualMachines'.`** — Use the correct metric name by running `az monitor metrics list-definitions --resource $VM_ID` to list available metrics.
Severity levels: 0 (Critical) → 1 (Error) → 2 (Warning) → 3 (Informational) → 4 (Verbose).

---

## Create a Storage Account and Container

```bash
RG=my-resource-group
SA=mystorageacct$RANDOM   # must be globally unique, 3-24 lowercase alphanumeric
CONTAINER=app-data

# Create storage account
az storage account create \
  --resource-group $RG \
  --name $SA \
  --location uksouth \
  --kind StorageV2 \
  --sku Standard_LRS \
  --access-tier Hot \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false \
  --https-only true

# Get the storage account key
SA_KEY=$(az storage account keys list -g $RG -n $SA --query '[0].value' -o tsv)

# Create a private blob container
az storage container create \
  --name $CONTAINER \
  --account-name $SA \
  --account-key $SA_KEY \
  --public-access off

# Enable blob versioning
az storage account blob-service-properties update \
  --resource-group $RG \
  --account-name $SA \
  --enable-versioning true

# Verify
az storage account show \
  --resource-group $RG \
  --name $SA \
  --query '{Name:name,SKU:sku.name,Kind:kind,AccessTier:accessTier,HTTPS:supportsHttpsTrafficOnly}' \
  -o table

az storage container list \
  --account-name $SA \
  --account-key $SA_KEY \
  --query '[].{Name:name,LeaseState:properties.leaseState,PublicAccess:properties.publicAccess}' \
  -o table
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-resource-group/providers/Microsoft.Storage/storageAccounts/mystorageacct28471",
  "name": "mystorageacct28471",
  "type": "Microsoft.Storage/storageAccounts",
  "location": "uksouth",
  "sku": {
    "name": "Standard_LRS"
  },
  "kind": "StorageV2",
  "accessTier": "Hot",
  "supportsHttpsTrafficOnly": true,
  "minimumTlsVersion": "TLS1_2",
  "allowBlobPublicAccess": false
}
Name                      SKU            Kind       AccessTier    HTTPS
------------------------  -------------  ---------  -----------   ------
mystorageacct28471        Standard_LRS   StorageV2  Hot           True

Name        LeaseState    PublicAccess
----------  -----------   -----------
app-data    Available     None
```

!!! warning "Common errors"
    **`Storage account name 'mystorageacct28471' is already taken.`** — Increase the $RANDOM value range or use a longer unique prefix to ensure global uniqueness across Azure.
    **`The provided account key is invalid or has expired.`** — Verify the storage account exists and re-run `az storage account keys list` to fetch a fresh key before using it in subsequent commands.
    **`ResourceNotFound: The Resource 'Microsoft.Storage/storageAccounts/mystorageacct28471' under resource group 'my-resource-group' was not found.`** — Confirm the resource group name matches exactly and the storage account creation completed successfully before running verification commands.
| SKU | Replication | Use case |
|---|---|---|
| Standard_LRS | 3x within one datacenter | Dev/test, low cost |
| Standard_ZRS | 3x across availability zones | Zone-resilient |
| Standard_GRS | LRS + async copy to paired region | Regional DR |
| Premium_LRS | SSD-backed, low latency | High-throughput workloads |

---

## Configure Entra ID (Azure AD) Group and Role Assignment

```bash
RG=my-resource-group

# --- Step 1: Create a security group in Entra ID ---
az ad group create \
  --display-name "Platform-Ops-Team" \
  --mail-nickname "platform-ops-team" \
  --description "Azure platform operations team — prod subscription access"

# Get the group object ID
GROUP_ID=$(az ad group show --group "Platform-Ops-Team" --query id -o tsv)

# --- Step 2: Add members to the group ---
USER_ID=$(az ad user show --id user@example.com --query id -o tsv)
az ad group member add --group "Platform-Ops-Team" --member-id $USER_ID

# --- Step 3: Assign a built-in RBAC role at subscription scope ---
SUB_ID=$(az account show --query id -o tsv)

az role assignment create \
  --assignee-object-id $GROUP_ID \
  --assignee-principal-type Group \
  --role "Contributor" \
  --scope "/subscriptions/$SUB_ID"

# --- Step 4: Assign a role at resource group scope (more restrictive) ---
az role assignment create \
  --assignee-object-id $GROUP_ID \
  --assignee-principal-type Group \
  --role "Virtual Machine Contributor" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG"

# Verify role assignments for the group
az role assignment list \
  --assignee $GROUP_ID \
  --query '[].{Role:roleDefinitionName,Scope:scope}' \
  -o table
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
Role                              Scope
--------------------------------  ----------------------------------------------------------------
Contributor                       /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
Virtual Machine Contributor       /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/my-resource-group
```

!!! warning "Common errors"
    **`Operation failed with status: 'Bad Request'. Details: Code: Authorization_RequestDenied`** — Ensure your user account has sufficient permissions (Owner or User Access Administrator role) on the subscription to create role assignments.
    **`No object was found that matches the filter 'Platform-Ops-Team'.`** — Verify the group display name matches exactly and wait a few seconds after group creation before querying it, as there may be replication delay.
    **`The user 'user@example.com' does not exist in the directory.`** — Replace `user@example.com` with a valid user principal name (UPN) that exists in your Entra ID tenant.
Common built-in roles:

| Role | Scope of access |
|---|---|
| Owner | Full access including role assignments |
| Contributor | Full CRUD except role assignments |
| Reader | Read-only |
| Virtual Machine Contributor | Create/manage VMs, not the VNet or Storage |
| Storage Blob Data Contributor | Read/write blob data (not account management) |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Azure — Health Checks](../health-checks/)
- [Azure — CLI Reference](../cli-reference/)
- [Azure — Common Issues](../../troubleshooting/common-issues/)
