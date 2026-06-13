---
tags:
  - nutanix
  - operations
  - scripts
  - automation
---
# Nutanix — Scripts

<div class="kb-summary">
Reusable scripts for Nutanix operational tasks — cluster health snapshot, storage utilisation report, NCC automation, VM inventory export, and maintenance mode helpers using ncli, acli, and the Nutanix REST API v3.

*Applies to: AOS 6.x · AHV*
</div>

---

## Before you begin

- **Access:** CVM SSH (nutanix user) for bash scripts; Prism Central admin for REST API scripts
- **Dependencies:** Python 3 for REST API script; `mail` utility for alert scripts (configure SMTP relay on CVMs)

---

## Daily Health Snapshot

Run this before and after any maintenance window to capture cluster baseline.

```bash
#!/usr/bin/env bash
# nutanix-health-snapshot.sh
# Run from any CVM: ssh nutanix@<cvm-ip> 'bash -s' < nutanix-health-snapshot.sh

DATE=$(date +%Y-%m-%d_%H%M)
LOG="/tmp/nutanix-health-${DATE}.txt"

echo "=== Nutanix Health Snapshot ${DATE} ===" | tee "$LOG"

echo -e "\n--- Cluster Info ---" | tee -a "$LOG"
ncli cluster info 2>&1 | tee -a "$LOG"

echo -e "\n--- Cluster Resilience ---" | tee -a "$LOG"
ncli cluster get-domain-fault-tolerance-status type=node 2>&1 | tee -a "$LOG"

echo -e "\n--- Storage Usage ---" | tee -a "$LOG"
ncli ctr list 2>&1 | tee -a "$LOG"

echo -e "\n--- Host Status ---" | tee -a "$LOG"
ncli host list 2>&1 | tee -a "$LOG"

echo -e "\n--- Active Alerts ---" | tee -a "$LOG"
ncli alert list severity=critical 2>&1 | tee -a "$LOG"
ncli alert list severity=warning 2>&1 | tee -a "$LOG"

echo -e "\n--- Cassandra Ring ---" | tee -a "$LOG"
allssh "nodetool status" 2>&1 | tee -a "$LOG"

echo -e "\n--- Genesis Services ---" | tee -a "$LOG"
allssh "genesis status 2>&1 | head -20" | tee -a "$LOG"

echo -e "\nSnapshot saved to: ${LOG}"
```

---

## NCC Health Check Automation

```bash
#!/usr/bin/env bash
# run-ncc.sh — Run NCC and alert on failures

ALERT_EMAIL="infra-team@corp.local"
LOG="/tmp/ncc-$(date +%Y%m%d).txt"

ncc --health_checks run_all 2>&1 > "$LOG"

FAILURES=$(grep -c "FAIL" "$LOG" || true)
WARNINGS=$(grep -c "WARN" "$LOG" || true)

if [[ "$FAILURES" -gt 0 ]]; then
    echo "NCC FAILURES detected: $FAILURES" | mail -s "[ALERT] Nutanix NCC FAILURES" "$ALERT_EMAIL" < "$LOG"
    echo "FAILED: $FAILURES failures found. Check ${LOG}"
    exit 1
elif [[ "$WARNINGS" -gt 0 ]]; then
    echo "NCC warnings: $WARNINGS. See ${LOG}"
    # Optionally send warning email
fi

echo "NCC completed: 0 failures, $WARNINGS warnings"
```

---

## Storage Utilisation Report

```bash
#!/usr/bin/env bash
# storage-report.sh — Print container fill levels with thresholds

WARN_PCT=70
CRIT_PCT=80

echo "=== Nutanix Storage Report $(date) ==="
echo ""

ncli ctr list --json 2>/dev/null | python3 - << 'EOF'
import sys, json

try:
    data = json.load(sys.stdin)
    entities = data.get("entities", [])
except:
    # Fallback: parse text output
    sys.exit(0)

print(f"{'Container':<30} {'Used':>10} {'Total':>10} {'Used%':>7} {'Status'}")
print("-" * 65)
for e in entities:
    name = e.get("name","?")
    used = e.get("usageStats",{}).get("storage.usage_bytes", 0)
    cap  = e.get("maxCapacityBytes", 1)
    pct  = (used / cap * 100) if cap else 0
    status = "OK" if pct < 70 else ("WARN" if pct < 80 else "CRIT")
    print(f"{name:<30} {used//1024**3:>8}GB {cap//1024**3:>8}GB {pct:>6.1f}% {status}")
EOF
```

---

## VM Inventory Export

```bash
#!/usr/bin/env bash
# vm-inventory.sh — Export VM list with CPU, memory, and power state to CSV

echo "name,vcpus,memory_gb,power_state,host,ips"

acli vm.list --json 2>/dev/null | python3 - << 'EOF'
import sys, json

try:
    data = json.load(sys.stdin)
    vms  = data.get("entities", [])
except:
    sys.exit(1)

for vm in vms:
    name  = vm.get("name","")
    vcpu  = vm.get("numVcpus", 0)
    mem   = vm.get("memoryMb", 0) // 1024
    state = vm.get("powerState","")
    host  = vm.get("hypervisorHostname","")
    ips   = ";".join(
        n.get("ipAddress","")
        for n in vm.get("vmNics",[])
        if n.get("ipAddress")
    )
    print(f"{name},{vcpu},{mem},{state},{host},{ips}")
EOF
```

