---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# Dell ECS — Diagnostics

<div class="kb-summary">
ECS diagnostic commands: authenticate to the Management REST API and check cluster node health with <code>GET /vdc/nodes</code>, inspect active alerts via <code>/vdc/alerts</code>, test the S3 data path with <code>aws s3api head-bucket</code> and <code>head-object</code>, SSH to individual nodes to inspect the storageos service and Cassandra ring health, check geo-replication lag via <code>/vdc/geo-replication/status</code>, and collect a support bundle via <code>POST /vdc/support-bundle</code> for Dell escalation.

*Applies to: ECS 3.x*
</div>
![Dell ECS — Diagnostics](../../../../assets/storage-dell-ecs-troubleshooting-diagnostics.svg)

```d2
direction: right

A: "ECS Issue Reported" {shape: rectangle}
B: "GET /vdc/nodes: cluster health\nGET /vdc/alerts: active alerts" {shape: rectangle}
C: "C" {shape: rectangle}
D: "SSH to affected node\nsystemctl status storageos caspian" {shape: rectangle}
E: "E" {shape: rectangle}
F: "journalctl -u storageos: logs\ndf -h /data/ — disk full?\nRestart only if logs confirm safe" {shape: rectangle}
G: "nodetool status: Cassandra ring\necho srvr | nc 2181: ZK mode\nlsblk: check for disk errors" {shape: rectangle}
H: "H" {shape: rectangle}
I: "aws s3api head-bucket: auth check\nCheck IAM user + bucket policy\nVerify addr style and namespace" {shape: rectangle}
J: "J" {shape: rectangle}
K: "nc -zv remote-node 9100: WAN port\nGET /vdc/nodes: remote VDC health\nMonitor WAN bandwidth" {shape: rectangle}
L: "Tail ECS logs for transient errors\ntail /var/log/ecs/*.log | grep ERR" {shape: rectangle}
M: "Collect support bundle\nPOST /vdc/support-bundle or Portal\nOpen Dell support case" {shape: rectangle}

A -> B
C -> D
E -> F
E -> G
H -> I
J -> K
J -> L
F -> M
G -> M
I -> M
K -> M
L -> M
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_management_api_health_check: "Step 1 — Management API health check" {shape: rectangle}
step_2_s3_api_diagnostics: "Step 2 — S3 API diagnostics" {shape: rectangle}
step_3_nodelevel_ssh_diagnostics: "Step 3 — Node-level SSH diagnostics" {shape: rectangle}
step_4_georeplication_diagnostics: "Step 4 — Geo-replication diagnostics" {shape: rectangle}
step_5_support_bundle_collection: "Step 5 — Support bundle collection" {shape: rectangle}
log_locations: "Log locations" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_management_api_health_check: investigate
symptom -> step_2_s3_api_diagnostics: investigate
symptom -> step_3_nodelevel_ssh_diagnostics: investigate
symptom -> step_4_georeplication_diagnostics: investigate
symptom -> step_5_support_bundle_collection: investigate
symptom -> log_locations: investigate
step_1_management_api_health_check -> resolution
step_2_s3_api_diagnostics -> resolution
step_3_nodelevel_ssh_diagnostics -> resolution
step_4_georeplication_diagnostics -> resolution
step_5_support_bundle_collection -> resolution
log_locations -> resolution
```

## Before you begin

- **Access:** Management REST API at `https://<ecs-node>:4443` (authenticate first to get a session token); SSH to ECS nodes as `admin`; ECS Portal admin account; S3 credentials (access key and secret key) for data path tests
- **Gather first:** ECS version (`GET /vdc/version`), active alerts (`GET /vdc/alerts`), VDC node list (`GET /vdc/nodes`), and the specific symptom — S3 HTTP error code, node state, or geo-replication lag percentage
- **Scope:** confirm whether the issue affects one node, one VDC, or geo-replication between VDCs — a single DEGRADED node is different from cluster-wide unavailability
- **Session tokens:** expire after 8 hours; re-authenticate with the `/login` endpoint if commands return 401

---

## Step 1 — Management API health check

