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

```text
┌───────────────────────────────────────── Dell SRDF/A (Async) ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Asynchronous SRDF — periodic delta-set replication between PowerMax arrays          │   │
│   │                 Protocols: SRDF over FC (GigE option) · SRDF/IP (TCP over WAN)                │   │
│   │                  Management: Unisphere for PowerMax · Solutions Enabler · SMC                 │   │
│   │            R1 write -> delta set capture -> cycle commit -> transmit to R2 -> apply           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Source           │  │      R1 (primary) array     │  │      Host writes to R1      │   │
│   │          Delta set          │  │         Async buffer        │  │    Accumulates per cycle    │   │
│   │             Link            │  │        SRDF/IP or FC        │  │     Transfers delta set     │   │
│   │            Target           │  │      R2 (replica) array     │  │      Applies delta set      │   │
│   │          Management         │  │       Unisphere / SMC       │  │      SRDF group config      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    R1 volume     │ Production copy  │     FC / iSCSI    │   Host zoning    │ Writable by host │   │
│   │    R2 volume     │   Replica copy   │     SRDF link     │       N/A        │ Read-only (repl) │   │
│   │    SRDF group    │   Link config    │      FC / IP      │   Array trust    │  RA port pairs   │   │
│   │Solutions Enabler │  CLI management  │     Local/REST    │   Admin creds    │ symmcli commands │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: R1 PowerMax -> SRDF RA ports -> WAN/FC link -> R2 PowerMax RA ports                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF         = Symmetrix Remote Data Facility; Dell PowerMax replication tech                        │
│  SRDF/A       = SRDF Asynchronous; batched delta-set replication (RPO > 0)                            │
│  R1           = Source (production) volume; host writes here                                          │
│  R2           = Replica volume; updated when delta set transmitted and applied                        │
│  Delta set    = set of changed tracks accumulated during one async cycle                              │
│  Cycle time   = interval at which delta sets are committed and transferred                            │
│  RA port      = SRDF port on PowerMax; dedicated to replication link traffic                          │
│  RDFA         = Remote Data Facility Async; older term for SRDF/A                                     │
│  SRDF group   = logical link between R1 and R2; defines RA ports used                                 │
│  Consistency  = all R2 volumes in a group updated together per cycle                                  │
│  Suspend      = pauses replication; delta set accumulates until resumed                               │
│  SMC          = Solutions Management Console; Java SRDF management GUI                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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

- [Dell SRDF-A — Common Issues](common-issues/)
- [Dell PowerMax — Known Issues](../../powermax/troubleshooting/known-issues.md)
- [Dell SRDF-S — Known Issues](../../srdf-s/troubleshooting/known-issues.md)
