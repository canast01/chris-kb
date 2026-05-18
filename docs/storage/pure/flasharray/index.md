# Pure FlashArray

<div class="kb-summary">
All-flash block storage running Purity//FA — ActiveDR, ActiveCluster, NVMe/FC, NVMe/RoCE, snapshots, protection groups, and Pure1 cloud management for tier-1 and mission-critical block workloads.
</div>

```
Pure FlashArray — HA Controller Pair
┌─────────────────────────────────────────────────────────────┐
│  Controller CT0 — Active                                    │
│  ├── Front-End Ports: FC / iSCSI / NVMe-oF                  │
│  ├── NVRAM (write acknowledged here — < 1 ms)               │
│  ├── Inline Dedup + Compression engine                      │
│  └── Back-End: NVMe Flash Shelves                           │
└───────────────────────┬─────────────────────────────────────┘
                        │  active/active HA link (NVRAM mirror)
┌───────────────────────▼─────────────────────────────────────┐
│  Controller CT1 — Active                                    │
│  (symmetric — both serve I/O simultaneously)                │
└─────────────────────────────────────────────────────────────┘
                        │
              ┌─────────▼──────────┐
              │  NVMe Flash Shelf  │  (shared between CT0 + CT1)
              ├────────────────────┤
              │  NVMe Flash Shelf  │
              └────────────────────┘

Host connectivity (multipath):
ESXi ──► 2× FC HBA ──► FC Fabric A + Fabric B ──► CT0 + CT1 ports
         (both paths active for I/O load balancing — ALUA AA)
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
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
