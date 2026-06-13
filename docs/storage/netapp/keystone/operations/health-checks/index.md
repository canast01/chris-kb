---
tags:
  - netapp
  - operations
---
# Keystone — Health Checks


<div class="kb-summary">
Part of the [Keystone Operations](../index.md) reference.
</div>
```text
┌─────────────────────────────────── NetApp Keystone — Health Checks ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Keystone health checks: routine verification of operational status and performance      │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
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
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
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

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Service health** — Keystone customer portal → Dashboard — check overall service status
2. **Consumed capacity** — verify consumed capacity vs committed capacity per service tier
3. **Burst usage** — check if burst capacity is being consumed — flag if sustained above committed
4. **SLA compliance** — verify performance metrics (IOPS, latency) meet contracted SLA
5. **Open support cases** — review any open cases affecting Keystone service delivery
6. **Billing alerts** — check for any threshold alerts from the Keystone portal

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Verify Keystone Collector service is running | `systemctl status keystone-collector` | Service must show `active (running)` |
| Check last successful telemetry timestamp | `journalctl -u keystone-collector -n 50 \| grep -i "collection\|reported\|error"` | Timestamp should be within the last hour |
| Review BlueXP Keystone dashboard | Navigate to BlueXP → Digital Wallet → Keystone Subscriptions | Check consumed vs. committed per tier |
| Check burst usage | Review BlueXP dashboard burst panel | Flag if burst > 10% above committed on any tier |
| Verify AQoS policy assignments | `volume show -fields qos-policy-group` on ONTAP cluster | No blank QoS policy groups on Keystone volumes |
| Confirm API endpoint reachability from Collector | `curl -sk https://keystone.netapp.com` from Collector VM | Must receive HTTP 200 or 401 (reachable) |
| Review Collector error log | `sudo tail -50 /var/log/keystone-collector/keystone-collector.log` | Look for `ERROR` or `WARN` entries |

---

## Health Check Criteria

A healthy Keystone environment meets all of the following:

- [ ] Keystone Collector service is `active (running)` — not failed, activating, or stopped
- [ ] Last successful telemetry collection is within the past 1 hour (or within the expected polling interval for your configuration)
- [ ] No `ERROR`-level entries in the Collector log in the last 24 hours
- [ ] BlueXP Keystone dashboard data is current — not stale from a previous day
- [ ] No service-level SLA breach notifications active (availability, latency, IOPS/TB)
- [ ] All Keystone-managed volumes have an AQoS adaptive policy-group assigned — no unclassified volumes
- [ ] Burst usage across all tiers is within acceptable range — not approaching the burst limit defined in the subscription
- [ ] No open Keystone support incidents with P1 or P2 severity

---

## Collector Health Commands

Run these commands on the Keystone Collector VM (SSH access required):

```bash
# Check Keystone Collector service status (systemd)
sudo systemctl status keystone-collector
# Expected: Active: active (running) since <timestamp>
# Uptime should reflect continuous operation without recent restarts

# View recent Collector logs — look for successful collection timestamps
sudo journalctl -u keystone-collector -n 100
# Look for lines containing: "collection complete", "data reported", "telemetry sent"

# Tail the Collector log file directly
sudo tail -100 /var/log/keystone-collector/keystone-collector.log

# Check for ERROR or WARN entries in the last 24 hours
sudo journalctl -u keystone-collector --since "24 hours ago" | grep -iE "ERROR|WARN|FAIL|exception"

# Test Collector connectivity to NetApp Keystone endpoint
curl -sk -o /dev/null -w "HTTP %{http_code}\n" https://keystone.netapp.com
# Expected: HTTP 200 or HTTP 401 (reachable; 401 is auth-required, which confirms network path is open)

# Check if a proxy is configured for the Collector (if your environment requires one)
sudo cat /etc/keystone-collector/config.conf | grep -i proxy
```

---

## ONTAP Health Commands

Run these commands on the ONTAP cluster backing the Keystone subscription:

