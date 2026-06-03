# NSX Microsegmentation Rollout

<div class="kb-summary">
Microsegmentation applies DFW firewall rules to east-west VM traffic at the hypervisor level —
without requiring network re-architecture or physical firewall changes. The rollout follows a
learn-then-enforce pattern: observe real traffic flows with Aria Networks first, then apply rules
in monitor mode to catch gaps, then switch to enforce. Skipping the observation phase and going
straight to enforce is the most common cause of application outages during microsegmentation
projects.
</div>

```text
┌─────────────────────────────── NSX Microsegmentation Rollout — Procedure Flow ────────────────────────────────────┐
│                                                                                                       │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  START: Enable IPFIX flow collection — Aria Networks proxy node receives flows from VDS via NSX IPFIX      ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Phase 1 (2-4 weeks) — Observe flows in Aria Networks: document all east-west and north-south connections  ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 1 — Create NSX security groups (dynamic membership via VM tags or folders)                           ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 2 — Define DFW policy in MONITOR mode: rules log violations but do not block traffic                 ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Phase 2 (1-2 weeks) — Review DFW monitor logs: add missing rules, fix group membership errors             ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 3 — Import Aria Networks recommended rules; switch DFW policy mode to ENFORCE                        ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Post-enforcement: monitor DFW block logs and Aria Networks security alerts; validate application health   ││
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Aria Networks needs to see real traffic flows before any rules are written. IPFIX is the protocol
that NSX uses to export flow records to Aria Networks.

NSX Manager → **Networking** → **IPFIX** → **Flows** → **Add Collector** → enter the Aria Networks
proxy node IP address and port (default: UDP 2055). Then enable IPFIX on the VDS:

NSX Manager → **Networking** → **IPFIX** → **Switch IPFIX** → select the VDS → **Enable**.

Verify flows are arriving: Aria Networks → **Network Map** → select a VM group → **Flows** tab.
If flows appear, IPFIX is working. Allow at least 24 hours before beginning analysis — you need
enough flow data to distinguish regular traffic from noise.

---

## 2. Observe Traffic Flows (Phase 1: 2-4 Weeks)

Aria Networks → **Network Map** → select the application or VM group being segmented → **Flows**.

Document every observed flow pattern:

| Source group | Destination group | Protocol | Port | Flow type |
|---|---|---|---|---|
| WebTier VMs | AppTier VMs | TCP | 8080 | East-West |
| AppTier VMs | DBTier VMs | TCP | 3306 | East-West |
| Monitoring server | All VMs | TCP | 5672 | North-South |
| All VMs | AD servers | TCP/UDP | 389, 53 | North-South |

The 2-4 week observation window captures infrequent but legitimate traffic: month-end batch jobs,
weekly backup agents, quarterly maintenance scripts. Rules written from a single day of flows
will block these when they next run.

---

## 3. Create NSX Security Groups

NSX → **Security** → **Inventory** → **Groups** → **Add Group**.

Create one group per application tier. Use dynamic membership criteria so new VMs automatically
inherit the correct group without manual intervention.

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

After creating groups, verify membership: select each group → **Members** → confirm the expected
VMs appear. A misconfigured group that excludes VMs will produce unexpected DFW blocks when
enforce mode is enabled.

---

## 4. Tag VMs in vCenter

NSX security groups reference vCenter tags. Tags must be applied to VMs before the groups will
have members.

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

NSX reads vCenter tag assignments in near-real-time. After applying tags, return to NSX and
verify the group membership updated correctly.

---

## 5. Define DFW Policy in Monitor Mode

NSX → **Security** → **Distributed Firewall** → **Add Policy**.

Name the policy to reflect the application (e.g., `ThreeTierApp-Microseg`). Before adding any
rules, set the policy mode to **Monitor**. In monitor mode, rules are evaluated against traffic
but no traffic is blocked — violations are logged only. This is the safety net that prevents
outages during rollout.

Add rules based on the flows documented in Phase 1:

```text
Rule 1: Allow WebTier  → AppTier    TCP 8080   Action: Allow
Rule 2: Allow AppTier  → DBTier     TCP 3306   Action: Allow
Rule 3: Allow Monitoring → Any      TCP 5672   Action: Allow
Rule 4: Allow Any      → AD-servers TCP 389    Action: Allow
Rule 5: Allow Any      → DNS        UDP 53     Action: Allow
Rule 6: Default catch-all           Any        Action: Drop (log)
```

The default Drop rule at the bottom is required — it defines what happens to traffic that matches
no explicit rule. Without it, the implicit DFW default (allow) applies and the policy has no effect.

---

## 6. Review Monitor Mode Logs (Phase 2: 1-2 Weeks)

With the policy in monitor mode, all traffic that would be blocked by the default Drop rule is
logged to the DFW packet log on each ESXi host.

```bash
# Review MONITOR DROP events on an ESXi host — identifies missing allow rules
cat /var/log/dfwpktlogs.log | grep "MONITOR DROP" | head -50
```

For each MONITOR DROP entry: determine if the flow is legitimate and add an allow rule, or confirm
it is unwanted traffic that should be blocked. Common legitimate flows that are frequently missed:

- Windows activation (TCP 1688)
- SNMP polling from monitoring (UDP 161)
- Backup agent communication (vendor-specific ports)
- Kerberos (TCP/UDP 88)
- RPC dynamic ports (TCP 49152-65535) for Windows services

Aria Networks → **Security** → **Security Groups** → **Recommended Rules** also generates rule
suggestions based on observed IPFIX flows. Import these as a second validation pass.

---

## 7. Import Aria Networks Recommended Rules

Aria Networks → **Security** → select the application → **Recommended Rules** → **Export to NSX**.

Aria Networks generates DFW rules derived from the actual IPFIX flow data. These rules reflect what
traffic was observed — not what was assumed. Compare the Aria Networks recommendations against the
manually created rules and reconcile any differences before enforcing.

---

## 8. Switch to Enforce Mode

Once monitor mode produces zero unexpected MONITOR DROP events for at least 5 business days:

NSX → **Security** → **Distributed Firewall** → select the policy → **Edit** → change mode from
**Monitor** to **Enforce** → **Save**.

Enforce mode is applied to all ESXi hosts in the transport zone immediately. Traffic that matches
no allow rule is now actively blocked.

```bash
# After switching to enforce: immediately check DFW logs for unexpected blocks
cat /var/log/dfwpktlogs.log | grep "DROP" | grep -v "MONITOR" | head -50
```

Have an application owner verify application functionality within 15 minutes of switching to
enforce mode. If an unexpected application break occurs, switch the policy back to monitor mode
immediately — this is non-disruptive and restores full connectivity.

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

## Related Scenarios

- NSX Edge Failure / BGP Down
- NSX Connectivity Broken
- Add ESXi Host to Cluster
- VM Performance Degraded
