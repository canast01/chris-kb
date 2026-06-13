---
tags:
  - dell
  - troubleshooting
---
# Unity — Troubleshooting

<div class="kb-summary">
Diagnosing Unity replication failures, host connectivity issues, LUN/share provisioning errors, and drive faults.
</div>

```text
┌───────────────────────────────────── Dell Unity Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Common faults: SP failure (failover to peer), drive failure, FAST VP stall, NAS fault     │   │
│   │          SP failure: peer SP takes all I/O; replace faulted SP; monitor for stability         │   │
│   │    Drive failure: RAID rebuild starts automatically; do not remove drive until rebuild done   │   │
│   │       FAST VP stall: pool too full to tier; free space or expand pool before VP can run       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Unisphere alert → health view → identify fault (SP/drive/NAS/pool) → remediate → verify            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        SP / Hardware        │  │        Data Services        │  │        NAS / Network        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │           SP fault          │  │        FAST VP stall        │  │       NAS unreachable       │   │
│   │        Drive failure        │  │       Snap space full       │  │        SMB auth fail        │   │
│   │         RAID rebuild        │  │           Repl lag          │  │        NFS mount fail       │   │
│   │       Fan / PSU fault       │  │        Pool near-full       │  │         AD join fail        │   │
│   │       SFP / port fault      │  │         KMIP outage         │  │         Slow NFS I/O        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Check Unisphere health → event log filter → uemcli health query → fix layer → verify               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │        Tool       │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     SP fault     │  SP state LEDs   │    Unisphere HW   │    Replace SP    │ Both SPs failed  │   │
│   │  Drive failure   │  Drive bay LED   │    uemcli disk    │  Replace drive   │  Rebuild fails   │   │
│   │  FAST VP stall   │  Pool capacity   │   Unisphere pool  │    Free space    │  Pool >95% full  │   │
│   │ NAS unreachable  │ NAS Server state │   Unisphere NAS   │   Failover NAS   │ SP owning fault  │   │
│                                                                                                       │
│    Physical: SP A/B LEDs; drive bay amber LED; SFP port light; PSU green/amber indicator              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SP failover    = When SP A fails, SP B takes ownership of all LUNs and NAS Servers                 │
│    RAID rebuild   = Drive replacement triggers automatic data reconstruction onto new drive           │
│    FAST VP stall  = Pool <10% free; automated tiering cannot move data; free space first              │
│    NAS failover   = NAS Server migrated to peer SP when owning SP faults                              │
│    AD join fail   = NAS Server cannot rejoin AD domain; SMB auth will fail for all shares             │
│    Pool near-full = Pool >80% used; alert threshold; FAST VP stalls at ~95%                           │
│    KMIP outage    = DARE key unavailable; Unity uses cached key temporarily; fix urgently             │
│    uemcli disk    = uemcli /stor/hw/disk -list; shows drive state, slot, and tier                     │
│    Both SPs failed= Complete array outage; contact Dell TAC immediately; P1 case                      │
│    SFP port fault = Fibre Channel or iSCSI port SFP failed; host paths go dead                        │
│    Failover NAS   = Manually move NAS Server to peer SP via Unisphere migration wizard                │
│    Slow NFS I/O   = Check SP CPU, network saturation, and FAST VP job contending for I/O              │
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
  <span>Diagnostic commands, log locations, and analysis tools.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Dell support portal, case opening, SLA tiers, and escalation path.</span>
</a>

</div>
