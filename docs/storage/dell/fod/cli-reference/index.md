# Flex on Demand (FOD) — CLI Reference

> Part of the [FOD](../) reference.

```mermaid
flowchart LR
    N["—"]
    N --> S0["Quick-Reference Command Table"]
    N --> S1["SYMCLI — Burst Usage and Allocations"]
    N --> S2["Unisphere REST API"]
    N --> S3["Monitoring Burst Threshold"]
    N --> S4["License Key Management"]
    N --> S5["Monthly Usage Tracking and Reporting"]
```

---

Flex on Demand is Dell's consumption-based capacity model for PowerMax/VMAX arrays. A base capacity is licensed outright; burst capacity above the committed level is metered and billed monthly. FOD monitoring involves tracking burst usage against the contracted burst threshold and pulling monthly consumption reports.

Management is via **SYMCLI** (Solutions Enabler) for local array queries and the **Unisphere REST API** for capacity and allocation data.

> **SID**: 12-digit SymmetrixID — find with `symcfg list`.  
> **Unisphere base URL**: `https://<unisphere_host>:8443`

---

## Quick-Reference Command Table

| Command | Purpose |
|---|---|
| `symcfg list -v -sid <sid>` | Array capacity overview including licensed and configured |
| `symcfg -sid <sid> list -allocations` | Allocation summary: consumed vs licensed capacity |
| `symcfg -sid <sid> show -pool` | SRP pool capacity (where FOD burst appears) |
| `symcfg -sid <sid> list -license` | License entitlements and FOD base/burst limits |
| `symlmf -sid <sid> report` | License management file report |
| `GET /univmax/restapi/100/system/symmetrix/{sid}` | Unisphere: array system info and capacity model |
| `GET /univmax/restapi/100/system/symmetrix/{sid}/system_capacity` | Unisphere: usable/subscribed/used capacity |
| `GET /univmax/restapi/100/sloprovisioning/symmetrix/{sid}/srp/{srp_id}` | SRP capacity breakdown for burst monitoring |

---

## SYMCLI — Burst Usage and Allocations

```bash
# --- Discover and list arrays ---
symcfg discover
symcfg list
symcfg list -v -sid <sid>

# --- Allocation summary: committed vs consumed ---
# Shows licensed (committed) capacity vs actual configured/used
symcfg -sid <sid> list -allocations

# Output key fields:
#   Allocated     – Capacity currently allocated to host volumes (TDEV)
#   Configured    – Capacity formatted into pools
#   Licensed      – Base + burst limit from license
#   Free          – Licensed minus Allocated (burst headroom)

# --- Storage Resource Pool capacity (burst shows as pool usage) ---
symcfg -sid <sid> show -pool
symcfg -sid <sid> show -pool -thin

# --- Per-device allocation (identify largest consumers) ---
# List all thin devices with allocated vs provisioned sizes
symdev -sid <sid> list -tdev

# Show allocation detail for a specific thin device
symdev -sid <sid> show <devid> -tdev

# --- SRP-level capacity per service level ---
symcfg -sid <sid> list -service_level_profile

# --- Disk group breakdown (base vs burst disk groups) ---
symcfg -sid <sid> list -disk

# --- Storage group capacity consumption ---
# List all storage groups with device count
symsg -sid <sid> list

# Show devices in a storage group with sizes
symsg -sid <sid> show <sg_name>

# --- Script: show capacity summary with burst threshold warning ---
BASE_TB=100    # Your contracted base capacity in TB
WARN_PCT=85    # Warn at this % of licensed capacity

symcfg list -v -sid <sid> | awk -v base="${BASE_TB}" -v warn="${WARN_PCT}" '
  /Licensed Capacity/  { lic=$NF }
  /Configured Capacity/{ cfg=$NF }
  END {
    lic_tb = lic/1048576
    cfg_tb = cfg/1048576
    pct    = (cfg_tb/lic_tb)*100
    printf "Licensed: %.1f TB  Configured: %.1f TB  Used: %.1f%%\n", lic_tb, cfg_tb, pct
    if (pct > warn) printf "WARNING: Usage exceeds %d%% of licensed capacity!\n", warn
  }'
```

---

## Unisphere REST API

```bash
UNISPHERE="https://<unisphere_host>:8443"
SID="<sid>"
USER="smc"
PASS="<password>"

# --- Get system info (includes licensing model: PERPETUAL, FOD, COD) ---
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/system/symmetrix/${SID}" \
  | python3 -m json.tool

# Key fields:
#   license_capability     – e.g. "FOD" indicating Flex on Demand array
#   model                  – Array model string
#   ucode                  – Firmware/microcode version

# --- Get system capacity (FOD burst monitoring) ---
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/system/symmetrix/${SID}/system_capacity" \
  | python3 -m json.tool

# Key capacity fields:
#   system_capacity.usable_total_tb          – Total licensed usable TB (base + activated burst)
#   system_capacity.usable_used_tb           – TB currently used
#   system_capacity.subscribed_total_tb      – Thin-provisioned total (logical allocation to hosts)
#   system_capacity.subscribed_allocated_tb  – TB actually written (demand vs subscribed)
#   system_capacity.snapshot_total_tb        – TB used by SnapVX snapshots

# --- SRP capacity breakdown ---
# List all SRPs
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/sloprovisioning/symmetrix/${SID}/srp" \
  | python3 -m json.tool

# Get SRP_1 details (primary SRP; shows FOD burst capacity tier)
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/sloprovisioning/symmetrix/${SID}/srp/SRP_1" \
  | python3 -m json.tool

# Calculate burst usage percentage from REST API response
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/system/symmetrix/${SID}/system_capacity" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)['system_capacity']
total = data.get('usable_total_tb', 0)
used  = data.get('usable_used_tb',  0)
pct   = (used / total * 100) if total else 0
print(f'Licensed: {total:.2f} TB  Used: {used:.2f} TB  ({pct:.1f}%)')
if pct > 80:
    print('ACTION: FOD burst usage above 80% — review with Dell account team.')
"
```

