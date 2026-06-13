---
tags:
  - scenarios
  - vmware
---
# DR Test and Planned Failover

<div class="kb-summary">
A DR test proves recovery works without impacting production — replicated VMs boot in an isolated
bubble network at the DR site while production continues running. A planned failover is a real
migration with graceful shutdown at the primary site, used for site maintenance or data centre
migrations. Both operations are orchestrated by SRM, but they differ significantly in scope,
risk, and required preparation. This scenario covers both paths and the common mistakes that cause
them to fail.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌───────────────────────────── DR Test / Planned Failover — Procedure Flow ─────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  DR Test: non-disruptive — VMs boot in isolated bubble network, production continues                  │
│  Planned Failover: real migration — graceful shutdown at primary, services move to DR site            │
│                                                                                                       │
│  START: SRM Recovery Plan selected — choose execution type                                            │
│                                                                                                       │
│  DR TEST PATH                                                                                         │
│  SRM powers on VM replicas in isolated bubble network at DR site                                      │
│  Application smoke test on isolated VMs — production unaffected throughout                            │
│  Cleanup: SRM powers off test VMs, removes test network · production unaffected                       │
│                                                                                                       │
│  PLANNED FAILOVER PATH                                                                                │
│  Pre-flight: check DR site capacity and verify replication RPO is within target                       │
│  SRM shuts down primary VMs · syncs final changed blocks → powers on at DR with prod IPs              │
│  Validate: VMs up · DNS resolves · NSX segments mapped · Aria Ops alerts clear                        │
│                                                                                                       │
│  COMMON ERRORS                                                                                        │
│  RPO not met before failover — check vSphere Replication health first                                 │
│  Forgot to run Cleanup after DR test — test replicas block real failover capacity                     │
│  NSX segment mapping not configured — VMs power on with no network at DR site                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


!!! warning "Production traffic cutover"
    Executing a planned failover transfers production traffic to the recovery site. Confirm all replication groups are synchronised (RPO = 0) and stakeholders are notified before starting.
## Products Involved

| Product | Role in This Scenario |
|---|---|
| VMware SRM | Orchestrates both DR test and planned failover; manages recovery plan execution and cleanup |
| vSphere Replication | Replicates VM data from primary to DR site at the configured RPO interval |
| vCenter Server | Present at both sites; SRM is a vCenter plugin at each site |
| NSX | Provides matching network segments at the DR site; SRM integrates with NSX for segment mapping |
| Aria Operations | Post-failover health validation; connected to DR site vCenter to monitor recovered VMs |

---

## DR Test — Non-Disruptive Recovery Validation

A DR test boots replicated VM snapshots in an isolated test network at the DR site while production VMs at the primary site continue running throughout.

### 1. Verify Replication Health Before the Test

Confirm all VMs in the recovery plan are within their RPO before starting the test.

```powershell
# Confirm all VMs in the recovery plan are at RPO — must show OK, not Warning or Error
# SRM → Site Recovery → Replication → review status column for all protected VMs
```

Expected: every VM shows status **OK** and last sync time within the configured RPO window. A VM showing **RPO Violated** or **Not Responding** will fail to power on during the test.

### 2. Run the DR Test

SRM → **Recovery Plans** → select the plan → **Test**.

SRM creates a temporary isolated test network (bubble network) and powers on the replicated VM
snapshots at the DR site. The test network uses a separate IP range or NAT so there are no IP
conflicts with production.

### 3. Validate Application Functionality

Log into each test VM and run application smoke tests:
- Can the application start and respond?
- Can it reach its database (if also in the recovery plan)?
- Are application-layer health checks passing?

Document any failures — the DR test is only valuable if results are recorded and acted on.

### 4. Clean Up After the Test

SRM → **Recovery Plans** → select the plan → **Cleanup**.

SRM powers off all test VMs and removes the isolated test network. **Do not skip the cleanup step.** Test VMs left running consume DR site capacity and may interfere with a real failover.

---

## Planned Failover — Graceful Production Migration to DR Site

A planned failover gracefully migrates all protected workloads from the primary to the DR site with typically zero data loss if replication is current at the time of failover.

### 1. Pre-Failover Checks

Confirm DR site capacity and replication currency before initiating failover.

```powershell
# Check replication status — all VMs must be at RPO before initiating planned failover
# SRM → Replication → confirm all statuses show OK

# Check DR site cluster has sufficient capacity for all failed-over VMs
Get-Cluster "DR-Cluster" | Select Name,
  @{N="EffectiveCPUMHz";E={($_ | Get-View).Summary.EffectiveCpu}},
  @{N="EffectiveMemMB";E={($_ | Get-View).Summary.EffectiveMemory}}
```

Expected: all VMs at RPO; DR cluster effective CPU and memory headroom sufficient for all recovery plan VMs plus HA admission control reservation.

### 2. Initiate Planned Failover

SRM → **Recovery Plans** → select the plan → **Run** → select **Planned Migration**.

