# NetApp Keystone Lifecycle

## Subscription Terms and Renewal

Keystone subscriptions typically run for 1, 2, or 3 years. Longer terms offer more favorable per-TB pricing and committed service-level guarantees. Begin renewal discussions at least 6 months before the subscription expiry date — the process includes capacity planning, commercial negotiation, order processing, and in some cases hardware refresh scheduling.

| Subscription Phase | Timeline Before Expiry | Action |
|---|---|---|
| Pre-renewal planning | 6 months | Engage Keystone Success Manager (KSM); review consumption trends and capacity forecast |
| Commercial review | 4–5 months | Negotiate per-TB rates, service levels, and term length; confirm hardware refresh plan |
| Order processing | 2–3 months | Signed order; NetApp procurement and logistics for any new hardware |
| Transition / cutover | 0–1 month | New subscription active; confirm Collector is reporting to new subscription ID in BlueXP |

Mid-term amendments are available for committed capacity increases — committed capacity can be increased at any point during the term but cannot be decreased until the next renewal. If requirements have significantly reduced mid-term, discuss partial release options with the KSM.

---

## True-Up Process

The Keystone Collector reports consumption telemetry continuously. NetApp aggregates this into a monthly consumption report. The invoice for each period reflects:

- **Committed capacity charge**: flat monthly rate for the contracted committed capacity per tier
- **Burst charge**: per-TB rate (higher than committed rate) applied to any usage above committed capacity during the billing period

```
Monthly Invoice = (Committed capacity × committed rate) + (Burst TiB × burst rate)
```

### True-Up Review Process

1. Before the end of each calendar month, log into BlueXP → Digital Wallet → Keystone Subscriptions
2. Download the month-to-date consumption report for each subscription
3. Compare consumed capacity per tier against committed capacity — identify any burst usage
4. For unexpected burst, trace back to the source: new volume provisioning, snapshot growth, or workload growth
5. If burst consumption appears incorrect (not matching ONTAP volume usage), raise a discrepancy with the KSM before the invoice is finalised
6. After invoice receipt, reconcile the invoice against the downloaded consumption report and archive both for audit records

```bash
# ONTAP: compare logical used capacity vs. what Keystone is billing
# Run on the ONTAP cluster backing the subscription

# Total logical used per SVM (what Keystone measures)
volume show -vserver * -fields vserver,volume,logical-used,size | sort -k4 -rn

# Check snapshot contribution to capacity
snapshot show -vserver * -volume * -fields vserver,volume,size | sort -k4 -rn | head -20

# Aggregate-level physical used (for cross-check)
storage aggregate show -fields aggregate,size,used,available
```

### Billing Discrepancy Procedure

1. Download the consumption report from BlueXP for the affected period
2. Export ONTAP volume logical-used data for the same period: `volume show -fields logical-used`
3. Identify any volumes in the Keystone report that do not match ONTAP data
4. Open a Keystone support case via BlueXP or the KSM with the report and ONTAP data attached
5. Discrepancies must be raised **before the invoice is finalised** — retrospective adjustments after invoice closure are not available

---

## Hardware Refresh

NetApp owns all hardware deployed under a Keystone subscription. NetApp is responsible for hardware refresh decisions based on its own lifecycle management — the customer does not purchase replacement hardware or manage the depreciation cycle.

### What NetApp Manages During Hardware Refresh

- Planning and scheduling of the hardware refresh (typically coordinated 3–6 months in advance)
- Data migration from old hardware to new hardware — NetApp Professional Services or Keystone SRE executes this
- Physical installation, racking, and cabling of the new hardware
- ONTAP configuration migration or fresh build on new hardware, matching the existing configuration
- Decommission and removal of old hardware after successful migration confirmation

### Customer Responsibilities During Hardware Refresh

- Confirm the maintenance window and sign off on the refresh schedule
- Coordinate application-owner notification for any workload impact during migration
- Validate data integrity and application connectivity after migration completes
- Update CMDB and capacity register with new hardware serial numbers if tracked internally

### Pre-Refresh Checklist

- [ ] All SnapMirror relationships are healthy before migration begins
- [ ] Application owners notified of the maintenance window and potential brief I/O pauses during migration
- [ ] Current capacity baseline documented from BlueXP before migration (for post-migration comparison)
- [ ] Keystone Collector is updated to a version compatible with the new ONTAP version being deployed on the new hardware
- [ ] Post-migration validation plan agreed with NetApp SRE — including connectivity tests, application smoke tests, and capacity comparison

