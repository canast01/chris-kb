---
tags:
  - scenarios
  - srm
  - vmware
---
# SRM Replication Lag / RPO Violation

<div class="kb-summary">
An RPO violation means replicated VMs are falling behind their target recovery point — the DR copy
is more than X minutes behind the production VM. If the production site fails during an RPO
violation, more data will be lost than your SLA allows. This scenario covers identifying which VMs
are lagging, diagnosing the cause (bandwidth, change rate, or appliance health), and restoring
replication to within RPO before verifying with an SRM test recovery.
</div>

```text
┌────────────────────── SRM Replication Lag / RPO Violation — Investigation Flow ───────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  RPO violation: the DR copy is more than X minutes behind production — data loss risk                 │
│  If production fails during a violation, more data will be lost than the SLA allows                   │
│                                                                                                       │
│  START: SRM alert — RPO Exceeded on one or more VMs, or Aria Operations fires RPO warning             │
│                                                                                                       │
│  STEP 1 — Identify Scope                                                                              │
│  One or a few VMs lagging → high change rate on specific VMs                                          │
│  Many VMs lagging across multiple hosts → inter-site link bandwidth issue                             │
│  Replication stopped entirely on some VMs → vSR appliance health issue                                │
│                                                                                                       │
│  STEP 2 — Diagnose Root Cause                                                                         │
│  Check vSR appliance health on both production and DR sites                                           │
│  Check inter-site bandwidth: NIC stats on ESXi vSphere Replication VMkernel                           │
│  Check VM change rate: SRM → Replication → Details → Current vs Average replication rate              │
│                                                                                                       │
│  STEP 3 — Resolution Branch                                                                           │
│  Appliance fault → redeploy or restart the vSR appliance                                              │
│  Bandwidth exhausted → throttle low-priority VMs, enable compression, or expand inter-site link       │
│  VM change rate too high → enable compression per VM or increase RPO target (requires SLA review)     │
│                                                                                                       │
│  CLOSE: Force Sync Now → monitor until RPO status returns to Met · validate with SRM test recovery    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Navigate to vCenter (production site) → **Site Recovery** → **Replication** → **vSphere Replication** → **Outgoing** tab → sort by **RPO Status**.

| RPO status | Meaning | Priority |
|---|---|---|
| Met | Replication within RPO window | Normal — no action |
| Warning | Within 20% of RPO limit | Monitor; check bandwidth |
| Exceeded | Replication behind RPO window | Investigate now |
| Error | Replication stopped | Urgent — check vSR appliance |

Look for: all lagging VMs on the same ESXi host = host-level NIC or VMkernel issue; lagging VMs spread across hosts = inter-site link is the cause.

---

## 2. Check vSphere Replication Appliance Health

Both the production and DR vSR appliances must be healthy — check via vCenter → **Site Recovery** → **Configure** → **vSphere Replication Servers**.

If an appliance shows a fault:

```bash
# SSH to vSR appliance — check service status
systemctl status vmware-hbrsrv
systemctl status vmware-hbr-cloudagent

# Check replication server logs for errors
tail -100 /var/log/vmware/hbr/hbrServer.log | grep -i error
```

Look for: certificate mismatch errors after a vCenter SSL renewal — fix by re-registering: vCenter → Site Recovery → Configure → vSphere Replication Servers → select appliance → **Reconnect**.

---

## 3. Check Inter-Site Replication Network

Replication traffic flows from the production ESXi host VMkernel (tagged for vSphere Replication) to the DR vSR appliance — total bandwidth equals the combined changed-block rate of all replicating VMs.

```bash
# From ESXi host — check which VMkernel is used for vSphere Replication
esxcli network ip interface list | grep -A5 "vSphereReplication"

# Check NIC traffic on the replication VMkernel's physical NIC
esxcli network nic stats get -n <vmnic-name>
```

Look for: replication NIC at or near 100% utilisation = link saturated; options: enable network compression (20–40% reduction), throttle low-priority VMs, or request a bandwidth increase.

---

## 4. Check VM Change Rate

High-write VMs — databases, transaction logs, large file servers — can outrun available replication bandwidth.

Check: vCenter → Site Recovery → Replication → select the lagging VM → **Details** → compare **Current replication rate** vs **Average replication rate**.

Look for: rate significantly above average = recent backup/log flush/app burst (transient); persistently elevated = VM needs a higher RPO target or dedicated bandwidth.

```bash
# Check replication rate from vSR appliance
# vSR REST API — get replication instance details for a specific VM
curl -sk -u admin:<password> \
  "https://vsr-appliance.domain.local/api/replication/instances" \
  | python3 -m json.tool | grep -A10 "vm-name"
