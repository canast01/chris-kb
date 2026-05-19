# Aria Suite Lifecycle — Health Checks

```
  LCM Health Check Chain
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

## Daily Health Checks

```bash
# LCM appliance disk usage — keep /data (NFS) and / below 80%
df -h

# LCM service status
systemctl status lcm
systemctl status nginx

# Check recent log errors
grep -E "ERROR|WARN" /var/log/vmware/vrlcm/lcm-app.log | tail -50

# Verify NFS mount is healthy
mount | grep /data
ls /data/ | head -20

# Check NTP sync — LCM certificate operations fail if time drift > 5 seconds
chronyc tracking | grep -E "System time|Stratum|RMS offset"
```

In the LCM UI:
- **Lifecycle Operations → Environments**: all environment cards should show green health indicators
- **Locker → Certificates**: check for certificates expiring within 30 days
- **Settings → My VMware**: verify bundle sync schedule last ran successfully

---

## Cluster Node Health via API

```bash
# Authenticate and get a session token
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.example.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

# List all environments and their health
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/environments" | \
  jq '.[] | {name: .environmentName, health: .environmentHealth}'

# Get all running requests (watch for stuck workflows)
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/requests?state=RUNNING" | \
  jq '.[] | {id: .requestId, type: .requestType, startTime: .startTime}'
```

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
