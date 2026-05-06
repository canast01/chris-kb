# Scripts

> Part of the [ESXi](../) reference.

---

## ESXi Host Health Check (PowerShell / PowerCLI)

Connect to vCenter or directly to an ESXi host and produce a per-host health report covering hardware sensors, datastore usage, network adapter state, and required service status.

~~~powershell
#Requires -Modules VMware.PowerCLI
# esxi_host_health.ps1
# Usage: pwsh -File esxi_host_health.ps1
# Env vars: VCENTER_HOST, VC_USER, VC_PASS

param(
    [string]$VCenterHost = $env:VCENTER_HOST,
    [string]$VCUser      = $env:VC_USER,
    [string]$VCPass      = $env:VC_PASS
)

Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null

$cred = New-Object System.Management.Automation.PSCredential(
    $VCUser, (ConvertTo-SecureString $VCPass -AsPlainText -Force)
)
Connect-VIServer -Server $VCenterHost -Credential $cred -ErrorAction Stop | Out-Null

$RequiredServices = @('hostd', 'vpxa', 'ntpd')
$DatastoreWarnPct  = 80
$overallExit = 0

function Write-Status {
    param($Label, $Status, $Detail)
    $colour = switch ($Status) {
        'PASS'     { 'Green'  }
        'WARNING'  { 'Yellow' }
        'CRITICAL' { 'Red'    }
        default    { 'White'  }
    }
    Write-Host ("[{0,-8}] {1,-35} {2}" -f $Status, $Label, $Detail) -ForegroundColor $colour
}

foreach ($vmhost in (Get-VMHost | Sort-Object Name)) {
    Write-Host "`n=== $($vmhost.Name) ===" -ForegroundColor Cyan

    # Connection / power state
    if ($vmhost.ConnectionState -ne 'Connected') {
        Write-Status "ConnectionState" "CRITICAL" $vmhost.ConnectionState
        $overallExit = 2; continue
    }
    if ($vmhost.PowerState -ne 'PoweredOn') {
        Write-Status "PowerState" "WARNING" $vmhost.PowerState
        $overallExit = [Math]::Max($overallExit, 1)
    } else {
        Write-Status "ConnectionState" "PASS" "Connected / PoweredOn"
    }

    # Hardware sensors
    try {
        $hw = Get-VMHostHardware -VMHost $vmhost -ErrorAction Stop
        $badSensors = $hw.CpuInfo | Where-Object { $_.HealthState -ne 'Green' }
        if ($badSensors) {
            Write-Status "Hardware Sensors" "WARNING" "$($badSensors.Count) sensor(s) not green"
            $overallExit = [Math]::Max($overallExit, 1)
        } else {
            Write-Status "Hardware Sensors" "PASS" "All sensors green"
        }
    } catch {
        Write-Status "Hardware Sensors" "WARNING" "Could not retrieve hardware info"
    }

    # Datastore capacity
    $datastores = Get-Datastore -VMHost $vmhost
    foreach ($ds in $datastores) {
        if ($ds.CapacityGB -eq 0) { continue }
        $usedPct = [Math]::Round((1 - $ds.FreeSpaceGB / $ds.CapacityGB) * 100, 1)
        $s = if ($usedPct -ge $DatastoreWarnPct) { 'WARNING' } else { 'PASS' }
        if ($s -eq 'WARNING') { $overallExit = [Math]::Max($overallExit, 1) }
        Write-Status "Datastore: $($ds.Name)" $s ("Used={0}%  Free={1:N0}GB" -f $usedPct, $ds.FreeSpaceGB)
    }

    # Network adapters
    $badNics = Get-VMHostNetworkAdapter -VMHost $vmhost | Where-Object { -not $_.BitRatePerSec -and $_.DeviceName -notmatch 'vmk' }
    if ($badNics) {
        Write-Status "Network Adapters" "WARNING" "$($badNics.DeviceName -join ', ') — no link"
        $overallExit = [Math]::Max($overallExit, 1)
    } else {
        Write-Status "Network Adapters" "PASS" "All adapters have link"
    }

    # Required services
    $services = Get-VMHostService -VMHost $vmhost
    foreach ($svc in $RequiredServices) {
        $s = $services | Where-Object { $_.Key -eq $svc }
        if (-not $s -or $s.Running -eq $false) {
            Write-Status "Service: $svc" "CRITICAL" "NOT RUNNING"
            $overallExit = 2
        } else {
            Write-Status "Service: $svc" "PASS" "Running"
        }
    }
}

