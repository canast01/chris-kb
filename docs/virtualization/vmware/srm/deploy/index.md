# SRM — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Site Recovery Manager DR orchestration. Phases 1–2 establish prerequisites and deploy SRM at both the protected and recovery sites; Phases 3–4 cover site pairing, inventory mappings, and replication (vSphere Replication or SRA); Phases 5–6 build protection groups, recovery plans, and validate with a test failover.
</div>

```text
┌──────────────────────────────────── SRM — Deployment Phases ──────────────────────────────────────────┐
│                                                                                                       │
│  Six phases from infrastructure prerequisites to a tested and validated recovery plan. Both sites     │
│  must be deployed before pairing; test failover is mandatory before sign-off.                         │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌──────────────────────────────┐    │
│   │  Phase 1: Prerequisites    │  │  Phase 2: SRM Appliance    │  │  Phase 3: Site Pairing       │    │
│   │  Two vCenters operational  │  │  Deployment                │  │  & Inventory Mappings        │    │
│   │  Ports 443, 8095, 9086     │  │  Deploy OVA: protected     │  │  Site Pair wizard            │    │
│   │  DNS for SRM FQDNs         │  │  Deploy OVA: recovery      │  │  Network + folder mappings   │    │
│   │  Replication mechanism     │  │  Register with vCenter     │  │  Resource + storage mappings │    │
│   └────────────────────────────┘  └────────────────────────────┘  └──────────────────────────────┘    │
│                                                                                                       │
│                ▼                               ▼                               ▼                      │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌──────────────────────────────┐    │
│   │  Phase 4: Replication      │  │  Phase 5: Protection       │  │  Phase 6: Recovery Plans     │    │
│   │  Configuration             │  │  Groups                    │  │  & Test Failover             │    │
│   │  vSphere Replication VRA   │  │  vSR groups: VMs + RPO     │  │  Create recovery plan        │    │
│   │  or SRA for array-based    │  │  ABR groups: array sets     │  │  IP customisation rules      │   │
│   │  Replication health: no lag│  │  All VMs: Protected status  │  │  Test failover + cleanup     │   │
│   │  Placeholder VMs created   │  │  Placeholders at DR site   │  │  RTO measurement + sign-off  │    │
│   └────────────────────────────┘  └────────────────────────────┘  └──────────────────────────────┘    │
│                                                                                                       │
│  Physical Infrastructure: SRM OVA VMs at each site; SQL Server (Windows-based installs);              │
│  replication network between sites; WAN/MPLS/dark fibre; vCenter at both sites.                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Site pair      = bidirectional trust between two SRM Servers; TCP 443 + 9086                         │
│  Protection group= set of VMs replicated together; maps to one or more recovery plans                 │
│  Recovery plan  = ordered failover runbook: priority groups, IP mappings, custom scripts              │
│  vSR            = vSphere Replication; host-based async replication; RPO 5 min–24 h                   │
│  SRA            = Storage Replication Adapter; integrates array-based replication with SRM            │
│  Test bubble    = isolated network for test failover; no production routing                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Prerequisites

**Exit criterion:** Both sites operational; network ports confirmed open; DNS resolves; replication mechanism in place.

### Infrastructure Readiness

| Check | Required | Notes |
|---|---|---|
| Protected site vCenter | Operational | Must be reachable from SRM VM |
| Recovery site vCenter | Operational | Must be reachable from SRM VM |
| Network ports between sites | 443, 8095, 9086 TCP | SRM Server ↔ SRM Server |
| vSphere Replication ports | 80, 443, 902, 31031 TCP | VRA ↔ VRA |
| DNS forward + reverse | SRM FQDN resolves from both sites | Required for certificate pairing |
| NTP | Both sites same source, < 500 ms drift | Certificate and log correlation |
| vCenter version match | Both sites same major version | Pairing requirement |

### Firewall Rules

```text
Protected SRM (srm-protected.example.local: 10.10.1.50)
  → Recovery SRM (srm-recovery.dr.example.local: 10.20.1.50)
  → TCP 443:  SRM management and vCenter plugin
  → TCP 9086: SRM inter-site replication and recovery coordination
  → TCP 8095: SRM internal API

