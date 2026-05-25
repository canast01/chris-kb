# SRM — How It Works

## Site Topology

SRM operates across two paired sites: a **protected site** (production) and a **recovery site** (DR). Each site requires:

- vCenter Server
- SRM Server (Windows-based installer pre-8.x, OVA appliance from 8.x+)
- SRM Server registers as a vCenter extension and appears under **Site Recovery** in the vSphere Client

The two SRM Servers form a **site pair**. Communication between them uses TCP 443 and TCP 9086. The pairing is authenticated via certificate thumbprint exchange — each site must trust the other's SSL certificate.

```text
Protected Site                        Recovery Site
┌─────────────────────┐               ┌─────────────────────┐
│  vCenter Server     │◄──── TCP 443 ─►│  vCenter Server     │
│  SRM Server         │◄──── TCP 9086 ─►│  SRM Server         │
│  ESXi Hosts         │               │  ESXi Hosts         │
│  Production VMs     │               │  Placeholder VMs    │
│  Storage Array A    │               │  Storage Array B    │
└─────────────────────┘               └─────────────────────┘
         │                                      │
         └──── Replication (ABR or VR) ─────────┘
```

---

## Replication Methods

| Attribute | Array-Based Replication (ABR) | vSphere Replication (VR) |
|---|---|---|
| RPO minimum | Depends on array (typically 0–15 min) | 5 minutes |
| Granularity | Entire LUN / volume | Per individual VM |
| Cost | Requires storage array replication license | Included with most vSphere editions |
| SRA required | Yes — vendor-specific SRA | No |
| Snapshot consistency | Array consistency groups | VM-level quiescing (VMware Tools) |
| Network bandwidth | Handled by array fabric | Uses VMkernel / management network |
| Change tracking | Block-level via array | vSphere Changed Block Tracking (CBT) |
| Recovery site storage | Must be same array vendor (usually) | Any datastore visible to recovery ESXi |
| Multi-VM consistency | Consistency groups (array-coordinated) | Independent per VM (no cross-VM atomicity) |

### ABR Mechanism

1. Array at protected site replicates blocks to array at recovery site asynchronously (or synchronously for RPO=0).
2. At recovery site, replicated volumes are presented to ESXi hosts as read-only.
3. SRA queries the array to discover which VMs live on replicated datastores.
4. On failover, SRA issues commands to the array to perform a storage failover (promote snapshot, break replication, mount writable).

### vSphere Replication Mechanism

1. VR filter (installed on ESXi kernel via VIB) intercepts writes to VMDK.
2. Changed blocks are sent to the VR appliance at the recovery site over TCP 31031 (VAMI) / TCP 44046 (replication data).
3. VR appliance writes received blocks to a staging area on the recovery site datastore.
4. At failover, SRM instructs VR to finalize the disk copy (apply any in-flight changes).

---

## Protection Group Types

### ABR Protection Group

- Groups VMs that reside on a replicated LUN/volume.
- All VMs on the same array replication group are included together — you cannot split a consistency group across protection groups.
- SRM automatically discovers VMs on replicated datastores via SRA.
- If a VM spans multiple datastores, all datastores must be included in the same replication group.

### vSphere Replication Protection Group (Individual VM)

- Each VM is independently replicated.
- You configure replication per VM — different RPOs per VM are valid.
- Protection group can contain any mix of VMs regardless of datastore.
- No storage-level consistency — if you need cross-VM consistency, coordinate with application quiescing or use ABR.

### Datastore Group (VR-based)

- Available when using vSAN stretched cluster — not applicable in standard two-site SRM.

---

## Protection Group States

| State | Meaning |
|---|---|
| OK | All VMs protected, RPO met, placeholder VMs exist |
| Warning | One or more VMs approaching RPO threshold |
| Error | RPO violated, replication stopped, or SRA unreachable |
| Not Configured | VMs exist on replicated datastore but not yet added to a group |

---

## Recovery Plan Structure

A Recovery Plan defines the exact steps SRM executes during failover. One Recovery Plan can reference multiple Protection Groups.

### Recovery Plan Components

```text
Recovery Plan
├── Protection Groups (one or more)
├── Priority Groups (1–5, executed sequentially)
│   ├── Priority 1 — infrastructure VMs (DNS, AD, DB)
│   ├── Priority 2 — application servers
│   ├── Priority 3 — web/frontend
│   └── Priority 5 — non-critical / batch
├── Steps (per VM within a priority group)
│   ├── Pre-power-on steps (run command, send message)
│   ├── Power on VM
│   └── Post-power-on steps (run command, wait for heartbeat)
├── Network Mappings (map protected site port groups → recovery site port groups)
├── IP Customization (static re-IP rules per VM or subnet)
└── Dependencies (optionally wait for another plan to complete first)
```

### Priority Groups

- VMs in **Priority 1** power on first. SRM waits for them to complete before moving to Priority 2.
- Within a priority group, VMs start concurrently (subject to host resource limits).
- Maximum of 5 priority groups. If you need finer ordering, use pre/post steps with `Wait for heartbeat` or custom scripts.
- Recovery Plan steps within a VM's sequence:
  1. Suspend or shut down VM at protected site (planned migration only)
  2. Storage operations (SRA: promote LUN / VR: finalize disk)
  3. Configure network (apply IP customization)
  4. Pre-power-on commands (optional)
  5. Power on VM
  6. Post-power-on commands (optional, typically wait for VM tools heartbeat)

### IP Customization

Two approaches:

**Subnet-level mapping** — define a source subnet and a target subnet. SRM translates any static IP in the source range to the corresponding address in the target range.

```text
Source: 10.10.0.0/24  →  Target: 10.20.0.0/24
VM at 10.10.0.50       →  Recovers at 10.20.0.50
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