```bash
# Authenticate to the ECS Management REST API
TOKEN=$(curl -sk -u "sysadmin:<password>" \
  -D - "https://<ecs-node>:4443/login" \
  | grep "X-SDS-AUTH-TOKEN" | awk '{print $2}' | tr -d '\r')

ECS="https://<ecs-node>:4443"

# VDC capacity — fields: totalProvisioned_gb, usedCapacity_gb, availableCapacity_gb
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/capacity" | python3 -m json.tool

# Node health — nodestatus: GOOD | DEGRADED | UNKNOWN
# All nodes must show GOOD before any planned change
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/nodes" | python3 -m json.tool

# Specific node details
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/nodes/<node-id>" | python3 -m json.tool

# Active alerts
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/alerts" | python3 -m json.tool

# ECS software version
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/version" | python3 -m json.tool

# Geo-replication status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/geo-replication/status" | python3 -m json.tool

# Replication groups (vpools)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/data-service/vpools" | python3 -m json.tool

# Dashboard zone health
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/dashboard/zones/localzone" | python3 -m json.tool

# Namespace list
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/object/namespaces" | python3 -m json.tool

# Bucket list for a namespace
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/object/bucket?namespace=<namespace>" | python3 -m json.tool

# Invalidate session
curl -sk -H "X-SDS-AUTH-TOKEN: $TOKEN" "$ECS/logout" > /dev/null
```


```text title="Expected output"
X-SDS-AUTH-TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzeXNhZG1pbiIsImV4cCI6MTcwOTMzNDU2MH0.a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
{
  "totalProvisioned_gb": 50000,
  "usedCapacity_gb": 34567,
  "availableCapacity_gb": 15433,
  "percentageUsed": 69.1
}
{
  "nodes": [
    {
      "id": "ecs-node-01",
      "nodestatus": "GOOD",
      "ip": "192.168.1.101",
      "version": "3.6.1.1.0.20240101"
    },
    {
      "id": "ecs-node-02",
      "nodestatus": "GOOD",
      "ip": "192.168.1.102",
      "version": "3.6.1.1.0.20240101"
    },
    {
      "id": "ecs-node-03",
      "nodestatus": "DEGRADED",
      "ip": "192.168.1.103",
      "version": "3.6.1.1.0.20240101"
    }
  ]
}
{
  "id": "ecs-node-03",
  "nodestatus": "DEGRADED",
  "cpuUsage": 78.5,
  "memoryUsage": 82.3,
  "diskUsage": 91.2,
  "replicationFactor": 3,
  "activeAlerts": 2
}
{
  "alerts": [
    {
      "id": "alert-8472",
      "severity": "WARNING",
      "message": "Disk usage on ecs-node-03 exceeds 90%",
      "timestamp": "2024-01-15T09:23:45Z"
    },
    {
      "id": "alert-8471",
      "severity": "CRITICAL",
      "message": "Replication lag detected on vpool-prod: 2.5GB behind",
      "timestamp": "2024-01-15T08:15:22Z"
    }
  ]
}
{
  "version": "3.6.1.1.0.20240101",
  "buildNumber": "20240101.001",
  "releaseDate": "2024-01-01"
}
{
  "geoReplicationStatus": "HEALTHY",
  "sites": [
    {
      "name": "dc-primary",
      "status": "ACTIVE",
      "lag_bytes": 0
    },
    {
      "name": "dc-secondary",
      "status": "ACTIVE",
      "lag_bytes": 1048576
    }
  ]
}
{
  "vpools": [
    {
      "id": "vpool-prod",
      "name": "Production",
```
---

## Step 2 — S3 API diagnostics

```bash
S3_EP="https://<ecs-s3-endpoint>:9021"
PROFILE="--profile ecs --endpoint-url $S3_EP --no-verify-ssl"

# Test S3 connectivity (list buckets)
aws s3 ls $PROFILE

# Head a specific bucket (tests auth and bucket existence)
aws s3api head-bucket --bucket <bucket> $PROFILE

# Head a specific object (tests object existence and access)
aws s3api head-object --bucket <bucket> --key <object-key> $PROFILE

# List objects in a bucket
aws s3 ls s3://<bucket>/ $PROFILE

# List incomplete multipart uploads
aws s3api list-multipart-uploads --bucket <bucket> $PROFILE

# Get bucket versioning state
aws s3api get-bucket-versioning --bucket <bucket> $PROFILE

# Get bucket policy
aws s3api get-bucket-policy --bucket <bucket> $PROFILE

# Get object lock configuration
aws s3api get-object-lock-configuration --bucket <bucket> $PROFILE

# TLS certificate check on S3 endpoint
openssl s_client -connect <ecs-s3-endpoint>:9021 -servername <ecs-s3-endpoint> \
  </dev/null 2>/dev/null | openssl x509 -noout -dates -subject -issuer

# Test raw HTTP connectivity to S3 endpoint
curl -sv --max-time 10 "https://<ecs-s3-endpoint>:9021/" \
  --resolve "<ecs-s3-endpoint>:9021:<ecs-node-ip>" \
  --insecure 2>&1 | grep -E "< HTTP|Connected|SSL|certificate"
```


