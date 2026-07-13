---
tags:
  - troubleshooting
  - vcf
  - vmware
search:
  boost: 1.5
description: "VMware Cloud Foundation diagnostic commands: check SDDC Manager services and health API, grep LCM upgrade logs for failures, diagnose NSX Manager cluster..."
---
# VCF — Diagnostics

<div class="kb-summary">
VMware Cloud Foundation diagnostic commands: check SDDC Manager services and health API, grep LCM upgrade logs for failures, diagnose NSX Manager cluster and transport nodes, collect the vc-support vCenter bundle, run the SOS utility for a full cross-component log bundle, and query the VCF health summary REST API.

*Applies to: VCF 4.x / 5.x*
</div>
![VCF — Diagnostics](../../../../../assets/virtualization-vmware-vmware-cloud-foundation-troubleshootin.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "systemctl status vmware-vcf-operationsmanager\ntail operationsmanager.log" {shape: rectangle}
D: "grep precheck lcm-debug.log\nGET /v1/tasks?status=FAILED" {shape: rectangle}
E: "NSX CLI: get cluster status\nget transport-nodes status" {shape: rectangle}
F: "vCenter: service-control --status --all\ntail vpxd.log" {shape: rectangle}
G: "PowerCLI: VsanQueryVcClusterHealthSummary\nesxcli vsan debug on ESXi" {shape: rectangle}
H: "GET /v1/system/health-summary\nsudo sos --health-check" {shape: rectangle}
I: "I" {shape: rectangle}
J: "systemctl restart vmware-vcf-operationsmanager\nCheck disk: df -h on SDDC Manager" {shape: rectangle}
K: "GET /v1/tasks?status=IN_PROGRESS for stuck task IDs\ngrep task-uuid operationsmanager.log" {shape: rectangle}
L: "L" {shape: rectangle}
M: "curl -v https://depot.vmware.com to test depot\nconnectivity\nCheck proxy: domain-manager.properties" {shape: rectangle}
N: "grep precheck FAIL lcm-debug.log for check name\nRemediate flagged item and retry" {shape: rectangle}
O: "grep UPGRADE_STAGE lcm-debug.log\nCheck last stage entry for timeout" {shape: rectangle}
P: "ESXi: vmkping -I vmk10 -d -s 1572 remote-tep-ip for MTU\nNSX: get bgp neighbor summary on Edge" {shape: rectangle}
Q: "service-control --restart vpxd if vpxd stopped\nCheck /storage partitions: df -h" {shape: rectangle}
R: "Get-VsanDiskGroup to check disk group state\nesxcli vsan debug object list on ESXi host" {shape: rectangle}
S: "Collect SOS bundle\nsudo sos --collect-all-logs" {shape: rectangle}
T: "Open VMware SR\nUpload SOS bundle + component logs" {shape: rectangle}
A: "VCF Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> K
L -> M
L -> N
L -> O
E -> P
F -> Q
G -> R
H -> S
J -> S
K -> S
M -> S
N -> S
O -> S
P -> S
Q -> S
R -> S
S -> T
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_sddc_manager_services_a: "Step 1 — Check SDDC Manager services and health" {shape: rectangle}
step_2_analyze_lcm_lifecycle_and_upg: "Step 2 — Analyze LCM lifecycle and upgrade logs" {shape: rectangle}
step_3_diagnose_nsx_manager_cluster_: "Step 3 — Diagnose NSX Manager cluster and\ntransport nodes" {shape: rectangle}
step_4_check_vcenter_appliance: "Step 4 — Check vCenter appliance" {shape: rectangle}
step_5_query_sddc_manager_health_api: "Step 5 — Query SDDC Manager health API" {shape: rectangle}
step_6_collect_sos_diagnostic_bundle: "Step 6 — Collect SOS diagnostic bundle" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_sddc_manager_services_a: investigate
symptom -> step_2_analyze_lcm_lifecycle_and_upg: investigate
symptom -> step_3_diagnose_nsx_manager_cluster_: investigate
symptom -> step_4_check_vcenter_appliance: investigate
symptom -> step_5_query_sddc_manager_health_api: investigate
symptom -> step_6_collect_sos_diagnostic_bundle: investigate
step_1_check_sddc_manager_services_a -> resolution
step_2_analyze_lcm_lifecycle_and_upg -> resolution
step_3_diagnose_nsx_manager_cluster_ -> resolution
step_4_check_vcenter_appliance -> resolution
step_5_query_sddc_manager_health_api -> resolution
step_6_collect_sos_diagnostic_bundle -> resolution
```

## Before you begin

- **Access:** SSH to SDDC Manager (vcf user, then sudo for SOS); SSH to VCSA, NSX Manager, and ESXi hosts as needed; SDDC Manager admin credentials for the REST API
- **Gather first:** the specific symptom (LCM task failed, SDDC Manager unreachable, NSX transport node disconnected, vSAN health alarm), the affected domain name and task ID if visible, and when the issue started
- **Scope:** confirm whether the issue is in the management domain or a workload domain, and which component (SDDC Manager, LCM, NSX, vCenter, vSAN) shows the first error

---

## Step 1 — Check SDDC Manager services and health

```bash
# SSH to SDDC Manager
ssh vcf@sddc-manager.corp.example.com

# All VCF service statuses
systemctl list-units 'vmware-vcf-*' --no-pager
# Expected: all services active (running)

# Key services
systemctl status vmware-vcf-operationsmanager   # Core SDDC Manager
systemctl status vmware-vcf-lcm                 # Lifecycle Manager
systemctl status vmware-vcf-domainmanager       # Domain Manager
systemctl status vmware-vcf-commonsvcs          # Common Services (auth)

# Tail the main SDDC Manager log
sudo tail -100 /var/log/vmware/vcf/operationsmanager/operationsmanager.log | grep -i "error\|fail\|exception"

# Restart a specific service if stopped
sudo systemctl restart vmware-vcf-lcm
```


```text title="Expected output"
● vmware-vcf-operationsmanager.service        loaded active running   VMware VCF Operations Manager
● vmware-vcf-lcm.service                      loaded active running   VMware VCF Lifecycle Manager
● vmware-vcf-domainmanager.service            loaded active running   VMware VCF Domain Manager
● vmware-vcf-commonsvcs.service               loaded active running   VMware VCF Common Services
● vmware-vcf-restapi.service                  loaded active running   VMware VCF REST API
● vmware-vcf-inventory.service                loaded active running   VMware VCF Inventory Service

● vmware-vcf-operationsmanager.service - VMware VCF Operations Manager
     Loaded: loaded (/etc/systemd/system/vmware-vcf-operationsmanager.service; enabled; vendor preset: disabled)
     Active: active (running) since Wed 2024-01-17 14:32:18 UTC; 2 days ago
   Main PID: 8472 (java)
      Tasks: 47
     Memory: 2.1G
     CGroup: /systemd/system.slice/vmware-vcf-operationsmanager.service

2024-01-19 09:15:42 sddc-manager systemd[1]: Started VMware VCF Lifecycle Manager.
2024-01-19 09:15:43 sddc-manager systemd[1]: Started VMware VCF Domain Manager.
2024-01-19 09:15:44 sddc-manager systemd[1]: Started VMware VCF Common Services.

(no output — tail command returns silently when no errors found)

(no output — restart command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unit vmware-vcf-lcm.service not found.` | Verify the VCF version is installed correctly and the service name matches your deployment with `systemctl list-units 'vmware-vcf-*'`. |
    | `Failed to restart vmware-vcf-lcm.service: Access denied` | Ensure you are running the command with `sudo` or as root user. |
    | `Connection refused` (when SSH'ing to sddc-manager)` | Verify the SDDC Manager hostname resolves correctly and SSH is enabled; check network connectivity with `ping sddc-manager.corp.example.com`. |
---

## Step 2 — Analyze LCM lifecycle and upgrade logs

`lcm-debug.log` is the primary log for all upgrade, patch, and bundle operations.

```bash
# Find precheck failures (most common first stop)
grep -i 'precheck.*FAIL\|compliance.*FAIL' \
  /var/log/vmware/vcf/lcm/lcm-debug.log | tail -50

# Find bundle download failures
grep -i 'download.*fail\|bundle.*error\|depot.*unreachable' \
  /var/log/vmware/vcf/lcm/lcm-debug.log

# Find upgrade stage progression (see which stage is stuck)
grep -i 'UPGRADE_STAGE\|stage.*complete\|stage.*failed' \
  /var/log/vmware/vcf/lcm/lcm-debug.log | tail -50

# Find a specific task by its UUID
grep "taskId=<task-uuid>" /var/log/vmware/vcf/lcm/lcm-debug.log

# Count errors per hour (useful for rate-of-failure analysis)
grep 'ERROR' /var/log/vmware/vcf/lcm/lcm-debug.log | \
  awk '{print $1, $2}' | cut -c1-13 | sort | uniq -c

# Test depot connectivity (for bundle download failures)
curl -v --max-time 30 https://depot.vmware.com/PROD2/evo/vmw/ 2>&1 | grep -E 'HTTP|Connected|SSL'

# Check proxy settings if depot is unreachable
cat /etc/vmware/vcf/domainmanager/domain-manager.properties | grep -i proxy
```


```text title="Expected output"
2024-01-15T09:23:45.123Z [PRECHECK] vSAN Cluster Precheck FAILED: Insufficient free space on host esx-01.lab.local
2024-01-15T09:24:12.456Z [PRECHECK] Network Connectivity Precheck FAILED: Cannot reach vCenter at 192.168.1.50
2024-01-15T09:25:33.789Z [COMPLIANCE] Compliance Check FAILED: ESXi build 20.1.0-18313628 does not meet minimum 20.1.0-18500000
2024-01-15T09:26:01.234Z [PRECHECK] Storage Precheck FAILED: vSAN object resync in progress (87% complete)

2024-01-15T10:15:44.567Z [BUNDLE] Download FAILED: depot.vmware.com connection timeout after 120s
2024-01-15T10:16:22.890Z [DEPOT] Bundle vmw-vcf-2024.01-bundle-12345.tar.gz unreachable: HTTP 503 Service Unavailable

2024-01-15T11:02:15.123Z [UPGRADE_STAGE] UPGRADE_STAGE=PRECHECK_VALIDATION stage complete
2024-01-15T11:03:44.456Z [UPGRADE_STAGE] UPGRADE_STAGE=BUNDLE_DOWNLOAD stage failed at 45% (taskId=a7f2c8d1-9e3b-4c2a-b1f5-6d8e9a0c1b2f)
2024-01-15T11:04:12.789Z [UPGRADE_STAGE] UPGRADE_STAGE=VCENTER_UPGRADE stage complete
2024-01-15T11:05:33.012Z [UPGRADE_STAGE] UPGRADE_STAGE=ESXI_UPGRADE stage in progress (3 of 8 hosts complete)

* Connected to depot.vmware.com (203.0.113.45) port 443 (#0)
* SSL connection using TLSv1.3 / ECDHE-RSA-AES256-GCM-SHA384
< HTTP/1.1 200 OK
< Content-Type: application/json

proxy.host=proxy.lab.local
proxy.port=8080
proxy.username=vcf_svc
proxy.protocol=http
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /var/log/vmware/vcf/lcm/lcm-debug.log: No such file or directory` | Verify the LCM service is running with `systemctl status vmware-vcf-lcm` and check the correct log path with `find /var/log -name "*lcm*" -type f`. |
    | `curl: (7) Failed to connect to depot.vmware.com port 443: Connection timed out` | Verify network connectivity and proxy settings with `curl -v --proxy [proxy:port] https://depot.vmware.com` or check firewall rules blocking outbound HTTPS. |
    | `taskId=<task-uuid>: No such file or directory` | Replace the literal `<task-uuid>` placeholder with an actual UUID from a previous grep output, e.g., `grep "taskId=a7f2c |
---

## Step 3 — Diagnose NSX Manager cluster and transport nodes

```bash
# SSH to NSX Manager
ssh admin@nsx-manager.corp.example.com

# Overall cluster health
get cluster status
# Expected: all 3 nodes STABLE

# Transport node summary
get transport-nodes status
# Expected: all nodes CONNECTED

# Logical router overview
get logical-routers

# BGP peer status on a gateway node
get logical-router <uuid> bgp neighbor summary

# Via REST API — degraded transport nodes
NSX="nsx-manager.corp.example.com"
AUTH="admin:NSXAdminPassword"

curl -sk -u "$AUTH" "https://$NSX/api/v1/transport-nodes/status-summary" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"Up={d.get('up_count','?')} Degraded={d.get('degraded_count','?')} Down={d.get('down_count','?')}\")"

# Find any transport node NOT in success state
curl -sk -u "$AUTH" "https://$NSX/api/v1/transport-nodes/status" | \
  python3 -c "
import json,sys
for tn in json.load(sys.stdin).get('results',[]):
    if tn.get('node_deployment_state',{}).get('state','') != 'success':
        print(f\"{tn.get('display_name','?')}: {tn.get('node_deployment_state',{}).get('state','?')}\")
"

# TEP MTU verification (from ESXi host)
vmkping -I vmk10 -d -s 1572 <remote-tep-ip>
# -d = DF bit; -s 1572 payload + 28 bytes header = 1600 total; must not fragment
```


```text title="Expected output"
admin@nsx-manager.corp.example.com's password: 
cluster status: STABLE (3/3 nodes online)
  Node: nsx-mgr-01.corp.example.com — STABLE
  Node: nsx-mgr-02.corp.example.com — STABLE
  Node: nsx-mgr-03.corp.example.com — STABLE

transport-nodes status:
  tn-esx01.corp.example.com — CONNECTED
  tn-esx02.corp.example.com — CONNECTED
  tn-esx03.corp.example.com — CONNECTED

logical-routers:
  UUID: 7a4c2e91-b3f8-4d6a-9e1c-5f8a2b3d4e5f — Name: tier0-gateway-01 — Type: TIER0
  UUID: 8b5d3f92-c4g9-5e7b-af2d-6g9b3c4e5f6g — Name: tier1-tenant-prod — Type: TIER1

Up=3 Degraded=0 Down=0

tn-esx01.corp.example.com: success
tn-esx02.corp.example.com: success
tn-esx03.corp.example.com: success

PING 192.168.100.45 (192.168.100.45): 1572 data bytes
1580 bytes from 192.168.100.45: icmp_seq=0 time=2.341 ms
1580 bytes from 192.168.100.45: icmp_seq=1 time=2.156 ms
1580 bytes from 192.168.100.45: icmp_seq=2 time=2.289 ms
--- 192.168.100.45 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip SSL verification (already present in example; verify NSX certificate is valid if this persists). |
    | `node_deployment_state: FAILED` | SSH to the affected transport node and check `/var/log/nsx-agent.log` for deployment errors, then re-run the NSX controller deployment task. |
    | `PING: sendto: No route to host` | Verify the TEP (Tunnel Endpoint) IP is reachable and that vmk10 is bound to the correct VLAN/segment on the ESXi host using `esxcli network ip interface list`. |
---

## Step 4 — Check vCenter appliance

```bash
# SSH to vCenter Appliance as root
ssh root@vcenter.corp.example.com

# Check all vCenter services
service-control --status --all | grep -v RUNNING
# Expected: no output (all services running)

# Tail vpxd log for task and API errors
tail -100 /var/log/vmware/vpxd/vpxd.log | grep -i "error\|fatal"

# Disk space (full /storage/db causes cascading failures)
df -h | grep storage

# Generate vCenter support bundle
/usr/lib/vmware-vpx/scripts/vc-support.sh -p
ls -lh /var/tmp/vc-*.tgz
scp root@vcenter.corp.example.com:/var/tmp/vc-<date>-<id>.tgz /local/path/

# vCenter API health check
VCSA="vcenter.corp.example.com"
SESSION=$(curl -sk -u "administrator@vsphere.local:<pass>" \
  -X POST "https://$VCSA/rest/com/vmware/cis/session" | tr -d '"')
curl -sk -H "vmware-api-session-id: $SESSION" \
  "https://$VCSA/rest/appliance/health/system" | python3 -m json.tool
```


```text title="Expected output"
Connected to vcenter.corp.example.com.
root@vcenter [ ~ ]# service-control --status --all | grep -v RUNNING
root@vcenter [ ~ ]# tail -100 /var/log/vmware/vpxd/vpxd.log | grep -i "error\|fatal"
2024-01-15T09:42:18.123Z [7F2A4C1E] [error] [vpxd] Task failed: vm-1234 snapshot consolidation timeout
2024-01-15T09:51:03.456Z [7F2A4C2F] [warn] [vpxd] API session limit approaching (487/500)
root@vcenter [ ~ ]# df -h | grep storage
/dev/mapper/storage_vg-storage_lv  500G  412G   88G  83% /storage
root@vcenter [ ~ ]# /usr/lib/vmware-vpx/scripts/vc-support.sh -p
Generating support bundle...
Support bundle generated: /var/tmp/vc-20240115-a7f3e9c2.tgz (2.3G)
root@vcenter [ ~ ]# ls -lh /var/tmp/vc-*.tgz
-rw-r--r-- 1 root root 2.3G Jan 15 09:55 /var/tmp/vc-20240115-a7f3e9c2.tgz
root@vcenter [ ~ ]# scp root@vcenter.corp.example.com:/var/tmp/vc-20240115-a7f3e9c2.tgz /local/path/
vc-20240115-a7f3e9c2.tgz                                    100% 2.3GB   45.2MB/s   00:51
root@vcenter [ ~ ]# SESSION=$(curl -sk -u "administrator@vsphere.local:<pass>" \
  -X POST "https://vcenter.corp.example.com/rest/com/vmware/cis/session" | tr -d '"')
root@vcenter [ ~ ]# curl -sk -H "vmware-api-session-id: $SESSION" \
  "https://vcenter.corp.example.com/rest/appliance/health/system" | python3 -m json.tool
{
  "value": "green",
  "messages": []
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to vcenter.corp.example.com port 443: Connection refused` | Verify vCenter API service is running with `service-control --status --all | grep -i api` and restart if needed with `service-control --start --all`. |
    | `Authentication failed for user 'administrator@vsphere.local'` | Confirm the password is correct and the SSO service is operational; check `/var/log/vmware/sso/sso-event.log` for lockouts. |
    | `/storage filesystem is 95% full` | Immediately increase `/storage` LVM volume or delete old logs/snapshots; full `/storage/db` will cause vCenter to become unresponsive. |
---

## Step 5 — Query SDDC Manager health API

```bash
# Authenticate to SDDC Manager REST API
TOKEN=$(curl -sk -X POST https://sddc-manager.corp.example.com/v1/tokens \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"AdminPassword"}' | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['accessToken'])")

SDDC="sddc-manager.corp.example.com"

# Overall health summary (all components in one call)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://$SDDC/v1/system/health-summary" | python3 -m json.tool

# Domain health (all workload domains)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://$SDDC/v1/domains" | \
  python3 -c "
import json,sys
for d in json.load(sys.stdin).get('elements',[]):
    print(f\"{d['name']}: {d['status']} ({d['type']})\")
"

# Host health (all managed hosts)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://$SDDC/v1/hosts" | \
  python3 -c "
import json,sys
for h in json.load(sys.stdin).get('elements',[]):
    if h.get('status') != 'ASSIGNED':
        print(f\"PROBLEM: {h['fqdn']}: {h.get('status','?')}\")
"

# Active tasks (for stuck tasks)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://$SDDC/v1/tasks?status=IN_PROGRESS" | \
  python3 -c "
import json,sys
for t in json.load(sys.stdin).get('elements',[]):
    print(f\"{t['id']}: {t['name']} ({t['status']}) created={t.get('creationTimestamp','?')}\")
"

# Credentials not in ACTIVE state (rotation failures)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://$SDDC/v1/credentials" | \
  python3 -c "
import json,sys
for c in json.load(sys.stdin).get('elements',[]):
    if c.get('credentialStatus') != 'ACTIVE':
        print(f\"{c['resourceName']} {c['accountName']}: {c.get('credentialStatus','?')}\")
"
```


```text title="Expected output"
{
  "status": "HEALTHY",
  "timestamp": "2024-01-15T09:42:33.521Z",
  "componentHealthSummary": {
    "SDDC_MANAGER": "HEALTHY",
    "VCENTER": "HEALTHY",
    "NSX_MANAGER": "HEALTHY",
    "VSAN": "HEALTHY",
    "HOSTS": "HEALTHY"
  }
}
management: HEALTHY (MANAGEMENT)
workload-domain-1: HEALTHY (WORKLOAD)
workload-domain-2: HEALTHY (WORKLOAD)
PROBLEM: esx-host-07.corp.example.com: UNASSIGNED
PROBLEM: esx-host-12.corp.example.com: MAINTENANCE_MODE
6f8a2c1d-9e4b-11ee-a8c3-005056a1b2c3: Configure NSX Cluster (IN_PROGRESS) created=2024-01-15T09:15:22.000Z
8b3f4e2a-9e4b-11ee-a8c3-005056a1b2c4: vSAN Rebalance (IN_PROGRESS) created=2024-01-15T08:47:11.000Z
SDDC_MANAGER sso-admin: EXPIRED
VCENTER vcenter-admin: ROTATION_FAILED
NSX_MANAGER nsx-admin: ACTIVE
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command (already present; if still failing, verify SDDC Manager hostname resolves correctly). |
    | `jq: command not found` or `python3: command not found` | Install python3 package on SDDC Manager or use `jq` instead of python3 for JSON parsing. |
    | `{"error":"Invalid token","status":401}` | Verify admin credentials are correct and account is not locked; re-run token generation command. |
---

## Step 6 — Collect SOS diagnostic bundle

```bash
# SSH to SDDC Manager and collect comprehensive log bundle
ssh vcf@sddc-manager.corp.example.com
sudo su -

# Full log collection (takes 20-40 minutes depending on cluster size)
/usr/lib/vmware-sddc-support/sos --collect-all-logs
# Output: /var/log/vmware/vcf/sddc-support/

# Health check only (faster — 5-10 minutes)
/usr/lib/vmware-sddc-support/sos --health-check

# Connectivity check only
/usr/lib/vmware-sddc-support/sos --connectivity-check

# List generated bundles
ls -lh /var/log/vmware/vcf/sddc-support/

# SCP the bundle to a transfer host
scp vcf@sddc-manager.corp.example.com:/var/log/vmware/vcf/sddc-support/<bundle>.zip ./
```


```text title="Expected output"
sddc-manager.corp.example.com
Last login: Wed Jan 15 14:32:18 2025 from 10.45.120.88
root@sddc-manager:~# /usr/lib/vmware-sddc-support/sos --collect-all-logs
Starting comprehensive log collection...
Collecting SDDC Manager logs...
Collecting vCenter logs...
Collecting NSX Manager logs...
Collecting vSAN logs...
Collecting ESXi host logs...
Log collection completed successfully.
Bundle saved to: /var/log/vmware/vcf/sddc-support/sddc-support-2025-01-15-143245.zip
Total size: 2.3 GB

root@sddc-manager:~# /usr/lib/vmware-sddc-support/sos --health-check
Running health check...
SDDC Manager: HEALTHY
vCenter: HEALTHY
NSX Manager: HEALTHY
vSAN: HEALTHY
All components operational.

root@sddc-manager:~# /usr/lib/vmware-sddc-support/sos --connectivity-check
Checking connectivity...
SDDC Manager ↔ vCenter: OK
SDDC Manager ↔ NSX Manager: OK
SDDC Manager ↔ ESXi hosts: OK (8/8 reachable)
All connectivity checks passed.

root@sddc-manager:~# ls -lh /var/log/vmware/vcf/sddc-support/
total 4.8G
-rw-r--r-- 1 root root 2.3G Jan 15 14:52 sddc-support-2025-01-15-143245.zip
-rw-r--r-- 1 root root 1.2G Jan 14 09:18 sddc-support-2025-01-14-091832.zip
-rw-r--r-- 1 root root 1.3G Jan 13 16:45 sddc-support-2025-01-13-164512.zip
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,password).` | Verify SSH key is loaded or use password authentication; confirm vcf user exists on SDDC Manager with `id vcf`. |
    | `/usr/lib/vmware-sddc-support/sos: command not found` | Ensure you are running as root with `sudo su -` and that VMware Cloud Foundation support tools are installed with `rpm -qa | grep vmware-sddc-support`. |
    | `No space left on device` | Free up disk space on SDDC Manager with `df -h` to identify full partitions, or move existing bundles to external storage before re-running collection. |
---

## Step 7 — VCF error code reference

| Error Code | Component | Meaning | Resolution |
|---|---|---|---|
| `LCM-3004` | LCM | Bundle download failed | Verify depot connectivity; check proxy settings |
| `LCM-3011` | LCM | Precheck failed — compliance | Run compliance check; remediate flagged items |
| `LCM-3015` | LCM | Upgrade vCenter — VAMI unreachable | Check VCSA VAMI service; restart if needed |
| `LCM-3020` | LCM | Host not in maintenance mode | Put host in maintenance or retry |
| `LCM-6003` | LCM | vSAN disk decommission timeout | Check vSAN resync progress; extend timeout |
| `NSX-2001` | NSX | Transport node config push failed | Check NSX agent on ESXi: `esxcli software vib list | grep nsx` |
| `NSX-4001` | NSX | BGP session down | Verify BGP config and upstream router reachability |
| `VSAN-0x00140029` | vSAN | Object degraded or absent | Check disk group health; look for disk failures |
| `VPXD-3016` | vCenter | HA configuration failed | Check HA cluster settings; verify storage connectivity |
| `CRED-1010` | SDDC Mgr | Credential rotation failed | Check account lockout; verify credential in SDDC Mgr vault |
| `DEPOT-001` | SDDC Mgr | Cannot reach online depot | Check DNS, proxy, firewall for depot.vmware.com |

---

## Log locations

| Component | Path / Command | What to look for |
|---|---|---|
| SDDC Manager | `/var/log/vmware/vcf/operationsmanager/operationsmanager.log` | Task and API errors |
| LCM | `/var/log/vmware/vcf/lcm/lcm-debug.log` | Precheck FAIL, upgrade stage errors |
| Domain Manager | `/var/log/vmware/vcf/domainmanager/domain-manager.log` | Domain expansion and host operations |
| vCenter | `/var/log/vmware/vpxd/vpxd.log` (on VCSA) | Task, event, and API errors |
| NSX Manager | `get log-file nsx-manager` (NSX CLI) | Control plane and cluster errors |
| Full bundle | `sudo sos --collect-all-logs` | All-in-one — required for VMware SR |

---

## See also

- [VCF Troubleshooting — Common Issues](../common-issues/)
- [VCF Troubleshooting — Escalation](../escalation/)

## Verify resolution

- `systemctl list-units vmware-vcf-*` shows all services active (running) on SDDC Manager
- `GET /v1/system/health-summary` returns all components in GREEN or HEALTHY state
- `GET /v1/tasks?status=IN_PROGRESS` returns an empty task list (no stuck tasks)
- LCM lifecycle operation completes: check `GET /v1/tasks/<task-id>` returns `status=SUCCESSFUL`
- NSX: `get cluster status` returns all Manager nodes STABLE; `get transport-nodes status` shows all CONNECTED
