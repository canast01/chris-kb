---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# PowerStore — Common Issues

<div class="kb-summary">
Common Issues reference covering Quick Reference, Host Connectivity Issues, Replication Issues, Performance Issues, Capacity Issues and 2 more sections.

*Applies to: PowerStore 3.x*
</div>
![PowerStore — Common Issues](../../../../assets/storage-dell-powerstore-troubleshooting-common-issues.svg)

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
quick_reference: "Quick Reference" {shape: rectangle}
host_connectivity_issues: "Host Connectivity Issues" {shape: rectangle}
replication_issues: "Replication Issues" {shape: rectangle}
performance_issues: "Performance Issues" {shape: rectangle}
capacity_issues: "Capacity Issues" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> quick_reference: investigate
symptom -> host_connectivity_issues: investigate
symptom -> replication_issues: investigate
symptom -> performance_issues: investigate
symptom -> capacity_issues: investigate
diagnostic_flow -> resolution
quick_reference -> resolution
host_connectivity_issues -> resolution
replication_issues -> resolution
performance_issues -> resolution
capacity_issues -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "See Quick Reference —\nAlert: drive fault / pool degraded" {shape: rectangle}
R2: "See Management Plane Issues —\nPowerStore Manager Inaccessible" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "See Host Connectivity —\nFC Host Cannot See Volumes" {shape: rectangle}
R4: "See Host Connectivity —\niSCSI Host Cannot Connect" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "See Replication Issues —\nReplication Session in Failed State" {shape: rectangle}
R6: "See Replication Issues —\nMetro Volume Link Down" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "See Quick Reference —\nNAS server offline" {shape: rectangle}
R8: "See Host Connectivity —\nMultipath Not Working" {shape: rectangle}
D5: "D5" {shape: rectangle}
R9: "See Capacity Issues —\nPool Approaching Full Capacity" {shape: rectangle}
R10: "See Snapshot Failures —\nSnapshot schedule failures" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "B4" {shape: rectangle}
B5: "B5" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
D4 -> R7
D4 -> R8
D5 -> R9
D5 -> R10
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Quick Reference

| Symptom | Likely Cause | First Action |
|---|---|---|
| Host cannot see volumes after provisioning | Host object has wrong initiators, or zoning is incomplete | Verify initiators; check SAN zone; rescan storage on host |
| Replication session shows `Failed` state | Network connectivity lost to remote system, or auth failure | Check WAN/firewall; verify remote system credentials; check replication port 443 |
| Volume snapshot failed | Pool capacity above 90%; or too many concurrent snapshots | Check pool utilisation; reduce snapshot frequency; expand capacity |
| NAS server offline | Node fault; NAS server auto-failed-over | Check node health; confirm NAS server current node |
| Metro Volume link down | Inter-site network loss; mediator unreachable | Check inter-site network; check mediator VM status; be prepared to promote secondary |
| PowerStore Manager inaccessible | Management node restart; certificate error; network issue | Try the peer node management IP; check network connectivity |
| Alert: drive fault | NVMe SSD failure | Confirm in hardware view; open Dell case for drive replacement |
| Alert: pool degraded | Drive failure or reconstruction in progress | Check drive health; monitor reconstruction; verify pool state |
| Performance degradation | Workload spike; workload imbalance; DRR inefficiency | Check performance metrics; review per-volume IOPS/latency; check if deduplication is being bypassed |
| iSCSI sessions not connecting | iSCSI network not reachable; CHAP credentials mismatch | Check iSCSI VLAN; verify CHAP credentials match both sides |
| Certificate expired | Management certificate past expiry | Renew and import certificate; see [Encryption](../security/encryption.md) |
| SupportAssist shows disconnected | Proxy blocking outbound HTTPS; ESRS service down | Check proxy for `esrs3.emc.com:443`; restart SupportAssist from Manager UI |

## Host Connectivity Issues

### FC Host Cannot See Volumes