Disconnect-VIServer -Confirm:$false
exit $overallExit
~~~

---

## Storage Path Health Check (Bash / esxcli)

Run on an ESXi host via SSH. Report per-device path counts (active / standby / dead) and exit non-zero if any dead paths exist.

~~~bash
#!/bin/bash
# esxi_path_health.sh
# Usage: ssh root@esxi-host 'bash -s' < esxi_path_health.sh
# Or run locally on the ESXi host.

CRIT=0
TS=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

echo "==================================="
echo " ESXi Storage Path Health Check"
echo " $TS"
echo "==================================="
printf "%-40s %8s %8s %8s %8s %s\n" "Device" "Active" "Standby" "Dead" "Total" "Status"
printf "%-40s %8s %8s %8s %8s %s\n" "------" "------" "-------" "----" "-----" "------"

# Build per-device path summary from nmp device list
current_device=""
declare -A active standby dead total

while IFS= read -r line; do
    if [[ $line =~ ^[[:space:]]Device\ Display\ Name:.*\(([^)]+)\) ]]; then
        current_device="${BASH_REMATCH[1]}"
    elif [[ $line =~ ^[[:space:]]Device\ Display\ Name:\ (.*) && -z "$current_device" ]]; then
        current_device="$(echo "$line" | awk -F': ' '{print $2}')"
    fi
done < <(esxcli storage nmp device list 2>/dev/null)

# Use path list for counts
declare -A path_active path_standby path_dead

while IFS= read -r line; do
    if [[ $line =~ ^[[:space:]]Device:\ (.*) ]]; then
        dev="${BASH_REMATCH[1]// /}"
    elif [[ $line =~ State:\ (active|standby|dead|disabled) ]]; do
        state="${BASH_REMATCH[1]}"
        case "$state" in
            active)   (( path_active["$dev"]++  )) ;;
            standby)  (( path_standby["$dev"]++ )) ;;
            dead)     (( path_dead["$dev"]++    )) ;;
        esac
    fi
done < <(esxcli storage core path list 2>/dev/null)

for dev in $(echo "${!path_active[@]} ${!path_standby[@]} ${!path_dead[@]}" | tr ' ' '\n' | sort -u); do
    a="${path_active[$dev]:-0}"
    s="${path_standby[$dev]:-0}"
    d="${path_dead[$dev]:-0}"
    t=$(( a + s + d ))
    if (( d > 0 )); then
        status="DEAD_PATHS"
        CRIT=1
    elif (( a == 0 )); then
        status="NO_ACTIVE"
        CRIT=1
    else
        status="OK"
    fi
    printf "%-40s %8d %8d %8d %8d %s\n" "$dev" "$a" "$s" "$d" "$t" "$status"
done

echo
if [ $CRIT -eq 1 ]; then
    echo "RESULT: CRITICAL — dead or missing paths detected"
else
    echo "RESULT: PASS — all paths healthy"
fi
exit $CRIT
~~~

---

## ESXi Syslog and Event Collector (Python)

Connect to vCenter via pyVmomi, retrieve events from the last 24 hours filtered by severity, and report NMP/storage errors.

~~~python
#!/usr/bin/env python3
"""
esxi_event_collector.py
Usage: python3 esxi_event_collector.py
Deps: pip install pyVmomi
"""

import os, ssl, sys
from datetime import datetime, timedelta, timezone
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

VCENTER_HOST = os.environ.get("VCENTER_HOST", "vcenter.local")
VC_USER      = os.environ.get("VC_USER",      "administrator@vsphere.local")
VC_PASS      = os.environ.get("VC_PASS",      "")
HOURS_BACK   = int(os.environ.get("HOURS_BACK", "24"))

# Event types to capture
WARN_TYPES = {
    vim.event.EventEx,
    vim.event.GeneralHostWarningEvent,
    vim.event.GeneralHostErrorEvent,
    vim.event.VmFailedToSuspendEvent,
    vim.event.DatastoreCapacityIncreasedEvent,
}

