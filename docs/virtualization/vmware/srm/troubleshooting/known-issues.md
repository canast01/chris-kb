---
tags:
  - troubleshooting
  - srm
  - vmware
  - known-issues
---
# VMware Site Recovery Manager — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known SRM bugs, error codes, and workarounds covering protection groups, recovery plans, and vSphere Replication integration.

*Applies to: SRM 8.x / 9.x*
</div>

```text
┌──────────────────────────────────── VMware Site Recovery Manager ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            DR orchestration — automated failover, test failover, and recovery plans           │   │
│   │              Protocols: HTTPS (SRM API) · vCenter API · VRMS (SRM-to-SRM) · VAIO              │   │
│   │              Management: SRM UI (vCenter plugin) · REST API · PowerCLI SRM module             │   │
│   │            Protection group -> recovery plan -> test/failover -> VM power-on -> DNS           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Protection         │  │       Protection group      │  │     VMs grouped per RPO     │   │
│   │         Replication         │  │       Array / vSphere       │  │      SRA or VR adapter      │   │
│   │        Orchestration        │  │        Recovery plan        │  │     Ordered steps + cmds    │   │
│   │           Testing           │  │        Test failover        │  │    Isolated network test    │   │
│   │           Pairing           │  │      Protected/DR site      │  │      VRMS link required     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    SRM server    │ DR orchestrator  │     HTTPS 443     │     SSO / AD     │ Paired per site  │   │
│   │       VRMS       │    Site link     │       HTTPS       │    SRM trust     │ Cross-site link  │   │
│   │       SRA        │Array replication │   Array-specific  │   Array creds    │Per-vendor plugin │   │
│   │  Recovery plan   │  Failover steps  │      Internal     │    SRM admin     │ Test or real run │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: protected site (SRM + vCenter) -> replication -> DR site (SRM + vCenter)                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM          = Site Recovery Manager; VMware DR orchestration product                                │
│  Protection group = set of VMs protected together; maps to a replication group                        │
│  Recovery plan = ordered failover procedure; includes custom steps and scripts                        │
│  SRA          = Storage Replication Adapter; array-vendor plugin for SRM                              │
│  VRMS         = vSphere Replication Management Server; SRM site-link component                        │
│  Test failover = runs recovery plan in isolated network; no prod impact                               │
│  Planned migration = graceful failover; shuts down source before starting target                      │
│  Disaster recovery = emergency failover; source may be unavailable                                    │
│  Reprotect    = reverses replication after failover; preps for failback                               │
│  Failback     = returns VMs to original protected site after reprotect                                │
│  Network mapping = maps protected-site portgroup to DR-site portgroup                                 │
│  IP customization = SRM changes VM IP on failover per mapping rules                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- SRM error codes appear in `Recovery Plan History` → view steps; expand failed step for detail.
- Collect `vmware-dr.log` from the SRM appliance for support escalation.
- Most recovery plan failures trace to network mapping, datastore mapping, or placeholder VM issues — check these before assuming a bug.

## Recovery Plan Failures

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Error: Cannot power on VM — network not found` | SRM 8.x | Network mapping not configured for recovery network | Configure network mappings in SRM → Mappings → Network Mappings | N/A |
| Recovery plan stuck at `Waiting for storage systems to complete failover` | SRM 8.x | Array-based replication (ABR) storage provider unresponsive | Check storage provider health; retest storage provider in SRM UI | N/A |
| `Placeholder VM not found` during recovery | SRM 8.x | Placeholder VM deleted or orphaned on recovery site vCenter | Re-synchronize protection group; placeholders are auto-recreated | N/A |
| Reprotect fails: `Cannot replicate — disk already exists` | SRM 8.x | Residual VMDK from previous failover test not cleaned up | Delete residual disk from recovery datastore manually; retry reprotect | N/A |

## vSphere Replication Integration

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| vSphere Replication RPO alarm despite healthy sync | SRM 8.x | vSphere Replication lag metric includes quiesce time for large VMs | Tune RPO threshold; or disable quiescing for high-change VMs | N/A |
| `VR appliance pairing failed — certificate mismatch` | SRM 8.x | VRMS certificates not trusted between sites | Resubmit VRMS certificate to vCenter trust on both sites | N/A |

## Site Pairing

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Site pairing fails: `SSL certificate verification failed` | SRM 8.x | Remote SRM appliance certificate not trusted | Accept remote site certificate in SRM Site Pairing wizard | N/A |
| `Lost connection to remote site` after network change | SRM 8.x | SRM inter-site port 9086 blocked after firewall change | Verify TCP 9086 open between both SRM appliances | N/A |

## See also

- [VMware SRM — Common Issues](common-issues/)
- [VMware vSphere Replication — Known Issues](../../vsphere-replication/troubleshooting/known-issues.md)
- [VMware vCenter — Known Issues](../../vcenter/troubleshooting/known-issues.md)