Recovery SRM → Protected SRM: same ports (bidirectional)

vSphere Replication (VRA protected: 10.10.1.60 → VRA recovery: 10.20.1.60)
  → TCP 443, 80:   VRA management
  → TCP 902, 31031: replication data channel
```

### Replication Mechanism Decision

Choose before deployment:

| Type | Components | RPO | Use case |
|---|---|---|---|
| vSphere Replication | VRA OVA at each site | 5 min – 24 h | General VM-level replication |
| Array-Based (SRA) | Storage array + SRA plugin | Near-zero (sync) | Mission-critical workloads on SAN |

---

## Phase 2 — SRM Appliance Deployment

**Exit criterion:** SRM appliance deployed and registered with vCenter at both sites; SRM plugin visible in vSphere Client at both sites.

### Deploy SRM OVA — Protected Site

In vCenter (protected site): **Actions → Deploy OVF Template**

```text
SRM OVA: VMware-srm-<version>.ova
Deployment size: Medium (up to 2,000 VMs)
Datastore: management datastore (not the replicated datastore)
Network: management port group

Customise template:
  Hostname:       srm-protected.example.local
  IPv4 address:   10.10.1.50
  Netmask:        255.255.255.0
  Gateway:        10.10.1.1
  DNS:            10.10.0.5, 10.10.0.6
  NTP:            ntp1.example.local
  Admin password: <admin password>
```

### Register SRM with Protected Site vCenter

After VM powers on, access the SRM setup UI at `https://srm-protected.example.local:9086/`:

```text
Setup → Configure vCenter Server connection:
  vCenter FQDN:  vcenter-protected.example.local
  Username:      administrator@vsphere.local
  Password:      <password>
  Accept SSL thumbprint

Apply licence key when prompted.
```

Verify: vSphere Client → Site Recovery — SRM plugin loads without errors.

### Deploy SRM OVA — Recovery Site

Repeat the identical OVA deployment procedure on the recovery site vCenter:

```text
Hostname:     srm-recovery.dr.example.local
IPv4 address: 10.20.1.50
vCenter:      vcenter-recovery.dr.example.local
```

---

## Phase 3 — Site Pairing and Inventory Mappings

**Exit criterion:** Site pair shows `Connected` status; all four mapping types configured; placeholder datastore configured at recovery site.

### Pair the Sites

From the **protected site vCenter** → Site Recovery → New Site Pair:

```text
Remote vCenter:           vcenter-recovery.dr.example.local
Remote SRM Server FQDN:   srm-recovery.dr.example.local
Credentials:              administrator@vsphere.local (recovery site)
Accept certificate thumbprints from both SRM servers
```

Verify: Site Recovery → Summary → Status = **Connected** on both sites.

### Configure Inventory Mappings

All four mapping types must be configured before creating protection groups:

**Network Mappings:**
```text
Site Recovery → Site Pair → Configure → Network Mappings
Protected: PG-Production-App (VLAN 100)  →  Recovery: PG-DR-App (VLAN 200)
Protected: PG-Production-DB  (VLAN 110)  →  Recovery: PG-DR-DB  (VLAN 210)
Test network: PG-DR-Test-Bubble (isolated, no uplink — for test failover)
```

**Folder Mappings:**
```text
Protected: VM-Folder-Production  →  Recovery: VM-Folder-DR-Recovered
```

**Resource Mappings:**
```text
Protected: cluster-protected / RP-Production  →  Recovery: cluster-recovery / RP-DR
```

**Placeholder Datastore:**
```text
Site Recovery → Site Pair → Placeholder Datastores
Select a small datastore at the recovery site for VM config files (2–5 GB sufficient)
```

