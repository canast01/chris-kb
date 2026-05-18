# Aria Suite Lifecycle — Install & Upgrade

```
  LCM Upgrade Sequence (strict order)
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: LCM itself                                             │
│   Lifecycle Operations → System Upgrade → select bundle         │
│   LCM restarts (~5-10 min); unavailable during upgrade          │
│                    │                                            │
│                    ▼                                            │
│  Step 2: Workspace ONE Access (VIDM)                            │
│   Must precede ALL other product upgrades                       │
│                    │                                            │
│                    ▼                                            │
│  Step 3+: Aria products (one at a time)                         │
│   Aria Operations → Aria Automation → Aria Log Insight          │
│   Aria Ops for Networks (after VIDM, any order)                 │
│                                                                 │
│  Each product upgrade:                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Snapshot VMs → Download bundle → Run pre-check          │    │
│  │ → Start Upgrade → Monitor Requests → Post-validate      │    │
│  │ → Delete snapshots (after confirm success)              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Upgrade Sequence

**Critical: LCM must always be upgraded first, then VIDM, then all other products.**

| Step | Product | Notes |
|---|---|---|
| 1 | Aria Suite Lifecycle (LCM) | Never skip — upgrading products with an older LCM is unsupported |
| 2 | Workspace ONE Access (VIDM) | Must precede all other product upgrades |
| 3 | Aria Operations | After VIDM |
| 4 | Aria Automation | After Aria Operations |
| 5 | Aria Log Insight | After VIDM |
| 6 | Aria Operations for Networks | After VIDM |

Check compatibility: [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com)

## Upgrade Procedure via LCM

1. **Pre-upgrade snapshot** — take a VM snapshot of LCM and all managed appliances before starting
   ```bash
   # Via vCenter: right-click each appliance VM → Snapshot → Take Snapshot
   # Name: pre-upgrade-$(date +%Y%m%d)
   ```

2. **Download product bundle** — LCM → Lifecycle Operations → Settings → Binary Mapping → Check for Updates
   - Or upload offline .pak files if no internet access

3. **Trigger upgrade** — LCM → Lifecycle Operations → Environments → select environment → Upgrade
   - LCM presents a pre-check list; all items must pass before proceeding

4. **Monitor progress** — LCM shows upgrade task progress; SSH to LCM and tail logs if needed:
   ```bash
   tail -f /var/log/lcm/lcm-app.log
   ```

5. **Post-upgrade validation** — verify product health in LCM dashboard before deleting snapshots

## EOL Tracking

| Product | Lifecycle Reference |
|---|---|
| All Aria products | [lifecycle.vmware.com](https://lifecycle.vmware.com) — check quarterly |

Key dates to track:
- **End of General Support**: last date for patches and updates
- **End of Technical Guidance**: last date for support calls

Alert at 90 days before End of General Support.

## LCM Upgrade (Upgrading LCM Itself)

LCM can upgrade itself via the binary mapping workflow:

1. LCM → Lifecycle Operations → Settings → System Upgrade
2. Select the new LCM bundle
3. Click Upgrade — LCM restarts after upgrade; takes 5–10 minutes

LCM is unavailable during its own upgrade — plan during a maintenance window.

## Backup and Recovery

### LCM Configuration Backup

```bash
# From LCM UI: Settings → System Details → Backup and Restore
# Or via API:
curl -k -u admin:password -X POST https://lcm.corp.local/lcm/lcops/api/v2/system/backup
```

Store backup archives off the LCM appliance (NFS, S3, or external storage).

### LCM Recovery

If LCM appliance is lost:
1. Deploy fresh LCM OVA from Easy Installer
2. Restore configuration from backup (Settings → System Details → Restore)
3. Reconnect managed products — LCM re-discovers product state
4. Verify Locker certificates are intact after restore

## Product Decommission via LCM

To remove a managed product (e.g., decommission Aria Log Insight):
1. LCM → Lifecycle Operations → Environments → select product → Delete
2. LCM powers off and unregisters product VMs
3. Delete VMs from vCenter after LCM confirms completion
4. Remove DNS records and CMDB entries

---

## Full Suite Upgrade Procedure

Covers upgrades for Aria Suite Lifecycle, Aria Operations, Aria Operations for Logs, and Aria Automation.

### Upgrade Order

1. Aria Suite Lifecycle
2. Aria Operations
3. Aria Operations for Logs
4. Aria Automation
5. Integrations and dashboards validation

Upgrade Aria Suite Lifecycle first if it manages the other products.

---

### Phase 1: Pre-Upgrade Checks

#### Access Validation

Confirm access to: Aria Suite Lifecycle, Aria Operations, Aria Logs, Aria Automation, vCenter, NSX if integrated, identity provider.

#### Health Validation

- Product UI loads
- Cluster and nodes healthy
- No failed services, disk space warnings, or certificate warnings
- Data collection active
- Authentication working
- Dashboards loading

#### Backup and Content Export

Before upgrade:

- Take supported product backup
- Export important dashboards
- Export custom alerts
- Export Aria Automation blueprints and templates
- Export extensibility workflows if needed
- Confirm rollback plan

#### Certificate Review

- Product, vCenter, NSX, load balancer, and identity provider certificates valid

---

### Phase 2: Aria Suite Lifecycle Upgrade

**Pre-check:** Suite Lifecycle appliance health, repository access, product inventory sync, password and certificate locker health, disk space.

**Steps:**
1. Log into Aria Suite Lifecycle
2. Confirm repository access and select target version
3. Run pre-check and resolve issues
4. Start upgrade
5. Monitor request status
6. Confirm services restart and validate login

**Post-check:** Product inventory visible, password and certificate lockers working, environment sync working.

---

### Phase 3: Aria Operations Upgrade

**Pre-check:** Cluster healthy, all nodes online, data collection active, vCenter adapters collecting, cloud proxies connected, dashboards loading.

**Steps:**
1. Upload upgrade package or use Suite Lifecycle
2. Run pre-check and resolve issues
3. Start upgrade and monitor node upgrade order
4. Wait for cluster to come online
5. Confirm UI access

**Post-check:** Cluster and all nodes online, data collection resumed, dashboards and alerts working, management packs healthy.

---

### Phase 4: Aria Operations for Logs Upgrade

**Pre-check:** Cluster healthy, log ingestion active, disk usage healthy, agents reporting, content packs compatible.

**Steps:**
1. Upload upgrade package or use Suite Lifecycle
2. Run pre-check
3. Start upgrade and monitor each node
4. Confirm cluster returns online

**Post-check:** Logs being received, searches return recent logs, dashboards and alerts working, agents connected.

---

### Phase 5: Aria Automation Upgrade

#### Pre-check

- Appliance cluster healthy, services running
- vCenter and NSX integrations working
- Cloud zones, projects, catalog items, and deployments visible
- Identity provider working

#### Content to Export Before Upgrade

- Cloud accounts, cloud zones, projects
- Flavor and image mappings
- Network and storage profiles
- Catalog items and blueprints
- Approval policies and extensibility workflows

#### Steps

1. Start upgrade from Suite Lifecycle if managed
2. Run pre-check and resolve issues
3. Start upgrade and monitor progress
4. Validate UI login and integrations

#### Post-check

- Catalog items load
- Existing deployments visible
- New test deployment works
- Day-2 actions work
- Approval workflow works
- vCenter and NSX integrations working
- Identity login working

---

### Phase 6: Final Validation

- All Aria products reachable and show target version
- Dashboards load and data collection active
- Alerts working, reports running, logs ingesting
- Automation catalog working
- Certificates trusted, integrations healthy

### Documentation

Update product versions, upgrade notes, pre/post-check results, issues found, integrations validated, rollback notes, and lessons learned.
