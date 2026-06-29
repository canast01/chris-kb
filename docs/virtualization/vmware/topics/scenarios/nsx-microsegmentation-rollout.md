---
tags:
  - nsx
  - nsx-4
  - scenarios
  - vmware
---
# NSX Microsegmentation Rollout

<div class="kb-summary">
Microsegmentation applies DFW firewall rules to east-west VM traffic at the hypervisor level —
without requiring network re-architecture or physical firewall changes. The rollout follows a
learn-then-enforce pattern: observe real traffic flows with Aria Networks first, then apply rules
in monitor mode to catch gaps, then switch to enforce. Skipping the observation phase and going
straight to enforce is the most common cause of application outages during microsegmentation
projects.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_enable_ipfix_flow_collection: "1. Enable IPFIX Flow Collection" {shape: rectangle}
2_observe_traffic_flows_phase_1_24_w: "2. Observe Traffic Flows (Phase 1: 2-4 Weeks)" {shape: rectangle}
3_create_nsx_security_groups: "3. Create NSX Security Groups" {shape: rectangle}
4_tag_vms_in_vcenter: "4. Tag VMs in vCenter" {shape: rectangle}
5_define_dfw_policy_in_monitor_mode: "5. Define DFW Policy in Monitor Mode" {shape: rectangle}

products_involved -> 1_enable_ipfix_flow_collection: uses
1_enable_ipfix_flow_collection -> 2_observe_traffic_flows_phase_1_24_w: uses
2_observe_traffic_flows_phase_1_24_w -> 3_create_nsx_security_groups: uses
3_create_nsx_security_groups -> 4_tag_vms_in_vcenter: uses
4_tag_vms_in_vcenter -> 5_define_dfw_policy_in_monitor_mode: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| Aria Operations for Networks | IPFIX flow collection and analysis; rule recommendations from observed traffic |
| NSX | DFW policy and group management; enforces rules at the hypervisor on each ESXi host |
| vCenter Server | VM inventory and tag source; NSX groups use vCenter tags for dynamic membership |
| Aria Operations | Post-enforcement application health monitoring; alert on blocked traffic anomalies |

---

## 1. Enable IPFIX Flow Collection

Configure IPFIX to export VDS flow records to Aria Networks before any rules are written.

NSX Manager → **Networking** → **IPFIX** → **Flows** → **Add Collector** → enter the Aria Networks proxy node IP and port (default: UDP 2055). Then: **Switch IPFIX** → select the VDS → **Enable**.

Look for: flows appearing in Aria Networks → **Network Map** → VM group → **Flows** tab within 15 minutes. Allow at least 24 hours before analysis to separate regular traffic from noise.

---

## 2. Observe Traffic Flows (Phase 1: 2-4 Weeks)

Document every observed east-west and north-south flow pattern from Aria Networks before writing any rules.

Aria Networks → **Network Map** → select the application or VM group being segmented → **Flows**.

Document every observed flow pattern:

| Source group | Destination group | Protocol | Port | Flow type |
|---|---|---|---|---|
| WebTier VMs | AppTier VMs | TCP | 8080 | East-West |
| AppTier VMs | DBTier VMs | TCP | 3306 | East-West |
| Monitoring server | All VMs | TCP | 5672 | North-South |
| All VMs | AD servers | TCP/UDP | 389, 53 | North-South |

The 2–4 week window captures infrequent but legitimate flows: month-end batch jobs, weekly backup agents, quarterly maintenance scripts — rules built from a single day's data will block these when they next run.

---

## 3. Create NSX Security Groups

Create one group per application tier using dynamic membership so new VMs automatically inherit the correct group.

NSX → **Security** → **Inventory** → **Groups** → **Add Group**.

Preferred membership criteria (in order of preference):

