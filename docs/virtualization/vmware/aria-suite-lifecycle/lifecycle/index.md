# Aria Suite Lifecycle — Product Lifecycle
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
