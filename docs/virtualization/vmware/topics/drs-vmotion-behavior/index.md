# DRS and vMotion Behavior


<div class="kb-summary">
DRS and vMotion Behavior reference covering DRS Modes, vMotion Requirements, EVC (Enhanced vMotion Compatibility), vMotion Validation, Common vMotion Failure Causes and 2 more sections.
</div>
```
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


## DRS Modes

| Mode | Behavior |
|---|---|
| **Manual** | DRS makes recommendations only — admin must approve each migration |
| **Partially Automated** | Initial placement is automated; migrations require approval |
| **Fully Automated** | DRS places and migrates VMs without intervention |

DRS evaluates cluster imbalance every 5 minutes. It uses a scale of 1–5 (1 = conservative, 5 = aggressive) for migration threshold.

## vMotion Requirements

| Requirement | Detail |
|---|---|
| Shared storage | VMs must live on datastores visible to both source and target host |
| Network reachability | vMotion VMkernel must be routable between hosts |
| CPU compatibility | CPUs must be in the same family, or EVC mode must be configured |
| No locked resources | VMs with USB passthrough, RDMs in physical mode, or NPIV cannot vMotion |
| VMware Tools | Must be installed and running for quiesced memory transfer |

## EVC (Enhanced vMotion Compatibility)

EVC masks CPU features to the lowest common denominator in the cluster, enabling vMotion across CPU generations.

```powershell
# Check current EVC mode on a cluster
Get-Cluster | Select-Object Name, EVCMode

# Set EVC mode (prevents incompatible VMs from powering on)
Set-Cluster -Cluster "<cluster>" -EVCMode "intel-skylake"
```

## vMotion Validation

```powershell
# Recent vMotion events
Get-VIEvent -MaxSamples 500 | Where-Object { $_.GetType().Name -eq "VmMigratedEvent" } |
    Select-Object CreatedTime, @{N="VM";E={$_.Vm.Name}}, @{N="From";E={$_.SourceHost.Name}}, @{N="To";E={$_.Host.Name}}

# DRS-initiated migrations
Get-VIEvent -MaxSamples 500 | Where-Object { $_.GetType().Name -eq "DrsVmMigratedEvent" } |
    Select-Object CreatedTime, @{N="VM";E={$_.Vm.Name}}

# Check for failed migrations
Get-VIEvent -MaxSamples 500 | Where-Object { $_.GetType().Name -match "MigrationError" } |
    Select-Object CreatedTime, FullFormattedMessage
```

## Common vMotion Failure Causes

| Cause | Symptoms | Fix |
|---|---|---|
| Network latency > 2s | Migration stalls, times out | Check vMotion VMkernel bandwidth and MTU |
| CPU incompatibility | Error: "incompatible CPU features" | Enable or lower EVC mode |
| Storage inaccessible | Error: "cannot access datastore" | Rescan adapters, check path state |
| Memory overcommit | Migration fails to reserve memory | Reduce memory balloon or add RAM to target host |
| Locked file (snapshot) | Error: "file is locked" | Consolidate snapshots before migrating |

## DRS Anti-Affinity / Affinity Rules

```powershell
# List DRS rules for a cluster
Get-DrsRule -Cluster "<cluster_name>"

# Create a must-not-run-together rule (e.g., two critical VMs)
New-DrsRule -Cluster "<cluster_name>" -Name "anti-affinity-db" `
    -KeepTogether:$false -VM (Get-VM "db01", "db02") -Enabled:$true

# Create a must-run-together rule (app + local cache VM)
New-DrsRule -Cluster "<cluster_name>" -Name "affinity-appdb" `
    -KeepTogether:$true -VM (Get-VM "app01", "cache01") -Enabled:$true
```

## Storage vMotion

```powershell
# Migrate a VM's disks to a different datastore (no downtime)
Move-VM -VM "<vm_name>" -Datastore (Get-Datastore "<target_ds>")

# Relocate VM files and disks together
Move-VM -VM "<vm_name>" -VMHost (Get-VMHost "<target_host>") -Datastore (Get-Datastore "<target_ds>")
```
