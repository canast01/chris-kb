# SRM Replication Lag / RPO Violation

<div class="kb-summary">
An RPO violation means replicated VMs are falling behind their target recovery point — the DR copy
is more than X minutes behind the production VM. If the production site fails during an RPO
violation, more data will be lost than your SLA allows. This scenario covers identifying which VMs
are lagging, diagnosing the cause (bandwidth, change rate, or appliance health), and restoring
replication to within RPO before verifying with an SRM test recovery.
</div>

```text
┌─────────────────────────── SRM Replication Lag / RPO Violation — Investigation Flow ───────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: SRM alert — RPO Exceeded on one or more VMs, or Aria Operations fires RPO warning alert     ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                   ┌────────────────────────────┼────────────────────────────┐                         │
│                   ▼                            ▼                            ▼                         │
│   ┌───────────────────────────┐   ┌───────────────────────────┐  ┌───────────────────────────┐        │
│   │  One or a few VMs lagging │   │  Many VMs lagging across  │  │  Replication stopped      │        │
│   │  → high change rate on    │   │  multiple hosts           │  │  entirely on some VMs     │        │
│   │    specific VMs           │   │  → inter-site link issue  │  │  → vSR appliance health   │        │
│   └────────────┬──────────────┘   └────────────┬──────────────┘  └────────────┬──────────────┘        │
│                │                               │                               │                      │
│                └───────────────────────────────┼───────────────────────────────┘                      │
│                                                ▼                                                      │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Check vSR appliance health → Check inter-site bandwidth → Check VM change rate                     ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                   ┌────────────────────────────┼────────────────────────────┐                         │
│                   ▼                            ▼                            ▼                         │
│   ┌───────────────────────────┐   ┌───────────────────────────┐  ┌───────────────────────────┐        │
│   │  Appliance fault          │   │  Bandwidth exhausted      │  │  VM change rate too high  │        │
│   │  → redeploy or restart    │   │  → throttle, compress,    │  │  → enable compression,   │         │
│   │    vSR appliance          │   │    or expand link         │  │    or increase RPO target │        │
│   └───────────────────────────┘   └───────────────────────────┘  └───────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| VMware Site Recovery Manager (SRM) | Recovery plan orchestration; RPO monitoring; test recovery execution |
| vSphere Replication (vSR) | Changed-block replication between production and DR vCenter; RPO tracking |
| vCenter (both sites) | VM inventory, vSR appliance registration, host and datastore health |
| Aria Operations | RPO alert generation; capacity trending on DR datastores |
| NSX | Stretched overlay segments — management connectivity between sites must be healthy |

---

## 1. Identify Which VMs Are Lagging

vCenter (production site) → **Site Recovery** → **Replication** → select **vSphere Replication** →
**Outgoing** tab. Sort by **RPO Status** or **Last Sync**.

| RPO status | Meaning | Priority |
|---|---|---|
| Met | Replication within RPO window | Normal — no action |
| Warning | Within 20% of RPO limit | Monitor; check bandwidth |
| Exceeded | Replication behind RPO window | Investigate now |
| Error | Replication stopped | Urgent — check vSR appliance |

Note the VM names and which ESXi hosts they run on. If all lagging VMs are on the same host,
the problem may be host-level (NIC saturation, VMkernel routing issue). If lagging VMs are
spread across hosts, the inter-site link is likely the cause.

---

## 2. Check vSphere Replication Appliance Health

Both the production site vSR appliance and the DR site vSR appliance must be healthy.

vCenter → **Site Recovery** → **Configure** → **vSphere Replication Servers**.

All appliances should show a green status. If an appliance shows a fault:

```bash
# SSH to vSR appliance — check service status
systemctl status vmware-hbrsrv
systemctl status vmware-hbr-cloudagent

# Check replication server logs for errors
tail -100 /var/log/vmware/hbr/hbrServer.log | grep -i error
```

A common vSR appliance failure is certificate mismatch after a vCenter SSL certificate renewal.
If the appliance shows a certificate error, re-register the vSR appliance with the vCenter:
vCenter → Site Recovery → Configure → vSphere Replication Servers → select appliance →
**Reconnect**.

---

## 3. Check Inter-Site Replication Network

vSphere Replication traffic flows from the production ESXi host (on the VMkernel interface
tagged for vSphere Replication) to the vSR appliance at the DR site. Traffic volume equals
the changed-block rate of all replicating VMs combined.

```bash
# From ESXi host — check which VMkernel is used for vSphere Replication
esxcli network ip interface list | grep -A5 "vSphereReplication"

