# SRDF/S

<div class="kb-summary">
Dell PowerMax SRDF/S synchronous replication — every host write committed to both R1 and R2 before acknowledgement; guarantees RPO = 0 with ≤10ms inter-site RTT requirement.
</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                      SRDF/S Architecture                             │
│                                                                      │
│  Primary Site (R1)                    DR Site (R2)                  │
│  ┌────────────────────┐               ┌────────────────────────┐    │
│  │  Host              │               │  PowerMax R2           │    │
│  │  Write I/O ──►     │               │                        │    │
│  │  PowerMax R1       │──sync write──►│  Write confirmed on R2 │    │
│  │  (holds ACK        │  (≤10ms RTT)  │  ──► ACK sent to R1    │    │
│  │   until R2         │               │                        │    │
│  │   confirms)        │◄──── ACK ─────│                        │    │
│  │  ──► ACK to host   │               │                        │    │
│  └────────────────────┘               └────────────────────────┘    │
│                                                                      │
│  RPO = 0 (zero data loss)                                           │
│  RTO = activate R2 ──► failover (< 15 min with automation)         │
│  RTT requirement: ≤ 10 ms (typically ≤ 5 ms recommended)           │
│                                                                      │
│  States: Synchronized ► Failed Over ► Suspended ► Re-sync          │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Synchronous write commit model, pair states, RTT requirements, SYMCLI commands, and RTO targets.</span>
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
