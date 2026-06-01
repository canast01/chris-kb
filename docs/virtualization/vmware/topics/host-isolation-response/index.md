
# Host Isolation Response


<div class="kb-summary">
vSphere HA host isolation response determines what happens to VMs on a host that loses all management network connectivity but may still be running.
</div>
```text
┌──────────────────────────────────── Virtualization Vmware Topics ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Vmware: Virtualization Vmware Topics platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                  Management: Virtualization Vmware Topics management console                  │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Topics infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Topics platform overview and core concepts              │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Isolation Response Options

| Setting | Behaviour | When to Use |
|---|---|---|
| Leave Powered On (default) | VMs keep running on the isolated host | Shared storage; HA can restart on another host if datastore heartbeat confirms isolation |
| Power Off | VMs are immediately powered off; HA restarts on other hosts | When guest OS can tolerate abrupt power-off; fastest VM restart |
| Shut Down | VMware Tools sends a graceful shutdown; HA restarts on other hosts | Guest-OS-sensitive workloads; slower than power-off |
| Disabled | No action taken; VMs stay running indefinitely | Not recommended — risk of split-brain |

## Recommended Configuration

**Leave Powered On** is the correct default for most environments with shared storage:

1. The isolated host checks datastore heartbeat — if VMs are still accessible, they stay running.
2. If a peer host detects the VMs are inaccessible (no datastore heartbeat from isolated host), HA restarts them.
3. Reduces unnecessary downtime from transient network glitches.

```powershell
# Check current isolation response setting
Get-Cluster | Get-View | ForEach-Object {
    [PSCustomObject]@{
        Cluster           = $_.Name
        IsolationResponse = $_.Configuration.DasConfig.DefaultVmSettings.IsolationResponse
    }
}

# Set isolation response via PowerCLI
$spec = New-Object VMware.Vim.ClusterConfigSpecEx
$spec.DasConfig = New-Object VMware.Vim.ClusterDasConfigInfo
$spec.DasConfig.DefaultVmSettings = New-Object VMware.Vim.ClusterDasVmSettings
$spec.DasConfig.DefaultVmSettings.IsolationResponse = "none"   # none = Leave Powered On
(Get-Cluster "ClusterName" | Get-View).ReconfigureComputeResource($spec, $true)
```

## Datastore Heartbeating

HA uses datastore heartbeats to distinguish true host failure from network isolation:

```powershell
# Check heartbeat datastores configured
Get-Cluster | Get-View | Select-Object -ExpandProperty Configuration |
    Select-Object -ExpandProperty DasConfig |
    Select-Object HeartbeatDatastore, HBDatastoreCandidatePolicy

# Minimum 2 heartbeat datastores recommended
# vCenter auto-selects unless overridden
```

## Split-Brain Risk

If isolation response is set to Shut Down or Power Off:

- Ensure shared storage is not accessible from the isolated host during isolation — otherwise the VM may be running on both the isolated host and the HA-restarted copy.
- Datastores with SCSI reservations or VMFS locking prevent split-brain; NFS datastores without file locking are higher risk.

## Per-VM Override

Isolation response can be overridden per VM for mixed workloads:

```powershell
# Set isolation response for a specific VM
$vm = Get-VM "db-prod-01"
$spec = New-Object VMware.Vim.VirtualMachineConfigSpec
$haOverride = New-Object VMware.Vim.ClusterDasVmConfigSpec
$haOverride.Info = New-Object VMware.Vim.ClusterDasVmConfigInfo
$haOverride.Info.Key = ($vm | Get-View).MoRef
$haOverride.Info.DasSettings = New-Object VMware.Vim.ClusterDasVmSettings
$haOverride.Info.DasSettings.IsolationResponse = "shutdown"
```

## Troubleshooting Isolation Events

```powershell
# Check HA events for isolation activity
Get-VIEvent -Types Warning,Error -MaxSamples 500 |
    Where-Object { $_.FullFormattedMessage -match "isolated\|isolation" } |
    Select-Object CreatedTime, Host, FullFormattedMessage
```

Log location on host: `/var/log/fdm.log` — search for `isolation` events with timestamps.
