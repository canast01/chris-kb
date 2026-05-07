# NetBackup Architecture
## Three-Tier Architecture

| Component | Role | Typical Scale |
|---|---|---|
| Master Server | Policy management, catalog, scheduling | 1 per domain (HA pair optional) |
| Media Server | Data movement, deduplication, storage writes | Multiple, load-balanced |
| Client | Backup agent on protected host | Per protected server/VM |
| Storage Unit | Target storage for backup data | BasicDisk, AdvancedDisk, OST, Cloud, Tape |
| OpsCenter / IT Analytics | Centralised reporting and monitoring | Separate server; multi-domain |


## Three-Tier Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                     NetBackup Architecture                               │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Primary Server (Master Server)                                 │    │
  │  │  NetBackup catalogue  Policy DB  Job scheduler  EMM DB          │    │
  │  └──────────────────────────────┬──────────────────────────────────┘    │
  │                                 │  policy / job control                 │
  │         ┌───────────────────────┼────────────────────────┐              │
  │         │                       │                        │              │
  │  ┌──────▼──────┐        ┌───────▼──────┐        ┌───────▼──────┐       │
  │  │  Media Svr 1│        │  Media Svr 2 │        │  Media Svr 3 │       │
  │  │  (Site A)   │        │  (Site B/DR) │        │  (Cloud gate)│       │
  │  └──────┬──────┘        └───────┬──────┘        └───────┬──────┘       │
  │         │  data                 │                       │              │
  │  ┌──────▼──────┐        ┌───────▼──────┐        ┌───────▼──────┐       │
  │  │ Disk / MSDP │        │ Disk / MSDP  │        │  Cloud (S3)  │       │
  │  │ (dedup pool)│        │  (DR copy)   │        │  (long-term) │       │
  │  └─────────────┘        └──────────────┘        └──────────────┘       │
  │                                                                          │
  │  Clients: NBU agents on VMs, DB hosts, NAS NDMP, VMware backup host     │
  └──────────────────────────────────────────────────────────────────────────┘
```

## Master Server

The master server is the single most critical component — it holds the NetBackup catalog (file system and database tracking all backup images) and all policy definitions. Master server failure means no new jobs schedule.

High availability:
- **NetBackup HA** (clustering): Master server as Windows cluster or Linux active/passive
- **Catalog DR**: Daily catalog backup to a separate media server; restore procedure documented in DR runbook

Verify catalog backup is running:
```bash
bplist -S <master_server> -t 0 -policy NBU_Catalog_Backup -s -7d   # Jobs in last 7 days
```

## Media Server

Media servers perform data movement and can host Data Domain OST deduplication:

```bash
# List media servers and their status
nbemmcmd -lisths -machinetype media

# Check media server connectivity
bpclntcmd -hn <media_server> -chk
```

## Data Flow

```
Client (backup agent) → TCP 13782
    │
    ▼
Media Server (reads client data, deduplicates if OST, writes to storage unit)
    │
    ├── AdvancedDisk/BasicDisk (local disk storage units)
    ├── OpenStorage (Data Domain OST)
    └── Cloud Storage Unit (S3, Azure Blob)
    │
Master Server (catalogs image metadata, orchestrates scheduling)
```

## Storage Units

| Type | Use Case | Notes |
|---|---|---|
| BasicDisk | Simple disk storage | No dedup; good for short-term |
| AdvancedDisk | Disk with load balancing | Multiple paths; auto-selection of best path |
| OpenStorage (OST) | Dell Data Domain | Inline dedup; DD Boost protocol; AIR replication |
| Cloud Storage Unit | S3 / Azure | Long-term retention; high latency — not for fast restore |
| MSDP (Media Server Dedup Pool) | Native NetBackup dedup | No external appliance needed |
| Tape | Archival | LTO8/9; WORM media for compliance |

## NetBackup Appliance (5250/5350)

Integrated master + media + storage in a single platform:
- Pre-configured, hardened OS (NetBackup Appliance OS)
- Managed via NetBackup Appliance Shell Menu (CLISH) or Appliance Management Console (AMC)
- Scale-out by adding additional appliances to the domain

## Key Ports

| Port | Protocol | Purpose |
|---|---|---|
| 1556 | TCP | vnetd (BPRD) — main communication |
| 13724 | TCP | bpcd — client daemon |
| 13782 | TCP | bpbrm — backup/restore manager |
| 13785 | TCP | bpdbm — database manager (master) |
