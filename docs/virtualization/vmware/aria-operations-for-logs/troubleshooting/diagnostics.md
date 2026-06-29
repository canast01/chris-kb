---
tags:
  - aria-logs
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Operations for Logs — Diagnostics

<div class="kb-summary">
Aria Operations for Logs (vRLI) diagnostic commands: inspect runtime.log and ingestion.log, check cluster node health via API, diagnose Cassandra performance, test syslog agent connectivity, verify NTP, and collect the VAMI support bundle for VMware SR cases.

*Applies to: VMware Aria Operations for Logs 8.x (vRealize Log Insight)*
</div>
![Aria Operations for Logs — Diagnostics](../../../../assets/virtualization-vmware-aria-operations-for-logs-troubleshooti.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "Check liagentd on agent host\nsystemctl status liagentd" {shape: rectangle}
D: "tail -f /var/log/loginsight/runtime.log\nLook for Java exceptions" {shape: rectangle}
E: "nodetool compactionstats\nCheck Cassandra compaction" {shape: rectangle}
F: "Check /var/log/loginsight/alerts.log\nCheck notification config" {shape: rectangle}
G: "G" {shape: rectangle}
H: "systemctl start liagentd\nCheck liagent.log for error" {shape: rectangle}
I: "nc -zv vRLI-IP 9543\nTest port reachability" {shape: rectangle}
J: "GET /api/v1/cluster/nodes\nCheck cluster node state" {shape: rectangle}
K: "K" {shape: rectangle}
L: "Wait for completion\n15-30 min; monitor nodetool" {shape: rectangle}
M: "nodetool info | grep Heap\nHeap > 90% = problem" {shape: rectangle}
N: "Check ingestion.log\nfor parse failures or drops" {shape: rectangle}
O: "Collect VAMI support bundle\nUpload to VMware SR" {shape: rectangle}
A: "vRLI Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
G -> H
G -> I
D -> J
K -> L
K -> M
I -> N
J -> N
F -> N
H -> N
L -> N
M -> N
N -> O
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_appliance_health: "Step 1 — Check appliance health" {shape: rectangle}
step_2_check_cluster_node_health: "Step 2 — Check cluster node health" {shape: rectangle}
step_3_check_syslog_and_ingestion: "Step 3 — Check syslog and ingestion" {shape: rectangle}
step_4_check_cassandra_performance: "Step 4 — Check Cassandra performance" {shape: rectangle}
step_5_check_agent_liagent_on_source: "Step 5 — Check agent (liagent) on source hosts" {shape: rectangle}
step_6_check_ntp: "Step 6 — Check NTP" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_appliance_health: investigate
symptom -> step_2_check_cluster_node_health: investigate
symptom -> step_3_check_syslog_and_ingestion: investigate
symptom -> step_4_check_cassandra_performance: investigate
symptom -> step_5_check_agent_liagent_on_source: investigate
symptom -> step_6_check_ntp: investigate
step_1_check_appliance_health -> resolution
step_2_check_cluster_node_health -> resolution
step_3_check_syslog_and_ingestion -> resolution
step_4_check_cassandra_performance -> resolution
step_5_check_agent_liagent_on_source -> resolution
step_6_check_ntp -> resolution
```

## Before you begin

- **Access:** SSH to the vRLI appliance as `admin`; VAMI access at `https://<vRLI-IP>:5480`; vRLI admin UI access
- **Gather first:** the symptom (no ingestion, UI error, slow search, alert not firing), the time the issue started, and the current EPS from Admin → System Monitor
- **Scope:** confirm whether the issue affects a single agent source, a specific content pack, or all ingestion
- **NTP:** clock skew between the vRLI appliance and source hosts causes event timestamp mismatches that look like missing data — always verify NTP first

---

## Step 1 — Check appliance health

```bash
# SSH to vRLI appliance
ssh admin@<vRLI-IP>

# Watch main application log in real time
tail -f /var/log/loginsight/runtime.log

# Search for errors across all core logs
grep -i "error\|exception\|fail" /var/log/loginsight/runtime.log | tail -100
grep -i "error\|drop"           /var/log/loginsight/ingestion.log | tail -50
grep -i "slow\|timeout\|error"  /var/log/loginsight/query.log | tail -50

# Check disk usage — vRLI stops accepting events if disk exceeds threshold
df -h /storage /dev/sdb
# Expected: < 80% on storage partition; > 80% = ingestion pauses
```


```text title="Expected output"
admin@vRLI-01's password: 
Last login: Wed Jan 15 14:32:18 2025 from 10.50.12.44

2025-01-15T14:35:22.441Z [main] ERROR com.vmware.loginsight.core.IndexWriter - Failed to write segment to disk: IOException on /storage/index/segment_2025_01_15_14_35
2025-01-15T14:35:45.892Z [ingestion] WARN  com.vmware.loginsight.ingestion.Parser - Dropped 1247 events due to queue overflow
2025-01-15T14:36:01.334Z [query] ERROR com.vmware.loginsight.query.Aggregator - Query timeout after 30000ms on datasource prod-cluster
2025-01-15T14:36:15.221Z [main] ERROR com.vmware.loginsight.core.EventProcessor - Connection refused to syslog relay at 10.50.8.99:514

Filesystem     Size  Used Avail Use% Mounted on
/storage       500G  425G   75G  85% /storage
/dev/sdb       200G  180G   20G  90% /dev/sdb
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify SSH key is loaded with `ssh-add` or use password authentication; confirm admin user exists on vRLI appliance.
    **`tail: cannot open '/var/log/loginsight/runtime.log' for reading: No such file or directory`** — SSH session may have disconnected or log directory path differs; verify correct vRLI IP and check `/var/log/loginsight/` directory exists with `ls -la`.
    **`Filesystem /storage is 90% full — ingestion paused`** — Clear old log data with vRLI UI (Administration > Retention) or expand storage partition; ingestion resumes automatically once usage drops below 80%.
---

## Step 2 — Check cluster node health

```bash
# Via REST API (run from any host that can reach vRLI)
curl -sk -u 'admin:<password>' \
  "https://<vRLI-IP>/api/v1/cluster/nodes" | \
  python3 -m json.tool
# Expected: each node shows "state": "ACTIVE"

# Check ingestion statistics
curl -sk -u 'admin:<password>' \
  "https://<vRLI-IP>/api/v2/cluster/stats" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('EPS:', d.get('eventsIngested'), 'Disk%:', d.get('diskUsagePercent'))"
# Expected: eventsIngested > 0 if senders are active

# Via UI: Admin → Cluster (top navigation)
# Each node shows: Status, Role (master/worker), Disk, CPU, Memory
```


```text title="Expected output"
{
  "nodes": [
    {
      "nodeId": "node-1",
      "hostname": "vRLI-master-01.corp.local",
      "ipAddress": "192.168.1.45",
      "state": "ACTIVE",
      "role": "MASTER",
      "version": "8.14.0.21234567"
    },
    {
      "nodeId": "node-2",
      "hostname": "vRLI-worker-01.corp.local",
      "ipAddress": "192.168.1.46",
      "state": "ACTIVE",
      "role": "WORKER",
      "version": "8.14.0.21234567"
    },
    {
      "nodeId": "node-3",
      "hostname": "vRLI-worker-02.corp.local",
      "ipAddress": "192.168.1.47",
      "state": "ACTIVE",
      "role": "WORKER",
      "version": "8.14.0.21234567"
    }
  ]
}
EPS: 487293 Disk%: 68.4
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the vRLI CA certificate into your system trust store.
    **`curl: (7) Failed to connect to <vRLI-IP> port 443: Connection refused`** — Verify the vRLI appliance is running and accessible on port 443 from your host using `telnet <vRLI-IP> 443`.
    **`{"error":"Unauthorized","statusCode":401}`** — Confirm the admin password is correct and URL-encoded if it contains special characters; test with `curl -sk -u 'admin:password' https://<vRLI-IP>/api/v1/cluster/nodes`.
---

## Step 3 — Check syslog and ingestion

```bash
# Verify syslog listeners are running
ss -tulnp | grep -E "514|1514|9543"
# Expected: UDP/TCP 514 (syslog), TCP 1514 (structured syslog), TCP 9543 (liagent)

# Test sending a test syslog event from a source host
logger -n <vRLI-IP> -P 514 -d "test message from diagnostic $(date)"
# Then search Interactive Analytics in vRLI UI for "test message" — should appear within 30 seconds

# Check for parse failures or dropped events
grep -i "drop\|parse error\|overflow\|reject" /var/log/loginsight/ingestion.log | tail -50
# Problem: "Dropping event" or "parse error" lines with high count
```


```text title="Expected output"
tcp        0      0 0.0.0.0:9543           0.0.0.0:*               LISTEN      12847/liagent
udp        0      0 0.0.0.0:514            0.0.0.0:*               12891/rsyslogd
tcp        0      0 0.0.0.0:1514           0.0.0.0:*               LISTEN      12847/liagent
2024-01-15T09:42:33.847Z [ingestion-worker-3] INFO: Processed 1247 events in 2.3s
2024-01-15T09:42:45.102Z [ingestion-worker-1] Dropping event from 192.168.1.45: buffer overflow on queue-syslog-udp
2024-01-15T09:42:51.334Z [ingestion-worker-2] Parse error: unrecognized syslog format from 10.20.30.40 — skipping malformed header
2024-01-15T09:43:02.556Z [ingestion-worker-4] INFO: Processed 892 events in 1.8s
2024-01-15T09:43:15.778Z [ingestion-worker-1] Dropping event from 192.168.1.50: buffer overflow on queue-syslog-udp
2024-01-15T09:43:22.441Z [ingestion-worker-3] Parse error: timestamp mismatch on syslog from 172.16.5.12
```

!!! warning "Common errors"
    **`Dropping event from <IP>: buffer overflow on queue-syslog-udp`** — Increase the UDP buffer size by running `sysctl -w net.core.rmem_max=134217728` and `sysctl -w net.core.rmem_default=134217728`, then restart rsyslogd.
    **`Parse error: unrecognized syslog format`** — Verify the source host is sending RFC3164 or RFC5424 compliant syslog format and check the syslog configuration on the source with `cat /etc/rsyslog.conf | grep -A5 "^*.* @"`.
---

## Step 4 — Check Cassandra performance

Slow search queries in vRLI are commonly caused by Cassandra compaction or heap saturation.

```bash
# SSH to vRLI appliance; Cassandra runs locally
ssh admin@<vRLI-IP>

# Check if Cassandra compaction is active (compaction = temporary slowness)
nodetool compactionstats
# Expected: 0 pending compactions = good
# If compaction is active: wait 15–30 minutes before further investigation

# Check Cassandra heap usage
nodetool info | grep -i "heap"
# Expected: Heap Memory (Used/Max) < 90%
# > 90% heap = queries slow; > 95% = OOM risk; requires memory increase or GC tuning

# Check recent Cassandra errors
grep -i "error\|warn\|exception" /var/log/loginsight/cassandra/system.log | tail -50
```


```text title="Expected output"
admin@vRLI-IP's password: 
CompactionStats:
pending tasks: 0
Active compactions:
compaction type keyspace table completed total unit progress
Compaction of each table shows ~0 MB of 0 MB complete

Heap Memory (Used/Max) : 4.27 GB / 8 GB
Heap Memory (Used/Max) : 4.27 GB / 8 GB

2024-01-15 09:23:14,521 WARN  [ScheduledTasks:1] cassandra.db.ColumnFamilyStore - Compacting large partition for system_auth/roles (1.2 GB)
2024-01-15 09:18:47,103 WARN  [GossipTasks:1] cassandra.gms.Gossiper - Not marking nodes as down due to local pause detection
2024-01-15 09:12:33,891 INFO  [main] cassandra.service.CassandraDaemon - Cassandra version: 3.11.10
2024-01-15 08:56:22,445 WARN  [ReadStage:42] cassandra.db.ReadCommand - Read timeout: 10000ms, received 1 of 3 responses
2024-01-15 08:45:11,203 WARN  [CompactionExecutor:0] cassandra.db.compaction.CompactionTask - Compaction of /var/lib/cassandra/data/loginsight/events-ka/na-1-big-Data.db produced no output
2024-01-15 08:32:05,667 ERROR [GossipTasks:2] cassandra.gms.Gossiper - Exception in thread Thread-123
```

!!! warning "Common errors"
    **`bash: nodetool: command not found`** — SSH directly to the vRLI appliance and run commands as root or use the full path `/usr/lib/cassandra/bin/nodetool`.
    **`Connection refused`** — Verify Cassandra is running with `systemctl status cassandra` and that port 7199 is not blocked by firewall rules.
    **`Permission denied`** — Run the nodetool commands with `sudo` or switch to the cassandra user with `sudo su - cassandra` before executing.
---

## Step 5 — Check agent (liagent) on source hosts

For sources using the vRLI agent rather than syslog:

```bash
# On the agent host
systemctl status liagentd
# Expected: active (running)

# Check agent log for errors
tail -100 /var/log/vmware/loginsight-agent/liagent.log | grep -i "error\|connect\|ssl\|fail"
# Common errors:
#   "connection refused" → vRLI port 9543 not reachable
#   "SSL handshake failed" → certificate mismatch or expired cert on vRLI
#   "authentication failed" → agent key no longer valid

# Test connectivity from agent to vRLI
nc -zv <vRLI-IP> 9543
# Expected: "succeeded"

# Check agent configuration
grep -v "^#\|^$" /var/lib/loginsight-agent/liagent.ini
# Verify: hostname (the vRLI address), proto=cfapi, ssl=yes/no

# Restart agent if configuration was changed
systemctl restart liagentd
systemctl status liagentd
```


```text title="Expected output"
● liagentd.service - VMware Log Insight Agent
     Loaded: loaded (/usr/lib/systemd/system/liagentd.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2 days ago
       PID: 4521
    Tasks: 8 (limit: 4915)
   Memory: 127.3M
   CGroup: /system.slice/liagentd.service
           └─4521 /usr/lib/vmware/loginsight-agent/liagentd -c /var/lib/loginsight-agent/liagent.ini

2024-01-18 14:32:18 liagentd[4521]: INFO: Agent started successfully
2024-01-18 14:35:42 liagentd[4521]: INFO: Connected to vRLI server at 192.168.1.105:9543
2024-01-18 15:12:03 liagentd[4521]: INFO: Heartbeat sent successfully

Connection to 192.168.1.105 9543 port [tcp/*] succeeded!

hostname=192.168.1.105
port=9543
proto=cfapi
ssl=yes
agentkey=a7f2c9e1-4b8d-11ee-be56-0242ac120002
loglevel=INFO

● liagentd.service - VMware Log Insight Agent
     Loaded: loaded (/usr/lib/systemd/system/liagentd.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:45:22 UTC; 1s ago
       PID: 5103
    Tasks: 8 (limit: 4915)
   Memory: 98.7M
```

!!! warning "Common errors"
    **`nc: connect to 192.168.1.105 port 9543 (tcp) failed: Connection refused`** — Verify vRLI service is running on the target host and port 9543 is not blocked by firewall rules.
    **`ERROR: SSL handshake failed: certificate verify failed`** — Ensure the vRLI server certificate is valid and trusted, or disable SSL verification in liagent.ini if using self-signed certificates.
    **`ERROR: Authentication failed: agent key invalid or revoked`** — Regenerate the agent key in vRLI UI and update the agentkey parameter in /var/lib/loginsight-agent/liagent.ini.
---

## Step 6 — Check NTP

Clock skew between vRLI and event sources causes events to appear out of order or "missing" when searched by time range.

```bash
# On the vRLI appliance
ssh admin@<vRLI-IP>

# Check NTP sync status
chronyc tracking
# Expected: "System time" offset < 0.1 seconds; "Leap status: Normal"

# Show NTP sources
chronyc sources -v
# Expected: at least one source with "*" (currently selected); offset < 10ms

# If NTP is drifting: restart chronyd
systemctl restart chronyd
chronyc sources
```


```text title="Expected output"
admin@vrli-01.lab.local's password: 
Last login: Wed Jan 15 14:32:18 2025 from 10.20.50.100

Reference ID    : 91002F (ntp.ubuntu.com)
Stratum         : 2
Ref time (UTC)  : Wed Jan 15 14:32:15 2025
System time     : 0.000087234 seconds fast of NTP time
Frequency       : 2.341 ppm slow
Residual freq   : +0.002 ppm
Skew            : 0.012 ppm
Root delay      : 0.031250 seconds
Root dispersion : 0.015625 seconds
Update interval : 1024.0 seconds
Leap status     : Normal

MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================
^* 10.20.1.50              1      6   377   12    -0.234ms[  -0.234ms] +/-   2.341ms
^- 10.20.1.51              1      7   377   45    +1.123ms[  +1.123ms] +/-   3.012ms
^- 91.189.89.198           2      8   377   52    +5.432ms[  +5.432ms] +/-  15.234ms
^? 169.254.169.123         0      0     0     -      +0.000ms[  +0.000ms] +/-    0.000ms

(no output — command completes silently)
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================
^* 10.20.1.50              1      6   377    8    -0.156ms[  -0.156ms] +/-   2.341ms
^- 10.20.1.51              1      7   377   41    +1.087ms[  +1.087ms] +/-   3.012ms
^- 91.189.89.198           2      8   377   48    +5.398ms[  +5.398ms] +/-  15.234ms
```

!!! warning "Common errors"
    **`chronyc: Could not talk to daemon`** — Ensure chronyd service is running with `systemctl status chronyd` and check firewall rules allowing NTP (UDP 123).
    **`System time : 2.345678 seconds fast of NTP time`** — Restart chronyd with `systemctl restart chronyd` and verify NTP sources are reachable; if drift persists, manually sync with `chronyc makestep`.
---

## Step 7 — Collect VAMI support bundle for VMware SR

```bash
# Via VAMI (recommended — most complete)
# 1. Browse to https://<vRLI-IP>:5480
# 2. Navigate to: Support → Generate Support Bundle
# 3. Wait for bundle creation (3–10 minutes depending on log volume)
# 4. Download the .gz file

# Via SSH (if VAMI is unavailable)
ssh admin@<vRLI-IP>
/usr/lib/loginsight/application/bin/generate-support-bundle
# Output: /tmp/support-bundle-<timestamp>.tar.gz
scp admin@<vRLI-IP>:/tmp/support-bundle-*.tar.gz ./

# Include in the VMware SR:
# - Support bundle (.tar.gz)
# - Timeline: when the issue started, any recent changes
# - vRLI version: Admin → About
```


```text title="Expected output"
admin@vRLI-01's password: 
Generating support bundle...
Collecting system logs (this may take several minutes)...
Collecting application logs...
Collecting configuration files...
Compressing bundle...
Support bundle generated successfully: /tmp/support-bundle-20240115-143022.tar.gz
Bundle size: 487 MB
support-bundle-20240115-143022.tar.gz          100%  487MB   8.2MB/s   00:59
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify SSH credentials and that the admin user has SSH access enabled in VAMI (Admin → Access).
    **`scp: /tmp/support-bundle-*.tar.gz: No such file or directory`** — Confirm the bundle generation completed successfully by checking `/tmp/` directly with `ssh admin@<vRLI-IP> ls -lh /tmp/support-bundle-*.tar.gz`.
---

## Log locations

| Component | Path | What to look for |
|---|---|---|
| Main application | `/var/log/loginsight/runtime.log` | Java exceptions, cluster events, startup errors |
| Ingestion | `/var/log/loginsight/ingestion.log` | Dropped events, parse failures |
| Query performance | `/var/log/loginsight/query.log` | Slow queries, timeouts |
| Cassandra | `/var/log/loginsight/cassandra/system.log` | Compaction errors, GC pauses |
| Alerts | `/var/log/loginsight/alerts.log` | Alert fire/no-fire events, notification errors |
| Agent (on source host) | `/var/log/vmware/loginsight-agent/liagent.log` | Connection, SSL, auth errors |

---

## See also

- [Aria Operations for Logs — Common Issues](../common-issues/)
- [Aria Ops for Logs — Escalation](../escalation/)

## Verify resolution

- Admin → System Monitor: EPS is at or above the expected baseline for this environment
- Interactive Analytics: a test event sent via `logger` appears within 30 seconds
- `nodetool compactionstats` shows 0 pending compactions
- `ss -tulnp | grep 9543` confirms the agent listener is running
- The original symptom (missing data, slow search, alert failure) does not recur after 10 minutes of monitoring
