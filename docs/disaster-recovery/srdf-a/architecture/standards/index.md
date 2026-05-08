# SRDF/A — Standards

> Part of the [SRDF/A](../../) reference.

---

## RPO and Cycle Time

SRDF/A cycle time defines the maximum data age (RPO) when a failure occurs mid-cycle. Default cycle time is 30 seconds; the maximum acceptable lag is negotiated per application class.

| Application Class | Target RPO | Cycle Time | Notes |
|---|---|---|---|
| Tier 1 (financial, critical DB) | ≤ 30s | 30s | Default |
| Tier 2 (business apps) | ≤ 60s | 60s | Allowed if WAN constrained |
| Tier 3 (dev/test replication) | ≤ 300s | 300s | Batch workloads |

Monitor actual achieved RPO — it is always ≤ cycle time in normal operation:
```bash
symrdf -g <rdfg> query -v | grep "Minimum Cycle Time"
```

## SRDF Group Naming Convention

```
RDFG-<site-pair>-<app-tier>-<seq>
```

Examples:
- `RDFG-DC1DC2-DB-01` — first DB-tier group between DC1 and DC2
- `RDFG-DC1DC2-APP-01` — application tier
- `RDFG-DC1DC3-ARCHIVE-01` — archival replication to tertiary site

## Device Group Naming

```
DG-<env>-<app>-<site>-<seq>
```

Examples:
- `DG-PROD-ERP-DC1-01`
- `DG-PROD-DB-DC1-01`

## SRDF Group Number Allocation

Maintain an SRDF group number allocation register in CMDB. Ranges:

| Range | Purpose |
|---|---|
| 1–50 | Tier 1 production sync/async groups |
| 51–100 | Tier 2 business apps |
| 101–150 | DR testing and pre-production |
| 151–200 | Reserved for future expansion |

## Consistency Group Design Rules

- One SRDF group per application tier (DB, APP, WEB) — never mix tiers in a single group
- Group all volumes of a multi-volume application into one consistency group to ensure write-order fidelity
- Do not exceed 2,048 devices per SRDF group
- Test consistency at minimum quarterly during DR tests

## Bandwidth Sizing

```
Required bandwidth (MB/s) = peak_change_rate_MB_per_cycle / cycle_time_s × 1.20
```

Where 1.20 = 20% headroom for burst absorption. Measure peak change rate with:

```bash
symrdf -g <rdfg> query -v | grep "MBs Written"
```

## Device Sizing

- R2 (target) volumes must be equal in size to R1 (source) — no thin over-subscription on R2
- R2 volumes must be formatted identically (track type, emulation) as R1
- Verify before establishing:
```bash
symdev show -sid <target_SID> <dev_id> | grep -E "Size|Track"
```
