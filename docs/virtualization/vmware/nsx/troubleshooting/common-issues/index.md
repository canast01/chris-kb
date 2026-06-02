# NSX — Common Issues


<div class="kb-summary">
Common Issues reference covering Incident Triage, VM Cannot Communicate with Gateway, Geneve Tunnel Down Between Two Hosts, DFW Rules Not Applying, NSX Manager Cluster UNSTABLE and 2 more sections.
</div>

## Incident Triage

Work through this checklist for any NSX-related incident before diving into specific areas:

- [ ] Check transport node status: `GET /api/v1/transport-nodes/status` — identify DOWN or DEGRADED nodes
- [ ] Check Edge node health: **UI → System → Fabric → Nodes → Edge Transport Nodes**
- [ ] Review open alarms: `GET /api/v1/alarms?status=OPEN` — filter by HIGH or CRITICAL
- [ ] Check BGP sessions from Edge CLI: `vrf <id>` → `get bgp neighbor summary`
- [ ] Check DFW for unintended block rules — review recent DFW changes in NSX audit log
- [ ] Verify NSX Manager cluster health: `get cluster status` on any Manager node
- [ ] Check segment/gateway overlay connectivity via Traceflow (UI: **Plan & Troubleshoot → Traceflow**)

| Question | First Check |
|---|---|
| Are transport nodes UP? | `GET /api/v1/transport-nodes/status` |
| Are Edge nodes reachable? | UI → Fabric → Edge Transport Nodes |
| What alarms are open? | `GET /api/v1/alarms?status=OPEN` |
| Are BGP sessions established? | Edge CLI: `vrf <id>` → `get bgp neighbor summary` |
| Is DFW blocking traffic? | ESXi host: `vsipioctl getstats -f <filter>` |

---

## VM Cannot Communicate with Gateway

### Symptom

A VM can reach other VMs on the same segment but cannot reach its default gateway (T1 gateway IP). Or a VM cannot reach another subnet through the T1.

### Diagnosis

