# ONTAP — Standards


<div class="kb-summary">
Standards reference covering Naming Conventions, Build Baseline, Sizing Guidelines, Configuration Checklist.
</div>
```
┌──────────────────────────── NetApp ONTAP — Architecture Design Standards ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       ONTAP design standards: network isolation, redundancy, sizing, naming conventions       │   │
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
│   │           Cluster           │  │        HA node pairs        │  │          Scale-out          │   │
│   │             SVM             │  │        Virtual server       │  │       Protocol access       │   │
│   │          Aggregate          │  │         RAID groups         │  │         Storage pool        │   │
│   │           FlexVol           │  │         Thin volume         │  │        Data container       │   │
│   │          SnapMirror         │  │         Replication         │  │          Async/Sync         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       SVM        │ Tenant isolation │   All protocols   │  Kerberos/NTLM   │  Virtual server  │   │
│   │    SnapMirror    │  DR replication  │    SM protocol    │   Certificate    │  Async or sync   │   │
│   │    FlexClone     │  Instant clone   │      Internal     │    Admin role    │ Space-efficient  │   │
│   │      SM-BC       │ Zero-RPO active- │    SM protocol    │     Mediator     │     SAN only     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: AFF/FAS HA node pairs · cluster network · client access network · MetroCluster           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ONTAP              = NetApp storage OS; unified NAS, SAN, and object across AFF, FAS, ONTAP Select │
│    SVM                = Storage Virtual Machine; logical storage server with protocols, IP, and vol...│
│    Aggregate          = RAID group of disks; underpins FlexVols and FlexGroups within a node          │
│    FlexVol            = flexible thin-provisioned volume within an aggregate; most common container   │
│    FlexGroup          = scale-out volume spanning multiple aggregates; for very large NAS workloads   │
│    SnapMirror         = async or synchronous replication between ONTAP systems for DR and backup      │
│    SnapVault          = backup-oriented SnapMirror variant; independent retention at destination      │
│    FlexClone          = instant space-efficient writable clone of a volume or LUN from snapshot       │
│    Snapshot           = ONTAP space-efficient PiT copy; stored in .snapshot directory on NFS          │
│    ONTAP Mediator     = third-site quorum for SnapMirror SM-BC; prevents split-brain scenarios        │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN repl...│
│    vserver            = ONTAP CLI name for SVM; vserver show and vserver nfs show are common commands │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Naming Conventions

| Object | Pattern | Example |
|---|---|---|
| Cluster | `<site>-<platform>-cl<nn>` | `lon-affa400-cl01` |
| Node | `<cluster-name>-0<n>` | `lon-affa400-cl01-01` |
| HA pair | `<cluster-name>-hap<n>` | `lon-affa400-cl01-hap1` |
| Aggregate | `<node-short>_aggr<n>_<tier>` | `cl01n01_aggr1_ssd` |
| SVM | `<env>-<app/team>-svm` | `prod-oracle-svm`, `dev-vmware-svm` |
| Data volume | `<svm-short>_<app>_<purpose>_<nn>` | `prodoracle_db01_data_01` |
| Root volume | `<svm-name>_root` | `prod-oracle-svm_root` |
| LUN | `<host>_<app>_<type>_<nn>` | `dbhost01_oracle_data_01` |
| igroup | `<host>_<protocol>_ig` | `dbhost01_fc_ig` |
| Snapshot policy | `<frequency>-<retention>` | `daily-7`, `hourly-24` |
| SnapMirror policy | `<type>-<purpose>` | `async-dr`, `xdp-vault` |
| QoS policy group | `<tier>-<env>-qos` | `gold-prod-qos`, `silver-dev-qos` |
| Intercluster LIF | `<node-short>_ic_lif<n>` | `cl01n01_ic_lif1` |
| Data LIF | `<svm-short>_<protocol>_lif<n>` | `prodoracle_nfs_lif1` |

## Build Baseline

- ONTAP version: track the current recommended release on the [NetApp support site](https://support.netapp.com); prefer the latest 9.x GA build shown in BlueXP upgrade advisor
- All clusters must have AutoSupport configured and confirmed sending (HTTPS preferred over SMTP)
- Cluster-management LIF must have a resolvable DNS entry
- NTP configured on all nodes with at least two external NTP sources
- SNMP v3 only; no SNMP v1/v2c in production
- SSH access to cluster management only; RSA-4096 or Ed25519 keys required; password auth disabled for admin
- Volume space guarantee: `none` (thin provisioning) on all data volumes; fractional reserve set to 0%
- Autogrow enabled on all volumes with an explicit maximum no greater than 2× initial size
- Snapshot policies: default `daily-7` on data volumes; no snapshots on temp/scratch volumes
- Aggregates: RAID-DP on AFF (SSD); RAID-DP on hybrid FAS; RAID-TEC on large SATA aggregates

## Sizing Guidelines

- **Nodes per cluster**: 2–24 nodes; AFF A-series for all-flash, FAS for hybrid; ONTAP Select for software-defined deployments
- **Aggregates**: Keep usable capacity below 90% to avoid WAFL metadata overhead and Snapshot spill-over; target 70–80% for production
- **Volumes per SVM**: Supported up to several thousand per cluster; practical limit depends on workload mix and management overhead
- **HA pair fan-out**: Each HA pair supports up to 12–24 disk shelves depending on platform; consult the NetApp Hardware Universe for exact limits
- **Protocols per SVM**: An SVM can serve multiple protocols simultaneously; for security and isolation, dedicated SVMs per protocol are common in regulated environments
- **QoS**: Set throughput floors (minimum) and ceilings (maximum) per volume or workload using adaptive QoS policies to prevent noisy-neighbor issues in mixed workload clusters

## Configuration Checklist

- [ ] Cluster name, time zone, and NTP sources set
- [ ] AutoSupport enabled, HTTPS delivery tested, proxy configured if needed
- [ ] Admin account uses public-key authentication; built-in `admin` password rotated and stored in vault
- [ ] SNMPv3 trap host configured; SNMP v1/v2 disabled
- [ ] Cluster management LIF on dedicated management VLAN
- [ ] Intercluster LIFs created on each node for SnapMirror and cluster peering
- [ ] HA storage failover enabled and verified (`storage failover show`)
- [ ] Aggregates named and within 80% capacity at build
- [ ] Root SVM created; data SVMs created per application domain with appropriate protocol licenses
- [ ] Broadcast domains and failover groups match physical NIC/switch topology
- [ ] QoS adaptive policy groups created and assigned to production volumes
- [ ] EMS email notifications configured for CRITICAL and ERROR severity events
- [ ] SnapMirror relationships initialized for all protected volumes
