# Aria Suite Lifecycle — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Service Status Verification, Certificate Expiry Checks, Disk Space Verification, NTP and Time Sync, Pre-Operation Health Summary.
</div>

  LCM Diagnostic Data Sources
```text
┌─────────────────────────────────────────────────────────────────┐
│  LCM Appliance (SSH as root)       LCM API                      │
│  ┌───────────────────────────┐     ┌──────────────────────────┐  │
│  │ vracli support-bundle     │     │ GET /lcm/api/v1/health   │  │
│  │ /var/log/vmware/vrlcm/    │     │ GET /api/v2/environments │  │
│  │  lcm-app.log (main)       │     │  → health per product    │  │
│  │  lcm-install.log (deploy) │     │ GET /api/v2/requests     │  │
│  │  locker.log (cert/pw ops) │     │  ?state=RUNNING          │  │
│  │  upgrade/ (per upgrade)   │     └──────────────────────────┘  │
│  └───────────────────────────┘                                   │
│                                                                  │
│  System Checks                     Certificate Checks            │
│  ┌───────────────────────────┐     ┌──────────────────────────┐  │
│  │ systemctl list-units      │     │ openssl s_client :443    │  │
│  │  --type=service | grep lcm│     │ GET /api/v1/certificates │  │
│  │ df -h (disk thresholds)   │     │  days-to-expiry          │  │
│  │ chronyc tracking (NTP)    │     └──────────────────────────┘  │
│  └───────────────────────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Aria Suite LCM Diagnostics ──────────────────────────────────────┐
│                                                                                                       │
│  Logscraper, vlcm log analysis, and environment health checks for LCM.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               LCM Log Analysis               │  │            REST API Health Checks           │   │
│   │            /var/log/vlcm/vlcm.log            │  │            GET /lcm/api/v1/health           │   │
│   │         installer.log: deploy steps          │  │           GET /environments status          │   │
│   │             grep ERROR vlcm.log              │  │           GET /products: versions           │   │
│   │         Check failed request ID log          │  │          Compare expected vs actual         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  vlcm.log reveals LCM internal errors; REST health confirms product state externally.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Logscraper Usage               │  │                Support Bundle               │   │
│   │          LCM UI: Tools > Logscraper          │  │             SSH: lcm-support.sh             │   │
│   │        Select environment + products         │  │             Bundle: all LCM logs            │   │
│   │           Download log archive ZIP           │  │           Logscraper + bundle = SR          │   │
│   │               Attach to GSS SR               │  │        VAMI: download support bundle        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM; SSH jump host; VAMI on port 5480; all managed product VMs accessible                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vlcm.log            = Primary LCM application log; first stop for any LCM issue                      │
│  installer.log       = Records each step of product deploy or upgrade action                          │
│  Logscraper          = LCM built-in tool collecting logs from all managed products                    │
│  Logscraper Archive  = ZIP of all product logs; generated per environment                             │
│  lcm-support.sh      = SSH script generating LCM-level support bundle                                 │
│  GET /health         = REST API endpoint for LCM and product health JSON                              │
│  GET /environments   = Lists environments with status for comparison                                  │
│  GET /products       = Lists product versions; validate against expected                              │
│  Request ID Log      = LCM writes per-request log for each action triggered                           │
│  grep ERROR          = Quick scan of vlcm.log to find exception lines                                 │
│  VAMI Support Bundle = Browser download of LCM support archive                                        │
│  GSS SR Attachment   = Logscraper archive + support bundle required for P1/P2                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

Key services and expected states:

| Service | Expected State | Notes |
|---|---|---|
| `vmware-vrlcm` | active (running) | Core LCM service |
| `vmware-vrlcm-db` | active (running) | Embedded Postgres |
| `nginx` | active (running) | Reverse proxy / UI |
| `vmware-vrlcm-certmanager` | active (running) | Certificate management |
| `sshd` | active (running) | Required for remote access |

## Certificate Expiry Checks

```bash
# Check LCM appliance certificate
openssl s_client -connect <lcm-fqdn>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates

# List all managed product certificates via LCM API
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/certificates \
  | python3 -m json.tool

# Check certificate expiry for a specific product
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/certificates?productId=<product-id>" \
  | python3 -m json.tool

# Trigger certificate rotation via LCM API
curl -sk -X POST -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/certificates/rotate \
  -H "Content-Type: application/json" \
  -d '{"productId": "<product-id>"}'
```

Certificate check thresholds:

| Days to Expiry | Status | Action |
|---|---|---|
| > 90 days | Healthy | No action required |
| 30–90 days | Warning | Plan rotation |
| 7–30 days | Critical | Rotate within a week |
| < 7 days | Emergency | Rotate immediately |

## Disk Space Verification

```bash
# Check all mount points
df -h

# Check LCM-specific data directories
du -sh /data/vmware/vrlcm/*
du -sh /var/log/vmware/vrlcm/

# Check Postgres database size
du -sh /data/vmware/vrlcm/db/

# Clean old LCM logs older than 30 days
find /var/log/vmware/vrlcm/ -name "*.log.*" -mtime +30 -delete

# Check available inodes (often missed)
df -i
```

Disk space thresholds:

| Mount | Warning | Critical | Action if Critical |
|---|---|---|---|
| `/` | 75% | 85% | Remove old bundles and logs |
| `/data` | 70% | 80% | Clean old content library cache |
| `/var/log` | 80% | 90% | Rotate and archive logs |

## NTP and Time Sync

```bash
# Check NTP sync status
timedatectl status

# Check chrony sources
chronyc sources -v

# Check time offset (must be < 5 seconds for SSO)
chronyc tracking | grep "System time"

# Force time sync
chronyc makestep

# Verify NTP config
cat /etc/chrony.conf
```

## Pre-Operation Health Summary

Before any LCM operation (upgrade, patch, certificate rotation), confirm all of the following pass:

```bash
# 1. All services running
systemctl is-active vmware-vrlcm vmware-vrlcm-db nginx

# 2. Disk space adequate
df -h | awk 'NR>1 && $5+0 > 70 {print "WARNING:", $0}'

# 3. No active LCM operations in progress
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/operations?status=RUNNING" \
  | python3 -m json.tool

# 4. NTP in sync
chronyc tracking | grep "System time"

# 5. LCM API reachable and healthy
curl -sk -o /dev/null -w "%{http_code}" https://<lcm-fqdn>/lcm/api/v1/health
```