---

## Collector Lifecycle

The Keystone Collector is a separate software component from ONTAP with its own release cadence. It runs as a Linux service on a VM managed by the customer.

### Collector Version Management

```bash
# Check current Collector version
sudo keystone-collector --version
# Or:
rpm -q keystone-collector    # RPM-based systems (RHEL, CentOS)
dpkg -l keystone-collector   # DEB-based systems (Ubuntu, Debian)

# Check for updates — follow NetApp release notifications for the Collector
# Updates are distributed via the NetApp support site or as a package repository

# Upgrade the Collector (RPM example)
sudo rpm -Uvh keystone-collector-<new-version>.rpm

# Or via package manager if NetApp repo is configured
sudo yum update keystone-collector    # RHEL/CentOS
sudo apt-get install --only-upgrade keystone-collector  # Ubuntu/Debian

# After upgrade, confirm the service starts cleanly
sudo systemctl restart keystone-collector
sudo systemctl status keystone-collector

# Verify the first collection cycle completes successfully post-upgrade
sudo journalctl -u keystone-collector -f
# Watch for "collection complete" or "telemetry sent" message
```

### Collector VM OS Maintenance

The Collector VM is customer-managed infrastructure. Apply the same OS hardening and patching standards as other management VMs.

```bash
# Apply OS security patches (RHEL/CentOS)
sudo yum update -y --security

# Apply OS security patches (Ubuntu/Debian)
sudo apt-get update && sudo apt-get upgrade -y

# After OS patching, confirm the Collector service is still running
sudo systemctl status keystone-collector

# Verify network connectivity to NetApp endpoint is intact post-patch
curl -sk -o /dev/null -w "%{http_code}" https://keystone.netapp.com
```

---

## Subscription Exit and Migration

At subscription expiry — whether transitioning to a new Keystone term, moving to a different vendor, or migrating to cloud — the customer is responsible for all data migration off the NetApp-managed infrastructure.

### Exit Timeline Planning

| Activity | Lead Time | Notes |
|---|---|---|
| Engagement with KSM on exit plan | 6 months before exit date | Defines migration scope, schedule, and support from NetApp |
| Identify target infrastructure | 5–6 months | New Keystone subscription, alternative vendor, or cloud |
| Data migration execution | 2–4 months | Depends on data volume; use ONTAP SnapMirror or rsync for NAS |
| Application reconfiguration | 1–2 months | Update mount paths, DNS, CIFS share paths, iSCSI/FC targets |
| Final data validation | Last 2–4 weeks | Confirm all data migrated; no active clients on Keystone hardware |
| Hardware decommission date | End of subscription | NetApp removes hardware; no data remains on Keystone infrastructure |

### Data Migration Approaches

```bash
# Option 1: SnapMirror to new ONTAP cluster (preferred for ONTAP-to-ONTAP migration)
# Establish cluster peer between Keystone ONTAP and target ONTAP
cluster peer create -generate-passphrase \
    -peer-addrs <target-intercluster-lif>

# Create XDP relationship to mirror data to the target
snapmirror create \
    -source-path svm_prod:vol_data \
    -destination-path svm_target:vol_data \
    -type XDP \
    -policy MirrorAllSnapshots

snapmirror initialize -destination-path svm_target:vol_data

# Once initial sync completes, schedule cutover
# Quiesce source, final update, break mirror, mount at target
snapmirror quiesce -destination-path svm_target:vol_data
snapmirror update -destination-path svm_target:vol_data
snapmirror break -destination-path svm_target:vol_data

# Option 2: rsync for NAS data migration to non-ONTAP target
# Run from a Linux host with access to both NFS mounts
rsync -avz --progress --checksum \
    /mnt/keystone-source/ \
    /mnt/target-destination/
```

### Pre-Decommission Validation

Before confirming hardware removal with NetApp:

- [ ] All volumes confirmed migrated: `volume show -vserver * -state online` on Keystone cluster returns no customer volumes
- [ ] No active NFS mounts to Keystone storage from any client hosts
- [ ] No active iSCSI or FC sessions to Keystone LUNs
- [ ] DNS entries updated to point to new storage infrastructure
- [ ] CIFS/NFS share access tested from all application hosts against new storage
- [ ] CMDB updated: Keystone hardware removed from asset records
- [ ] Keystone Collector decommissioned after final billing period: `sudo systemctl stop keystone-collector && sudo systemctl disable keystone-collector`