```bash
# Step 1 — Confirm the VM's segment and gateway IP
# Check segment config in NSX Manager UI or API
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/segments/<segment-id>"

# Step 2 — Check DFW on the VM's ESXi host
# SSH to the ESXi host running the VM
summarize-dvfilter | grep <vm-name>
vsipioctl getrules -f <filter-name>
vsipioctl getstats -f <filter-name>

# Look for a DENY or DROP rule with non-zero packet count
# The last rule (65535) being hit with high counts = default deny is blocking

# Step 3 — Traceflow from the VM to the gateway
# NSX Manager UI: Plan & Troubleshoot → Traceflow
# Source: VM vNIC, Destination: gateway IP, Protocol: ICMP
```
┌───────────────────────────────────────── NSX — Common Issues ─────────────────────────────────────────┐
│                                                                                                       │
│  BGP session down, DFW unexpected drops, transport node failures, and fixes.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             BGP / Routing Issues             │  │               DFW Drop Issues               │   │
│   │           Session Idle or Connect            │  │         Traffic unexpectedly dropped        │   │
│   │            Check Edge uplink VLAN            │  │             Check DFW rule order            │   │
│   │           Verify BGP timers match            │  │             Enable DFW flow logs            │   │
│   │            Check ASN/neighbor IP             │  │              Use Traceflow tool             │   │
│   │           get bgp neighbor summary           │  │            Check group membership           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  BGP/routing diagnosis first; DFW Traceflow for east-west drop issues.                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Transport Node Issues             │  │            Manager Cluster Issues           │   │
│   │             Node shows degraded              │  │             Node shows DEGRADED             │   │
│   │           Check NSX agent on ESXi            │  │           Check disk space on mgr           │   │
│   │            Resync transport node             │  │            Restart proton service           │   │
│   │            Check TEP connectivity            │  │              Verify NTP in sync             │   │
│   │           N-VDS mtu / uplink check           │  │            Check /var/log/proton            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs, Edge VMs, ESXi transport nodes, ToR switches, vCenter                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  BGP session = routing peer; Idle/Connect = not established                                           │
│  Traceflow   = NSX tool; sends test packet to debug path/drops                                        │
│  DFW flow log= per-rule hit log; enabled in rule settings                                             │
│  Transport node = ESXi/Edge with N-VDS; resync forces config refresh                                  │
│  TEP         = Tunnel Endpoint; GENEVE source; ping to verify                                         │
│  N-VDS       = NSX distributed switch; check uplink binding                                           │
│  proton      = NSX Manager core service; restart to recover stuck state                               │
│  DEGRADED    = NSX cluster status; one or more nodes unhealthy                                        │
│  Group memb  = DFW group members; wrong group = wrong firewall policy                                 │
│  ASN         = Autonomous System Number; must match on BGP peers                                      │
│  Edge uplink = VLAN uplink on Edge to physical switch; check tagging                                  │
│  Resync      = NSX Manager pushes config to transport node again                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────────── NSX — Common Issues ─────────────────────────────────────────┐
│                                                                                                       │
│  BGP session down, DFW unexpected drops, transport node failures, and fixes.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             BGP / Routing Issues             │  │               DFW Drop Issues               │   │
│   │           Session Idle or Connect            │  │         Traffic unexpectedly dropped        │   │
│   │            Check Edge uplink VLAN            │  │             Check DFW rule order            │   │
│   │           Verify BGP timers match            │  │             Enable DFW flow logs            │   │
│   │            Check ASN/neighbor IP             │  │              Use Traceflow tool             │   │
│   │           get bgp neighbor summary           │  │            Check group membership           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  BGP/routing diagnosis first; DFW Traceflow for east-west drop issues.                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Transport Node Issues             │  │            Manager Cluster Issues           │   │
│   │             Node shows degraded              │  │             Node shows DEGRADED             │   │
│   │           Check NSX agent on ESXi            │  │           Check disk space on mgr           │   │
│   │            Resync transport node             │  │            Restart proton service           │   │
│   │            Check TEP connectivity            │  │              Verify NTP in sync             │   │
│   │           N-VDS mtu / uplink check           │  │            Check /var/log/proton            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs, Edge VMs, ESXi transport nodes, ToR switches, vCenter                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  BGP session = routing peer; Idle/Connect = not established                                           │
│  Traceflow   = NSX tool; sends test packet to debug path/drops                                        │
│  DFW flow log= per-rule hit log; enabled in rule settings                                             │
│  Transport node = ESXi/Edge with N-VDS; resync forces config refresh                                  │
│  TEP         = Tunnel Endpoint; GENEVE source; ping to verify                                         │
│  N-VDS       = NSX distributed switch; check uplink binding                                           │
│  proton      = NSX Manager core service; restart to recover stuck state                               │
│  DEGRADED    = NSX cluster status; one or more nodes unhealthy                                        │
│  Group memb  = DFW group members; wrong group = wrong firewall policy                                 │
│  ASN         = Autonomous System Number; must match on BGP peers                                      │
│  Edge uplink = VLAN uplink on Edge to physical switch; check tagging                                  │
│  Resync      = NSX Manager pushes config to transport node again                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Geneve Tunnel Down Between Two Hosts

### Symptom

VMs on the same segment hosted on different ESXi hosts cannot communicate. The segment is UP, but traffic between the two hosts is not flowing.

### Diagnosis

```bash
# From NSX Manager CLI
nsxcli
get tunnel status
# Look for DOWN tunnels between specific TEP pairs

get tunnel status <remote-tep-ip>

# Identify which hosts have the affected TEPs
get tunnel endpoints

# From the ESXi host — verify TEP IP is assigned
esxcli network ip interface ipv4 get | grep vmk

# Test TEP reachability
vmkping -I vmk<n> <remote-tep-ip>

# Test with the right MTU
vmkping -I vmk<n> -d -s 1572 <remote-tep-ip>
```

### Common Causes

| Cause | Test | Fix |
|---|---|---|
| MTU < 1600 on underlay | `vmkping -d -s 1572` fails | Set physical switch MTU to 9000 on TEP VLAN |
| Underlay VLAN mismatch | No connectivity at all | Verify TEP port group VLAN matches physical switch |
| TEP IP not assigned | `esxcli network ip interface ipv4 get` — no TEP vmk | Re-prepare transport node; check IP pool |
| BFD failure | Tunnel flapping | Check underlay path stability; adjust BFD timers |
| NSX VIB not installed | `esxcli software vib list \| grep nsx` — empty | Re-run transport node preparation |

---

## DFW Rules Not Applying

### Symptom

A DFW policy change was made in NSX Manager, but the rules are not taking effect on a specific VM.

### Diagnosis

