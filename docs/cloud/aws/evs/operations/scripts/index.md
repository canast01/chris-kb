# Amazon EVS — Scripts

<div class="kb-summary">
Operational scripts for EVS: daily health check, host add/remove workflow, vSAN capacity report, HCX migration status tracker, safe host removal, VCF password rotation, and capacity reporting.
</div>

```text
┌────────────────────────────────── Amazon EVS — Operational Scripts ───────────────────────────────────┐
│                                                                                                       │
│   Six operational scripts covering EVS cluster health, host lifecycle, credential management          │
│   All scripts require environment variables for credentials; no plaintext passwords in script files   │
│                                                                                                       │
│   health-check.sh    Daily EVS cluster, host, and NSX-T health check with exit code                   │
│   vsan-capacity.ps1  PowerCLI vSAN capacity report with WARN/INFO/OK thresholds                       │
│   hcx-status.sh      HCX service mesh link status and version check                                   │
│   host-remove.sh     Safe host removal: BytesToSync check, maintenance mode, AWS delete               │
│   vcf-password-rotate.sh  SDDC Manager credential rotation via REST API with task polling             │
│   evs-capacity-report.sh  Full capacity report: AWS hosts, vSAN storage, VM count per host            │
│                                                                                                       │
│   Key terms:                                                                                          │
│   EVS environment  = the AWS-managed VMware cluster; environment-id is the unique identifier          │
│   NSX control cluster = NSX-T management plane; STABLE means all managers are in consensus            │
│   HCX service mesh = VMware HCX interconnect between on-premises and EVS; links must be UP            │
│   BytesToSync      = vSAN resync metric; must be 0 before removing a host safely                      │
│   SDDC Manager     = VCF management appliance; owns all component credentials for rotation            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## health-check.sh

```bash
#!/bin/bash
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
  || echo "  [FAIL] $FAILED_HOSTS host(s) not in CREATED state"
PASS=$((PASS + (FAILED_HOSTS == 0))); FAIL=$((FAIL + (FAILED_HOSTS > 0)))

echo ""
echo "[NSX-T Manager]"
NSX_STATUS=$(curl -sk -u "admin:$NSX_PASS" "$NSX_URL/api/v1/cluster/status" \
  --connect-timeout 5 | python3 -c \
  "import sys,json; print(json.load(sys.stdin).get('control_cluster_status',{}).get('status','UNKNOWN'))" 2>/dev/null)
[[ "$NSX_STATUS" == "STABLE" ]] && echo "  [OK]  NSX control cluster: $NSX_STATUS" \
  || echo "  [FAIL] NSX control cluster: $NSX_STATUS (expected STABLE)"
PASS=$((PASS + (NSX_STATUS == "STABLE"))); FAIL=$((FAIL + (NSX_STATUS != "STABLE")))

echo ""
echo "[Summary]"
echo "  PASSED: $PASS  FAILED: $FAIL"
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
```

## vsan-capacity.ps1

```powershell
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

## host-remove.sh

Automates the safe host removal sequence. Refuses to proceed if vSAN has outstanding resync data.