### IP Customisation Rules

Configure IP re-mapping rules so VMs acquire the correct recovery-site IPs at failover:

```text
Site Recovery → Site Pair → Configure → IP Customisation → Add Mapping
  Source network:      10.10.1.0/24  (protected site)
  Destination network: 10.20.1.0/24  (recovery site)
  Gateway:             10.20.1.1
  DNS primary:         10.20.0.5
  DNS secondary:       10.20.0.6
```

For VMs that need a per-NIC override (different IP, not just subnet mapping):
```text
VM-level customisation → Add per-VM rule
  VM: db-server-01
  NIC: Network adapter 1
  Recovery IP: 10.20.1.101/24
  Gateway:     10.20.1.1
```

---

## Phase 4 — Replication Configuration

**Exit criterion:** Replication active for all target VMs; no lag exceeding RPO targets; placeholder VMs visible at recovery site.

### vSphere Replication — VRA Deployment

If using vSphere Replication, deploy the VRA OVA at each site first:

```text
vCenter (protected) → Actions → Deploy OVF Template
  OVA: VMware-vSphere-Replication-<version>.ova
  Hostname:     vra-protected.example.local
  IPv4:         10.10.1.60/24
  vCenter:      vcenter-protected.example.local

  Repeat at recovery site:
  Hostname:     vra-recovery.dr.example.local
  IPv4:         10.20.1.60/24
```

Pair VRAs via the protected site vCenter → Site Recovery → New Site Pair (VRA pairing follows after SRM pairing completes).

### Configure vSphere Replication for VMs

```text
VM → Configure → vSphere Replication → Configure Replication
  Target site:        recovery site
  Target datastore:   dr-datastore (at recovery site)
  RPO:                15 minutes   (5 min minimum; lower RPO = more replication I/O)
  Multiple point in time (MPIT): Enable (keep 3 instances for point-in-time recovery)
```

```powershell
# Verify replication status via PowerCLI
$vrServer = Connect-VIServer vcenter-protected.example.local
Get-VM | Get-VRReplication | Where-Object { $_.State -ne "Active" }
# Expected: no output (all replications Active)
```

### SRA — Array-Based Replication

If using SRA (e.g., Pure Storage FlashArray, Dell SRDF), install the SRA on **both** SRM Servers:

```powershell
# Example: Pure Storage SRA — install on protected SRM Server
Pure_Storage_SRA_<version>.exe /silent

# Install on recovery SRM Server (same version)
Pure_Storage_SRA_<version>.exe /silent

# Register SRA in SRM (protected site):
# Site Recovery → Storage → Storage Adapters → Configure Adapter
#   Adapter: Pure Storage FlashArray
#   Array manager: fa-protected.example.local
#   API token: <FlashArray API token>
```

---

## Phase 5 — Protection Groups

**Exit criterion:** All target VMs assigned to protection groups; every VM shows `Protected` status; placeholders exist at recovery site.

### Create a vSphere Replication Protection Group

```text
Site Recovery → Protection Groups → New Protection Group
  Site: protected site
  Type: vSphere Replication
  Name: PG-AppTier-vSR
  Select VMs:
    web-server-01, web-server-02, app-server-01, app-server-02
  Replication: confirm each VM has active vSphere Replication configured
```

### Create an Array-Based Replication Protection Group

```text
Site Recovery → Protection Groups → New Protection Group
  Type: Array Based Replication
  Name: PG-DBTier-ABR
  SRA: Pure Storage FlashArray
  Consistency group / datastore group: select the replicated datastore
  VMs auto-discovered from the replicated datastore
```

### Verify Protection Status

```powershell
# PowerCLI — list all VMs and their SRM protection status
$srm = Connect-SrmServer -SrmServerAddress srm-protected.example.local
$protectedVMs = $srm.ExtensionData.Protection.QueryVms()
$protectedVMs | Where-Object { $_.ProtectionState -ne "protected" } |
    Select-Object Name, ProtectionState
# Expected: no output (all VMs show protected)
```

