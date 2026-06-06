# Brocade SANnav — Operations Scripts

```bash
#!/usr/bin/env bash
# sannav-auth.sh — obtain and export a SANnav API token

SANNAV_HOST="https://sannav-dc1.corp.example.com"
SANNAV_USER="svc-automation"
SANNAV_PASS="${SANNAV_PASS:-}"  # pass via env variable

if [[ -z "$SANNAV_PASS" ]]; then
  echo "ERROR: Set SANNAV_PASS environment variable"
  exit 1
fi

export SANNAV_TOKEN=$(curl -sk -X POST "${SANNAV_HOST}/rest/login" \
  -H "Content-Type: application/json" \
  -d "{\"credentials\":{\"loginName\":\"${SANNAV_USER}\",\"password\":\"${SANNAV_PASS}\"}}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('authToken',''))")

if [[ -z "$SANNAV_TOKEN" ]]; then
  echo "ERROR: Failed to obtain SANnav token"
  exit 1
fi

echo "Authenticated as ${SANNAV_USER}"

cleanup() {
  curl -sk -X DELETE "${SANNAV_HOST}/rest/logout" \
    -H "Authorization: Bearer ${SANNAV_TOKEN}" > /dev/null
  echo "Session logged out"
}
trap cleanup EXIT
```
```text
┌───────────────────────────────── Brocade SANnav — Operations Scripts ─────────────────────────────────┐
│                                                                                                       │
│  SANnav scripting: REST API automation, zone management, reporting, Ansible playbooks.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              REST API Scripting              │  │           Zone Automation Scripts           │   │
│   │        Auth: POST /api/v1/login token        │  │         Python: create alias + zone         │   │
│   │        GET /api/v1/fabric/switch list        │  │           Ansible: broadcom.sannav          │   │
│   │         GET /api/v1/port/performance         │  │         Validate: cfgshow post-push         │   │
│   │         POST /api/v1/zone to create          │  │          Batch zone from CSV input          │   │
│   │         DELETE /api/v1/zone cleanup          │  │           WWN lookup: nsshow parse          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  REST API enables full zone lifecycle automation; Ansible collection wraps API calls.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Reporting Scripts               │  │             Maintenance Scripts             │   │
│   │         Port utilisation: weekly CSV         │  │          supportsave: all switches          │   │
│   │          Zone audit: unused aliases          │  │          Backup trigger: pre-change         │   │
│   │         SFP inventory: power levels          │  │         Firmware check: ver compare         │   │
│   │          MAPS: alert summary email           │  │          Stale zone cleanup script          │   │
│   │         Fabric topology: PDF report          │  │           Port error daily report           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · REST API port 443 · Brocade FC switches · automation host (Linux/Windows)                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  REST API        = SANnav northbound API; JSON over HTTPS port 443                                    │
│  Token auth      = JWT token issued on login; passed as Bearer in all API requests                    │
│  broadcom.sannav = Ansible Galaxy collection for SANnav automation modules                            │
│  Zone alias      = named grouping of WWNs used as zone member; managed via API                        │
│  cfgshow         = zone config verification; run post-push to confirm zone state                      │
│  nsshow          = name server parse; maps WWPN to device names and ports                             │
│  supportsave     = automated collection of diagnostic bundle from all switches                        │
│  SFP inventory   = REST API retrieves transceiver power levels for predictive alerts                  │
│  Stale zone      = zone with an alias that has no active device login; safe to remove                 │
│  MAPS summary    = automated email report of MAPS violations above threshold                          │
│  WWN             = World Wide Name; 64-bit HBA/port identifier for zone membership                    │
│  CSV input       = bulk zone creation from spreadsheet; scripted via REST API batch                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```python
#!/usr/bin/env python3
# sannav-offline-ports.py

import sys, json, os, csv
import urllib.request, ssl

