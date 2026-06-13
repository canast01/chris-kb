---
tags:
  - azure
---
# Azure Disk Snapshots


<div class="kb-summary">
Azure Disk Snapshots reference covering Overview, Snapshot Lifecycle, Creating Snapshots, Snapshot vs Full Backup Comparison, Restoring from Snapshot and 3 more sections.
</div>
```text
┌───────────────────────────────────────── Cloud Azure Storage ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Azure: Cloud Azure Storage platform                              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: Cloud Azure Storage management console                      │   │
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
│    Physical: Cloud Azure Storage infrastructure · management network · monitoring                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Storage platform overview and core concepts                       │
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


## Overview

Azure managed disk snapshots capture the full state of a managed disk at a point in time. Incremental snapshots store only changed blocks since the last snapshot, significantly reducing storage costs and copy time. Snapshots are stored as page blobs in Azure Storage and can be used to restore disks or copy across regions.

## Snapshot Lifecycle

```mermaid
flowchart LR
    sourceDisk["Source Managed Disk\n(OS or data disk)"]
    snapshot["Snapshot\npoint-in-time · incremental"]
    subgraph uses["Snapshot Uses"]
        restoreDisk["Restore to same disk\ndisk reset"]
        newDisk["Create new disk\nfrom snapshot"]
        crossRegion["Copy to another region\ndisaster recovery"]
        exportVHD["Export as VHD\nfor migration"]
    end

    sourceDisk -->|"az snapshot create"| snapshot
    snapshot --> restoreDisk & newDisk & crossRegion & exportVHD
```

## Creating Snapshots

```bash
# Full snapshot of a managed disk
az snapshot create \
  --resource-group rg-compute-prod \
  --name "snap-vm01-osdisk-20260507" \
  --source "/subscriptions/<sub-id>/resourceGroups/rg-compute-prod/providers/Microsoft.Compute/disks/vm01-osdisk" \
  --sku Standard_LRS \
  --location eastus

# Incremental snapshot (recommended — much lower cost)
az snapshot create \
  --resource-group rg-compute-prod \
  --name "snap-vm01-osdisk-20260507-incr" \
  --source "/subscriptions/<sub-id>/resourceGroups/rg-compute-prod/providers/Microsoft.Compute/disks/vm01-osdisk" \
  --incremental true \
  --sku Standard_LRS

# List all snapshots in a resource group
az snapshot list \
  --resource-group rg-compute-prod \
  --output table

# Show snapshot details including size and incremental chain
az snapshot show \
  --resource-group rg-compute-prod \
  --name "snap-vm01-osdisk-20260507-incr"
```

## Snapshot vs Full Backup Comparison

| Property | Full Snapshot | Incremental Snapshot |
|---|---|---|
| First snapshot size | Full disk size | Full disk size |
| Subsequent sizes | Full disk size again | Changed blocks only |
| Copy speed | Slower (full copy) | Faster (delta only) |
| Storage cost | Higher | Lower |
| Restore capability | From single object | Requires snapshot chain |
| Cross-region copy | Supported | Supported |

## Restoring from Snapshot

```bash
# Create a new managed disk from a snapshot
az disk create \
  --resource-group rg-compute-prod \
  --name "vm01-osdisk-restored" \
  --source "/subscriptions/<sub-id>/resourceGroups/rg-compute-prod/providers/Microsoft.Compute/snapshots/snap-vm01-osdisk-20260507" \
  --sku Premium_LRS \
  --location eastus

# Swap the OS disk of a stopped VM to the restored disk
az vm stop --resource-group rg-compute-prod --name vm01
az vm update \
  --resource-group rg-compute-prod \
  --name vm01 \
  --os-disk "/subscriptions/<sub-id>/resourceGroups/rg-compute-prod/providers/Microsoft.Compute/disks/vm01-osdisk-restored"
az vm start --resource-group rg-compute-prod --name vm01
```

## Cross-Region Snapshot Copy

```bash
# Copy a snapshot to another region
az snapshot create \
  --resource-group rg-compute-dr \
  --name "snap-vm01-osdisk-20260507-westus" \
  --source "/subscriptions/<sub-id>/resourceGroups/rg-compute-prod/providers/Microsoft.Compute/snapshots/snap-vm01-osdisk-20260507" \
  --location westus2 \
  --sku Standard_LRS \
  --copy-start true

# Check copy status
az snapshot show \
  --resource-group rg-compute-dr \
  --name "snap-vm01-osdisk-20260507-westus" \
  --query "completionPercent"
```

## Snapshot Retention and Cleanup

```bash
# List snapshots older than 30 days
az snapshot list \
  --resource-group rg-compute-prod \
  --query "[?timeCreated < '$(date -u -d '30 days ago' +%Y-%m-%dT%H:%MZ)'].{name:name, created:timeCreated, size:diskSizeGB}" \
  --output table

# Delete a specific snapshot
az snapshot delete \
  --resource-group rg-compute-prod \
  --name "snap-vm01-osdisk-20260407"

# Delete multiple old snapshots matching a pattern
for snap in $(az snapshot list \
  --resource-group rg-compute-prod \
  --query "[?timeCreated < '2026-04-01T00:00Z'].name" \
  --output tsv); do
  echo "Deleting $snap"
  az snapshot delete --resource-group rg-compute-prod --name "$snap" --yes
done
```

## Snapshot Costs

```bash
# Get snapshot storage used (bytes)
az snapshot show \
  --resource-group rg-compute-prod \
  --name "snap-vm01-osdisk-20260507-incr" \
  --query "{name:name, diskSize:diskSizeGB, incrementalSizeGB:incrementalSnapshotFamilyId}" \
  --output json
```

Snapshot storage pricing reference:

| SKU | Price Tier | Notes |
|---|---|---|
| Standard_LRS | Low | Locally redundant; suitable for backups |
| Standard_ZRS | Medium | Zone-redundant; higher availability |
| Premium_LRS | Higher | Required if source disk is Premium |
