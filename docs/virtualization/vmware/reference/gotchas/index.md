---
tags:
  - reference
  - vmware
---
# VMware Gotchas

<div class="kb-summary">
Underdocumented behaviours, default limits, and common traps across the VMware platform. Each entry documents what happens, why it happens, and how to prevent or fix it. These are the issues that cause real incidents — things that work fine until they don't.
</div>

```text
┌────────────────────────────────────── VMware — Gotchas ───────────────────────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  Each gotcha: what happens · why · impact · how to avoid / fix                                        │
│  Categories: HA/DRS · vSAN · NSX · Snapshots · Lifecycle · Limits · Certificates                      │
│                                                                                                       │
│  HA / DRS GOTCHAS                                                                                     │
│  Slot-based AC over-reserves with large VMs · vCLS VMs cannot be deleted · FT incompatible with vSAN  │
│                                                                                                       │
│  vSAN / STORAGE GOTCHAS                                                                               │
│  Resync blocks maintenance mode · 80% capacity hard stops writes · dedup ratio drops post-encryption  │
│                                                                                                       │
│  NSX / NETWORK GOTCHAS                                                                                │
│  TEP MTU mismatch silent · DFW default deny not visible in UI by default · tag case-sensitive         │
│                                                                                                       │
│  LIFECYCLE GOTCHAS                                                                                    │
│  vDS rollback 30-second window · upgrade order matters · certificate expiry cascades                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## HA and DRS Gotchas

### vCLS VMs Appear in Cluster and Cannot Be Deleted

**What happens:** After enabling DRS or HA on a cluster, vSphere automatically deploys 1–3 small `vCLS` (vSphere Cluster Services) VMs in a special hidden datastore (`vsanDatastore` or a shared datastore). These VMs appear in inventory but cannot be deleted or moved through normal means. Attempts to power them off are automatically reverted within minutes.

**Why:** vCLS VMs are the coordination agents for DRS placement decisions and HA operations in vSphere 7+. They replaced a monolithic vCenter component with distributed agents. vSphere monitors them and restores them if deleted.

**Impact:** vCLS VMs consume CPU, RAM (~2 GB each), and datastore capacity. They will trigger backup job failures if a backup tool tries to protect them without the correct exclusion filter.

**Fix:**
```text
To exclude vCLS VMs from backup jobs, filter by VM name pattern: vCLS-*
To temporarily disable vCLS (for troubleshooting only), use:
  Advanced cluster setting: config.vcls.clusters.<cluster-id>.enabled = false
  (Re-enable immediately after troubleshooting — disabling vCLS degrades HA/DRS)