```text title="Expected output"
2024-01-15 10:23:45 prod-bucket-01
2024-01-15 10:24:12 prod-bucket-02
2024-01-15 10:24:33 archive-bucket
(no output — command completes silently)
(no output — command completes silently)
2024-01-15 10:25:01       4096 backup/
2024-01-15 10:25:02    1048576 data-export-2024-01.tar.gz
2024-01-15 10:25:03     512000 config.json
(no output — command completes silently)
Status: ENABLED
MFADelete: DISABLED
(no output — command completes silently)
(no output — command completes silently)
notBefore=Jan 15 08:30:00 2024 GMT
notAfter=Jan 15 08:30:00 2025 GMT
subject=CN=ecs-s3-node01.prod.local
issuer=CN=ECS-CA,O=Dell EMC,C=US
* Connected to ecs-s3-node01.prod.local (192.168.1.45) port 9021 (#0)
< HTTP/1.1 200 OK
* SSL connection using TLSv1.2 / ECDHE-RSA-AES256-GCM-SHA384
* Server certificate: subject name 'ecs-s3-node01.prod.local' matched
```

!!! warning "Common errors"
    **`An error occurred (InvalidAccessKeyId) when calling the ListBuckets operation: The Access Key Id you provided does not exist in our records.`** — Verify the AWS profile credentials in ~/.aws/credentials are correct and the ECS user has S3 access permissions.
    **`An error occurred (NoSuchBucket) when calling the HeadBucket operation: The specified bucket does not exist.`** — Confirm the bucket name is spelled correctly and exists in the ECS cluster by listing all buckets first.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `--insecure` flag to curl or import the ECS CA certificate into your system trust store to bypass SSL verification.
### Workflow: S3 Access Denied

1. Confirm the access key and secret key are correct (secret keys cannot be retrieved from ECS — if lost, rotate)
2. Confirm the object user exists in the correct namespace: `ecscli user list-object-users --namespace <ns>`
3. Check the bucket policy: `aws s3api get-bucket-policy --bucket <bucket> $PROFILE`
4. Check the bucket ACL: `aws s3api get-bucket-acl --bucket <bucket> $PROFILE`
5. Verify the S3 request is using the correct addressing style (path-style vs virtual-hosted-style)
6. Check that the bucket exists in the expected namespace: `ecscli bucket get --namespace <ns> --name <bucket>`

---

## Step 3 — Node-level SSH diagnostics

```bash
# SSH to an ECS node
ssh admin@<ecs-node>

# ECS service health
systemctl status storageos     # Main ECS data service
systemctl status caspian       # ECS fabric agent

# Check across all nodes simultaneously
viprexec -v -cmd "systemctl is-active storageos"
viprexec -v -cmd "systemctl is-active caspian"

# Disk diagnostics
df -h /data/                                           # Data partition usage
df -h                                                  # All disk mounts
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,STATE             # Disk layout, type, state
viprexec -v -cmd "df -h /data/"                        # Check across all cluster nodes

# System resources
uptime
free -h
viprexec -v -cmd "free -h"
ps aux | grep -E "storageos|caspian|java" | grep -v grep
```


```text title="Expected output"
admin@ecs-node-01:~$ systemctl status storageos
● storageos.service - Dell EMC ECS StorageOS Service
     Loaded: loaded (/etc/systemd/system/storageos.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:18 UTC; 45min ago
   Main PID: 2847 (java)
      Tasks: 87 (limit: 4915)
     Memory: 2.3G
     CGroup: /system.slice/storageos.service
             └─2847 /usr/lib/jvm/java-11-openjdk/bin/java -Xmx4g...

admin@ecs-node-01:~$ systemctl status caspian
● caspian.service - ECS Fabric Agent
     Loaded: loaded (/etc/systemd/system/caspian.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:31:55 UTC; 46min ago
   Main PID: 1923 (caspian)
      Tasks: 12 (limit: 4915)
     Memory: 156.2M

admin@ecs-node-01:~$ viprexec -v -cmd "systemctl is-active storageos"
ecs-node-01: active
ecs-node-02: active
ecs-node-03: active

admin@ecs-node-01:~$ df -h /data/
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       2.7T  1.8T  847G  68% /data

admin@ecs-node-01:~$ lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,STATE
NAME    SIZE FSTYPE MOUNTPOINT STATE
sda     2.7T
├─sda1  512M vfat   /boot      live
├─sda2  100G ext4   /          live
└─sda3  2.6T ext4   /data      live
sdb     1.8T
└─sdb1  1.8T ext4   /archive   live

admin@ecs-node-01:~$ uptime
 14:58:22 up 12 days, 3:14, 2 users, load average: 2.34, 2.18, 2.41

admin@ecs-node-01:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:           31Gi       18Gi       8.2Gi       512Mi       4.8Gi       12Gi
Swap:          8.0Gi      1.2Gi       6.8Gi

admin@ecs-node-01:~$ viprexec -v -cmd "free -h"
ecs-node-01: Mem: 31Gi used: 18Gi free: 8.2Gi
ecs-node-02: Mem: 31Gi used: 19Gi free: 7.1Gi
ecs-node-03: Mem: 31Gi used: 17Gi free: 9.3Gi
```
### Cassandra (metadata store)

