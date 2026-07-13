---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
---
# Cisco Nexus Dashboard — Troubleshooting Diagnostics

*Applies to: Cisco MDS / NX-OS*
![Cisco Nexus Dashboard — Troubleshooting Diagnostics](../../../../assets/san-cisco-nexus-dashboard-troubleshooting-diagnostics.svg)


```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# View platform-level logs
acs system logs --tail 100

# Filter by component
acs system logs --component ndfc --tail 100
acs system logs --component ndi --tail 100
acs system logs --component security --tail 100

# Show audit log entries (user activity)
acs system logs --component audit --tail 50
```


```text title="Expected output"
Last login: Wed Mar 13 14:22:18 2024 from 10.45.22.88
nd-dc1-1.corp.example.com#
nd-dc1-1.corp.example.com# acs system logs --tail 100
2024-03-13T14:21:47.823Z [INFO] ndfc-manager: Fabric sync completed for fabric-prod-01 (sync_id: a7f2c9e1-4b3d-11ee-9c2a-0050569f1234)
2024-03-13T14:21:32.156Z [WARN] ndi-agent: High memory usage detected on leaf-switch-03 (usage: 87%)
2024-03-13T14:21:15.492Z [INFO] security: Certificate renewal scheduled for nd-dc1-1.corp.example.com (expires: 2025-04-22)
2024-03-13T14:20:58.734Z [ERROR] ndfc-manager: Failed to reach spine-01.dc1 (timeout after 30s)
2024-03-13T14:20:42.109Z [INFO] ndi-agent: Policy deployment completed on 24 devices
2024-03-13T14:20:15.667Z [INFO] ndfc-manager: Backup job started (backup_id: bkp_20240313_142015)
...
nd-dc1-1.corp.example.com# acs system logs --component ndfc --tail 100
2024-03-13T14:21:47.823Z [INFO] ndfc-manager: Fabric sync completed for fabric-prod-01 (sync_id: a7f2c9e1-4b3d-11ee-9c2a-0050569f1234)
2024-03-13T14:20:58.734Z [ERROR] ndfc-manager: Failed to reach spine-01.dc1 (timeout after 30s)
2024-03-13T14:20:42.109Z [INFO] ndi-agent: Policy deployment completed on 24 devices
2024-03-13T14:19:33.445Z [INFO] ndfc-manager: Configuration push to leaf-switch-02 successful
...
nd-dc1-1.corp.example.com# acs system logs --component ndi --tail 100
2024-03-13T14:21:32.156Z [WARN] ndi-agent: High memory usage detected on leaf-switch-03 (usage: 87%)
2024-03-13T14:20:42.109Z [INFO] ndi-agent: Policy deployment completed on 24 devices
2024-03-13T14:18:47.821Z [INFO] ndi-agent: Device health check passed for 48 devices
2024-03-13T14:17:22.334Z [WARN] ndi-agent: Interface flap detected on eth1/47 (spine-02)
...
nd-dc1-1.corp.example.com# acs system logs --component security --tail 100
2024-03-13T14:21:15.492Z [INFO] security: Certificate renewal scheduled for nd-dc1-1.corp.example.com (expires: 2025-04-22)
2024-
```
```bash
# CPU and memory usage per node
acs system resources

# Detailed Kubernetes node metrics
kubectl top nodes

# Per-pod resource usage (most memory/CPU hungry pods)
kubectl top pods --all-namespaces --sort-by=memory | head -20

# Node disk usage
kubectl get nodes -o wide
# SSH to each node and check:
df -h
du -sh /data/
```

