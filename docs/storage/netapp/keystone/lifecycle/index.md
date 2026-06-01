# NetApp Keystone Lifecycle


<div class="kb-summary">
NetApp Keystone Lifecycle reference covering Subscription Terms and Renewal, True-Up Process, Hardware Refresh, Collector Lifecycle, Subscription Exit and Migration.
</div>

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

```text
Monthly Invoice = (Committed capacity × committed rate) + (Burst TiB × burst rate)
```
┌───────────────────────────────────── NetApp Keystone — Lifecycle ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Keystone lifecycle: contract -> install -> operate -> capacity change -> renew        │   │
│   │          Contract: 1-5 year term; committed TB per service level; burst allowance set         │   │
│   │         Install: NetApp ships AFF/FAS; rack + cable + ONTAP config by NetApp engineer         │   │
│   │         Capacity change: add TB via KSM; contract amendment; hardware added if needed         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Contract sign -> install -> operate -> capacity change -> renew or exit                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Pre-Deploy         │  │           In-Life           │  │         End of Term         │   │
│   │        Contract sign        │  │          Operations         │  │        Renewal option       │   │
│   │          HW sizing          │  │       Capacity review       │  │         Upgrade term        │   │
│   │         Site survey         │  │       Burst monitoring      │  │       Exit: data move       │   │
│   │         Rack install        │  │         Capacity add        │  │          HW return          │   │
│   │         ONTAP config        │  │        ONTAP upgrade        │  │        Contract close       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Quarterly review with KSM: usage vs committed; plan capacity change before burst                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Phase       │      Action      │       Owner       │       SLA        │      Notes       │   │
│   │      Deploy      │   Rack/install   │       NetApp      │    30-60 days    │  Site ready req  │   │
│   │     Cap add      │  Contract amend  │        KSM        │     30 days      │   HW lead time   │   │
│   │    ONTAP upg     │  Patch/upgrade   │    NetApp/cust    │    Scheduled     │  Non-disruptive  │   │
│   │       Exit       │  Data migration  │      Customer     │     EOL date     │   HW returned    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NetApp ships AFF/FAS + disk shelves; customer provides rack/power/cooling                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    KSM                = Keystone Success Manager; lifecycle advisor; quarterly reviews                │
│    Contract term      = 1, 3, or 5 years; defines committed TB and burst allowance                    │
│    Capacity amendment = Formal change to contract committed TB; requires KSM sign-off                 │
│    Site survey        = Pre-install assessment: rack space, power, cooling, network                   │
│    Non-disruptive upg = ONTAP upgrade without host I/O interruption via rolling                       │
│    Exit plan          = 90-day notice; customer migrates data; NetApp reclaims HW                     │
│    Burst monitoring   = Active IQ alerts at 80%, 90% of burst ceiling                                 │
│    ONTAP upgrade      = Cluster rolling upgrade; one node at a time; HA takes over                    │
│    HW return          = Hardware is NetApp property; decommission on contract end                     │
│    SFO                = Storage Failover; HA takeover during ONTAP upgrade cycles                     │
│    Quarterly review   = KSM meets customer; reviews usage, forecasts, adjusts plan                    │
│    HW lead time       = 30-60 days for new AFF/FAS nodes post-amendment                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```sql

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
