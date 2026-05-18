# Horizon (VDI) — Troubleshooting

```
  Troubleshooting Decision Tree
┌──────────────────────────────────────────────────────────┐
│  Problem reported                                        │
│         │                                                │
│         ▼                                                │
│  ┌─────────────────────────────────────────────────┐     │
│  │ Can user reach the login page (UAG/CS HTTPS)?   │     │
│  │  No ──► Network / firewall / UAG issue           │     │
│  │  Yes ──► continue                                │     │
│  └─────────────────────┬───────────────────────────┘     │
│                        ▼                                 │
│  ┌─────────────────────────────────────────────────┐     │
│  │ Can user authenticate?                          │     │
│  │  No ──► AD / RADIUS / SAML / True SSO issue     │     │
│  │  Yes ──► continue                               │     │
│  └─────────────────────┬───────────────────────────┘     │
│                        ▼                                 │
│  ┌─────────────────────────────────────────────────┐     │
│  │ Can user launch a desktop?                      │     │
│  │  No ──► Pool capacity / entitlement issue        │     │
│  │  Yes, but: blank screen / slow / app missing     │     │
│  │  ──► Protocol / Agent / AppVolumes / DEM issue   │     │
│  └─────────────────────────────────────────────────┘     │
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
