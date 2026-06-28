---
tags:
  - operations
  - vmware
  - vsphere-replication
---
# vSphere Replication — Health Checks

<div class="kb-summary">
Health Checks reference covering VRA and Site Pairing Status, Check All Replications for RPO Violations, Verify VRA Disk Space, VRS Health (if deployed), Verify Replication Files on Target Datastore and 2 more sections.

*Applies to: vSphere Replication 8.x*
</div>

  Health Check Chain

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **VR appliance health** — open the VAMI console and verify all services show running: `https://<vr-appliance>:5480` → Summary → check hms and vrms service status.
2. **VRS (scale-out server) health** — if VRS nodes are deployed, confirm each is registered and healthy: vCenter → Site Recovery → vSphere Replication → Replication Servers → all show Connected/Healthy.
3. **Replication count and status** — vSR UI → Monitor → Replication → note total active replication count and confirm no items show in Error state.
4. **RPO violations** — vSR UI → Monitor → Replication → filter by "RPO Violated" → investigate any flagged VMs; each violation needs a root-cause note before close of check.
5. **Disk space on target datastores** — verify all target datastores holding replica VMDKs have >20% free headroom; use vCenter → Datastore → Summary for each target.
6. **Network connectivity between VRAs** — from the source VRA appliance shell, confirm round-trip reachability to the target VRA:
   ```bash
   ping <target-VRA-IP>
   ```
7. **VRA-to-VRA data port reachability** — verify TCP 31031 is open between source and target VRA appliances (this is the vSphere Replication data channel):
   ```bash
   nc -zv <target-VRA-IP> 31031
   ```
8. **VRA registration with vCenter** — vCenter → Site Recovery → vSphere Replication → Replication Appliances → confirm VRA shows Registered and Connected for both sites.
9. **SRM integration check** — if SRM is in use: SRM → Protection Groups → confirm no groups display "Replication Error"; expand any amber groups for detail.
10. **Last successful sync timestamp** — vSR UI → per-VM detail → review "Last Sync" field; flag any VM whose last sync is older than 2× its configured RPO interval.

---

## VRA and Site Pairing Status

![VRA and Site Pairing Status](../../../../assets/virtualization-vmware-vsphere-replicatio-hc-vra-and-site-pairing-status.svg)

```text
vCenter → Site Recovery → Sites
  Both sites should show: Connected
  VRA status: Healthy (green)

vCenter → Site Recovery → vSphere Replication
  Replication Appliances tab: VRA status = OK, Connected
```

```bash
# VRA health via API
curl -sk https://vra-london.example.local/api/rest/vr/health | python3 -m json.tool
# Status should be "OK"
```

---

## Check All Replications for RPO Violations

![Check All Replications for RPO Violations](../../../../assets/virtualization-vmware-vsphere-replicatio-hc-check-all-replications-for-rpo-v.svg)

```text
vCenter → Site Recovery → Replications
  Status column: Green = within RPO
  Amber = approaching RPO limit (>75% of RPO elapsed)
  Red = RPO violation (replication lag > configured RPO)

Any red VM: investigate immediately
```

```bash
# Via REST API — list replications with lag
TOKEN=$(curl -sk -X POST \
  "https://vra-london.example.local/api/rest/vr/authentication/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-london.example.local/api/rest/vr/replications" | \
  python3 -c "
import json, sys
reps = json.load(sys.stdin)
for r in reps.get('list', []):
    state = r.get('overallStatus', '')
    name = r.get('name', '?')
    if state != 'OK':
        print(f'[{state}] {name}')
"
```

---

## See also

- [vSphere Replication — Common Issues](../troubleshooting/common-issues/)
- [vSphere Replication — Procedures](procedures/)
- [vSphere Replication — CLI Reference](cli-reference/)

## Verify VRA Disk Space

![Verify VRA Disk Space](../../../../assets/virtualization-vmware-vsphere-replicatio-hc-verify-vra-disk-space.svg)

```bash
ssh admin@vra-london.example.local
df -h
# Monitor /opt and /var partitions
# VRA appliance disk: should have >20% free
```

Target-site datastore containing replica VMDKs:
```bash
vCenter (Target Site) → Datastore → check % used
# Keep below 80% — VRA stops writing when datastore fills up
```

---

## VRS Health (if deployed)

![VRS Health (if deployed)](../../../../assets/virtualization-vmware-vsphere-replicatio-hc-vrs-health-if-deployed.svg)

```text
vCenter → Site Recovery → vSphere Replication → Replication Servers
  Each VRS should show: Connected, Healthy
  VMs assigned to each VRS: should be balanced
```

```bash
ssh admin@vrs-london-01.example.local
systemctl status hms
```

---

## Verify Replication Files on Target Datastore

![Verify Replication Files on Target Datastore](../../../../assets/virtualization-vmware-vsphere-replicatio-hc-verify-replication-files-on-targ.svg)

Replication data is stored as `.vrepl` and `.hbr` files:

```bash
# SSH to ESXi host on target site
ls /vmfs/volumes/<target-datastore>/<VM-folder>/
# You should see: *.vmdk, *.vmx, *.vrepl, *.hbr files
# .vrepl = replica disk
# .hbr = replication control file

# No .vrepl files = replication not established or recovery was completed
```

---

## Certificate Expiry

![Certificate Expiry](../../../../assets/virtualization-vmware-vsphere-replicatio-hc-certificate-expiry.svg)

```bash
# Check VRA management certificate
echo | openssl s_client -connect vra-london.example.local:443 -servername vra-london.example.local 2>/dev/null \
  | openssl x509 -noout -dates

# Check VRA-to-VRA port (44046)
echo | openssl s_client -connect vra-amsterdam.example.local:44046 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## Monthly DR Test Trigger

![Monthly DR Test Trigger](../../../../assets/virtualization-vmware-vsphere-replicatio-hc-monthly-dr-test-trigger.svg)

Run a test recovery on at least one VR-protected VM monthly. For VMs managed by SRM:
```text
SRM → Recovery Plans → [plan] → Test
```

For standalone VR (without SRM):
```text
vCenter → Site Recovery → Replications → [VM] → Recover
  Mode: Test (isolated network)
  After test: Delete the recovered test VM (do not clean up the replication)
```

Document test results — record which VMs were tested, the RPO at time of recovery, and any issues found.