```

---

### HA Slot-Based Admission Control Over-Reserves With Mixed VM Sizes

**What happens:** If a cluster uses Slot-Based admission control and contains even one VM with large CPU or memory reservations, the slot size is calculated from that VM. All other VMs are treated as if they were that large. HA blocks new VM power-ons even when there is plenty of capacity — because the calculated "available slots" is very low.

**Example:** A cluster with 3 hosts × 512 GB RAM each (1.5 TB total). One VM has a 256 GB RAM reservation. Slot size = 256 GB. "Available slots" = 3 after reserving 1 host. A new 4 GB VM cannot power on because 4 slots × 256 GB = 1 TB of reserved RAM, which exceeds availability — even though the actual VM only needs 4 GB.

**Fix:** Switch to Percentage-based admission control. Reserve the equivalent of one host's contribution (e.g., 25% for a 4-node cluster, 20% for a 5-node cluster).

---

### DRS Does Not Balance vSAN Resync Traffic

**What happens:** When vSAN is rebuilding absent components after a disk failure, the resync traffic runs across the vSAN VMkernel. DRS does not consider resync I/O when making vMotion decisions — it may move VMs *onto* the host with the most active resync, worsening storage contention.

**Impact:** During a disk failure risk window (between disk failure and rebuild completion), DRS may inadvertently increase storage latency on the affected host by adding VM workloads to it.

**Fix:** During active vSAN resyncs, temporarily set the affected host to "Partially Automated" DRS or add a DRS anti-affinity rule to keep latency-sensitive VMs away from it. Remove after resync completes.

---

### Fault Tolerance (FT) Is Incompatible With vSAN and Most Advanced Features

**What happens:** vSphere Fault Tolerance (continuous availability, RPO=0) has a long list of incompatible features: vSAN datastores, snapshots, linked clones, large pages, 3D graphics, NVMe controllers, and multi-vCPU VMs above 8 vCPU.

**Why:** FT works by recording and replaying every CPU instruction between primary and secondary VM — any feature that introduces non-determinism breaks this model.

**Impact:** Enabling FT on a VM stored on vSAN will fail with an error. Attempts to snapshot an FT-protected VM will fail. FT only works on VMFS or NFS datastores.

**Fix:** Use HA with custom restart priority for critical VMs on vSAN instead of FT. For true zero-RPO protection, use vSAN stretched cluster with ActiveCluster (FlashArray) or synchronous SRM replication.

---

## vSAN Gotchas

### Placing a Host in Maintenance Mode During Active Resync Causes Data Loss Risk

**What happens:** If you put a host into maintenance mode while vSAN is actively rebuilding components (resync in progress), you reduce the protection level further. For FTT=1 VMs that already have one absent component and one host in maintenance mode, some VMs may become non-compliant and lose their last surviving data copy.

**Fix:** Always check resync status before putting any host into maintenance:
```bash
esxcli vsan debug resync summary get
# Only proceed if BytesToResync = 0
```

---

### vSAN Stops Accepting Writes at 80% Capacity

**What happens:** When vSAN physical capacity reaches 80%, the cluster enters a degraded write mode. Above 92%, vSAN may place the datastore in read-only mode, causing VM crashes.

**Why:** vSAN requires capacity headroom for resync operations and for the write buffer. Without headroom, a disk failure would leave no space to rebuild absent components.

**Impact:** VM freezes, application crashes, and data corruption if the threshold is hit without warning.

**Fix:** Set a capacity alarm at 70% (not 80%). At 75%, begin capacity relief operations. Never rely on the default 75% alarm as an early warning — by the time the alarm fires, headroom is already limited.

---

### vSAN Dedup Savings Collapse When Workloads Are Encrypted

**What happens:** vSAN dedup and compression is calculated before data is written. If VM-level encryption (vSphere VM Encryption) or application-level encryption is enabled, all data entering vSAN is already encrypted and random — dedup finds zero duplicate blocks and compression finds zero compressibility. The dedup ratio drops to 1:1.

**Impact:** If capacity was sized based on an expected dedup ratio (e.g., 3:1 for VDI workloads), enabling encryption halves or triples the effective storage consumption.

**Fix:** When sizing vSAN for encrypted workloads, do not count dedup/compression savings. Size on raw physical capacity only. Consider vSAN Data-at-Rest Encryption (array-level) instead of VM-level encryption — vSAN DAR encryption is applied after dedup/compression, preserving the savings ratio.

---

## NSX Gotchas

### TEP MTU Mismatch Causes Silent Packet Drops

**What happens:** If any switch in the TEP (Tunnel Endpoint) path is configured with MTU 1500 instead of 9000, Geneve-encapsulated packets above ~1450 bytes are silently dropped or fragmented. VMs appear to have connectivity for small packets (ping works) but fail for large transfers (file copies, database queries, application timeouts).

**Why:** Geneve adds a 50-byte header overhead. A 1500-byte IP packet becomes a 1550-byte Geneve frame — exceeding 1500 MTU and causing fragmentation or drops.

**Fix:**
```bash
# Test MTU from ESXi TEP VMkernel to another TEP
vmkping -I vmk10 -d -s 8972 <remote-tep-ip>
# -d = do not fragment; -s 8972 = 8972 bytes payload + 28 bytes IP/ICMP = 9000 bytes
# Must succeed from every host to every other host in the transport zone
```

Confirm MTU 9000 on: ESXi vDS portgroup (TEP portgroup), physical ToR switch ports, any intermediate switches in the path.

---

### NSX DFW Default Deny Is Not Visible in the Main Rule Table

**What happens:** When a DFW section is configured with an "Allow Listed" security policy, there is an implicit default-deny rule at the bottom of that section. This rule is not visible in the normal DFW rule table — it only appears in the rule hit counts and Traceflow output.

**Impact:** A VM that is not included in any allow rule will have all traffic silently dropped without any visible blocking rule in the UI. Engineers assume there is no rule blocking traffic and overlook DFW entirely.

**Fix:** Use Traceflow first for any unexplained connectivity failure. The Traceflow output reports the exact rule ID (including the implicit deny rule ID) that dropped the packet.

---

### NSX Tags Are Case-Sensitive

**What happens:** NSX tag values are case-sensitive. A dynamic group with criterion `tag = "web-tier"` will not match a VM tagged with `Web-Tier` or `WEB-TIER`.

**Impact:** DFW allow rules stop applying after a manual tag update that changes capitalisation. VM is dropped by the implicit deny rule.

**Fix:** Establish a naming standard for NSX tags and enforce it. Common convention: all lowercase, hyphen-separated (e.g., `web-tier`, `db-tier`, `app-tier`). Add a compliance check to alert on tag values that do not match the standard pattern.

---

## Snapshot Gotchas

### Snapshot Delta Growth Is Unbounded and Accelerates Under Load

**What happens:** A snapshot delta disk grows with every write to the base VMDK after the snapshot is taken. For write-heavy workloads (databases, log files), a snapshot taken on a Monday and forgotten can fill the datastore by Wednesday.

**Key data point:** A 100 GB database server writing 2 GB/hour will consume 48 GB of snapshot delta space in 24 hours. After one week, the delta is larger than the original VMDK.

**Impact:** Datastore capacity alarm → vSAN cluster near-full → snapshot consolidation required alarm → potential VM freeze during forced consolidation.

**Fix:** Backup tools must have verified snapshot removal. Set a maximum snapshot age alarm (e.g., any snapshot older than 24 hours). Never take manual snapshots on database VMs without a removal plan.

---

### Snapshot Consolidation Required Does Not Remove Snapshot Delta Automatically

**What happens:** After a backup tool fails to cleanly remove a snapshot, vCenter detects residual delta files and raises the "Virtual Machine Disks Consolidation Needed" alarm. The alarm does NOT automatically consolidate — it only notifies. The delta continues to grow.

**Fix:**
```text
vCenter → right-click VM → Snapshots → Consolidate
```

Monitor consolidation progress in Recent Tasks — it can take hours for large deltas. The VM remains live during consolidation but I/O latency increases. Schedule consolidation during off-peak hours for production VMs.

---

## Lifecycle and Certificate Gotchas

### vCenter Upgrade Without Closing vDS Edit Session Leaves Network in Read-Only Mode

**What happens:** If a vDS port group or switch is being edited in another browser session when a vCenter upgrade begins, the vDS edit lock is not released cleanly. After the upgrade, the vDS is stuck in a "read-only" state and no port group changes can be made until the lock is manually cleared via the vSphere Managed Object Browser (MOB).

**Fix:** Before any vCenter upgrade, confirm no vDS edit sessions are open:
```text
vCenter → Networking → right-click vDS → Actions — check for any pending edits
```

---

### vDS Configuration Rollback Window Is 30 Seconds

**What happens:** When a host is migrated to a vDS, there is a 30-second rollback window during which vCenter tests connectivity. If vCenter cannot reach the host within 30 seconds of applying the new configuration, the change is rolled back automatically to the last working state.

**Impact:** Network changes that break management connectivity are automatically reversed — but this also means a misconfigured network change will silently revert, and the engineer may not notice immediately.

**Fix:** Confirm management VLAN connectivity before migrating vmk0 to vDS. Test from a host that will NOT be migrated first. Always have out-of-band (iDRAC/IPMI) access available during networking changes.

---

### NTP Drift Breaks SSO, HA, vSAN, and Certificates Simultaneously

**What happens:** If NTP is misconfigured and ESXi hosts drift > 5 minutes from vCenter time, SSO authentication tokens become invalid. Symptoms appear simultaneously: SSO login failures, vSAN components showing as absent, HA agent disconnections, and certificate errors — all caused by the same root cause.

**Why:** Kerberos-based SSO tokens have a 5-minute clock skew tolerance. vSAN also uses Paxos consensus with timestamps. Certificate validity checking uses system time.

**Fix:** Configure NTP on every component: ESXi hosts, vCenter VCSA, NSX Manager, and all infrastructure VMs. Use at least two NTP sources. Verify with:
```bash
# On ESXi
esxcli system time get
ntpq -p

