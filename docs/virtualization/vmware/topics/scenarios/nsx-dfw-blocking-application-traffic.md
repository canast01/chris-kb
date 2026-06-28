---
tags:
  - nsx
  - nsx-4
  - scenarios
  - vmware
---
# NSX DFW Blocking Application Traffic

<div class="kb-summary">
An application suddenly cannot reach its database or a dependent service after an NSX DFW
rule change or a new workload is deployed. This scenario covers how to determine whether
DFW is causing the block, identify the specific rule responsible, and resolve it without
opening broad exceptions — using Traceflow, hit count analysis, and packet capture.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_confirm_dfw_is_the_cause: "1. Confirm DFW Is the Cause" {shape: rectangle}
2_identify_the_blocking_rule: "2. Identify the Blocking Rule" {shape: rectangle}
3_check_group_membership: "3. Check Group Membership" {shape: rectangle}
4_resolve_rule_group_or_tag_fix: "4. Resolve: Rule, Group, or Tag Fix" {shape: rectangle}
5_packet_capture_at_vnic_level: "5. Packet Capture at vNIC Level" {shape: rectangle}

products_involved -> 1_confirm_dfw_is_the_cause: uses
1_confirm_dfw_is_the_cause -> 2_identify_the_blocking_rule: uses
2_identify_the_blocking_rule -> 3_check_group_membership: uses
3_check_group_membership -> 4_resolve_rule_group_or_tag_fix: uses
4_resolve_rule_group_or_tag_fix -> 5_packet_capture_at_vnic_level: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| NSX Manager | DFW policy management; Traceflow; group and tag configuration |
| vCenter | VM inventory; VM-to-host mapping for DFW context |
| ESXi | DFW kernel module; packet capture at vNIC level |
| Aria Operations for Networks | Flow visibility; rule hit analysis; topology view |

---

## 1. Confirm DFW Is the Cause

Before touching any rule, confirm that DFW is responsible and not a routing issue, firewall appliance, or OS-level firewall on the VM.

```text
Quick elimination checklist:
  VM OS firewall (iptables/Windows Firewall)?
      → Test: temporarily disable inside the guest and retry
  NSX Edge firewall (not DFW)?
      → Only applies if traffic crosses a T0 or T1 gateway
  Physical firewall / ACL?
      → Trace the path — is the destination on the same overlay segment?
  DFW (distributed, per-vNIC)?
      → Applies to ALL VM-to-VM traffic regardless of IP subnet
```

Run **Traceflow** in NSX Manager to get a definitive answer:

**NSX Manager → Plan & Troubleshoot → Traceflow**

```text
Traceflow settings:
  Source:       Select the source VM vNIC
  Destination:  Enter the destination VM vNIC or IP address
  Protocol:     Layer 4 — TCP, UDP, or ICMP
  Port:         Destination port (e.g., 1433 for SQL, 5432 for PostgreSQL)
  Direction:    Unidirectional (source to destination only)
```

Look for: a result showing **Dropped — DFW** at the source vNIC confirms DFW is the blocker. The output includes the rule ID that caused the drop.

---

## 2. Identify the Blocking Rule

Traceflow output includes the NSX rule ID. Use this to locate the exact rule in the DFW policy table.

**NSX Manager → Security → Distributed Firewall → find rule by ID**

```text
DFW rule table — columns to check:
  Rule ID      — matches Traceflow output exactly
  Action       — DROP or REJECT (REJECT sends TCP RST; DROP silently discards)
  Source       — group, IP set, or Any
  Destination  — group, IP set, or Any
  Service      — port/protocol; check if the required port is included
  Applied To   — which transport zone, DFW section, or specific group the rule applies to
  Hit Count    — number of times this rule has been matched; confirms it is active
```

Check hit count on the suspect rule to confirm it is matching traffic (not just a theoretical match). A recent spike in hit count correlates with when the connectivity issue started.

Look for: **Default Drop** rules at the bottom of a section are the most common culprit when a new VM is deployed or a group membership changes — the VM falls outside all allow rules and hits the implicit deny.

---

## 3. Check Group Membership

The most common cause of unexpected DFW drops is a VM not being a member of the group targeted by the allow rule.

**NSX Manager → Inventory → Groups → select group → View Members**

```text
Group membership types and how to check:
  Static members    → look for the specific VM in the member list
  Dynamic criteria  → check if the VM satisfies the criteria (name pattern, OS, tag)
  IP set            → confirm the VM's IP is in the set; check for IP change
  VM tag            → confirm the correct NSX tag is applied to the VM
```

```bash
# Check NSX tags on a VM via NSX Manager API
curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/fabric/virtual-machines?display_name=<vm-name>" \
  | python3 -m json.tool | grep -A5 "tags"
```

Look for: a recently changed IP address on the source or destination VM will invalidate an IP-set-based group membership. Dynamic tag criteria are the most fragile — confirm the tag is still present and spelled correctly.

---

## 4. Resolve: Rule, Group, or Tag Fix

