# DR Test and Planned Failover

<div class="kb-summary">
A DR test proves recovery works without impacting production — replicated VMs boot in an isolated
bubble network at the DR site while production continues running. A planned failover is a real
migration with graceful shutdown at the primary site, used for site maintenance or data centre
migrations. Both operations are orchestrated by SRM, but they differ significantly in scope,
risk, and required preparation. This scenario covers both paths and the common mistakes that cause
them to fail.
</div>

```text
┌──────────────────────────────── DR Test vs Planned Failover — Procedure Paths ─────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: SRM Recovery Plan selected — choose execution type                                               ││
│   └────────────────────────────────────┬─────────────────────────────────────────────────────────────────────┘│
│                                        │                                                              │
│                 ┌──────────────────────┴──────────────────────┐                                       │
│                 ▼                                             ▼                                       │
│   ┌──────────────────────────────┐             ┌──────────────────────────────┐                       │
│   │  DR TEST (non-disruptive)    │             │  PLANNED FAILOVER            │                       │
│   │  Production continues        │             │  Graceful shutdown at primary│                       │
│   └──────────────┬───────────────┘             └──────────────┬───────────────┘                       │
│                  │                                             │                                      │
│                  ▼                                             ▼                                      │
│   ┌──────────────────────────────┐             ┌──────────────────────────────┐                       │
│   │  SRM powers on VM replicas   │             │  Pre-flight: check DR site   │                       │
│   │  in isolated bubble network  │             │  capacity and replication RPO│                       │
│   └──────────────┬───────────────┘             └──────────────┬───────────────┘                       │
│                  │                                             │                                      │
│                  ▼                                             ▼                                      │
│   ┌──────────────────────────────┐             ┌──────────────────────────────┐                       │
│   │  Application smoke test on   │             │  SRM shuts down primary VMs  │                       │
│   │  isolated VMs at DR site     │             │  syncs final blocks → powers  │                      │
│   └──────────────┬───────────────┘             │  on at DR with production IPs│                       │
│                  │                             └──────────────┬───────────────┘                       │
│                  ▼                                             │                                      │
│   ┌──────────────────────────────┐                            ▼                                       │
│   │  Cleanup: SRM powers off     │             ┌──────────────────────────────┐                       │
│   │  test VMs, removes test net  │             │  Validate: VMs up, DNS, NSX  │                       │
│   │  Production unaffected       │             │  segments, Aria Ops alerts   │                       │
│   └──────────────────────────────┘             └──────────────────────────────┘                       │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

A DR test is designed to be run regularly (at minimum annually, often quarterly) without any impact
to production. SRM boots replicated VM snapshots in an isolated test network at the DR site.
Production VMs at the primary site continue running throughout.

### 1. Verify Replication Health Before the Test

```powershell
# Confirm all VMs in the recovery plan are at RPO — must show OK, not Warning or Error
# SRM → Site Recovery → Replication → review status column for all protected VMs
```

From the SRM UI: **Site Recovery → Replication**. Every VM in the recovery plan must show status
**OK** and the last sync time must be within the configured RPO window. A VM showing **RPO
Violated** or **Not Responding** will fail to power on during the test.

### 2. Run the DR Test

SRM → **Recovery Plans** → select the plan → **Test**.

SRM creates a temporary test network (isolated — no routing to production) and powers on the
replicated VM snapshots at the DR site. The test network uses a separate IP range or a bubble
network with NAT so there are no IP conflicts with production.

### 3. Validate Application Functionality

Log into each test VM and run application smoke tests:
- Can the application start and respond?
- Can it reach its database (if also in the recovery plan)?
- Are application-layer health checks passing?

Document any failures — the DR test is only valuable if results are recorded and acted on.

### 4. Clean Up After the Test

SRM → **Recovery Plans** → select the plan → **Cleanup**.

SRM powers off all test VMs and removes the isolated test network. The production environment
is completely unaffected throughout. **Do not skip the cleanup step.** If test VMs are left
running, they consume DR site compute and storage capacity, and they may interfere with a real
failover if one is needed before the next test.

---

## Planned Failover — Graceful Production Migration to DR Site

A planned failover gracefully migrates all protected workloads from the primary to the DR site.
The primary site is shut down cleanly, the final changed blocks are synced, and the VMs power on
at the DR site with their production IP addresses. Data loss is typically zero if replication
is current at the time of failover.

Use planned failover for: scheduled site maintenance, data centre migrations, or hardware refresh
at the primary site.

### 1. Pre-Failover Checks

```powershell
# Check replication status — all VMs must be at RPO before initiating planned failover
# SRM → Replication → confirm all statuses show OK

