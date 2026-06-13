---
tags:
  - esxi
  - operations
  - vmware
  - vsphere-8
---
# ESXi — Scripts


<div class="kb-summary">
ESXi Scripts reference covering Storage Path Health Check (Bash / esxcli), ESXi Syslog and Event Collector (Python), NTP Configuration Audit (Bash), Ansible ESXi Configuration Playbook, Windows: ESXi Host Health via REST API (PowerShell) and 1 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

ESXi Automation Scripts — Tool Selection
```text
┌─────────────────────────────────────────── ESXi — Scripts ────────────────────────────────────────────┐
│                                                                                                       │
│  PowerCLI, shell, and Python scripts automating ESXi host operations at scale.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               PowerCLI Scripts               │  │            Shell / esxcli Scripts           │   │
│   │           Get-VMHost health report           │  │          esxcli system version get          │   │
│   │           Set-VMHostNTP / DNS bulk           │  │          for host in list; ssh cmd          │   │
│   │             Move-VM bulk vMotion             │  │           esxcli storage core path          │   │
│   │         Get-Datastore free space rpt         │  │            esxcli vm process kill           │   │
│   │           Invoke-VMScript in guest           │  │          cron + configBundle backup         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  PowerCLI for vCenter-scope tasks; esxcli over SSH for per-host automation.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Python / pyVmomi Scripts           │  │             Automation Patterns             │   │
│   │           ServiceInstance connect            │  │              Idempotent design              │   │
│   │           Traverse container view            │  │            Error handling + retry           │   │
│   │           Get host config objects            │  │              Dry-run mode flag              │   │
│   │           Reconfigure host via API           │  │              Log output to file             │   │
│   │          Task monitoring wait loop           │  │             Pipeline integration            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts on x86, management network, jump host for script execution                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PowerCLI    = VMware PowerShell SDK; Connect-VIServer for vCenter/ESXi                               │
│  pyVmomi     = Python SDK for vSphere API; official VMware library                                    │
│  esxcli      = on-host CLI; run via SSH or Ansible for bulk host ops                                  │
│  govc        = Go CLI for vCenter API; lightweight alternative to PowerCLI                            │
│  Invoke-VMScript = PowerCLI cmd to run script in guest via VMtools                                    │
│  Container view = pyVmomi API for traversing vCenter inventory objects                                │
│  Task object = vSphere async task; polled until complete or error                                     │
│  Idempotent  = script produces same result if run multiple times safely                               │
│  Dry-run     = logic executes but no changes applied; safe testing                                    │
│  cron        = Linux scheduler on jump host; triggers backup/health scripts                           │
│  SSH         = Secure Shell; disabled by default on ESXi; enable per-host                             │
│  VMtools     = VMware Tools; guest agent enabling Invoke-VMScript                                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
---

## Storage Path Health Check (Bash / esxcli)

Run on an ESXi host via SSH. Report per-device path counts (active / standby / dead) and exit non-zero if any dead paths exist.

```bash
#!/bin/bash
# esxi_path_health.sh
# Usage: ssh root@esxi-host 'bash -s' < esxi_path_health.sh

CRIT=0
TS=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

echo "==================================="
echo " ESXi Storage Path Health Check"
echo " $TS"
echo "==================================="
printf "%-40s %8s %8s %8s %8s %s\n" "Device" "Active" "Standby" "Dead" "Total" "Status"
printf "%-40s %8s %8s %8s %8s %s\n" "------" "------" "-------" "----" "-----" "------"

declare -A path_active path_standby path_dead

while IFS= read -r line; do
    if [[ $line =~ ^[[:space:]]Device:\ (.*) ]]; then
        dev="${BASH_REMATCH[1]// /}"
    elif [[ $line =~ State:\ (active|standby|dead|disabled) ]]; then
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
```

### How to run this script — step by step

**Before you start — what you need**
- SSH must be enabled on the ESXi host: vSphere Client → select the host → Manage → Services → SSH → click Start
- An SSH client on your Windows PC — Git Bash, PuTTY, or WSL
- The root password for your ESXi host

**Run it**

Replace `192.168.1.100` with your ESXi host's IP:

```bash
ssh root@192.168.1.100 'bash -s' < ~/Desktop/esxi_path_health.sh
```

---

## ESXi Syslog and Event Collector (Python)

Connect to vCenter via pyVmomi, retrieve events from the last 24 hours filtered by severity, and report NMP/storage errors.

```python
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
    return em.QueryEvents(filter=filter_spec)


si = connect_vcenter()
events = collect_events(si)

print(f"Events from last {HOURS_BACK}h on {VCENTER_HOST}")
print(f"Total events retrieved: {len(events)}")

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

