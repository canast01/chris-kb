---
tags:
  - aria-operations
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Operations Common Issues
![Aria Operations Common Issues](../../../../assets/virtualization-vmware-aria-operations-troubleshooting-common.svg)

```bash
# SSH to primary node and inspect adapter state
ssh admin@vrops-prod-01.example.local
vracli adapter list --verbose

# Check the collector log for adapter-specific errors
tail -500 /data/vcops/log/collector.log | grep -i "error\|exception\|fail"

# Check per-adapter log
ls /data/vcops/log/adapters/
tail -200 /data/vcops/log/adapters/VMwareAdapter/adapter.log | grep -i "error\|auth\|connect"

# Restart the watchdog (restarts failed services automatically)
service vmware-vcops-watchdog restart
```


```text title="Expected output"
admin@vrops-prod-01.example.local's password: 
Adapter Name          Status    Version    Last Heartbeat
VMwareAdapter         STARTED   8.10.1     2024-01-15 14:32:18
vSphereAdapter        STARTED   8.10.1     2024-01-15 14:31:55
NSXAdapter            STOPPED   8.10.1     2024-01-15 14:15:42
CustomAdapter         ERROR     8.10.0     2024-01-15 13:48:09

2024-01-15 14:35:22 ERROR [AdapterManager] VMwareAdapter connection timeout after 30s
2024-01-15 14:34:18 EXCEPTION [CollectorService] java.net.SocketTimeoutException: Connection refused
2024-01-15 14:33:05 ERROR [AuthHandler] Authentication failed for vCenter credentials

VMwareAdapter
NSXAdapter
vSphereAdapter

2024-01-15 14:28:33 ERROR [VMwareAdapter] Failed to authenticate: Invalid credentials for vcenter.example.com
2024-01-15 14:27:15 ERROR [ConnectionPool] Connection timeout: vcenter.example.com:443
2024-01-15 14:26:42 AUTH [SSLContext] Certificate validation failed for host

Stopping vmware-vcops-watchdog: [  OK  ]
Starting vmware-vcops-watchdog: [  OK  ]
```

!!! warning "Common errors"
    **`ERROR [AdapterManager] VMwareAdapter connection timeout after 30s`** — Verify network connectivity to the target vCenter and check firewall rules allowing port 443 from the vROps appliance.
    **`ERROR [AuthHandler] Authentication failed for vCenter credentials`** — Re-enter the vCenter adapter credentials in the vROps UI under Administration > Adapters and ensure the service account password has not expired.
    **`Certificate validation failed for host`** — Add the vCenter SSL certificate to the vROps trust store using `vracli certificate add --file /path/to/cert.pem` or disable certificate validation in the adapter configuration if using a self-signed cert.
```bash
# Check analytics processing — if analytics queue is backed up, processing is delayed
tail -200 /data/vcops/log/analytics.log | grep -i "queue\|backlog\|warn\|error"

# Check GemFire (real-time cache) health
tail -100 /data/vcops/log/gemfire/vcopssuite_gemfire.log | grep -i "warn\|error"

# Confirm the adapter is actually collecting (not just in a Collecting state with zero data)
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/adapterkinds/VMWARE/resourcekinds/VirtualMachine/resources?pageSize=5" | \
  jq '.resourceList[] | {name: .resourceKey.name, lastCollected: .identifier}'
```