What SRM does during a planned migration (in order):
1. Quiesces and powers off primary site VMs gracefully (in the order defined by the recovery plan)
2. Triggers a final vSphere Replication sync to capture any remaining changed blocks
3. Powers on DR site VMs in the order defined by the recovery plan (priority groups)
4. Applies network customisation: maps primary site networks to DR site networks using the
   Network Mapping configured in SRM

### 3. NSX Network Configuration at the DR Site

Verify all required NSX segments exist and are mapped in SRM before initiating failover.

```bash
# Verify required segments exist at DR site NSX Manager before failover
# NSX Manager (DR site) → Networking → Segments → confirm all required segments are present
# SRM → Site Recovery → Network Mappings → confirm all primary segments have a DR mapping
```

Expected: every primary segment has a corresponding DR segment and an SRM network mapping entry. Missing mappings cause VMs to power on with disconnected NICs.

### 4. DNS After Planned Failover

Update DNS only if VMs receive new IP addresses at the DR site (different subnet — no stretched L2).

```bash
# Update DNS A records to point to the new DR IP for each application FQDN
# If using Active Directory DNS — run on a DC at the DR site after VMs are up:
# dnscmd /recorddelete <zone> <hostname> A <old-IP>
# dnscmd /recordadd <zone> <hostname> A <new-DR-IP>

# Verify resolution from a DR site client after DNS update
nslookup app.domain.local <DR-DNS-server-IP>
```

Expected: `nslookup` returns the DR site IP for each application FQDN.

### 5. Post-Failover Validation

Confirm all VMs are powered on and connect Aria Operations to the DR site vCenter.

```powershell
# Verify all VMs in the recovery plan are powered on at the DR site
Get-Cluster "DR-Cluster" | Get-VM |
  Where-Object {$_.PowerState -ne "PoweredOn"} |
  Select Name, PowerState
```

Expected: zero VMs returned (all are PoweredOn). Aria Operations manual collection returns no critical alerts.

### 6. Failback to Primary Site

When the primary site is ready to resume, run Reprotect to reverse replication, then execute a planned migration back.

SRM → **Recovery Plans** → **Reprotect** — this reconfigures the recovery plan for DR-to-Primary
direction. Then run the plan as a planned migration from DR back to primary.

Confirm that primary site hosts, storage, and networking are fully healthy before initiating
failback. A failback to a site still under maintenance causes an immediate second failover.

---

## Post-Task Validation

| Check | Method | Expected Result |
|---|---|---|
| All VMs powered on at DR | vCenter DR site → Cluster → VMs | 100% PoweredOn |
| Application connectivity | Application smoke test per app | All apps responding on expected URLs |
| DNS resolving to DR IPs | `nslookup <app-fqdn>` from client | Returns DR site IP |
| NSX segment connectivity | Ping test between VMs on same segment | Reachable |
| Replication reversed (post-failback) | SRM → Replication | DR→Primary direction, status OK |
| Aria Ops — no critical alerts | Aria Ops against DR vCenter | No critical alerts on recovered VMs |

---

## Key Terms

| Term | Definition |
|---|---|
| SRM | Site Recovery Manager — the VMware product that orchestrates DR tests, planned failovers, and failbacks by executing recovery plans that define VM startup order, network mappings, and IP customisation |
| vSR | vSphere Replication — the VMware-native replication engine that continuously replicates VM changed blocks from the primary site to the DR site at a configured RPO interval |
| RPO | Recovery Point Objective — the maximum acceptable age of data at the DR site after a failure; a 15-minute RPO means replication must transfer changed blocks at least every 15 minutes |
| RTO | Recovery Time Objective — the maximum acceptable time from a failure event to workloads being accessible at the DR site; RTO is reduced by pre-staging VMs and having tested recovery plans |
| bubble network | An isolated test network created by SRM during a DR test that has no routing to production; allows DR-site VMs to power on and be tested without creating IP conflicts with their running production counterparts |
| test recovery | The SRM execution mode that powers on replicated VM snapshots in an isolated bubble network at the DR site without disrupting production — used for regular DR testing |
| planned migration | The SRM execution mode that gracefully shuts down primary site VMs, performs a final replication sync, then powers on VMs at the DR site with production IPs — used for scheduled maintenance or migrations |
| reprotect | The SRM operation that reverses the replication direction after a failover, making the DR site the new replication source so that changes made at DR are replicated back to the primary site before failback |
| failback | The process of returning workloads from the DR site back to the primary site after a failover; requires a Reprotect operation to reverse replication first |
| NSX stretched network | An NSX-T configuration where the same logical segment (same IP subnet) spans both primary and DR sites, allowing VMs to retain their IP addresses after failover without DNS changes |
| recovery plan | An SRM object that defines which VMs are protected, their startup order and priority groups, network mappings, and any pre/post-power-on scripts — the unit of execution for both DR tests and failovers |
| HA admission control | vCenter HA mechanism that reserves cluster capacity for VM restarts after a host failure; the DR site cluster's effective capacity after HA reservation must be checked before failover to confirm it can host all failed-over VMs |

---

## See also

- [SRM — Operations](../../srm/operations/)
- [vSphere Replication — Operations](../../vsphere-replication/operations/)
- [Scenarios — SRM RPO Violation](srm-replication-lag-rpo-violation/)
