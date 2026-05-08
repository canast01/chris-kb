# NetBackup — Architecture Overview

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

## Key Ports

| Port | Protocol | Purpose |
|---|---|---|
| 1556 | TCP | vnetd (BPRD) — main communication |
| 13724 | TCP | bpcd — client daemon |
| 13782 | TCP | bpbrm — backup/restore manager |
| 13785 | TCP | bpdbm — database manager (master) |
