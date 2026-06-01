# NetApp Keystone — Common Issues


<div class="kb-summary">
Common Issues reference covering Keystone Collector Not Reporting, Subscription Consumption Shows Unexpected Spike, SnapMirror Lag Alert, Collector VM Cannot Reach ONTAP Array, Keystone Portal Shows Wrong Committed Capacity and 1 more sections.
</div>
```
┌─────────────────────────────────── NetApp Keystone — Common Issues ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Keystone common issues: quick-reference for frequently encountered problems          │   │
│   │         Issues: path failures, connectivity errors, capacity alerts, and auth failures        │   │
│   │         For each issue: symptoms, root cause, diagnostic steps, and resolution actions        │   │
│   │           Escalate to vendor support if the issue persists after standard procedures          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify symptom → check logs → diagnose root cause → resolve → verify                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Hardware          │  │       AFF/FAS on-prem       │  │         NetApp-owned        │   │
│   │        Service level        │  │       Extreme/Perf/Std      │  │         Latency SLA         │   │
│   │          Collector          │  │         Telemetry VM        │  │        ONTAP polling        │   │
│   │          Dashboard          │  │            BlueXP           │  │       Usage visibility      │   │
│   │           Billing           │  │       Committed+burst       │  │       Monthly invoice       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │Keystone Collecto │  Usage metering  │     ONTAP REST    │ Service account  │    On-prem VM    │   │
│   │      BlueXP      │   SaaS portal    │       HTTPS       │    OAuth2/SSO    │   NetApp SaaS    │   │
│   │   AFF Extreme    │  NVMe perf tier  │    FC/iSCSI/NFS   │  Kerberos/CHAP   │  Sub-ms latency  │   │
│   │   AutoSupport    │ Telemetry relay  │       HTTPS       │   Certificate    │    Call-home     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NetApp AFF/FAS arrays on-prem · Keystone Collector VM · BlueXP cloud portal              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Keystone           = NetApp STaaS; fixed-term subscription for ONTAP or StorageGRID capacity       │
│    Service level      = tiered SLA: Extreme (NVMe), Performance (SSD), Standard (HDD)                 │
│    Committed capacity = minimum contracted TiB; billed monthly even if below threshold                │
│    Burst capacity     = usage above committed; available without pre-ordering; billed monthly         │
│    Keystone Collector = on-prem VM that gathers usage metrics and sends to NetApp Keystone            │
│    BlueXP             = NetApp SaaS control plane; Keystone dashboard, DRaaS, and cloud integrations  │
│    AFF                = All Flash FAS; ONTAP-based NVMe/SSD array used for Extreme and Performance ...│
│    FAS                = Fabric Attached Storage; ONTAP hybrid HDD/SSD for Standard service level      │
│    StorageGRID        = NetApp S3 object storage; Object service level in Keystone subscriptions      │
│    AutoSupport        = ONTAP telemetry relay; sends call-home data and log bundles to NetApp         │
│    Service request    = NetApp SR; support ticket opened via mysupport.netapp.com portal              │
│    SKU                = Keystone service SKU identifies the service level and raw or usable capacity  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Keystone Collector Not Reporting

**Symptom:** Keystone portal shows arrays as "not reporting" or last collection timestamp is stale.

**Checks:**

```bash
# On Collector VM
keystone-collector status
keystone-collector show-last-collection

# Check network connectivity to Keystone cloud endpoints
curl -I https://keystone.netapp.com
curl -I https://api.keystone.netapp.com

# Check Collector logs
journalctl -u keystone-collector --since "1 hour ago"
```

**Resolution:**

1. Confirm outbound HTTPS (443) is allowed from Collector VM to NetApp cloud endpoints
2. Re-validate configuration: `keystone-config validate`
3. Force a collection: `keystone-collector collect --force`
4. If still failing, restart the service: `systemctl restart keystone-collector`

---

## Subscription Consumption Shows Unexpected Spike

**Symptom:** Keystone portal reports a sudden jump in consumed TiB not explained by provisioning.

**Checks:**

```bash
# On ONTAP — check which volumes grew
volume show -vserver <keystone-svm> -fields size,used,percent-used | sort -k3 -r

# Check for large snapshot accumulation
volume snapshot show -vserver <keystone-svm> -fields size

# Check for new qtrees or volumes provisioned without Keystone awareness
volume show -vserver <keystone-svm>
qtree show -vserver <keystone-svm>
```

**Common causes:** Snapshot accumulation from a missed cleanup job; a bulk data ingest; a new volume provisioned directly on the SVM outside of Keystone portal workflow.

---

## SnapMirror Lag Alert

**Symptom:** Keystone portal or ONTAP reports replication lag on a Keystone-backed SnapMirror relationship.

```bash
# Check SnapMirror relationship status
snapmirror show -vserver <svm> -fields state,lag-time,health

# Re-sync if relationship is broken
snapmirror resync -source-path <src> -destination-path <dst>

# Update immediately
snapmirror update -destination-path <dst>
```

---

## Collector VM Cannot Reach ONTAP Array

**Symptom:** `keystone-collector list-arrays` shows an array as unreachable.

```bash
# Test from Collector VM
ping <ontap-mgmt-ip>
curl -sk -u admin:<pass> https://<ontap-mgmt-ip>/api/cluster | jq .name

# Check ONTAP management LIF status
network interface show -role cluster-mgmt
```

**Resolution:** Confirm ONTAP management LIF is up, firewall rules allow 443 from Collector VM, and credentials stored in Collector config are current.

---

## Keystone Portal Shows Wrong Committed Capacity

**Symptom:** Portal committed TiB doesn't match the signed order.

**Action:** Open a support case with NetApp referencing subscription number. The committed values are provisioned by NetApp — they cannot be self-corrected.

---

## Quick Reference — Error Patterns

| Symptom | First Check |
|---|---|
| Stale last-collection timestamp | `keystone-collector status` + outbound 443 |
| Consumption spike | Snapshot accumulation on SVM |
| SnapMirror lag | `snapmirror show -fields lag-time,health` |
| Array unreachable | ONTAP mgmt LIF + firewall |
| Wrong committed capacity | NetApp support ticket |
