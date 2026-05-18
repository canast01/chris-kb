# vCenter — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware vCenter Server. Covers common VCSA failure patterns, SSO and certificate issues, diagnostic commands, log collection, and escalation procedures.
</div>

```
vCenter Troubleshooting Triage
════════════════════════════════════════════════════════

  Symptom                  First Check              Likely Cause
  ┌───────────────────┐    ┌──────────────────┐     ┌─────────────────┐
  │ UI not loading    │───▶│ service-control  │────▶│ vpxd stopped    │
  │ 503 / blank page  │    │ --status vpxd    │     │ or DB down      │
  └───────────────────┘    └──────────────────┘     └─────────────────┘

  ┌───────────────────┐    ┌──────────────────┐     ┌─────────────────┐
  │ SSO login fails   │───▶│ service-control  │────▶│ vmware-stsd     │
  │ (wrong creds err) │    │ --status vmware- │     │ stopped or AD   │
  │                   │    │ stsd             │     │ bind broken     │
  └───────────────────┘    └──────────────────┘     └─────────────────┘

  ┌───────────────────┐    ┌──────────────────┐     ┌─────────────────┐
  │ Cert error        │───▶│ VAMI → Cert Mgmt │────▶│ Machine SSL or  │
  │ in browser / API  │    │ openssl s_client  │     │ STS cert expired│
  └───────────────────┘    └──────────────────┘     └─────────────────┘

  ┌───────────────────┐    ┌──────────────────┐     ┌─────────────────┐
  │ Host Disconnected │───▶│ vpxd.log grep    │────▶│ vpxa agent /    │
  │ / Not Responding  │    │ <hostname>       │     │ cert thumbprint │
  └───────────────────┘    └──────────────────┘     └─────────────────┘

  Always check first:  df -h  (full partition = root cause ~40% of cases)
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known failure modes, symptoms, causes, and fixes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>What to collect before opening a support case and how to engage vendor support.</span>
</a>

</div>