---

## Monitoring Burst Threshold

FOD contracts define a **base** commitment and a **burst ceiling**. Usage between base and ceiling is billed monthly. Usage above the burst ceiling may trigger over-usage charges or require an immediate license upgrade.

```bash
# --- Check current burst headroom ---
# Run monthly (or schedule via cron) to generate a burst usage snapshot

DATE=$(date +%Y-%m-%d)
REPORT_DIR="/var/log/fod-reports"
mkdir -p "${REPORT_DIR}"

symcfg list -v -sid <sid> > "${REPORT_DIR}/capacity_${DATE}.txt"
symcfg -sid <sid> list -allocations >> "${REPORT_DIR}/capacity_${DATE}.txt"
symcfg -sid <sid> show -pool >> "${REPORT_DIR}/capacity_${DATE}.txt"

echo "FOD capacity snapshot saved to ${REPORT_DIR}/capacity_${DATE}.txt"

# --- Cron job: daily capacity snapshot at 06:00 ---
# Add to /etc/cron.d/fod-monitor:
# 0 6 * * * root /usr/symcli/bin/symcfg list -v -sid <sid> > /var/log/fod-reports/capacity_$(date +\%Y-\%m-\%d).txt

# --- Alert if usage exceeds threshold ---
# Run from a monitoring script or cron:
BURST_WARN_TB=90    # Warn threshold in TB (below your burst ceiling)
BURST_CEIL_TB=120   # Your contracted burst ceiling

USED_TB=$(curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/system/symmetrix/${SID}/system_capacity" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['system_capacity']['usable_used_tb'])")

python3 -c "
used=${USED_TB}; warn=${BURST_WARN_TB}; ceil=${BURST_CEIL_TB}
if used > ceil:
    print(f'CRITICAL: FOD burst ceiling exceeded ({used:.1f} TB > {ceil} TB ceiling)')
elif used > warn:
    print(f'WARNING:  FOD burst threshold approaching ({used:.1f} TB > {warn} TB warning)')
else:
    print(f'OK: FOD burst usage nominal ({used:.1f} TB / {ceil} TB ceiling)')
"
```

---

## License Key Management

```bash
# --- List all license entitlements (identifies FOD base and burst tiers) ---
symcfg -sid <sid> list -license

# Common FOD-related license feature names:
#   PowerMax FOD Base Capacity      – Committed base TB
#   PowerMax FOD Burst Capacity     – Burst ceiling TB
#   VMAX3 Flex on Demand Base       – Legacy VMAX3 FOD base

# --- Show license management report ---
symlmf -sid <sid> report

# Export to file for record-keeping
symlmf -sid <sid> report -out /tmp/fod_license_report_$(date +%Y%m%d).txt

# --- Import an updated license file ---
# Obtained from Dell License Management portal (support.dell.com → Licensing)
# after purchasing additional base or burst capacity
symlmf -sid <sid> import -file /tmp/new_fod_license.dat

# Verify the import updated the licensed capacity
symcfg -sid <sid> list -license
symcfg list -v -sid <sid> | grep -E "Licensed|FOD|Configured"

# --- Check Solutions Enabler version ---
symcfg -version
```

---

## Monthly Usage Tracking and Reporting

FOD is billed based on the **maximum capacity used in any hour** during the billing month (peak-hour metering). Track this to forecast your monthly bill.

```bash
# --- Unisphere: capacity history (where available) ---
# Unisphere stores short-term capacity history; export for monthly records

curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/performance/Array/keys" \
  | python3 -m json.tool

# Get array-level performance data (includes capacity metrics)
curl -s -k -X POST \
  -u "${USER}:${PASS}" \
  -H "Content-Type: application/json" \
  "${UNISPHERE}/univmax/restapi/100/performance/Array/metrics" \
  -d "{
    \"symmetrixId\": \"${SID}\",
    \"startDate\": $(date -v-30d +%s000 2>/dev/null || date -d '30 days ago' +%s000),
    \"endDate\":   $(date +%s000),
    \"metrics\":   [\"HostIOs\", \"HostMBs\", \"PercentBusy\"],
    \"dataFormat\": \"Average\"
  }" | python3 -m json.tool

# --- Generate monthly FOD usage summary CSV ---
MONTH=$(date +%Y-%m)
OUT="/var/log/fod-reports/monthly_${MONTH}.csv"

{
  echo "date,licensed_tb,configured_tb,used_pct"
  for snapshot in /var/log/fod-reports/capacity_${MONTH}-*.txt; do
    d=$(basename "${snapshot}" .txt | sed 's/capacity_//')
    lic=$(grep "Licensed Capacity" "${snapshot}" | awk '{print $NF}')
    cfg=$(grep "Configured Capacity" "${snapshot}" | awk '{print $NF}')
    echo "${d},${lic},${cfg}"
  done
} > "${OUT}"

echo "Monthly FOD report written to ${OUT}"
```
