# Site Recovery Manager — Troubleshooting

```
  SRM Troubleshooting Decision Tree
┌──────────────────────────────────────────────────────────┐
│  Is site pairing Connected?                              │
│   No ──► Cert thumbprint / TCP 9086 / SRM service        │
│   Yes ──► continue                                       │
│                   │                                      │
│                   ▼                                      │
│  Are Protection Groups all OK?                           │
│   No ──► RPO lag / VRA unreachable / SRA error           │
│   Yes ──► continue                                       │
│                   │                                      │
│                   ▼                                      │
│  Does Recovery Plan pre-check pass?                      │
│   No ──► Network mapping / resource pool / placeholder   │
│   Yes ──► Run test failover                              │
│                   │                                      │
│                   ▼                                      │
│  Test failover VMs power on and respond?                 │
│   No ──► Resource / IP customization / network issue     │
│   Yes ──► Cleanup and document result                    │
└──────────────────────────────────────────────────────────┘
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
