# Alarms & Events

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).
## Triggered Alarms

```powershell
# List all alarm definitions
Get-AlarmDefinition

# VMs with active triggered alarms
Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}

# Triggered alarms on all hosts
Get-VMHost | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}

# All triggered alarms across inventory
Get-Datacenter | ForEach-Object {
    $_.ExtensionData.TriggeredAlarmState | ForEach-Object {
        [PSCustomObject]@{
            Entity  = $_.Entity
            Alarm   = $_.Alarm
            Status  = $_.OverallStatus
            Time    = $_.Time
        }
    }
}
```

## Acknowledge and Reset Alarms

```powershell
# Acknowledge a triggered alarm on a VM
$vm = Get-VM "<vm_name>"
$alarmMgr = Get-View AlarmManager
$alarmMgr.AcknowledgeAlarm($vm.ExtensionData.TriggeredAlarmState[0].Alarm, $vm.ExtensionData.MoRef)

# Reset alarm to green (use only when alarm is false-positive)
$alarmMgr.SetAlarmStatus($vm.ExtensionData.TriggeredAlarmState[0].Alarm, $vm.ExtensionData.MoRef, "green")
```

## Events

```powershell
# Last 200 events (most recent first)
Get-VIEvent -MaxSamples 200 | Select-Object CreatedTime, UserName, FullFormattedMessage

# Events in the last 24 hours
Get-VIEvent -Start (Get-Date).AddHours(-24) | Select-Object CreatedTime, UserName, FullFormattedMessage

# Events for a specific VM
Get-VIEvent -Entity (Get-VM "<vm_name>") -MaxSamples 50 |
    Select-Object CreatedTime, FullFormattedMessage

# Filter task events — useful for change auditing
Get-VIEvent -MaxSamples 500 |
    Where-Object { $_.GetType().Name -eq "TaskEvent" } |
    Select-Object CreatedTime, UserName, FullFormattedMessage |
    Sort-Object CreatedTime -Descending

# Error events only
Get-VIEvent -MaxSamples 1000 | Where-Object { $_.GetType().Name -match "Error|Fault" } |
    Select-Object CreatedTime, FullFormattedMessage
```

## Export Events to CSV

```powershell
Get-VIEvent -Start (Get-Date).AddDays(-7) -MaxSamples 5000 |
    Select-Object CreatedTime, UserName, FullFormattedMessage |
    Export-Csv -Path vcenter_events_7d.csv -NoTypeInformation
```

## Common Event Types

| Type | Meaning |
|---|---|
| `TaskEvent` | User-initiated action (power on, migrate, etc.) |
| `VmPoweredOnEvent` | VM powered on |
| `VmMigratedEvent` | vMotion completed |
| `VmGuestRebootEvent` | Guest OS reboot |
| `DrsVmMigratedEvent` | DRS-initiated migration |
| `AlarmStatusChangedEvent` | Alarm transitioned state |
| `UserLoginSessionEvent` | User connected to vCenter |