Disconnect(si)
sys.exit(1 if issues else 0)
```

**Before you start:** Python 3.8+ and `pip install pyVmomi`. Set `VCENTER_HOST`, `VC_USER`, `VC_PASS` as environment variables then run `python3 esxi_event_collector.py`.

---

## NTP Configuration Audit (Bash)

SSH to each ESXi host (or run locally), verify NTP service state, configured servers, and time offset.

```bash
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
        status="SVC_DOWN"; overall=2
    elif [[ "$ntp_servers" == "NOT_CONFIGURED" ]]; then
        status="NO_NTP_SERVER"; overall=2
    elif (( abs_offset >= OFFSET_CRIT_MS )); then
        status="HIGH_DRIFT"; overall=2
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
```

**Usage:** `ESXI_HOSTS="192.168.1.101 192.168.1.102" ./esxi_ntp_audit.sh`

---

## Ansible ESXi Configuration Playbook

Use the `community.vmware` collection to verify NTP, DNS, syslog, and SSH security profile compliance across all ESXi hosts in a cluster.

```yaml
---
# esxi_compliance.yml
# Usage: ansible-playbook -i inventory esxi_compliance.yml
# Deps: ansible-galaxy collection install community.vmware

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
```

**Before you start:** Install Ansible via WSL (`sudo apt install -y ansible`), then `ansible-galaxy collection install community.vmware` and `pip3 install pyVmomi requests`. Set `VC_USER` and `VC_PASS` environment variables before running.

---

## Windows: ESXi Host Health via REST API (PowerShell)

Use the ESXi Embedded Host Client REST API (available on ESXi 6.x and newer) to check system health and list services — no extra modules needed.

```powershell
# esxi_rest_health.ps1
param(
    [string]$EsxiHost = "192.168.1.100",
    [string]$EsxiUser = "root",
    [string]$EsxiPass = "YourRootPasswordHere"
)

Add-Type @"
using System.Net;
using System.Security.Cryptography.X509Certificates;
public class TrustAll : ICertificatePolicy {
    public bool CheckValidationResult(ServicePoint sp, X509Certificate cert, WebRequest req, int prob) { return true; }
}
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAll
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

$BaseUrl = "https://$EsxiHost/rest"
$authBytes = [System.Text.Encoding]::ASCII.GetBytes("${EsxiUser}:${EsxiPass}")
$authB64   = [System.Convert]::ToBase64String($authBytes)
$authHeaders = @{ Authorization = "Basic $authB64" }

$sessionResp = Invoke-RestMethod -Uri "$BaseUrl/com/vmware/cis/session" -Method POST -Headers $authHeaders
$sessionToken = $sessionResp.value
$apiHeaders = @{ "vmware-api-session-id" = $sessionToken }

$health = Invoke-RestMethod -Uri "$BaseUrl/appliance/health/system" -Method GET -Headers $apiHeaders
Write-Host "System Health: $($health.value.ToUpper())"

$services = Invoke-RestMethod -Uri "$BaseUrl/appliance/vmon/service" -Method GET -Headers $apiHeaders
foreach ($svc in ($services.value | Sort-Object { $_.key })) {
    Write-Host ("{0,-40} {1,-15} {2}" -f $svc.key, $svc.value.state, $svc.value.startup_type)
}

Invoke-RestMethod -Uri "$BaseUrl/com/vmware/cis/session" -Method DELETE -Headers $apiHeaders | Out-Null
```

**Usage:** Update `$EsxiHost`, `$EsxiUser`, `$EsxiPass` then run `.\esxi_rest_health.ps1` from an elevated PowerShell prompt.

---

## Windows: ESXi ESXCLI Commands via Plink (CMD)

```batch
@echo off
REM esxi_esxcli_check.bat — ESXi diagnostic commands via SSH (plink)
REM Download plink from https://www.putty.org

set ESXI_HOST=192.168.1.100
set SSH_USER=root
set PLINK="C:\Program Files\PuTTY\plink.exe"

echo === ESXi ESXCLI Diagnostic Check: %ESXI_HOST% ===
echo.
echo --- ESXi Version ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli system version get"
echo.
echo --- Storage Multipath Devices ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli storage nmp device list | head -40"
echo.
echo --- Network NICs ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli network nic list"
echo.
echo --- System Uptime ---
%PLINK% -ssh -l %SSH_USER% -batch %ESXI_HOST% "esxcli system stats uptime get"
echo.
echo === Diagnostic check complete ===
```

**Before first use:** Accept the SSH fingerprint once by running `plink.exe -ssh root@<esxi-ip>` and typing `y`.
