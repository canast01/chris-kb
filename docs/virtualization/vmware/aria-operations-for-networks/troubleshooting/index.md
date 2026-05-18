# Aria Ops for Networks — Troubleshooting

```
┌──────── Aria Networks Troubleshooting Decision Tree ───────────────────────────┐
│                                                                                 │
│  Symptom                                                                        │
│      │                                                                          │
│      ├── Collector Disconnected ──► TCP 443 to Platform │ disk usage │ re-pair │
│      │                                                                          │
│      ├── Data Source Sync Error ──► credentials │ cert thumbprint │ perms       │
│      │                                                                          │
│      ├── No Flows in UI          ──► NetFlow on switch │ UDP 2055 │ vDS IPFIX  │
│      │                                                                          │
│      ├── NSX topology missing    ──► NSX data source added? │ Auditor role     │
│      │                                                                          │
│      ├── UI slow / searches hang ──► Platform VM CPU/mem │ query too broad     │
│      │                                                                          │
│      ├── License expired         ──► Settings ► License ── enter new key       │
│      │                                                                          │
│      └── Platform not responding ──► systemctl status hms nginx                │
│                                      support bundle ► VMware Support            │
└────────────────────────────────────────────────────────────────────────────────┘
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
