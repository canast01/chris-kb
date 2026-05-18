# RASR

<div class="kb-summary">
Dell RASR (Recovery and System Restore) bare-metal recovery for Windows Server — WinPE boot media, sector-level image capture, and iDRAC virtual media for headless recovery.
</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                       RASR Workflow                                  │
│                                                                      │
│  Backup phase:                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Windows Server (running)                                     │   │
│  │    │  VSS snapshot (app-consistent)                           │   │
│  │    ▼                                                           │  │
│  │  RASR captures sector-level image ──► USB / network share    │    │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Restore phase (bare-metal):                                         │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Boot via WinPE (USB / iDRAC Virtual Media)                   │   │
│  │    │                                                           │  │
│  │    ▼                                                           │  │
│  │  RASR restores image to target disk (same or replacement HW)  │   │
│  │    │                                                           │  │
│  │    ▼                                                           │  │
│  │  Windows boots ──► post-restore validation ──► rejoin domain  │   │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Headless recovery via iDRAC: mount ISO remotely via virtual media   │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Recovery workflow, WinPE environment, Dell hardware integration, and RASR vs alternatives.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, recovery procedures, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
