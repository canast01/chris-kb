# Aria Operations for Networks — Diagnostics

```text
┌────────────── Aria Networks Diagnostics: Support Bundle ───────────────────────┐
│                                                                                 │
│  Fastest path: UI ► Settings ► Support ► Download Support Bundle               │
│  (includes Platform + all Collector logs, system state, config)                 │
│                                                                                 │
│  Manual log collection if UI unavailable:                                       │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Platform VM                                                             │  │
│  │  /var/log/vmware/hms/      ── core platform service                    │    │
│  │  journalctl -u hms -f      ── follow HMS service log                   │    │
│  │  journalctl -u nginx -f    ── API gateway log                          │    │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Collector VM                                                            │  │
│  │  /var/log/vmware/collector/ ── data collection logs                    │    │
│  │  journalctl -u hms -f       ── collector agent log                     │    │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  Connectivity tests (from Collector VM):                                         │
│  curl -sk https://<vcenter>/rest/.../session  ── vCenter API                   │
│  curl -sk https://<nsxmgr>/api/v1/cluster     ── NSX API                       │
│  nc -vz <platform> 443                        ── upload path                   │
│  tcpdump -i eth0 udp port 2055                ── NetFlow arriving               │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Support Bundle

Collect the support bundle before opening a case — it includes Platform and Collector logs, system state, and configuration.

```text
Settings → Support → Download Support Bundle
  Select: Platform + All Collectors
  Download and attach to VMware Support case
```

---

## Platform VM Log Locations

```bash
ssh ubuntu@vrni.example.local

# Main application logs
/var/log/vmware/hms/           # Home Management Server — core platform service
/var/log/vmware/ni-proxy/      # API proxy
/var/log/vmware/vcops/         # Analytics engine

# System logs
/var/log/syslog                # OS syslog
journalctl -u hms -f           # Follow HMS service log
journalctl -u nginx -f         # Nginx (API gateway) log

# Check HMS service status
sudo systemctl status hms
sudo systemctl status nginx
```

---

## Collector VM Log Locations

```bash
ssh admin@<collector-vm-ip>

/var/log/vmware/hms/           # Collector HMS agent
/var/log/vmware/collector/     # Data collection logs

# Check services
sudo systemctl status hms
sudo systemctl status collector

# Real-time collector log
journalctl -u hms -f
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
