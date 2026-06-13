---
tags:
  - aria-networks
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Operations for Networks — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Support Bundle, Collector VM Log Locations, Test Data Source Connectivity, Verify NetFlow Receipt, Check Data Source Last-Sync via API and 3 more sections.

*Applies to: Aria Networks 6.x*
</div>

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Support Bundle

Collect the support bundle before opening a case — it includes Platform and Collector logs, system state, and configuration.

```text
┌────────────────────────────────────────── vRNI Diagnostics ───────────────────────────────────────────┐
│                                                                                                       │
│  app.log analysis, REST API diagnostic checks, and support bundle for vRNI.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Log File Diagnostics             │  │               REST API Checks               │   │
│   │          /var/log/app.log: main log          │  │           GET /api/ni/infra/health          │   │
│   │          /var/log/proxy.log: flows           │  │          GET /data-sources: status          │   │
│   │              grep ERROR app.log              │  │          GET /flows: verify receipt         │   │
│   │         Check timestamp of last flow         │  │           GET /entities/vms: count          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Logs reveal internal errors; REST API checks validate data availability from outside.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Support Bundle                │  │            Collector Diagnostics            │   │
│   │         SSH: support-bundle generate         │  │               SSH collector VM              │   │
│   │          VAMI: download bundle ZIP           │  │           tail /var/log/proxy.log           │   │
│   │           Bundle includes all logs           │  │           service collector status          │   │
│   │               Attach to GSS SR               │  │           ping platform from coll           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform + collector VMs; SSH jump host; VAMI browser access on port 5480                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  app.log             = Primary platform log: errors, auth events, analytics issues                    │
│  proxy.log           = Collector log: flow receipt rate and forwarding to platform                    │
│  GET /infra/health    = REST endpoint returning component health status JSON                          │
│  Support Bundle      = Compressed archive of all logs; generated via SSH or VAMI                      │
│  GSS SR              = Global Support Services case; attach bundle for analysis                       │
│  grep ERROR          = Quick scan of app.log for exception and error entries                          │
│  Flow Timestamp      = Last-seen time on flow records; stale = collection stopped                     │
│  GET /entities/vms   = Returns VM count; empty = vCenter source not syncing                           │
│  service collector   = Systemd service on collector VM; check status first                            │
│  ping platform       = Basic connectivity test from collector to platform IP                          │
│  VAMI Download       = Browser-based support bundle download from port 5480                           │
│  Collector Log Level = Adjust in collector config for verbose debugging output                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
---

## Test Data Source Connectivity

```bash
# From Collector VM — test vCenter API
curl -sk https://<vcenter-ip>/rest/com/vmware/cis/session \
  -X POST -u svc-vrni-vc@corp.local:<password>
# Should return a session token

# From Collector VM — test NSX Manager API
curl -sk -u svc-vrni-nsx:<password> \
  https://<nsx-manager-ip>/api/v1/cluster/status | python3 -m json.tool

# From Collector VM — test port connectivity
nc -vz <platform-vm-ip> 443
nc -vz <vcenter-ip> 443
nc -vz <nsx-manager-ip> 443
```

---

## Verify NetFlow Receipt

```bash
# On Collector VM — capture NetFlow UDP 2055 traffic
sudo tcpdump -i eth0 -n udp port 2055 -c 20

# If packets appear, NetFlow is arriving — check vRNI data source configuration
# If no packets, the switch is not sending or UDP 2055 is blocked by firewall
```

---

## Check Data Source Last-Sync via API

```bash
TOKEN=$(curl -sk -X POST https://vrni.example.local/api/ni/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<pass>","domain":{"domain_type":"LOCAL"}}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

# List vCenter data sources with status
curl -sk -H "Authorization: NetworkInsight $TOKEN" \
  "https://vrni.example.local/api/ni/data-sources/vcenters" \
  | python3 -c "
import json,sys
for ds in json.load(sys.stdin).get('results', []):
    print(ds['ip'], '|', ds.get('nickname',''), '|', ds.get('connection_status',''))
"
```

---

## REST API Health Endpoint

```bash
# Check Platform API health (no auth required)
curl -sk https://vrni.example.local/api/ni/health
# Response should be {"status":"OK"} or similar

# Check API version
curl -sk https://vrni.example.local/api/ni/info
```

---

## Disk Space Check

```bash
# Platform VM
df -h /data    # vRNI data partition
df -h /var/log # Log partition

# Collector VM
df -h          # Overall disk usage

# If /data is full on Platform VM, old config backups can be removed:
ls -lh /data/backup/
sudo rm -rf /data/backup/<old-backup-date>/
```

---

## Certificate Diagnostics

```bash
# Check current Platform VM certificate
echo | openssl s_client -connect vrni.example.local:443 -servername vrni.example.local 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer

# Check if cert is from expected CA
echo | openssl s_client -connect vrni.example.local:443 2>/dev/null \
  | openssl x509 -noout -issuer
```