```bash
# Step 1: Verify the host object has the correct initiator WWNs
curl -k -X GET "https://<mgmt-ip>/api/rest/host_initiator?host_id=<host-id>&select=port_name,port_type" \
  -H "DELL-EMC-TOKEN: <token>"

# Compare with what the host actually reports:
# ESXi: esxcli storage core adapter list | grep fc
# Linux: cat /sys/class/fc_host/host*/port_name

# Step 2: Verify volume is mapped to the correct host or host group
curl -k -X GET "https://<mgmt-ip>/api/rest/host_volume_mapping?volume_id=<volume-id>" \
  -H "DELL-EMC-TOKEN: <token>"

# Step 3: Check SAN zoning (on the FC switch)
# Brocade: switch:admin> zoneshow | grep <host-wwn>
# Cisco MDS: switch# show zoneset active | include <host-wwn>

# Step 4: On ESXi — rescan storage after confirming zoning is correct
esxcli storage core adapter rescan --all
```


```text title="Expected output"
{
  "entries": [
    {
      "id": "host_initiator_1",
      "port_name": "50:00:14:40:5a:2b:c1:e3",
      "port_type": "FC"
    },
    {
      "id": "host_initiator_2",
      "port_name": "50:00:14:40:5a:2b:c1:e4",
      "port_type": "FC"
    }
  ]
}

{
  "entries": [
    {
      "id": "host_volume_mapping_1",
      "volume_id": "vol-0a1b2c3d",
      "host_id": "host-prod-01",
      "lun": 0
    }
  ]
}

zone: ZONE_ESXi_Prod_01
  members:
    50:00:14:40:5a:2b:c1:e3
    50:00:09:73:8a:4f:d2:b1

HBA Port 1 (vmhba1) rescan started.
HBA Port 2 (vmhba2) rescan started.
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to the curl command to skip SSL verification, or import the PowerStore management certificate into your system's trusted store.
    **`HTTP/1.1 401 Unauthorized`** — Verify the DELL-EMC-TOKEN is valid and not expired by re-authenticating with the PowerStore API using your credentials.
    **`zone: ZONE_ESXi_Prod_01 not found`** — Confirm the host WWN is spelled correctly and check that the zone exists on the active zoneset using `zoneshow` or `show zoneset active`.
### iSCSI Host Cannot Connect

```bash
# Step 1: Verify iSCSI network reachability
ping -s 8972 -M do <powerstore-iscsi-ip>   # Jumbo frame test
# If ping fails with fragmentation needed, MTU is not consistent end-to-end

# Step 2: Discover PowerStore iSCSI targets from the host
iscsiadm -m discovery -t sendtargets -p <powerstore-iscsi-ip>

# Step 3: Verify initiator IQN matches the host object in PowerStore
cat /etc/iscsi/initiatorname.iscsi
curl -k -X GET "https://<mgmt-ip>/api/rest/host_initiator?host_id=<host-id>&select=port_name" \
  -H "DELL-EMC-TOKEN: <token>"

# Step 4: Check CHAP credentials (if configured)
# Mismatch is a common cause of iSCSI session failure
iscsiadm -m session -P 3 | grep -i chap

# Step 5: Rescan iSCSI sessions after fixing the issue
iscsiadm -m session --rescan
```


```text title="Expected output"
PING 10.50.12.45 (10.50.12.45) 8972(9000) bytes of data.
8980 bytes from 10.50.12.45: icmp_seq=1 ttl=64 time=2.341 ms
8980 bytes from 10.50.12.45: icmp_seq=2 ttl=64 time=2.156 ms
8980 bytes from 10.50.12.45: icmp_seq=3 ttl=64 time=2.289 ms
--- 10.50.12.45 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 2.156/2.262/2.341/0.078 ms

10.50.12.45:3260,1 iqn.1991-05.com.dell:storage.powerstore.a1b2c3d4
10.50.12.45:3260,2 iqn.1991-05.com.dell:storage.powerstore.a1b2c3d4

InitiatorName=iqn.1993-08.org.linux-iscsi:host-esx01-5f8a9c2b