# Check NIC traffic on the replication VMkernel's physical NIC
esxcli network nic stats get -n <vmnic-name>
```

If the replication NIC is at or near 100% utilisation, the inter-site link is saturated.
Options:
- Enable **network compression** on vSphere Replication (reduces bandwidth by 20–40%)
- Throttle specific VMs to prioritise the most critical (highest RPO tolerance VMs can wait)
- Request a bandwidth increase from the network team for the inter-site circuit

---

## 4. Check VM Change Rate

High write VMs — databases, transaction logs, large file servers — can outrun the available
replication bandwidth. vSphere Replication tracks the current change rate per VM.

vCenter → Site Recovery → Replication → select a lagging VM → **Details** →
**Current replication rate** vs **Average replication rate**.

If the current rate is significantly above the average: a recent backup job, database log
flush, or application burst is the cause. If elevated rates are persistent: the VM needs
a higher RPO target or dedicated bandwidth.

```bash
# Check replication rate from vSR appliance
# vSR REST API — get replication instance details for a specific VM
curl -sk -u admin:<password> \
  "https://vsr-appliance.domain.local/api/replication/instances" \
  | python3 -m json.tool | grep -A10 "vm-name"
```

---

## 5. Enable Compression or Adjust Throttle Settings

For VMs with persistently high change rates:

1. vCenter → Site Recovery → Replication → select VM → **Edit**
2. Enable **Network Compression** — compresses changed blocks before transmitting
3. Or set a **Bandwidth Throttle** (Mbps limit per VM) — lower-priority VMs get throttled,
   freeing bandwidth for critical replicating VMs

For VMs where the RPO target is genuinely unachievable given the change rate and link capacity:
adjust the RPO target to a realistic value (e.g., from 15 minutes to 30 minutes). This is a
formal change and requires SLA review.

---

## 6. Force a Manual Sync to Catch Up

If a specific VM has a large accumulated lag that needs to catch up quickly:

vCenter → Site Recovery → Replication → select the lagging VM → **Sync Now**.

This forces an immediate full changed-block sync, prioritised over the scheduled replication
cycle. Monitor the status until it returns to **Met** state.

```bash
# Verify replication status via vSR REST API after manual sync
curl -sk -u admin:<password> \
  "https://vsr-appliance.domain.local/api/replication/instances?state=REPLICATING" \
  | python3 -m json.tool | grep -E '"vmName"|"rpoStatus"|"rpoViolation"'
```

---

## 7. Verify NSX Inter-Site Management Connectivity

If VMs use NSX overlay segments stretched between sites, the NSX management plane must also
have connectivity between the production and DR vCenter. A broken NSX management connection
does not stop replication directly, but it prevents SRM from reconfiguring network mappings
during a real failover.

NSX Manager → **System** → **Fabric** → check that both site's transport nodes are visible
and green. If the DR site NSX Manager is isolated, resolve the management plane connectivity
issue before running any SRM test or real failover.

---

## 8. Run an SRM Test Recovery to Validate RPO Is Met

After resolving the replication lag, validate recovery with a non-disruptive SRM test:

SRM → **Recovery Plans** → select the plan → **Test**.

SRM powers on the DR replicas in an **isolated network** (bubble network) at the DR site.
No production traffic is affected. Verify:
- All VMs in the plan power on successfully
- RPO status is **Met** for all VMs before the test
- Application connectivity (web, database) is verified inside the test bubble

After validation: SRM → Recovery Plan → **Cleanup Test**. This powers down the test replicas
and removes the test network. **Always run Cleanup** — leaving test replicas running consumes
DR site resources and can interfere with real replication.

---

## Common Mistakes

- **Confusing RTO and RPO.** RPO (Recovery Point Objective) is the maximum acceptable data
  loss — how old the DR copy can be. RTO (Recovery Time Objective) is the maximum acceptable
  downtime — how long recovery takes. vSphere Replication manages RPO. SRM recovery plan
  execution time determines whether RTO is met.
- **Not reserving inter-site bandwidth for replication.** Backup jobs, log shipping, and ad hoc
  file transfers compete for the same inter-site link as vSphere Replication. Without a QoS
  policy or dedicated bandwidth allocation, replication loses during peak traffic and RPO is
  violated.
- **Forgetting to clean up after SRM test recovery.** Test replicas left running consume DR site
  compute and datastore resources. If enough tests are left uncleaned, the DR site runs out of
  capacity for a real failover.
- **Re-configuring replication without checking the DR datastore capacity.** If the DR datastore
  is near full, vSphere Replication cannot write replicated data. Always verify DR site capacity
  before troubleshooting replication lag — the lag may be caused by a full DR datastore, not the
  inter-site network.

---

## Related Scenarios

- [Datastore Full / Capacity Alarm](../datastore-full-capacity-alarm/index.md) — A full DR datastore is a hidden cause of replication lag; vSphere Replication silently queues when the DR datastore cannot accept writes.
- [NSX Edge Failure / BGP Down](../nsx-edge-failure-bgp-down/index.md) — A BGP failure at the DR site prevents SRM from establishing network connectivity for recovered VMs.
- [vSAN Stretched Cluster Split-Brain](../vsan-stretched-cluster-split-brain/index.md) — A site partition that triggers stretched cluster split-brain also disrupts vSphere Replication traffic flowing over the same inter-site link.
