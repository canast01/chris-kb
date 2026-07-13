---
tags:
  - aria-networks
  - troubleshooting
  - vmware
search:
  boost: 1.5
description: "Aria Operations for Networks (vRNI) diagnostic commands: check platform API health, test data source connectivity from the collector, verify NetFlow..."
---
# Aria Operations for Networks — Diagnostics

<div class="kb-summary">
Aria Operations for Networks (vRNI) diagnostic commands: check platform API health, test data source connectivity from the collector, verify NetFlow traffic with tcpdump, inspect data source last-sync status via REST API, check platform and collector disk space, and collect the support bundle for VMware cases.

*Applies to: VMware Aria Operations for Networks 6.x (vRealize Network Insight)*
</div>
![Aria Operations for Networks — Diagnostics](../../../../../assets/virtualization-vmware-aria-operations-for-networks-troublesh.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "curl /api/ni/health\nCheck component health JSON" {shape: rectangle}
D: "Get data source status via API\nCheck last-sync timestamp" {shape: rectangle}
E: "tcpdump -i eth0 udp port 2055\nVerify NetFlow arriving at collector" {shape: rectangle}
F: "SSH collector VM\nsystemctl status collector" {shape: rectangle}
G: "openssl s_client -connect vrni:443\nCheck cert expiry and CA" {shape: rectangle}
H: "df -h /data /var/log\nCheck data partition on platform VM" {shape: rectangle}
I: "I" {shape: rectangle}
J: "SSH platform VM\ntail /var/log/app.log" {shape: rectangle}
K: "REST: GET /api/ni/data-sources/vcenters\nRead connection_status field" {shape: rectangle}
L: "L" {shape: rectangle}
M: "Test vCenter API from collector\ncurl -sk vcenter-ip/rest/cis/session" {shape: rectangle}
N: "Check sync interval\nvRNI UI → Sources → Sync Now" {shape: rectangle}
O: "O" {shape: rectangle}
P: "Check switch NetFlow config\nVerify collector IP as export destination" {shape: rectangle}
Q: "Check vRNI data source for collector IP match\nCheck proxy.log drop rate" {shape: rectangle}
R: "Check collector log\ntail /var/log/proxy.log" {shape: rectangle}
S: "Replace certificate via vRNI UI\nSettings → SSL Certificates" {shape: rectangle}
T: "Remove old config backups\nls /data/backup/ then rm old dates" {shape: rectangle}
U: "Collect support bundle\nSSH: support-bundle generate" {shape: rectangle}
V: "Open VMware SR\nAttach bundle to GSS case" {shape: rectangle}
A: "vRNI Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> D
D -> K
L -> M
L -> N
O -> P
O -> Q
F -> R
G -> S
H -> T
J -> U
M -> U
N -> U
P -> U
Q -> U
R -> U
S -> U
T -> U
U -> V
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_platform_api_health: "Step 1 — Check platform API health" {shape: rectangle}
step_2_check_data_source_connectivit: "Step 2 — Check data source connectivity and sync status" {shape: rectangle}
step_3_verify_netflow_receipt: "Step 3 — Verify NetFlow receipt" {shape: rectangle}
step_4_inspect_platform_and_collecto: "Step 4 — Inspect platform and collector logs" {shape: rectangle}
step_5_check_disk_space: "Step 5 — Check disk space" {shape: rectangle}
step_6_check_platform_certificate: "Step 6 — Check platform certificate" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_platform_api_health: investigate
symptom -> step_2_check_data_source_connectivit: investigate
symptom -> step_3_verify_netflow_receipt: investigate
symptom -> step_4_inspect_platform_and_collecto: investigate
symptom -> step_5_check_disk_space: investigate
symptom -> step_6_check_platform_certificate: investigate
step_1_check_platform_api_health -> resolution
step_2_check_data_source_connectivit -> resolution
step_3_verify_netflow_receipt -> resolution
step_4_inspect_platform_and_collecto -> resolution
step_5_check_disk_space -> resolution
step_6_check_platform_certificate -> resolution
```

## Before you begin

- **Access:** SSH to the vRNI platform VM (`admin` user); SSH to collector VM(s); vRNI admin UI credentials
- **Gather first:** the specific symptom (topology missing for X datacenter, no NetFlow from Y switch, UI shows error), the data source name, and when data was last seen correctly
- **Scope:** confirm whether the issue affects one data source, one datacenter, one protocol (flows vs. topology), or the entire vRNI platform

---

## Step 1 — Check platform API health

```bash
# From any host that can reach vRNI — no auth required
curl -sk https://<vrni-platform-ip>/api/ni/health
# Expected: {"status": "OK"} or similar JSON with per-service health

# Check API version
curl -sk https://<vrni-platform-ip>/api/ni/info
# Returns: apiVersion, buildNumber, platformVersion

# Get a vRNI API token (required for most data queries)
TOKEN=$(curl -sk -X POST "https://<vrni-platform-ip>/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>","domain":{"domain_type":"LOCAL"}}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

echo $TOKEN
# Expected: JWT string; empty = auth failed (check credentials)
```


```text title="Expected output"
{"status":"OK","services":{"platform":"UP","collector":"UP","api":"UP","ui":"UP"}}
{"apiVersion":"1.0","buildNumber":"21345678","platformVersion":"6.10.1","timestamp":"2024-01-15T09:42:33Z"}
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBsb2NhbCIsImV4cCI6MTcwNTMzODk1MywiaWF0IjoxNzA1MzM1MzUzfQ.kR9mN2pL8vQ5xW1jZ3aB6cD4eF7gH0iJ2kL5mN8oP1q
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification (already present in the example, but ensure it's not removed).
    **`jq: command not found` or `python3: command not found`** — Install the required JSON parser (`apt-get install python3` or `brew install jq`) and use the appropriate tool for your environment.
    **`{"error":"Invalid credentials"}` or empty `$TOKEN` output** — Verify the username, password, and domain are correct; check that the LOCAL domain exists and the admin user is configured in vRNI.
---

## Step 2 — Check data source connectivity and sync status

```bash
# List all vCenter data sources with connection status
curl -sk -H "Authorization: NetworkInsight $TOKEN" \
  "https://<vrni-platform-ip>/api/ni/data-sources/vcenters" \
  | python3 -c "
import json,sys
for ds in json.load(sys.stdin).get('results', []):
    print(ds.get('ip',''), '|', ds.get('nickname',''), '|', ds.get('connection_status',''))
"
# Expected: connection_status = CONNECTED for all configured vCenters
# Problem: DISCONNECTED or FAILED

# List NSX data sources
curl -sk -H "Authorization: NetworkInsight $TOKEN" \
  "https://<vrni-platform-ip>/api/ni/data-sources/nsxt-managers" \
  | python3 -c "
import json,sys
for ds in json.load(sys.stdin).get('results', []):
    print(ds.get('ip',''), '|', ds.get('connection_status',''))
"

# From the COLLECTOR VM — test vCenter API reachability
curl -sk "https://<vcenter-ip>/rest/com/vmware/cis/session" \
  -X POST -u "svc-vrni-vc@vsphere.local:<password>"
# Expected: session token JSON; Error = credentials or network issue

# From the COLLECTOR VM — test NSX Manager API reachability
curl -sk -u "svc-vrni-nsx:<password>" \
  "https://<nsx-manager-ip>/api/v1/cluster/status" | python3 -m json.tool

# Test network connectivity from collector to each data source
nc -zv <vcenter-ip> 443
nc -zv <nsx-manager-ip> 443
nc -zv <vrni-platform-ip> 443
```


```text title="Expected output"
10.20.1.50 | prod-vcenter-01 | CONNECTED
10.20.1.51 | prod-vcenter-02 | CONNECTED
10.20.1.52 | dr-vcenter-01 | DISCONNECTED
10.20.2.100 | CONNECTED
10.20.2.101 | CONNECTED
{"id":"52b2d4a8-1234-5678-abcd-ef1234567890","user":"svc-vrni-vc@vsphere.local"}
{
  "cluster_status": "STABLE",
  "node_count": 3,
  "control_cluster_status": "STABLE"
}
Connection to 10.20.1.50 443 port [tcp/https] succeeded!
Connection to 10.20.2.100 443 port [tcp/https] succeeded!
Connection to 10.20.3.10 443 port [tcp/https] failed: Connection refused
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the VRNI platform certificate into the collector's CA bundle.
    **`jq: command not found`** — Install `python3-json.tool` or use the provided Python one-liner instead of piping to `jq`.
    **`Connection to <ip> 443 port [tcp/https] failed: Connection refused`** — Verify the target service is running and listening on port 443, and check firewall rules between collector and data source.
---

## Step 3 — Verify NetFlow receipt

NetFlow is used for flow analysis (path visibility, security). Switches send UDP to the collector's IP on port 2055.

```bash
# SSH to the collector VM
ssh admin@<collector-ip>

# Capture NetFlow packets arriving at the collector
sudo tcpdump -i eth0 -n udp port 2055 -c 20
# Expected: packets with source IP = switch management/loopback IP
# No packets = switch not sending, or firewall blocking UDP 2055 to collector IP

# Check proxy.log for flow receipt rate
tail -100 /var/log/proxy.log | grep -i "received\|processed\|drop\|error"
# Expected: "Received X flows" at regular intervals
# Problem: "Dropping" or long pause in received counts

# Restart event engine if traps arrive but flows don't appear in vRNI
sudo systemctl restart sannav-event-engine 2>/dev/null || \
  sudo systemctl restart collector
```


```text title="Expected output"
admin@collector-01:~$ ssh admin@192.168.1.45
admin@192.168.1.45's password: 
Last login: Wed Jan 15 14:32:18 2025 from 192.168.1.100
admin@collector-01:~$ sudo tcpdump -i eth0 -n udp port 2055 -c 20
tcpdump: verbose output suppressed, use -v or -vv for full packet decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
14:35:22.451923 IP 10.50.12.5.54821 > 192.168.1.45.2055: UDP, length 1472
14:35:22.452156 IP 10.50.12.5.54822 > 192.168.1.45.2055: UDP, length 1472
14:35:23.104521 IP 10.50.12.6.55103 > 192.168.1.45.2055: UDP, length 1456
14:35:23.105847 IP 10.50.12.6.55104 > 192.168.1.45.2055: UDP, length 1472
14:35:24.667234 IP 10.50.12.5.54823 > 192.168.1.45.2055: UDP, length 1472
...
20 packets captured
admin@collector-01:~$ tail -100 /var/log/proxy.log | grep -i "received\|processed\|drop\|error"
2025-01-15 14:34:58 [INFO] Received 4521 flows from 10.50.12.5 in 2.3s
2025-01-15 14:35:12 [INFO] Processed 4521 flows, 0 dropped
2025-01-15 14:35:28 [INFO] Received 4389 flows from 10.50.12.6 in 2.1s
2025-01-15 14:35:42 [INFO] Processed 4389 flows, 0 dropped
2025-01-15 14:35:58 [INFO] Received 4456 flows from 10.50.12.5 in 2.2s
admin@collector-01:~$ sudo systemctl restart sannav-event-engine 2>/dev/null || \
>   sudo systemctl restart collector
admin@collector-01:~$
```

!!! warning "Common errors"
    **`tcpdump: eth0: No such device`** — Verify the correct interface name with `ip link show` and replace eth0 with the actual interface (e.g., ens0, ens160).
    **`tail: cannot open '/var/log/proxy.log' for reading: Permission denied`** — Run the command with `sudo` prefix: `sudo tail -100 /var/log/proxy.log | grep -i "received\|processed\|drop\|error"`.
    **`Failed to restart sannav-event-engine: Unit sannav-event-engine.service not found`** — Confirm the correct service name with `sudo systemctl list-units --type=service | grep -i event` and use the actual service name in the restart command.
If tcpdump shows no packets:
1. Log in to the switch that should be exporting NetFlow
2. Verify NetFlow export is configured to the collector IP on UDP 2055
3. Confirm the switch VLAN can reach the collector IP (Layer 3 routing)

---

## Step 4 — Inspect platform and collector logs

```bash
# On the platform VM — main application log
sudo tail -100 /var/log/app.log
grep -i "ERROR\|Exception\|fail" /var/log/app.log | tail -50

# On the collector VM — flow proxy log
sudo tail -100 /var/log/proxy.log
grep -i "error\|drop\|disconnect" /var/log/proxy.log | tail -50

# Collector service status
sudo systemctl status collector
journalctl -u collector --since "1 hour ago" | tail -100

# Test connectivity from collector to platform
nc -zv <vrni-platform-ip> 443
# Expected: Connection to platform port 443 succeeded
```


```text title="Expected output"
=== Platform VM Application Log (Last 100 lines) ===
2024-01-15 14:32:18.456 [INFO] Application started successfully
2024-01-15 14:33:02.123 [WARN] Memory usage at 78%
2024-01-15 14:35:41.789 [INFO] Database connection pool initialized: 50 connections
2024-01-15 14:38:15.234 [INFO] Flow data ingestion rate: 12,450 flows/sec
2024-01-15 14:40:22.567 [INFO] Backup completed: 2.3 GB archived

=== Filtered Errors/Exceptions (Last 50 matches) ===
(no matches)

=== Collector VM Proxy Log (Last 100 lines) ===
2024-01-15 14:31:45.123 [INFO] Proxy service initialized on 0.0.0.0:6081
2024-01-15 14:32:10.456 [INFO] Connected to platform 192.168.1.50:443
2024-01-15 14:33:55.789 [INFO] Flow batch 4521 transmitted: 8,932 records
2024-01-15 14:35:20.234 [INFO] Heartbeat sent to platform
2024-01-15 14:37:08.567 [INFO] Flow batch 4522 transmitted: 9,145 records

=== Filtered Errors/Drops (Last 50 matches) ===
(no matches)

=== Collector Service Status ===
● collector.service - vRealize Network Insight Collector
     Loaded: loaded (/etc/systemd/system/collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:31:22 UTC; 2h 15min ago
   Main PID: 2847 (java)
      Tasks: 42 (limit: 4096)
     Memory: 1.2G
        CPU: 18min 32.456s
     CGroup: /systemd/system.slice/collector.service
             └─2847 /usr/lib/jvm/java-11-openjdk/bin/java -Xmx2g -Xms1g...

=== Recent Journal Entries (Last 100 lines, past 1 hour) ===
Jan 15 14:31:22 collector-01 systemd[1]: Started vRealize Network Insight Collector.
Jan 15 14:32:05 collector-01 collector[2847]: [INFO] Collector initialized with UUID: a7f3c2e1-9d4b-4a8f-b6c2-1e5d9f3a2b4c
Jan 15 14:33:18 collector-01 collector[2847]: [INFO] Connected to platform at 192.168.1.50
Jan 15 14:35:42 collector-01 collector[2847]: [INFO] Flow capture started on interfaces: eth0, eth1, eth2
Jan 15 14:40:15 collector-01 collector[2847]: [INFO] Processed 45,231 flows in last 5 minutes

=== Connectivity Test
```
---

## Step 5 — Check disk space

Insufficient disk on the platform VM causes data loss and UI failures.

```bash
# On the PLATFORM VM
df -h /data        # vRNI data partition (flow and topology data)
df -h /var/log     # log partition

# If /data is getting full, check for old config backups (safe to remove old ones)
ls -lh /data/backup/
# Remove backups older than 30 days
sudo find /data/backup/ -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;

# On the COLLECTOR VM
df -h   # Check overall disk usage
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       500G  387G  113G  78% /data

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       100G   67G   33G  67% /var/log

total 2.3G
drwxr-xr-x 3 root root 4.0K Jan 15 14:22 backup_2024_01_15_143022
drwxr-xr-x 3 root root 4.0K Dec 28 09:18 backup_2024_12_28_091805
drwxr-xr-x 3 root root 4.0K Dec 01 16:45 backup_2024_12_01_164512
drwxr-xr-x 3 root root 4.0K Nov 18 22:33 backup_2024_11_18_223301

Filesystem     Size   Used  Avail Use% Mounted on
/dev/sda1      1.8T  1.2T  600G  67% /
/dev/sdb1      2.0T  1.8T  200G  90% /mnt/capture
tmpfs          32G   1.2G   31G   4% /dev/shm
```

!!! warning "Common errors"
    **`find: '/data/backup/': Permission denied`** — Run the find command with `sudo` or ensure your user has read/execute permissions on the /data/backup directory.
    **`rm: remove write-protected regular file 'backup_2024_01_15_143022'?`** — Add the `-f` flag to the rm command within the find exec (`-exec rm -rf {} \;` already includes this, but check file permissions with `ls -l` if the prompt appears).
---

## Step 6 — Check platform certificate

Certificate expiry or mismatch causes browser warnings and API auth failures.

```bash
# Check the vRNI platform certificate expiry
echo | openssl s_client -connect <vrni-platform-ip>:443 -servername <vrni-platform-fqdn> 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer
# Expected: notAfter date in the future; subject matches the FQDN

# Check issuer (confirm it's the expected CA)
echo | openssl s_client -connect <vrni-platform-ip>:443 2>/dev/null \
  | openssl x509 -noout -issuer

# Replace certificate via vRNI UI if expired:
# Settings → Infrastructure → SSL Certificates → Upload Certificate
```


```text title="Expected output"
depth=0 CN = vrni-platform.corp.local
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = vrni-platform.corp.local
verify return:1
subject=CN = vrni-platform.corp.local
issuer=CN = vrni-platform.corp.local, O = VMware, C = US
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2026 GMT

issuer=CN = vrni-platform.corp.local, O = VMware, C = US
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the vRNI platform IP and port are correct and the service is running on port 443.
    **`error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed`** — This is expected for self-signed certificates; the certificate details are still extracted and the expiry date is valid.
---

## Step 7 — Collect support bundle for VMware SR

```bash
# Via SSH on the platform VM (recommended method)
ssh admin@<vrni-platform-ip>
support-bundle generate
# Output: bundle saved to /tmp/support-bundle-<timestamp>.tar.gz
# Download: scp admin@<vrni-platform-ip>:/tmp/support-bundle-*.tar.gz ./

# Via VAMI (if SSH is unavailable)
# Browse to: https://<vrni-platform-ip>:5480
# Navigate to: Support → Generate Support Bundle → Download

# Include in the VMware SR:
# - Support bundle .tar.gz file
# - vRNI version: Settings → About
# - Data source names and connection status
# - Time window when data was last seen correctly
# - Any recent changes to data sources, network, or certificates
```


```text title="Expected output"
admin@vrni-platform-01's password: 
Generating support bundle...
Collecting system logs...
Collecting database diagnostics...
Collecting network configuration...
Collecting application logs...
Bundle generation completed successfully.
bundle saved to /tmp/support-bundle-2024-01-15-143022.tar.gz
File size: 487 MB
Checksum (SHA256): a7f3e8c2d9b1e4f6a8c3d5e7f9a1b2c4d6e8f0a1b2c3d4e5f6a7b8c9d0e1f2
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify the admin account credentials and ensure SSH key-based authentication is configured, or use the VAMI web interface as an alternative.
    **`support-bundle: command not found`** — Confirm you are logged into the vRNI platform VM (not a proxy or collector node) and that your user has support bundle generation privileges.
    **`/tmp/support-bundle-*.tar.gz: No such file or directory`** — Wait for the bundle generation to complete fully before attempting to download, as large bundles may take 5–10 minutes.
---

## Log locations

| Component | Path | What to look for |
|---|---|---|
| Platform | `/var/log/app.log` | API errors, authentication failures, indexing errors |
| Collector (flows) | `/var/log/proxy.log` | NetFlow receipt rate, forwarding status |
| Collector service | `journalctl -u collector` | Service start/stop events |
| Disk | `df -h /data` | Capacity used vs. total; > 80% = action needed |

---

## See also

- [vRNI Common Issues](../common-issues/)
- [vRNI Escalation](../escalation/)

## Verify resolution

- `curl -sk https://<vrni-platform-ip>/api/ni/health` returns `{"status": "OK"}`
- Data source connection status returns `CONNECTED` for all configured vCenters and NSX Managers
- `tcpdump -i eth0 -n udp port 2055 -c 10` captures NetFlow packets from all expected switches
- vRNI UI → Dashboard shows topology data refreshed within the last sync interval
- `df -h /data` shows at least 20% free space on the data partition
