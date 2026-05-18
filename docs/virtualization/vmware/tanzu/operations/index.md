# Tanzu — Operations

```
┌───────────────────── Tanzu Operations Overview ───────────────────────────────┐
│                                                                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │ CLI Ref     │  │ Health      │  │ Procedures  │  │ Install & Upgrade   │   │
│  │ tanzu/kubectl│  │ Checks      │  │ Namespaces  │  │ Supervisor ► mgmt   │  │
│  │ Carvel/Velero│ │ Supervisor  │  │ RBAC, Ingress│  │ cluster ► workload  │  │
│  │ Harbor CLI  │  │ TKC ► nodes │  │ Helm deploy │  │ rolling upgrade     │   │
│  └─────────────┘  │ PVCs/certs  │  └─────────────┘  └─────────────────────┘   │
│                   └─────────────┘                                              │
│  ┌─────────────┐  ┌─────────────────────────────────────────────────────────┐ │
│  │ Backup &    │  │  Scripts                                                │ │
│  │ Restore     │  │  List clusters │ PVC audit │ resource usage │ cert expiry│ │
│  │ Velero/VCSA │  │  Harbor CVE scan │ Harbor vuln check                   │  │
│  └─────────────┘  └─────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Commands, syntax, and quick reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Routine checks, service validation, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Day-to-day operational tasks and how-to guides.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation, upgrade, patching, and decommission.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup configuration, restore procedures, and validation.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and reusable code.</span>
</a>

</div>