```bash
#!/bin/bash
set -euo pipefail

ENV_ID="${EVS_ENV_ID:?Set EVS_ENV_ID}"
HOST_ID="${EVS_HOST_ID:?Set EVS_HOST_ID}"
VCENTER="${VCENTER_HOST:?Set VCENTER_HOST}"
VCENTER_USER="${VCENTER_USER:-administrator@vsphere.local}"
VCENTER_PASS="${VCENTER_PASSWORD:?Set VCENTER_PASSWORD}"
ESXI_HOST="${ESXI_HOSTNAME:?Set ESXI_HOSTNAME (FQDN of the host to remove)}"
CLUSTER_NAME="${CLUSTER_NAME:-EVS-Management-Cluster}"

check_bytes_to_sync() {
  pwsh -NonInteractive -Command "
    Connect-VIServer -Server '${VCENTER}' -User '${VCENTER_USER}' -Password '${VCENTER_PASS}' -WarningAction SilentlyContinue | Out-Null
    \$cluster = Get-Cluster -Name '${CLUSTER_NAME}'
    \$resync = Get-VsanResyncDashboard -Cluster \$cluster
    Write-Output \$resync.BytesToSync
    Disconnect-VIServer -Confirm:\$false | Out-Null
  " 2>/dev/null
}

enter_maintenance_mode() {
  echo "  Putting ${ESXI_HOST} into maintenance mode with vSAN full data evacuation..."
  pwsh -NonInteractive -Command "
    Connect-VIServer -Server '${VCENTER}' -User '${VCENTER_USER}' -Password '${VCENTER_PASS}' -WarningAction SilentlyContinue | Out-Null
    Set-VMHost -VMHost '${ESXI_HOST}' -State Maintenance -Evacuate \$true -Confirm:\$false | Out-Null
    Write-Output 'Maintenance mode requested.'
    Disconnect-VIServer -Confirm:\$false | Out-Null
  "
}

poll_bytes_to_sync() {
  local max_wait=7200
  local elapsed=0
  local interval=60
  echo "  Polling vSAN BytesToSync (timeout: ${max_wait}s)..."
  while [[ $elapsed -lt $max_wait ]]; do
    local bts
    bts=$(check_bytes_to_sync)
    echo "    [$(date +%T)] BytesToSync=${bts}"
    if [[ "$bts" == "0" ]]; then
      echo "  vSAN evacuation complete."
      return 0
    fi
    sleep $interval
    elapsed=$((elapsed + interval))
  done
  echo "  ERROR: vSAN evacuation did not complete within ${max_wait}s. Aborting."
  return 1
}

verify_host_gone() {
  local max_wait=1800
  local elapsed=0
  local interval=30
  echo "  Waiting for host to disappear from EVS host list..."
  while [[ $elapsed -lt $max_wait ]]; do
    local state
    state=$(aws evs list-environment-hosts --environment-id "$ENV_ID" \
      --query "hostSummaries[?hostId=='${HOST_ID}'].state" --output text 2>/dev/null)
    if [[ -z "$state" ]]; then
      echo "  Host ${HOST_ID} is no longer in the host list."
      return 0
    fi
    echo "    [$(date +%T)] Host state: ${state}"
    sleep $interval
    elapsed=$((elapsed + interval))
  done
  echo "  WARNING: Host did not disappear within ${max_wait}s."
  return 1
}

echo "=== EVS Host Removal: ${HOST_ID} ==="
echo ""

echo "[Step 1] Pre-check: verifying minimum host count..."
HOST_COUNT=$(aws evs list-environment-hosts --environment-id "$ENV_ID" \
  --query 'length(hostSummaries)' --output text)
if [[ "$HOST_COUNT" -le 3 ]]; then
  echo "  ERROR: Only ${HOST_COUNT} host(s) in cluster. Cannot remove — minimum is 3 remaining."
  exit 1
fi
echo "  Host count: ${HOST_COUNT} (will be $((HOST_COUNT - 1)) after removal — OK)"

echo ""
echo "[Step 2] Pre-check: verifying vSAN BytesToSync is 0..."
BTS=$(check_bytes_to_sync)
if [[ "$BTS" != "0" ]]; then
  echo "  ERROR: vSAN BytesToSync=${BTS}. Cluster has outstanding resync data."
  echo "  Wait for vSAN to finish resyncing before removing a host."
  exit 1
fi
echo "  BytesToSync=0 — vSAN is healthy."

echo ""
echo "[Step 3] Entering maintenance mode with vSAN full data evacuation..."
enter_maintenance_mode

echo ""
echo "[Step 4] Waiting for vSAN evacuation to complete..."
poll_bytes_to_sync

echo ""
echo "[Step 5] Deleting host via AWS EVS API..."
aws evs delete-environment-host \
  --environment-id "$ENV_ID" \
  --host-id "$HOST_ID"
echo "  delete-environment-host submitted."

echo ""
echo "[Step 6] Waiting for host to be removed from EVS list..."
verify_host_gone

echo ""
echo "[Step 7] Remaining hosts in cluster:"
aws evs list-environment-hosts --environment-id "$ENV_ID" \
  --query 'hostSummaries[*].[hostId,hostName,state]' --output table

echo ""
echo "=== Host removal complete ==="
```