```text title="Expected output"
CPU and memory usage per node:
Node: nexus-dashboard-node-1
  CPU Usage: 45%
  Memory Usage: 62%
  Status: Healthy

Node: nexus-dashboard-node-2
  CPU Usage: 38%
  Memory Usage: 58%
  Status: Healthy

Node: nexus-dashboard-node-3
  CPU Usage: 52%
  Memory Usage: 71%
  Status: Healthy

NAME                          CPU(cores)   MEMORY(Mi)
nexus-dashboard-node-1        2847m        8192Mi
nexus-dashboard-node-2        2156m        7456Mi
nexus-dashboard-node-3        3124m        9216Mi

NAMESPACE            NAME                                    CPU(m)   MEMORY(Mi)
kube-system          etcd-nexus-dashboard-node-1             156      512
nexus-dashboard      nd-api-server-7d4f9c2b1a8e9            342      1024
nexus-dashboard      nd-postgres-0                           89       2048
nexus-dashboard      nd-elasticsearch-0                      267      3072
kube-system          coredns-558bd4d5db-2xk9l                45       128
nexus-dashboard      nd-redis-master-0                       78       512
nexus-dashboard      nd-influxdb-0                           156      1536
kube-system          kube-proxy-9x2kl                        32       96
...

NAME                          STATUS   ROLES    AGE    VERSION            INTERNAL-IP      EXTERNAL-IP
nexus-dashboard-node-1        Ready    master   45d    v1.24.8            10.48.12.101     <none>
nexus-dashboard-node-2        Ready    worker   45d    v1.24.8            10.48.12.102     <none>
nexus-dashboard-node-3        Ready    worker   45d    v1.24.8            10.48.12.103     <none>

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1      500G  287G  213G  58% /
/dev/sdb1      1.0T  756G  244G  76% /data
tmpfs          16G   0    16G   0%  /dev/shm

/data/: 756G
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: metrics not available yet` | Wait 1–2 minutes after cluster startup for metrics-server to initialize, then retry the kubectl top command. |
    | `error: unable to connect to the server: dial tcp: lookup nexus-dashboard-node-1: no such host` | Verify DNS resolution or use the node's IP address directly instead of hostname in SSH commands. |
    | `Filesystem /dev/sdb1 is 76% full` | Archive or delete old logs and snapshots from `/data/` directory, or expand the volume if persistent growth is expected. |
```bash
# Recent cluster events (shows pod failures, scheduling issues, etc.)
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -50

# Events in a specific namespace
kubectl get events -n ndfc --sort-by='.lastTimestamp' | tail -20
```

```text title="Expected output"
NAMESPACE     NAME                                             TYPE      REASON                AGE    MESSAGE
kube-system   coredns-558bd4d5db-7k9m2.17a4f8c1a2b3d4e5      Warning   BackOff               45m    Back-off restarting failed container
kube-system   etcd-nexus-ctrl-01.17a4f8c1a2b3d4e6            Normal    Started               2d     Started container etcd
ingress-ng    nginx-ingress-controller-5d8f7c.17a4f8c1a2b3d4 Warning   FailedScheduling      12m    0/3 nodes available: 3 Insufficient memory
ndfc          ndfc-api-deployment-7f8c2d-abc12.17a4f8c1a2b3d Normal    Created               8h     Created container ndfc-api
ndfc          ndfc-db-statefulset-0.17a4f8c1a2b3d4e7         Warning   Unhealthy             3m     Readiness probe failed: connection refused
ndfc          ndfc-collector-daemonset-xyz9k.17a4f8c1a2b3d4e Normal    NodeAllocatable       1d     Updated Node Allocatable
monitoring   prometheus-operator-5c8d9f.17a4f8c1a2b3d4e8     Normal    Pulled                6h     Successfully pulled image "prom/prometheus:v2.41.0"
ndfc          ndfc-api-deployment-7f8c2d-def45.17a4f8c1a2b3d Warning   ImagePullBackOff      25m    Failed to pull image "nexus-dashboard:2.3.1": rpc error: code = Unknown
...

NAMESPACE   NAME                                             TYPE      REASON              AGE   MESSAGE
ndfc        ndfc-api-deployment-7f8c2d-abc12.17a4f8c1a2b3d Normal    Created             8h    Created container ndfc-api
ndfc        ndfc-db-statefulset-0.17a4f8c1a2b3d4e7         Warning   Unhealthy           3m    Readiness probe failed: connection refused
ndfc        ndfc-collector-daemonset-xyz9k.17a4f8c1a2b3d4e Normal    NodeAllocatable     1d    Updated Node Allocatable
ndfc        ndfc-api-deployment-7f8c2d-def45.17a4f8c1a2b3d Warning   ImagePullBackOff    25m   Failed to pull image "nexus-dashboard:2.3.1": rpc error: code = Unknown
ndfc        ndfc-scheduler-job-5c8d9f.17a4f8c1a2b3d4e8     Normal    Completed           2h    Job completed successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "events"` | Verify kubectl version is 1.19+ and the API server is responding with `kubectl cluster-info`. |
    | `error: namespace "ndfc" not found` | Confirm the ndfc namespace exists with `kubectl get namespaces | grep ndfc` and create it if missing with ` |
```bash
# Check etcd cluster health
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health