Choose the fix based on the root cause identified in Step 3.

**Option A — Add a targeted allow rule above the deny:**

```text
New rule placement (most specific first):
  Priority  Action  Source               Destination          Service
  100       Allow   App-Server-Group     DB-Server-Group      TCP:5432
  200       Drop    Any                  DB-Server-Group      Any          ← existing deny
  999       Drop    Any                  Any                  Any          ← default deny
```

The new allow rule must be placed at a higher priority (lower number) than the blocking rule. Rules are evaluated top to bottom; the first match wins.

**Option B — Fix group membership:**

```text
For static groups: add the VM directly to the group via NSX Manager UI
For dynamic groups: apply the correct NSX tag to the VM
For IP-set groups: update the IP set with the VM's current IP address
```

```bash
# Apply an NSX tag to a VM via API
curl -sk -X POST -u admin:<password> \
  -H "Content-Type: application/json" \
  -d '{"external_id":"<vm-moid>","tags":[{"scope":"app","tag":"web-tier"}]}' \
  "https://<nsx-manager>/api/v1/fabric/virtual-machines?action=update_tags"
```

After any rule or group change, re-run Traceflow to confirm the packet now shows **Delivered** at the destination.

Look for: if Traceflow shows Delivered but the application still fails — the issue is now above Layer 4 (application layer, TLS, auth) rather than DFW.

---

## 5. Packet Capture at vNIC Level

If Traceflow is inconclusive, capture at the ESXi vNIC level to see the raw traffic.

```bash
# SSH to the ESXi host running the source VM
# List VM vNIC interfaces to find the right port
esxcli network vm list
esxcli network vm port list -w <WorldID>

# Capture traffic on the vNIC (pktcap-uw)
pktcap-uw --switchport <SwitchPort> --proto 6 --dstport 5432 -c 200 -o /tmp/cap.pcap

# Transfer and analyse in Wireshark
# Filter in Wireshark: tcp.port==5432 and tcp.flags.reset==1
```

Look for: TCP RST packets in the capture confirm the DFW is sending a reset (REJECT rule). No response at all confirms a DROP rule. If neither appears and traffic is flowing out the vNIC, the issue is downstream.

---

## Key Terms

| Term | Definition |
|---|---|
| DFW | Distributed Firewall — NSX-T stateful firewall implemented in the ESXi kernel at the vNIC of every VM; inspects all East-West traffic |
| Traceflow | NSX diagnostic tool that injects a test packet into the data plane and reports which component (DFW rule, routing, physical) handled or dropped it |
| Applied-To | DFW setting that scopes which VMs or transport zones a rule applies to; misconfigured applied-to is a common source of unexpected rule matches |
| Group | NSX logical construct containing VMs, IP sets, MAC addresses, or dynamic criteria; used as source/destination in DFW rules |
| NSX tag | Label applied to a VM via NSX inventory; used as dynamic group membership criteria; applied independently of vCenter tags |
| Hit count | Number of packets matched by a DFW rule; visible per-rule in NSX Manager; useful for identifying which rule is actively blocking traffic |
| REJECT vs DROP | REJECT sends TCP RST back to the source (visible to the application); DROP silently discards the packet (application sees timeout) |
| T0/T1 gateway | NSX logical routers; East-West traffic between VMs on the same overlay segment does NOT traverse the gateway — only DFW applies |
| Implicit deny | Default behaviour of a DFW section configured in Allow-Listed mode; any traffic not matching an explicit allow rule is dropped |

---

## Common Mistakes

- **Assuming routing or a physical firewall is the cause before checking DFW.** DFW blocks at the vNIC level — traffic never leaves the ESXi host. Checking a perimeter firewall will show no traffic at all, which does not rule out DFW.
- **Adding a broad "Any → Any → Allow" rule to fix connectivity.** This bypasses all microsegmentation. Always add the minimum specific rule needed (source group, destination group, required port).
- **Not checking Applied-To scope.** A rule scoped to one section or segment will not apply to VMs on a different segment. The VM may have moved or a new segment was created.
- **Forgetting rule ordering.** Rules are evaluated top to bottom; the first match wins. Placing an allow rule below the deny rule it is meant to override has no effect.
- **Confusing NSX tags with vCenter tags.** They are separate systems. DFW group dynamic criteria use NSX tags only; vCenter tags are not directly visible in NSX group membership.

---

## Related Scenarios

- [NSX Connectivity Broken](nsx-connectivity-broken/index.md) — broader NSX connectivity failures including routing, transport zones, and TEP misconfiguration.
- [NSX Edge Failure / BGP Down](nsx-edge-failure-bgp-down/index.md) — North-South traffic failures when the T0/T1 gateway is unavailable.
- [NSX Microsegmentation Rollout](nsx-microsegmentation-rollout/index.md) — planned procedure for designing and deploying DFW rules across a cluster.
- [VM Performance Degraded](vm-performance-degraded/index.md) — DFW hit count overhead can contribute to latency in high-traffic VMs.
