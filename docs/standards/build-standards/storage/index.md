# Storage Build Standards

## LUN Naming Convention

LUN names must be unique across the array and encode enough context to identify the host, application, purpose, and sequence number without consulting a spreadsheet.

Pattern: `{host}_{app}_{purpose}_{num}`

| Component | Description | Example |
|---|---|---|
| `host` | Short hostname (without env/site prefix) | `wsql01` |
| `app` | Application or workload abbreviation | `mssql` |
| `purpose` | `data`, `log`, `temp`, `os`, `backup` | `data` |
| `num` | Two-digit sequence | `01` |

Examples:

- `wsql01_mssql_data_01` — first SQL data LUN on wsql01
- `wsql01_mssql_log_01` — SQL transaction log LUN
- `wapp02_tomcat_data_01` — application data LUN on a Tomcat host

LUN names are set at array provisioning time and must not be renamed after host mapping. Renaming requires a change record and re-validation of multipath.

## Multipath Configuration

All Linux hosts connected to SAN storage must use device-mapper multipath (`multipathd`). Default policy is `service-time 0`.

```ini
# /etc/multipath.conf (key sections)
defaults {
    user_friendly_names  yes
    find_multipaths      yes
    path_grouping_policy multibus
    path_selector        "service-time 0"
    failback             immediate
    no_path_retry        fail
}

blacklist {
    devnode "^sda$"   # local OS disk — never multipath
}
```

Verify after mapping a new LUN:

```bash
multipath -ll
multipath -v3 2>&1 | grep -i "wsql01"
lsblk | grep dm-
```

Expected output: all paths `active ready`, queue depth per path as configured, DM device visible under `/dev/mapper/`.

## Filesystem Layout and Mount Points

Standard mount point layout for application servers:

| Mount Point | Purpose | Filesystem | Mount Options |
|---|---|---|---|
| `/` | OS root | xfs | defaults |
| `/boot` | Kernel/initrd | xfs | defaults |
| `/var` | Variable data | xfs | defaults,nodev |
| `/tmp` | Temporary files | xfs | defaults,nodev,nosuid,noexec |
| `/data` | Application data | xfs | defaults,nodev,nosuid |
| `/logs` | Application logs | xfs | defaults,nodev,nosuid |
| `/backup` | Local backup staging | xfs | defaults,nodev,nosuid |

SQL Server additional mounts: `/mssql/data`, `/mssql/log`, `/mssql/temp` — each on a dedicated LUN.

XFS is the standard filesystem for all data and log volumes. ext4 is acceptable for OS volumes on older builds. ZFS is not in standard use.

## Disk Labelling and fstab

All non-OS disks must be mounted by label or UUID — never by device name (`/dev/sdb`). Device names change when new disks are added.

```bash
# Set filesystem label at mkfs time
mkfs.xfs -L mssql_data_01 /dev/mapper/wsql01_mssql_data_01

# Mount by label
echo "LABEL=mssql_data_01  /mssql/data  xfs  defaults,nodev,nosuid  0 0" >> /etc/fstab

# Verify
mount -a && df -hT /mssql/data
```

For multipath devices, use the DM persistent name (`/dev/mapper/{alias}`) in fstab, not the dm-N path.

## Snapshot and Backup Standards

Array-level snapshots supplement but do not replace backup. Snapshot policy per tier:

| Tier | Snapshot Frequency | Retention | Notes |
|---|---|---|---|
| Production | Every 4 hours | 48 hours | Plus daily for 7 days |
| Staging | Daily | 3 days | — |
| Dev | None by default | — | Enable on request |

Snapshots must not be used for production data recovery without testing consistency. SQL and Oracle volumes require application-consistent snapshots using VSS (Windows) or the array's application-aware plugin.

All new storage builds must have a backup job configured and a successful test restore completed before going live.
