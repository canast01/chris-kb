---
tags:
  - netapp
  - operations
---
# NetApp Keystone — Script Reference


<div class="kb-summary">
Script Reference reference covering Subscription Utilization Report, ONTAP Volume Usage Snapshot, Keystone Collector Health Monitor.
</div>
```text
┌────────────────────────────── NetApp Keystone — Scripts and Automation ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Keystone scripts: automation for reporting, health monitoring, and provisioning        │   │
│   │         REST API available for all operations; PowerShell and Python modules supported        │   │
│   │          Scripts must run from dedicated service accounts with least-privilege roles          │   │
│   │        Store credentials in vault; rotate service account passwords on defined schedule       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Script → authenticate REST → execute operation → verify → log result                               │
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


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Subscription Utilization Report

Queries the Keystone portal API and generates a CSV report of committed vs consumed capacity per service tier.

```python
#!/usr/bin/env python3
"""
keystone-capacity-report.py
Requires: pip install requests
"""
import requests, csv, os
from datetime import datetime

PORTAL   = "https://keystone.netapp.com/api/v1"
TOKEN    = os.environ.get("KEYSTONE_TOKEN", "")
HDR      = {"Authorization": f"Bearer {TOKEN}"}
OUT_FILE = f"keystone-report-{datetime.now().strftime('%Y%m%d')}.csv"

def main():
    resp = requests.get(f"{PORTAL}/subscriptions", headers=HDR)
    resp.raise_for_status()
    subscriptions = resp.json().get("subscriptions", [])

    with open(OUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Subscription", "ServiceLevel", "CommittedTiB",
                         "ConsumedTiB", "BurstTiB", "PctUsed"])
        for sub in subscriptions:
            for tier in sub.get("serviceLevels", []):
                committed = tier.get("committedCapacity", 0)
                consumed  = tier.get("consumedCapacity", 0)
                burst     = tier.get("burstCapacity", 0)
                pct       = round(consumed / committed * 100, 1) if committed else 0
                writer.writerow([
                    sub.get("subscriptionNumber"),
                    tier.get("name"),
                    committed, consumed, burst, pct
                ])
                print(f"{tier.get('name'):<20} {consumed:>8.2f} / {committed:<8.2f} TiB  ({pct}%)")

    print(f"\nReport saved: {OUT_FILE}")

if __name__ == "__main__":
    main()
```

## ONTAP Volume Usage Snapshot

Pulls current volume usage from all Keystone-managed ONTAP arrays via REST API.

```bash
#!/usr/bin/env bash
# ontap-volume-usage.sh
# Usage: ONTAP_IP=<ip> ONTAP_USER=admin ONTAP_PASS=<pass> ./ontap-volume-usage.sh

ONTAP_IP="${ONTAP_IP:?ONTAP_IP required}"
ONTAP_USER="${ONTAP_USER:-admin}"
ONTAP_PASS="${ONTAP_PASS:?ONTAP_PASS required}"
SVM="${SVM:-}"   # optional: filter by SVM name

AUTH="$ONTAP_USER:$ONTAP_PASS"
BASE="https://$ONTAP_IP/api"
QUERY="fields=name,svm,space"
[[ -n "$SVM" ]] && QUERY="$QUERY&svm.name=$SVM"

echo "=== Volume Usage Report: $ONTAP_IP $(date) ==="
printf "%-40s %-20s %12s %12s %8s\n" "Volume" "SVM" "UsedGiB" "TotalGiB" "Used%"
printf '%.0s-' {1..96}; echo

curl -sk -u "$AUTH" "$BASE/storage/volumes?$QUERY&limit=500" | \
jq -r '.records[] | [
    .name,
    .svm.name,
    (.space.used / 1073741824 | round),
    (.space.size / 1073741824 | round),
    (if .space.size > 0 then (.space.used / .space.size * 100 | round) else 0 end)
] | @tsv' | \
awk -F'\t' '{ printf "%-40s %-20s %12s %12s %7s%%\n", $1, $2, $3, $4, $5 }' | sort
```

## Keystone Collector Health Monitor

Runs from cron on the Collector VM. Sends an alert if Collector has not collected within the last 2 hours.

```bash
#!/usr/bin/env bash
# ks-collector-monitor.sh
# Add to cron: 0 * * * * /opt/scripts/ks-collector-monitor.sh

ALERT_EMAIL="infra@example.com"
MAX_AGE_HOURS=2

LAST=$(keystone-collector show-last-collection 2>/dev/null | \
    grep -oP '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')

if [[ -z "$LAST" ]]; then
    echo "Keystone Collector: no collection timestamp found" | \
        mail -s "[ALERT] Keystone Collector - No Collection Data" "$ALERT_EMAIL"
    exit 1
fi

LAST_EPOCH=$(date -d "$LAST" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "$LAST" +%s)
NOW_EPOCH=$(date +%s)
AGE_HOURS=$(( (NOW_EPOCH - LAST_EPOCH) / 3600 ))

if (( AGE_HOURS >= MAX_AGE_HOURS )); then
    echo "Last successful collection was ${AGE_HOURS}h ago (threshold: ${MAX_AGE_HOURS}h)" | \
        mail -s "[ALERT] Keystone Collector - Stale Collection" "$ALERT_EMAIL"
    exit 1
fi

echo "Keystone Collector OK - last collection ${AGE_HOURS}h ago"
```
