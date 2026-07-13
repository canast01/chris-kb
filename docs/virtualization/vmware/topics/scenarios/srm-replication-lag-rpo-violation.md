---
tags:
  - scenarios
  - srm
  - vmware
description: "An RPO violation means replicated VMs are falling behind their target recovery point — the DR copy is more than X minutes behind the production VM. If the..."
---
# SRM Replication Lag / RPO Violation

<div class="kb-summary">
An RPO violation means replicated VMs are falling behind their target recovery point — the DR copy
is more than X minutes behind the production VM. If the production site fails during an RPO
violation, more data will be lost than your SLA allows. This scenario covers identifying which VMs
are lagging, diagnosing the cause (bandwidth, change rate, or appliance health), and restoring
replication to within RPO before verifying with an SRM test recovery.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_identify_which_vms_are_lagging: "1. Identify Which VMs Are Lagging" {shape: rectangle}
2_check_vsphere_replication_applianc: "2. Check vSphere Replication Appliance Health" {shape: rectangle}
3_check_intersite_replication_networ: "3. Check Inter-Site Replication Network" {shape: rectangle}
4_check_vm_change_rate: "4. Check VM Change Rate" {shape: rectangle}
5_enable_compression_or_adjust_throt: "5. Enable Compression or Adjust Throttle Settings" {shape: rectangle}

products_involved -> 1_identify_which_vms_are_lagging: uses
1_identify_which_vms_are_lagging -> 2_check_vsphere_replication_applianc: uses
2_check_vsphere_replication_applianc -> 3_check_intersite_replication_networ: uses
3_check_intersite_replication_networ -> 4_check_vm_change_rate: uses
4_check_vm_change_rate -> 5_enable_compression_or_adjust_throt: uses
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


```text title="Expected output"
● vmware-hbrsrv.service - VMware vSphere Replication Server
     Loaded: loaded (/usr/lib/systemd/system/vmware-hbrsrv.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:18 UTC; 2 days ago
   Main PID: 4521 (java)
     CGroup: /system.slice/vmware-hbrsrv.service
             └─4521 /usr/java/default/bin/java -Xmx2048m -Xms512m...

● vmware-hbr-cloudagent.service - VMware HBR Cloud Agent
     Loaded: loaded (/usr/lib/systemd/system/vmware-hbr-cloudagent.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:33:05 UTC; 2 days ago
   Main PID: 5847 (python)
     CGroup: /system.slice/vmware-hbr-cloudagent.service
             └─5847 /usr/bin/python3 /opt/vmware/hbr/cloudagent/agent.py

2024-01-17T14:45:22.341Z ERROR [hbrServer] Replication task failed for VM vm-1847: Connection timeout after 30s
2024-01-17T14:52:18.903Z ERROR [hbrServer] Failed to authenticate with vCenter 192.168.1.50: Invalid credentials
2024-01-17T15:01:44.556Z ERROR [hbrServer] Insufficient disk space on /storage/replication: 2.1GB required, 1.8GB available
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unit vmware-hbrsrv.service could not be found.` | Verify the vSphere Replication Server is installed with `rpm -qa | grep vmware-hbr` and reinstall if missing. |
    | `tail: cannot open '/var/log/vmware/hbr/hbrServer.log' for reading: No such file or directory` | Check that the replication server has started at least once and verify the log directory exists with `ls -la /var/log/vmware/hbr/`. |
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


```text title="Expected output"
Name                          Enabled Connected MTU     IPv4 Address         IPv4 Netmask         IPv6 Address
vmk0                          true    true      1500    192.168.1.45         255.255.255.0        fe80::250:56ff:fe9a:b1c2
vmk1                          true    true      1500    192.168.2.50         255.255.255.0        fe80::250:56ff:fe9a:b1c3
vmk2                          true    true      1500    192.168.3.100        255.255.255.0        fe80::250:56ff:fe9a:b1c4
vSphereReplication            true    true      1500    192.168.4.75         255.255.255.0        fe80::250:56ff:fe9a:b1c5

NIC name: vmnic2
Packets received: 1847293
Packets sent: 2156847
Bytes received: 3847293847
Bytes sent: 4156847293
Broadcast packets received: 12
Multicast packets received: 847
Dropped packets received: 0
Dropped packets sent: 0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown option or malformed command at position 6` | Verify the exact vmnic name (e.g., vmnic0, vmnic1) and use the correct syntax: `esxcli network nic stats get -n vmnic2`. |
    | `Could not find a matching VMkernel adapter` | Ensure vSphere Replication is configured and the VMkernel interface exists; check with `esxcli network ip interface list` first. |
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


```text title="Expected output"
{
    "instances": [
        {
            "vm-name": "prod-db-01",
            "replication_rate_mbps": 245.3,
            "lag_seconds": 12,
            "status": "in_sync",
            "last_sync": "2024-01-15T14:32:18Z",
            "target_site": "dr-datacenter-02",
            "rpo_minutes": 5
        },
        {
            "vm-name": "prod-web-03",
            "replication_rate_mbps": 89.7,
            "lag_seconds": 3,
            "status": "in_sync",
            "last_sync": "2024-01-15T14:33:45Z"
        }
    ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification (already present in example; if error persists, verify vSR appliance hostname matches certificate CN). |
    | `curl: (7) Failed to connect to vsr-appliance.domain.local port 443: Connection refused` | Verify the vSR appliance is running and accessible on the network; check firewall rules and confirm the hostname/IP in the URL. |
    | `jq: parse error: Invalid JSON at line 1` | Ensure the vSR API is responding with valid JSON; check authentication credentials and confirm the API endpoint is correct for your vSR version. |
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


```text title="Expected output"
{
  "vmName": "prod-db-01",
  "rpoStatus": "COMPLIANT",
  "rpoViolation": false
}
{
  "vmName": "prod-web-02",
  "rpoStatus": "COMPLIANT",
  "rpoViolation": false
}
{
  "vmName": "prod-app-03",
  "rpoStatus": "WARNING",
  "rpoViolation": true
}
{
  "vmName": "dr-cache-01",
  "rpoStatus": "COMPLIANT",
  "rpoViolation": false
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the vSR appliance certificate into your system CA bundle. |
    | `curl: (7) Failed to connect to vsr-appliance.domain.local port 443: Connection refused` | Verify the vSR appliance hostname/IP is correct and the REST API service is running with `systemctl status vmware-vsr-api` on the appliance. |
    | `jq: parse error: Invalid JSON text at line 1` | Ensure the API response is valid JSON by testing the curl command without piping to `python3 -m json.tool` first to see the raw response. |
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

- [Datastore Full / Capacity Alarm](datastore-full-capacity-alarm.md) — A full DR datastore is a hidden cause of replication lag; vSphere Replication silently queues when the DR datastore cannot accept writes.
- [NSX Edge Failure / BGP Down](nsx-edge-failure-bgp-down.md) — A BGP failure at the DR site prevents SRM from establishing network connectivity for recovered VMs.
- [vSAN Stretched Cluster Split-Brain](vsan-stretched-cluster-split-brain.md) — A site partition that triggers stretched cluster split-brain also disrupts vSphere Replication traffic flowing over the same inter-site link.
