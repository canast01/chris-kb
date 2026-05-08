# ESXi Backup & Restore

## Host Maintenance Mode Process

### Pre-Checks

- Confirm cluster has sufficient capacity to absorb workload
- Confirm DRS is enabled and set to at least Partially Automated
- Check for VMs with DRS anti-affinity or must-run-on rules
- Confirm vSAN evacuation setting if vSAN is in use

### Entering Maintenance Mode

1. In vCenter, right-click the host → **Maintenance Mode** → **Enter Maintenance Mode**
2. Select evacuation option:
   - **Move powered-off and suspended VMs** (standard)
   - **Ensure accessibility** (vSAN — leaves data accessible but does not fully evacuate)
   - **Full data migration** (vSAN — migrates all data off the host)
3. Click OK and monitor the task

### Monitoring the Process

- Watch DRS task progress in Recent Tasks
- Confirm VMs are migrating to other hosts
- Check vSAN resync if full migration was selected — wait for it to complete before proceeding

### Completing Approved Work

- Perform hardware, firmware, or patching work as planned
- Do not extend beyond the approved maintenance window without notification

### Exiting Maintenance Mode

1. Right-click the host → **Maintenance Mode** → **Exit Maintenance Mode**
2. Confirm the host reconnects and shows as Connected
3. Wait for vSAN to rebalance if applicable

### Post-Maintenance Validation

- Confirm host is Connected in vCenter
- Confirm no new alerts on the host
- Confirm vSAN health is green if vSAN is used
- Confirm VMs are distributed as expected by DRS
- Confirm host hardware health in iDRAC

## ESXi Host Configuration Backup

Export the ESXi host configuration before any major change or on a regular schedule:

```bash
# Via PowerCLI — export host configuration bundle
Get-VMHostFirmware -VMHost <esxi-host> -BackupConfiguration -DestinationPath C:\backups\
```

```bash
# Via vSphere Client
# Host → Configure → System → Security Profile → Export
```

The configuration bundle includes network settings, storage policies, service state, and advanced settings. It does not include VMFS datastores or VM data.

## VM-Level Backup

VM backup is handled by the backup solution (e.g., Veeam Backup & Replication) using VMware VADP. See the [integration page](../../architecture/integrations/) for transport mode details.

Key requirements:
- Changed Block Tracking (CBT) enabled on VMs
- Snapshot quiescing configured for consistent backups of databases
- Backup proxy with sufficient throughput for the backup window
