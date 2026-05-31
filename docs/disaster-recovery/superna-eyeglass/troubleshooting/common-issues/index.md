# Superna Eyeglass — Common Issues

```text
┌────────────────────────────────── Superna Eyeglass — Common Issues ───────────────────────────────────┐
│                                                                                                       │
│   │     Symptom      │   Likely Cause   │    First Check    │       Fix        │      Verify      │   │
│   │     Sync lag     │SyncIQ policy slo │  igls sync status │ check bandwidth  │  isi sync polic  │   │
│   │    RAPA alert    │ransomware detect │  igls rapa status │quarantine + esca │   rapa report    │   │
│   │    DFS broken    │namespace not upd │  igls dfs status  │ retry DFS update │   dfsutil view   │   │
│   │  Failover fail   │ pre-check error  │  igls dr precheck │fix issue + re-ru │     igls log     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     General Triage Pattern                                    │   │
│   │          Is the issue new or recurring? New = recent change; Recurring = config problem       │   │
│   │             Is it isolated to one source or all? Isolated = agent; All = server/repo          │   │
│   │                                Check logs first: igls sync status                             │   │
│   │                    If unresolved in 2h: open vendor case with full log bundle                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link   │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection            │
│  RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats       │
│  SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies         │
│  DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS        │
│  Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster              │
│  Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product       │
│  Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits            │
│  Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site            │
│  Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team                  │
│  Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha       │
│  Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation      │
│  igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations                         │
│  SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation         │
│  Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Common Eyeglass issues include SyncIQ policies not being detected, low DR readiness scores, DNS cutover failures, and failover jobs that stall or complete with errors. Most issues trace back to API connectivity between Eyeglass and the PowerScale clusters, configuration drift between the primary and DR cluster, or DNS delegation misconfiguration.

| Issue | Likely Cause | Resolution |
|---|---|---|
| SyncIQ policy not detected | Eyeglass-to-OneFS API connectivity failure | Check Eyeglass cluster credentials and OneFS API reachability; re-register cluster in Eyeglass |
| DR readiness score low | Quota or share mismatch between clusters | Review Eyeglass sync log; re-run share/quota sync; check for manually created shares not in Eyeglass |
| DNS cutover failure | DNS delegation not configured or DNS plugin issue | Verify DNS delegation zone configuration; check Eyeglass DNS plugin logs; test manual DNS cutover |
| Failover stuck / not completing | API timeout, share conflict, or quota error | Review Eyeglass admin UI task log; check OneFS audit log for errors; use manual intervention steps in Eyeglass UI |
| RPO breach alerts | SyncIQ replication lag exceeding threshold | Check SyncIQ job status on source cluster (`isi sync jobs list`); check network bandwidth between sites |
| Eyeglass appliance unreachable | VM or network issue | Verify VM is powered on in vCenter; check management network connectivity; check Eyeglass service status via console |
