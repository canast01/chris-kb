# Aria Suite Lifecycle — Health Checks


<div class="kb-summary">
Health Checks reference covering Cluster Node Health via API, Locker Health Checks, Pre-Upgrade Health Gate, Checking Product Health via LCM API, Log File Locations.
</div>

  LCM Health Check Chain
```
┌─────────────────────────────────────────────────────────────────┐
│  LCM Appliance           Locker              Environments        │
│  ┌──────────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │ systemctl status │    │ Certs: days  │    │ All cards    │   │
│  │  lcm / nginx     │    │  to expiry   │    │  GREEN?      │   │
│  │ df -h (disk <80%)│    │  < 30 days   │    │ No RUNNING   │   │
│  │ chronyc tracking │    │  → renew now │    │  requests?   │   │
│  │  (NTP < 5s drift)│    └──────────────┘    └──────────────┘   │
│  └──────────────────┘                                           │
│                                                                 │
│  Pre-Upgrade Gate (all must pass)                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ ✓ All env cards GREEN   ✓ No in-progress requests       │    │
│  │ ✓ /data < 75%           ✓ NFS mount active + writable   │    │
│  │ ✓ NTP delta < 5s        ✓ No certs expiring < 7 days    │    │
│  │ ✓ VM snapshots taken    ✓ LCM pre-check passes          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```
```
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
```bash

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