# Check DR site cluster has sufficient capacity for all failed-over VMs
Get-Cluster "DR-Cluster" | Select Name,
  @{N="EffectiveCPUMHz";E={($_ | Get-View).Summary.EffectiveCpu}},
  @{N="EffectiveMemMB";E={($_ | Get-View).Summary.EffectiveMemory}}
```

Confirm the DR site cluster has sufficient effective CPU and memory headroom to run all VMs in
the recovery plan simultaneously. Factor in the DR cluster's own HA admission control reservation.

### 2. Initiate Planned Failover

SRM → **Recovery Plans** → select the plan → **Run** → select **Planned Migration**.

What SRM does during a planned migration (in order):
1. Quiesces and powers off primary site VMs gracefully (in the order defined by the recovery plan)
2. Triggers a final vSphere Replication sync to capture any remaining changed blocks
3. Powers on DR site VMs in the order defined by the recovery plan (priority groups)
4. Applies network customisation: maps primary site networks to DR site networks using the
   Network Mapping configured in SRM

Unlike an emergency failover (which skips the graceful shutdown and accepts potential data loss),
planned migration waits for the final sync to complete before powering on DR VMs.

### 3. NSX Network Configuration at the DR Site

If primary site VMs use NSX segments, the DR site NSX Manager must have the matching segments
configured before failover. SRM integrates with NSX to apply these mappings, but the segments
themselves must already exist.

```bash
# Verify required segments exist at DR site NSX Manager before failover
# NSX Manager (DR site) → Networking → Segments → confirm all required segments are present
# SRM → Site Recovery → Network Mappings → confirm all primary segments have a DR mapping
```

If a segment mapping is missing, VMs power on at the DR site but their NICs connect to nothing —
they have no network connectivity.

### 4. DNS After Planned Failover

SRM maps IP addresses from the primary network to the DR network. If VMs retain their original
production IP addresses (same subnet exists at DR — stretched L2 or NSX-T), DNS records do not
need to change.

If IP addresses change at DR (different subnet):

```bash
# Update DNS A records to point to the new DR IP for each application FQDN
# If using Active Directory DNS:
# Run this on a DC at the DR site after VMs are up:
# dnscmd /recorddelete <zone> <hostname> A <old-IP>
# dnscmd /recordadd <zone> <hostname> A <new-DR-IP>

# Verify resolution from a DR site client after DNS update
nslookup app.domain.local <DR-DNS-server-IP>
```

### 5. Post-Failover Validation

```powershell
# Verify all VMs in the recovery plan are powered on at the DR site
Get-Cluster "DR-Cluster" | Get-VM |
  Where-Object {$_.PowerState -ne "PoweredOn"} |
  Select Name, PowerState
```

Connect Aria Operations to the DR site vCenter and run a manual data collection to populate the
dashboard with the DR site VMs. Check for any critical alerts.

### 6. Failback to Primary Site

When the primary site is ready to resume (maintenance complete, hardware replaced), reverse the
replication and run another planned migration in the opposite direction.

SRM supports **reverse replication**: the DR site becomes the new source, replicating changes
back to the primary site. This ensures zero data loss on failback.

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

## Common Mistakes

- **Not cleaning up after a DR test.** Test VMs remain running at the DR site, consuming capacity
  and potentially conflicting with a real failover. Always run the SRM Cleanup step.
- **Failing over without checking DR site capacity.** If the DR cluster cannot host all failed-over
  VMs simultaneously, VMs fail to power on or get constrained. Check effective capacity before
  initiating failover.
- **Missing NSX segment configuration at the DR site.** Segments must exist and be mapped in SRM's
  Network Mappings before failover. VMs power on with disconnected NICs if the mapping is absent.
- **Initiating failback to a site still under maintenance.** The primary site must be fully
  operational before failback. A return to a degraded site causes an immediate second failover
  and potential data loss.
- **Skipping reprotect after planned failover.** Without running Reprotect, replication does not
  reverse. If a failure then occurs at the DR site (now the production site), there is no
  replicated copy at the primary site to recover from.

---

## Related Scenarios

- SRM Replication Lag and RPO Violation
- Certificate Expiry and Rotation
- Aria Ops Alert Storm
