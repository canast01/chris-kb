---
tags:
  - aria-lcm
  - operations
  - vmware
---
# Aria Suite Lifecycle — Health Checks


<div class="kb-summary">
Health Checks reference covering Cluster Node Health via API, Locker Health Checks, Pre-Upgrade Health Gate, Checking Product Health via LCM API, Log File Locations.

*Applies to: Aria LCM 8.x*
</div>

  LCM Health Check Chain
```text
┌──────────────────────────────────── Aria Suite LCM Health Checks ─────────────────────────────────────┐
│                                                                                                       │
│  Product health, depot connectivity, and certificate expiry checks for LCM.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             LCM Appliance Health             │  │            Product Health Checks            │   │
│   │            vlcm service running?             │  │          LCM: Environments > Health         │   │
│   │            Disk < 80% on LCM VM?             │  │         All products: Green status?         │   │
│   │                 NTP in sync?                 │  │         vIDM: accessible + auth OK?         │   │
│   │               VAMI accessible?               │  │          vROps: collection active?          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  LCM appliance health feeds into product health; depot and cert checks follow.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Depot Connectivity              │  │              Certificate Health             │   │
│   │          Depot: sync status green?           │  │           Certs: expiry > 30 days?          │   │
│   │         Binaries: latest available?          │  │           LCM cert dashboard check          │   │
│   │          Network: depot reachable?           │  │             Renew expiring certs            │   │
│   │             Local NFS: mount OK?             │  │           Validate after rotation           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; NFS for depot/backup; internet or proxy for online depot                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vlcm Service        = LCM main service; check status if UI is unresponsive                           │
│  Product Health      = LCM Environments page showing green/yellow/red per product                     │
│  Depot Sync          = LCM download of latest product PAK catalog from VMware                         │
│  Cert Dashboard      = LCM page listing all managed certs with expiry dates                           │
│  Cert Expiry         = Days remaining on TLS cert; alert at 60/30/14 day marks                        │
│  NFS Mount           = Local depot content share; unmounted = install/upgrade fails                   │
│  vIDM Health         = vIDM reachable and authenticating; critical for all products                   │
│  NTP Sync            = LCM and all product VMs must sync to same NTP source                           │
│  Disk Usage          = LCM disk fills with PAK files; monitor and clean old content                   │
│  Green Status        = Product health indicator; all services running correctly                       │
│  Pre-check Result    = LCM validation output; review before any upgrade action                        │
│  Logscraper          = Run after health check failure to collect diagnostic logs                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Run these 8 checks in order at the start of each shift or before any planned change.

1. **LCM service health** — `curl -sk https://<lcm-appliance>:8080/lcm/health` — expect `{"status":"UP"}`
2. **Disk usage** — SSH to LCM appliance and run `df -h /` — flag if root partition is above 75%
3. **Certificate expiry** — LCM UI → Settings → Certificates → review all expiry dates; renew anything within 30 days
4. **Product environment health** — LCM → Environments → confirm every product card shows "Healthy"
5. **Pending requests** — LCM → Requests → check for any operations in RUNNING or FAILED state longer than 30 minutes
6. **vRSLCM service status** — SSH to appliance → `systemctl status vrlcm.service` — must be active (running)
7. **NTP sync** — SSH to appliance → `timedatectl status` — confirm system clock is synchronised
8. **Available product binaries in Locker** — LCM → Locker → verify expected product versions are present before any upgrade

---

## Locker Health Checks

The Locker stores certificates, passwords, and licences. Run these checks weekly and before any upgrade.

```bash
# List all certificates and days-to-expiry
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.example.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/locker/api/v2/certificates" | \
  jq '.certificates[] | {alias: .alias, expiry: .expirationDate, days: .daysToExpiry}' | \
  jq -s 'sort_by(.days)'

# List all passwords stored in Locker
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/locker/api/v2/passwords" | \
  jq '.passwords[] | {alias: .alias, username: .userName}'
```

UI path: **LCM → Locker → Certificates** — columns show Alias, Subject, Expiry, and Status. Sort by Expiry to identify near-term renewals.