```bash
# Ring status: UN = Up/Normal | DN = Down | UJ = Joining | UL = Leaving
/opt/storageos/tools/nodetool status

# Compaction activity (high compaction = elevated metadata latency)
/opt/storageos/tools/nodetool compactionstats

# Heap usage (heap pressure = GC pauses = slow metadata responses)
/opt/storageos/tools/nodetool info | grep -iE "heap|load"

# Flush Cassandra memtables (can help if writes are stalled)
/opt/storageos/tools/nodetool flush

# Node info (token, DC, rack, load)
/opt/storageos/tools/nodetool ring
```


```text title="Expected output"
Datacenter: DC1
===============
Status=Up/Normal
|/ State=Normal/Leaving/Joining/Moving
--  Address          Load       Tokens  Owns (effective)  Host ID                               Rack
UN  192.168.1.45     156.82 GB  256     33.3%             a7f2c8d1-9e4b-42f3-8c1a-5d6e9f2b3c4d  RAC1
UN  192.168.1.46     149.21 GB  256     33.3%             b8e3d9e2-af5c-53g4-9d2b-6e7f0a3c4d5e  RAC1
UN  192.168.1.47     152.65 GB  256     33.4%             c9f4eaf3-bg6d-64h5-ae3c-7f8g1b4d5e6f  RAC2
DN  192.168.1.48     0 B        256     0.0%              d0g5fbg4-ch7e-75i6-bf4d-8g9h2c5e6f7g  RAC2

pending tasks: 2
- compaction: 1
- validation: 1
Compaction from [default] sstable(s)
Estimated remaining time : 2m45s
Active : 1 (147.2 MB)

Heap Memory (MB) : 8192.00 / 16384.00
Non Heap Memory (MB) : 128.45 / -1.00
Load : 156.82 GB

Token            : 85070591730234615865843651857942052864
Datacenter       : DC1
Rack             : RAC1
Status           : Up/Normal
State             : Normal
Load              : 156.82 GB
Owns              : 33.3%
Host ID          : a7f2c8d1-9e4b-42f3-8c1a-5d6e9f2b3c4d
...
```

!!! warning "Common errors"
    **`nodetool: command not found`** — Verify the ECS node is running and `/opt/storageos/tools/` exists; if missing, reinstall the ECS package or check the installation path.
    **`Connection refused`** — Ensure the Cassandra/ECS metadata service is running with `systemctl status storageos` and restart if needed.
    **`Flush operation timed out`** — Increase the nodetool timeout with `-Dcom.sun.jndi.rmi.factory.socket.timeout=30000` or reduce concurrent flushes by checking `nodetool compactionstats` for stuck operations.
### ZooKeeper (cluster coordination)

```bash
# Mode should be 'leader' on one node and 'follower' on all others
echo "srvr" | nc localhost 2181 | grep Mode

# Outstanding requests should be near zero during steady state
echo "stat" | nc localhost 2181 | grep outstanding

# Connection count (elevated connections may indicate a stuck client)
echo "stat" | nc localhost 2181 | grep connections

# List all ZK nodes in the ensemble
echo "conf" | nc localhost 2181
```


```text title="Expected output"
Mode: leader
Outstanding: 0
Connections: 4
server.1=zk-node-1.internal:2888:3888
server.2=zk-node-2.internal:2888:3888
server.3=zk-node-3.internal:2888:3888
```

