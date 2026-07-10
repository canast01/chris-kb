---
tags:
  - aria-logs
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Operations for Logs — Common Issues

*Applies to: VMware Aria 8.x*
![Aria Operations for Logs — Common Issues](../../../../../assets/virtualization-vmware-aria-operations-for-logs-troubleshooti.svg)

```bash
# Check ingestion stats from master node
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/stats" | \
  jq '{eventsPerSecond: .eventsIngested, diskPct: .diskUsagePercent}'

# Verify syslog listeners are running
ss -tulnp | grep -E "514|1514|9543"
# Expected: UDP 514, TCP 1514, TCP 9543 all listening
# If any port is not listening: restart the loginsight service
systemctl restart loginsight

# Test syslog reception from a source
logger -n vrli-prod-01.example.local -P 514 -d "test ingestion check"
# Then check Interactive Analytics for "test ingestion check" within 30 seconds

# Check ingestion log for parse failures or drops
grep -i "drop\|overflow\|parse error\|reject" /var/log/loginsight/ingestion.log | tail -50
```

```powershell
# Check agent service status
Get-Service "VMware Log Insight Agent"

# View agent event log
Get-EventLog -LogName Application -Source "VMware*" -Newest 50 | Format-List

# Restart agent
Restart-Service "VMware Log Insight Agent"
```
```bash
# Check Cassandra compaction — long compaction causes slow queries
ssh admin@vrli-prod-01.example.local
nodetool compactionstats

# Check Cassandra heap usage — high heap (>90%) causes query slowness
nodetool info | grep -i "heap"

# Check current query load
tail -50 /var/log/loginsight/query.log | grep -i "slow\|timeout\|error\|duration"

# Reduce query load by narrowing time ranges and adding field filters
# Use: last 1 hour instead of last 7 days when investigating active incidents
```

```text title="Expected output"
admin@vrli-prod-01.example.local's password: 
Compaction Manager
Current compaction tasks:
task type : Compaction
keyspace : loginsight
table : events
completed : 847392645120 bytes, 2156 MB/s, 39% done
remaining : 1342087564288 bytes
total : 2189480209408 bytes

Heap Memory (MB): 28672 / 32768

2024-01-15 14:23:47,891 [pool-12-thread-4] WARN  QueryExecutor - Slow query detected duration=4521ms query_id=a7f3e2c1-9d4b-11ee-b9d7-0050569e1234
2024-01-15 14:24:12,445 [pool-12-thread-8] ERROR QueryExecutor - Query timeout after 5000ms for tenant_id=prod-cluster-1
2024-01-15 14:25:33,221 [pool-12-thread-2] WARN  QueryExecutor - Slow query detected duration=3847ms query_id=b8e4f3d2-9d4b-11ee-c2e8-0050569e5678
2024-01-15 14:26:01,556 [pool-12-thread-6] ERROR QueryExecutor - Query timeout after 5000ms for tenant_id=prod-cluster-2
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify SSH credentials and that the admin user exists on the target node with `ssh-keyscan vrli-prod-01.example.local` to confirm connectivity.
    **`nodetool: command not found`** — Ensure you are in the Cassandra installation directory or add `$CASSANDRA_HOME/bin` to your PATH with `export PATH=$PATH:/opt/cassandra/bin`.
    **`tail: cannot open '/var/log/loginsight/query.log' for reading: Permission denied`** — Run the tail command with `sudo` or ensure the admin user has read permissions on the loginsight log directory.
```bash
# Check the cluster nodes via API from the master
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state}'

# SSH to the worker node and check the loginsight service
ssh admin@vrli-prod-02.example.local
systemctl status loginsight
tail -100 /var/log/loginsight/runtime.log | grep -i "join\|cluster\|error\|master"