| Certificate Status | Meaning | Action |
|---|---|---|
| Valid | More than 60 days remaining | No action required |
| Expiring Soon | 30–60 days remaining | Schedule renewal |
| Critical | Less than 30 days remaining | Renew immediately |
| Expired | Past expiry date | Product integration failures likely — renew now |

---

## Pre-Upgrade Health Gate

Run this checklist before initiating any LCM-orchestrated upgrade:

- [ ] All environment cards show green in **Lifecycle Operations → Environments**
- [ ] No in-progress requests: **Lifecycle Operations → Requests** — no RUNNING or PENDING items
- [ ] LCM appliance disk `/` < 70% used, `/data` < 75% used
- [ ] NFS mount active and responsive: `df -h /data && touch /data/.healthtest && rm /data/.healthtest`
- [ ] NTP delta < 5 seconds on LCM appliance: `chronyc tracking`
- [ ] No certificates expiring within 7 days (would be invalidated mid-upgrade)
- [ ] VM snapshot taken for each product appliance being upgraded
- [ ] vCenter with target product VMs is accessible from LCM
- [ ] LCM pre-check passes (LCM runs pre-check automatically when Upgrade is clicked)

---

## Checking Product Health via LCM API

```bash
# Get health status for a specific environment
ENV_ID="<your-env-id>"
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/environments/$ENV_ID/health" | \
  jq '.'

# Get product details within an environment
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/environments/$ENV_ID/products" | \
  jq '.[] | {product: .productId, version: .version, health: .productHealth}'
```

Expected output: `health` field should be `GREEN` for all products in a healthy environment. `YELLOW` indicates a configuration warning; `RED` indicates a failure requiring investigation.

---

## Log File Locations

| Log | Path on LCM Appliance | Purpose |
|---|---|---|
| LCM application | `/var/log/vmware/vrlcm/lcm-app.log` | Main application events, workflow execution |
| LCM installer | `/var/log/vmware/vrlcm/lcm-install.log` | Product deployment and upgrade logs |
| Locker service | `/var/log/vmware/vrlcm/locker.log` | Certificate and password operations |
| Nginx | `/var/log/nginx/access.log`, `error.log` | API and UI HTTP requests |
| System | `/var/log/messages` | OS-level events, NFS mount issues |

```bash
# Tail the main application log for real-time workflow progress
tail -f /var/log/vmware/vrlcm/lcm-app.log

# Search for errors in the last 500 lines
tail -500 /var/log/vmware/vrlcm/lcm-app.log | grep -i "error\|exception\|failed"

# Check upgrade-specific logs (written during product upgrade workflows)
ls -lth /var/log/vmware/vrlcm/upgrade/
tail -200 /var/log/vmware/vrlcm/upgrade/<latest-upgrade-log>
```

---

## Environment Deployment Health

Check managed product service health via LCM UI and logs.

**Product status check (UI):**
Navigate to **Environments → select environment → Products** — the Status column should show green / Available for every product. Any product showing yellow (Warning) or red (Error) requires investigation before any change window.

**Task queue check:**
Navigate to **LCM → Lifecycle Operations → Requests → Active Requests** — if any task has been in RUNNING state for more than 30 minutes without progress, it is likely stuck. Collect the request ID and check the LCM application log:

```bash
# Tail LCM log and filter for a specific request ID
tail -500 /var/log/vmware/vrlcm/lcm-app.log | grep "<request-id>"

# Check for generic workflow errors in the last 200 lines
tail -200 /var/log/vmware/vrlcm/lcm-app.log | grep -i "ERROR\|WARN\|exception"
```

Common causes of stuck tasks: expired certificates mid-workflow, vCenter connectivity loss, NFS mount dropped, or a product VM that lost its management IP.

**LCM service log** — primary location: `/var/log/vmware/lcm/lcm.log` on the LCM appliance. Tail this file for real-time ERROR entries during any active operation.

---

## Certificate Expiry Check

Run weekly. Alert on any certificate expiring within 60 days; critical below 30 days.

**UI check:**
LCM → **Locker → Certificates** — review the Expiry Date column. Sort ascending to surface the nearest expiries first.

**CLI check — LCM appliance cert (SSH to LCM):**

