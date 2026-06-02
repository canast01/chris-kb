# Nexus Dashboard Operations


<div class="kb-summary">
Nexus Dashboard Operations reference.
</div>

```text
┌──────────────────────────────────── Nexus Dashboard — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Daily            │  │            Weekly           │  │           Monthly           │   │
│   │      Review NDI health      │  │        Anomaly review       │  │       Compliance audit      │   │
│   │       Check anomalies       │  │      Act on ITSM items      │  │       Threshold review      │   │
│   │      Verify cluster OK      │  │       Review flow data      │  │        Access review        │   │
│   │       Check backup ran      │  │      Dismiss false pos      │  │        Report to mgmt       │   │
│   │      Triage new events      │  │       Capacity outlook      │  │       Upgrade planning      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Operations via ND web UI and acs CLI · ND management IP via browser                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NDI health = Site health score overview; check daily for score drops                                 │
│  Cluster check = acs health to confirm all 3 nodes ACTIVE                                             │
│  Backup verification = acs backup list to confirm daily backup completed                              │
│  Anomaly review = Weekly triage of open NDI anomalies; dismiss or create tickets                      │
│  Flow review = Weekly check of NDI flow analytics for unexpected traffic patterns                     │
│  Compliance audit = Monthly NDI assurance run verifying fabric matches policy                         │
│  Access review = Monthly audit of ND user list; remove stale accounts                                 │
│  Upgrade planning = Monthly check of ND/NDI release cadence for patch scheduling                      │
│  False positive = Anomaly that does not represent a real issue; dismiss with reason                   │
│  Capacity outlook = ND storage and compute resource trending; plan expansion                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Daily operational checks begin on the Nexus Dashboard health page to confirm all cluster nodes are green and all installed services are running. Review fabric health scores for all onboarded fabrics and sort active faults by severity to triage any P1 or P2 items. Check endpoint connectivity anomalies in NDI and review NDFC policy deployment status for any failed deployments. Weekly, review fabric utilisation metrics and capacity headroom across all fabrics.

**Daily Checklist**
- ND Admin > System Health — all nodes green, all services running
- Fabric health scores — flag any fabric below acceptable threshold
- Active faults — sort by severity, triage P1/P2 immediately
- NDI Endpoint Connectivity — review anomaly alerts
- NDFC — check policy deployment job status, resolve any failures

**Weekly Tasks**
- Review fabric utilisation and capacity metrics in NDI
- Check for new ND or NDFC software updates
- Review audit log for unexpected policy changes
