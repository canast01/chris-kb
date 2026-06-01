# vSphere Replication — Health Checks


<div class="kb-summary">
Health Checks reference covering VRA and Site Pairing Status, Check All Replications for RPO Violations, Verify VRA Disk Space, VRS Health (if deployed), Verify Replication Files on Target Datastore and 2 more sections.
</div>

  Health Check Chain
```text
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  VRA Status      │    │  VR Agents       │    │  Replication     │
│  (both sites)    │───►│  on ESXi hosts   │───►│  Status per VM   │
│  ┌────────────┐  │    │  ┌────────────┐  │    │  ┌────────────┐  │
│  │ hms/vrms   │  │    │  │ hbrsvc     │  │    │  │ Green: OK  │  │
│  │ running?   │  │    │  │ running on │  │    │  │ Amber: near│  │
│  │ Site pair  │  │    │  │ source host│  │    │  │  RPO limit │  │
│  │ Connected? │  │    │  └────────────┘  │    │  │ Red: RPO   │  │
│  └────────────┘  │    └──────────────────┘    │  │  VIOLATION │  │
└──────────────────┘                            │  └────────────┘  │
```
                                                └──────────────────┘

---

## VRA and Site Pairing Status

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

## Verify VRA Disk Space

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
