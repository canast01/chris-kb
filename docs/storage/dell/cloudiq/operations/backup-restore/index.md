# CloudIQ — Backup & Restore


<div class="kb-summary">
> Part of the [CloudIQ](../../index.md) reference.
</div>

---

CloudIQ is a SaaS platform — there is no customer-managed backup of the CloudIQ analytics service itself. Dell manages data retention, service continuity, and platform backups on the back end. The historical telemetry and health score data retained by CloudIQ is covered by Dell's SaaS data retention policy (typically 13 months rolling).

The items you are responsible for backing up are the artefacts and configuration that enable CloudIQ to function in your environment, and the data that CloudIQ generates that you need to retain independently.

---

## What to Back Up on the Customer Side

### API Credentials

API client credentials (client ID and client secret) are the most critical item to protect. The client secret is shown only once at creation time — it cannot be retrieved from the CloudIQ portal after that.

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
```text

### Audit Log Exports

CloudIQ's audit log records user logins, configuration changes, and API activity. The retention window in the CloudIQ portal is limited. Export the audit log regularly and retain the exports per your organisation's security policy (typically 90 days minimum, 12 months for PCI or HIPAA environments).

```bash
# Export audit log via CloudIQ portal
# Admin > Audit Log > Export as CSV
# Set date range: last 30 days (run monthly)

# Store exports with naming convention:
# cloudiq_audit_YYYYMM.csv
# Retain for minimum 90 days; 12 months if under PCI-DSS, HIPAA, or ISO 27001
```

### Custom Dashboard and Report Configurations

If you have created custom dashboards or scheduled reports in CloudIQ, document their configuration. These are not exportable and would need to be recreated manually if the account is reset.

---

## SCG Appliance Backup

The SCG virtual appliance stores its registration database, proxy settings, and device credentials locally. Back up the SCG VM using your standard hypervisor snapshot or backup tooling.

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

After SCG restore from backup, verify all registered devices are still reporting by checking the CloudIQ portal — the systems should reappear within 30 minutes of the SCG coming back online.

---

## Recovery Procedures

### Recover API Credentials (Secret Lost)

If a client secret has been lost and was not stored in a vault:

1. Log into the CloudIQ portal as an admin
2. Navigate to **Settings → API Access**
3. Locate the affected client credential
4. Click **Regenerate Secret** (this invalidates the old secret immediately)
5. Copy the new secret — it is shown only once
6. Update all automation scripts and vaults with the new secret
7. Test authentication using the [authentication validation command](#api-credentials) above

> **Important**: Regenerating the secret immediately breaks any automation still using the old secret. Coordinate with all teams using the credential before rotating.

### Rebuild SCG from Scratch (No Backup)

If the SCG appliance is lost with no usable VM backup:

1. Download the latest SCG OVA from the Dell support portal
2. Deploy the OVA on the ESXi or vSphere host
3. Complete the SCG initial configuration wizard (set management IP, NTP, proxy if required)
4. Re-register each storage system with the new SCG:
   - For PowerStore: **PowerStore Manager → Settings → Support → SupportAssist → Register with SCG**
   - For PowerMax: **Unisphere → Settings → Connectivity → SCG → Register**
   - For Unity: **Unisphere for Unity → System → Connectivity → SCG**
5. Allow 30–60 minutes for all systems to reappear in CloudIQ
6. Verify all systems show `CONNECTED` in the CloudIQ dashboard

### Recreate Notification Rules

After an account reset, recreate notification rules from your documentation:

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

---

## Backup Verification Checklist (Quarterly)

- [ ] Confirm client ID and client secret for all API credentials are stored in the secrets vault
- [ ] Validate stored secrets authenticate successfully against the CloudIQ API
- [ ] Audit log export for the last 30 days completed and stored
- [ ] Notification rule configuration documented and up to date
- [ ] SCG device registration list exported (systems CSV)
- [ ] SCG VM backup completed and tested (restore to non-production if possible)
- [ ] All API credentials with upcoming rotation dates flagged for rotation before expiry