## vcf-password-rotate.sh

Automates VCF credential rotation via SDDC Manager REST API.

```bash
#!/bin/bash
set -euo pipefail

SDDC_HOST="${SDDC_MANAGER_HOST:?Set SDDC_MANAGER_HOST}"
SDDC_USER="${SDDC_MANAGER_USER:-administrator@vsphere.local}"
SDDC_PASS="${SDDC_MANAGER_PASSWORD:?Set SDDC_MANAGER_PASSWORD}"
SDDC_URL="https://${SDDC_HOST}"
POLL_INTERVAL=30
POLL_TIMEOUT=1800

get_token() {
  curl -sk -X POST "${SDDC_URL}/v1/tokens" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"${SDDC_USER}\",\"password\":\"${SDDC_PASS}\"}" | \
    python3 -c "import sys,json; print(json.load(sys.stdin).get('accessToken',''))"
}

list_credentials() {
  local token="$1"
  curl -sk -H "Authorization: Bearer ${token}" \
    "${SDDC_URL}/v1/credentials" | \
    python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"{'Entity':<40} {'Type':<20} {'Username':<30}\")
print('-' * 90)
for c in d.get('elements', []):
    print(f\"{c.get('entityName',''):<40} {c.get('credentialType',''):<20} {c.get('username',''):<30}\")
"
}

initiate_rotation() {
  local token="$1"
  curl -sk -X PATCH \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    "${SDDC_URL}/v1/credentials" \
    -d '{"operationType":"ROTATE","elements":[{"resourceName":"ALL"}]}' | \
    python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))"
}

poll_task() {
  local token="$1"
  local task_id="$2"
  local elapsed=0
  echo "  Polling task ${task_id}..."
  while [[ $elapsed -lt $POLL_TIMEOUT ]]; do
    local result
    result=$(curl -sk -H "Authorization: Bearer ${token}" \
      "${SDDC_URL}/v1/tasks/${task_id}" | \
      python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('status',''), d.get('completionTimestamp',''))
")
    local status
    status=$(echo "$result" | awk '{print $1}')
    echo "    [$(date +%T)] Status: ${result}"
    if [[ "$status" == "Successful" ]]; then
      return 0
    elif [[ "$status" == "Failed" ]]; then
      echo "  ERROR: Rotation task failed."
      return 1
    fi
    sleep $POLL_INTERVAL
    elapsed=$((elapsed + POLL_INTERVAL))
  done
  echo "  ERROR: Task did not complete within ${POLL_TIMEOUT}s."
  return 1
}

echo "=== VCF Credential Rotation ==="
echo "  SDDC Manager: ${SDDC_HOST}"
echo ""

echo "[Step 1] Authenticating to SDDC Manager..."
TOKEN=$(get_token)
if [[ -z "$TOKEN" ]]; then
  echo "  ERROR: Failed to get access token. Check credentials."
  exit 1
fi
echo "  Token obtained."

echo ""
echo "[Step 2] Current credentials managed by SDDC Manager:"
list_credentials "$TOKEN"

echo ""
echo "[Step 3] Initiating credential rotation for ALL components..."
TASK_ID=$(initiate_rotation "$TOKEN")
if [[ -z "$TASK_ID" ]]; then
  echo "  ERROR: Failed to initiate rotation task."
  exit 1
fi
echo "  Rotation task ID: ${TASK_ID}"

echo ""
echo "[Step 4] Polling rotation task until complete..."
poll_task "$TOKEN" "$TASK_ID"

echo ""
echo "[Step 5] Final credential list after rotation:"
NEW_TOKEN=$(get_token)
list_credentials "$NEW_TOKEN"

echo ""
echo "=== Credential rotation complete ==="
echo "  Update any external automation or scripts that reference VCF credentials."
```

