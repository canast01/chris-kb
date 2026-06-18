---
tags:
  - troubleshooting
  - netbackup
  - backup
  - known-issues
---
# Veritas NetBackup — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known NetBackup bugs, error codes, and workarounds covering backup policies, media servers, and VMware integration.

*Applies to: NetBackup 10.x*
</div>

```text
┌────────────────────────────────────────── Veritas NetBackup ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Enterprise backup — Master/Media servers, policies, NetBackup catalog             │   │
│   │               Protocols: NDMP · VTL emulation · DD Boost · TCP 1556 (PBX/vnetd)               │   │
│   │                Management: NetBackup Admin Console / OpsCenter / Web UI (10.x)                │   │
│   │           Policy schedule -> Master server -> Media server -> Storage unit -> Client          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Control           │  │        Master server        │  │   Catalog (NBDB), policies  │   │
│   │          Data mover         │  │         Media server        │  │   Writes to storage units   │   │
│   │            Client           │  │          bpcd agent         │  │    Per-host backup agent    │   │
│   │           Storage           │  │      Storage unit / DD      │  │     Disk, tape, DD Boost    │   │
│   │            Certs            │  │     Host ID certificates    │  │      NBU 8.x+ mandatory     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  Master server   │ Catalog+schedule │      TCP 1556     │  Cert (NBU 8+)   │NBDB Sybase-based │   │
│   │   Media server   │  Data movement   │      TCP 1556     │       Cert       │ Many per master  │   │
│   │       bpcd       │   Client agent   │      TCP 1556     │       Cert       │ Each client runs │   │
│   │       AIR        │ Auto Img Replic. │      TCP 1556     │       Cert       │Cross-domain copy │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: master server - media servers - Data Domain/tape library - clients                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master server  = central control plane; owns the catalog and policies                                │
│  Media server   = writes backup data to storage units; can combine with master                        │
│  NBDB           = NetBackup relational database (Sybase) storing the catalog                          │
│  Policy         = defines schedule, client list, and backup type for clients                          │
│  Storage unit   = logical target (disk pool, tape, cloud) media servers write to                      │
│  bpcd           = NetBackup client daemon listening for backup/restore requests                       │
│  vnetd          = NetBackup network daemon; multiplexes traffic over fewer ports                      │
│  AIR            = Auto Image Replication; replicates images between NBU domains                       │
│  Host ID cert   = NBU 8.x+ mandatory cert authenticating client to master                             │
│  DD Boost       = NetBackup-to-Data-Domain dedup offload integration                                  │
│  Catalog backup = backup of the NBDB itself; critical for full env recovery                           │
│  bpps           = command listing active NetBackup processes for triage                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- NetBackup error codes are documented at `veritas.com/support` — most codes have a dedicated KB article.
- Run `bpgetconfig` on master server and clients to verify connectivity.
- `nbcertcmd` manages certificate operations in NetBackup 8.x+ (mandatory web certificate).

## Common Error Codes

| Error Code | Description | Cause | Fix |
|---|---|---|---|
| Status 96 | `An error occurred when trying to write to a file` | Disk storage unit full | Free space on storage unit; increase storage unit quota |
| Status 58 | `Can't connect to client` | Client not reachable on port 1556 (VNETD) | Verify TCP 1556 from media server to client; check client NBU service |
| Status 2074 | `Client host is busy` | Too many concurrent streams to client | Reduce concurrent jobs in policy; check client resource limits |
| Status 196 | `Client backup was not attempted because backup window closed` | Job window too short for data size | Extend backup window; or reduce client data size |
| Status 25 | `Cannot connect on socket` | NBU service not running on client | Start `bpcd` on client; verify `netbackup` service status |

## VMware Integration

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VMware policy backup fails: `Snapshot error` | NBU 10.x | ESXi host cannot create snapshot during backup window | Check vCenter events for snapshot failure reason; reduce concurrent VMware jobs | N/A |
| `Discovery failed` for VMware policy | NBU 10.x | vCenter credentials invalid or vCenter not reachable | Update vCenter credentials in NetBackup → Credentials → VMware | N/A |

## DD Boost

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| DD Boost backup failing: `Network error` | NBU 10.x | TCP 2052 blocked between NBU media server and Data Domain | Verify TCP 2052 open from all media servers to Data Domain | N/A |
| AIR (Auto Image Replication) not replicating | NBU 10.x | Target domain not reachable via port 1556 | Verify TCP 1556 between source and destination NBU master servers | N/A |

## Certificates (NBU 8.x+)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Client shows `Certificate error` — not connecting to master | NBU 8.x+ | Host ID-based certificate expired or not enrolled | Re-enroll: `nbcertcmd -enrollCertificate -server <master>` | N/A |

## See also

- [NetBackup — Common Issues](common-issues/)
- [Dell Data Domain — Known Issues](../../../storage/dell/data-domain/troubleshooting/known-issues.md)
