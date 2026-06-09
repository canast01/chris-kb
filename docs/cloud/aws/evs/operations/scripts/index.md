# Amazon EVS — Scripts

<div class="kb-summary">
Operational scripts for EVS: daily health check, host add/remove workflow, vSAN capacity report, and HCX migration status tracker.
</div>

```text
┌────────────────────────────────── Amazon EVS — Operational Scripts ───────────────────────────────────┐
│                                                                                                       │
│   Three operational scripts: daily health check, vSAN capacity report, and HCX service mesh status    │
│   All scripts require environment variables for credentials; no plaintext passwords in script files   │
│   Run health-check.sh daily via cron; vsan-capacity.ps1 and hcx-status.sh on-demand or scheduled      │
│                                                                                                       │
│   health-check.sh                                                                                     │
│   Checks: EVS environment state (expect CREATED), all host states, NSX control cluster stability      │
│   Inputs: EVS_ENV_ID, VCENTER_HOST, VCENTER_PASSWORD, NSX_MANAGER_URL, NSX_PASSWORD                   │
│   Output: per-check [OK]/[FAIL] lines; exits 0 on all-pass, exits 1 on any failure                    │
│                                                                                                       │
│   vsan-capacity.ps1                                                                                   │
│   Connects to vCenter via PowerCLI; queries all vSAN datastores for capacity and free space           │
│   Thresholds: >80% used = WARN, >70% = INFO, ≤70% = OK; outputs formatted table                       │
│   Inputs: VCENTER_HOST, VCENTER_PASSWORD environment variables                                        │
│                                                                                                       │
│   hcx-status.sh                                                                                       │
│   Queries HCX Manager REST API for service mesh link status and HCX version                           │
│   Inputs: HCX_MANAGER_IP, HCX_PASSWORD environment variables                                          │
│   Output: per-link [OK]/[FAIL] with label and status; HCX version string                              │
│                                                                                                       │
│   Key terms:                                                                                          │
│   EVS environment = the AWS-managed VMware cluster; environment-id is the unique identifier           │
│   NSX control cluster = NSX-T management plane; STABLE means all managers are in consensus            │
│   HCX service mesh = VMware HCX interconnect between on-premises and EVS; links must be UP            │
│   vSAN datastore  = VMware vSAN storage pool on the EVS cluster; monitored for capacity headroom      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## health-check.sh

```bash
#!/bin/bash
# EVS Daily Health Check Script
# Usage: EVS_ENV_ID=env-xxx VCENTER_HOST=vcenter.vcf.internal ./health-check.sh

set -euo pipefail
ENV_ID="${EVS_ENV_ID:?Set EVS_ENV_ID}"
VCENTER="${VCENTER_HOST:?Set VCENTER_HOST}"
VCENTER_PASS="${VCENTER_PASSWORD:?Set VCENTER_PASSWORD}"
NSX_URL="${NSX_MANAGER_URL:?Set NSX_MANAGER_URL}"
NSX_PASS="${NSX_PASSWORD:?Set NSX_PASSWORD}"

PASS=0; FAIL=0

check() {
  local name="$1"; shift
  if eval "$@" &>/dev/null; then
    echo "  [OK]  $name"
    ((PASS++))
  else
    echo "  [FAIL] $name"
    ((FAIL++))
  fi
}

echo "=== EVS Health Check $(date +%F) ==="

echo ""
echo "[AWS EVS Cluster]"
STATE=$(aws evs get-environment --environment-id "$ENV_ID" \
  --query 'environment.state' --output text 2>/dev/null)
[[ "$STATE" == "CREATED" ]] && echo "  [OK]  Cluster state: $STATE" \
  || echo "  [FAIL] Cluster state: $STATE (expected CREATED)"; ((STATE == "CREATED")) && PASS++ || FAIL++

HOST_STATES=$(aws evs list-environment-hosts --environment-id "$ENV_ID" \
  --query 'hostSummaries[*].state' --output text 2>/dev/null)
FAILED_HOSTS=$(echo "$HOST_STATES" | tr ' ' '\n' | grep -cv "^CREATED$" || true)
[[ "$FAILED_HOSTS" -eq 0 ]] && echo "  [OK]  All hosts CREATED" \
  || echo "  [FAIL] $FAILED_HOSTS host(s) not in CREATED state"; PASS=$((PASS + (FAILED_HOSTS == 0))); FAIL=$((FAIL + (FAILED_HOSTS > 0)))

echo ""
echo "[NSX-T Manager]"
NSX_STATUS=$(curl -sk -u "admin:$NSX_PASS" "$NSX_URL/api/v1/cluster/status" \
  --connect-timeout 5 | python3 -c "import sys,json; print(json.load(sys.stdin).get('control_cluster_status',{}).get('status','UNKNOWN'))" 2>/dev/null)
[[ "$NSX_STATUS" == "STABLE" ]] && echo "  [OK]  NSX control cluster: $NSX_STATUS" \
  || echo "  [FAIL] NSX control cluster: $NSX_STATUS (expected STABLE)"; PASS=$((PASS + (NSX_STATUS == "STABLE"))); FAIL=$((FAIL + (NSX_STATUS != "STABLE")))

echo ""
echo "[Summary]"
echo "  PASSED: $PASS  FAILED: $FAIL"
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
```

## vsan-capacity.ps1

```powershell
# EVS vSAN Capacity Report
# Usage: VCENTER_PASSWORD=xxx pwsh -File vsan-capacity.ps1

param(
    [string]$VCenter = $env:VCENTER_HOST,
    [string]$User    = "administrator@vsphere.local",
    [string]$Pass    = $env:VCENTER_PASSWORD
)

Connect-VIServer -Server $VCenter -User $User -Password $Pass -WarningAction SilentlyContinue | Out-Null

Get-Datastore -Name *vsan* | ForEach-Object {
    $ds = $_
    $usedGB = [math]::Round($ds.CapacityGB - $ds.FreeSpaceGB, 1)
    $usedPct = [math]::Round($usedGB / $ds.CapacityGB * 100, 1)
    $status = if ($usedPct -gt 80) { "WARN" } elseif ($usedPct -gt 70) { "INFO" } else { "OK" }
    [PSCustomObject]@{
        Datastore   = $ds.Name
        CapacityGB  = [math]::Round($ds.CapacityGB, 1)
        UsedGB      = $usedGB
        FreeGB      = [math]::Round($ds.FreeSpaceGB, 1)
        UsedPct     = "$usedPct%"
        Status      = $status
    }
} | Format-Table -AutoSize

Disconnect-VIServer -Confirm:$false | Out-Null
```

## hcx-status.sh

```bash
#!/bin/bash
# HCX Service Mesh Status Check
# Usage: HCX_MANAGER_IP=10.x.x.x HCX_PASSWORD=xxx ./hcx-status.sh

HCX_IP="${HCX_MANAGER_IP:?Set HCX_MANAGER_IP}"
HCX_PASS="${HCX_PASSWORD:?Set HCX_PASSWORD}"

echo "=== HCX Service Mesh Status ==="
curl -sk -u "admin:$HCX_PASS" \
  "https://$HCX_IP/hybridity/api/interconnect/links" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for link in data.get('items', []):
    status = link.get('status', 'UNKNOWN')
    label = link.get('label', 'unknown')
    icon = '[OK]' if status == 'UP' else '[FAIL]'
    print(f'  {icon}  {label}: {status}')
"

echo ""
echo "=== HCX Version ==="
curl -sk -u "admin:$HCX_PASS" \
  "https://$HCX_IP/hybridity/api/about" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"  Version: {d.get('version','unknown')}\")"
```