```text title="Expected output"
==> tail -200 /data/vcops/log/analytics.log | grep -i "queue\|backlog\|warn\|error"
2024-01-15 14:32:18,445 WARN  [AnalyticsProcessor-7] Queue depth at 8,234 events — processing lag detected
2024-01-15 14:33:02,891 WARN  [AnalyticsProcessor-12] Backlog threshold exceeded: 12,456 pending calculations
2024-01-15 14:33:45,123 ERROR [AnalyticsQueue] Failed to dequeue metric batch: timeout after 30s
2024-01-15 14:34:12,567 WARN  [MetricsAggregator] Queue utilization at 87% capacity

==> tail -100 /data/vcops/log/gemfire/vcopssuite_gemfire.log | grep -i "warn\|error"
2024-01-15 14:35:01,234 WARN  [GemFireServer-1] Member vrops-prod-02.example.local:40404 slow to respond (latency 2847ms)
2024-01-15 14:35:33,456 WARN  [CacheManager] Eviction triggered — heap usage at 91%

==> curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" "https://vrops-prod-01.example.local/suite-api/api/adapterkinds/VMWARE/resourcekinds/VirtualMachine/resources?pageSize=5" | jq '.resourceList[] | {name: .resourceKey.name, lastCollected: .identifier}'
{
  "name": "prod-web-01.example.local",
  "lastCollected": "2024-01-15T14:38:22Z"
}
{
  "name": "prod-db-02.example.local",
  "lastCollected": "2024-01-15T14:38:19Z"
}
{
  "name": "prod-app-03.example.local",
  "lastCollected": "2024-01-15T14:38:21Z"
}
{
  "name": "dev-test-04.example.local",
  "lastCollected": "2024-01-15T14:37:55Z"
}
{
  "name": "legacy-vm-05.example.local",
  "lastCollected": "2024-01-15T14:36:42Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag (already present) or import the vRops certificate into your system CA bundle with `update-ca-certificates`.
    **`jq: error (at <stdin>:1): Cannot index array with string "resourceList"`** — Verify the API token is valid by checking `echo $TOKEN` and confirm the vRops API endpoint is responding with JSON using `curl -sk ... | head -c 200`.
    **`Authorization: vRealizeOpsToken: command not found`** — Ensure the TOKEN variable is exported in your shell session with `export TOKEN=$(cat /path/to/token.txt)` before running the curl command.
```bash
# Force a capacity recalculation
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/analytics/run" \
  -H "Content-Type: application/json" \
  -d '{"analyticsJobName": "CapacityAnalytics"}'

# Check analytics job status
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/analytics" | \
  jq '.[] | select(.name == "CapacityAnalytics") | {status: .status, lastRun: .lastRunTime}'
```

```text title="Expected output"
{"status":"RUNNING","lastRun":1699564823000}
{"status":"COMPLETED","lastRun":1699564945000}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification, or import the vROps certificate into your system trust store.
    **`jq: error (at <stdin>:1): Cannot index object with string "[]"`** — Ensure the API response is valid JSON by checking that `$TOKEN` is set correctly and the vROps instance is accessible; test with `curl -sk https://vrops-prod-01.example.local/suite-api/api/analytics`.
    **`{"error":"Invalid token or insufficient permissions"}`** — Regenerate the API token in vROps Administration > API Access and ensure the service account has Analytics Administrator role assigned.
```bash
# Test LDAP connectivity from the Aria Operations appliance
ssh admin@vrops-prod-01.example.local
vracli auth test --source <ldap-source-name>

# Manually test LDAP bind
ldapsearch -H ldaps://dc01.example.local:636 \
  -D "CN=svc-vrops-ldap,OU=Service Accounts,DC=corp,DC=local" \
  -w '<password>' \
  -b "DC=corp,DC=local" \
  "(sAMAccountName=testuser)" sAMAccountName | head -10
```

```text title="Expected output"
Connected to vrops-prod-01.example.local.
Testing LDAP source: corp-ldap-prod
Connection: SUCCESS
Bind: SUCCESS
Search: SUCCESS
User resolution: SUCCESS
Test completed successfully.

# LDAP manual bind test output:
version: 3
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=local> with scope subtree
# filter (sAMAccountName=testuser)
# requesting: sAMAccountName
#

dn: CN=Test User,OU=Users,OU=Corp,DC=corp,DC=local
sAMAccountName: testuser

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    **`ldapsearch: error code 49 "80090308: LdapErr: DSID-0C090453, comment: AcceptSecurityContext error, data 52e, v3839 WILL_NOT_PERFORM"`** — Verify the service account password is correct and the account is not locked; reset credentials in Active Directory if needed.
    **`ldapsearch: error code 1 "Operations error"`** — Confirm the LDAP source hostname and port (636 for LDAPS) are correct and the firewall allows outbound connectivity from the Aria Operations appliance to the domain controller.
    **`vracli: command not found`** — SSH into the Aria Operations appliance using the correct admin credentials and ensure you are in the correct shell context; try `/usr/bin/vracli` with the full path if needed.
```bash
# Verify SMTP configuration
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/notifications" | \
  jq '.notificationList[] | {name: .name, plugin: .pluginTypeId, enabled: .active}'

# Send a test notification via API
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/notifications/<notification-id>/actions/test"

# Check outbound SMTP from the appliance
ssh admin@vrops-prod-01.example.local
curl -v smtp://smtp.example.local:25 --mail-from aria-ops@corp.local \
  --mail-rcpt test@corp.local 2>&1 | head -30