# Check etcd leader
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint status --write-out=table

# Expected: one LEADER, two followers for a 3-node cluster
```

```text title="Expected output"
https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 12.456ms

+------------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|       ENDPOINT         |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+------------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
| https://127.0.0.1:2379 | 8e4a7c2d9f1b5a3e |   3.5.9 | 45 MB   | true      | false      |    18     |   2847391  |      2847391       |        |
+------------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: context deadline exceeded` | Increase the timeout with `--command-timeout=10s` or verify etcd service is running with `systemctl status etcd`. |
    | `Error: x509: certificate signed by unknown authority` | Verify certificate paths are correct and CA certificate matches the etcd server's signing CA with `openssl verify -CAfile /etc/kubernetes/pki/etcd/ca.crt /etc/kubernetes/pki/etcd/server.crt`. |
```bash
# Check discovery manager logs for a specific switch
kubectl logs -n ndfc deployment/ndfc-discovery-manager --tail=500 \
  | grep "<switch-ip>"

# Test SSH from ND data network
acs network test --host <switch-ip> --port 22

# Test SNMP v3
kubectl exec -n ndfc deployment/ndfc-server -- \
  snmpget -v3 -u ndfc_poll -l authPriv -a SHA -A <auth-pass> \
  -x AES -X <priv-pass> <switch-ip> sysDescr.0

# Trigger a manual rediscovery via API
TOKEN=$(curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"admin","userPasswd":"<pass>","domain":"local"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -X POST \
  "https://nd-dc1.corp.example.com/appcenter/cisco/ndfc/api/v1/san/fabrics/rediscover" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"fabricName":"DC1-FABRIC-A","rediscoverAll":false,"switchSerialNumbers":["<serial>"]}'
```

```text title="Expected output"
2024-01-15T09:42:31.847Z INFO Discovery manager starting fabric scan for 192.168.1.100
2024-01-15T09:42:32.102Z DEBUG SSH connection established to 192.168.1.100:22
2024-01-15T09:42:33.456Z INFO Device fingerprint verified: N9K-C93180YC-EX
2024-01-15T09:42:34.221Z DEBUG SNMP v3 authentication successful for 192.168.1.100
2024-01-15T09:42:34.889Z INFO sysDescr: Cisco NX-OS Software, Version 10.1(2)

SSH connectivity test to 192.168.1.100:22 ... OK (response time: 12ms)

SNMP v3 query successful
SNMPv3 User: ndfc_poll
Auth Protocol: SHA
Privacy Protocol: AES
Response: Cisco Nexus Operating System (NX-OS) Software 10.1(2)

