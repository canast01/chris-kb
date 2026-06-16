---
tags:
  - troubleshooting
  - recoverpoint
  - dell
  - known-issues
---
# Dell RecoverPoint — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known RecoverPoint bugs, error codes, and workarounds covering RPA clustering, replication groups, and failover.

*Applies to: RecoverPoint for VMs (RP4VM) 5.x / RecoverPoint Classic 5.x*
</div>

```text
┌────────────────────────────────────────── Dell RecoverPoint ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Continuous data protection — any-point-in-time recovery for block storage           │   │
│   │                Protocols: FC · iSCSI (splitter) · IP WAN (journal replication)                │   │
│   │               Management: RecoverPoint Management Application (RPMA) · REST API               │   │
│   │             Write splitter -> journal capture -> replication -> any-point recovery            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Cluster           │  │        RPA appliances       │  │        Min 2 per site       │   │
│   │           Capture           │  │        Write splitter       │  │      FC or iSCSI layer      │   │
│   │           Journal           │  │          Change log         │  │     Stores writes per CG    │   │
│   │         Replication         │  │           WAN link          │  │     Async/sync to remote    │   │
│   │           Recovery          │  │       Bookmark / APIT       │  │    Rollback to any point    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       RPA        │Replication engine│     FC / iSCSI    │     Internal     │Physical appliance│   │
│   │     Splitter     │ Write intercept  │     FC / iSCSI    │       N/A        │On array or fabric│   │
│   │     Journal      │    Write log     │      Internal     │       N/A        │  Sized for RPO   │   │
│   │       RPMA       │  Management UI   │     HTTPS 443     │  Admin account   │   Java web app   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: host -> splitter (FC/iSCSI) -> RPA -> journal volumes -> remote RPA -> copy                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA          = RecoverPoint Appliance; physical or virtual appliance per site                        │
│  CG           = Consistency Group; set of volumes protected and recovered together                    │
│  Journal      = RecoverPoint write log; stores all changes to enable any-point recovery               │
│  Splitter     = intercepts host writes; sends copy to RPA journal simultaneously                      │
│  RPO          = Recovery Point Objective; max data loss; linked to replication lag                    │
│  APIT         = Any Point In Time; RecoverPoint capability to restore to any second                   │
│  Bookmark     = user-labeled APIT recovery point; e.g. before a patch                                 │
│  Image access = mount a past journal image to a host without failing over                             │
│  Failover     = activate the replica copy at DR site; reverse replication to recover                  │
│  WAN          = IP link between RPA clusters; RecoverPoint replicates journal over WAN                │
│  RPMA         = RecoverPoint Management Application; Java-based management UI                         │
│  Lag          = difference in write log between production and replica; drives RPO                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- RecoverPoint errors appear in Unisphere for RecoverPoint → Alerts.
- `rpcheck` tool on the RPA for connectivity diagnostics.
- Most replication failures are WAN port (11111/7218) or storage splitter issues.

## Replication Groups

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Replication group `Error — link lost` | RecoverPoint 5.x | TCP 11111 or 7218 blocked between RPA clusters | Verify ports 11111/7218 between RPA management IPs cross-site | N/A |
| RPO violation alarm despite recent writes | RecoverPoint 5.x | WAN bandwidth saturated; replication behind | Reduce replication group bandwidth limit; or increase WAN capacity | N/A |
| `Splitter error` on vSphere with RP4VM | RP4VM 5.x | RP4VM vSphere plugin not registered on ESXi host | Re-register RP4VM splitter on affected ESXi hosts | N/A |

## RPA Cluster

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| RPA cluster shows `Partial failure` | RecoverPoint 5.x | One RPA offline in HA pair | Check RPA hardware; cluster continues with degraded HA | N/A |
| `RPA cluster communication error` | RecoverPoint 5.x | Port 7225 blocked between RPAs within cluster | Verify TCP 7225 between all RPAs in the same cluster | N/A |

## Failover

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Test failover success but production failover fails | RecoverPoint 5.x | Production failover requires additional steps (enable access on copy) | Follow RecoverPoint failover procedure: `Enable Image Access` → `Failover` | N/A |
| `Cannot failover — consistency group not synchronized` | RecoverPoint 5.x | Group behind RPO; data may be lost | Accept data loss up to last consistent image; or wait for sync | N/A |

## See also

- [Dell RecoverPoint — Common Issues](common-issues.md)
- [Dell VPLEX — Known Issues](../../vplex/troubleshooting/known-issues/)
