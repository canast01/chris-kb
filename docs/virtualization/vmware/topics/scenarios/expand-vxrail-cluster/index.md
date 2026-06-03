# Expand VxRail Cluster (Add Node)

<div class="kb-summary">
Adding a node to a VxRail cluster is done exclusively through VxRail Manager — never manually
through vCenter. VxRail Manager validates firmware, enforces the bundle version, and orchestrates
the full join sequence: network configuration, vSAN disk claim, NSX transport node registration,
and vCenter cluster join. Bypassing VxRail Manager causes firmware mismatches that break future
LCM upgrades and voids the support configuration.
</div>

```text
┌──────────────────────────── Expand VxRail Cluster (Add Node) — Procedure Flow ────────────────────────────────────┐
│                                                                                                       │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  START: Rack and cable new node — assign iDRAC IP via DCUI, confirm iDRAC reachable on mgmt network       ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 1 — Network pre-checks: verify mgmt, vMotion, vSAN VLANs reachable; DNS A+PTR records pre-created   ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 2 — VxRail Manager → Cluster Expansion → Discover Nodes: new node appears on management network     ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 3 — Run expansion wizard: supply mgmt IP, vMotion IP, vSAN IP, FQDN hostname                        ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                              ┌───────────────────────┼───────────────────────┐                        │
│                              ▼                       ▼                       ▼                        │
│          ┌─────────────────────────┐   ┌─────────────────────────┐  ┌─────────────────────────┐       │
│          │  Firmware update        │   │  Join vCenter cluster,  │  │  NSX transport node     │       │
│          │  (if bundle mismatch)   │   │  VMkernel config, disks │  │  configuration          │       │
│          └────────────┬────────────┘   └────────────┬────────────┘  └────────────┬────────────┘       │
│                       └────────────────────────────┬─┘──────────────────────────┘                     │
│                                                    ▼                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 4 — vSAN rebalance: monitor resyncing objects until 0 bytes remain; validate in OMIVV               ││
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| VxRail Manager | Expansion wizard — the only supported entry point for adding a node |
| vCenter Server | Receives the new node into the cluster; hosts the OMIVV plugin |
| vSAN | Automatically claims disks on the new node; rebalances data post-expansion |
| NSX | Transport node registration performed by VxRail Manager during expansion |
| iDRAC | Out-of-band management; node readiness verification before expansion |
| OMIVV (OpenManage Integration) | Hardware inventory and health visibility post-join |

---

## 1. Hardware Pre-Checks and iDRAC

Rack and cable the new node following the same physical configuration as existing nodes in the
cluster (same switch ports, same VLAN assignments, same cable types). Assign the iDRAC IP address
via the DCUI before doing anything else — VxRail Manager discovery uses the management network,
but iDRAC gives out-of-band visibility throughout the expansion.

```bash
# Confirm iDRAC is reachable on the management network
ping <new-node-idrac-ip>

