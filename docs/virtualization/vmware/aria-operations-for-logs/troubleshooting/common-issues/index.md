# Aria Operations for Logs — Common Issues

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
```text
┌────────────────────────────── Aria Operations for Logs — Common Issues ───────────────────────────────┐
│                                                                                                       │
│  Common vRLI issues: disk full, missing sources, alert failures, LDAP auth errors.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Ingestion Issues               │  │            Authentication Issues            │   │
│   │      Source not sending: check firewall      │  │     LDAP auth fail: bind account locked     │   │
│   │       Drop rate high: disk nearly full       │  │      SSO fail: cert mismatch vIDM/vRLI      │   │
│   │      ESXi logs missing: syslog not set       │  │       Login loop: check SAML assertion      │   │
│   │      High ingest lag: worker overloaded      │  │       Local admin: password forgotten       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Check disk first; full disk stops ingestion and can corrupt the vRLI index.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Alert and Cluster Issues           │  │                 Quick Fixes                 │   │
│   │       Alert not firing: check disabled       │  │     Disk full: archive + purge old data     │   │
│   │       Webhook 500: target URL changed        │  │     Source missing: check syslog config     │   │
│   │        Worker disconnected: NTP skew         │  │      LDAP: reset bind account password      │   │
│   │       Cluster split: network partition       │  │         Alert: re-enable + test fire        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI appliance · /storage disk · ESXi syslog config · AD/LDAP · vIDM · firewall                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Drop rate         = Events discarded; spikes when disk full or ingest rate exceeds capacity          │
│  Disk full         = /storage partition fills with log index; causes ingestion to stop                │
│  syslog not set    = ESXi syslog.global.logHost not configured or pointing to wrong host              │
│  Bind account lock = LDAP service account locked in AD; vRLI cannot authenticate users                │
│  SAML loop         = Browser redirects to vIDM repeatedly; check cert SAN and clock sync              │
│  Alert disabled    = Imported or upgraded alerts may be disabled; manually re-enable                  │
│  Webhook 500       = HTTP error from alert target; update URL or check target service                 │
│  NTP skew          = Time difference between vRLI nodes breaks cluster consensus                      │
│  Cluster split     = Network partition causing master and worker to lose contact                      │
│  Archive + purge   = Export logs to NFS then reduce retention period to free disk                     │
│  Ingest lag        = Events delayed; add worker node or reduce ingest sources                         │
│  Worker overloaded = Worker CPU/RAM at limit; scale out by adding another worker VM                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