!!! warning "Common errors"
    **`Connection refused`** — Verify ZooKeeper is running with `systemctl status zookeeper` and listening on port 2181.
    **`Mode: follower` on the expected leader node** — Check cluster quorum status with `echo "stat" | nc localhost 2181` and review ZooKeeper logs at `/var/log/zookeeper/zookeeper.log` for election failures.
    **`Outstanding: <high number>` (e.g., Outstanding: 847)** — Identify slow clients with `echo "cons" | nc localhost 2181` and check for network latency or client-side processing delays.
### NTP and clock sync

```bash
chronyc tracking
timedatectl status
# All nodes should agree within 100ms; mismatched clocks cause geo-replication errors
viprexec -v -cmd "date"
```


```text title="Expected output"
reference ID    : 91.189.89.198 (ntp.ubuntu.com)
stratum         : 2
ref time (UTC)  : Fri Nov 17 14:32:18 2023
system time     : 0.000234567 seconds fast of NTP time
latest offset   : +0.000156 seconds
rms offset      : 0.000089 seconds
frequency       : -2.341 ppm
residual freq   : +0.002 ppm
skew            : 0.087 ppm
root delay      : 0.035682 seconds
root dispersion : 0.012456 seconds
max_distance    : 0.050138 seconds
leap status     : Normal

               Local time: Fri 2023-11-17 14:32:18 UTC
           Universal time: Fri 2023-11-17 14:32:18 UTC
                 RTC time: Fri 2023-11-17 14:32:18
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
                 RTC in UTC: yes

node-01: Fri Nov 17 14:32:18 UTC 2023
node-02: Fri Nov 17 14:32:19 UTC 2023
node-03: Fri Nov 17 14:32:18 UTC 2023
```

!!! warning "Common errors"
    **`chronyc: command not found`** — Install chrony with `apt-get install chrony` or `yum install chrony` depending on your OS.
    **`viprexec: command not found or not in PATH`** — Source the ECS environment setup script or add the viprexec binary directory to your PATH.
    **`node-02: Fri Nov 17 14:32:28 UTC 2023` (10+ second drift detected)** — Restart the chronyd service on the drifted node with `systemctl restart chronyd` and verify NTP connectivity.
### Network connectivity

```bash
# Test inter-node connectivity on the data network
ping -c 4 <other-ecs-node-data-ip>

# Test WAN connectivity to remote VDC nodes (geo-replication port)
nc -zv <remote-vdc-node> 9100

# Test KMIP connectivity (if encryption at rest with external KMS is configured)
nc -zv <kmip-server> 5696
```


```text title="Expected output"
PING 10.50.12.45 (10.50.12.45) 56(84) bytes of data.
64 bytes from 10.50.12.45: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 10.50.12.45: icmp_seq=2 ttl=64 time=2.41 ms
64 bytes from 10.50.12.45: icmp_seq=3 ttl=64 time=2.38 ms
64 bytes from 10.50.12.45: icmp_seq=4 ttl=64 time=2.39 ms

--- 10.50.12.45 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 2.34/2.38/2.41/0.03 ms
Connection to 172.16.8.92 9100 port [tcp] succeeded!
Connection to 203.0.113.54 5696 port [tcp] succeeded!
```

!!! warning "Common errors"
    **`connect to 172.16.8.92 port 9100 (tcp) failed: Connection refused`** — Verify the remote VDC node's replication service is running with `systemctl status ecs-replication` on the target node.
    **`PING: sendto: No route to host`** — Confirm the data network interface is up and the subnet routing is correct with `ip route show` and `ip link show`.
    **`connect to 203.0.113.54 port 5696 (tcp) failed: Connection timed out`** — Check firewall rules and network ACLs allow port 5696 from the ECS node to the KMIP server, and verify the KMIP server IP/hostname is correct.
### Workflow: Node Marked DEGRADED

1. `GET /vdc/nodes` — identify which node is DEGRADED and its node ID
2. `GET /vdc/alerts` — check for disk or NIC failure alerts correlated with the node
3. SSH to the affected node: `ssh admin@<ecs-node>`
4. `systemctl status storageos` — confirm whether the ECS service is running
5. `df -h /data/` — check if the data partition is full or unmounted
6. `lsblk` — identify any disks showing error state in the OS
7. Check system log: `journalctl -xe | grep -iE "disk|error|fault" | tail -50`
8. If a disk failure is confirmed: initiate disk replacement via **ECS Portal → Hardware → Disks → Replace Disk**
9. Monitor rebuild progress in **ECS Portal → Hardware → Disks** until the new disk shows `GOOD`

---

## Step 4 — Geo-replication diagnostics

