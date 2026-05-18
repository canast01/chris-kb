# NSX — Common Issues

```
┌─────────────────────────────────────────────────────────────┐
│              NSX Triage Decision Flow                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Incident reported                                          │
│        │                                                    │
│        ▼                                                    │
│  ┌─────────────────┐  no  ┌──────────────────────────────┐ │
│  │ Overlay conn?   │─────►│ Check DFW on source ESXi     │ │
│  │ VM→VM / VM→GW   │      │ vsipioctl getstats / getrules│ │
│  └────────┬────────┘      └──────────────────────────────┘ │
│           │ yes                                             │
│           ▼                                                 │
│  ┌─────────────────┐  no  ┌──────────────────────────────┐ │
│  │ Tunnels UP?     │─────►│ get tunnel status            │ │
│  │ get tunnel      │      │ vmkping TEP -d -s 1572       │ │
│  │ status          │      │ Check MTU ≥ 1600 on underlay │ │
│  └────────┬────────┘      └──────────────────────────────┘ │
│           │ yes                                             │
│           ▼                                                 │
│  ┌─────────────────┐  no  ┌──────────────────────────────┐ │
│  │ BGP/OSPF UP?    │─────►│ vrf <id> → get bgp neighbor  │ │
│  │ Edge CLI check  │      │ Check MD5 auth, ASN, uplink  │ │
│  └────────┬────────┘      └──────────────────────────────┘ │
│           │ yes                                             │
│           ▼                                                 │
│  ┌─────────────────┐  no  ┌──────────────────────────────┐ │
│  │ Manager stable? │─────►│ get cluster status           │ │
│  │                 │      │ get corfu-cluster status     │ │
│  └────────┬────────┘      └──────────────────────────────┘ │
│           │ yes → check fabric / alarms / open support case │
└─────────────────────────────────────────────────────────────┘
```

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

### Common Causes

| Cause | Fix |
|---|---|
| DFW default-deny blocking | Add allow rule for gateway traffic in Infrastructure policy |
| Wrong gateway IP configured on segment | Update segment subnet in NSX Manager |
| T1 not connected to a T0 | Connect T1 to T0 in NSX Manager |
| T1 not advertising connected routes | Enable `TIER1_CONNECTED` route advertisement on T1 |
| Missing route on T0 | Check T0 routing table from Edge CLI |

---

## BGP Session Down

### Symptom

BGP neighbor on Tier-0 gateway shows state other than `Established`. External prefixes are not being received; NSX overlay routes are not being advertised to physical network.

### Diagnosis

```bash
# SSH to the Edge node
vrf <tier0-vrf-id>
get bgp neighbor summary
# Look for: State: Active, Idle, or Connect — not Established

# Detailed neighbor info
get bgp neighbor <neighbor-ip>
# Reason for not establishing: auth failure, TCP failure, hold timer, etc.

# Check physical uplink interface
get interface fp-eth0
get interface fp-eth0 counters
# Verify UP state and non-zero Rx counters
```

### Common Causes

| Cause | Diagnosis | Fix |
|---|---|---|
| MD5 password mismatch | Neighbour shows `Auth Failure` in logs | Match passwords on both sides |
| ASN mismatch | `get bgp config` — verify remote ASN | Correct in NSX policy or on router |
| Physical link down | `get interface fp-eth0` — DOWN | Fix physical connectivity |
| MTU mismatch | BFD timers firing; route established then drops | Verify MTU on physical switch ports |
| BFD hold timer | BFD session flapping | Tune BFD timers to match physical path latency |
| Underlay routing | Edge cannot reach peer IP | Add static route on Edge: `set appliance gw-route` |

### Recovery

After fixing the root cause, BGP re-establishes automatically. No manual reset needed. Monitor:

```bash
# From Edge CLI — watch BGP state
get bgp neighbor summary
# State should change from Active → OpenSent → Established within 30–60 seconds
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
