---
tags:
  - troubleshooting
  - vmware
  - vsphere-replication
search:
  boost: 1.5
description: "vSphere Replication (VR) diagnostic commands: check VRA service status with systemctl, inspect HMS and VRMS logs, test replication port 31031 from the..."
---
# vSphere Replication — Diagnostics

<div class="kb-summary">
vSphere Replication (VR) diagnostic commands: check VRA service status with systemctl, inspect HMS and VRMS logs, test replication port 31031 from the source ESXi host, verify hbrsvc on the source host, check the REST API health endpoint, capture replication traffic with pktcap-uw, and collect the VAMI support bundle for VMware SRs.

*Applies to: vSphere Replication 8.x*
</div>
![vSphere Replication — Diagnostics](../../../../../assets/virtualization-vmware-vsphere-replication-troubleshooting-di.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "systemctl status hms vrms nginx\njournalctl -u hms -n 100" {shape: rectangle}
D: "nc -zv target-VRA 31031 from source ESXi\nCheck hbrsvc on source ESXi" {shape: rectangle}
E: "vCenter → Monitor → Recent Tasks\nFilter for HBR or vSphere Replication" {shape: rectangle}
F: "openssl s_client -connect VRA:443\nCheck notAfter date" {shape: rectangle}
G: "Check hbr.log on source ESXi\nRead per-VM replication error" {shape: rectangle}
H: "Test TCP 443 to vCenter from VRA\nnc -zv vcenter-ip 443" {shape: rectangle}
I: "I" {shape: rectangle}
J: "systemctl start hms\nCheck disk: df -h /" {shape: rectangle}
K: "systemctl start vrms\njournalctl -u vrms -n 50 for error" {shape: rectangle}
L: "L" {shape: rectangle}
M: "Check firewall rules between sites\nVerify target VRA IP and routing" {shape: rectangle}
N: "Check hbr.log for bandwidth or timeout errors\nCheck VMkernel adapter used for replication" {shape: rectangle}
O: "Cancel stuck task if > 30 min\nvCenter → Recent Tasks → right-click Cancel" {shape: rectangle}
P: "Check cert via VAMI\nhttps://VRA:5480 → Certificate → Renew" {shape: rectangle}
Q: "tail /var/log/hbr.log | grep -i error\nCompare replication timestamps" {shape: rectangle}
R: "Check DNS resolution of vCenter from VRA\nnslookup vcenter-fqdn" {shape: rectangle}
S: "Collect VRA VAMI support bundle\nhttps://VRA:5480 → Support → Generate" {shape: rectangle}
T: "Open VMware SR\nAttach bundle and replication task ID" {shape: rectangle}
A: "vSphere Replication Issue" {shape: rectangle}

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
E -> O
F -> P
G -> Q
H -> R
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
step_1_check_vra_service_status: "Step 1 — Check VRA service status" {shape: rectangle}
step_2_check_vra_rest_api_health: "Step 2 — Check VRA REST API health" {shape: rectangle}
step_3_read_vra_logs: "Step 3 — Read VRA logs" {shape: rectangle}
step_4_test_connectivity_from_source: "Step 4 — Test connectivity from source ESXi to\ntarget VRA" {shape: rectangle}
step_5_check_hbrsvc_on_source_esxi: "Step 5 — Check hbrsvc on source ESXi" {shape: rectangle}
step_6_verify_vra_certificate: "Step 6 — Verify VRA certificate" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_vra_service_status: investigate
symptom -> step_2_check_vra_rest_api_health: investigate
symptom -> step_3_read_vra_logs: investigate
symptom -> step_4_test_connectivity_from_source: investigate
symptom -> step_5_check_hbrsvc_on_source_esxi: investigate
symptom -> step_6_verify_vra_certificate: investigate
step_1_check_vra_service_status -> resolution
step_2_check_vra_rest_api_health -> resolution
step_3_read_vra_logs -> resolution
step_4_test_connectivity_from_source -> resolution
step_5_check_hbrsvc_on_source_esxi -> resolution
step_6_verify_vra_certificate -> resolution
```

## Before you begin

- **Access:** SSH to the VRA appliance (`admin` user) at each site; SSH to the source ESXi hosts; vCenter Client access to view replication tasks
- **Gather first:** the specific symptom (replication lag, error in vCenter UI, VRA unreachable), the VM name being replicated, the source and target site VRA IP addresses, and the time the issue started
- **Scope:** confirm whether the issue affects one VM, one replication group, or all replications to/from a specific VRA

---

## Step 1 — Check VRA service status

```bash
# SSH to the VRA appliance
ssh admin@<vra-ip>

# Check core VRA services
systemctl status hms     # Home Management Server — must be active
systemctl status vrms    # VR Management Service — must be active
systemctl status nginx   # API gateway — must be active

# Expected: all three should be active (running)

# Recent service events (useful for crash or restart diagnosis)
journalctl -u hms -n 100 --no-pager
journalctl -u vrms -n 100 --no-pager

# Check disk space (full disk = VRA service failures)
df -h /
# Expected: < 80% used

# Restart a specific service if stopped
systemctl start hms
systemctl start vrms
```


```text title="Expected output"
admin@vra-appliance01:~$ systemctl status hms
● hms.service - Home Management Server
     Loaded: loaded (/etc/systemd/system/hms.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 3 days ago
   Main PID: 2847 (java)
      Tasks: 45 (limit: 4915)
     Memory: 512.3M
        CPU: 2h 14m 32s
     CGroup: /system.slice/hms.service
             └─2847 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xmx2g...

admin@vra-appliance01:~$ systemctl status vrms
● vrms.service - VR Management Service
     Loaded: loaded (/etc/systemd/system/vrms.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:25 UTC; 3 days ago
   Main PID: 2891 (java)
      Tasks: 38 (limit: 4915)
     Memory: 384.7M
        CPU: 1h 58m 11s

admin@vra-appliance01:~$ systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:30 UTC; 3 days ago
   Main PID: 2934 (nginx)
      Tasks: 3 (limit: 4915)
     Memory: 18.2M

admin@vra-appliance01:~$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       100G   67G   28G  71% /

admin@vra-appliance01:~$ systemctl start hms
admin@vra-appliance01:~$ systemctl start vrms
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unit hms.service not found.` | Verify the VRA appliance version and confirm hms.service exists with `systemctl list-unit-files | grep hms`. |
    | `Failed to start vrms.service: Unit vrms.service is masked.` | Unmask the service with `systemctl unmask vrms` before attempting to start it. |
    | `Filesystem is 95% full; cannot start services` | Free disk space immediately by removing old logs with `journalctl --vacuum=500M` or clearing replication cache directories. |
---

## Step 2 — Check VRA REST API health

```bash
# Quick health check — no authentication required
curl -sk "https://<vra-ip>/api/rest/vr/health"
# Expected: 200 OK with JSON health response

# Get an authentication token for detailed queries
TOKEN=$(curl -sk -X POST \
  "https://<vra-ip>/api/rest/vr/authentication/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('token',''))")

echo $TOKEN
# Expected: JWT string; empty = auth failed

# List all replications with their state and lag
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-ip>/api/rest/vr/replications" \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin).get('replications', []):
    print(r.get('vmName',''), '|', r.get('replicationState',''), '|', 'lag:', r.get('rpo',''))
"
# Look for: replicationState = ERROR or lag exceeding the configured RPO
```


```text title="Expected output"
{"status":"UP","version":"8.7.2.1","components":{"replication":"HEALTHY","database":"HEALTHY","network":"OK"}}
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwOTMxNjQ4MiwiZXhwIjoxNzA5MzIwMDgyLCJpc3MiOiJ2cmEtMDEuZXhhbXBsZS5jb20ifQ.kX9pL2mQ8vN5oR7sT3uW1xY2zA4bC6dE8fG9hI0jK1l
prod-vm-001 | SYNCED | lag: 0
prod-vm-002 | SYNCING | lag: 45
prod-vm-003 | ERROR | lag: 3600
test-vm-004 | SYNCED | lag: 0
test-vm-005 | PAUSED | lag: 120
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip certificate verification, or import the VRA's certificate into your system trust store. |
    | `jq: command not found` or `python3: command not found` | Install the required JSON parser (`apt install python3` or `brew install jq`) before running the script. |
    | `{"error":"Invalid credentials","code":401}` | Verify the username and password are correct and the admin account is not locked; check VRA audit logs for failed login attempts. |
---

## Step 3 — Read VRA logs

```bash
# SSH to VRA
ssh admin@<vra-ip>

# HMS log directory (management and vCenter registration events)
ls /opt/vmware/logs/hms/
tail -100 /opt/vmware/logs/hms/hms.log | grep -i "error\|exception\|fail"

# VRMS log directory (replication workflow events)
ls /opt/vmware/logs/vrms/
tail -100 /opt/vmware/logs/vrms/vrms.log | grep -i "error\|exception\|fail"

# Follow logs in real time during a failing operation
journalctl -u hms -f
journalctl -u vrms -f

# Nginx log (API gateway; for 5xx errors from the UI or API)
journalctl -u nginx -n 50 --no-pager | grep -i "error\|warn"
```


```text title="Expected output"
admin@vra-prod-01:~$ ssh admin@192.168.1.45
admin@192.168.1.45's password: 
Last login: Wed Jan 15 14:22:33 2025 from 10.0.50.12
admin@vra-prod-01:~$ ls /opt/vmware/logs/hms/
hms.log  hms.log.1  hms.log.2  hms.log.3  hms-audit.log

admin@vra-prod-01:~$ tail -100 /opt/vmware/logs/hms/hms.log | grep -i "error\|exception\|fail"
2025-01-15T14:18:22.456Z ERROR [hms.manager.VcenterManager] Failed to authenticate with vCenter: javax.net.ssl.SSLHandshakeException: PKIX path validation failed
2025-01-15T14:19:05.123Z EXCEPTION [hms.replication.TaskScheduler] NullPointerException in replication task ID: rep-task-8f4a2c1d

admin@vra-prod-01:~$ ls /opt/vmware/logs/vrms/
vrms.log  vrms.log.1  vrms.log.2  vrms-sync.log

admin@vra-prod-01:~$ tail -100 /opt/vmware/logs/vrms/vrms.log | grep -i "error\|exception\|fail"
2025-01-15T14:17:44.789Z ERROR [vrms.replication.Engine] Replication failed for VM: prod-web-server-03 (UUID: 50123456-abcd-ef01-2345-6789abcdef01)
2025-01-15T14:20:11.234Z WARN [vrms.network.Datastore] Datastore connectivity issue detected on ds-repl-02

admin@vra-prod-01:~$ journalctl -u hms -f
-- Logs begin at Wed Jan 15 09:00:01 2025. --
Jan 15 14:22:45 vra-prod-01 hms[2847]: [INFO] HMS service started successfully
Jan 15 14:23:12 vra-prod-01 hms[2847]: [ERROR] Connection timeout to vCenter 192.168.1.100:443 after 30s
^C

admin@vra-prod-01:~$ journalctl -u vrms -f
-- Logs begin at Wed Jan 15 09:00:01 2025. --
Jan 15 14:23:18 vra-prod-01 vrms[3102]: [INFO] Replication sync cycle started
Jan 15 14:23:45 vra-prod-01 vrms[3102]: [ERROR] Insufficient disk space on /var/lib/vrms/cache: 95% full
^C

admin@vra-prod-01:~$ journalctl -u nginx -n 50 --no-pager | grep -i "error\|warn"
Jan 15 14:21:33 vra-prod-01 nginx[1456]: 192.168.1.50 - - [15/Jan/2025:
```
---

## Step 4 — Test connectivity from source ESXi to target VRA

All replication data flows from the source ESXi host to the **target** VRA on TCP 31031.

```bash
# SSH to the source ESXi host
ssh root@<source-esxi-ip>

# Test replication data port (31031) to the TARGET VRA
nc -vz <target-vra-ip> 31031
# Expected: "Connection to <ip> 31031 port [tcp] succeeded!"
# Failure: "Connection refused" or timeout → firewall rule missing

# Test VRA management inter-site port (44046)
nc -vz <target-vra-ip> 44046
# Expected: success
# This port is used for VRA-to-VRA management communication

# VMkernel ping to target VRA (tests Layer 3 from the VMK used for replication)
vmkping -I vmk0 <target-vra-ip>

# Check which VMkernel adapter is used for replication
esxcli network ip interface list | grep -v "^--"
# The hbrsvc daemon uses vmk0 by default unless overridden
```


```text title="Expected output"
Connection to 192.168.45.120 31031 port [tcp] succeeded!
Connection to 192.168.45.120 44046 port [tcp] succeeded!
PING 192.168.45.120 (192.168.45.120): 56 data bytes
64 bytes from 192.168.45.120: icmp_seq=0 time=2.341 ms
64 bytes from 192.168.45.120: icmp_seq=1 time=2.156 ms
64 bytes from 192.168.45.120: icmp_seq=2 time=2.289 ms
64 bytes from 192.168.45.120: icmp_seq=3 time=2.401 ms

Name          IPV4           IPV6                         MAC              MTU  Enabled
vmk0          192.168.40.15  fe80::250:56ff:fe9a:b1c2    00:50:56:9a:b1:c2  1500  true
vmk1          192.168.50.18  fe80::250:56ff:fe9a:b1d4    00:50:56:9a:b1:d4  1500  true
vmk2          192.168.60.22  fe80::250:56ff:fe9a:b1e6    00:50:56:9a:b1:e6  1500  true
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nc: connect to 192.168.45.120 port 31031 (tcp) failed: Connection refused` | Verify the target VRA is running with `systemctl status vmware-hbrsvc` and confirm the firewall rule allows port 31031 from the source ESXi host. |
    | `PING 192.168.45.120 (192.168.45.120): sendto: No route to host` | Check that the replication network is properly routed between sites and that the target VRA IP is reachable from the source ESXi management network. |
    | `vmkping: Unknown option -I vmk0` | Use the correct syntax `vmkping -I vmk0 <target-vra-ip>` or verify the VMkernel adapter name with `esxcli network ip interface list` if vmk0 does not exist. |
If TCP 31031 test fails:
1. Check firewall rules between the source and target networks
2. Verify the target VRA IP address configured in vCenter → Site Recovery → vSphere Replication
3. Confirm Layer 3 routing between sites for the management VLANs

---

## Step 5 — Check hbrsvc on source ESXi

```bash
# SSH to source ESXi host
ssh root@<source-esxi-host>

# Check the replication daemon
/etc/init.d/hbrsvc status
# Expected: Running

# Restart hbrsvc if stopped (safe — does not delete replications)
/etc/init.d/hbrsvc restart

# View hbr.log for per-VM replication events
tail -100 /var/log/hbr.log
grep -i "error\|fail\|disconnect" /var/log/hbr.log | tail -30

# Check for hbr activity in hostd.log
grep -i "hbr\|replication" /var/log/hostd.log | tail -30

# List active replication processes on this host
esxcli vm process list | grep -i replication
```


```text title="Expected output"
root@esx-prod-01:~# /etc/init.d/hbrsvc status
hbrsvc is running.
root@esx-prod-01:~# /etc/init.d/hbrsvc restart
Stopping hbrsvc...
Starting hbrsvc...
root@esx-prod-01:~# tail -100 /var/log/hbr.log
2024-01-15T09:42:31.245Z [7F2A4C1E] HBR: Replication started for VM: prod-db-vm-01 (uuid: 50123456-abcd-1234-5678-9abcdef01234)
2024-01-15T09:43:15.892Z [7F2A4C1F] HBR: Sync checkpoint created: 2.1 GB transferred
2024-01-15T09:45:22.156Z [7F2A4C20] HBR: Network bandwidth throttled to 50 Mbps
2024-01-15T10:12:44.334Z [7F2A4C21] HBR: Replication paused for VM: web-app-vm-02
2024-01-15T10:15:33.667Z [7F2A4C22] HBR: Replication resumed for VM: web-app-vm-02
root@esx-prod-01:~# grep -i "error\|fail\|disconnect" /var/log/hbr.log | tail -30
2024-01-15T08:22:11.445Z [7F2A4C1A] HBR: ERROR: Failed to connect to target host 192.168.100.50:31031 (Connection timeout)
2024-01-15T08:23:45.221Z [7F2A4C1B] HBR: WARNING: Replication lag detected for prod-db-vm-01 (45 seconds behind)
root@esx-prod-01:~# grep -i "hbr\|replication" /var/log/hostd.log | tail -30
2024-01-15T09:41:58.123Z [hostd.HbrManager] HBR replication session initiated for VM: prod-db-vm-01
2024-01-15T09:42:02.456Z [hostd.HbrManager] Replication state: SYNCING (Initial sync 15% complete)
2024-01-15T10:14:22.789Z [hostd.HbrManager] Replication state: IDLE (Waiting for delta sync)
root@esx-prod-01:~# esxcli vm process list | grep -i replication
(no output — no active replication processes currently running)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `hbrsvc is stopped.` | Run `/etc/init.d/hbrsvc start` to restart the replication daemon. |
    | `ERROR: Failed to connect to target host <IP>:<port> (Connection timeout)` | Verify network connectivity between source and target ESXi hosts, check firewall rules for port 31031, and confirm the target host is reachable and running vSphere Replication. |
    **`/var/log/hbr.log: No such file or directory`**
---

## Step 6 — Verify VRA certificate

Expired certificates cause TLS handshake failures between VRA and vCenter and between VRA appliances.

```bash
# Check source VRA management certificate
echo | openssl s_client \
  -connect <vra-source-fqdn>:443 \
  -servername <vra-source-fqdn> 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer
# Expected: notAfter date > 30 days in the future

# Check inter-site VRA certificate (port 44046)
echo | openssl s_client \
  -connect <vra-target-fqdn>:44046 2>/dev/null \
  | openssl x509 -noout -dates -subject

# If certificate is expired, renew via VAMI
# Browse to: https://<vra-ip>:5480 → Certificate → Renew Certificate

# Capture network traffic on the replication port for deep debugging
# On source ESXi host:
pktcap-uw --vmk vmk0 --dstport 31031 -o /tmp/hbr-capture.pcap --count 1000
scp root@<esxi-host>:/tmp/hbr-capture.pcap /local/path/
# Analyze in Wireshark: filter for TCP RST or TLS handshake failure
```


```text title="Expected output"
depth=0 OU = VMware, O = VMware, CN = vra-source.lab.local
verify error:num=18:self signed certificate
verify return:0
subject=OU = VMware, O = VMware, CN = vra-source.lab.local
issuer=OU = VMware, O = VMware, CN = vra-source.lab.local
notBefore=Jan 15 08:22:14 2023 GMT
notAfter=Jan 15 08:22:14 2025 GMT

depth=0 OU = VMware, O = VMware, CN = vra-target.lab.local
verify error:num=18:self signed certificate
verify return:0
subject=OU = VMware, O = VMware, CN = vra-target.lab.local
issuer=OU = VMware, O = VMware, CN = vra-target.lab.local
notBefore=Feb 20 14:51:03 2024 GMT
notAfter=Feb 20 14:51:03 2026 GMT

Capturing on vmk0, 1000 packets
Packet count: 1000
Output file: /tmp/hbr-capture.pcap
root@esxi-host's password: 
hbr-capture.pcap                                100%  2.4MB   8.2MB/s   00:00
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `openssl: connect: Connection refused` | Verify the VRA service is running and the FQDN/port is correct with `netstat -tlnp | grep 443` on the VRA appliance. |
    | `notAfter=<date> GMT` (where date is in the past)` | Renew the certificate immediately via VAMI at `https://<vra-ip>:5480` under Certificate Management to restore replication connectivity. |
    | `Permission denied` (when running pktcap-uw)` | Execute the packet capture command with root privileges or add your user to the appropriate group with `sudo pktcap-uw`. |
---

## Step 7 — Collect VRA support bundle for VMware SR

```bash
# Via VAMI (recommended)
# Browse to: https://<vra-ip>:5480
# Navigate to: Support → Generate Support Bundle → Download
# The bundle includes: all VRA logs, configuration, service state

# Via SSH if VAMI is unreachable
ssh admin@<vra-ip>
/opt/vmware/support/support-bundle.sh
# Output: /tmp/vr-support-<timestamp>.tar.gz

# Transfer the bundle
scp admin@<vra-ip>:/tmp/vr-support-*.tar.gz /local/path/

# Include in VMware SR:
# - VRA VAMI support bundle from both source and target sites
# - hbr.log excerpt from the source ESXi host (grep for the affected VM name)
# - Replication task ID from vCenter → Monitor → Recent Tasks
# - VR version: VRA UI → About (vSphere Replication version)
# - Network connectivity test results (nc -vz output for port 31031 and 44046)
```


```text title="Expected output"
admin@vra-prod-01's password: 
Generating support bundle...
Creating archive of VRA logs and configuration...
Bundle generation completed successfully.
Output: /tmp/vr-support-20240215-143022.tar.gz
Size: 287MB

admin@vra-prod-01:/tmp$ scp admin@vra-prod-01:/tmp/vr-support-20240215-143022.tar.gz /local/path/
vr-support-20240215-143022.tar.gz          100%  287MB   8.2MB/s   00:35

admin@vra-prod-01:/tmp$ nc -vz vra-target-02 31031
Connection to vra-target-02 31031 port [tcp/*] succeeded!

admin@vra-prod-01:/tmp$ nc -vz vra-target-02 44046
Connection to vra-target-02 44046 port [tcp/*] succeeded!

admin@vra-prod-01:/tmp$ grep "vm-prod-web-01" /var/log/vmware/hbr/hbr.log | head -5
2024-02-15T14:28:33.421Z INFO [HbrTask] Replication sync for vm-prod-web-01 completed: 2.3GB transferred
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,password).` | Verify SSH credentials and ensure the admin account is enabled on the VRA appliance via VAMI. |
    | `Connection refused` | Confirm network connectivity between source and target VRA sites and verify firewall rules allow ports 31031 and 44046. |
    | `No such file or directory: /tmp/vr-support-*.tar.gz` | Run the support-bundle.sh script first and verify the output path exists before attempting SCP transfer. |
---

## Log locations

| Component | Path / Command | What to look for |
|---|---|---|
| HMS (VRA) | `/opt/vmware/logs/hms/hms.log` | vCenter registration, management events |
| VRMS (VRA) | `/opt/vmware/logs/vrms/vrms.log` | Replication workflow orchestration errors |
| hbrsvc (ESXi) | `/var/log/hbr.log` | Per-VM replication transfer events and errors |
| hostd (ESXi) | `/var/log/hostd.log` | VM operations and hbrsvc interaction |
| VRA system | `journalctl -u hms` / `journalctl -u vrms` | Service start/stop and crash events |

---

## See also

- [vSphere Replication — Common Issues](../common-issues/)
- [vSphere Replication — Escalation](../escalation/)

## Verify resolution

- `curl -sk https://<vra-ip>/api/rest/vr/health` returns 200 OK from both source and target VRA
- `GET /api/rest/vr/replications` shows all VMs with replicationState = SYNCING or IDLE (not ERROR)
- `nc -zv <target-vra-ip> 31031` from the source ESXi host succeeds
- vCenter → Monitor → Recent Tasks shows no stuck or failed replication tasks for the affected VM
- The replication lag (RPO) for the affected VM is within the configured target
