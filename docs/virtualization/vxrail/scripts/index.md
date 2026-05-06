# Scripts

> Part of the [VxRail](../) reference.

---

## VxRail Cluster Health Check (PowerShell / PowerCLI)

Connect to vCenter managing VxRail and query the VxRail Manager REST API to report cluster health, node states, and active faults.

~~~powershell
#!/usr/bin/env pwsh
# vxrail-cluster-health.ps1
# Usage: ./vxrail-cluster-health.ps1 -VxRailMgrHost <host> -VxRailUser <user> -VxRailPass <pass>

param(
    [Parameter(Mandatory)][string]$VxRailMgrHost = $env:VXRAIL_MGR_HOST,
    [Parameter(Mandatory)][string]$VxRailUser    = $env:VXRAIL_USER,
    [Parameter(Mandatory)][string]$VxRailPass    = $env:VXRAIL_PASS
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Suppress SSL certificate errors for self-signed certs
if (-not ([System.Management.Automation.PSTypeName]'TrustAllCertsPolicy').Type) {
    Add-Type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) { return true; }
    }
"@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
}
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

$BaseUrl = "https://$VxRailMgrHost/rest/vxm"
$Auth    = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${VxRailUser}:${VxRailPass}"))
$Headers = @{ Authorization = "Basic $Auth"; "Content-Type" = "application/json" }

function Invoke-VxRailApi {
    param([string]$Path)
    $response = Invoke-RestMethod -Uri "$BaseUrl$Path" -Headers $Headers -Method GET
    return $response
}

Write-Host "`n=== VxRail Cluster Health Check ===" -ForegroundColor Cyan
Write-Host "Host: $VxRailMgrHost  Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"

# --- Cluster overview ---
$cluster = Invoke-VxRailApi "/v1/cluster"
Write-Host "Cluster Version : $($cluster.version)"
Write-Host "Cluster Health  : $($cluster.health)"

# --- Host list ---
$hosts = Invoke-VxRailApi "/v1/hosts"
Write-Host "Node Count      : $($hosts.Count)`n"

$faultCount = 0

Write-Host ("{0,-20} {1,-12} {2,-8} {3,-8} {4,-8} {5,-8}" -f "Serial", "Health", "CPU", "Memory", "Disk", "NIC")
Write-Host ("-" * 70)

