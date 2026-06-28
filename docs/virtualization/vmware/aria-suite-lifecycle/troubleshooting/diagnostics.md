---
tags:
  - aria-lcm
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Suite Lifecycle — Diagnostics

<div class="kb-summary">
Aria Suite Lifecycle (vRSLCM) diagnostic commands: check service health, inspect vlcm.log for errors, verify certificate expiry for all managed products, check disk space on the LCM appliance, confirm NTP sync, query the LCM REST API for environment status, run the logscraper, and collect the support bundle for VMware cases.

*Applies to: Aria Suite Lifecycle 8.x*
</div>
![Aria Suite Lifecycle — Diagnostics](../../../../assets/virtualization-vmware-aria-suite-lifecycle-troubleshooting-d.svg)




```mermaid
graph TD
    A([LCM Issue]) --> B{What type of problem?}
    B -->|LCM UI unresponsive or slow| C[systemctl status vmware-vrlcm\njournalctl -u vmware-vrlcm -n 100]
    B -->|Deploy or upgrade operation failed| D[grep request-ID /var/log/vmware/vrlcm/vlcm.log\nRead installer.log for failed step]
    B -->|Certificate expiry warning| E[GET /lcm/api/v1/certificates\nCheck notAfter date per product]
    B -->|Disk space alert| F[df -h; du -sh /data/vmware/vrlcm/*\nClean old logs and bundles]
    B -->|NTP drift or SSO login failure| G[chronyc tracking\ntimedatectl status]
    B -->|Product environment shows error| H[GET /lcm/api/v1/environments\nCheck environment health JSON]
    C --> I{Service state?}
    I -->|Not running| J[systemctl start vmware-vrlcm\nCheck disk space first]
    I -->|Running but slow| K[Check disk /data for fullness\nCheck DB size du -sh /data/vmware/vrlcm/db]
    D --> L[grep ERROR vlcm.log | tail -50\nRead install step and failed component]
    E --> M{Days to expiry?}
    M -->|< 30 days| N[LCM UI → Lifecycle → Certificate Management\nTrigger rotation]
    M -->|Already expired| O[Rotate immediately\nStop all operations first]
    F --> P[find /var/log/vmware/vrlcm -name *.log.* -mtime +30 -delete\nRemove old snapshots and content library cache]
    G --> Q[chronyc makestep\nVerify offset < 5 seconds]
    H --> R[Check all required ports to product VMs\nnc -zv product-vm 443]
    J --> S[Collect logscraper bundle\nLCM UI → Support → Logscraper]
    K --> S
    L --> S
    N --> S
    O --> S
    P --> S
    Q --> S
    R --> S
    S --> T[Open VMware SR\nAttach logscraper ZIP]

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,I,M dark
    class C,D,E,F,G,H,J,K,L,N,O,P,Q,R action
    class S,T escalate
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_lcm_service_status: "Step 1 — Check LCM service status" {shape: rectangle}
step_2_inspect_vlcmlog_for_errors: "Step 2 — Inspect vlcm.log for errors" {shape: rectangle}
step_3_check_certificate_expiry: "Step 3 — Check certificate expiry" {shape: rectangle}
step_4_check_disk_space: "Step 4 — Check disk space" {shape: rectangle}
step_5_preoperation_health_check: "Step 5 — Pre-operation health check" {shape: rectangle}
step_6_check_environment_and_product: "Step 6 — Check environment and product status" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_lcm_service_status: investigate
symptom -> step_2_inspect_vlcmlog_for_errors: investigate
symptom -> step_3_check_certificate_expiry: investigate
symptom -> step_4_check_disk_space: investigate
symptom -> step_5_preoperation_health_check: investigate
symptom -> step_6_check_environment_and_product: investigate
step_1_check_lcm_service_status -> resolution
step_2_inspect_vlcmlog_for_errors -> resolution
step_3_check_certificate_expiry -> resolution
step_4_check_disk_space -> resolution
step_5_preoperation_health_check -> resolution
step_6_check_environment_and_product -> resolution
```

## Before you begin

