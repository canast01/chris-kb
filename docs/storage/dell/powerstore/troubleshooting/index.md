# PowerStore — Troubleshooting
```
┌─────────────────────────────────── Dell PowerStore Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Common faults: NVMe drive failure, replication lag, KMIP unreachable, capacity near-full   │   │
│   │    Drive failure: RAID rebuild auto-starts; replace failed drive; monitor rebuild progress    │   │
│   │     KMIP outage: array continues I/O while keys are cached; fix KMIP before cache expires     │   │
│   │        Replication lag: check network path, bandwidth throttle, and RPO policy schedule       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    CloudIQ alert → PowerStore Manager event → identify fault category → remediate → verify            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Hardware Faults       │  │         Replication         │  │       Security / Data       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       NVMe drive fail       │  │        Repl lag >RPO        │  │       KMIP unreachable      │   │
│   │         RAID rebuild        │  │        Policy paused        │  │        Capacity >90%        │   │
│   │          Node fault         │  │         Network loss        │  │         DARE key err        │   │
│   │        SSD wear high        │  │        Failover stuck       │  │       Snap space full       │   │
│   │       Fan / PSU fault       │  │         Cert expired        │  │        LDAP auth fail       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Check CloudIQ score → event log → hardware health view → isolate layer → fix and verify            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │        Tool       │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │  Drive failure   │   Drive health   │   PS Manager HW   │  Replace drive   │RAID rebuild fail │   │
│   │   KMIP outage    │  KMIP reachable  │   PS Manager sec  │  Fix KMIP reach  │  Volumes locked  │   │
│   │     Repl lag     │   Network path   │  PS Manager repl  │ Fix BW throttle  │   RPO exceeded   │   │
│   │  Capacity >90%   │   Usage trend    │      CloudIQ      │  Delete/archive  │ Pool full blocks │   │
│                                                                                                       │
│    Physical: check drive bay LED (amber = degraded); PSU LED; SFP port for replication link           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RAID rebuild   = PowerStore reconstructs data after NVMe drive failure onto hot spare              │
│    KMIP unreachable= Key server offline; array serves cached keys temporarily; fix before expiry      │
│    Volumes locked = DARE-encrypted volumes locked when KMIP key unavailable and cache expired         │
│    Repl lag >RPO  = Replication behind schedule; data loss exposure exceeds agreed RPO                │
│    Policy paused  = Replication policy suspended; resume after fixing network or space issue          │
│    Failover stuck = Metro Volume or async failover did not complete; check event log for error        │
│    Cert expired   = Replication TLS cert expired on source or target; renew and re-pair               │
│    SSD wear high  = NVMe drive write endurance approaching limit; replace before failure              │
│    Snap space full= Snapshot delta store consumed available capacity; delete old snaps first          │
│    LDAP auth fail = Admin cannot log in; check AD/LDAP connectivity and group membership              │
│    BW throttle    = Replication bandwidth limit; increase or remove throttle to clear lag             │
│    Pool full blocks= When usable capacity = 0%, all writes fail; emergency capacity needed            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known problems, error messages, and resolutions.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log collection, and analysis.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Escalation paths and Dell support.</span>
</a>

</div>
