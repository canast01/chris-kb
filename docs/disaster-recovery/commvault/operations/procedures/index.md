```bash
# Check client connectivity readiness
qoperation execscript -sn QS_CheckReadiness

# Confirm all jobs are complete (no active jobs)
qlist jobs

# Check CommServe services status
qlist services
```

```text
┌───────────────────────────── Commvault Operational Procedures — Runbooks ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Procedure Library                                       │   │
│   │                  Standard runbooks for recurring Commvault operational tasks                  │   │
│   │              Each procedure: purpose, prerequisites, steps, validation, rollback              │   │
│   │           Change-controlled: procedures require CAB approval for production changes           │   │
│   │                 Test quarterly in staging CommCell before production execution                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Procedures cover storage, client management, DR, compliance, and recovery                          │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Storage Mgmt     │      Client Mgmt      │     DR / Recovery     │       Compliance      │   │
│   │    Add disk library   │     Add new client    │    CS failover test   │     WORM extension    │   │
│   │   Extend library LUN  │     Push iDA agent    │   Restore to DR site  │    Audit log export   │   │
│   │     Add tape drive    │     Retire client     │   CommCell DR drill   │    Legal hold apply   │   │
│   │  DDB move to new disk │  Edit storage policy  │  Cloud recovery test  │     SLA report gen    │   │
│   │    Library pruning    │   Subclient changes   │   CSDB restore test   │    Retention review   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    CommServe Failover Procedure (abbreviated):                                                        │
│      1. Verify SQL log shipping is current (< 15 min lag) on DR CommServe                             │
│      2. Stop CommVault services on primary CommServe                                                  │
│      3. Apply pending SQL logs on DR CommServe; bring CSDB online                                     │
│      4. Update DNS A record to point CommServe FQDN to DR server IP                                   │
│      5. Start CommVault services on DR CommServe; verify Job Manager starts                           │
│      6. Run test backup on representative client to confirm CommCell operational                      │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CS failover: DR CommServe needs same hostname/IP reachability as primary (DNS/IP change)             │
│  Library access: DR MAs must have mount path access to all disk libraries post-failover               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CAB            = Change Advisory Board; approves production changes to backup infrastructure         │
│  WORM Lock      = Compliance lock preventing deletion of backup data before expiry                    │
│  Legal Hold     = Indefinite retention lock applied to data involved in litigation                    │
│  CS Failover    = Switching CommCell to DR CommServe after primary failure                            │
│  DR Drill       = Periodic test of CommServe failover and restore procedures                          │
│  DDB Move       = Migrating DDB from one disk to another without data loss                            │
│  Library Pruning = Removing expired backup chunks from disk library to reclaim space                  │
│  Retire Client  = Removing client from CommCell; requires data expiry and decommission                │
│  iDA Push       = Installing client agent remotely from CommServe without local access                │
│  Subclient Edit = Modifying content, schedule, or storage policy assignment for a subclient           │
│  SQL Log Ship   = Transaction log replication from primary CSDB to DR CommServe                       │
│  Mount Path     = File system path on MediaAgent where disk library chunks are stored                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
