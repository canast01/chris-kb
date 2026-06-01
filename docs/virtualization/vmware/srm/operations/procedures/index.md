# SRM — Procedures


<div class="kb-summary">
Procedures reference covering Create a Protection Group (vSphere Replication), Create a Recovery Plan, Run a Test Failover (Non-Disruptive), Run a Planned Migration, Run a Disaster Recovery (Protected Site Down) and 4 more sections.
</div>

  Test Failover vs Actual Failover
```
┌──────────────────────────────────────────────────────────────┐
│  Test Failover (non-disruptive)                              │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ VMs powered on at recovery site in isolated network   │   │
│  │ Production VMs still running at protected site        │   │
│  │ ──► verify, then Cleanup (removes test VMs)           │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  Planned Migration (both sites up)                           │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ Protected VMs gracefully shut down ──► replicate      │   │
│  │ ──► power on at recovery site ──► update DNS          │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  Disaster Recovery (protected site down)                     │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ Use last replicated point ──► power on at recovery    │   │
│  │ ──► Reprotect (reverse replication) ──► Failback      │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────── VMware SRM — Common Procedures ────────────────────────────────────┐
│                                                                                                       │
│  Routine SRM procedures: add VM to protection group, run DR test, perform planned                     │
│  failover, reprotect after failover, and update recovery plan steps.                                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              DR Test Procedure               │  │               Planned Failover              │   │
│   │          Test: bubble network only           │  │          Notify stakeholders first          │   │
│   │           Select plan: Test option           │  │           Replication sync: verify          │   │
│   │            Monitor: plan progress            │  │            Run: Planned migration           │   │
│   │           Cleanup: remove test VMs           │  │           Failback: Reprotect+run           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DR test must always use Test mode; run actual failover only with explicit approval.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Protection Group Mgmt             │  │               Plan Maintenance              │   │
│   │               Add VM to group                │  │             Update startup order            │   │
│   │          Configure IP customisation          │  │           Add custom recovery step          │   │
│   │          Verify replication running          │  │           Update network mappings           │   │
│   │           Remove decommissioned VM           │  │             Document RTO target             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Test failover uses isolated network on recovery site; cleanup deletes test VMs;                      │
│  planned failover powers off protected site VMs before starting.                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Test mode     = failover to bubble network; no production impact                                     │
│  Planned migration= graceful failover; quiesce source then fail over                                  │
│  Disaster recovery= forced failover; uses last available replica                                      │
│  Reprotect     = reverses replication; recovery becomes protected                                     │
│  Failback      = reprotect then planned migration back to original                                    │
│  Bubble network= isolated VLAN; test VMs not routable to production                                   │
│  IP customisation= re-IP VMs with recovery-site addresses on failover                                 │
│  Startup order = priority sequence; lower number powers on first                                      │
│  Custom step   = script or manual step in recovery plan                                               │
│  Cleanup       = SRM removes test VMs and associated snapshots                                        │
│  Protection group= collection of VMs replicated and failed over together                              │
│  Network mapping= maps source portgroup to recovery portgroup                                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Create a Recovery Plan

```text
Site Recovery → Recovery → Recovery Plans → New

  Name: SQL-DR-Plan
  Protection Groups: add SQL-PG
  Recovery Site: Recovery-Site

  Configure steps:
    Priority 1 — Infrastructure VMs (DNS, DC)
    Priority 2 — Database servers (SQL)
    Priority 3 — Application servers
    Priority 4 — Web servers

  Network Mappings: verify mapped (inherited from site pair or add per-plan)
  IP Customization: for static-IP VMs:
    Site Recovery → Recovery Plans → [plan] → IP Customization
    Add rule: source IP → recovery IP mapping (per-VM or per-subnet)
```

---

## Run a Test Failover (Non-Disruptive)

Test failover powers on VMs in an isolated bubble network — production is unaffected.

```text
Site Recovery → Recovery Plans → [plan] → Test
  Confirm: Test
  Monitor progress: Site Recovery → Recovery Plans → [plan] → History → [current run]
  
After test completes:
  Verify VMs powered on at recovery site (vCenter recovery site → VMs)
  Verify IP customization applied correctly
  Verify application-level health in isolated network

Cleanup (mandatory — must clean up before running another test or real recovery):
  Site Recovery → Recovery Plans → [plan] → Cleanup
  Cleanup removes powered-on test VMs from recovery site
```

---

## Run a Planned Migration

Both sites are available. VMs are gracefully shut down at protected site, replicated, and powered on at recovery site.

```yaml
Site Recovery → Recovery Plans → [plan] → Run
  Type: Planned Migration
  Confirm: check "I understand this will shut down VMs at the protected site"
  Monitor: watch each step complete

Post-migration:
  Verify VMs running at recovery site
  Update DNS records for moved VMs (if not handled by IP customization)
  Notify application teams
```

---

## Run a Disaster Recovery (Protected Site Down)

```yaml
Site Recovery → Recovery Plans → [plan] → Run
  Type: Disaster Recovery
  Confirm: acknowledge data loss risk (last sync point used)
  Monitor: watch recovery progress

Note: VMs at protected site must be considered "lost" — do NOT try to power them on
```

---

## Perform Failback After Recovery

After the protected site is restored and ready:

```text
1. Re-protect VMs at recovery site (reverse replication direction):
   Site Recovery → Protection → Protection Groups → [group] → Reprotect
   This configures replication from recovery site back to protected site

2. Wait for initial replication to complete (RPO achieved)

3. Run Planned Migration back to protected site:
   Site Recovery → Recovery Plans → [original plan] → Run → Planned Migration
```

---

## Add a VM to an Existing Protection Group

For ABR protection groups: add the VM to the storage replication group on the array, then rediscover:
```text
Site Recovery → Protection → [PG] → Discover Devices
```
The new VM appears automatically if it is on a replicated datastore.

For vSphere Replication groups: configure VR on the VM first, then:
```text
Site Recovery → Protection → [PG] → Add VMs
```

---

## Change RPO on a vSphere Replication VM

```text
vCenter (Protected Site) → [VM] → right-click → Configure Replication → Edit
  RPO: change from current value (minimum 5 minutes, maximum 24 hours)
  Save → replication schedule updates immediately
```

---

## Remove VM from Protection (Decommission)

```text
1. Remove VM from Protection Group:
   Site Recovery → Protection → [PG] → VMs → [VM] → Remove

2. If VR-replicated: stop replication on the VM:
   vCenter → [VM] → right-click → Remove Replication

3. Clean up placeholder VM at recovery site:
   vCenter (Recovery) → delete placeholder VM
```
