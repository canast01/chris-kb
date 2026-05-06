# Daily Health Check

Morning checks covering all components that can silently degrade overnight. Target: complete in under 15 minutes.

## 1. vCenter Availability

```powershell
# Connect and verify vCenter services
Connect-VIServer -Server vcenter.corp.local
Get-View -ViewType ServiceInstance | Select-Object -ExpandProperty ServerClock

# Check vCenter services from appliance shell
service-control --status --all | grep -v stopped
```

Also check: VCSA VAMI at `https://vcenter:5480` — confirm appliance health, disk usage, and certificate expiry.

## 2. Host Connectivity

```powershell
# All hosts should be Connected/PoweredOn
Get-VMHost | Select-Object Name, ConnectionState, PowerState, OverallStatus |
    Where-Object { $_.ConnectionState -ne "Connected" -or $_.PowerState -ne "PoweredOn" }

# Any result here = action required
```

## 3. Cluster HA / DRS

```powershell
# Check HA and DRS are enabled
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel

# Check active HA errors
Get-VIEvent -Types Error -MaxSamples 200 |
    Where-Object { $_.FullFormattedMessage -match "HA|DRS" } |
    Select-Object CreatedTime, FullFormattedMessage | Select-Object -First 10
```

## 4. Datastore Free Space

```powershell
# Flag datastores below 20% free
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.20 } |
    Select-Object Name,
        @{N="FreeGB"; E={ [math]::Round($_.FreeSpaceGB,1) }},
        @{N="CapGB";  E={ [math]::Round($_.CapacityGB,1) }},
        @{N="Free%";  E={ [math]::Round($_.FreeSpaceGB/$_.CapacityGB*100,1) }}
```

## 5. vSAN Health

```bash
# Run on any ESXi host in the vSAN cluster
esxcli vsan health cluster list | grep -v "Green\|healthy"

# Check for resyncing objects
esxcli vsan debug object list | grep -i "Resyncing\|Degraded\|Absent" | wc -l
```

## 6. Critical VM Status

```powershell
# Check VMs with PoweredOff state (expected list should be known)
Get-VM | Where-Object { $_.PowerState -ne "PoweredOn" } |
    Select-Object Name, PowerState, Guest

# Check snapshots older than 3 days
Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-3) } |
    Select-Object VM, Name, Created, SizeGB
```

## 7. Active Alarms

```powershell
# All triggered alarms at cluster and higher scope
Get-Folder "Datacenters" | Get-View |
    Select-Object -ExpandProperty TriggeredAlarmState |
    ForEach-Object {
        [PSCustomObject]@{
            Entity = (Get-View $_.Entity).Name
            Alarm  = (Get-View $_.Alarm).Info.Name
            Status = $_.OverallStatus
            Time   = $_.Time
        }
    } | Where-Object { $_.Status -ne "green" }
```

## 8. Backup Job Status

```powershell
# Veeam — check last 24h job results
Get-VBRJob | ForEach-Object {
    $last = Get-VBRRestorePoint -Job $_ | Sort-Object CreationTime -Descending | Select-Object -First 1
    [PSCustomObject]@{ Job = $_.Name; LastResult = $_.GetLastResult(); LastRun = $_.ScheduleOptions.LatestRunLocal }
} | Where-Object { $_.LastResult -ne "Success" }
```

## 9. Identity Source / SSO

```powershell
# Verify LDAP/AD identity source is reachable
Get-SsoAuthenticationSource | Select-Object Name, Type, Enabled
# Check for recent SSO errors in vCenter events
Get-VIEvent -MaxSamples 100 | Where-Object { $_.FullFormattedMessage -match "SSO\|identity\|LDAP" } |
    Select-Object -First 5 CreatedTime, FullFormattedMessage
```

## Daily Check Summary Template

| Area | Status | Notes |
|---|---|---|
| vCenter reachable | | |
| All hosts connected | | |
| HA/DRS enabled | | |
| No datastores < 20% free | | |
| vSAN health all green | | |
| No critical VM alarms | | |
| No stale snapshots | | |
| All backup jobs succeeded | | |
| Identity source healthy | | |
