# Aria Operations — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Alert Tuning, Capacity Planning, Dashboards, Reports, Related Sections.
</div>

```
┌───────────────────────────────────── Aria Operations Diagnostics ─────────────────────────────────────┐
│                                                                                                       │
│  Support bundle generation, log analysis, and REST API diagnostics for vROps.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Log File Diagnostics             │  │          REST API Diagnostic Checks         │   │
│   │            /var/log/vmware/vcops/            │  │          GET /suite-api/api/health          │   │
│   │         analytics.log: engine issues         │  │          GET /api/resources: count          │   │
│   │        collector.log: adapter errors         │  │         GET /api/alerts: active list        │   │
│   │         grep ERROR | tail to narrow          │  │         Compare before/after counts         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Logs reveal internal errors; REST API checks confirm cluster and collection health.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Support Bundle Generation           │  │             Cluster Diagnostics             │   │
│   │            SSH: vcops-support gen            │  │          VAMI: Cluster status page          │   │
│   │            VAMI: Admin > Support             │  │           cluster-mgmt-cli status           │   │
│   │          Download ZIP from VAMI UI           │  │           Check node role + state           │   │
│   │               Attach to GSS SR               │  │           Verify replica heartbeat          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster nodes on vSphere; SSH jump host; VAMI browser access on port 5480                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  analytics.log       = Engine log; check for out-of-memory or processing errors                       │
│  collector.log       = Adapter log; records collection attempts and failures                          │
│  vcops-support       = CLI command to generate full support bundle ZIP                                │
│  Support Bundle      = Compressed log + config archive; mandatory for GSS SR                          │
│  GET /health         = REST endpoint; returns cluster component health summary                        │
│  GET /resources      = Returns monitored object count; drop indicates issue                           │
│  GET /alerts         = Returns active alert list; useful for volume diagnosis                         │
│  cluster-mgmt-cli    = SSH CLI tool showing node roles and cluster join state                         │
│  Replica Heartbeat   = Periodic signal from replica to master; loss = HA risk                         │
│  VAMI Support Page   = Browser interface to download bundle without SSH                               │
│  grep ERROR          = First-pass log scan to identify exceptions quickly                             │
│  GSS SR              = Support case; attach bundle and describe issue timeline                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Aria Operations Diagnostics ─────────────────────────────────────┐
│                                                                                                       │
│  Support bundle generation, log analysis, and REST API diagnostics for vROps.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Log File Diagnostics             │  │          REST API Diagnostic Checks         │   │
│   │            /var/log/vmware/vcops/            │  │          GET /suite-api/api/health          │   │
│   │         analytics.log: engine issues         │  │          GET /api/resources: count          │   │
│   │        collector.log: adapter errors         │  │         GET /api/alerts: active list        │   │
│   │         grep ERROR | tail to narrow          │  │         Compare before/after counts         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Logs reveal internal errors; REST API checks confirm cluster and collection health.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Support Bundle Generation           │  │             Cluster Diagnostics             │   │
│   │            SSH: vcops-support gen            │  │          VAMI: Cluster status page          │   │
│   │            VAMI: Admin > Support             │  │           cluster-mgmt-cli status           │   │
│   │          Download ZIP from VAMI UI           │  │           Check node role + state           │   │
│   │               Attach to GSS SR               │  │           Verify replica heartbeat          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster nodes on vSphere; SSH jump host; VAMI browser access on port 5480                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  analytics.log       = Engine log; check for out-of-memory or processing errors                       │
│  collector.log       = Adapter log; records collection attempts and failures                          │
│  vcops-support       = CLI command to generate full support bundle ZIP                                │
│  Support Bundle      = Compressed log + config archive; mandatory for GSS SR                          │
│  GET /health         = REST endpoint; returns cluster component health summary                        │
│  GET /resources      = Returns monitored object count; drop indicates issue                           │
│  GET /alerts         = Returns active alert list; useful for volume diagnosis                         │
│  cluster-mgmt-cli    = SSH CLI tool showing node roles and cluster join state                         │
│  Replica Heartbeat   = Periodic signal from replica to master; loss = HA risk                         │
│  VAMI Support Page   = Browser interface to download bundle without SSH                               │
│  grep ERROR          = First-pass log scan to identify exceptions quickly                             │
│  GSS SR              = Support case; attach bundle and describe issue timeline                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Alert Tuning

Alert tuning is important because too many low-value alerts create noise.

### Good Alert Tuning Should Include

- Clear severity levels
- Actionable descriptions
- Ownership or assignment
- Escalation path
- Suppression rules for known maintenance windows
- Review of repeat alerts
- Removal of stale or low-value alerts

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident Notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

---

## Capacity Planning

### Cluster CPU and Memory

- Review CPU demand vs capacity per cluster
- Identify clusters approaching the threshold where HA failover capacity would be impacted
- Track CPU ready — high CPU ready indicates overcommitment

### Datastore and vSAN Capacity

- Review datastore usage — alert when free space drops below 20%
- For vSAN, track usable capacity and thin-provisioned risk
- Review snapshot growth contribution to capacity

### VM Growth Trends

- Use Aria Operations capacity reports to forecast VM count growth
- Review which clusters are projected to run out of capacity soonest

### Rightsizing

- Review oversized VMs — high CPU and memory allocation with consistently low usage
- Review undersized VMs — high CPU ready or memory ballooning under normal load
- Use Aria Operations rightsizing recommendations as a starting point — validate before making changes

### Monthly Review Process

1. Run the capacity dashboard in Aria Operations
2. Review cluster headroom report
3. Review datastore free space report
4. Review top growth VMs
5. Review rightsizing recommendations
6. Identify clusters or datastores needing action
7. Document findings and recommendations in the monthly capacity review

---

## Dashboards

### Common Dashboards

| Dashboard | Purpose |
|---|---|
| VMware Platform Health | Shows vCenter, clusters, hosts, datastores, and VM health |
| Capacity Dashboard | Tracks CPU, memory, datastore, and vSAN capacity |
| Alert Dashboard | Shows active alerts by severity |
| VM Performance Dashboard | Shows CPU ready, memory pressure, disk latency, and network usage |
| vSAN Dashboard | Shows disk group, capacity, object health, and resync status |
| Login and Access Dashboard | Tracks authentication failures and access events |

---

## Reports

### Aria Operations Rightsizing Review

Use Aria Operations to identify VMs that are oversized or undersized.

#### Oversized VMs

- High CPU and memory allocation with consistently low demand
- Review the CPU demand and memory demand charts over the last 30 days
- Use Aria Operations rightsizing recommendations as a starting point
- Validate with application owner before reducing resources

#### Undersized VMs

- High CPU ready or memory ballooning under normal load
- Indicates the VM needs more CPU or memory
- Review trend data before increasing resources

#### Resize Process

1. Identify the VM and its application owner
2. Review Aria Operations recommendations
3. Get change approval from the application owner
4. Schedule a maintenance window if a reboot is required
5. Resize the VM
6. Monitor CPU ready, memory, and application performance after resize
7. Document before and after metrics

#### Monthly Review

- Run the rightsizing report monthly
- Review top 10 oversized VMs
- Review top 10 undersized VMs
- Track progress on recommendations from previous months

---

## Related Sections

- [Operations](../../operations/index.md) — health checks and procedures
- [Escalation](../escalation/index.md) — opening vendor support cases