{
  "entries": [
    {
      "id": "host_init_001",
      "port_name": "iqn.1993-08.org.linux-iscsi:host-esx01-5f8a9c2b"
    }
  ]
}

Current iSCSI sessions:
sid 1: CHAP username: initiator_user
sid 2: CHAP username: initiator_user

iscsiadm: No active sessions.
```

!!! warning "Common errors"
    **`ping: sendto: Operation not permitted`** — Add `-M do` flag to enforce DF bit and verify MTU settings match across network path (typically 9000 for jumbo frames).
    **`iscsiadm: No records found`** — Verify the PowerStore iSCSI IP is reachable and the iSCSI service is running on the array; check firewall rules allowing port 3260.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification or import the PowerStore CA certificate into the host's certificate store.
### Multipath Not Working (Linux)

```bash
# Verify multipathd is running
systemctl status multipathd

# Show multipath device topology
multipath -ll

# If a path is shown as 'faulty' or 'ghost', investigate the specific path:
# - FC: check the zone for that fabric; check the target port health
# - iSCSI: check network connectivity on that iSCSI VLAN

# Check for DM-Multipath configuration matching PowerStore vendor string
grep -A 5 'DELL' /etc/multipath.conf

# Reload multipath configuration after changes
systemctl reload multipathd
```


```text title="Expected output"
● multipathd.service - Device-Mapper Multipath Daemon
     Loaded: loaded (/usr/lib/systemd/system/multipathd.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:32:18 UTC; 2 days ago
       Main PID: 2847 (multipathd)
        Tasks: 6 (limit: 4915)
       Memory: 12.3M
       CGroup: /system.slice/multipathd.service
               └─2847 /sbin/multipathd -d

mpatha (360060e80057900000057900000a0001) dm-0 DELL,PowerStore
size=2.0T features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 2:0:0:1 sdb 8:16 active ready running
| `- 3:0:0:1 sdc 8:32 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 4:0:0:1 sdd 8:48 active faulty offline
  `- 5:0:0:1 sde 8:64 active ready running

mpathb (360060e80057900000057900000a0002) dm-1 DELL,PowerStore
size=1.5T features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 2:0:1:1 sdf 8:80 active ready running
  `- 3:0:1:1 sdg 8:96 active ready running

devices {
        device {
                vendor "DELL"
                product "PowerStore"
                path_grouping_policy "group_by_prio"
                path_checker "tur"
                hardware_handler "1 alua"
                failback "immediate"
                rr_weight "priorities"
        }
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`multipathd.service is not running.`** — Run `systemctl start multipathd` and verify with `systemctl status multipathd`.
    **`No multipath devices found. Is multipathd running?`** — Ensure multipath daemon is active and FC/iSCSI initiators are properly configured; check `dmesg` for device discovery errors.
    **`grep: /etc/multipath.conf: No such file or directory`** — Create the multipath configuration file with `touch /etc/multipath.conf` or restore it from a backup, then add the DELL PowerStore device stanza.
## Replication Issues

### Replication Session in `Failed` State

```bash
# Get the replication session details and error
curl -k -X GET "https://<mgmt-ip>/api/rest/replication_session/<session-id>?select=name,state,last_sync_time,failed_reason" \
  -H "DELL-EMC-TOKEN: <token>"

# Check network connectivity to the remote system
curl -k -X GET "https://<mgmt-ip>/api/rest/remote_system?select=name,management_address,replication_interfaces" \
  -H "DELL-EMC-TOKEN: <token>"

# Test connectivity from the PowerStore to the remote management IP
# (this must be done from the PowerStore node — initiate a ping test via Manager UI or support)
# PowerStore Manager → Settings → Connectivity → Test → Remote System → Ping

# Common causes:
# - Firewall blocking port 443 between the two PowerStore management IPs
# - Remote PowerStore has had a password change and the remote system credentials need updating
# - WAN link failure between sites

# Update remote system credentials if they have changed
curl -k -X PATCH "https://<mgmt-ip>/api/rest/remote_system/<remote-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"password": "<new-remote-admin-password>"}'

# Resume the session after fixing connectivity
curl -k -X POST "https://<mgmt-ip>/api/rest/replication_session/<session-id>/resume" \
  -H "DELL-EMC-TOKEN: <token>"
```


```text title="Expected output"
{
  "id": "repl_sess_12345",
  "name": "prod-to-dr-sync",
  "state": "paused",
  "last_sync_time": "2024-01-15T14:32:18Z",
  "failed_reason": "Remote system unreachable"
}
{
  "id": "remote_sys_67890",
  "name": "dr-powerstore-01",
  "management_address": "192.168.100.50",
  "replication_interfaces": [
    {
      "ip_address": "10.20.30.40",
      "gateway": "10.20.30.1",
      "netmask": "255.255.255.0"
    }
  ]
}
{
  "id": "remote_sys_67890",
  "password": "***",
  "last_updated": "2024-01-15T15:47:22Z"
}
{
  "id": "repl_sess_12345",
  "state": "running",
  "resumed_at": "2024-01-15T15:48:05Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to bypass certificate verification, or import the PowerStore management certificate into your system's CA bundle.
    **`{"error_code": 401, "message": "Invalid or expired token"}`** — Regenerate the DELL-EMC-TOKEN by re-authenticating to the PowerStore management API and update the token in your request headers.
    **`{"error_code": 404, "message": "Remote system not found"}`** — Verify the `<remote-id>` value matches an existing remote system by listing all remote systems with `curl -k -X GET "https://<mgmt-ip>/api/rest/remote_system" -H "DELL-EMC-TOKEN: <token>"`.
### Metro Volume Link Down

```bash
# Check Metro Volume session state
curl -k -X GET "https://<mgmt-ip>/api/rest/replication_session?select=name,state,sync_state" \
  -H "DELL-EMC-TOKEN: <token>"

# Expected states during failure:
# state=Paused, sync_state=Unknown → site partition — both sites waiting for mediator verdict

# Check mediator reachability from both sites
# Mediator port: TCP 6666
nc -zv <mediator-ip> 6666   # Run from both sites

# If mediator is unreachable from both sites:
# DO NOT manually promote — both sites may attempt to resume simultaneously causing a split-brain
# Resolve network issue first, or contact Dell Support

# If mediator is reachable from only one site:
# The mediator will promote that site automatically
# If automatic promotion has not occurred within 5 minutes, check mediator VM health

# Manual promotion (only if mediator is not performing automatic failover):
# On the surviving secondary PowerStore:
curl -k -X POST "https://<secondary-mgmt-ip>/api/rest/replication_session/<session-id>/promote" \
  -H "DELL-EMC-TOKEN: <token>"
```


```text title="Expected output"
{
  "entries": [
    {
      "id": "repl_sess_001",
      "name": "metro_vol_prod_01",
      "state": "Paused",
      "sync_state": "Unknown"
    },
    {
      "id": "repl_sess_002",
      "name": "metro_vol_prod_02",
      "state": "Paused",
      "sync_state": "Unknown"
    }
  ]
}
Connection to 192.168.50.45 6666 port [tcp/*] succeeded!
Connection to 192.168.50.45 6666 port [tcp/*] succeeded!
{
  "id": "repl_sess_001",
  "state": "Active",
  "sync_state": "Synchronized"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to bypass certificate verification, or import the PowerStore management certificate into your system trust store.
    **`Connection to <mediator-ip> 6666 port [tcp/*] failed!`** — Verify mediator VM is running and network connectivity exists; check firewall rules allow TCP 6666 between PowerStore sites and mediator.
    **`{"error_code":"REPL_SESSION_NOT_FOUND","message":"Session <session-id> not found"}`** — Confirm the session ID is correct by re-running the GET query to list all replication sessions and their IDs.
## Performance Issues

### High Latency

```bash
# Get per-volume performance metrics via REST API
curl -k -X GET "https://<mgmt-ip>/api/rest/volume/<volume-id>/query_metrics" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "entity": "volume",
    "entity_id": "<volume-id>",
    "metrics": ["avg_latency", "read_iops", "write_iops", "read_bandwidth", "write_bandwidth"],
    "interval": "last_1_hour"
  }'

# Check if the pool is oversubscribed
curl -k -X GET "https://<mgmt-ip>/api/rest/pool?select=name,percent_used,size_used,size_total" \
  -H "DELL-EMC-TOKEN: <token>"

# Common causes of high latency:
# - Pool utilisation above 85% (write performance degrades as pool fills)
# - NVDIMM destage backpressure (check for 'destage' related alerts)
# - Workload spike (identify the top I/O consuming volumes)
# - Deduplication disabled for a workload that would benefit from it
```


```text title="Expected output"
{
  "metrics": [
    {
      "timestamp": "2024-01-15T14:32:00Z",
      "avg_latency": 4.2,
      "read_iops": 8420,
      "write_iops": 3150,
      "read_bandwidth": 267.8,
      "write_bandwidth": 89.4
    },
    {
      "timestamp": "2024-01-15T14:31:00Z",
      "avg_latency": 3.8,
      "read_iops": 7890,
      "write_iops": 2980,
      "read_bandwidth": 251.2,
      "write_bandwidth": 84.6
    }
  ]
}

{
  "entries": [
    {
      "id": "pool_1a2b3c4d",
      "name": "SSD_Pool_01",
      "percent_used": 78.4,
      "size_used": 15.6,
      "size_total": 19.9
    },
    {
      "id": "pool_2e5f6g7h",
      "name": "SSD_Pool_02",
      "percent_used": 92.1,
      "size_used": 46.2,
      "size_total": 50.3
    },
    {
      "id": "pool_3i8j9k0l",
      "name": "Hybrid_Pool_03",
      "percent_used": 68.9,
      "size_used": 27.5,
      "size_total": 39.9
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification (already present in the example, but ensure it's not removed in production use).
    **`{"error": "Unauthorized", "error_code": "UNAUTHENTICATED"}`** — Verify the DELL-EMC-TOKEN is valid and not expired by re-authenticating against the management IP.
    **`curl: (7) Failed to connect to <mgmt-ip> port 443: Connection refused`** — Confirm the management IP is reachable and the REST API service is running with `ping <mgmt-ip>` and check array status.
### Data Reduction Ratio Below Expectation

```bash
# Check DRR per volume group
curl -k -X GET "https://<mgmt-ip>/api/rest/volume_group?select=name,data_reduction_ratio" \
  -H "DELL-EMC-TOKEN: <token>"

# Common causes:
# - Volume is storing pre-encrypted data (backup data, DB with TDE)
# - Volume is storing pre-compressed media (video, compressed archives)
# - Volume has deduplication explicitly disabled

# Check if deduplication is disabled for a volume group
curl -k -X GET "https://<mgmt-ip>/api/rest/volume_group/<vg-id>?select=name,is_replication_destination,protection_policy_id" \
  -H "DELL-EMC-TOKEN: <token>"
```


```text title="Expected output"
{
  "entries": [
    {
      "id": "vg_12345abc",
      "name": "prod-db-vg",
      "data_reduction_ratio": 1.2
    },
    {
      "id": "vg_67890def",
      "name": "backup-vg",
      "data_reduction_ratio": 1.0
    },
    {
      "id": "vg_11223344",
      "name": "media-archive-vg",
      "data_reduction_ratio": 1.05
    }
  ]
}
{
  "id": "vg_12345abc",
  "name": "prod-db-vg",
  "is_replication_destination": false,
  "protection_policy_id": "pp_9876xyz"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to bypass SSL verification (already present in the example, but ensure it's included if removed).
    **`{"error_code":"401","message":"Unauthorized"}`** — Verify the DELL-EMC-TOKEN is valid and not expired by requesting a fresh token from the management API.
    **`curl: (7) Failed to connect to <mgmt-ip> port 443: Connection refused`** — Confirm the management IP is correct and reachable on port 443 using `ping` or `nc -zv <mgmt-ip> 443`.
## Capacity Issues

### Pool Approaching Full Capacity

```bash
# Identify the most space-consuming volumes
curl -k -X GET "https://<mgmt-ip>/api/rest/volume?select=name,size,size_used,type&order=size_used desc&limit=20" \
  -H "DELL-EMC-TOKEN: <token>"

# Check for large manual snapshots consuming space
curl -k -X GET "https://<mgmt-ip>/api/rest/volume_snapshot?select=name,size,creation_timestamp&order=size desc&limit=20" \
  -H "DELL-EMC-TOKEN: <token>"

# Emergency options if pool is critically full (above 90%):
# 1. Delete unnecessary manual snapshots
# 2. Delete unused cloned volumes
# 3. Reclaim space from over-provisioned thin volumes (host-side: zero the free space; let array dedup/compress)
# 4. Expand the pool by adding drive enclosures (requires hardware; schedule with Dell)
# 5. Migrate volumes to a less-full pool or appliance (if cluster has multiple appliances)
```


```text title="Expected output"
{
  "entries": [
    {
      "id": "vol-00a1b2c3d4e5f6g7",
      "name": "prod-db-primary",
      "size": 5368709120,
      "size_used": 4831838208,
      "type": "Primary"
    },
    {
      "id": "vol-00a1b2c3d4e5f6g8",
      "name": "backup-archive-2024",
      "size": 2147483648,
      "size_used": 2089582592,
      "type": "Primary"
    },
    {
      "id": "vol-00a1b2c3d4e5f6g9",
      "name": "dev-test-clone",
      "size": 1099511627776,
      "size_used": 987654321,
      "type": "Clone"
    },
    {
      "id": "vol-00a1b2c3d4e5f6ga",
      "name": "analytics-staging",
      "size": 3298534883328,
      "size_used": 2684354560,
      "type": "Primary"
    }
  ]
}
{
  "entries": [
    {
      "id": "snap-f7e6d5c4b3a29180",
      "name": "prod-db-primary.snap.20240115-0200",
      "size": 536870912,
      "creation_timestamp": "2024-01-15T02:00:00Z"
    },
    {
      "id": "snap-f7e6d5c4b3a29181",
      "name": "backup-archive-2024.snap.20240114-2300",
      "size": 429496729,
      "creation_timestamp": "2024-01-14T23:00:00Z"
    },
    {
      "id": "snap-f7e6d5c4b3a29182",
      "name": "dev-test-clone.snap.20240110-1500",
      "size": 268435456,
      "creation_timestamp": "2024-01-10T15:00:00Z"
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to bypass SSL verification, or import the PowerStore management certificate into your system's CA bundle.
    **`{"error_code":"401","message":"Invalid or expired token"}`** — Regenerate the DELL-EMC-TOKEN via the PowerStore management UI (Settings > Security > API Tokens) and ensure it has not exceeded its expiration window.
    **`curl: (7) Failed to connect to <mgmt-ip> port 443: Connection refused`** — Verify the management IP is correct and reachable with `ping <mgmt-ip>`, and confirm the PowerStore management service is running with `ssh <mgmt-ip> systemctl status rest-server`.
## Snapshot Failures

```bash
# Check for snapshot schedule failures
curl -k -X GET "https://<mgmt-ip>/api/rest/job?type=snapshot&state=failed&order=start_time desc&limit=10" \
  -H "DELL-EMC-TOKEN: <token>"

# Common causes:
# - Pool utilisation above the snapshot reserve threshold
# - Too many concurrent snapshot jobs (schedule conflict)
# - Protection policy misconfigured

# Check snapshot count per volume (too many snapshots can slow performance)
curl -k -X GET "https://<mgmt-ip>/api/rest/volume_snapshot?select=volume_id&volume_id=<volume-id>" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))"
# If snapshot count is very high (>100 per volume), review retention policy
```


```text title="Expected output"
{
  "entries": [
    {
      "id": "job-5847291",
      "type": "snapshot",
      "state": "failed",
      "start_time": "2024-01-15T14:32:18Z",
      "end_time": "2024-01-15T14:33:22Z",
      "error_code": "POOL_THRESHOLD_EXCEEDED",
      "error_message": "Pool utilization 94% exceeds snapshot reserve threshold of 90%"
    },
    {
      "id": "job-5847190",
      "type": "snapshot",
      "state": "failed",
      "start_time": "2024-01-15T13:15:47Z",
      "end_time": "2024-01-15T13:16:05Z",
      "error_code": "CONCURRENT_JOB_LIMIT",
      "error_message": "Maximum concurrent snapshot jobs (8) reached"
    },
    {
      "id": "job-5847089",
      "type": "snapshot",
      "state": "failed",
      "start_time": "2024-01-15T12:00:33Z",
      "error_code": "POLICY_CONFIG_ERROR",
      "error_message": "Protection policy 'daily-backup' references deleted replication target"
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 47
}
287
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to the curl command to skip SSL verification, or import the management node's certificate into your CA bundle.
    **`{"error_code":"INVALID_TOKEN","message":"Authentication token expired or invalid"}`** — Regenerate the API token in the PowerStore management console and update the DELL-EMC-TOKEN header value.
    **`jq: command not found`** — Install `jq` package (`apt install jq` or `yum install jq`) or use the provided `python3 -c` JSON parser instead.
## Management Plane Issues

### PowerStore Manager Inaccessible

1. Try the alternate management IP (if cluster has multiple appliances)
2. Try the direct node management IP for Node A and Node B individually
3. Check if HTTPS port 443 is reachable: `nc -zv <mgmt-ip> 443`
4. If the management node is restarting (e.g., post-upgrade), wait 5 minutes and retry
5. Check the SupportAssist call-home — if the array has triggered an alert, Dell may already be aware

### REST API Returns 401 Unauthorized

```bash
# Common causes:
# - Token has expired (sessions expire after idle timeout)
# - Wrong credentials
# - Account is locked out

# Check if the account is locked (too many failed attempts)
curl -k -X GET "https://<mgmt-ip>/api/rest/user/local?select=name,is_locked" \
  -H "DELL-EMC-TOKEN: <admin-token>"

# Unlock a locked account
curl -k -X PATCH "https://<mgmt-ip>/api/rest/user/local/<user-id>" \
  -H "DELL-EMC-TOKEN: <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"lock_status": "Unlocked"}'

# Re-authenticate to get a fresh token
TOKEN=$(curl -ks -X POST "https://<mgmt-ip>/api/rest/login_session" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' \
  | jq -r '.token')
```


```text title="Expected output"
{
  "entries": [
    {
      "id": "user-001",
      "name": "admin",
      "is_locked": false
    },
    {
      "id": "user-002",
      "name": "readonly",
      "is_locked": false
    }
  ]
}
{
  "id": "user-001",
  "name": "admin",
  "lock_status": "Unlocked",
  "last_modified": "2024-01-15T09:42:33Z"
}
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwNTMzODk1MywiaWF0IjoxNzA1MzM4MzUzfQ.kR9mN2pQxL7vZ8wJ4sT6uY3aB5cD1eF9gH2jK4mN6oP
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification, or import the PowerStore management certificate into your system's CA bundle.
    **`jq: parse error: Invalid numeric literal at line 1 column 10`** — Verify the API response is valid JSON by removing the `jq` filter temporarily and checking the raw response for error messages.
    **`{"error":"Invalid or expired token"}`** — Re-authenticate using the login endpoint to obtain a fresh token, as the current token has exceeded its idle timeout or session limit.
---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Powerstore — Diagnostics](../diagnostics/)
- [Powerstore — Escalation](../escalation/)
- [Powerstore — Health Checks](../../operations/health-checks/)
