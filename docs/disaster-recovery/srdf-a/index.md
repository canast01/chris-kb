# SRDF/A

<div class="kb-summary">
Dell PowerMax SRDF/A asynchronous replication — delta set cycle model buffers host writes and transmits to the R2 target on ~30-second cycles; RPO equals the last completed cycle.
</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                      SRDF/A Architecture                             │
│                                                                      │
│  Primary Site (R1)                    DR Site (R2)                  │
│  ┌────────────────────┐               ┌────────────────────────┐    │
│  │  PowerMax R1       │               │  PowerMax R2           │    │
│  │  Host writes ──►   │               │                        │    │
│  │  Delta Set N       │──cycle xmit──►│  Delta Set N applied   │    │
│  │  (buffered writes) │  (WAN/DWDM)   │  to R2 LUNs            │    │
│  │  Delta Set N+1     │               │                        │    │
│  │  (accumulating)    │               │  R2 usable after       │    │
│  └────────────────────┘               │  activation (failover) │    │
│                                       └────────────────────────┘    │
│                                                                      │
│  RPO = last completed cycle duration (~30s default)                 │
│  RTO = activate R2 copies ──► register VMs ──► power on (< 1hr)    │
│                                                                      │
│  States: Synchronized ► Transmitting ► Consistent ► Suspended       │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Delta set mechanics, dual-site topology, pair states, SYMCLI commands, and bandwidth sizing.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