foreach ($node in $hosts) {
    $cpu    = $node.component_health | Where-Object { $_.component -eq "CPU" }    | Select-Object -ExpandProperty health
    $mem    = $node.component_health | Where-Object { $_.component -eq "MEMORY" } | Select-Object -ExpandProperty health
    $disk   = $node.component_health | Where-Object { $_.component -eq "DISK" }   | Select-Object -ExpandProperty health
    $nic    = $node.component_health | Where-Object { $_.component -eq "NIC" }    | Select-Object -ExpandProperty health

    $rowColor = if ($node.health -ne "Healthy") { "Red" } else { "Green" }
    Write-Host ("{0,-20} {1,-12} {2,-8} {3,-8} {4,-8} {5,-8}" -f `
        $node.serial_number, $node.health, $cpu, $mem, $disk, $nic) -ForegroundColor $rowColor

    if ($node.health -ne "Healthy") { $faultCount++ }
}

# --- System health / active faults ---
Write-Host ""
$sysHealth = Invoke-VxRailApi "/v1/system/health"

if ($sysHealth.faults -and $sysHealth.faults.Count -gt 0) {
    Write-Host "Active Faults ($($sysHealth.faults.Count)):" -ForegroundColor Red
    foreach ($fault in $sysHealth.faults) {
        Write-Host "  [$(($fault.severity).ToUpper())] $($fault.description)" -ForegroundColor Yellow
        $faultCount++
    }
} else {
    Write-Host "Active Faults   : None" -ForegroundColor Green
}

Write-Host ""
if ($faultCount -gt 0) {
    Write-Host "RESULT: UNHEALTHY — $faultCount issue(s) found." -ForegroundColor Red
    exit 1
} else {
    Write-Host "RESULT: HEALTHY" -ForegroundColor Green
    exit 0
}
~~~

---

## LCM Upgrade Readiness Check (Bash)

Query the VxRail Manager REST API to determine the current version, available updates, and whether all nodes are healthy before an LCM upgrade.

~~~bash
#!/usr/bin/env bash
# vxrail-lcm-readiness.sh
# Usage: VXRAIL_MGR_HOST=<host> VXRAIL_USER=<user> VXRAIL_PASS=<pass> ./vxrail-lcm-readiness.sh

set -euo pipefail

VXRAIL_MGR_HOST="${VXRAIL_MGR_HOST:?VXRAIL_MGR_HOST is required}"
VXRAIL_USER="${VXRAIL_USER:?VXRAIL_USER is required}"
VXRAIL_PASS="${VXRAIL_PASS:?VXRAIL_PASS is required}"

BASE_URL="https://${VXRAIL_MGR_HOST}/rest/vxm"
CURL_OPTS=(-sk -u "${VXRAIL_USER}:${VXRAIL_PASS}" -H "Content-Type: application/json")

rc=0

vxm_get() {
    curl "${CURL_OPTS[@]}" "${BASE_URL}${1}"
}

echo ""
echo "=== VxRail LCM Upgrade Readiness Check ==="
echo "Host : ${VXRAIL_MGR_HOST}"
echo "Time : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# --- Current version ---
CURRENT_VERSION=$(vxm_get "/v1/system/version" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('version','unknown'))")
echo "Current Version  : ${CURRENT_VERSION}"

# --- Available updates ---
ADVISORY=$(vxm_get "/v2/lcm/upgrade/advisory")
AVAILABLE_VERSION=$(echo "${ADVISORY}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
releases = d.get('advisory', {}).get('upgrade_advisories', [])
if releases:
    print(releases[0].get('target_version', 'none'))
else:
    print('none')
")
echo "Available Version: ${AVAILABLE_VERSION}"

if [[ "${AVAILABLE_VERSION}" == "none" ]]; then
    echo "No upgrade available. Cluster is at latest."
fi

# --- Node health ---
echo ""
echo "Node Health:"
echo "-------------------------------------------------------------"
printf "%-20s %-12s %-10s\n" "Serial" "Health" "PSNT"

HOSTS_JSON=$(vxm_get "/v1/hosts")
ALL_HEALTHY=true

python3 - <<EOF
import json, sys
hosts = json.loads('''${HOSTS_JSON}''')
all_ok = True
for h in hosts:
    health = h.get('health', 'unknown')
    serial = h.get('serial_number', 'unknown')
    psnt   = h.get('psnt', 'unknown')
    status = "OK" if health == "Healthy" else "FAULT"
    if health != "Healthy":
        all_ok = False
    print(f"{serial:<20} {health:<12} {psnt:<10}  {status}")
print()
if all_ok:
    print("All nodes: HEALTHY")
    sys.exit(0)
else:
    print("ERROR: One or more nodes are NOT healthy. Upgrade not recommended.")
    sys.exit(1)
EOF
node_rc=$?

# --- vSAN health (via vCenter API placeholder) ---
echo ""
echo "vSAN Health      : (verify manually via vCenter or vSAN Health Check plugin)"

# --- Summary ---
echo ""
if [[ $node_rc -ne 0 ]]; then
    echo "PRE-CHECK RESULT : FAIL — Unhealthy nodes detected. Do not proceed with LCM."
    exit 1
elif [[ "${AVAILABLE_VERSION}" == "none" ]]; then
    echo "PRE-CHECK RESULT : INFO — No upgrade available."
    exit 0
else
    echo "PRE-CHECK RESULT : PASS — Ready to upgrade from ${CURRENT_VERSION} to ${AVAILABLE_VERSION}."
    exit 0
fi
~~~

---

## Node Hardware Status (Bash)

Retrieve per-node hardware health from the VxRail Manager REST API and flag any component not in a Healthy state.

~~~bash
#!/usr/bin/env bash
# vxrail-node-hardware.sh
# Usage: VXRAIL_MGR_HOST=<host> VXRAIL_USER=<user> VXRAIL_PASS=<pass> ./vxrail-node-hardware.sh

set -euo pipefail

VXRAIL_MGR_HOST="${VXRAIL_MGR_HOST:?VXRAIL_MGR_HOST is required}"
VXRAIL_USER="${VXRAIL_USER:?VXRAIL_USER is required}"
VXRAIL_PASS="${VXRAIL_PASS:?VXRAIL_PASS is required}"

BASE_URL="https://${VXRAIL_MGR_HOST}/rest/vxm"
CURL_OPTS=(-sk -u "${VXRAIL_USER}:${VXRAIL_PASS}" -H "Content-Type: application/json")

FAULT_COUNT=0

vxm_get() {
    curl "${CURL_OPTS[@]}" "${BASE_URL}${1}"
}

echo ""
echo "=== VxRail Node Hardware Status ==="
echo "Host : ${VXRAIL_MGR_HOST}"
echo "Time : $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Get all host serial numbers
HOST_SERIALS=$(vxm_get "/v1/hosts" | python3 -c "
import sys, json
hosts = json.load(sys.stdin)
for h in hosts:
    print(h['serial_number'])
")

for SERIAL in ${HOST_SERIALS}; do
    echo "Node: ${SERIAL}"
    echo "  $(printf '%-8s %-20s %-10s %s' 'Type' 'Component' 'Health' 'Details')"
    echo "  $(printf '%0.s-' {1..65})"

    HW_JSON=$(vxm_get "/v1/hosts/${SERIAL}/hardware")

    python3 - <<EOF
import json, sys

hw = json.loads('''${HW_JSON}''')

sections = {
    'PSU':  hw.get('psu', []),
    'Fan':  hw.get('fan', []),
    'Disk': hw.get('disk', []),
    'NIC':  hw.get('nic', []),
}

fault_count = 0
for section, items in sections.items():
    for item in items:
        name   = item.get('name', item.get('slot', 'unknown'))
        health = item.get('health', 'unknown')
        detail = item.get('description', '')
        flag   = '' if health == 'Healthy' else '  <-- FAULT'
        if health != 'Healthy':
            fault_count += 1
        print(f"  {section:<8} {name:<20} {health:<10} {detail}{flag}")

if fault_count:
    print(f"\n  FAULTS DETECTED: {fault_count} component(s) not Healthy")
    sys.exit(1)
else:
    print(f"\n  All components Healthy")
    sys.exit(0)
EOF
    hw_rc=$?
    if [[ $hw_rc -ne 0 ]]; then
        FAULT_COUNT=$((FAULT_COUNT + 1))
    fi
    echo ""
done

if [[ $FAULT_COUNT -gt 0 ]]; then
    echo "OVERALL: ${FAULT_COUNT} node(s) with hardware faults."
    exit 1
else
    echo "OVERALL: All nodes hardware Healthy."
    exit 0
fi
~~~

---

## Ansible VxRail Health Playbook

Use the Ansible `uri` module to authenticate against VxRail Manager, collect cluster and host health, retrieve system faults, assert no critical faults, and print a structured summary.

~~~yaml
---
# vxrail-health.yml
# Usage: ansible-playbook vxrail-health.yml -e "vxrail_mgr=192.0.2.10 vxrail_user=admin vxrail_pass=secret"

- name: VxRail Health Check
  hosts: localhost
  gather_facts: false

  vars:
    vxrail_mgr:  "{{ lookup('env', 'VXRAIL_MGR_HOST') }}"
    vxrail_user: "{{ lookup('env', 'VXRAIL_USER') }}"
    vxrail_pass: "{{ lookup('env', 'VXRAIL_PASS') }}"
    base_url:    "https://{{ vxrail_mgr }}/rest/vxm"
    auth_header: "{{ ('Basic ' + (vxrail_user + ':' + vxrail_pass) | b64encode) }}"

  tasks:

    # --- 1. Get cluster health ---
    - name: Get cluster health
      uri:
        url: "{{ base_url }}/v1/cluster"
        method: GET
        headers:
          Authorization: "{{ auth_header }}"
          Content-Type: "application/json"
        validate_certs: false
        return_content: true
      register: cluster_result

    - name: Set cluster facts
      set_fact:
        cluster_version: "{{ cluster_result.json.version }}"
        cluster_health:  "{{ cluster_result.json.health }}"

    # --- 2. Get host health ---
    - name: Get host health
      uri:
        url: "{{ base_url }}/v1/hosts"
        method: GET
        headers:
          Authorization: "{{ auth_header }}"
          Content-Type: "application/json"
        validate_certs: false
        return_content: true
      register: hosts_result

    - name: Set host facts
      set_fact:
        vxrail_hosts: "{{ hosts_result.json }}"

    # --- 3. Get system faults ---
    - name: Get system faults
      uri:
        url: "{{ base_url }}/v1/system/faults"
        method: GET
        headers:
          Authorization: "{{ auth_header }}"
          Content-Type: "application/json"
        validate_certs: false
        return_content: true
      register: faults_result

    - name: Set faults fact
      set_fact:
        system_faults: "{{ faults_result.json }}"

    # --- 4. Assert no critical faults ---
    - name: Assert no critical faults
      assert:
        that:
          - "system_faults | selectattr('severity', 'equalto', 'CRITICAL') | list | length == 0"
        fail_msg: >
          CRITICAL faults detected:
          {{ system_faults | selectattr('severity', 'equalto', 'CRITICAL') | map(attribute='description') | list | join(', ') }}
        success_msg: "No critical faults found."

    # --- 5. Print health summary ---
    - name: Print cluster summary
      debug:
        msg:
          - "Cluster Version : {{ cluster_version }}"
          - "Cluster Health  : {{ cluster_health }}"
          - "Node Count      : {{ vxrail_hosts | length }}"

    - name: Print per-node health
      debug:
        msg: >
          Node {{ item.serial_number }}: health={{ item.health }}
          {% for comp in item.component_health | default([]) %}
          {{ comp.component }}={{ comp.health }}
          {% endfor %}
      loop: "{{ vxrail_hosts }}"
      loop_control:
        label: "{{ item.serial_number }}"

    - name: Print fault list
      debug:
        msg: "[{{ item.severity }}] {{ item.description }}"
      loop: "{{ system_faults }}"
      loop_control:
        label: "{{ item.severity }}"
      when: system_faults | length > 0
~~~
