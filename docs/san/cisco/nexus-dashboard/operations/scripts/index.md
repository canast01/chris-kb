# Nexus Dashboard — Scripts

> Part of the [Nexus Dashboard](../../) reference.

---

## Overview

Automation scripts for Nexus Dashboard and NDFC via the REST API. All scripts use `curl` and Python 3 standard library. Set `ND_HOST`, `ND_USER`, and `ND_PASS` (via environment variable) before use.

---

## Authentication Helper

```bash
#!/usr/bin/env bash
# nd-auth.sh — obtain a Nexus Dashboard API token

ND_HOST="${ND_HOST:-https://nd-dc1.corp.example.com}"
ND_USER="${ND_USER:-svc-automation}"

if [[ -z "${ND_PASS}" ]]; then
  echo "ERROR: Set ND_PASS environment variable"
  exit 1
fi

export ND_TOKEN=$(curl -sk -X POST "${ND_HOST}/login" \
  -H "Content-Type: application/json" \
  -d "{\"userName\":\"${ND_USER}\",\"userPasswd\":\"${ND_PASS}\",\"domain\":\"local\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('token',''))")

if [[ -z "${ND_TOKEN}" ]]; then
  echo "ERROR: Failed to obtain ND token — check credentials and ND_HOST"
  exit 1
fi

echo "Authenticated to ${ND_HOST} as ${ND_USER}"

cleanup() {
  curl -sk -X POST "${ND_HOST}/logout" \
    -H "Authorization: Bearer ${ND_TOKEN}" > /dev/null
  echo "Session logged out"
}
trap cleanup EXIT
```

---

## NDFC Switch Inventory Export

Exports all managed switches to CSV including management state and firmware version:

```bash
#!/usr/bin/env bash
# nd-switch-inventory.sh

ND_HOST="${ND_HOST:-https://nd-dc1.corp.example.com}"
NDFC="${ND_HOST}/appcenter/cisco/ndfc/api/v1"

source ./nd-auth.sh

OUTPUT="nd-switches-$(date +%Y%m%d).csv"

curl -sk "${NDFC}/inventory/switches" \
  -H "Authorization: Bearer ${ND_TOKEN}" \
  | python3 - <<'PYEOF'
import sys, json, csv

data = json.load(sys.stdin)
fields = ["switchName","ipAddress","model","release","managementState",
          "fabricName","serialNumber","switchRole"]

writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
writer.writeheader()
for sw in data:
    writer.writerow({f: sw.get(f,"") for f in fields})
PYEOF

echo "Export complete: ${OUTPUT}"
```

---

## ND Cluster Health Check

Reports cluster node health and NDFC fabric status — suitable for nagios/Icinga or a CI health gate:

```python
#!/usr/bin/env python3
# nd-health-check.py

import sys, json, os, urllib.request, ssl

ND_HOST = os.environ.get("ND_HOST", "https://nd-dc1.corp.example.com")
ND_USER = os.environ.get("ND_USER", "svc-monitor")
ND_PASS = os.environ.get("ND_PASS", "")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def login():
    req = urllib.request.Request(ND_HOST + "/login", method="POST",
          data=json.dumps({"userName": ND_USER, "userPasswd": ND_PASS,
                           "domain": "local"}).encode(),
          headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.load(r)["token"]

def get(path, token):
    req = urllib.request.Request(ND_HOST + path,
          headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.load(r)

TOKEN = login()
issues = []

try:
    # Check cluster nodes
    nodes = get("/nexus/api/v1/nodes", TOKEN)
    unhealthy = [n["hostname"] for n in nodes
                 if n.get("status","") != "healthy"]
    if unhealthy:
        issues.append(f"Unhealthy nodes: {', '.join(unhealthy)}")

    # Check NDFC switches
    switches = get("/appcenter/cisco/ndfc/api/v1/inventory/switches", TOKEN)
    unmanageable = [s["switchName"] for s in switches
                    if s.get("managementState","") not in ("manageable","managed")]
    if unmanageable:
        issues.append(f"Unmanageable switches: {', '.join(unmanageable[:5])}"
                      + (f" (+{len(unmanageable)-5} more)" if len(unmanageable) > 5 else ""))

    if issues:
        print("WARNING: " + "; ".join(issues))
        sys.exit(1)
    else:
        print(f"OK: {len(nodes)} nodes healthy, {len(switches)} switches managed")
        sys.exit(0)

finally:
    urllib.request.urlopen(
        urllib.request.Request(ND_HOST + "/logout", method="POST",
        headers={"Authorization": f"Bearer {TOKEN}"}), context=ctx
    ).close()
```

---

## Zone Database Nightly Export

Exports zone databases for all NDFC fabrics each night:

```bash
#!/usr/bin/env bash
# nd-zone-export.sh
# Cron: 0 2 * * * /opt/scripts/nd-zone-export.sh >> /var/log/nd-zone-export.log 2>&1

ND_HOST="${ND_HOST:-https://nd-dc1.corp.example.com}"
NDFC="${ND_HOST}/appcenter/cisco/ndfc/api/v1"
EXPORT_DIR="/opt/nd-exports/zones"
DATE=$(date +%Y%m%d)

mkdir -p "${EXPORT_DIR}"

# Authenticate
TOKEN=$(curl -sk -X POST "${ND_HOST}/login" \
  -H "Content-Type: application/json" \
  -d "{\"userName\":\"svc-automation\",\"userPasswd\":\"${ND_PASS}\",\"domain\":\"local\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

trap "curl -sk -X POST '${ND_HOST}/logout' -H 'Authorization: Bearer ${TOKEN}' > /dev/null" EXIT

# Get fabric list
FABRICS=$(curl -sk "${NDFC}/san/fabrics" \
  -H "Authorization: Bearer ${TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for f in data.get('DATA', data if isinstance(data,list) else []):
    print(f.get('fabricName',''))
")

# Export zone DB for each fabric
for FABRIC in ${FABRICS}; do
  OUTPUT="${EXPORT_DIR}/${FABRIC}-zones-${DATE}.json"
  curl -sk "${NDFC}/san/zoning?fabricName=${FABRIC}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -o "${OUTPUT}"
  echo "Exported: ${OUTPUT}"
done

# Purge exports older than 90 days
find "${EXPORT_DIR}" -name "*-zones-*.json" -mtime +90 -delete

echo "Zone export complete: $(date)"
```

---

## NDI Anomaly Summary Report

Generates a daily anomaly summary and emails it to the SAN team:

```python
#!/usr/bin/env python3
# nd-anomaly-report.py

import os, json, sys, smtplib, ssl, urllib.request
from email.mime.text import MIMEText
from datetime import datetime

ND_HOST = os.environ.get("ND_HOST", "https://nd-dc1.corp.example.com")
ND_PASS = os.environ.get("ND_PASS", "")
NDI = f"{ND_HOST}/appcenter/cisco/ndinsight/api/v1"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login
req = urllib.request.Request(ND_HOST + "/login", method="POST",
      data=json.dumps({"userName":"svc-monitor","userPasswd":ND_PASS,
                       "domain":"local"}).encode(),
      headers={"Content-Type":"application/json"})
with urllib.request.urlopen(req, context=ctx) as r:
    TOKEN = json.load(r)["token"]

try:
    req = urllib.request.Request(
        f"{NDI}/anomalies?timeRange=LAST_DAY",
        headers={"Authorization": f"Bearer {TOKEN}"})
    with urllib.request.urlopen(req, context=ctx) as r:
        anomalies = json.load(r).get("DATA", [])

    by_severity = {}
    for a in anomalies:
        sev = a.get("severity","UNKNOWN")
        by_severity.setdefault(sev, []).append(a)

    lines = [f"NDI Anomaly Summary — {datetime.utcnow().strftime('%Y-%m-%d')}",
             "=" * 50]
    for sev in ("CRITICAL","MAJOR","MINOR","WARNING"):
        count = len(by_severity.get(sev, []))
        lines.append(f"{sev}: {count}")
    lines.append("")
    for a in by_severity.get("CRITICAL", [])[:10]:
        lines.append(f"[CRITICAL] {a.get('title','')}: {a.get('description','')[:80]}")

    body = "\n".join(lines)
    print(body)

    # Send email
    msg = MIMEText(body)
    msg["Subject"] = f"NDI Daily Anomaly Report — {datetime.utcnow().strftime('%Y-%m-%d')}"
    msg["From"] = "nexus-dashboard@corp.example.com"
    msg["To"] = "san-team@corp.example.com"

    with smtplib.SMTP("smtp.corp.example.com", 587) as smtp:
        smtp.starttls()
        smtp.send_message(msg)

finally:
    urllib.request.urlopen(
        urllib.request.Request(ND_HOST + "/logout", method="POST",
        headers={"Authorization": f"Bearer {TOKEN}"}), context=ctx
    ).close()
```

---

## NDFC Firmware Compliance Check

Checks all switches against minimum NX-OS firmware baseline:

```python
#!/usr/bin/env python3
# nd-firmware-check.py

import os, sys, json, urllib.request, ssl

ND_HOST = os.environ.get("ND_HOST", "https://nd-dc1.corp.example.com")
ND_PASS = os.environ.get("ND_PASS", "")
NDFC = f"{ND_HOST}/appcenter/cisco/ndfc/api/v1"

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

req = urllib.request.Request(ND_HOST + "/login", method="POST",
      data=json.dumps({"userName":"svc-monitor","userPasswd":ND_PASS,
                       "domain":"local"}).encode(),
      headers={"Content-Type":"application/json"})
with urllib.request.urlopen(req, context=ctx) as r:
    TOKEN = json.load(r)["token"]

req = urllib.request.Request(f"{NDFC}/inventory/switches",
      headers={"Authorization": f"Bearer {TOKEN}"})
with urllib.request.urlopen(req, context=ctx) as r:
    switches = json.load(r)

non_compliant = []
for sw in switches:
    model = sw.get("model","")
    fw = sw.get("release","")
    for prefix, min_ver in BASELINE.items():
        if model.startswith(prefix) and fw < min_ver:
            non_compliant.append((sw.get("switchName",""), model, fw, min_ver))

if non_compliant:
    print(f"NON-COMPLIANT ({len(non_compliant)} switches):")
    for name, model, fw, req_ver in non_compliant:
        print(f"  {name:<35} {model:<15} current={fw} min={req_ver}")
    sys.exit(1)
else:
    print(f"OK: All {len(switches)} switches meet firmware baseline.")

urllib.request.urlopen(
    urllib.request.Request(ND_HOST + "/logout", method="POST",
    headers={"Authorization": f"Bearer {TOKEN}"}), context=ctx
).close()
```
