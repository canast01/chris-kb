# Windows Server — Troubleshooting

```
┌───────────────────────────────────────────────────────┐
│           Windows Server Triage Decision Tree         │
└──────────────────────┬────────────────────────────────┘
                       ▼
          ┌────────────────────────┐
          │  Server unreachable?   │
          └──────┬─────────────────┘
         Yes ◄───┤──► No
         ▼               ▼
┌───────────────┐  ┌─────────────────────────────────┐
│  Services     │  │  Identify symptom                  │
│  sc query /   │  ├──────────┬──────────┬───────────┤
│  Get-Service  │  │  Service │ Network  │  AD Auth     │
│  Event ID     │  │  stopped │ no route │  failures    │
│  7034/7036    │  └────┬─────┴────┬─────┴─────┬─────┘
└───────────────┘       ▼          ▼           ▼ 
               ┌──────────────┐ ┌──────────┐ ┌──────────────┐
               │ Get-WinEvent │ │ Test-Net │ │ dcdiag /test │
               │ -LogName Sys │ │Connection│ │ :replications│
               └──────┬───────┘ └────┬─────┘ └──────┬───────┘
                      └──────────────┴───────────────┘
                                     ▼
                         ┌─────────────────────────┐
                         │  Event Viewer / eventvwr │
                         │  System │ Application    │
                         │  Security log            │
                         └─────────────────────────┘
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