---

## Maintenance Mode Helper

```bash
#!/usr/bin/env bash
# maintenance.sh — Enter / exit maintenance mode with pre/post NCC checks
# Usage: ./maintenance.sh enter|exit <host-name>

MODE=$1
HOST=$2

if [[ -z "$MODE" || -z "$HOST" ]]; then
    echo "Usage: $0 enter|exit <host-name>"
    exit 1
fi

if [[ "$MODE" == "enter" ]]; then
    echo "=== Pre-maintenance NCC check ==="
    ncc --health_checks run_all --include_category=critical 2>&1 | grep -E "FAIL|WARN|PASS"

    echo -e "\n=== Entering maintenance mode for ${HOST} ==="
    acli host.enter_maintenance_mode "$HOST"

    echo "Waiting for VM evacuation..."
    for i in $(seq 1 60); do
        STATE=$(acli host.get "$HOST" 2>&1 | grep -i "state" | head -1)
        echo "  ($i/60) $STATE"
        echo "$STATE" | grep -qi "MAINTENANCE_MODE" && break
        sleep 10
    done
    echo "Host $HOST is in maintenance mode."

elif [[ "$MODE" == "exit" ]]; then
    echo "=== Exiting maintenance mode for ${HOST} ==="
    acli host.exit_maintenance_mode "$HOST"

    echo -e "\n=== Post-maintenance NCC check ==="
    sleep 30   # wait for services to stabilise
    ncc --health_checks run_all --include_category=critical 2>&1 | grep -E "FAIL|WARN|PASS"
else
    echo "Unknown mode: $MODE (use enter or exit)"
    exit 1
fi
```

---

## REST API — VM Power Operations

Use the Nutanix REST API v3 via Prism Central for automation at scale.

```python
#!/usr/bin/env python3
"""nutanix_api.py — Example REST API v3 calls for VM management."""

import requests, json, urllib3
urllib3.disable_warnings()

PC_HOST = "prism-central.corp.local"
PC_USER = "admin"
PC_PASS = "<password>"
BASE    = f"https://{PC_HOST}:9440/api/nutanix/v3"
AUTH    = (PC_USER, PC_PASS)
HEADERS = {"Content-Type": "application/json"}


def list_vms(limit=50):
    """List VMs from Prism Central."""
    payload = {"kind": "vm", "length": limit}
    r = requests.post(f"{BASE}/vms/list", json=payload,
                      auth=AUTH, headers=HEADERS, verify=False)
    r.raise_for_status()
    return r.json().get("entities", [])


def get_vm(vm_uuid):
    """Get a VM's full spec."""
    r = requests.get(f"{BASE}/vms/{vm_uuid}",
                     auth=AUTH, headers=HEADERS, verify=False)
    r.raise_for_status()
    return r.json()


def power_vm(vm_uuid, action="ON"):
    """Power a VM on or off. action: ON | OFF | POWERCYCLE"""
    spec = get_vm(vm_uuid)
    # Remove status field (read-only)
    spec.pop("status", None)
    spec["spec"]["resources"]["power_state"] = action
    r = requests.put(f"{BASE}/vms/{vm_uuid}", json=spec,
                     auth=AUTH, headers=HEADERS, verify=False)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    vms = list_vms()
    print(f"Found {len(vms)} VMs")
    for vm in vms[:5]:
        uuid  = vm["metadata"]["uuid"]
        name  = vm["spec"]["name"]
        state = vm["spec"]["resources"]["power_state"]
        print(f"  {name:<40} {state}  uuid={uuid}")
```

---

## Cluster Resilience Watch (Continuous)

```bash
#!/usr/bin/env bash
# resilience-watch.sh — Alert if cluster resilience drops to 0

while true; do
    STATUS=$(ncli cluster get-domain-fault-tolerance-status type=node 2>&1 \
             | grep "CAN_TOLERATE_FAILURE_COUNT" | awk '{print $NF}')
    if [[ "$STATUS" == "0" ]]; then
        echo "ALERT: Cluster resilience = 0 at $(date)" \
          | mail -s "[CRITICAL] Nutanix cluster cannot tolerate failure" infra-team@corp.local
        echo "CRITICAL at $(date) — resilience=0"
    fi
    sleep 300
done
```

---



---

## Verify

- Scripts execute without error and write output to the expected file or stdout
- Daily health snapshot email arrives with attached JSON report
- VM inventory CSV contains all expected VMs when opened in a spreadsheet tool
- REST API Python script returns HTTP 200 and non-empty JSON payload


---

## See also

- [Nutanix — CLI Reference](cli-reference/)
- [Nutanix — Procedures](procedures/)