| Criteria type | Example | When to use |
|---|---|---|
| VM tag | Tag: `Environment:Production`, Tag: `Tier:Web` | Best — works across clusters and folders |
| VM folder | `/Production/WebServers` | Use if tags are not in use |
| IP address range | `10.10.1.0/24` | Last resort — IPs change; tags do not |
| Static VM list | Individual VM objects | Avoid — new VMs are never included automatically |

Example groups for a three-tier application:

```text
Group: WebTier       — Membership: VM Tag = "Tier:Web"
Group: AppTier       — Membership: VM Tag = "Tier:App"
Group: DBTier        — Membership: VM Tag = "Tier:DB"
Group: Monitoring    — Membership: VM Tag = "Role:Monitoring"
```

Expected: each group → **Members** shows the correct VMs. A misconfigured group that excludes VMs will produce unexpected DFW blocks when enforce mode is enabled.

---

## 4. Tag VMs in vCenter

Apply vCenter tags to VMs so NSX security groups have members before any rules are evaluated.

```powershell
# Create tag categories and tags in vCenter
New-TagCategory -Name "Tier" -Cardinality Single -EntityType VirtualMachine
New-Tag -Name "Web" -Category (Get-TagCategory "Tier")
New-Tag -Name "App" -Category (Get-TagCategory "Tier")
New-Tag -Name "DB"  -Category (Get-TagCategory "Tier")

# Apply tags to VMs
Get-VM "web-vm-01", "web-vm-02" | New-TagAssignment -Tag (Get-Tag "Web")
Get-VM "app-vm-01", "app-vm-02" | New-TagAssignment -Tag (Get-Tag "App")
Get-VM "db-vm-01"               | New-TagAssignment -Tag (Get-Tag "DB")
```

Expected: NSX group membership updates in near-real-time — return to NSX and verify the groups show the correct VMs.

---

## 5. Define DFW Policy in Monitor Mode

Create the DFW policy in monitor mode so rules log violations without blocking traffic — the safety net that prevents outages during rollout.

NSX → **Security** → **Distributed Firewall** → **Add Policy** → set mode to **Monitor** before adding any rules.

Add rules based on the flows documented in Phase 1:

```text
Rule 1: Allow WebTier  → AppTier    TCP 8080   Action: Allow
Rule 2: Allow AppTier  → DBTier     TCP 3306   Action: Allow
Rule 3: Allow Monitoring → Any      TCP 5672   Action: Allow
Rule 4: Allow Any      → AD-servers TCP 389    Action: Allow
Rule 5: Allow Any      → DNS        UDP 53     Action: Allow
Rule 6: Default catch-all           Any        Action: Drop (log)
```

The default Drop rule at the bottom is required — without it the implicit DFW default (allow) applies and the policy has no enforcement effect.

---

## 6. Review Monitor Mode Logs (Phase 2: 1-2 Weeks)

Review the DFW packet log on each host to find traffic that the default Drop rule would block, then add missing allow rules.

```bash
cat /var/log/dfwpktlogs.log | grep "MONITOR DROP" | head -50
```


```text title="Expected output"
2024-01-15T09:23:47.123Z [MONITOR DROP] src=192.168.1.45 dst=10.0.0.8 proto=tcp port=443 reason=policy_deny
2024-01-15T09:24:12.456Z [MONITOR DROP] src=172.16.5.22 dst=10.0.0.9 proto=udp port=53 reason=rate_limit
2024-01-15T09:25:03.789Z [MONITOR DROP] src=192.168.2.100 dst=10.0.0.10 proto=tcp port=22 reason=blacklist
2024-01-15T09:26:15.234Z [MONITOR DROP] src=10.1.1.5 dst=10.0.0.11 proto=icmp reason=protocol_blocked
2024-01-15T09:27:44.567Z [MONITOR DROP] src=203.0.113.77 dst=10.0.0.12 proto=tcp port=3306 reason=policy_deny
2024-01-15T09:28:22.891Z [MONITOR DROP] src=192.168.3.15 dst=10.0.0.13 proto=tcp port=8080 reason=anomaly_detected
2024-01-15T09:29:01.345Z [MONITOR DROP] src=172.31.45.88 dst=10.0.0.14 proto=udp port=5353 reason=rate_limit
2024-01-15T09:30:18.678Z [MONITOR DROP] src=198.51.100.42 dst=10.0.0.15 proto=tcp port=445 reason=malware_signature
```

