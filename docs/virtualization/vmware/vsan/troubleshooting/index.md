# vSAN — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware vSAN. Covers common failure patterns, diagnostic commands, log collection, and escalation procedures for engaging VMware support.
</div>

```
vSAN TRIAGE FLOW

  Symptom reported
  (VM slow / inaccessible / health alarm)
         │
         ▼
  Step 1 — Cluster status
  esxcli vsan cluster get
         │
         ├── Hosts missing from cluster?
         │       └──► Check host power / network connectivity
         │
         ├── Step 2 — Object health
         │   esxcli vsan debug object list | grep -v Healthy
         │       ├── Degraded → host or disk failure likely
         │       └── Inaccessible → multiple failures or partition
         │
         ├── Step 3 — Resync status
         │   esxcli vsan debug resync summary get
         │       └── Bytes > 0 → resync in progress (expected after failure)
         │
         ├── Step 4 — Disk groups
         │   esxcli vsan storage list
         │       └── Degraded DG → cache SSD or capacity disk failure
         │
         └── Step 5 — Network
             esxcli vsan debug network test
                 └── Packet loss → MTU mismatch / NIC / switch issue
                           │
                           ▼
                   Resolve → monitor resync → verify health green
                           │
                    still stuck after 4h → Escalate (VMware GSS)
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
