---
tags:
  - troubleshooting
  - data-domain
  - dell
  - known-issues
---
# Dell Data Domain — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Data Domain bugs, error codes, and workarounds covering DD Boost, replication, NFS/CIFS, and filesystem health.

*Applies to: Data Domain OS 7.x*
</div>

```text
┌────────────────────────────────────────── Dell Data Domain ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Data Domain: purpose-built deduplication backup appliance and target             │   │
│   │                      Protocols: DD Boost · NFS · CIFS · iSCSI · FC · NDMP                     │   │
│   │                              Management: DDMC / DD System Manager                             │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │          Data path          │  │       DD Boost client       │  │      Client-side dedup      │   │
│   │          Appliance          │  │          DD engine          │  │         15-55x dedup        │   │
│   │         Replication         │  │        DD Replicator        │  │         Async MTREE         │   │
│   │          Management         │  │             DDMC            │  │       Central console       │   │
│   │            Cloud            │  │        DD Cloud Tier        │  │        Object archive       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │     DD Boost     │  Offload dedup   │    DD Boost lib   │  Cert/password   │   Client-side    │   │
│   │      MTREE       │  Data container  │   NFS/CIFS/Boost  │       RBAC       │  Per backup job  │   │
│   │  DD Replicator   │  DR replication  │   Encrypted TCP   │   Certificate    │      Async       │   │
│   │       DDMC       │   Central mgmt   │       HTTPS       │    LDAP/local    │     Multi-DD     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Data Domain appliance (DD3300/6400/9800) · replication WAN · backup application servers  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DD Boost           = client-side dedup library; shifts dedup processing to backup client hosts     │
│    MTREE              = logical data container on Data Domain; backup jobs target a specific MTREE    │
│    DD Replicator      = async MTREE replication between DD systems; source and destination must matc  │
│    DDMC               = Data Domain Management Center; centrally manages multiple DD appliances       │
│    Cloud Tier         = inactive backup data tiered to S3/Azure Blob/GCS object storage automaticall  │
│    Dedup ratio        = deduplicated size / original size; 20:1 typical for mixed backup workloads    │
│    Active Tier        = high-performance SSD/HDD tier holding recent backup data on the appliance     │
│    NDMP               = Network Data Management Protocol; NAS backup without requiring a host agent   │
│    VTL                = Virtual Tape Library; DD emulates tape drives for legacy backup software com  │
│    Retention Lock     = WORM protection on MTREE data; prevents deletion for a configured period      │
│    FastCopy           = efficient space-saving internal copy of MTREE data with no physical data mov  │
│    Encryption         = AES-256 at rest; FIPS 140-2 certified models available for compliance         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Data Domain alerts appear in DD System Manager → Health → Alerts.
- Logs: `log view` in the DDOS CLI; key log is `debug.log` for backup integration errors.
- Run `filesys status` and `filesys show compression` for filesystem health.

## DD Boost (Backup Integration)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Veeam/Commvault backup fails: `DD Boost connection refused` | DDOS 7.x | DD Boost user not enabled or TCP 2052 blocked | Enable DD Boost user: `ddboost user assign <user>`; verify TCP 2052 from backup server | N/A |
| DD Boost throughput lower than expected | DDOS 7.x | Distributed segment processing (DSP) disabled | Enable DSP on backup server — improves dedup efficiency and throughput | N/A |

## Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| DD Replicator pair showing `Error` state | DDOS 7.x | Network interruption; port 2051 blocked | Verify TCP 2051 between source and destination Data Domain; replication will resume automatically when connectivity restored | N/A |
| Replication lag growing | DDOS 7.x | WAN bandwidth insufficient for backup change rate | Throttle replication schedule; or increase WAN bandwidth | N/A |

## Filesystem

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `filesys status: needs cleaning` | DDOS 7.x | Filesystem cleaning has not run for >7 days | Run: `filesys clean start` | N/A |
| Capacity alarm despite recent expired-file cleanup | DDOS 7.x | Expired files not yet cleaned from filesystem | Filesystem cleaning must run to reclaim space; schedule or run manually | N/A |
| `ALERT: data collection suspended — filesystem full` | DDOS 7.x | Filesystem at 100% — writes suspended | Expire old backups; run cleaning; or expand filesystem capacity | N/A |

## See also

- [Dell Data Domain — Common Issues](common-issues.md)
- [Veeam — Known Issues](../../../backup/veeam/troubleshooting/known-issues/)
- [Commvault — Known Issues](../../../backup/commvault/troubleshooting/known-issues/)