# Test connectivity from worker to master on required ports
nc -zv vrli-prod-01.example.local 443
nc -zv vrli-prod-01.example.local 16520  # cluster internal communication port
```

```text title="Expected output"
{
  "host": "vrli-prod-01.example.local",
  "state": "MASTER"
}
{
  "host": "vrli-prod-02.example.local",
  "state": "WORKER"
}
{
  "host": "vrli-prod-03.example.local",
  "state": "WORKER"
}
● loginsight.service - VMware vRealize Log Insight
   Loaded: loaded (/etc/systemd/system/loginsight.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2 days ago
   Main PID: 4521 (java)
     CGroup: /system.slice/loginsight.service
             └─4521 /usr/lib/jvm/java-11-openjdk-11.0.18.0.10-1.el7_9.x86_64/bin/java
2024-01-15 14:32:45 vrli-prod-02 loginsight[4521]: [INFO] Cluster join initiated for node vrli-prod-02
2024-01-15 14:33:12 vrli-prod-02 loginsight[4521]: [INFO] Successfully joined cluster with master vrli-prod-01.example.local
2024-01-15 14:33:15 vrli-prod-02 loginsight[4521]: [INFO] Cluster state synchronized
Connection to vrli-prod-01.example.local 443 [tcp/https] succeeded!
Connection to vrli-prod-01.example.local 16520 [tcp/*] succeeded!
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification, or import the master's CA certificate into your system trust store.
    **`Connection refused`** — Verify the loginsight service is running on the master node with `systemctl status loginsight` and check firewall rules allow traffic on ports 443 and 16520.
    **`ssh: Could not resolve hostname vrli-prod-02.example.local: Name or service not known`** — Ensure DNS resolution is working or add the worker node IP to `/etc/hosts` on the master node.
```bash
# Verify alert is enabled
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/alerts/<alert-id>" | \
  jq '{name: .name, enabled: .enabled, numHits: .numHits}'

# Test the notification channel
curl -sk -X POST -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/notification/<channel-id>/test"

# Check the runtime log for notification delivery errors
grep -i "notification\|email\|webhook\|smtp\|fail" /var/log/loginsight/runtime.log | tail -50
```

```text title="Expected output"
{
  "name": "Critical Memory Threshold Alert",
  "enabled": true,
  "numHits": 847
}

Test notification sent successfully to channel: email-prod-alerts (ID: ch-8f2a9c1d)

2024-01-15 14:32:18,421 INFO  [NotificationService] Notification delivery successful for alert ID: alert-7b4e2f9a to recipient: ops-team@example.local
2024-01-15 14:31:45,892 WARN  [SMTPClient] SMTP connection timeout after 30s, retrying...
2024-01-15 14:31:16,334 INFO  [WebhookNotifier] Webhook POST to https://slack.example.local/hooks/alerts returned 200 OK
2024-01-15 14:30:52,167 ERROR [EmailNotifier] Failed to deliver email: javax.mail.AuthenticationFailedException: 535 5.7.8 Authentication credentials invalid
2024-01-15 14:29:33,445 INFO  [NotificationService] Channel test completed with status: SUCCESS
2024-01-15 14:28:19,771 WARN  [SMTPClient] Certificate validation disabled for SMTP host mail.example.local
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the vRLI certificate into your system CA bundle.
    **`jq: parse error: Cannot index number with string "name"`** — Verify the alert ID exists and is valid by listing alerts with `curl -sk -u 'admin:<password>' "https://vrli-prod-01.example.local/api/v2/alerts" | jq '.alerts[] | {id, name}'`.
    **`grep: /var/log/loginsight/runtime.log: No such file or directory`** — SSH into the vRLI appliance and check the correct log path with `find /var/log -name "*runtime*" -o -name "*notification*"`.
```bash
# Check NTP on the Aria Ops for Logs appliance
chronyc tracking
chronyc sources -v

# If NTP is drifting: restart chronyd and check sources
systemctl restart chronyd
chronyc sources

# Verify all cluster nodes are synced to the same NTP source
for node in vrli-prod-01 vrli-prod-02 vrli-prod-03; do
  echo -n "$node.example.local: "
  ssh admin@$node.example.local "chronyc tracking 2>/dev/null | grep 'System time'"
done
```

```text title="Expected output"
Reference ID    : 91F0B524 (ntp.ubuntu.com)
Stratum         : 2
Ref time (UTC)  : Wed Dec 13 14:32:18 2024
System time     : 0.000234567 seconds fast of NTP time
Frequency       : -12.456 ppm fast
Residual freq   : +0.123 ppm
Skew            : 0.087 ppm
Root delay      : 0.045678 seconds
Root dispersion : 0.156234 seconds
Update interval : 1024.2 seconds
Leap status     : Normal

MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================
^* 91.189.89.198              1  10   377    45   -234us[ -198us] +/-   21ms
^- 185.125.190.39             2  10   377   102   +456us[ +512us] +/-   45ms
^+ 139.162.238.205            2  10   377    67   +123us[ +145us] +/-   38ms

vrli-prod-01.example.local: System time : 0.000156789 seconds fast of NTP time
vrli-prod-02.example.local: System time : 0.000198765 seconds fast of NTP time
vrli-prod-03.example.local: System time : 0.000167234 seconds fast of NTP time
```

!!! warning "Common errors"
    **`Temporary failure in name resolution`** — Verify DNS resolution is working with `nslookup vrli-prod-01.example.local` and ensure all cluster nodes are reachable via SSH.
    **`Permission denied (publickey,password)`** — Ensure the admin SSH key is configured on all cluster nodes or use `ssh-copy-id admin@$node.example.local` to deploy your public key.
    **`Stratum : 16` or `Leap status : Not synchronised`** — Restart chronyd with `systemctl restart chronyd` and verify NTP server connectivity with `chronyc sources`.
```bash
# Confirm disk usage
df -h /var/log/loginsight

# Check if hot retention is set too long for current disk size
# Reduce retention to free space: Administration → General → Retention → reduce days

# Remove old archives from the NFS target if archiving is enabled
# Do NOT manually delete files from /var/log/loginsight — Cassandra manages this path

# If retention cannot be reduced, add a worker node with additional disk
# Workers can be added without downtime: deploy OVA → setup wizard → Join Cluster
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
B1: "Agent not sending logs" {shape: rectangle}
B2: "Ingestion rate dropped" {shape: rectangle}
B3: "Syslog source not appearing" {shape: rectangle}
B4: "Alert not firing" {shape: rectangle}
B5: "Disk usage over 80 percent" {shape: rectangle}
B6: "Worker node disconnected" {shape: rectangle}
D1: "D1" {shape: rectangle}
R1: "Restart VMware Log Insight Agent Service\n→ Ingestion Issues" {shape: rectangle}
R2: "Check Agent Config · Firewall Port 514 or 9543\n→ Ingestion Issues" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Archive and Purge Old Data · Reduce Retention\n→ Disk Usage Over 80 Percent" {shape: rectangle}
R4: "Check Worker Node Load · Add Worker VM\n→ Ingestion Issues" {shape: rectangle}
R5: "Check syslog.global.logHost on ESXi · Test logger\nCommand\n→ Ingestion Issues" {shape: rectangle}
D3: "D3" {shape: rectangle}
R6: "Re-enable Alert · Test Notification Channel\n→ Alert and Cluster Issues" {shape: rectangle}
R7: "Check Webhook URL · SMTP Connectivity\n→ Alert and Cluster Issues" {shape: rectangle}
R8: "Reduce Hot Retention · Archive to NFS · Add Worker Disk\n→ Disk Usage Over 80 Percent" {shape: rectangle}
R9: "Check NTP Skew · Verify Port 16520 · Restart\nloginsight Service\n→ Alert and Cluster Issues" {shape: rectangle}

S -> B1
S -> B2
S -> B3
S -> B4
S -> B5
S -> B6
D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
B3 -> R5
D3 -> R6
D3 -> R7
B5 -> R8
B6 -> R9
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## See also

- [Aria Operations for Logs — Diagnostics](../diagnostics/)
- [Aria Ops for Logs — Escalation](../escalation/)
- [Aria Operations for Logs — Health Checks](../../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