NMP_PATTERNS = ["NMP", "Dead path", "SCSI", "storage", "LUN", "vmhba"]


def connect_vcenter():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=VCENTER_HOST, user=VC_USER, pwd=VC_PASS, sslContext=context)
    return si


def collect_events(si):
    content = si.RetrieveContent()
    em = content.eventManager

    start_time = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)
    filter_spec = vim.event.EventFilterSpec(
        time=vim.event.EventFilterSpec.ByTime(beginTime=start_time),
    )
    events = em.QueryEvents(filter=filter_spec)
    return events


def collect_host_vmkernel_events(si):
    """Scan vmkernel.log for NMP/storage messages via host ConfigManager."""
    content = si.RetrieveContent()
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.HostSystem], True
    )
    findings = []
    for host in container.view:
        try:
            dm = host.configManager.diagnosticSystem
            if not dm:
                continue
            # Read last 500 lines of vmkernel
            lines = dm.BrowseDiagnosticLog(key="vmkernel", start=None, lines=500)
            for entry in (lines.lineText or "").splitlines():
                if any(p.lower() in entry.lower() for p in NMP_PATTERNS):
                    findings.append(f"  [{host.name}] {entry.strip()}")
        except Exception:
            pass
    container.Destroy()
    return findings


si = connect_vcenter()
events = collect_events(si)

print(f"Events from last {HOURS_BACK}h on {VCENTER_HOST}")
print(f"Total events retrieved: {len(events)}")
print()

issues = []
for e in sorted(events, key=lambda x: x.createdTime):
    msg = getattr(e, 'fullFormattedMessage', str(e))
    lvl = "INFO"
    if isinstance(e, (vim.event.GeneralHostErrorEvent,)):
        lvl = "ERROR"
    elif isinstance(e, (vim.event.GeneralHostWarningEvent,)):
        lvl = "WARNING"
    if lvl in ("ERROR", "WARNING"):
        ts = e.createdTime.strftime('%Y-%m-%dT%H:%M:%SZ')
        host = getattr(e.host, 'name', 'N/A') if hasattr(e, 'host') else 'N/A'
        issues.append(f"  [{lvl}] {ts}  host={host}  {msg[:120]}")

if issues:
    print(f"Host events (WARNING/ERROR):")
    for i in issues:
        print(i)
else:
    print("No WARNING/ERROR host events found.")

print()
print("VMkernel NMP/storage log entries:")
vmk_entries = collect_host_vmkernel_events(si)
if vmk_entries:
    for e in vmk_entries[:50]:
        print(e)
else:
    print("  None found.")

Disconnect(si)
sys.exit(1 if issues or vmk_entries else 0)
~~~

---

## NTP Configuration Audit (Bash)

SSH to each ESXi host (or run locally), verify NTP service state, configured servers, and time offset.

~~~bash
#!/bin/bash
# esxi_ntp_audit.sh
# Usage: ESXI_HOSTS="host1 host2 host3" ./esxi_ntp_audit.sh
# Requires passwordless SSH to each host as root.

ESXI_HOSTS="${ESXI_HOSTS:-esxi01 esxi02 esxi03}"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10 -o BatchMode=yes"
OFFSET_WARN_MS=500
OFFSET_CRIT_MS=2000
overall=0

printf "%-25s %-20s %-10s %-12s %s\n" "Hostname" "NTP Server(s)" "Service" "Offset(ms)" "Status"
printf "%-25s %-20s %-10s %-12s %s\n" "--------" "-------------" "-------" "----------" "------"