## evs-capacity-report.sh

Generates a consolidated capacity report covering AWS host inventory, vSAN storage, and VM density.

```bash
#!/bin/bash
set -euo pipefail

ENV_ID="${EVS_ENV_ID:?Set EVS_ENV_ID}"
VCENTER="${VCENTER_HOST:?Set VCENTER_HOST}"
VCENTER_USER="${VCENTER_USER:-administrator@vsphere.local}"
VCENTER_PASS="${VCENTER_PASSWORD:?Set VCENTER_PASSWORD}"
CLUSTER_NAME="${CLUSTER_NAME:-EVS-Management-Cluster}"
WARN_THRESHOLD=80
REPORT_DATE=$(date +%F)

print_section() {
  echo ""
  echo "================================================================"
  echo "  $1"
  echo "================================================================"
}

get_aws_hosts() {
  aws evs list-environment-hosts --environment-id "$ENV_ID" \
    --query 'hostSummaries[*].[hostName,instanceType,state]' \
    --output table
}

get_vsan_capacity() {
  pwsh -NonInteractive -Command "
    Connect-VIServer -Server '${VCENTER}' -User '${VCENTER_USER}' -Password '${VCENTER_PASS}' -WarningAction SilentlyContinue | Out-Null
    Get-Datastore -Name '*vsan*' | ForEach-Object {
      \$ds = \$_
      \$usedGB = [math]::Round(\$ds.CapacityGB - \$ds.FreeSpaceGB, 1)
      \$usedPct = [math]::Round(\$usedGB / \$ds.CapacityGB * 100, 1)
      \$freeGB = [math]::Round(\$ds.FreeSpaceGB, 1)
      \$headroomGB = [math]::Round(\$ds.CapacityGB * (1 - ${WARN_THRESHOLD}/100), 1)
      \$status = if (\$usedPct -gt ${WARN_THRESHOLD}) { 'WARN' } elseif (\$usedPct -gt 70) { 'INFO' } else { 'OK' }
      Write-Output \"  Datastore : \$(\$ds.Name)\"
      Write-Output \"  Capacity  : \$([math]::Round(\$ds.CapacityGB,1)) GB\"
      Write-Output \"  Used      : \${usedGB} GB (\${usedPct}%)\"
      Write-Output \"  Free      : \${freeGB} GB\"
      Write-Output \"  Headroom  : \${headroomGB} GB at ${WARN_THRESHOLD}% threshold\"
      Write-Output \"  Status    : \${status}\"
    }
    Disconnect-VIServer -Confirm:\$false | Out-Null
  " 2>/dev/null
}

get_vm_count_per_host() {
  pwsh -NonInteractive -Command "
    Connect-VIServer -Server '${VCENTER}' -User '${VCENTER_USER}' -Password '${VCENTER_PASS}' -WarningAction SilentlyContinue | Out-Null
    Get-Cluster -Name '${CLUSTER_NAME}' | Get-VMHost | ForEach-Object {
      \$h = \$_
      \$vmCount = (Get-VM -Location \$h).Count
      \$cpuPct = [math]::Round(\$h.ExtensionData.Summary.QuickStats.OverallCpuUsage / (\$h.NumCpu * 1000) * 100, 1)
      \$memPct = [math]::Round(\$h.MemoryUsageGB / \$h.MemoryTotalGB * 100, 1)
      Write-Output \"  \$(\$h.Name)  VMs=\${vmCount}  CPU=\${cpuPct}%  MEM=\${memPct}%\"
    }
    Disconnect-VIServer -Confirm:\$false | Out-Null
  " 2>/dev/null
}

echo "=== EVS Capacity Report — ${REPORT_DATE} ==="
echo "  Environment: ${ENV_ID}"
echo "  vCenter: ${VCENTER}"

print_section "AWS Host Inventory"
get_aws_hosts

print_section "vSAN Storage Capacity"
get_vsan_capacity

print_section "VM Count and Resource Usage per Host"
get_vm_count_per_host

print_section "Report Complete"
echo "  Generated: $(date)"
```
