---
tags:
  - dr
  - troubleshooting
---
# DR Troubleshooting

<div class="kb-summary">
Troubleshooting guides for DR failures — backup job errors, replication lag, failover issues, IRE connectivity problems, and backup validation failures.
</div>

```text
┌─────────────────────────────────── DR Operations — Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   Coverage: backup job failures, replication lag, failover failures, IRE connectivity                 │
│   First checks: job log, replication status, network connectivity, storage capacity                   │
│   Escalation paths: backup vendor support, storage team, network team, DR coordinator                 │
│   Use structured triage: determine if issue is data, network, storage, or compute layer               │
│                                                                                                       │
│   Backup job failures                                                                                 │
│   Check job log in backup console (Veeam / CommVault / NBU) for exact error code                      │
│   Common causes: network timeout, storage full, permission denied, VSS snapshot failure               │
│   VSS errors: check VSS event logs on source VM; restart VSS writers if stale                         │
│   Storage full: check repository capacity; extend or expire old backup sets before retry              │
│                                                                                                       │
│   Replication lag                                                                                     │
│   Query replication status from backup console; compare last sync time to RPO target                  │
│   Causes: network bandwidth saturation, source I/O spike, storage performance issue                   │
│   Throttle other backup jobs to free bandwidth; check network utilisation on WAN link                 │
│   Replication jobs stuck: disconnect and reconnect replication mapping; force resync                  │
│                                                                                                       │
│   Failover failures                                                                                   │
│   Verify DR storage is healthy and volumes are promoted before powering VMs on                        │
│   Check DNS resolution at DR site; confirm management VLAN reachable from DR hosts                    │
│   VM power-on failures: check VM config, vSAN health, datastore availability at DR site               │
│   If partial failover: document what succeeded; do not attempt full rollback mid-failover             │
│                                                                                                       │
│   IRE connectivity                                                                                    │
│   IRE = Isolated Recovery Environment; air-gapped network for ransomware recovery testing             │
│   Verify IRE firewall rules; confirm backup appliance can reach IRE segment                           │
│   IRE DNS must resolve backup server and proxy names inside the isolated network                      │
│                                                                                                       │
│   Physical infrastructure                                                                             │
│   Backup servers and proxies at both primary and DR sites; out-of-band management access              │
│   Replication network: dedicated VLAN or WAN circuit with QoS prioritising replication                │
│                                                                                                       │
│   Key terms:                                                                                          │
│   VSS          = Volume Shadow Copy Service; Windows snapshot provider for consistent backups         │
│   IRE          = Isolated Recovery Environment; air-gapped recovery lab for malware incidents         │
│   replication mapping = configured pair of source volume and DR target volume                         │
│   job log      = per-job execution log in backup console; first place to check failures               │
│   repository   = storage target defined in backup tool; holds all backup data and metadata            │
│   RPO breach   = replication lag exceeds the agreed Recovery Point Objective threshold                │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="backup-failures/">
  <strong>Backup Failures</strong>
  <span>Diagnosing and resolving backup job failures across Veeam, Commvault, and NetBackup — failure classification, diagnostic flowcharts, and resolution steps.</span>
</a>

</div>