# On VCSA
/usr/lib/vmware-tools/sbin/ntpq -p
```

---

### Upgrade Order Matters — Out-of-Order Upgrades Break APIs

**What happens:** VMware components have strict upgrade ordering. If NSX is upgraded before vCenter, or if vSAN is upgraded while ESXi is still at the previous major version, API compatibility breaks occur and SDDC Manager workflows fail.

**Required upgrade order for VCF/vSphere:**
```text
1. SDDC Manager
2. vCenter
3. ESXi hosts (one cluster at a time)
4. vSAN ESA upgrade (if applicable)
5. NSX Manager
6. NSX Transport Nodes (ESXi and Edge)
7. Aria Suite (via LCM)
```

Never upgrade NSX before vCenter. Never upgrade ESXi past the vCenter build it is managed by. Check the VMware Interoperability Matrix before any upgrade.

---

## Limits and Defaults Gotchas

### vCenter Manages a Maximum of 2,000 Hosts and 35,000 VMs

**What happens:** vCenter Server has hard limits. Exceeding them causes performance degradation and eventually vCenter instability, not a clean failure.

| Resource | Limit per vCenter |
|---|---|
| ESXi hosts | 2,000 |
| VMs | 35,000 |
| Hosts per cluster | 96 |
| VMs per cluster | 8,000 |
| vDS port groups | 10,000 |
| Concurrent vMotion | 8 per host (1 GbE), 16 per host (10 GbE) |

**Fix:** For environments approaching these limits, use Enhanced Linked Mode to distribute inventory across multiple vCenter instances while maintaining a single management view.

---

### ESXi Host Has a Default 1,024 VM Limit

**What happens:** ESXi hosts have a per-host VM limit of 1,024 powered-on VMs. This limit is almost never hit in physical environments but is a real constraint in nested virtualisation (ESXi-on-ESXi) test labs.

---

### vMotion Concurrent Migrations Are Limited by Network Speed

```text
Per-host vMotion concurrency limits:
  1 GbE:    2 concurrent vMotions
  10 GbE:   4 concurrent vMotions
  25 GbE:   8 concurrent vMotions
  40 GbE+:  16 concurrent vMotions
```

DRS and maintenance mode operations respect these limits — a 96-host cluster entering maintenance mode on one host will queue vMotions rather than parallelise them all simultaneously.