# iDRAC web UI should be accessible at https://<idrac-ip>
# Default credentials: root / Calvin — change immediately after expansion
```

Confirm iDRAC shows the node in a healthy hardware state: all PSUs present, no drive faults, BIOS
POST completed successfully. Do not proceed if iDRAC shows hardware faults.

---

## 2. Network Pre-Checks

The new node must have layer-2 connectivity on all required VLANs before VxRail Manager can
discover it. VxRail Manager will not proceed with expansion if the node cannot reach the
management network broadcast domain.

| Network | MTU requirement | Verification |
|---|---|---|
| Management | 1500 | ping from jump host to management network gateway |
| vMotion | 1500 or 9000 (match cluster) | check switch port VLAN assignment |
| vSAN | 9000 (jumbo frames required) | MTU configured on switch port and VDS |

DNS records must be created before running the expansion wizard. VxRail Manager validates the
FQDN during the wizard and will fail if the A record or PTR record is missing.

```bash
# Verify DNS from the VxRail Manager VM or jump host
nslookup new-node-hostname.domain.local
nslookup <new-node-management-ip>
```

Both directions must resolve correctly before starting the wizard.

---

## 3. Discover the New Node in VxRail Manager

VxRail Manager → **Cluster Expansion** → **Discover Nodes**.

VxRail Manager scans the management network broadcast domain for unconfigured VxRail nodes — nodes
that have factory ESXi installed but have not yet been configured or joined a cluster. The new node
must appear in the discovery list.

If the node does not appear:

| Symptom | Likely cause |
|---|---|
| Node not visible in discovery | Management VLAN not reaching the node |
| Node appears but shows error | Factory ESXi boot failed — check iDRAC for POST errors |
| Duplicate node found | Node was previously partially configured — factory reset required |

---

## 4. Run the Expansion Wizard

Select the discovered node and click **Next** to start the expansion wizard. Provide:

- **Management IP** — new node's management VMkernel IP
- **vMotion IP** — new node's vMotion VMkernel IP
- **vSAN IP** — new node's vSAN VMkernel IP
- **Hostname** — FQDN that matches the pre-created DNS records

VxRail Manager runs a pre-check validation before committing. All checks must pass (green) before
expansion begins. Common pre-check failures:

| Pre-check failure | Resolution |
|---|---|
| DNS validation failed | Create or fix A+PTR records |
| Network connectivity failed | Check VLAN assignment on switch port |
| Firmware bundle mismatch | VxRail Manager will auto-update — allow extra time |
| Existing cluster health not green | Resolve vSAN or host issues before expanding |

---

## 5. Firmware Bundle Check and Update

VxRail Manager compares the new node's firmware (BIOS, HBA, NIC, iDRAC) and ESXi version against
the cluster's current LCM bundle. If any component is below the cluster bundle version, VxRail
Manager automatically stages and applies the firmware before joining the node. This is not
optional — it runs automatically.

This step adds significant time: a full firmware update pass typically takes 30-60 minutes. The
node will reboot during firmware updates. This is expected and requires no intervention.

Do not power off the node or disconnect cables during this phase.

---

## 6. Expansion Runs Automatically

Once the wizard is confirmed, VxRail Manager orchestrates the full expansion sequence without
further input:

1. Applies firmware (if required)
2. Configures ESXi: hostname, management IP, VMkernel ports
3. Joins the node to the vCenter cluster
4. Deploys the HA agent on the new node
5. Configures the NSX transport node (if NSX is deployed on the cluster)
6. Claims vSAN disks and creates a disk group on the new node

Monitor progress in VxRail Manager → **Cluster Expansion** → **Status**. The full expansion
typically takes 45-90 minutes from wizard confirmation to completion.

---

## 7. vSAN Rebalance Monitoring

After the new node joins and its disks are claimed, vSAN automatically rebalances data across all
nodes to distribute the load across the new capacity. This is a background operation and does not
require manual triggering.

Monitor the rebalance: vCenter → **vSAN** → **Monitor** → **Resyncing Objects**.

```powershell
# Check resyncing state via PowerCLI
Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"

# Verify the new host's disk group is present and healthy
Get-VMHost "new-node.domain.local" | Get-VsanDiskGroup
```

Do not put any other host in maintenance mode while rebalancing is in progress. A second host in
maintenance mode during rebalance can reduce vSAN redundancy below the policy requirement.

---

## 8. OMIVV Hardware Inventory Verification

After expansion completes, OMIVV should automatically inventory the new node and add it to the
hardware overview. Allow 10-15 minutes for the automatic discovery to complete.

Verify: vCenter → **Menu** → **Dell** → **OpenManage Integration for VMware vCenter** →
**Infrastructure Overview** → confirm the new node appears.

If the node does not appear automatically: OMIVV → **Settings** → **Discovery** → **Run Discovery**
to force an immediate inventory scan.

```powershell
# Confirm new host appears in vCenter cluster
Get-Cluster "vxrail-cluster" | Get-VMHost | Select Name, ConnectionState, Version

# Confirm vSAN disk group on new node
Get-VMHost "new-node.domain.local" | Get-VsanDiskGroup
```

---

## Post-Task Validation

| Check | Expected Result |
|---|---|
| New node in vCenter cluster | Connected, PoweredOn |
| vSAN disk group on new node | All disks claimed, disk group healthy |
| vSAN rebalance complete | 0 bytes resyncing |
| NSX transport node status | Configured / Success (green) |
| OMIVV hardware inventory | New node visible in Infrastructure Overview |
| iDRAC default password changed | Not root / Calvin |
| LCM bundle version | New node matches cluster bundle version |

---

## Common Mistakes

- **Adding the node to vCenter directly instead of through VxRail Manager.** The node joins the
  cluster but firmware and driver versions are not validated. Future VxRail Manager LCM upgrades
  will fail because the node is outside the managed bundle.
- **Not pre-creating DNS A and PTR records.** The expansion wizard validates the FQDN before
  committing. A missing DNS record causes wizard failure after the firmware update phase has already
  run, resulting in a partially configured node.
- **Checking vSAN rebalance before expansion fully completes.** The resyncing objects count shows
  partial data during expansion. Wait for VxRail Manager to report expansion complete before
  interpreting vSAN resync metrics.
- **Leaving iDRAC on default credentials.** The default root/Calvin credential is publicly known.
  Change it immediately after expansion.

---

## Related Scenarios

- Add ESXi Host to Cluster
- Host Maintenance and Patching
- VxRail LCM Upgrade Failure
- vSAN Disk or Component Failure