- **Access:** SSH to the LCM appliance (`admin` user); LCM admin UI credentials; vCenter credentials (required for some product health checks)
- **Gather first:** the failing operation name and request ID (shown in LCM UI after any failed action), the product or environment affected, and the exact error message from the LCM event log
- **Scope:** confirm whether the issue is with the LCM service itself, a specific managed product environment, or a specific operation (deploy, upgrade, certificate rotation)
- **Pre-operation rule:** before any LCM operation, run Step 5 to confirm all services, disk, NTP, and no in-progress operations

---

## Step 1 — Check LCM service status

```bash
# SSH to LCM appliance
ssh admin@<lcm-fqdn>

# Core service status
systemctl status vmware-vrlcm        # LCM application
systemctl status vmware-vrlcm-db     # Embedded PostgreSQL
systemctl status nginx               # Reverse proxy / UI

# Expected: all three should be active (running)

# Quick one-liner to confirm all expected services
systemctl is-active vmware-vrlcm vmware-vrlcm-db nginx vmware-vrlcm-certmanager sshd

# Recent service events
journalctl -u vmware-vrlcm -n 100 --no-pager | tail -50
journalctl -u vmware-vrlcm-db -n 50 --no-pager

# If LCM is not running, check disk space before restarting
df -h /data
# Expected: < 80% used
systemctl start vmware-vrlcm
```

Key services and expected states:

| Service | Expected State | Notes |
|---|---|---|
| `vmware-vrlcm` | active (running) | Core LCM service |
| `vmware-vrlcm-db` | active (running) | Embedded PostgreSQL |
| `nginx` | active (running) | Reverse proxy / UI |
| `vmware-vrlcm-certmanager` | active (running) | Certificate management |
| `sshd` | active (running) | Required for remote access |

---

## Step 2 — Inspect vlcm.log for errors

```bash
# Most recent errors in the LCM application log
grep -i "ERROR\|Exception\|FATAL" /var/log/vmware/vrlcm/vlcm.log | tail -50

# Follow the log in real time during a failing operation
tail -f /var/log/vmware/vrlcm/vlcm.log | grep -i "error\|warn\|fail"

# Find the log for a specific request ID (shown in LCM UI after failed operations)
grep "<request-id>" /var/log/vmware/vrlcm/vlcm.log | head -50

# Installer log — most detailed for deploy and upgrade failures
# Path varies per operation; check for the most recent:
ls -lt /var/log/vmware/vrlcm/ | grep installer | head -5
tail -200 /var/log/vmware/vrlcm/installer*.log
```

---

## Step 3 — Check certificate expiry

```bash
# List all managed product certificates via LCM API
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/certificates" \
  | python3 -c "
import json,sys
for c in json.load(sys.stdin).get('certificates', []):
    print(c.get('productId',''), '|', c.get('subject',''), '|', c.get('validUntil',''))
"
# Look for: validUntil dates within 30 days

# Check the LCM appliance's own HTTPS certificate
echo | openssl s_client -connect <lcm-fqdn>:443 -servername <lcm-fqdn> 2>/dev/null \
  | openssl x509 -noout -subject -dates -issuer
# Expected: notAfter date should be > 30 days in the future
```

Certificate check thresholds:

| Days to Expiry | Status | Action |
|---|---|---|
| > 90 days | Healthy | No action required |
| 30–90 days | Warning | Plan rotation |
| 7–30 days | Critical | Rotate within a week |
| < 7 days | Emergency | Rotate immediately; stop operations |

---

## Step 4 — Check disk space

```bash
# Check all mount points
df -h
# Alert if > 70% used on /data or > 85% on /

# LCM-specific data directories
du -sh /data/vmware/vrlcm/*
du -sh /var/log/vmware/vrlcm/

# PostgreSQL database size
du -sh /data/vmware/vrlcm/db/

# Check inode exhaustion (can cause failures even if disk bytes are free)
df -i

# Clean old LCM logs older than 30 days
find /var/log/vmware/vrlcm/ -name "*.log.*" -mtime +30 -delete

# List and remove old support bundles
ls -lh /data/vmware/vrlcm/bundles/ 2>/dev/null
# Remove bundles older than 30 days
find /data/vmware/vrlcm/bundles/ -mtime +30 -delete 2>/dev/null
```

