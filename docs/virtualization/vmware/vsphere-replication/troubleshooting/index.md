# vSphere Replication — Troubleshooting

```
  VR Troubleshooting Decision Tree
┌─────────────────────────────────────────────────────────────────┐
│  Site Recovery UI accessible?                                   │
│    No  → VRA services down / cert expired → Diagnostics        │
│    Yes ▼                                                        │
│  Sites show "Connected"?                                        │
│    No  → TCP 44046 blocked / thumbprint mismatch               │
│           → Common Issues: Site Pair Disconnected              │
│    Yes ▼                                                        │
│  Any replications in RPO violation (amber/red)?                 │
│    Yes → bandwidth / CPU / VRA disk full                        │
│           → Common Issues: RPO Violation                       │
│    No  ▼                                                        │
│  Replication fails with error?                                  │
│    Yes → TCP 31031 blocked / no route to VRA                   │
│           → Common Issues: Connection Refused                  │
│    No  ▼                                                        │
│  Unable to resolve → Escalation                                 │
└─────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