Verify at recovery site: vSphere Client → Site Recovery → Protection Groups → [PG] — all VMs show **Protected**; placeholder VMs exist in the recovery site inventory.

---

## Phase 6 — Recovery Plans and Test Failover

**Exit criterion:** Recovery plan test passes; RTO measured and documented; test cleanup completes; plan in `Ready` state.

### Create a Recovery Plan

```text
Site Recovery → Recovery Plans → New Recovery Plan
  Name:              RP-AppTier-Failover
  Recovery site:     recovery site
  Protection groups: PG-AppTier-vSR, PG-DBTier-ABR

  VM startup groups:
    Priority 1: db-server-01, db-server-02   (databases first)
    Priority 2: app-server-01, app-server-02  (app tier waits for DB)
    Priority 3: web-server-01, web-server-02  (frontend last)

  Custom steps:
    Before Priority 1 power-on:
      Script: "C:\Scripts\pre-failover-notify.ps1 -site recovery"
    After Priority 3 power-on:
      Prompt: "Verify application health before continuing"
```

### Run Test Failover

```text
Site Recovery → Recovery Plans → RP-AppTier-Failover → Test
  Confirm: production VMs remain running during test
  SRM creates snapshot of replicated datastores at recovery site
  VMs power on in isolated bubble network (PG-DR-Test-Bubble)
  IP customisation applies recovery-site IPs
  Record start time → measure per-priority-group boot time
```

```powershell
# Monitor test via PowerCLI
$srm = Connect-SrmServer -SrmServerAddress srm-protected.example.local
$plan = $srm.ExtensionData.Recovery.ListPlans() |
    Where-Object { $_.Name -eq "RP-AppTier-Failover" }
$srm.ExtensionData.Recovery.GetHistory($plan.MoRef) |
    Select-Object StartTime, EndTime, ResultState, Error
```

### Verify Recovery Plan Test Results

```powershell
# Run a pre-check only (no actual power-on) at any time
$srm.ExtensionData.Recovery.Start($plan.MoRef, "PRECHECK_ONLY")

# Check plan history for last test outcome
$history = $srm.ExtensionData.Recovery.GetHistory($plan.MoRef)
$history | Select-Object StartTime, ResultState
# Expected: ResultState = Success (or Warning with acceptable warnings)
```

Measure RTO from test records: time from plan start to last VM in Priority 3 booted. Document against agreed RTO target.

### Test Cleanup

```text
Site Recovery → Recovery Plans → RP-AppTier-Failover → Cleanup
  SRM powers off test VMs
  Test snapshots deleted
  Placeholder VMs restored to pre-test state
  Plan returns to Ready state
```

### Post-Deployment Checklist

| Check | Location / Command | Pass Criterion |
|---|---|---|
| Site pair status | Site Recovery → Summary | Connected (both sites) |
| SRM plugin loaded | vSphere Client → Site Recovery | Loads without errors |
| Inventory mappings | Site Pair → Configure → Mappings | All 4 types configured |
| VM protection status | Protection Groups → [PG] | All VMs: Protected |
| Placeholder VMs | Recovery site vCenter inventory | Present for all protected VMs |
| Replication health | vSphere Replication or array console | No lag > RPO target |
| Recovery plan pre-check | `Recovery.Start(plan, "PRECHECK_ONLY")` | No critical errors |
| Test failover | Recovery Plan → Test | ResultState: Success |
| RTO measurement | Recovery Plan history | Within agreed RTO target |
| Test cleanup | Recovery Plan → Cleanup | Plan back to Ready state |
| IP customisation | Post-test VM IP in bubble network | Recovery-site IPs applied |
| Recurring test schedule | Site Recovery → Reporting | Schedule set (quarterly minimum) |