!!! warning "Common errors"
    **`cat: /var/log/dfwpktlogs.log: No such file or directory`** — Verify the DFW (Distributed Firewall) logging is enabled in vSphere and check the correct log path for your ESXi version.
    **`grep: (standard input): Permission denied`** — Run the command with `sudo` or as root to access protected log files on the ESXi host.
Look for: MONITOR DROP entries with legitimate source/destination pairs. For each entry, either add an allow rule or confirm it is traffic that should be blocked. Common legitimate flows frequently missed:

- Windows activation (TCP 1688)
- SNMP polling from monitoring (UDP 161)
- Backup agent communication (vendor-specific ports)
- Kerberos (TCP/UDP 88)
- RPC dynamic ports (TCP 49152-65535) for Windows services

Also run: Aria Networks → **Security** → **Security Groups** → **Recommended Rules** as a second validation pass against the manually created rules.

---

## 7. Import Aria Networks Recommended Rules

Export Aria Networks rule recommendations to NSX and reconcile them against manually created rules before enforcing.

Aria Networks → **Security** → select the application → **Recommended Rules** → **Export to NSX**.

Expected: Aria Networks rule set covers all observed IPFIX flows; any gaps versus manually created rules are resolved before switching to enforce mode.

---

## 8. Switch to Enforce Mode

Switch to enforce mode only after monitor mode produces zero unexpected MONITOR DROP events for at least 5 business days.

NSX → **Security** → **Distributed Firewall** → select the policy → **Edit** → change mode from **Monitor** to **Enforce** → **Save**.

```bash
# Immediately after switching — check for unexpected real DFW blocks
cat /var/log/dfwpktlogs.log | grep "DROP" | grep -v "MONITOR" | head -50
```


```text title="Expected output"
2024-01-15T09:42:31.245Z [DROP] SRC=192.168.1.105 DST=10.0.0.50 PROTO=TCP DPORT=443 RULE=default-deny-egress
2024-01-15T09:42:35.612Z [DROP] SRC=172.16.5.20 DST=8.8.8.8 PROTO=UDP DPORT=53 RULE=default-deny-dns
2024-01-15T09:42:41.089Z [DROP] SRC=192.168.1.110 DST=10.20.0.1 PROTO=TCP DPORT=3306 RULE=db-access-restricted
2024-01-15T09:42:48.334Z [DROP] SRC=10.0.0.75 DST=203.0.113.45 PROTO=TCP DPORT=22 RULE=ssh-outbound-blocked
2024-01-15T09:42:52.901Z [DROP] SRC=172.16.8.88 DST=192.0.2.100 PROTO=ICMP RULE=ping-blocked-prod
2024-01-15T09:43:01.567Z [DROP] SRC=192.168.1.200 DST=10.50.0.10 PROTO=TCP DPORT=5432 RULE=postgres-restricted
2024-01-15T09:43:15.223Z [DROP] SRC=10.0.0.99 DST=198.51.100.5 PROTO=TCP DPORT=8080 RULE=app-port-blocked
...
```

!!! warning "Common errors"
    **`cat: /var/log/dfwpktlogs.log: No such file or directory`** — Verify the DFW logging path is correct for your vSphere version (check `/etc/vmware/vdfw/` for active config) or enable packet logging in the Distributed Firewall settings.
    **`grep: (standard input): Permission denied`** — Run the command with `sudo` or as root to access the DFW packet log file.
Expected: no application-breaking DROP entries. Have an application owner verify functionality within 15 minutes. If an unexpected break occurs, revert to monitor mode immediately — this restores full connectivity in under 30 seconds.