Disk space thresholds:

| Mount | Warning | Critical | Action if Critical |
|---|---|---|---|
| `/` | 75% | 85% | Remove old bundles and logs |
| `/data` | 70% | 80% | Clean content library cache |
| `/var/log` | 80% | 90% | Rotate and archive logs |

---

## Step 5 — Pre-operation health check

Run before any LCM operation (upgrade, patch, certificate rotation):

```bash
# 1. All services running
systemctl is-active vmware-vrlcm vmware-vrlcm-db nginx
# Expected: active active active

# 2. Disk space adequate (no mount > 70%)
df -h | awk 'NR>1 && $5+0 > 70 {print "WARNING:", $0}'

# 3. No active LCM operations in progress
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/operations?status=RUNNING" \
  | python3 -c "
import json,sys
data = json.load(sys.stdin)
ops = data.get('operations', [])
print(f'{len(ops)} operations running')
for op in ops:
    print(op.get('id',''), op.get('name',''), op.get('status',''))
"
# Expected: 0 operations running

# 4. NTP in sync
chronyc tracking | grep "System time"
# Expected: offset < 5 seconds (required for Aria SSO)

# 5. LCM API reachable and healthy
curl -sk -o /dev/null -w "HTTP %{http_code}\n" \
  -u admin:<password> "https://<lcm-fqdn>/lcm/api/v1/health"
# Expected: HTTP 200

# 6. NTP configuration
timedatectl status
chronyc sources -v
# Force re-sync if offset is large
sudo chronyc makestep
```

---

## Step 6 — Check environment and product status

```bash
# List all environments with health status
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/environments" \
  | python3 -c "
import json,sys
for e in json.load(sys.stdin).get('environments', []):
    print(e.get('environmentName',''), '|', e.get('status',''))
"
# Expected: status = COMPLETED or ACTIVE for all environments

# Get products in a specific environment
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/environments/<env-id>" \
  | python3 -m json.tool

# Check for stuck or failed operations
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/operations?status=FAILED" \
  | python3 -m json.tool
```

---

## Step 7 — Collect logscraper bundle for VMware SR

```bash
# Via LCM UI (recommended)
# Navigate to: LCM UI → Support → Logscraper
# Select: environment and products to include; time range
# Click: Generate Bundle
# Download: the .zip archive

# Via LCM CLI (if UI is unavailable)
ssh admin@<lcm-fqdn>
/opt/vmware/vlcm/tools/lcm-support.sh
# Output: /tmp/lcm-support-<timestamp>.tar.gz

# Via VAMI (appliance-level bundle)
# Browse to: https://<lcm-fqdn>:5480
# Navigate to: Support → Generate Support Bundle → Download

# What to include in VMware SR:
# - Logscraper ZIP (covers all managed products)
# - LCM appliance support bundle from VAMI
# - Failed operation ID from LCM UI
# - LCM version: LCM UI → Administration → About
# - Timeline of the failed operation and any recent changes
```

---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| LCM application | `/var/log/vmware/vrlcm/vlcm.log` | Exceptions, operation failures |
| Installer steps | `/var/log/vmware/vrlcm/installer*.log` | Step-by-step deploy/upgrade trace |
| Service events | `journalctl -u vmware-vrlcm` | Service start/stop/crash events |
| PostgreSQL | `journalctl -u vmware-vrlcm-db` | DB errors and restart events |
| Nginx | `journalctl -u nginx` | API gateway errors, 5xx responses |

---

## See also

- [Aria Suite Lifecycle — Common Issues](../common-issues/)
- [Aria Suite Lifecycle — Escalation](../escalation/)

## Verify resolution

- `systemctl is-active vmware-vrlcm vmware-vrlcm-db nginx` outputs `active active active`
- `GET /lcm/api/v1/health` returns HTTP 200 with healthy status JSON
- `GET /lcm/api/v1/operations?status=RUNNING` returns 0 in-progress operations
- The failing LCM operation (upgrade, certificate rotation, deploy) completes successfully after the fix
- `chronyc tracking` shows offset < 5 seconds from the NTP source
