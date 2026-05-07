# Post-Upgrade Validation

Complete all items after every upgrade (vCenter, ESXi, vSAN, NSX, VxRail). Document evidence for the change record.

```mermaid
flowchart LR
    Post_Upgrade_Validat["Post-Upgrade Validatio"]
    Post_Upgrade_Validat --> S0["Immediate Validation (within 15 minutes of upgrade completion)"]
    Post_Upgrade_Validat --> S1["vCenter Health"]
    Post_Upgrade_Validat --> S2["Cluster HA and DRS"]
    Post_Upgrade_Validat --> S3["vSAN Validation (if applicable)"]
    Post_Upgrade_Validat --> S4["NSX Validation (if NSX was upgraded or touched)"]
    Post_Upgrade_Validat --> S5["VxRail Validation (if applicable)"]
    Post_Upgrade_Validat --> S6["Aria Suite Validation (if LCM-managed)"]
    Post_Upgrade_Validat --> S7["Backup Validation"]
```

## Immediate Validation (within 15 minutes of upgrade completion)

```powershell
# 1. Confirm vCenter is reachable and version is correct
(Get-View ServiceInstance).Content.About.Version
(Get-View ServiceInstance).Content.About.Build

# 2. All hosts connected
Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"} | Select-Object Name, ConnectionState

# 3. No unexpected VM power state changes
Get-VM | Where-Object {$_.PowerState -ne "PoweredOn" -and $_.PowerState -ne "PoweredOff"} | Select-Object Name, PowerState
```

## vCenter Health

- [ ] Login to vCenter with SSO admin credentials: `administrator@vsphere.local`
- [ ] vCenter version shows target build number (Administration → About)
- [ ] vCenter services all running: Administration → Deployments → System Configuration → vCenter Server → Services
- [ ] Identity source connected: Administration → Single Sign On → Configuration → Identity Sources — `Connected`
- [ ] vSphere Client loads without certificate errors

## Cluster HA and DRS

```powershell
Get-Cluster | Select-Object Name, HAEnabled, HAAdmissionControlEnabled, DrsEnabled, DrsAutomationLevel
```

- [ ] HA re-enabled and showing green
- [ ] DRS re-enabled in correct automation level
- [ ] No `HA error` events on any host (check host Events tab)

## vSAN Validation (if applicable)

```bash
# On any cluster host
esxcli vsan health cluster list | grep -v Green    # Should return nothing
esxcli vsan debug resync summary                   # Should show no active resync
esxcli vsan debug object list | grep -v Healthy    # Should return nothing
```

## NSX Validation (if NSX was upgraded or touched)

```bash
# SSH to NSX Manager
get cluster status        # STABLE
get services              # All core services running
get edge-clusters         # All edge clusters healthy

# Verify edge BGP sessions
get bgp neighbor summary  # All peers Established
```

## VxRail Validation (if applicable)

```bash
# VxRail Manager
# Log in to VxRail Manager → Cluster → Health
# All nodes should show "Healthy"
# VxRail version should reflect the upgrade target
```

## Aria Suite Validation (if LCM-managed)

- [ ] Log in to LCM: all environments show green health
- [ ] Log in to Aria Operations: collection state `OK` for all adapters
- [ ] Log in to Aria Automation: service health page shows all services running

## Backup Validation

```powershell
# Check if backup jobs can still enumerate VMs (Veeam example)
# Run a "Quick Backup" on a non-critical VM to confirm backup proxy connectivity is intact
```

- [ ] Trigger a test backup of one non-critical VM — confirm it completes successfully
- [ ] Confirm monitoring agents are still collecting from all hosts

## Performance Baseline

Capture post-upgrade versions for CMDB update and future reference:

```powershell
# Capture all component versions
Get-VMHost | Select-Object Name, Version, Build | Sort-Object Name | Export-Csv -Path /tmp/host_versions_$(Get-Date -Format yyyyMMdd).csv

# vCenter version
(Get-View ServiceInstance).Content.About | Select-Object Version, Build

# NSX version (SSH to NSX Manager)
# get version
```

## Change Record Closure

- [ ] All hosts connected: confirmed
- [ ] Target build numbers verified on all components
- [ ] HA/DRS re-enabled and healthy
- [ ] vSAN health green
- [ ] NSX cluster stable
- [ ] Test backup completed successfully
- [ ] Monitoring collecting data
- [ ] Application owner sign-off received
- [ ] Snapshots removed after 48-hour validation period (schedule snapshot deletion reminder)
- [ ] Component version table updated in CMDB
