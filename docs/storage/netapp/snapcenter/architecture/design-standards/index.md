# SnapCenter — Standards


<div class="kb-summary">
> Part of the [SnapCenter Architecture](../index.md) reference.
</div>
```
┌────────────────────────── NetApp SnapCenter — Architecture Design Standards ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     SnapCenter design standards: network isolation, redundancy, sizing, naming conventions    │   │
│   │          Network: dedicated storage VLAN; jumbo frames for iSCSI; dual-fabric for FC          │   │
│   │          Redundancy: dual controllers, multipath I/O, and no single points of failure         │   │
│   │       Monitoring: set capacity and latency alerts; baseline performance after deployment      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Requirements → architecture design → redundancy review → size → deploy                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │          Windows VM         │  │       Central control       │   │
│   │           Plug-in           │  │          Host agent         │  │        App-consistent       │   │
│   │            Policy           │  │       Schedule/retain       │  │         Backup rule         │   │
│   │        Resource group       │  │       Grouped targets       │  │        Shared policy        │   │
│   │           Recovery          │  │       Volume/LUN/file       │  │       Granular restore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   SQL plug-in    │  MSSQL backups   │       HTTPS       │   Windows auth   │  App-consistent  │   │
│   │  Oracle plug-in  │  Oracle backups  │       HTTPS       │       SSH        │ RMAN integratio  │   │
│   │  VMware plug-in  │  VM/VMDK backup  │   HTTPS/vCenter   │   vCenter SSO    │   vSphere API    │   │
│   │ SAP HANA plug-in │   HANA backups   │       HTTPS       │     SAP auth     │   Backint API    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapCenter         = NetApp backup orchestration; coordinates app-consistent snapshots via plug-ins│
│    Plug-in            = host-side agent; quiesces application before snapshot: SQL, Oracle, VMware    │
│    Resource group     = set of resources sharing a backup policy and schedule in SnapCenter           │
│    Policy             = SnapCenter object defining snapshot frequency, retention, and replication t...│
│    App-consistent     = snapshot taken after DB quiesce; guarantees crash-consistent recovery         │
│    Clone lifecycle    = SnapCenter clone: create from snapshot, provision to host, then delete        │
│    FlexClone          = underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone      │
│    Vault policy       = SnapCenter policy that also replicates snapshots to SnapVault destination     │
│    Mirror policy      = SnapCenter policy that replicates snapshots via SnapMirror to DR cluster      │
│    RBAC               = SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles  │
│    SMF                = SnapCenter MySQL database storing job history, policies, and resource configs │
│    SnapCenter API     = REST API on port 8143; full feature coverage for automation workflows         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Naming Conventions

| Object | Pattern | Example |
|---|---|---|
| Backup policy | `<app>-<frequency>-<retention>` | `oracle-daily-14`, `sql-hourly-48`, `vm-weekly-8` |
| SnapVault policy | `<app>-vault-<retention-days>` | `oracle-vault-365`, `sql-vault-90` |
| Resource group | `<env>-<app>-<tier>-rg` | `prod-oracle-primary-rg`, `prod-sql-dr-rg` |
| Backup job name | `<resource-group>_<timestamp>` | Auto-generated by SnapCenter; do not override |
| Clone name | `<source-resource>_clone_<date>` | `prod-oracle-primary_clone_20250501` |
| Plugin host entry | FQDN (not short hostname) | `dbhost01.corp.domain.com` |
| ONTAP storage connection | `<cluster-name>` | `lon-affa400-cl01` |
| SnapCenter RBAC role | `<scope>-<permission-level>` | `oracle-restore-operator`, `sql-backup-viewer` |
| Pre/post script | `<action>-<app>-<stage>.ps1` / `.sh` | `quiesce-oracle-pre.sh`, `unquiesce-oracle-post.sh` |

## Build Baseline

- SnapCenter Server runs on Windows Server 2019 or 2022; .NET Framework 4.8+ required
- MySQL repository on the same host for small deployments; dedicated MySQL HA cluster for environments >100 hosts
- TLS 1.2 minimum for all connections; configure in IIS and SnapCenter global settings
- SMTP notifications enabled for all resource groups — at minimum, alert on job failure
- All plugin hosts registered using FQDN; DNS must resolve from the SnapCenter Server
- Pre/post quiesce scripts stored in a central managed path (`C:\Program Files\NetApp\SnapCenter\scripts\` on Windows, `/opt/netapp/snapcenter/spl/scripts/` on Linux)
- Scripts must return exit code 0 for success; any non-zero exit code aborts the backup job
- SnapCenter Server and all plugins must run the same major.minor version — mixed versions cause API errors
- Service account used by SnapCenter to connect to ONTAP must use `vsadmin` role at minimum (prefer a custom least-privilege role for production)

## Configuration Checklist

- [ ] SnapCenter Server installed on dedicated Windows Server VM (not shared with other applications)
- [ ] MySQL repository backup job configured and tested
- [ ] SMTP notification configured; test email delivered
- [ ] TLS 1.2 enforced in IIS bindings and SnapCenter global settings
- [ ] ONTAP storage systems registered with service account credentials (not personal admin accounts)
- [ ] SnapCenter agent deployed on all protected hosts; plugin status shows "Available"
- [ ] Backup policies created for each retention tier (daily, weekly, monthly; SnapVault where required)
- [ ] Resource groups created, policies attached, and schedules enabled
- [ ] RBAC roles defined; application owners granted restore/clone access; no blanket admin grants
- [ ] Pre/post quiesce scripts tested manually on each application type before attaching to resource groups
- [ ] Manual backup job run on each resource group; verified in Jobs → Monitor
- [ ] Restore test executed and documented (at least one full restore + one granular restore per application type)
- [ ] SnapCenter Plug-in for VMware OVA registered in vCenter if VMware workloads are protected
