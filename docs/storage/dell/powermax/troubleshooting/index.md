# PowerMax — Troubleshooting

<div class="kb-summary">
PowerMax — Troubleshooting reference.
</div>

```
┌──────────────────────────────────── Dell PowerMax Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common faults: SRDF link degraded, masking view missing, SRP near-full, DARE key unreachable │   │
│   │        SRDF: check RDF link state, RDF group consistency, and ISL utilization on fabric       │   │
│   │     Masking: verify initiator group WWN, port group FA ports, and storage group membership    │   │
│   │         Performance: identify hot SLO tier, FA port saturation, or SRP over-commitment        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Alert fires → check Unisphere event log → run symrdf/symcfg → isolate layer → remediate            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         SRDF Issues         │  │        Host / Masking       │  │       Perf / Capacity       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Link degraded        │  │       Host sees no LUN      │  │        SRP >80% full        │   │
│   │         Out of sync         │  │       Wrong initiator       │  │      FA port saturated      │   │
│   │       Suspended state       │  │        No port group        │  │         SLO not met         │   │
│   │         Group split         │  │       Masking missing       │  │       DARE key timeout      │   │
│   │        ISL congestion       │  │         HBA offline         │  │        Snap gen full        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Isolate layer (fabric / array / host) → confirm with symrdf -g query or symcfg list                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │        Tool       │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │  SRDF link down  │  RDF link state  │  symrdf -g query  │   Resume link    │ Link stays down  │   │
│   │  No LUN visible  │   Masking view   │    symmask list   │   Fix masking    │  Zoning correct  │   │
│   │  Perf degraded   │  SLO compliance  │   Unisphere perf  │  Rebalance SRP   │ SLO breach cont. │   │
│   │  DARE key error  │  KMIP reachable  │  Unisphere alert  │  Fix KMIP reach  │ Array locked out │   │
│                                                                                                       │
│    Physical: check RDF director LEDs; FA port LEDs; ISL port counters on SAN switch                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RDF link state = SRDF link health: In Sync / Suspended / Failed / Consistent states                │
│    Snap gen full  = TimeFinder/Snap generation limit reached; oldest snap must be terminated          │
│    SLO compliance = Percentage of volumes meeting their Service Level Objective latency target        │
│    symmask        = SYMAPI masking tool; list and audit masking views, initiator and port groups      │
│    ISL congestion = Inter-Switch Link saturation between fabric switches; affects SRDF bandwidth      │
│    DARE key timeout= KMIP server unreachable; array may lock encrypted volumes after threshold        │
│    SRP over-commit = Thin pool subscribed beyond physical capacity; data at risk if all written       │
│    FA port saturated= Front-End director port at bandwidth limit; redistribute hosts to other ports   │
│    Group split    = SRDF consistency group members diverged; requires re-establish from R1            │
│    symmaskdb      = SYMAPI database for masking configuration; exportable for audit                   │
│    RDF director LED= Physical indicator on director blade; amber = degraded, red = failed             │
│    symcfg list    = SYMAPI command to list array config: SRP, director, port, volume info             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Dell PowerMax Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common faults: SRDF link degraded, masking view missing, SRP near-full, DARE key unreachable │   │
│   │        SRDF: check RDF link state, RDF group consistency, and ISL utilization on fabric       │   │
│   │     Masking: verify initiator group WWN, port group FA ports, and storage group membership    │   │
│   │         Performance: identify hot SLO tier, FA port saturation, or SRP over-commitment        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Alert fires → check Unisphere event log → run symrdf/symcfg → isolate layer → remediate            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         SRDF Issues         │  │        Host / Masking       │  │       Perf / Capacity       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Link degraded        │  │       Host sees no LUN      │  │        SRP >80% full        │   │
│   │         Out of sync         │  │       Wrong initiator       │  │      FA port saturated      │   │
│   │       Suspended state       │  │        No port group        │  │         SLO not met         │   │
│   │         Group split         │  │       Masking missing       │  │       DARE key timeout      │   │
│   │        ISL congestion       │  │         HBA offline         │  │        Snap gen full        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Isolate layer (fabric / array / host) → confirm with symrdf -g query or symcfg list                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │        Tool       │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │  SRDF link down  │  RDF link state  │  symrdf -g query  │   Resume link    │ Link stays down  │   │
│   │  No LUN visible  │   Masking view   │    symmask list   │   Fix masking    │  Zoning correct  │   │
│   │  Perf degraded   │  SLO compliance  │   Unisphere perf  │  Rebalance SRP   │ SLO breach cont. │   │
│   │  DARE key error  │  KMIP reachable  │  Unisphere alert  │  Fix KMIP reach  │ Array locked out │   │
│                                                                                                       │
│    Physical: check RDF director LEDs; FA port LEDs; ISL port counters on SAN switch                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RDF link state = SRDF link health: In Sync / Suspended / Failed / Consistent states                │
│    Snap gen full  = TimeFinder/Snap generation limit reached; oldest snap must be terminated          │
│    SLO compliance = Percentage of volumes meeting their Service Level Objective latency target        │
│    symmask        = SYMAPI masking tool; list and audit masking views, initiator and port groups      │
│    ISL congestion = Inter-Switch Link saturation between fabric switches; affects SRDF bandwidth      │
│    DARE key timeout= KMIP server unreachable; array may lock encrypted volumes after threshold        │
│    SRP over-commit = Thin pool subscribed beyond physical capacity; data at risk if all written       │
│    FA port saturated= Front-End director port at bandwidth limit; redistribute hosts to other ports   │
│    Group split    = SRDF consistency group members diverged; requires re-establish from R1            │
│    symmaskdb      = SYMAPI database for masking configuration; exportable for audit                   │
│    RDF director LED= Physical indicator on director blade; amber = degraded, red = failed             │
│    symcfg list    = SYMAPI command to list array config: SRP, director, port, volume info             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known issues, symptoms, and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and performance analysis.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Dell support portal, case opening, SLA tiers, and escalation path.</span>
</a>

</div>