```bash
echo | openssl s_client -connect localhost:443 \
  -servername $(hostname -f) 2>/dev/null \
  | openssl x509 -noout -dates
# notAfter= line shows expiry; calculate days remaining manually or with:
echo | openssl s_client -connect localhost:443 \
  -servername $(hostname -f) 2>/dev/null \
  | openssl x509 -noout -checkend 5184000 \
  && echo "OK: >60 days" || echo "WARN: <60 days"
```

**CLI check — each managed product (run from any host with network access):**

```bash
# Replace <product-fqdn> with the product's FQDN (e.g., vrops-prod-01.example.local)
echo | openssl s_client -connect <product-fqdn>:443 \
  -servername <product-fqdn> 2>/dev/null \
  | openssl x509 -noout -dates

# Batch check for multiple products
for fqdn in vrops-prod-01.example.local vra-prod-01.example.local vidm-prod-01.example.local; do
  expiry=$(echo | openssl s_client -connect ${fqdn}:443 -servername ${fqdn} 2>/dev/null \
    | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "${fqdn}: ${expiry}"
done
```

Renew any certificate expiring within 60 days using the procedure in the Procedures page (Request and Install Product Certificates via LCM).

---

## Backup Health Check

Run daily (automated) and manually before any major change.

**UI check:**
Navigate to **Settings → Backup and Restore** — confirm the **Last Successful Backup** timestamp. Alert if the last successful backup is more than 24 hours old.

**Target verification (SSH to backup target):**

```bash
# SFTP/NFS target — verify backup file exists and is recent
ls -lh /backup/lcm-backup-*
# Most recent file should be timestamped within the last 24 hours

# Check file size — a valid LCM backup is typically 50 MB–2 GB depending on Locker content
du -sh /backup/lcm-backup-$(date +%Y%m%d)*
```

If no backup file exists for today: check LCM → Settings → Backup and Restore → review error messages; common causes are SFTP credential expiry, NFS connectivity loss, or insufficient disk space on the target.

---

## Disk Usage Check

LCM accumulates product binaries, upgrade logs, and temp files. Monitor weekly; clean proactively.

**SSH to LCM appliance:**

```bash
df -h
# Key partitions to check:
# /                     — root; keep < 75% used
# /dev/mapper/data      — LCM data volume; keep < 80% used
# /data/lcm             — product binaries and working files; largest consumer

# Show top disk consumers under /data
du -sh /data/* | sort -rh | head -20
```

**Clean unused binaries (UI):**
Navigate to **Locker → Binary Mappings** — identify product versions that are no longer needed (older than two versions back from current). Select the binary mapping and click **Delete** — this removes the binary from `/data/` and frees disk space.

Failed upgrade cleanup: if an upgrade failed mid-process, temp files may remain in `/data/lcm/upgrade/`. Review and delete directories older than 7 days:

```bash
find /data/lcm/upgrade/ -maxdepth 1 -type d -mtime +7 -exec ls -lhd {} \;
# If confirmed safe to remove:
# find /data/lcm/upgrade/ -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
```

---

## Integration Health

Verify all external system connections LCM depends on.

**vCenter connectivity:**
Navigate to **LCM → Settings → vCenter Servers** (or **Lifecycle Operations → Data Centers**) — each registered vCenter should show as **Connected**. If a vCenter shows Disconnected:

```bash
# From LCM appliance — verify network reachability
curl -sk https://<vcenter-fqdn>/rest/com/vmware/cis/session \
  -X POST -u "svc-lcm@vsphere.local:<password>" | jq .
# Expect a session ID in the response; 401 = credential issue; timeout = network issue
```

**VIDM (Workspace ONE Access) connectivity:**
Navigate to **LCM → Settings → VIDM** — click **Test Connection**. A successful test returns a green indicator; failure means either the VIDM service is down or the LCM-to-VIDM network path is blocked (TCP 443).

```bash
# From LCM appliance — test VIDM reachability
curl -sk https://<vidm-fqdn>/SAAS/API/1.0/REST/system/health | jq .
# Expect {"allOk":true} or equivalent health indicator
```

**Depot connectivity (online depot):**
Navigate to **LCM → Settings → My VMware / Broadcom Support Portal** — verify the depot status shows as Connected. If offline: check proxy settings under **Settings → Proxy** and verify outbound HTTPS to `depot.vmware.com` is permitted by the firewall.

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
