# Cisco DCNM — Scripts

> Part of the [Cisco DCNM](../../index.md) reference.

---

## Overview

Automation scripts for DCNM via the REST API. All scripts use `curl` and Python 3 standard library. Adapt `DCNM_HOST`, `DCNM_USER`, and `DCNM_PASS` for your environment. Pass `DCNM_PASS` via environment variable, never hard-code it.

---

## Authentication Helper

```bash
#!/usr/bin/env bash
# dcnm-auth.sh — obtain a DCNM session cookie

DCNM_HOST="https://dcnm-dc1.corp.example.com"
DCNM_USER="svc-automation"
COOKIE_FILE="/tmp/dcnm-cookie-$$.txt"

if [[ -z "$DCNM_PASS" ]]; then
  echo "ERROR: Set DCNM_PASS environment variable"
  exit 1
fi

curl -sk -c "${COOKIE_FILE}" -X POST \
  "${DCNM_HOST}/rest/logon" \
  -H "Content-Type: application/json" \
  -d '{"expirationTime": 3600}' \
  -u "${DCNM_USER}:${DCNM_PASS}" > /dev/null

if [[ ! -s "${COOKIE_FILE}" ]]; then
  echo "ERROR: Authentication failed"
  exit 1
fi

export COOKIE_FILE DCNM_HOST

cleanup() {
  curl -sk -b "${COOKIE_FILE}" -X POST "${DCNM_HOST}/rest/logout" > /dev/null
  rm -f "${COOKIE_FILE}"
}
trap cleanup EXIT
echo "Authenticated to ${DCNM_HOST}"
```

---

## Switch Inventory Export

```bash
#!/usr/bin/env bash
# dcnm-switch-inventory.sh

source ./dcnm-auth.sh

OUTPUT="dcnm-switches-$(date +%Y%m%d).csv"

curl -sk -b "${COOKIE_FILE}" "${DCNM_HOST}/rest/inventory/switches" \
  | python3 - <<'EOF'
import sys, json, csv

data = json.load(sys.stdin)
fields = ["switchName","ipAddress","model","release","managementState",
          "fabricName","serialNumber","switchRole"]

writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
writer.writeheader()
for sw in data:
    writer.writerow({f: sw.get(f,"") for f in fields})
EOF

echo "Export complete: ${OUTPUT}"
```

---

## Fabric Health Report

Generates a concise health summary for all fabrics: switch count, unmanageable switches, active alarms:

```python
#!/usr/bin/env python3
# dcnm-fabric-health.py

import sys, json, os
import urllib.request, http.cookiejar, ssl

HOST = "https://dcnm-dc1.corp.example.com"
USER = "svc-monitor"
PASS = os.environ.get("DCNM_PASS", "")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.HTTPCookieProcessor(jar)
)

# Login
req = urllib.request.Request(HOST + "/rest/logon", method="POST",
      data=json.dumps({"expirationTime": 600}).encode(),
      headers={"Content-Type": "application/json",
               "Authorization": "Basic " + __import__("base64").b64encode(
                   f"{USER}:{PASS}".encode()).decode()})
opener.open(req)

def get(path):
    with opener.open(HOST + path) as r:
        return json.load(r)

try:
    switches = get("/rest/inventory/switches")
    alarms = get("/rest/alarms/activealarms")

    # Group by fabric
    fabrics = {}
    for sw in switches:
        fn = sw.get("fabricName", "unknown")
        fabrics.setdefault(fn, {"total": 0, "unmanageable": []})
        fabrics[fn]["total"] += 1
        if sw.get("managementState") != "manageable":
            fabrics[fn]["unmanageable"].append(sw.get("switchName", sw.get("ipAddress")))

    critical_alarms = [a for a in alarms if a.get("severity") in ("CRITICAL","critical")]

    print(f"{'Fabric':<25} {'Switches':<10} {'Unmanageable'}")
    print("-" * 55)
    for fabric, data in sorted(fabrics.items()):
        unman = ", ".join(data["unmanageable"]) if data["unmanageable"] else "none"
        print(f"{fabric:<25} {data['total']:<10} {unman}")

    print(f"\nActive critical alarms: {len(critical_alarms)}")
    for a in critical_alarms[:10]:
        print(f"  [{a.get('severity')}] {a.get('message','')[:80]}")

finally:
    req = urllib.request.Request(HOST + "/rest/logout", method="POST")
    opener.open(req)
```

