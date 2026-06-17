---
tags:
  - troubleshooting
  - vsan
  - vmware
  - known-issues
  - vsphere-8
---
# VMware vSAN — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known vSAN bugs, error codes, and workarounds including degraded component handling, resync issues, and health check false positives.

*Applies to: vSAN 7.x / 8.x (ESA and OSA)*
</div>

```text
┌───────────────────────────────────────────── VMware vSAN ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Software-defined storage — pooled local disks across ESXi hosts                │   │
│   │             Protocols: vSAN (internal) · iSCSI (file service/target) · NFS v3/v4.1            │   │
│   │                Management: vCenter vSAN UI · ESXCLI · RVC · vSAN Health checks                │   │
│   │             VM write -> object manager -> CLOM placement -> disk group -> replica             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Cache            │  │       Cache disk (SSD)      │  │        Per disk group       │   │
│   │           Capacity          │  │        Capacity disks       │  │          HDD or SSD         │   │
│   │           Cluster           │  │        vSAN datastore       │  │      Single per cluster     │   │
│   │           Witness           │  │      Stretched cluster      │  │     Third site tie-break    │   │
│   │            Health           │  │       vSAN Health Svc       │  │     70+ built-in checks     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    Disk group    │   Storage unit   │   vSAN internal   │       N/A        │1 cache+N capacity│   │
│   │       CLOM       │ Object placement │      Internal     │       N/A        │Honors FTT policy │   │
│   │      CLOMD       │ Placement daemon │      Internal     │       N/A        │Runs on each host │   │
│   │  Health Service  │  Cluster health  │  HTTPS (vCenter)  │      Admin       │ Proactive alarms │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: ESXi hosts with local disks (cache SSD + capacity disks) -> vSAN datastore                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FTT          = Failures to Tolerate; vSAN storage policy defining redundancy                         │
│  PFTT/SFTT    = Primary/Secondary FTT; stretched cluster tolerance levels                             │
│  Disk group   = cache SSD + capacity disks grouped on one host                                        │
│  Object       = vSAN unit of data (e.g. VM home, vmdk, swap)                                          │
│  CLOM         = Cluster Level Object Manager; decides component placement                             │
│  Resync       = vSAN rebalancing or repair after disk/host event                                      │
│  Stretched cluster = vSAN across two sites + witness for FTT=1                                        │
│  Witness      = lightweight host in third site providing quorum votes                                 │
│  vSAN ESA     = Express Storage Architecture; all-NVMe, no disk groups                                │
│  OSA          = Original Storage Architecture; cache + capacity disk group model                      │
│  Deduplication = reduces capacity by eliminating duplicate blocks per disk group                      │
│  SPBM         = Storage Policy-Based Management; per-VM vSAN policy config                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Check `esxcli vsan health cluster list` for active health alarms before assuming a known bug.
- vSAN ESA (Express Storage Architecture) and OSA (Original Storage Architecture) have separate bug tracks — note which applies.
- Run `cmmds-tool find -t DOM_OBJECT` to inspect object health directly.

## Degraded Objects and Resync

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Resync stuck at 0 bytes remaining but objects still degraded | vSAN 7.x | DOM owner reassignment race during resync | Run `esxcli vsan debug resync summary get`; restart DOM owner VM or reboot ESXi host | 7.0 U3 |
| Objects show `Absent` after host maintenance exit | vSAN 7.x / 8.x | Component rebuild delayed by 60-minute timer | Wait 60 minutes after maintenance exit; accelerate with `esxcli vsan debug resync start` | N/A |
| `Immediate resync` not triggering after disk replacement | vSAN 7.0 U1 | Disk claimed but DOM not triggering rebuild | Restart `vsanmgmtd` on owning host | 7.0 U2 |

## Health Check False Positives

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `vSAN Build Recommendation` health alarm after upgrade | vSAN 7.x / 8.x | CEIP / Cloud Health comparison uses stale build database | Disable or acknowledge; update CEIP opt-in to refresh | N/A |
| `Controller firmware` health check fails on qualified HBA | vSAN 7.x | HBA firmware on HCL but health check uses stale HCL cache | Sync HCL database: `esxcli vsan cluster hcl-db sync` | N/A |
| `Unicast agent` alarm on healthy stretched cluster witness | vSAN 7.x | Witness appliance reports unicast agent warning falsely | Confirm witness connectivity via `esxcli vsan cluster unicastagent list` | 7.0 U3 |

## Capacity and Encryption

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Deduplication savings drop to 0% unexpectedly | vSAN OSA 7.x | Dedup engine paused during high-load resync | Dedup resumes automatically when resync completes | N/A |
| vSAN encryption key re-key fails: `KMS unreachable` | vSAN 7.x / 8.x | KMS not reachable from all ESXi hosts (not just vCenter) | Ensure KMS reachable on port 5696 from all ESXi VMkernel management IPs | N/A |
| Capacity alarm at 70% even with correct object policy | vSAN 7.x | Slack space reserved for rebuild operations counts toward used capacity | Normal behavior; expand cluster or reduce FTT policy | N/A |

## File Services

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| vSAN File Services NFS share returns `Access Denied` after ESXi upgrade | vSAN 7.0 U2 | File service agent VM NFS export config reset during upgrade | Re-configure NFS share permissions via vSAN File Service UI | 7.0 U3 |

## Stretched Cluster

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Witness appliance loses vSAN connectivity after IP change | vSAN 7.x / 8.x | vSAN unicast agent cache uses old IP | Update preferred fault domain and witness IP; re-add witness via vSAN → Configure → Fault Domains | N/A |
| Split-brain after network partition: preferred site not winning | vSAN 7.x | Partition bias config not set or overridden by `vSANForceProvisioning` | Confirm `vSAN.DOMOwnerForceProvisioning = 0`; verify preferred fault domain | N/A |

## See also

- [VMware vSAN — Common Issues](common-issues.md)
- [VMware ESXi — Known Issues](../../esxi/troubleshooting/known-issues/)
- [VMware vCenter — Known Issues](../../vcenter/troubleshooting/known-issues/)
