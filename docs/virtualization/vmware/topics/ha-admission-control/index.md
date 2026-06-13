---
tags:
  - vmware
---
# HA Admission Control


<div class="kb-summary">
HA Admission Control reference covering Purpose, Admission Control Policies, Checking Admission Control Status, Configure Admission Control, Admission Control and Overcommit and 3 more sections.

*Applies to: vSphere 7.x / 8.x*
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


## Purpose

Admission control reserves cluster capacity so that in the event of a host failure, vSphere HA can restart all VMs from the failed host on remaining hosts. Without it, a cluster at 100% utilisation cannot restart failed VMs.

## Admission Control Policies

| Policy | How It Works | Best For |
|---|---|---|
| **Host failures tolerated** | Reserves capacity equivalent to N hosts worth of CPU and memory | Homogeneous clusters |
| **Cluster resource percentage** | Reserves X% of total cluster CPU and memory | Heterogeneous clusters |
| **Dedicated failover hosts** | Designated hosts sit idle, used only for failover | Compliance environments requiring dedicated DR capacity |

## Checking Admission Control Status

```powershell
# HA configuration including admission control policy
Get-Cluster | Select-Object Name, HAEnabled,
    @{N="FailoverLevel";E={$_.ExtensionData.Configuration.DasConfig.AdmissionControlPolicy.FailoverLevel}},
    @{N="AdmissionControlEnabled";E={$_.ExtensionData.Configuration.DasConfig.AdmissionControlEnabled}}

# Cluster current failover capacity
Get-Cluster | ForEach-Object {
    $view = $_.ExtensionData
    [PSCustomObject]@{
        Cluster     = $_.Name
        FailoverCPU = $view.Summary.AdmissionControlInfo.CurrentFailoverResourcesUsed.Cpu
        FailoverMem = $view.Summary.AdmissionControlInfo.CurrentFailoverResourcesUsed.Memory
    }
}
```

## Configure Admission Control

```powershell
# Set to tolerate 1 host failure (percentage policy)
Set-Cluster -Cluster "<cluster_name>" -HAAdmissionControlEnabled:$true -HAFailoverLevel 1

# Disable admission control (not recommended for production)
Set-Cluster -Cluster "<cluster_name>" -HAAdmissionControlEnabled:$false
```

## Admission Control and Overcommit

Admission control uses *reservation* values where set, or a default 32 MHz / 0 MB where no reservations exist. VMs with large reservations can cause admission control to block VM power-ons even when physical resources are available.

```powershell
# Find VMs with CPU reservations
Get-VM | Where-Object { $_.VMResourceConfiguration.CpuReservationMhz -gt 0 } |
    Select-Object Name, @{N="CpuResMHz";E={$_.VMResourceConfiguration.CpuReservationMhz}}

# Find VMs with memory reservations
Get-VM | Where-Object { $_.VMResourceConfiguration.MemReservationMB -gt 0 } |
    Select-Object Name, @{N="MemResMB";E={$_.VMResourceConfiguration.MemReservationMB}}
```

## Risk Indicators

| Warning | Meaning |
|---|---|
| "Insufficient failover resources" | Cluster is too full — HA cannot guarantee restarts |
| Admission control disabled | Any host failure may leave VMs unrecoverable |
| All hosts at DRS imbalance level 4–5 | Pre-failure utilisation too high |
| Host in maintenance with no headroom | Remaining hosts cannot absorb a second failure |

## HA Heartbeat Datastores

HA uses datastore heartbeats to distinguish host isolation from host failure (avoiding false restarts).

```powershell
# Heartbeat datastores configured on a cluster
$cluster = Get-Cluster "<cluster_name>"
$cluster.ExtensionData.Configuration.DasConfig.HeartbeatDatastore
```

Ensure at least 2 heartbeat datastores are configured — ideally on different storage arrays.

## Operational Checklist

- [ ] Admission control enabled and policy matches cluster design
- [ ] Failover capacity available (no "Insufficient failover resources" warning)
- [ ] HA heartbeat datastores ≥ 2
- [ ] No hosts in unexpected maintenance mode reducing capacity
- [ ] VM reservations reviewed — excessive reservations inflate required failover capacity
