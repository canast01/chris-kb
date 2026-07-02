---
tags:
  - architecture
  - veeam
---
# Veeam — Standards

<div class="kb-summary">
Standards reference covering Job Naming Convention, Retention Schedule, Backup Job Configuration Standards, Encryption Standard, Proxy Standards and 3 more sections.

*Applies to: Veeam Backup & Replication 12.x*
</div>

```d2
direction: down

job_naming_convention: "Job Naming Convention" {shape: rectangle}
retention_schedule: "Retention Schedule" {shape: rectangle}
backup_job_configuration_standards: "Backup Job Configuration Standards" {shape: rectangle}
encryption_standard: "Encryption Standard" {shape: rectangle}
proxy_standards: "Proxy Standards" {shape: rectangle}
repository_standards: "Repository Standards" {shape: rectangle}

job_naming_convention -> retention_schedule: hardens
retention_schedule -> backup_job_configuration_standards: hardens
backup_job_configuration_standards -> encryption_standard: hardens
encryption_standard -> proxy_standards: hardens
proxy_standards -> repository_standards: hardens
```

## Job Naming Convention

| Object | Convention | Example |
|---|---|---|
| Backup job | `<env>-<workload>-<type>` | `prod-vm-daily`, `dr-fileserver-weekly` |
| Backup copy job | `<env>-<workload>-copy-<dest>` | `prod-vm-copy-offsite` |
| Replication job | `<env>-<workload>-repl` | `prod-critical-vm-repl` |
| SOBR | `<site>-sobr-<tier>` | `dc1-sobr-primary` |
| Repository | `<site>-repo-<type>-<seq>` | `dc1-repo-ssd-01`, `dc2-repo-linux-01` |

## Retention Schedule

| Level | Restore Points | Schedule | Repository |
|---|---|---|---|
| Daily | 14 | Incremental (synthetic full weekly) | Performance tier (fast disk) |
| Weekly | 8 | Synthetic full | Performance tier |
| Monthly | 12 | Active full (monthly) | SOBR capacity tier offload |
| Yearly | 7 | Active full (yearly) | Object storage archive |

SOBR capacity tier offload: configure automatic offload after 14 days → moves monthly/yearly points to object storage.

### Backup Job Types Comparison

## Backup Job Configuration Standards

- **Backup window**: 22:00–06:00 (default); set hard stop to prevent daytime impact
- **Source-side deduplication**: Enabled on all jobs (reduces WAN for copy jobs)
- **Compression**: Optimal (default) — do not use Extreme unless backup window permits extra CPU time
- **Application-aware processing**: Enabled for all jobs containing SQL Server, Oracle, Exchange, Active Directory VMs
- **Guest OS quiescence**: VSS quiescence for Windows VMs; file system freeze for Linux VMs

## Encryption Standard

Mandatory encryption for:
- All backup copy jobs targeting off-site repositories
- All cloud repository targets (SOBR capacity tier)
- Any job protecting VMs with classified or regulated data (PII, financial, healthcare)

Algorithm: AES-256.

**Key management**:
- Export encryption keys immediately after creation
- Store in CyberArk → dedicated VBR Encryption Keys safe
- Rotate keys annually — plan for re-encryption of existing backup files

## Proxy Standards

| Setting | Standard |
|---|---|
| Minimum proxies per site | 2 (redundancy + parallel capacity) |
| Transport mode preference | Hot-add (SAN) > Direct NFS > NBD |
| Max concurrent tasks per proxy | vCPU count / 2 (default) |
| Proxy OS | Windows Server 2022 or RHEL 8+ (Linux proxy) |

## Repository Standards

| Repository Type | Use Case | Performance Target |
|---|---|---|
| Linux hardened (immutable) | Primary onsite backup | XFS or ReFS; 10 GbE minimum |
| NFS/SMB share | Secondary onsite storage | Dedicated NAS volume; 10 GbE |
| S3-compatible (SOBR capacity) | Long-term / archival | Glacier-class for yearly; Standard for monthly |

## Sizing Guidelines

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {"text": "Backup Server — vCPU and RAM by Scale", "fontSize": 13, "fontWeight": "normal"},
  "width": 360,
  "height": 180,
  "data": {
    "values": [
      {"scale": "<100 VMs",     "metric": "vCPU",    "val": 4},
      {"scale": "<100 VMs",     "metric": "RAM (GB)", "val": 8},
      {"scale": "100–500 VMs",  "metric": "vCPU",    "val": 8},
      {"scale": "100–500 VMs",  "metric": "RAM (GB)", "val": 16},
      {"scale": "500–2000 VMs", "metric": "vCPU",    "val": 16},
      {"scale": "500–2000 VMs", "metric": "RAM (GB)", "val": 32}
    ]
  },
  "mark": {"type": "bar", "cornerRadiusEnd": 3},
  "encoding": {
    "x": {
      "field": "scale", "type": "nominal",
      "sort": ["<100 VMs", "100–500 VMs", "500–2000 VMs"],
      "axis": {"title": "Deployment Scale"}
    },
    "y": {"field": "val", "type": "quantitative", "axis": {"title": "Count / GB"}},
    "color": {
      "field": "metric", "type": "nominal",
      "scale": {"domain": ["vCPU", "RAM (GB)"], "range": ["#1d4ed8", "#15803d"]},
      "legend": {"title": "Resource"}
    },
    "xOffset": {"field": "metric", "type": "nominal"},
    "tooltip": [
      {"field": "scale",  "type": "nominal",     "title": "Scale"},
      {"field": "metric", "type": "nominal",     "title": "Resource"},
      {"field": "val",    "type": "quantitative","title": "Value"}
    ]
  }
}
```

| Scale | Backup Server | Proxies per Site |
|---|---|---|
| < 100 VMs | 4 vCPU, 8 GB RAM | 1–2 |
| 100–500 VMs | 8 vCPU, 16 GB RAM | 2–4 |
| 500–2,000 VMs | 16 vCPU, 32 GB RAM (+ full SQL) | 4–8 |

## Instant VM Recovery RTO Targets

| Application Tier | Target RTO |
|---|---|
| Tier 1 (critical DB, ERP) | < 15 minutes via Instant VM Recovery |
| Tier 2 (business apps) | < 1 hour |
| Tier 3 (dev/test) | < 4 hours |

Document agreed RTOs in the DR plan; validate quarterly via Instant VM Recovery test.

---

## See also

- [Veeam — Deploy](../../deploy/)
