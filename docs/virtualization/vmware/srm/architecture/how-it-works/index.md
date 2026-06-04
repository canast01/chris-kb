# SRM — How It Works (VMware Platform)


<div class="kb-summary">
How It Works (VMware Platform) reference covering Site Topology, Test Failover Workflow, Planned Migration, Disaster Recovery Failover, Failback Process and 2 more sections.
</div>

## Site Topology

SRM operates across two paired sites: a **protected site** (production) and a **recovery site** (DR). Each site requires:

- vCenter Server
- SRM Server (Windows-based installer pre-8.x, OVA appliance from 8.x+)
- SRM Server registers as a vCenter extension and appears under **Site Recovery** in the vSphere Client

The two SRM Servers form a **site pair**. Communication between them uses TCP 443 and TCP 9086. The pairing is authenticated via certificate thumbprint exchange — each site must trust the other's SSL certificate.

Protected Site                        Recovery Site
```text
┌────────────────────────────────────── VMware SRM — How It Works ──────────────────────────────────────┐
│                                                                                                       │
│  SRM orchestrates VM failover between a protected site and recovery site using                        │
│  replication (vSphere Replication or array-based) and recovery plans.                                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Protected Site                │  │                Recovery Site                │   │
│   │             SRM Server: primary              │  │             SRM Server: recovery            │   │
│   │           VMs: production running            │  │            Replicas: powered off            │   │
│   │           Replication: vSR or ABR            │  │           Recovery plan: failover           │   │
│   │           Site pair: bidirectional           │  │          Test: no production impact         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Site pair connects two SRM servers; recovery plans define failover order and steps.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Recovery Plan Execution            │  │              Replication Types              │   │
│   │        Test: isolated bubble network         │  │           vSR: vSphere Replication          │   │
│   │          Planned: graceful failover          │  │           ABR: array-based SAN rep          │   │
│   │          Disaster: forced failover           │  │              RPO: vSR 5min–24h              │   │
│   │          Failback: reprotect + run           │  │              ABR: near-zero RPO             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SRM Servers run as Windows VMs on vCenter; replication traffic uses dedicated network                │
│  or SAN replication; sites connected by WAN/MPLS/dark fibre.                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM Server    = Windows VM; Horizon-like broker for DR orchestration                                 │
│  Site pair     = bidirectional connection between two SRM servers                                     │
│  Recovery plan = ordered list of VMs + steps for failover                                             │
│  vSR           = vSphere Replication; host-based async replication                                    │
│  ABR           = Array-Based Replication; SAN-level sync/async                                        │
│  RPO           = Recovery Point Objective; max data age at recovery                                   │
│  Test failover = runs in bubble network; does not impact production                                   │
│  Planned failover= graceful; sync replication, then failover                                          │
│  Disaster failover= forced; uses last available replica state                                         │
│  Failback      = reprotect recovery site as new protected site                                        │
│  Bubble network= isolated test network; no production routing                                         │
│  Reprotect     = reverse replication direction after failover                                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌───────────────────────────────── VMware SRM — Recovery Orchestration ─────────────────────────────────┐
│                                                                                                       │
│  Protection groups bind VMs to replication; recovery plans orchestrate their failover order.          │
│  SRM has three execution modes: Test (bubble), Planned (graceful), Disaster (forced).                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │       Protection Group (what to protect)     │  │       Recovery Plan (how to fail over)      │   │
│   │   Links VMs to a replication group or LUN    │  │   Ordered VM list with priority groups 1–5  │   │
│   │   vSphere Replication: per-VM RPO 5 m – 24 h │  │   Priority group 1 powers on first          │   │
│   │   ABR: SRA links LUN or consistency group    │  │   Pre/post power-on custom commands per VM  │   │
│   │   One PG can contain many VMs                │  │   IP customisation per NIC per VM           │   │
│   │   PG state: Protected / Error / Unconfigured │  │   One plan can span multiple PGs            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Recovery Plan references Protection Groups; SRM validates all mappings before any execution runs.    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │       Execution Modes (three types)          │  │       Post-Recovery Operations              │   │
│   │   Test: bubble VLAN, snapshot, no impact     │  │   Re-protect: reverse replication direction │   │
│   │   Planned: graceful shutdown; RPO=0; power on│  │   vSR: reconfigure VR source/target sites  │    │
│   │   Disaster: forced; uses last sync point     │  │   ABR: SRA reverses the LUN replication     │   │
│   │   All modes: IP customisation + scripts      │  │   Failback: planned migration back to origin│   │
│   │   Test requires Cleanup before real failover │  │   Cycle: Recover → Re-protect → Failback    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SRM Server runs as a Windows VM (pre-8.x) or OVA appliance (8.x+) at each site; sites connected      │
│  via WAN/MPLS; replication uses dedicated SAN fabric or network; SRA is array vendor plugin.          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM Server        = DR orchestration broker; Windows VM or OVA; one per site                         │
│  Site pair         = bidirectional trust between two SRM servers; certificate-based auth              │
│  Protection group  = set of VMs bound to a replication group or LUN at the protected site             │
│  Recovery plan     = ordered VM failover script; priority groups, custom commands, IP mapping         │
│  SRA               = Storage Replication Adapter; array-specific plugin for ABR failover              │
│  vSR               = vSphere Replication; host-based async replication; RPO 5 min to 24 h             │
│  ABR               = Array-Based Replication; SAN-level replication; near-zero RPO                    │
│  RPO               = Recovery Point Objective; maximum accepted data age at the recovery site         │
│  Test failover     = non-disruptive; isolated bubble network; production VMs continue running         │
│  Planned failover  = graceful; protected VMs shut down cleanly; RPO=0 at cutover                      │
│  Disaster failover = forced; uses last received replica; no graceful shutdown of source VMs           │
│  Bubble network    = isolated port group with no uplink; test VMs cannot reach production             │
│  Re-protect        = reverse replication direction after failover; makes recovery site the new source │
│  Failback          = return VMs to original protected site after re-protect; uses planned failover    │
│  Placeholder VM    = lightweight inventory object at recovery site; represents the protected VM       │
│  IP customisation  = per-NIC IP/mask/gateway/DNS mapping applied at recovery site on power-on         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Per-VM customization** — define exact IP, netmask, gateway, DNS per NIC per VM. Used when target IPs don't follow a simple subnet mapping.

IP customization is applied using the Guest OS customization engine (VMware Tools required). If the VM does not have VMware Tools running, customization is skipped and the VM retains its protected-site IP (may cause routing issues at recovery site).

### Custom Command Steps

SRM can execute commands before or after powering on a VM:

- **Script (on recovery site)** — runs a command/script on the SRM Server or on a VM (via VMware Tools `RunProgram`).
- **Prompt** — pauses execution and waits for manual confirmation before proceeding. Used to gate critical steps.
- **Call an Alarm** — triggers a vCenter alarm.

---

## Test Failover Workflow

Test failover is non-disruptive: production VMs remain running. SRM powers on placeholder VMs in an isolated **bubble network**.

### Test Failover Steps

1. User initiates **Test** from the Recovery Plan in SRM UI.
2. SRM creates a **snapshot** of the replicated datastore at recovery site (ABR: writable snapshot / VR: point-in-time copy).
3. Placeholder VMs are reconfigured to use this test snapshot datastore (not the live replicated datastore).
4. SRM connects each test VM to an **isolated test network** (port group with no uplink, or a dedicated VLAN).
   - This prevents test VMs from impacting production by sending traffic on production networks.
5. IP customization runs on the test VMs (they get recovery-site IPs but are isolated).
6. VMs power on in priority order.
7. Custom steps (pre/post power-on commands) execute as configured.
8. Test result: pass / warning / error — each step logged with timestamp and outcome.

### Test Cleanup

After verifying the test:

1. Initiate **Cleanup** from the Recovery Plan.
2. SRM powers off test VMs.
3. Snapshots created for the test are deleted.
4. Placeholder VMs return to their pre-test state.
5. Recovery Plan returns to **Ready** state.

Test cleanup must complete before running a real failover or another test.

---

## Planned Migration

Used when both sites are operational (datacenter move, scheduled maintenance).

1. SRM shuts down protected VMs gracefully (respects VM tools shutdown).
2. Waits for final replication sync to complete — ensures RPO = 0.
3. VMs power on at recovery site using the final synced data.
4. IP customization is applied.
5. VMs are now running at recovery site — protected site VMs are removed from inventory.

Planned migration is fully reversible via **Failback** once you have re-protected (reversed replication).

---

## Disaster Recovery Failover

Used when the protected site is unavailable (power failure, network loss, site disaster).

1. Operator initiates **Run** (Recovery) from the Recovery Plan.
2. SRM assumes protected VMs are offline — no graceful shutdown.
3. For ABR: SRA promotes replicated LUN to writable (may involve accepting a crash-consistent snapshot).
4. For VR: VR appliance applies all received data up to the last sync point.
5. VMs power on at recovery site.
6. IP customization is applied.
7. Recovery Plan history logs all steps with outcome.

There is a **Force Recovery** option if SRM cannot reach the protected site SRM Server — this bypasses the normal handshake and proceeds unilaterally.

---

## Failback Process

Failback returns VMs from the recovery site to the protected site after a recovery. Requires:

1. Protected site is back online.
2. **Re-protect** the VMs — reverses replication direction (recovery site → protected site).
   - For VR: configure VR with new source = recovery site, new target = protected site.
   - For ABR: SRA reverses the replication pair on the array.
3. Create a new Recovery Plan (or use the original plan after re-pairing) in the opposite direction.
4. Run **Planned Migration** or **DR** back to the original protected site.
5. Re-protect again in the original direction to restore normal operations.

Full failback cycle: `Recover → Re-protect → Failback → Re-protect`

---

## Placeholder VMs

Placeholder VMs are lightweight VM objects at the recovery site that represent protected VMs. They exist so that:

- The recovery site vCenter knows about the VM before failover.
- Network mappings and IP customization can be pre-configured and validated.
- The Recovery Plan can reference the VMs for power-on ordering and dependencies.
- Alarms and monitoring at the recovery site can be configured.

### What a Placeholder VM Contains

- VM configuration file (`.vmx`) with hardware configuration matching the protected VM.
- No active VMDKs — disks are pointed at the replicated datastore (not yet promoted writable).
- Not powered on — exists only in vCenter inventory in a suspended/unregistered state.
- Network adapters assigned to recovery-site port groups (as per network mappings).

### Placeholder VM Problems

If a placeholder VM is missing or corrupt, SRM re-creates it automatically on the next **Configure All** or protection group reconfigure. If a placeholder VM shows errors, delete it manually from the recovery site vCenter and trigger a reconfigure on the Protection Group.

---

## SRM Inventory Mappings

Before VMs can recover, SRM requires:

| Mapping Type | Description |
|---|---|
| Network mappings | Map protected-site port group/vDS → recovery-site port group/vDS |
| Folder mappings | Map VM folders at protected site → folders at recovery site |
| Resource mappings | Map clusters/resource pools at protected site → at recovery site |
| Storage policy mappings | Map VM storage policies (optional, affects datastore placement at recovery) |

Network and folder mappings are bidirectional — configuring them in one direction auto-populates the reverse. Resource mappings define where recovered VMs are placed in the vCenter hierarchy.
