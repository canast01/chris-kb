---
tags:
  - dell
  - operations
---
# Dell CloudIQ Backup and Restore

```bash
# Verify your secrets vault has the following stored per API client:
# - Client ID (shown on the API Access page)
# - Client Secret (copy at creation time only)
# - Date created
# - Date of next scheduled rotation
# - Associated integrations (e.g., "Splunk poller", "Ansible pre-check")

# Verify that a stored secret is still valid
CLIENT_ID="<stored-client-id>"
CLIENT_SECRET="<stored-client-secret>"

curl -s -X POST "https://cloudiq.apis.dell.com/auth/oauth/v2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if 'access_token' in d else 'FAIL')"
```
```text
┌─────────────────────────────────── Dell CloudIQ Backup and Restore ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          CloudIQ SaaS platform backed up by Dell; SCG configuration exported manually         │   │
│   │            SCG VM snapshot or OVA export preserves system credentials and settings            │   │
│   │              CloudIQ telemetry data retained in Dell cloud for 90 days by default             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SCG VM snapshot → export settings → restore to new SCG VM → re-register in CloudIQ                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SCG Backup                  │  │                 CloudIQ SaaS                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          VM snapshot (ESXi/Hyper-V)          │  │           Dell manages SaaS backup          │   │
│   │          Settings export via SCG UI          │  │           Historical data: 90 days          │   │
│   │           System credential backup           │  │            Config replicated geo            │   │
│   │              Certificate backup              │  │          No customer action needed          │   │
│   │             OVA re-deploy for DR             │  │       Org data persists after SCG loss      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    SCG restore: deploy new OVA → import settings → re-register with CloudIQ org → verify              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Restore procedure: 1) Deploy fresh SCG OVA on VMware/Hyper-V                 │   │
│   │                       2) Import exported settings file via SCG admin UI                       │   │
│   │                       3) Re-register SCG with CloudIQ organisation token                      │   │
│   │                   4) Verify storage systems reconnect and telemetry resumes                   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SCG settings export = JSON export of all system credentials, proxy config, and certs               │
│    Org token          = CloudIQ organisation registration token; links SCG to correct tenant          │
│    90-day retention   = CloudIQ keeps 90 days of telemetry; older data rolled off automatically       │
│    SaaS backup        = Dell guarantees CloudIQ platform HA and geo-redundant backup                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Export audit log via CloudIQ portal
# Admin > Audit Log > Export as CSV
# Set date range: last 30 days (run monthly)

# Store exports with naming convention:
# cloudiq_audit_YYYYMM.csv
# Retain for minimum 90 days; 12 months if under PCI-DSS, HIPAA, or ISO 27001
```
```bash
# VM-level backup (example: ESXi snapshot before SCG update)
# Run from vCenter or via ESXCLI on the ESXi host

# Quiesce the SCG VM before snapshotting
# vCenter → SCG VM → Actions → Snapshots → Take Snapshot
# Name: "pre-update-YYYYMMDD"
# Enable: Snapshot the virtual machine's memory (optional)
# Enable: Quiesce guest file system (requires VMware Tools)

# For Veeam integration:
# Veeam → Jobs → Backup Job → Add SCG VM
# Recommended: daily backup; retain 7 days of restore points
```
```bash
# Create a new notification rule via REST API (example: email rule for CRITICAL alerts)
curl -s -X POST "${BASE}/notification-rules" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "storage-ops-critical-email",
    "severity": ["CRITICAL"],
    "notification_type": "EMAIL",
    "recipients": ["storage-ops@corp.example.com"],
    "enabled": true
  }' | python3 -m json.tool

# Create webhook notification rule for ServiceNow
curl -s -X POST "${BASE}/notification-rules" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "servicenow-incident-critical",
    "severity": ["CRITICAL"],
    "notification_type": "WEBHOOK",
    "webhook_url": "https://your-instance.service-now.com/api/now/table/incident",
    "enabled": true
  }' | python3 -m json.tool

# Send a test notification to validate
curl -s -X POST "${BASE}/notification-rules/<rule-id>/test" \
  -H "Authorization: Bearer ${TOKEN}"
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

