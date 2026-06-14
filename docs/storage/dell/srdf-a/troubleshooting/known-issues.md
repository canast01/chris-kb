---
tags:
  - troubleshooting
  - srdf
  - dell
  - known-issues
---
# Dell SRDF/A — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known SRDF/A (Asynchronous) bugs, error codes, and workarounds covering journal overflow, WAN performance, and failover.

*Applies to: PowerMax SRDF/A*
</div>

## Before you begin

- SRDF/A state: `symrdf -g <dev-group> query` or Unisphere → Replication → SRDF.
- Journal capacity must accommodate delta changes during WAN outages — size journal for expected RTO.
- Delta changes exceeding journal → SRDF/A pauses and requires full resync.

## SRDF/A Pauses

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| SRDF/A in `Suspended` state | PowerMax | WAN link down; or journal overflow | Restore WAN; resume: `symrdf -g <dg> resume`; if journal overflow: full resync required | N/A |
| SRDF/A journal overflow after extended WAN outage | PowerMax | Delta accumulation exceeded journal LUN size | Expand journal LUN; tune SRDF/A cycle time; ensure journal ≥ (peak change rate × RTO window) | N/A |

## Failover

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Failover not allowed — R2 not ready` | PowerMax | Journal not flushed; destination not consistent | Wait for journal apply; or use `symrdf -g <dg> failover -force` for emergency (potential data loss) | N/A |
| Applications show data inconsistency after SRDF/A failover | PowerMax | Normal behavior — async gap depends on last committed cycle | Use SRDF/S for zero-RPO; SRDF/A has seconds to minutes of potential data loss | N/A |

## Performance

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Production host I/O latency increasing during SRDF/A resync | PowerMax | Resync competes with production for host I/O | Run resync during off-peak; use pace-of-resync throttle | N/A |

## See also

- [Dell SRDF-A — Common Issues](common-issues.md)
- [Dell PowerMax — Known Issues](../../powermax/troubleshooting/known-issues/)
- [Dell SRDF-S — Known Issues](../../srdf-s/troubleshooting/known-issues/)