HOST = "https://sannav-dc1.corp.example.com"
USER = "svc-monitor"
PASS = os.environ.get("SANNAV_PASS", "")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def api_get(path, token):
    req = urllib.request.Request(HOST + path,
          headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.load(r)

# Login
import urllib.parse
req = urllib.request.Request(HOST + "/rest/login", method="POST",
      data=json.dumps({"credentials": {"loginName": USER, "password": PASS}}).encode(),
      headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, context=ctx) as r:
    TOKEN = json.load(r)["authToken"]

try:
    data = api_get("/rest/resourcegroups/all/ports", TOKEN)
    writer = csv.writer(sys.stdout)
    writer.writerow(["Switch", "Port", "Type", "State", "Connected WWN"])
    for p in data.get("ports", []):
        ptype = p.get("portType", "")
        state = p.get("portState", "")
        if ptype in ("F_PORT", "E_PORT") and state != "ONLINE":
            writer.writerow([
                p.get("switchName", ""),
                p.get("portIndex", ""),
                ptype,
                state,
                p.get("connectedWwn", "")
            ])
finally:
    req = urllib.request.Request(HOST + "/rest/logout", method="DELETE",
          headers={"Authorization": f"Bearer {TOKEN}"})
    urllib.request.urlopen(req, context=ctx).close()
```
```bash
#!/usr/bin/env bash
# sannav-zone-export.sh
# Cron: 0 2 * * * /opt/scripts/sannav-zone-export.sh >> /var/log/sannav-zone-export.log 2>&1

SANNAV_HOST="https://sannav-dc1.corp.example.com"
EXPORT_DIR="/opt/sannav-exports/zones"
DATE=$(date +%Y%m%d)

mkdir -p "${EXPORT_DIR}"

# Get token
TOKEN=$(curl -sk -X POST "${SANNAV_HOST}/rest/login" \
  -H "Content-Type: application/json" \
  -d "{\"credentials\":{\"loginName\":\"svc-automation\",\"password\":\"${SANNAV_PASS}\"}}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['authToken'])")

# Get list of fabric IDs
FABRICS=$(curl -sk "${SANNAV_HOST}/rest/resourcegroups" \
  -H "Authorization: Bearer ${TOKEN}" \
  | python3 -c "
import sys,json
data = json.load(sys.stdin)
for rg in data.get('resourceGroups',[]):
    print(rg['id'], rg['name'].replace(' ','-'))
")

# Export zone set for each fabric
while IFS=' ' read -r FABRIC_ID FABRIC_NAME; do
  OUTPUT="${EXPORT_DIR}/${FABRIC_NAME}-zones-${DATE}.json"
  curl -sk "${SANNAV_HOST}/rest/resourcegroups/${FABRIC_ID}/zonedb" \
    -H "Authorization: Bearer ${TOKEN}" \
    -o "${OUTPUT}"
  echo "Exported: ${OUTPUT}"
done <<< "${FABRICS}"

# Cleanup old exports (keep 90 days)
find "${EXPORT_DIR}" -name "*.json" -mtime +90 -delete

# Logout
curl -sk -X DELETE "${SANNAV_HOST}/rest/logout" \
  -H "Authorization: Bearer ${TOKEN}" > /dev/null

echo "Zone export complete: $(date)"
```
```python
#!/usr/bin/env python3
# sannav-firmware-check.py

import sys, json, os
import urllib.request, ssl
from packaging.version import Version  # pip install packaging

HOST = "https://sannav-dc1.corp.example.com"
PASS = os.environ.get("SANNAV_PASS", "")

# Minimum approved firmware by model prefix
BASELINE = {
    "G730": "9.2.1a",
    "G720": "9.2.1a",
    "G630": "9.1.1c",
    "G620": "9.1.1c",
    "G610": "9.1.1c",
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(HOST + "/rest/login", method="POST",
      data=json.dumps({"credentials": {"loginName": "svc-monitor", "password": PASS}}).encode(),
      headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, context=ctx) as r:
    TOKEN = json.load(r)["authToken"]

req = urllib.request.Request(HOST + "/rest/resourcegroups/all/switches",
      headers={"Authorization": f"Bearer {TOKEN}"})
with urllib.request.urlopen(req, context=ctx) as r:
    switches = json.load(r).get("switches", [])

non_compliant = []
for sw in switches:
    model = sw.get("model", "")
    fw = sw.get("firmwareVersion", "")
    for prefix, min_ver in BASELINE.items():
        if model.startswith(prefix):
            try:
                if Version(fw.replace("v","")) < Version(min_ver):
                    non_compliant.append((sw["name"], model, fw, min_ver))
            except Exception:
                pass

if non_compliant:
    print(f"NON-COMPLIANT SWITCHES ({len(non_compliant)}):")
    for name, model, fw, required in non_compliant:
        print(f"  {name:<30} {model:<10} current={fw:<10} required>={required}")
    sys.exit(1)
else:
    print(f"All {len(switches)} switches meet firmware baseline.")

req = urllib.request.Request(HOST + "/rest/logout", method="DELETE",
      headers={"Authorization": f"Bearer {TOKEN}"})
urllib.request.urlopen(req, context=ctx).close()
```