---

## Post-Task Validation

| Check | Location | Expected Result |
|---|---|---|
| DFW policy mode | NSX → Security → DFW | Enforce |
| Group membership correct | NSX → Security → Inventory → Groups | All expected VMs present |
| No unexpected DFW blocks | `/var/log/dfwpktlogs.log` | No application-breaking DROP entries |
| Application health | Aria Operations | No new critical alerts |
| Aria Networks security alerts | Aria Networks → Security | No unexpected exposed ports |
| DFW rule hit counts | NSX → Security → DFW → Rules | Allow rules show traffic; Drop rule count stable |

---

## Common Mistakes

- **Skipping monitor mode and going straight to enforce.** Even well-researched rule sets miss
  edge-case traffic. Monitor mode is the only reliable way to discover missing rules without
  causing an outage.
- **Using static group membership.** New VMs spun up for the application do not inherit DFW rules
  and operate outside the segmentation boundary. Dynamic tag-based membership is the correct
  approach.
- **Not reviewing DFW logs during monitor mode.** The monitoring phase is only useful if the logs
  are reviewed. An unreviewed monitor phase produces false confidence — the same flows that were
  never looked at will cause blocks when enforce mode is enabled.
- **Not having a rollback plan.** When switching to enforce, always have the NSX console open and
  ready to revert the policy to monitor mode. Switching back takes under 30 seconds and restores
  connectivity immediately.

---

---

## Key Terms

| Term | Definition |
|---|---|
| DFW | Distributed Firewall — the NSX stateful firewall implemented in the ESXi hypervisor kernel on every host; enforces rules on VM traffic at the vNIC level before it enters or leaves the virtual switch |
| Microsegmentation | A security model that applies granular east-west firewall rules between workloads at the hypervisor level, without requiring physical firewall changes or network re-architecture |
| IPFIX | IP Flow Information Export — the protocol NSX uses to send VDS flow records to Aria Networks; each record describes a traffic flow between two endpoints with protocol, port, and byte count |
| NSX security group | A logical container for VMs used as DFW rule source or destination; membership can be dynamic (by tag, folder, or IP range) so new VMs inherit rules automatically |
| Dynamic membership | NSX group membership criteria that evaluates VMs continuously — when a VM receives a matching vCenter tag it is added to the group in near-real-time without manual intervention |
| Monitor mode vs enforce mode | Monitor mode evaluates DFW rules and logs would-be violations but does not block traffic; enforce mode actively blocks traffic that matches no allow rule |
| Policy priority | The order in which DFW policies are evaluated top-to-bottom; a rule in a higher-priority policy overrides matching rules in lower-priority policies |
| East-west traffic | VM-to-VM traffic flowing within the same data centre, typically between application tiers; DFW intercepts this traffic at the hypervisor before it reaches any physical switch |
| Aria Networks | VMware Aria Operations for Networks — the network observability product that collects IPFIX flows, maps application dependencies, and generates DFW rule recommendations based on observed traffic |
| Application discovery | The Aria Networks process of building a traffic-flow map for an application by analysing IPFIX data; used to identify all east-west connections before writing microsegmentation rules |
| Rule recommendation | An Aria Networks feature that generates DFW allow rules derived directly from observed IPFIX flows; exported to NSX to supplement or validate manually created rules |
| dfwpktlogs | The DFW packet log file on each ESXi host (`/var/log/dfwpktlogs.log`) that records flows matching logged DFW rules; MONITOR DROP entries identify missing allow rules during the monitor phase |

## Related Scenarios

- NSX Edge Failure / BGP Down
- NSX Connectivity Broken
- Add ESXi Host to Cluster
- VM Performance Degraded

---

## See also

- [NSX Data Plane — Internals](../../../internals/nsx-data-plane/)
- [Scenarios — NSX DFW Blocking](../nsx-dfw-blocking-application-traffic/)
- [NSX — Deploy](../../../nsx/deploy/)