```

---

## 5. Enable Compression or Adjust Throttle Settings

For VMs with persistently high change rates, edit the replication settings: vCenter → Site Recovery → Replication → select VM → **Edit** → enable **Network Compression** or set a **Bandwidth Throttle** (Mbps limit per VM).

For VMs where the RPO target is genuinely unachievable given change rate and link capacity, adjust the RPO target to a realistic value — this is a formal change requiring SLA review.

---

## 6. Force a Manual Sync to Catch Up

Force an immediate changed-block sync for a specific lagging VM: vCenter → Site Recovery → Replication → select the VM → **Sync Now**.

Look for: status returning to **Met** after the sync completes — monitor until confirmed.

```bash
# Verify replication status via vSR REST API after manual sync
curl -sk -u admin:<password> \
  "https://vsr-appliance.domain.local/api/replication/instances?state=REPLICATING" \
  | python3 -m json.tool | grep -E '"vmName"|"rpoStatus"|"rpoViolation"'
```

---

## 7. Verify NSX Inter-Site Management Connectivity

If VMs use NSX stretched overlay segments, a broken NSX management connection does not stop replication but prevents SRM from reconfiguring network mappings during failover.

Check: NSX Manager → **System** → **Fabric** — both sites' transport nodes must be visible and green before running any SRM test or real failover.

---

## 8. Run an SRM Test Recovery to Validate RPO Is Met

After resolving the lag, validate with a non-disruptive test: SRM → **Recovery Plans** → select the plan → **Test**.

SRM powers on DR replicas in an isolated bubble network — no production traffic is affected.

Look for: all VMs powering on, RPO status **Met**, and application connectivity confirmed inside the bubble.

After validation run **Cleanup Test** immediately — leaving test replicas running consumes DR resources and can interfere with real replication.

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

## Key Terms

| Term | Definition |
|---|---|
| SRM (Site Recovery Manager) | VMware DR orchestration product that automates failover and failback of VMs between sites; manages recovery plans and integrates with vSphere Replication for RPO tracking |
| vSphere Replication (vSR) | The VMware replication engine built into vCenter; tracks changed blocks on production VMs and transfers them to a vSR appliance at the DR site on a configurable sync interval |
| RPO (Recovery Point Objective) | The maximum acceptable data loss expressed as time — if RPO is 15 minutes, the DR copy must never be more than 15 minutes behind the production VM |
| RTO (Recovery Time Objective) | The maximum acceptable time for recovery to complete after a failure; vSphere Replication manages RPO, while SRM recovery plan execution determines whether RTO is met |
| Replication appliance | The vSR virtual appliance deployed at each site that receives changed-block data from ESXi hosts and writes it to the DR datastore; must be healthy on both production and DR sides |
| Changed block tracking | The vSphere mechanism that records which disk sectors have been written since the last replication sync; allows vSR to send only the delta rather than the full disk each cycle |
| Sync interval | The configured frequency at which vSphere Replication performs a changed-block transfer; must be equal to or shorter than the VM's RPO target |
| Replication lag | The time gap between the last completed sync and the current time; exceeds RPO when bandwidth, change rate, or appliance health prevents syncs from completing on schedule |
| Test recovery | An SRM operation that powers on DR replicas in an isolated bubble network without impacting production; used to validate that recovery plans and RPO are working correctly |
| Bubble network | The isolated network created by SRM during a test recovery; DR replicas communicate only within this network so production traffic is unaffected |
| Failback | The process of replicating VMs back from the DR site to the production site after a failover; requires re-enabling vSphere Replication in the reverse direction |
| Reprotect | The SRM operation that reverses the replication direction after a failover — makes the DR site the new source and the original production site the new DR target |

---

## Related Scenarios

- [Datastore Full / Capacity Alarm](datastore-full-capacity-alarm/index.md) — A full DR datastore is a hidden cause of replication lag; vSphere Replication silently queues when the DR datastore cannot accept writes.
- [NSX Edge Failure / BGP Down](nsx-edge-failure-bgp-down/index.md) — A BGP failure at the DR site prevents SRM from establishing network connectivity for recovered VMs.
- [vSAN Stretched Cluster Split-Brain](vsan-stretched-cluster-split-brain/index.md) — A site partition that triggers stretched cluster split-brain also disrupts vSphere Replication traffic flowing over the same inter-site link.
