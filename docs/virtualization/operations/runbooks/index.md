# Virtualization Runbooks


<div class="kb-summary">
Practical runbooks for incidents, maintenance, lifecycle work, validation, evidence collection, and RCA follow-up.
</div>

```text
Runbook Selection Flow
═══════════════════════════════════════════════════════════

  Event or task triggered
           │
     ┌─────┴──────────────────────────────┐
     ▼                                    ▼
  Unplanned incident               Planned work
     │                                    │
     ├─ VMs/hosts impacted ──► Incident Response
     ├─ vCenter unavailable ──► vCenter Outage
     ├─ Backup failed       ──► Backup Failure
     └─ Unknown cause       ──► Evidence Collection
                                 + RCA Template
                                    │
                                    ├─ Host maintenance  ──► Host Evacuation
                                    ├─ Cert expiring     ──► Cert Renewal
                                    ├─ Snapshots stale   ──► Snapshot Cleanup
                                    ├─ VM request        ──► VM Lifecycle
                                    ├─ Storage change    ──► Storage Path Validation
                                    ├─ Network change    ──► Network Validation
                                    └─ Scheduled window  ──► Maintenance Window
```
┌─────────────────────────────────────── Virtualization Runbooks ───────────────────────────────────────┐
│                                                                                                       │
│    Practical runbooks for incidents, maintenance, lifecycle work, and RCA follow-up                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Incident Response      │  │         Planned Work        │  │          Reference          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Backup failure       │  │       Host evacuation       │  │      Health check index     │   │
│   │        vCenter outage       │  │       Snapshot cleanup      │  │       Troubleshooting       │   │
│   │      Host disconnected      │  │         VM lifecycle        │  │          Inventory          │   │
│   │       Evidence collect      │  │         Cert renewal        │  │       Quick reference       │   │
│   │         RCA template        │  │      Maintenance window     │  │        Decision trees       │   │
│   │      Incident response      │  │      Network validation     │  │         Cheat sheets        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Runbook          = Step-by-step procedure for a known task or incident type                        │
│    Evidence collect = Gather logs and screenshots before any remediation begins                       │
│    RCA              = Root Cause Analysis; post-incident document explaining why failure occurred     │
│    Host evacuation  = vMotion all VMs off a host before patching or hardware work                     │
│    VM lifecycle     = Standard steps for deploy, rename, reconfigure, and decommission                │
│    Incident         = Unplanned disruption; follow incident response runbook immediately              │
│    Planned work     = Scheduled change; requires approved change record before starting               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```text
┌─────────────────────────────────────── Virtualization Runbooks ───────────────────────────────────────┐
│                                                                                                       │
│    Practical runbooks for incidents, maintenance, lifecycle work, and RCA follow-up                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Incident Response      │  │         Planned Work        │  │          Reference          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Backup failure       │  │       Host evacuation       │  │      Health check index     │   │
│   │        vCenter outage       │  │       Snapshot cleanup      │  │       Troubleshooting       │   │
│   │      Host disconnected      │  │         VM lifecycle        │  │          Inventory          │   │
│   │       Evidence collect      │  │         Cert renewal        │  │       Quick reference       │   │
│   │         RCA template        │  │      Maintenance window     │  │        Decision trees       │   │
│   │      Incident response      │  │      Network validation     │  │         Cheat sheets        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Runbook          = Step-by-step procedure for a known task or incident type                        │
│    Evidence collect = Gather logs and screenshots before any remediation begins                       │
│    RCA              = Root Cause Analysis; post-incident document explaining why failure occurred     │
│    Host evacuation  = vMotion all VMs off a host before patching or hardware work                     │
│    VM lifecycle     = Standard steps for deploy, rename, reconfigure, and decommission                │
│    Incident         = Unplanned disruption; follow incident response runbook immediately              │
│    Planned work     = Scheduled change; requires approved change record before starting               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-5">

<a class="kb-card" href="incident-response/">
  <strong>Incident Response</strong>
  <span>Use this during virtualization incidents where VMs, hosts, clusters, datastores, networking, or management tools are impacted.</span>
</a>

<a class="kb-card" href="maintenance-window/">
  <strong>Maintenance Window Runbook</strong>
  <span>Use this for planned work across VMware, VxRail, NSX, Aria, hosts, clusters, or related services.</span>
</a>

<a class="kb-card" href="host-evacuation/">
  <strong>Host Evacuation Runbook</strong>
  <span>Use this before host maintenance, patching, hardware work, or lifecycle activity.</span>
</a>

<a class="kb-card" href="snapshot-cleanup/">
  <strong>VM Snapshot Cleanup Runbook</strong>
  <span>Use this to find and clean up old or risky VM snapshots.</span>
</a>

<a class="kb-card" href="vm-lifecycle/">
  <strong>VM Lifecycle Runbook</strong>
  <span>Use this for VM build, change, ownership, review, retirement, and cleanup.</span>
</a>

<a class="kb-card" href="storage-path-validation/">
  <strong>Storage Path Validation</strong>
  <span>Use this after SAN changes, storage maintenance, host work, or datastore alerts.</span>
</a>

<a class="kb-card" href="network-validation/">
  <strong>Network Validation</strong>
  <span>Use this after network changes, VLAN changes, host work, NSX changes, or VM connectivity issues.</span>
</a>

<a class="kb-card" href="certificate-renewal-planning/">
  <strong>Certificate Renewal Planning</strong>
  <span>Use this before vCenter, NSX, VxRail, Aria, or related certificate renewals.</span>
</a>

<a class="kb-card" href="evidence-collection/">
  <strong>Evidence Collection</strong>
  <span>Use this before vendor escalation, RCA work, or major incident review.</span>
</a>

<a class="kb-card" href="rca-template/">
  <strong>RCA Template</strong>
  <span>Use this after a virtualization incident or recurring problem.</span>
</a>


<a class="kb-card" href="backup-failure/">
  <strong>Backup Failure</strong>
  <span>Triage failed or missed VM backups — Veeam job errors, repository issues, and snapshot cleanup.</span>
</a>

<a class="kb-card" href="vcenter-outage/">
  <strong>vCenter Outage</strong>
  <span>Triage vCenter unavailability — VCSA services, VCHA failover, and host connectivity in standalone mode.</span>
</a>
</div>