```bash
# Verify AQoS adaptive policy-groups exist for all Keystone service levels
qos adaptive-policy-group show

# Check all volumes and their QoS policy-group assignments
volume show -fields vserver,volume,qos-policy-group

# Identify volumes with no QoS policy-group (unclassified — billing risk)
volume show -fields vserver,volume,qos-policy-group | grep " - "
# Any volume showing "-" in the qos-policy-group column is unclassified

# Confirm ONTAP cluster is reachable from the Collector VM
# (run from the Collector VM)
curl -sk https://<cluster-mgmt-lif>/api/cluster | python3 -m json.tool
# Verify cluster name and ONTAP version in the response

# Review logical used capacity per volume (what Keystone measures for billing)
volume show -fields size,used,logical-used,percent-used

# Check aggregate-level free space (must remain adequate for Keystone provisioning)
storage aggregate show -fields size,used,available,percent-used

# View QoS workload statistics for Keystone service level tiers
qos statistics performance show
```

---

## Capacity and Burst Health

```bash
# Check current consumed vs. committed via the Keystone REST API
# (replace with your actual subscription ID and token)
SUBSCRIPTION_ID="KS-XXXXX"
TOKEN="<your-api-token>"

curl -s "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/usage" \
    -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tier in data.get('service_levels', data.get('tiers', [])):
    name      = tier.get('name', 'unknown')
    committed = float(tier.get('committed_tib', tier.get('committed', 0)))
    consumed  = float(tier.get('consumed_tib',  tier.get('consumed',  0)))
    burst     = float(tier.get('burst_tib',     tier.get('burst',     0)))
    pct       = (consumed / committed * 100) if committed > 0 else 0
    status    = 'BURST' if consumed > committed else ('WARN' if pct >= 90 else 'OK')
    print(f'{status:6s}  {name:20s}  {consumed:8.2f} / {committed:8.2f} TiB  ({pct:.1f}%  burst={burst:.2f} TiB)')
"
```

---

## Burst Threshold Escalation

| Consumed vs. Committed | Status | Action |
|---|---|---|
| < 80% of committed | Normal | No action |
| 80–89% of committed | Warning | Review growth trend; consider capacity amendment request |
| 90–99% of committed | Near-burst | Initiate capacity amendment process; notify KSM |
| > 100% of committed (burst active) | Burst billing active | Identify source of overconsumption; decommission unused volumes; expedite amendment |
| Approaching burst limit | Critical | Emergency amendment required; contact KSM immediately |

---

## Weekly Health Review

Beyond the daily checks, perform these weekly:

```bash
# Compare ONTAP volume logical usage vs. Keystone billing report
# to identify any discrepancy between what ONTAP reports and what is billed
volume show -vserver * -fields vserver,volume,logical-used | sort -k3 -rn | head -20

# Check snapshot usage on Keystone volumes — excessive snapshots consume committed capacity
snapshot show -vserver * -volume * -fields vserver,volume,size | sort -k4 -rn | head -20

# Review QoS throttling events — volumes being throttled may indicate workloads
# exceeding their service level IOPS ceiling
qos statistics performance show | grep -v "0 IOPS"

# Verify no new volumes were created without a QoS policy-group
volume show -fields vserver,volume,qos-policy-group -state online | grep " - "
```

---

## Health Check Output Reference

| Field | Healthy Value | Investigate If |
|---|---|---|
| Collector systemd status | `active (running)` | `failed`, `inactive`, or recent restarts |
| Last collection timestamp | < 1 hour ago | > 2 hours without a successful collection |
| Collector log ERROR entries | 0 in last 24h | Any ERROR in last 24h |
| BlueXP data freshness | Current day | Shows yesterday's data or older |
| Volumes with no QoS policy | 0 | Any online Keystone volume without a policy |
| Burst status | 0% on all tiers | Any tier > 90% consumed |
| ONTAP cluster reachable from Collector | HTTP 200/401 | HTTP 000 (connection failure) or HTTP 500 |
