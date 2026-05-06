# Alarms & Events

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

---

## Alarms & Events

```powershell
# Triggered alarms
Get-AlarmDefinition
Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 }

# Events
Get-VIEvent -MaxSamples 200
Get-VIEvent -Start (Get-Date).AddHours(-24)
Get-VIEvent -Entity (Get-VM <name>) -MaxSamples 50
Get-VIEvent -MaxSamples 500 | Where-Object { $_.GetType().Name -eq "TaskEvent" } | Select-Object CreatedTime, UserName, FullFormattedMessage
```