```bash
# Current geo-replication status (all replication groups)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/geo-replication/status" | python3 -m json.tool

# Replication groups (vpools)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/data-service/vpools" | python3 -m json.tool
```


```text title="Expected output"
{
  "replication_groups": [
    {
      "id": "urn:storageos:ReplicationGroupInfo:8f3c9e2a-1b4d-4e7f-9c2b-5d8a1f6e3c9a:vdc1",
      "name": "us-west-prod",
      "status": "HEALTHY",
      "replication_lag_ms": 245,
      "last_sync": "2024-01-15T14:32:18Z",
      "peer_vdc": "eu-central-prod"
    },
    {
      "id": "urn:storageos:ReplicationGroupInfo:3d7e2c1f-9a4b-4c6e-8d1a-2f5b9e3c7a1d:vdc1",
      "name": "us-east-dr",
      "status": "HEALTHY",
      "replication_lag_ms": 512,
      "last_sync": "2024-01-15T14:32:05Z",
      "peer_vdc": "us-west-prod"
    }
  ],
  "total_groups": 2
}
{
  "vpools": [
    {
      "id": "urn:storageos:VirtualPool:4a2f8c1e-7b3d-4f9a-1c5e-8d2b6f3a9c1e",
      "name": "tier1-ssd",
      "description": "High-performance SSD pool",
      "protocols": ["S3", "SWIFT"],
      "replication_group": "us-west-prod",
      "capacity_gb": 5242880,
      "used_gb": 2097152
    },
    {
      "id": "urn:storageos:VirtualPool:9e1c3f7a-2d5b-4a8c-6f1d-3e9a2c5b7f4a",
      "name": "tier2-sata",
      "description": "Standard capacity SATA pool",
      "protocols": ["S3"],
      "replication_group": "us-east-dr",
      "capacity_gb": 10485760,
      "used_gb": 4194304
    }
  ],
  "total_vpools": 2
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to 10.20.30.40 port 443: Connection refused`** — Verify the ECS management endpoint is running and accessible; check `curl -v https://$ECS:4443/` to confirm connectivity.
    **`error: 401 Unauthorized`** — Ensure the authentication token in `$TOKEN` is valid and not expired; regenerate it with the login endpoint.
    **`json.tool: No JSON object could be decoded`** — Confirm the API endpoint URL is correct and the response is valid JSON; test with `curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" "$ECS/vdc/geo-replication/status"` without piping to verify raw output.
### Workflow: Geo-Replication Lag Growing

1. **ECS Portal → Geo Monitoring** — identify which replication group has growing lag and which VDC is behind
2. Confirm the remote VDC is healthy: `GET /vdc/nodes` against the remote VDC endpoint
3. Check WAN bandwidth utilisation on the inter-site link at the time lag started growing
4. Confirm port 9100 is reachable between VDCs: `nc -zv <remote-vdc-node> 9100`
5. Check for alerts on the remote VDC: `GET /vdc/alerts` against the remote VDC endpoint
6. If the remote VDC is healthy and WAN is not saturated: check ECS data service logs for replication errors
7. If the WAN link is saturated: adjust replication group bandwidth throttle in **ECS Portal → Replication → Bandwidth Management**

```bash
# Search for geo-replication errors in service logs
grep -r "replication" /var/log/ecs/ | grep -iE "error|failed|timeout" | tail -50

# Check for time sync drift between VDC sites (mismatched clocks cause geo-rep errors)
viprexec -v -cmd "date"
chronyc tracking
```


```text title="Expected output"
/var/log/ecs/replication-service.log:2024-01-15T09:23:44.521Z [ERROR] Replication failed for bucket-prod-01: Connection timeout after 30s to vdc-site-2.example.com
/var/log/ecs/replication-service.log:2024-01-15T09:24:12.103Z [ERROR] Replication queue overflow: 2847 pending objects in vdc-site-1
/var/log/ecs/replication-service.log:2024-01-15T09:25:33.891Z [WARN] Replication retry attempt 3/5 for object uuid-a4c2-9f1e-7b3d
/var/log/ecs/geo-replication.log:2024-01-15T09:26:01.445Z [ERROR] Failed to replicate metadata: clock skew detected (drift: 2.847s)
/var/log/ecs/replication-service.log:2024-01-15T09:27:15.662Z [ERROR] Replication timeout on vdc-site-3: no response from 10.42.18.55:4443

viprexec -v -cmd "date"
2024-01-15 09:28:47.123456 UTC

chronyc tracking
Reference ID    : 169.254.169.123 (ntp.aws.amazon.com)
Stratum         : 2
Ref time (UTC)  : Mon Jan 15 09:28:45 2024
System time     : 0.000234567 seconds slow of NTP time
Frequency       : -12.456 ppm
Residual freq   : +0.123 ppm
Skew            : 0.089 ppm
Root delay      : 0.031234 seconds
Root dispersion : 0.087654 seconds
Update interval : 64.2 seconds
Leap status     : Normal
```

