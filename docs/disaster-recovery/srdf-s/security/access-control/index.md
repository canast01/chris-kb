# SRDF/S — Access Control

```
┌─────────────────────────────────────── SRDF/S — Access Control ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                SRDF/S — RBAC and Access Control                               │   │
│   │       Auth: Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access       │   │
│   │             Principle of least privilege: each role gets only required permissions            │   │
│   │              Service accounts: dedicated, non-interactive; rotation every 90 days             │   │
│   │               Emergency break-glass: documented, monitored, time-limited access               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Role       │   Access Level   │    Typical User   │   Review Freq    │    Granted By    │   │
│   │      Admin       │ Full config/ops  │   Sr Backup Eng   │    Quarterly     │  Security team   │   │
│   │     Operator     │ Start/stop jobs  │     Backup Eng    │    Quarterly     │    Team lead     │   │
│   │     Monitor      │  Read-only view  │      NOC / L1     │    Quarterly     │    Team lead     │   │
│   │   Service Acct   │  API / headless  │     Automation    │   Per rotation   │  Security team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment        │
│  R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency       │
│  R2            = target volume; must acknowledge each write; acts as synchronous mirror               │
│  RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency       │
│  RPO=0         = zero recovery point objective; no data loss possible under normal operation          │
│  RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min       │
│  symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver       │
│  Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split                          │
│  Consistent    = transient state where R1 write is in transit but not yet confirmed on R2             │
│  Failover      = makes R2 read-write; production continues from DR site after R1 failure              │
│  Restore       = re-synchronises after failover; direction is reversed until R1 catches up            │
│  RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters           │
│  FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)            │
│  RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [SRDF/S Security](../index.md) reference.

---

## Preventing Accidental Failover

SRDF/S failovers are zero-data-loss but cause site-wide impact. Guard against accidental execution:

- Require second-factor confirmation for `symrdf failover` in production:
  ```bash
  export SYMCLI_CONFIRM=prompt    # Requires manual y/n before executing
  ```
- Implement a two-person rule: all production SRDF failovers require peer approval before execution
- Restrict `symrdf establish -full` (full resync) to break-glass account — this destroys R2 content

---

## Audit Logging

All SRDF state changes are recorded in the PowerMax audit log:

```bash
# View recent RDF events
symevent list -sid <SID> -type rdf -last 100

# Export for SIEM ingest
symevent list -sid <SID> -type rdf -output csv > /tmp/rdf_events.csv
```

Configure Unisphere → Notifications → Syslog to forward SRDF events to SIEM. Alert on:
- `SRDF Split` outside maintenance windows
- `SRDF Failover` (any occurrence)
- `SRDF Suspend` without corresponding maintenance ticket
- `SRDF Invalid` (indicates device state inconsistency)