---

## Zone Database Export (All Fabrics)

Nightly cron job to export zone sets for all fabrics:

```bash
#!/usr/bin/env bash
# dcnm-zone-export.sh
# Cron: 0 1 * * * /opt/scripts/dcnm-zone-export.sh >> /var/log/dcnm-zone-export.log 2>&1

DCNM_HOST="https://dcnm-dc1.corp.example.com"
EXPORT_DIR="/opt/dcnm-exports/zones"
DATE=$(date +%Y%m%d)

mkdir -p "${EXPORT_DIR}"

# Auth
COOKIE_FILE="/tmp/dcnm-zone-export-$$.txt"
curl -sk -c "${COOKIE_FILE}" -X POST "${DCNM_HOST}/rest/logon" \
  -H "Content-Type: application/json" -d '{"expirationTime":600}' \
  -u "svc-automation:${DCNM_PASS}" > /dev/null

trap "curl -sk -b ${COOKIE_FILE} -X POST ${DCNM_HOST}/rest/logout > /dev/null; rm -f ${COOKIE_FILE}" EXIT

# Get fabric list
FABRICS=$(curl -sk -b "${COOKIE_FILE}" "${DCNM_HOST}/rest/san/fabric" \
  | python3 -c "import sys,json; [print(f['fabricName']) for f in json.load(sys.stdin)]")

for FABRIC in ${FABRICS}; do
  OUTPUT="${EXPORT_DIR}/${FABRIC}-zones-${DATE}.json"
  curl -sk -b "${COOKIE_FILE}" \
    "${DCNM_HOST}/rest/san/zoning?fabricName=${FABRIC}" \
    -o "${OUTPUT}"
  echo "Exported: ${OUTPUT}"
done

# Cleanup: keep 90 days
find "${EXPORT_DIR}" -name "*-zones-*.json" -mtime +90 -delete
echo "Zone export complete: $(date)"
```

---

## Firmware Compliance Check

Checks all switches against minimum firmware version per model:

```python
#!/usr/bin/env python3
# dcnm-firmware-check.py

import sys, json, os, re
import urllib.request, http.cookiejar, ssl

HOST = "https://dcnm-dc1.corp.example.com"
PASS = os.environ.get("DCNM_PASS", "")

# Min firmware by MDS model prefix (NX-OS version string matching)
BASELINE = {
    "MDS 9718": "8.4(2a)",
    "MDS 9710": "8.4(2a)",
    "MDS 9706": "8.4(2a)",
    "MDS 9396T": "8.4(2a)",
    "MDS 9148T": "8.4(2a)",
    "MDS 9132T": "8.4(2a)",
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.HTTPCookieProcessor(jar)
)

req = urllib.request.Request(HOST + "/rest/logon", method="POST",
      data=json.dumps({"expirationTime": 300}).encode(),
      headers={"Content-Type": "application/json",
               "Authorization": "Basic " + __import__("base64").b64encode(
                   f"svc-monitor:{PASS}".encode()).decode()})
opener.open(req)

try:
    with opener.open(HOST + "/rest/inventory/switches") as r:
        switches = json.load(r)

    non_compliant = []
    for sw in switches:
        model = sw.get("model", "")
        fw = sw.get("release", "")
        for prefix, min_ver in BASELINE.items():
            if model.startswith(prefix):
                # Simple string comparison works for NX-OS versions of same major
                if fw < min_ver:
                    non_compliant.append((sw["switchName"], model, fw, min_ver))

    if non_compliant:
        print(f"NON-COMPLIANT ({len(non_compliant)} switches):")
        for name, model, fw, req_ver in non_compliant:
            print(f"  {name:<35} {model:<15} current={fw:<12} min={req_ver}")
        sys.exit(1)
    else:
        print(f"OK: All {len(switches)} switches meet firmware baseline.")

finally:
    req = urllib.request.Request(HOST + "/rest/logout", method="POST")
    opener.open(req)
```