```

```text title="Expected output"
{
  "name": "Email Notification",
  "plugin": "EmailNotificationPlugin",
  "enabled": true
}
{
  "name": "Slack Integration",
  "plugin": "SlackNotificationPlugin",
  "enabled": false
}
{
  "name": "PagerDuty Alert",
  "plugin": "PagerDutyNotificationPlugin",
  "enabled": true
}

*   Trying 10.45.120.88...
* Connected to vrops-prod-01.example.local (10.45.120.88) port 443 (#0)
* Server certificate:
*   subject: CN=vrops-prod-01.example.local
*   issuer: CN=Example Root CA
* SSL connection made
> POST /suite-api/api/notifications/notif-8f2c4a91-7e3d-4b2a-9f1c-3d5e8a2b4c6f/actions/test HTTP/1.1
< HTTP/1.1 202 Accepted
< Content-Type: application/json
< X-vRealizeOps-Version: 8.14.1

admin@vrops-prod-01.example.local's password:
*   Trying 10.45.120.99...
* Connected to smtp.example.local (10.45.120.99) port 25 (#0)
< 220 smtp.example.local ESMTP Postfix 3.4.8
> EHLO vrops-prod-01.example.local
< 250-smtp.example.local
< 250-PIPELINING
< 250-SIZE 10240000
< 250-VRFY
< 250 HELP
> MAIL FROM:<aria-ops@corp.local>
< 250 2.1.0 Ok
> RCPT TO:<test@corp.local>
< 250 2.1.5 Ok
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification or import the vROps certificate into your system trust store.
    **`curl: (7) Failed to connect to vrops-prod-01.example.local port 443: Connection refused`** — Verify the vROps appliance is running and accessible on the network; check firewall rules and DNS resolution with `nslookup vrops-prod-01.example.local`.
    **`jq: parse error: Invalid JSON`** — Confirm the `$TOKEN` variable is set correctly with `echo $TOKEN` and that the API endpoint is responding with valid JSON using `curl -sk ... | head -c 500`.
```bash
# Check CPU and memory pressure on the primary node
ssh admin@vrops-prod-01.example.local
top -bn1 | head -20

# Check GemFire heap usage (in-memory cache)
tail -20 /data/vcops/log/gemfire/vcopssuite_gemfire.log | grep -i "heap\|memory"

# Check Cassandra compaction — heavy compaction causes query slowness
ssh admin@vrops-prod-01.example.local
nodetool compactionstats

# Check for very large queries — long-running queries appear in the analytics log
tail -200 /data/vcops/log/analytics.log | grep -i "slow\|timeout\|duration"
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
B1: "Adapter not collecting data" {shape: rectangle}
B2: "Dashboard blank or no data" {shape: rectangle}
B3: "Alert storm" {shape: rectangle}
B4: "Capacity calculation wrong" {shape: rectangle}
B5: "vSAN management pack missing metrics" {shape: rectangle}
B6: "Node offline or cluster issue" {shape: rectangle}
D1: "D1" {shape: rectangle}
R1: "Re-test Adapter Connection · Unlock Service Account\n→ Adapter Disconnected" {shape: rectangle}
R2: "Verify Source Reachability · Check Collector Log\n→ Adapter Disconnected" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Resolve Adapter Issue First\n→ Adapter Disconnected" {shape: rectangle}
R4: "Check Widget Scope · Widen Time Range\n→ No Data in Dashboards" {shape: rectangle}
R5: "Raise Alert Threshold · Add Wait Cycles · Suppress During Maintenance\n→ Alert Storm" {shape: rectangle}
R6: "Force Capacity Recalculation via API\n→ Capacity Calculation Wrong" {shape: rectangle}
R7: "Verify vSAN Management Pack Installed · Check Adapter Log\n→ vSAN Management Pack Missing Metrics" {shape: rectangle}
D3: "D3" {shape: rectangle}
R8: "Power On Node · Check Inter-node Network\n→ Node Offline / Cluster Issue" {shape: rectangle}
R9: "Restart vmware-vcops Service · Check VAMI Cluster Status\n→ Node Offline / Cluster Issue" {shape: rectangle}

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
B4 -> R6
B5 -> R7
D3 -> R8
D3 -> R9
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

- [Aria Operations — Diagnostics](../diagnostics/)
- [Aria Operations — Escalation](../escalation/)
- [Aria Operations Health Checks](../../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
