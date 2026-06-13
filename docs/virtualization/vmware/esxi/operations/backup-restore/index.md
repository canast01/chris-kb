---
tags:
  - esxi
  - operations
  - vmware
  - vsphere-8
---
# ESXi Backup & Restore


<div class="kb-summary">
ESXi Backup & Restore reference covering VM-Level Backup.

*Applies to: vSphere 7.x / 8.x*
</div>

ESXi Backup & Restore Flow
```text
┌────────────────────────────────────── ESXi — Backup and Restore ──────────────────────────────────────┐
│                                                                                                       │
│  configBundle backup, Host Profiles, and full reinstall restore procedure.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Config Backup (configBundle)         │  │             Host Profile Backup             │   │
│   │          vim-cmd hostsvc/firmware/           │  │         Export profile from vCenter         │   │
│   │         sync_config → backup_config          │  │           Includes NIC/storage/dns          │   │
│   │          Exports .tgz configBundle           │  │          Attach to host compliance          │   │
│   │           Schedule via cron/script           │  │          vLCM image backup included         │   │
│   │           Store off-host (NFS/NAS)           │  │          Compare with desired state         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Backup configBundle → store safely → restore via firmware/restore_config.                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Restore Procedure               │  │              Verification Steps             │   │
│   │         Reinstall ESXi same version          │  │            Check vmk0 IP restored           │   │
│   │         Upload configBundle to host          │  │          Verify vCenter reconnects          │   │
│   │           firmware/restore_config            │  │            Check datastore mounts           │   │
│   │           Reboot → rejoin cluster            │  │             Validate VM power-on            │   │
│   │          Apply Host Profile if used          │  │           Confirm HA agent running          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 host, local boot media (SD/M.2), management network, NAS backup store                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  configBundle = .tgz ESXi host config archive; firmware/backup_config cmd                             │
│  vim-cmd     = ESXi CLI tool for host service and management tasks                                    │
│  Host Profile = vCenter policy capturing desired ESXi configuration state                             │
│  vLCM        = vSphere Lifecycle Mgr; manages ESXi image and firmware                                 │
│  restore_config = vim-cmd call to apply a previously saved configBundle                               │
│  HA agent    = fdm process on ESXi; communicates with vCenter HA master                               │
│  sync_config = vim-cmd call to flush pending config before backup                                     │
│  NAS         = Network Attached Storage; stores configBundle files                                    │
│  Desired state = Host Profile compliance target; re-applied after restore                             │
│  DCUI        = Direct Console UI; local console for host configuration                                │
│  fdm         = Fault Domain Manager; ESXi HA agent process                                            │
│  Cluster     = group of ESXi hosts sharing HA, DRS, and vSAN resources                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
The configuration bundle includes network settings, storage policies, service state, and advanced settings. It does not include VMFS datastores or VM data.

## VM-Level Backup

VM backup is handled by the backup solution (e.g., Veeam Backup & Replication) using VMware VADP. See the [integration page](../../architecture/integrations/index.md) for transport mode details.

Key requirements:
- Changed Block Tracking (CBT) enabled on VMs
- Snapshot quiescing configured for consistent backups of databases
- Backup proxy with sufficient throughput for the backup window