!!! warning "Common errors"
    **`grep: /var/log/ecs/: No such file or directory`** — Verify ECS service is running with `systemctl status ecs-replication-service` and check the correct log path with `find /var/log -name "*replication*" -type f`.
    **`viprexec: command not found`** — Source the ECS environment setup script with `source /opt/emc/ecs/bin/ecs-env.sh` or verify viprexec is in PATH with `which viprexec`.
    **`Stratum         : 16`** — NTP is not synchronized; restart chrony with `systemctl restart chrony` and verify NTP server reachability with `chronyc sources`.
---

## Step 5 — Support bundle collection

```bash
# ECS software version
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/version" | python3 -m json.tool

# Node list and health status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/nodes" | python3 -m json.tool

# Active alerts
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/alerts" | python3 -m json.tool

# VDC capacity
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/capacity" | python3 -m json.tool

# Replication group status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/data-service/vpools" | python3 -m json.tool

# Namespace and bucket inventory
ecscli namespace list
ecscli bucket list --namespace <affected-namespace>
ecscli bucket get --namespace <affected-namespace> --name <affected-bucket>

# Generate support bundle (mandatory for Sev1/Sev2)
curl -s -k -X POST \
  -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/support-bundle" | python3 -m json.tool
# Alternatively: ECS Portal → Support → Collect Logs
```


```text title="Expected output"
{
  "version": "3.6.1.0.20240115",
  "build": "r20240115-release",
  "release_date": "2024-01-15T00:00:00Z"
}
{
  "nodes": [
    {
      "id": "10.50.1.101",
      "name": "ecs-node-01",
      "status": "GOOD",
      "cpu_usage": 42.3,
      "memory_usage": 58.7
    },
    {
      "id": "10.50.1.102",
      "name": "ecs-node-02",
      "status": "GOOD",
      "cpu_usage": 39.1,
      "memory_usage": 61.2
    },
    {
      "id": "10.50.1.103",
      "name": "ecs-node-03",
      "status": "DEGRADED",
      "cpu_usage": 78.9,
      "memory_usage": 85.4
    }
  ]
}
{
  "alerts": [
    {
      "id": "alert-2024-0847",
      "severity": "WARNING",
      "message": "Node ecs-node-03 CPU utilization above 75%",
      "timestamp": "2024-01-15T14:32:18Z"
    },
    {
      "id": "alert-2024-0846",
      "severity": "INFO",
      "message": "Replication lag detected on vpool-prod: 2.3GB",
      "timestamp": "2024-01-15T13:45:02Z"
    }
  ]
}
{
  "capacity": {
    "total_gb": 102400,
    "used_gb": 87654,
    "available_gb": 14746,
    "utilization_percent": 85.6
  }
}
{
  "vpools": [
    {
      "id": "vpool-prod",
      "name": "Production",
      "replication_factor": 3,
      "status": "HEALTHY",
      "nodes": 3
    },
    {
      "id": "vpool-archive",
      "name": "Archive",
      "replication_factor": 2,
      "status": "HEALTHY",
      "nodes": 3
    }
  ]
}
Namespace: prod-ns
Namespace: archive-ns
Namespace: test-ns

Bucket: app-data-prod (Size: 2.4TB, Objects: 1847293)
Bucket: logs-archive (Size: 8.7TB, Objects: 12456789)
Bucket: temp-cache (Size: 156GB, Objects: 89234)

{
  "name": "app-data-prod",
  "namespace": "prod-ns",
  "created": "2023-06-10T09:15:22Z",
  "size_gb": 2457.3,
  "object_count": 1847293,
  "versioning": "ENABLED",
  "encryption": "AES-256"
}
{
  "bundle_id": "support-bundle-20240115-143521
```
**Information to prepare before the call:**

| Item | Detail |
|---|---|
| ECS software version | From `GET /vdc/version` |
| Number of VDCs and nodes per VDC | Topology description |
| Replication group configuration | Mode (sync/async), VDC pairing |
| Approximate time the issue started | As precise as possible |
| Recent changes | Upgrades, network changes, new buckets, IAM changes in the 48h before the issue |
| Error messages | From ECS Portal, S3 client logs, and application logs |
| Impact | Which namespaces/buckets/applications are affected |