for host in $ESXI_HOSTS; do
    run() { ssh $SSH_OPTS "root@${host}" "$1" 2>/dev/null; }

    svc_status=$(run "/etc/init.d/ntpd status" | grep -io 'running\|stopped\|not running' | head -1)
    svc_status="${svc_status:-unknown}"

    ntp_servers=$(run "esxcli system ntp get" | awk '/NTP Servers:/{for(i=3;i<=NF;i++) printf $i" "; print ""}' | xargs)
    [ -z "$ntp_servers" ] && ntp_servers="NOT_CONFIGURED"

    # Get time offset from ntpq or chronyc
    offset_raw=$(run "ntpq -p 2>/dev/null | awk 'NR>2{print \$9}' | head -1")
    if [[ "$offset_raw" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
        offset_ms=$(printf "%.0f" "$offset_raw")
        abs_offset=${offset_ms#-}
    else
        offset_ms="N/A"
        abs_offset=0
    fi

    status="OK"
    if [[ "$svc_status" != "running" ]]; then
        status="SVC_DOWN"
        overall=2
    elif [[ "$ntp_servers" == "NOT_CONFIGURED" ]]; then
        status="NO_NTP_SERVER"
        overall=2
    elif (( abs_offset >= OFFSET_CRIT_MS )); then
        status="HIGH_DRIFT"
        overall=2
    elif (( abs_offset >= OFFSET_WARN_MS )); then
        status="WARN_DRIFT"
        [ $overall -lt 1 ] && overall=1
    fi

    printf "%-25s %-20s %-10s %-12s %s\n" "$host" "${ntp_servers:0:20}" "$svc_status" "${offset_ms}ms" "$status"
done

echo
case $overall in
    0) echo "Overall: PASS"    ;;
    1) echo "Overall: WARNING" ;;
    2) echo "Overall: CRITICAL";;
esac
exit $overall
~~~

---

## Ansible ESXi Configuration Playbook

Use the `community.vmware` collection to verify NTP, DNS, syslog, and SSH security profile compliance across all ESXi hosts in a cluster.

~~~yaml
---
# esxi_compliance.yml
# Usage: ansible-playbook -i inventory esxi_compliance.yml
# Deps: ansible-galaxy collection install community.vmware
# Vars: vcenter_hostname, datacenter_name, cluster_name, vc_username, vc_password

- name: ESXi Host Configuration Compliance Check
  hosts: localhost
  gather_facts: false
  vars:
    vcenter_hostname: vcenter.local
    datacenter_name:  Production
    cluster_name:     Cluster-01
    vc_username:      "{{ lookup('env','VC_USER') }}"
    vc_password:      "{{ lookup('env','VC_PASS') }}"
    ntp_servers:
      - 192.168.1.1
      - 192.168.1.2
    dns_servers:
      - 192.168.1.53
    syslog_host: "udp://syslog.local:514"

  tasks:

    - name: Gather ESXi host facts
      community.vmware.vmware_host_facts:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        cluster:    "{{ cluster_name }}"
        validate_certs: false
      register: host_facts

    - name: Check NTP configuration per host
      community.vmware.vmware_host_ntp:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        esxi_hostname: "{{ item }}"
        ntp_servers: "{{ ntp_servers }}"
        validate_certs: false
        state: present
      loop: "{{ host_facts.hosts_facts.keys() | list }}"

    - name: Check DNS configuration per host
      community.vmware.vmware_host_dns:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        esxi_hostname: "{{ item }}"
        dns_servers: "{{ dns_servers }}"
        validate_certs: false
      loop: "{{ host_facts.hosts_facts.keys() | list }}"

    - name: Check syslog target per host
      community.vmware.vmware_host_config_manager:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        esxi_hostname: "{{ item }}"
        options:
          'Syslog.global.logHost': "{{ syslog_host }}"
        validate_certs: false
      loop: "{{ host_facts.hosts_facts.keys() | list }}"

    - name: Check SSH security profile (SSH should be disabled in production)
      community.vmware.vmware_host_service:
        hostname:   "{{ vcenter_hostname }}"
        username:   "{{ vc_username }}"
        password:   "{{ vc_password }}"
        esxi_hostname: "{{ item }}"
        service_name: TSM-SSH
        state: stopped
        validate_certs: false
      loop: "{{ host_facts.hosts_facts.keys() | list }}"
      register: ssh_result
      failed_when: false

    - name: Assert compliance summary
      ansible.builtin.assert:
        that:
          - host_facts.hosts_facts | length > 0
        fail_msg: "No hosts found in cluster {{ cluster_name }}"
        success_msg: "Compliance check complete for {{ host_facts.hosts_facts | length }} hosts"
~~~
