# SRM — Procedures

---

## Create a Protection Group (Array-Based Replication)

```
vCenter (Protected Site) → Site Recovery → Protection → Protection Groups → New

  Type: Array Based Replication
  Name: SQL-PG
  Storage Adapter: Pure Storage FlashArray
  Datastore Group: select replication group containing SQL VMs
    (SRA discovers replication groups from the array — must already be replicated)
  → Next → Finish
```

The protection group will include all VMs on the replicated datastores.

---

## Create a Protection Group (vSphere Replication)

```
Site Recovery → Protection → Protection Groups → New

  Type: vSphere Replication groups
  Name: WebApp-VR-PG
  VMs: select individual VMs (each must have VR configured — right-click → Configure Replication)
  → Finish
```

---

## Create a Recovery Plan

```
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

```
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

```
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

```
Site Recovery → Recovery Plans → [plan] → Run
  Type: Disaster Recovery
  Confirm: acknowledge data loss risk (last sync point used)
  Monitor: watch recovery progress

Note: VMs at protected site must be considered "lost" — do NOT try to power them on
```

---

## Perform Failback After Recovery

After the protected site is restored and ready:

```
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
```
Site Recovery → Protection → [PG] → Discover Devices
```
The new VM appears automatically if it is on a replicated datastore.

For vSphere Replication groups: configure VR on the VM first, then:
```
Site Recovery → Protection → [PG] → Add VMs
```

---

## Change RPO on a vSphere Replication VM

```
vCenter (Protected Site) → [VM] → right-click → Configure Replication → Edit
  RPO: change from current value (minimum 5 minutes, maximum 24 hours)
  Save → replication schedule updates immediately
```

---

## Remove VM from Protection (Decommission)

```
1. Remove VM from Protection Group:
   Site Recovery → Protection → [PG] → VMs → [VM] → Remove

2. If VR-replicated: stop replication on the VM:
   vCenter → [VM] → right-click → Remove Replication

3. Clean up placeholder VM at recovery site:
   vCenter (Recovery) → delete placeholder VM
```