---

## Log locations

| Log | Location | Content |
|---|---|---|
| ECS data service log | `/var/log/ecs/` on each node | Object I/O, erasure coding, replication errors, chunk placement |
| ECS portal / management log | `/var/log/ecs-portal/` or `journalctl -u ecs-portal` | API requests, portal events, authentication failures |
| ECS fabric agent log | `/opt/emc/caspian/fabric/agent/logs/agent.log` | Node lifecycle, upgrade, and fabric events |
| OS system log | `/var/log/messages` or `journalctl -xe` | Node OS events, hardware errors, kernel messages |
| Cassandra log | `/opt/storageos/db/logs/system.log` | Metadata store events, compaction, GC events |
| ZooKeeper log | `/opt/storageos/zookeeper/logs/zookeeper.log` | Cluster coordination events |
| Geo-replication log | ECS Portal → Logs → Geo Replication | Replication job status and per-object replication errors |
| Audit log | ECS Portal → Monitoring → Audit | Admin actions — create/modify/delete namespace, bucket, IAM |

```bash
# Tail ECS data service log for real-time error monitoring
tail -f /var/log/ecs/*.log | grep -iE "error|exception|failed|degraded"

# Tail fabric agent log
tail -f /opt/emc/caspian/fabric/agent/logs/agent.log

# Journalctl for ECS services
journalctl -u storageos -f --no-pager
journalctl -u caspian -f --no-pager

# Search Cassandra log for recent errors
journalctl -u cassandra --since "1 hour ago" | grep -iE "error|exception|heap"
```


```text title="Expected output"
==> /var/log/ecs/data-service.log <==
2024-01-15T14:32:18.445Z ERROR [DataService] Failed to replicate chunk 0x7f2a3c9e to node-03: Connection timeout
2024-01-15T14:33:02.112Z EXCEPTION [ReplicationManager] java.io.IOException: Disk space critical on /data/chunks (92% full)
2024-01-15T14:34:45.667Z ERROR [ObjectStore] Degraded read performance detected: avg latency 450ms (threshold: 200ms)

==> /opt/emc/caspian/fabric/agent/logs/agent.log <==
[2024-01-15 14:35:12] INFO: Fabric agent started on 10.42.1.15
[2024-01-15 14:36:01] ERROR: Failed to register with orchestrator at 10.42.0.5:8443 - retrying in 30s
[2024-01-15 14:36:31] INFO: Successfully registered with orchestrator

Jan 15 14:37:22 ecs-node-02 storageos[4521]: ERROR: vpool-001 health check failed - 2 replicas unavailable
Jan 15 14:37:45 ecs-node-02 caspian[5847]: INFO: Rebalancing initiated for bucket redistribution

Jan 15 14:38:10 ecs-node-01 cassandra[3294]: ERROR [StorageProxy] Read timeout from replica 10.42.1.18 after 5000ms
Jan 15 14:38:22 ecs-node-01 cassandra[3294]: EXCEPTION [CassandraDaemon] java.lang.OutOfMemoryError: Java heap space
```

!!! warning "Common errors"
    **`tail: cannot open '/var/log/ecs/*.log' for reading: No such file or directory`** — Verify ECS is installed and running with `systemctl status storageos`, then check actual log path with `find /var/log -name "*ecs*" -o -name "*data*service*"`.
    **`Unit cassandra.service could not be found.`** — Confirm Cassandra is installed and enabled with `systemctl list-units --type=service | grep cassandra`, or use the correct service name for your ECS version.
    **`Permission denied`** — Run commands with `sudo` or ensure your user is in the `storageos` or `caspian` group with `groups $USER`.
---

## See also

- [ECS — Common Issues](../common-issues/)
- [ECS — Escalation](../escalation/)
- [ECS — Health Checks](../../operations/health-checks/)

## Verify resolution

- `GET /vdc/nodes` returns all nodes with `nodestatus: GOOD`
- `GET /vdc/alerts` returns empty or only previously acknowledged alerts
- `aws s3api head-bucket --bucket <bucket> $PROFILE` returns HTTP 200 (no 403 or 500 errors)
- `GET /vdc/geo-replication/status` shows replication lag is stable or decreasing
- `/opt/storageos/tools/nodetool status` shows all nodes as `UN` (Up/Normal) on the affected node
- `systemctl is-active storageos && systemctl is-active caspian` returns `active` on all cluster nodes
