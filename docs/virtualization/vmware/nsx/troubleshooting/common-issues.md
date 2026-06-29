---
tags:
  - nsx
  - nsx-4
  - troubleshooting
  - vmware
search:
  boost: 2
---
# NSX — Common Issues
![NSX — Common Issues](../../../../assets/virtualization-vmware-nsx-troubleshooting-common-issues.svg)

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
```bash
# SSH to Edge node
get node cpu-usage
get service dataplane stats

# Check active connections
get load-balancer status
get load-balancer virtual-servers
get nat translations | wc -l
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
A: "VM cannot reach\nanother VM" {shape: rectangle}
B: "North-south broken\n/ BGP down" {shape: rectangle}
C: "Transport node\nconfig failed" {shape: rectangle}
D: "NSX Manager\nunreachable" {shape: rectangle}
A1: "Run Traceflow in NSX UI\nbetween source and dest" {shape: rectangle}
A2: "A2" {shape: rectangle}
A3: "→ DFW Rules section\ncheck applied policy" {shape: rectangle}
A4: "→ Segment Config section\ncheck port binding" {shape: rectangle}
A5: "→ Routing section\ncheck route tables" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "→ Edge Failure section\ncheck HA and BFD" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "→ BGP section\ncheck AS, timers, upstream" {shape: rectangle}
B5: "Check T0 static routes\nand route redistribution" {shape: rectangle}
C1: "→ Transport Node section\ncheck VIBs and TEP IP" {shape: rectangle}
D1: "D1" {shape: rectangle}
D2: "→ Manager Cluster section" {shape: rectangle}
D3: "Check API gateway\nand LB VIP" {shape: rectangle}

S -> A
S -> B
S -> C
S -> D
A -> A1
A2 -> A3
A2 -> A4
A2 -> A5
B1 -> B2
B3 -> B4
B3 -> B5
C -> C1
D1 -> D2
D1 -> D3
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## See also

- [NSX Data Plane — Internals](../../../internals/nsx-data-plane/)
- [NSX — Operations](../../operations/)
- [Scenarios — NSX Connectivity Broken](../../../topics/scenarios/nsx-connectivity-broken/)

---

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