{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyTmFtZSI6ImFkbWluIiwiZXhwIjoxNzA1MzI4NTUxfQ.x7kZ9mP2qL4vN8wR3jT6sY1bF5cD9eH2gK4nM7pO0aQ"}

{"status":"success","message":"Rediscovery initiated for fabric DC1-FABRIC-A","jobId":"job-2024-01-15-094235-7f3a2c1e","switchCount":1,"estimatedDuration":"45 seconds"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to curl commands to skip certificate verification in lab/test environments, or import the ND certificate into your system trust store. |
    | `jq: command not found` | Install jq with `apt-get install jq` or `yum install jq`, or use the provided `python3 -c` JSON parser instead. |
    | `SNMP request timed out` | Verify the switch IP is reachable with `ping <switch-ip>`, confirm SNMP v3 credentials match the switch configuration, and check that the ndfc_poll user exists on the target device. |
```bash
# Check NDFC zone manager logs
kubectl logs -n ndfc deployment/ndfc-zone-manager --tail=200 \
  | grep -i "error\|fail\|conflict"

# Verify zone consistency on a specific MDS switch (NX-OS CLI)
# From a terminal to the switch:
show zoneset active vsan <vsan-id>
show zone status vsan <vsan-id>
show zone merge-failure vsan <vsan-id>
```

```text title="Expected output"
2024-01-15T09:42:33.123Z ERROR [ZoneManager] Failed to apply zone config to switch 10.48.2.15: timeout after 30s
2024-01-15T09:42:45.456Z WARN [ZoneManager] Zone merge conflict detected on VSAN 10: member count mismatch (local=12, remote=14)
2024-01-15T09:43:02.789Z ERROR [ZoneManager] Unable to retrieve zone status from switch 10.48.2.16: SSH connection refused
2024-01-15T09:43:18.234Z INFO [ZoneManager] Retrying zone activation for VSAN 10 (attempt 2/3)

zoneset name prod_zones vsan 10
  zone name app_tier
    member pwwn 50:00:14:40:5a:2b:c1:e0
    member pwwn 50:00:14:40:5a:2b:c1:e1
  zone name db_tier
    member pwwn 50:00:14:40:5a:2b:c2:f0
    member pwwn 50:00:14:40:5a:2b:c2:f1

VSAN 10:
  Status: Active
  Number of zones: 8
  Number of members: 24
  Merge status: In Progress (85% complete)

Zone Merge Failures for VSAN 10:
  Switch 10.48.2.16 (Fabric B): Member 50:00:14:40:5a:2b:c3:a0 not found in Fabric A
  Switch 10.48.2.17 (Fabric B): Zone "legacy_storage" missing from Fabric A
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: unable to decode an event from the watch stream: unexpected EOF` | Restart the ndfc-zone-manager pod with `kubectl rollout restart deployment/ndfc-zone-manager -n ndfc`. |
    | `Connection refused` or `SSH connection refused` | Verify switch IP reachability and SSH credentials with `ssh -v admin@<switch-ip>` and check firewall rules. |
    | `Zone merge conflict detected` or `Member count mismatch` | Manually trigger a zone merge resync from NDFC UI or run `zone merge-failure clear` on the affected switch. |
```bash
# Connect to NDFC database (PostgreSQL)
kubectl exec -n ndfc deployment/ndfc-server -- \
  psql -U postgres -c "\l"
# Lists databases: ndfc, pmdb, etc.

# Check NDFC main DB size
kubectl exec -n ndfc deployment/ndfc-server -- \
  psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('ndfc'));"

# Find large tables
kubectl exec -n ndfc deployment/ndfc-server -- \
  psql -U postgres ndfc -c "
SELECT relname, pg_size_pretty(pg_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_relation_size(relid) DESC
LIMIT 10;"
```

```text title="Expected output"
List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 ndfc      | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 pmdb      | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres
(5 rows)

 pg_size_pretty
----------------
 2847 MB
(1 row)

            relname            |  size
-------------------------------+----------
 fabric_device_config          | 1247 MB
 fabric_device_facts           | 892 MB
 audit_log                      | 456 MB
 fabric_policy_config          | 234 MB
 fabric_interface_status       | 187 MB
 device_inventory              | 156 MB
 fabric_topology               | 98 MB
 policy_deployment_history     | 67 MB
 fabric_vlan_mapping           | 45 MB
 system_events                 | 32 MB
(10 rows)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: could not translate host name "localhost" to address: Name or service not known` | Ensure the ndfc-server pod is running with `kubectl get pods -n ndfc` and verify network connectivity within the cluster. |
    | `FATAL: role "postgres" does not exist` | Check that the PostgreSQL user exists by connecting with the correct credentials or use `kubectl exec` to verify the pod's database initialization logs. |
    | `ERROR: database "ndfc" does not exist` | Confirm the ndfc database was created during deployment by running the first command to list all databases, or check pod startup logs for initialization errors. |
```bash
# Check NDI flow collector pod
kubectl get pods -n ndi | grep collector
kubectl logs -n ndi deployment/ndi-flow-collector --tail=200 | grep -i "error\|drop"

# Check Elasticsearch health (NDI primary storage)
kubectl exec -n ndi deployment/ndi-elasticsearch -- \
  curl -sk http://localhost:9200/_cluster/health?pretty
# Expected: status "green"; if "red": shards are unassigned (disk or node issue)

# Check Elasticsearch disk usage
kubectl exec -n ndi deployment/ndi-elasticsearch -- \
  curl -sk http://localhost:9200/_cat/allocation?v
# If disk.percent > 85%: Elasticsearch watermark triggered, stops accepting writes
```

```text title="Expected output"
ndi-flow-collector-7d4f2c9b-kxmq2   1/1     Running   0          14d
ndi-flow-collector-7d4f2c9b-pqr8n   1/1     Running   0          8d
2024-01-15T09:42:31.123Z [WARN] Packet drop detected: 2.3% loss on interface eth0
2024-01-15T09:43:15.456Z [ERROR] Failed to connect to Elasticsearch node 10.42.0.18:9200, retrying...

{
  "cluster_name" : "ndi-elasticsearch",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 3,
  "number_of_data_nodes" : 3,
  "active_primary_shards" : 24,
  "active_shards" : 72,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}

ip        node.role   disk.indices  disk.used disk.avail disk.total disk.percent
10.42.0.16 d           487.2gb       512.5gb   1.8tb      2.3tb      22
10.42.0.18 d           491.8gb       518.3gb   1.7tb      2.3tb      23
10.42.0.22 d           485.1gb       509.9gb   1.8tb      2.3tb      22
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: unable to upgrade connection: container not found ("ndi-elasticsearch")` | Verify the Elasticsearch pod is running with `kubectl get pods -n ndi | grep elasticsearch` and check pod logs for crash reasons. |
    | `curl: (7) Failed to connect to localhost port 9200: Connection refused` | Ensure the Elasticsearch service is listening by checking if the pod is in Running state and not in CrashLoopBackOff. |
    | `{"error":{"type":"cluster_block_exception","reason":"index [.ds-ndi-flow-2024.01.15-000042] blocked for writes"}}` | Reduce disk usage below 85% watermark by deleting old indices with `curl -X DELETE http://localhost:9200/.ds-ndi-flow-2024.01.01*` or expanding storage. |
```bash
# Check anomaly engine logs
kubectl logs -n ndi deployment/ndi-anomaly-engine --tail=200 | grep -i "error\|fail"

# Verify NDI license is valid
kubectl exec -n ndi deployment/ndi-anomaly-engine -- \
  curl -sk http://nd-license-service/api/v1/licenses | python3 -m json.tool | grep -i "ndi\|insights"
```

```text title="Expected output"
2024-01-15T09:42:33.521Z ERROR [AnomalyEngine] Failed to connect to metrics-collector: connection timeout after 30s
2024-01-15T09:42:45.103Z WARN [LicenseValidator] License expiration check skipped: service unavailable
2024-01-15T09:43:12.667Z ERROR [DataProcessor] Anomaly detection pipeline stalled: insufficient memory (2048MB < 4096MB required)
2024-01-15T09:43:28.445Z FAIL [HealthCheck] NDI insights module offline
{
  "licenses": [
    {
      "product": "ndi-insights",
      "status": "active",
      "expiration": "2025-06-30T23:59:59Z",
      "seats": 50
    },
    {
      "product": "ndi-core",
      "status": "active",
      "expiration": "2025-06-30T23:59:59Z"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: unable to upgrade connection: container not found` | Verify the ndi-anomaly-engine pod is running with `kubectl get pods -n ndi` and check pod logs for crash reasons. |
    | `curl: (7) Failed to connect to nd-license-service port 80: Connection refused` | Ensure the nd-license-service is deployed and accessible by running `kubectl get svc -n ndi` and checking service DNS resolution. |
    | `jq: parse error: Invalid JSON at line 1` | The license service returned non-JSON output; verify the service endpoint with `kubectl port-forward -n ndi svc/nd-license-service 8080:80` and test directly. |
```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Test connectivity to all managed switch IPs
acs network test --host <switch-ip> --port 22     # SSH
acs network test --host <switch-ip> --port 161    # SNMP
acs network test --host ldap.corp.example.com --port 636  # LDAPS

# Capture traffic on the data interface (requires tcpdump)
kubectl exec -n ndfc deployment/ndfc-discovery-manager -- \
  timeout 30 tcpdump -i eth0 -n host <switch-ip> -c 50

# Check SNMP trap reception
kubectl exec -n ndfc deployment/ndfc-server -- \
  timeout 30 tcpdump -i eth0 -n udp port 162 -c 10
```

```text title="Expected output"
Last login: Wed Jan 15 14:32:18 2025 from 10.45.22.108
ndadmin@nd-dc1-1:~$ acs network test --host 10.50.100.45 --port 22
Host 10.50.100.45:22 — Connection successful (response time: 12ms)

ndadmin@nd-dc1-1:~$ acs network test --host 10.50.100.45 --port 161
Host 10.50.100.45:161 — Connection successful (response time: 8ms)

ndadmin@nd-dc1-1:~$ acs network test --host ldap.corp.example.com --port 636
Host ldap.corp.example.com:636 — Connection successful (response time: 24ms)

ndadmin@nd-dc1-1:~$ kubectl exec -n ndfc deployment/ndfc-discovery-manager -- timeout 30 tcpdump -i eth0 -n host 10.50.100.45 -c 50
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
14:32:45.123456 IP 10.45.22.50.22 > 10.50.100.45.54321: Flags [S], seq 892341234
14:32:45.134567 IP 10.50.100.45.54321 > 10.45.22.50.22: Flags [S.], seq 1234567890
14:32:45.145678 IP 10.45.22.50.22 > 10.50.100.45.54321: Flags [.], ack 1234567891
50 packets captured
50 packets received by filter
0 packets dropped by kernel

ndadmin@nd-dc1-1:~$ kubectl exec -n ndfc deployment/ndfc-server -- timeout 30 tcpdump -i eth0 -n udp port 162 -c 10
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
14:32:50.234567 IP 10.50.100.45.38921 > 10.45.22.50.162: UDP, length 156
14:32:55.345678 IP 10.50.100.46.38922 > 10.45.22.50.162: UDP, length 148
10 packets captured
10 packets received by filter
0 packets dropped by kernel
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: unable to connect to the server: dial tcp: lookup nd-dc1-1.corp.example.com: no such host` | Verify the Nexus Dashboard hostname is resolvable by running `nslookup nd-dc1-1.corp.example.com` and check DNS or /etc/hosts. |
    | `Host <switch-ip>:<port> — Connection timeout (no response after 5s)` | Confirm the switch IP is reachable with `ping <switch-ip>` and verify firewall rules allow traffic from the ND management interface to that port. |
    **`error: no
```bash
# ND cluster resource snapshot
acs system resources

# Kubernetes resource usage per namespace
kubectl top pods --all-namespaces --sort-by=cpu | head -20

# Measure REST API response time
time curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"svc-monitor","userPasswd":"<pass>","domain":"local"}'
# Expected: < 2 seconds; > 5 seconds indicates platform performance issue

# Check NDFC API response time
TOKEN=$(... obtain token ...)
time curl -sk \
  "https://nd-dc1.corp.example.com/appcenter/cisco/ndfc/api/v1/inventory/switches" \
  -H "Authorization: Bearer ${TOKEN}" > /dev/null
# Expected: < 5 seconds for < 200 switches
```

```text title="Expected output"
System Resources:
  CPU Usage: 62%
  Memory Usage: 78% (31.2 GB / 40 GB)
  Disk Usage: 84% (/var/lib/docker: 156 GB / 186 GB)
  Network I/O: RX 2.3 Gbps / TX 1.8 Gbps

NAME                                    CPU(m)   MEMORY(Mi)
ndfc-platform-api-7d4c9f2b-k8s9m       1240     4821
kube-apiserver-nd-dc1                   856      2104
etcd-nd-dc1                             634      1876
ndfc-dcnm-scheduler-5f8b2a1c-9x7k2     512      2341
prometheus-operator-8c3d1f9a-2m5n8     428      1687
...

real	0m1.847s
user	0m0.234s
sys	0m0.156s

real	0m4.312s
user	0m0.198s
sys	0m0.142s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the ND CA certificate into your system trust store. |
    | `curl: (7) Failed to connect to nd-dc1.corp.example.com port 443: Connection refused` | Verify ND cluster is running with `acs system status` and confirm DNS resolution with `nslookup nd-dc1.corp.example.com`. |
    | `{"error":"Invalid credentials","code":401}` | Confirm the service account password is correct and the account has API access permissions in ND RBAC settings. |
```bash
# Patch NDFC server log level to DEBUG
kubectl set env deployment/ndfc-server -n ndfc LOG_LEVEL=DEBUG

# Reproduce the issue and collect logs
kubectl logs -n ndfc deployment/ndfc-server --tail=500 | grep -i "debug\|error" > /tmp/ndfc-debug.log

# Return to INFO level after troubleshooting
kubectl set env deployment/ndfc-server -n ndfc LOG_LEVEL=INFO
kubectl rollout restart deployment/ndfc-server -n ndfc
kubectl rollout status deployment/ndfc-server -n ndfc
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> verify_resolution: investigate
verify_resolution -> resolution
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Nexus Dashboard — Common Issues](../common-issues/)
- [Nexus Dashboard — Escalation](../escalation/)
- [Nexus Dashboard — Health Checks](../../operations/health-checks/)
