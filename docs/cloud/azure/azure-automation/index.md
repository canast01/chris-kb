# Azure Automation

Azure Automation — runbook automation, update management, configuration management (DSC), and change tracking.

## Key Capabilities

| Capability | Description |
|---|---|
| Runbooks | PowerShell, Python, or Graphical workflows |
| Update Management | Automated OS patching across Azure and on-premises VMs |
| Change Tracking | Track software, file, registry, and service changes |
| DSC (State Config) | Desired State Configuration for VM compliance |
| Shared resources | Credentials, variables, schedules, connections, modules |

## Common Azure CLI Commands

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

## Update Management

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

## Runbook Example — Restart Azure VM

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

## Hybrid Runbook Worker

For running runbooks against on-premises systems:
```bash
# List hybrid worker groups
az automation hybrid-runbook-worker-group list -g <rg> --automation-account-name <aa-name> \
  --query '[*].{Name:name,Type:groupType}' -o table
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Runbook job failing | Job output / exception | `az automation job get-output` — check error details |
| Authentication failure in runbook | Managed identity assigned? | Assign automation account managed identity a role on the target resource |
| Scheduled job not running | Schedule enabled? | Verify schedule `isEnabled=true`; check next run time |
| Update Management not scanning VM | Log Analytics agent | Verify MMA/AMA agent is healthy and workspace matches automation account |
| Hybrid Runbook Worker offline | Worker process | Restart `HybridRunbookWorkerService` on the on-premises host |