```bash
# Step 1 — Confirm the policy is published (not in draft)
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/domains/default/security-policies/<policy-id>"
# Check: "publish_state": "realized"

# Step 2 — Check realisation status on the transport node
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/realized-state/realized-entities?intent_path=<policy-path>"

# Step 3 — Check rules on the ESXi host
# SSH to ESXi host running the VM
summarize-dvfilter | grep <vm-name>
vsipioctl getrules -f <filter-name> | grep <rule-id>

# Step 4 — Check group membership
# Is the VM actually in the security group referenced by the rule?
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/domains/default/groups/<group-id>/members/virtual-machines"
```

### Common Causes

| Cause | Fix |
|---|---|
| VM not in security group | Add VM tag that matches group expression, or add VM explicitly |
| Policy not in `Applied To` scope | Set `Applied To` to include the relevant segment or group |
| Rule order wrong — earlier allow rule matches before block rule | Move block rule earlier in the policy |
| Policy not realized | Check realisation state; check Manager-to-TN connectivity |
| VM on excluded list (DFW bypass) | Check `GET /api/v1/firewall/excludelist` — remove if listed incorrectly |

---

## NSX Manager Cluster UNSTABLE

### Symptom

`get cluster status` shows `UNSTABLE`, or two of the three Manager nodes are unreachable.

### Diagnosis

```bash
# From any reachable Manager node
nsxcli
get cluster status
get managers
get corfu-cluster status

# Check services on this node
get services
get service http
get service manager
```

### Recovery Steps

1. **Can you reach all three nodes?** If all three are down, restore from backup (see Backup & Restore page).

2. **One node down**: The cluster remains operational with 2/3 nodes. Power cycle or redeploy the failed node, then rejoin it to the cluster.

3. **Two nodes down**: The cluster loses quorum and becomes read-only. Power on the failed nodes. If the nodes are unrecoverable, restore from backup.

4. **Corfu DB issues**: If `get corfu-cluster status` shows errors:
   ```bash
   get corfu-cluster status
   # If shows UNSTABLE — collect logs and open a P1 support case immediately
   # Do NOT attempt manual Corfu repair without Broadcom guidance
   ```

5. **Disk space**: Full disk is a common cause of Manager instability:
   ```bash
   df -h /
   # /var/log/vmware/ can grow large
   du -sh /var/log/vmware/nsx-manager/
   ```
   If disk is full, truncate old logs (not current log files) and restart services.

---

## Transport Node Preparation Failing

### Symptom

A vSphere cluster host fails to reach `Success` state after applying a Transport Node Profile. Host shows `Failed` or stuck in `In Progress`.

### Diagnosis

```bash
# Check transport node state details
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/transport-nodes/<tn-id>/state"

# Check the specific error message
# It will indicate which step failed: VIB install, TEP IP allocation, etc.

# On the ESXi host (SSH)
esxcli software vib list | grep -i nsx
# If VIBs are missing or showing wrong version, re-run preparation

# Check IP pool has available IPs
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/pools/ip-pools/<pool-id>/ip-allocations"
```

### Common Causes

| Cause | Fix |
|---|---|
| VIB install failed (host in maintenance mode requirement) | Put host in maintenance mode; retry |
| IP pool exhausted | Expand the TEP IP pool |
| VIB acceptance level too restrictive | Set `esxcli software acceptance set --level=VMwareAccepted` |
| vCenter connectivity lost during preparation | Verify vCenter is reachable; retry |
| Transport zone not matching vDS on host | Verify vDS is correct in the TNP |

---

## Edge Node Performance Issues (High CPU)

### Symptom

Edge node CPU is consistently above 80%. Load balancer or NAT throughput is degraded.

### Diagnosis

```bash
# SSH to Edge node
get node cpu-usage
get service dataplane stats

# Check active connections
get load-balancer status
get load-balancer virtual-servers
get nat translations | wc -l
```

### Common Causes and Fixes

| Cause | Fix |
|---|---|
| Single Edge node handling all traffic (no ECMP) | Enable ECMP on T0 or add a second active Edge |
| LB pool with too many concurrent connections | Scale backend pool; add more Edge nodes to cluster |
| Undersized Edge VM (Small/Medium) | Upgrade to Large Edge VM |
| NAT connection table overflow | Check `get nat translations` count; reduce NAT scope or increase Edge size |

Edge CPU is dedicated to the NSX dataplane — do not add VMs to Edge node hosts. If the Edge node hosts other VMs, the NSX dataplane and VMs compete for CPU.
