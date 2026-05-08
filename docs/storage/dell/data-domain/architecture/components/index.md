# Data Domain — Components

## Core Components

| Component | Description |
|---|---|
| DDOS | Data Domain Operating System — the purpose-built OS managing the filesystem, dedup engine, protocols, and services |
| DDFS | Data Domain Filesystem — the underlying deduplicated storage layer; manages segments, containers, and references |
| SISL Engine | Stream-Informed Segment Layout — determines which segments are unique vs. duplicates using locality-based filtering before writing to disk |
| MTree | Logical namespace partition within DDFS; provides per-tenant or per-application capacity isolation, quotas, replication, and retention lock scope |
| DD Boost | Application-aware deduplication protocol; moves dedup processing partially to the backup client, reducing network traffic by 50% or more |
| VTL | Virtual Tape Library — emulates physical tape drives and libraries over Fibre Channel for backup software expecting tape |
| DD Encryption (D@RE) | Data at Rest Encryption — encrypts all on-disk data; integrates with RSA DPM or KMIP key managers |
| Cloud Tier | Extends DDFS to cloud object storage (AWS S3, Azure Blob, ECS) for long-term retention without a separate archive tier |
| NVRAM | Non-volatile write cache — absorbs incoming writes to protect against data loss during power failure |

## Protocol Interfaces

| Protocol | Use Case |
|---|---|
| DD Boost (over IP) | Veeam, NetBackup, CommVault, Avamar — application-aware dedup, fastest ingest |
| NFS v3/v4 | Generic Linux/Unix backup servers; NAS backup targets |
| CIFS/SMB | Windows backup clients; generic file-level targets |
| VTL (FC) | Backup software requiring tape emulation (NetBackup, TSM, older CommVault configs) |
| DD Boost (over FC) | High-throughput FC-attached DD Boost for high-performance environments |
| REST API | Programmatic management, automation, and monitoring |
| S3 | Cloud Tier gateway — aged backup data offloaded to cloud object storage |

## Connectivity and Network Design

- **Management network**: Dedicated NIC for DDOS management, System Manager GUI, REST API access. Recommend a separate management VLAN.
- **Data network**: Dedicated 10GbE or 25GbE bonds for backup traffic (DD Boost / NFS / CIFS). Bond with LACP for throughput and redundancy.
- **Replication network**: Separate interface or VLAN for MTree replication. Replication can be throttled per-schedule to protect production bandwidth.
- **FC SAN (VTL)**: HBAs connected to the SAN fabric for VTL tape emulation. Zone only the backup media servers to the VTL ports.

## Replication

Operational guidance for managing Data Domain replication — monitoring, troubleshooting, and failover.

### Replication Lag Thresholds

| Lag | Action |
|---|---|
| < 1 hour | Healthy |
| 1–4 hours | Monitor — could indicate network or load issue |
| > 4 hours | Alert — investigate immediately |
| Not updating | Context may be in error state |

### Replication Topologies

| Topology | Use Case |
|---|---|
| MTree replication (point-to-point) | Replicate individual MTrees independently to one or more targets |
| Collection replication | Full filesystem replication — replicates all MTrees as a single stream; used for full site DR |
| Cascaded replication | Source → Intermediate → Remote; useful when remote site is WAN-limited |
| Managed file replication | File-level replication for granular copy workflows |

### Routine Checks

```bash
# All replication contexts and their state
replication show all

# Contexts with issues (not replicating or idle)
replication status | grep -v "replicating\|idle"

# Current lag (bytes behind)
replication show stats | grep lag
```

### Manual Operations

```bash
# Trigger an immediate sync
replication sync <context_id>

# Pause replication (source continues writing; changes accumulate)
replication disable <context_id>

# Resume
replication enable <context_id>

# Resync (re-establishes after break or failover)
replication resync <context_id>
```

### Failover Procedure

Run on the **destination** Data Domain when the source is unavailable:

```bash
# Step 1 — break the context to make destination writeable
replication failover <context_id>

# Step 2 — redirect backup application to destination DD
# (update backup application target configuration)

# Step 3 — validate backup jobs complete successfully
ddboost show clients   # or nfs show clients
```

### Recovery After Primary Returns

```bash
# Step 1 — re-establish and resync
replication resync <context_id>

# Step 2 — confirm sync complete (lag = 0)
replication show stats | grep lag

# Step 3 — redirect backup application back to primary
```

### Common Replication Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Context in `error` state | Network, auth, or filesystem issue | Check `alert show current` |
| High lag | Bandwidth saturation or high source I/O | Check `replication show stats` — bytes/sec |
| Initialization stalled | Destination filesystem full | Check `filesys show space` on destination |
| Context stuck | Process issue on DD | `replication disable <id>` then `replication enable <id>` |
