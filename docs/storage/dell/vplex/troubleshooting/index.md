# Dell VPLEX — Troubleshooting


```text
┌───────────────────────────────────── Dell VPLEX Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Common faults: director failure, WAN link loss, split-brain, back-end path, cache fault    │   │
│   │      Director fault: peer director in cluster takes I/O; replace blade; check DRAM cache      │   │
│   │          WAN loss (Metro): witness determines survivor; losing cluster fences volumes         │   │
│   │    Detached volumes: virtual volume not accessible; check back-end path and director state    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Alert fires → VPLEX CLI → director/volume state check → isolate fault → remediate → verify         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Director Issues       │  │         Metro Issues        │  │        Volume Issues        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Director failed       │  │        WAN link lost        │  │       Volume detached       │   │
│   │         Cache fault         │  │         Split-brain         │  │        Back-end path        │   │
│   │         Port offline        │  │         Witness loss        │  │         Host no I/O         │   │
│   │       Director degrad       │  │        Fenced cluster       │  │         Storage view        │   │
│   │         Power fault         │  │        Failover stuck       │  │        Rebuild volume       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    VPLEX CLI → ls directors → ls virtual-volumes -t → check comm-links → fix root cause               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │    CLI command    │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │  Director fail   │  Director LEDs   │    ls directors   │  Replace blade   │  Cache corrupt   │   │
│   │     WAN loss     │ Comm-link state  │   ls comm-links   │  Fix WAN route   │   Split-brain    │   │
│   │   Vol detached   │  BE path state   │  ls virtual-vols  │   Fix BE path    │Vol unrecoverable │   │
│   │   Split-brain    │  Witness state   │    ls witnesses   │ Restore witness  │ Manual fence req │   │
│                                                                                                       │
│    Physical: director blade LEDs in chassis; FC SFP port lights; WAN IP link ping test                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Director fault = I/O or Storage director blade failure; peer director takes over in cluster        │
│    Cache fault    = DRAM write cache error; may require director replacement to clear                 │
│    WAN link lost  = Metro cluster communication disrupted; both clusters wait for witness             │
│    Split-brain    = Both clusters operational but disconnected; witness arbitrates survivor           │
│    Fenced cluster = Losing Metro cluster fences its volumes; I/O stops at losing site                 │
│    Witness loss   = Witness unreachable; Metro cluster cannot resolve split-brain safely              │
│    Volume detached= Virtual volume not serving I/O; check back-end path and director state            │
│    Back-end path  = FC path from Storage Director to array port; failure detaches volumes             │
│    ls directors   = Show director operational state: Online, Degraded, Faulted                        │
│    ls comm-links  = Show WAN link state and latency between Metro clusters                            │
│    Manual fence   = Force one cluster to fence when witness is also unreachable                       │
│    Rebuild volume = After BE path recovery, VPLEX re-attaches volume and syncs distributed state      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
