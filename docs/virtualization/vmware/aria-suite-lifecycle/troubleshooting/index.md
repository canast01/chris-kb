# Aria Suite Lifecycle — Troubleshooting

```
  LCM Troubleshooting Decision Tree
┌─────────────────────────────────────────────────────────────────┐
│  LCM UI accessible?                                             │
│    No  → check vmware-vrlcm / nginx services; vracli status     │
│    Yes ▼                                                        │
│  Product cards all GREEN?                                       │
│    No  → click red card → check service / disk / cert on prod   │
│    Yes ▼                                                        │
│  Upgrade/deploy request stuck (RUNNING > 2h)?                   │
│    Yes → check lcm-app.log for timeout; do NOT power off VMs    │
│           → Common Issues: Upgrade Stuck                        │
│    No  ▼                                                        │
│  VIDM login broken?                                             │
│    Yes → VIDM health check; re-register VIDM in LCM             │
│    No  ▼                                                        │
│  Certificate import / replacement failing?                      │
│    Yes → openssl verify chain; key modulus check; passphrase    │
│           → Common Issues: Locker Cert Import Fails             │
│    No  → Diagnostics → support bundle → Escalation              │
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
