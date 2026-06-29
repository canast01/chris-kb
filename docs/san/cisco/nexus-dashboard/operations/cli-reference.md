---
tags:
  - operations
  - san
---
# Cisco Nexus Dashboard — Operations CLI Reference
![Cisco Nexus Dashboard — Operations CLI Reference](../../../../assets/san-cisco-nexus-dashboard-operations-cli-reference.svg)

```bash
# Show cluster health summary
acs health

# List all cluster nodes with status
acs nodes list

# Show cluster configuration
acs cluster info

# Show platform version
acs version
```


```text title="Expected output"
Cluster Health Summary:
  Overall Status: Healthy
  Last Updated: 2024-01-15T14:32:18Z
  Services Running: 12/12
  Alerts: 0 critical, 2 warning

Cluster Nodes:
  Node ID          Hostname              IP Address      Status    Role
  node-001         nexus-dash-01.lab     10.20.50.11     Ready     Leader
  node-002         nexus-dash-02.lab     10.20.50.12     Ready     Follower
  node-003         nexus-dash-03.lab     10.20.50.13     Ready     Follower

Cluster Configuration:
  Cluster Name: prod-dashboard-cluster
  Cluster ID: a7f2c9e1-4b6d-11ee-be56-0242ac120002
  Node Count: 3
  HA Mode: Enabled
  Replication Factor: 3

Platform Version:
  Nexus Dashboard: 3.1.2
  Build Number: 3.1.2.20240115
  Release Date: 2024-01-15
```

!!! warning "Common errors"
    **`acs: command not found`** — Ensure the ACS CLI is installed and the PATH includes the installation directory, or source the environment setup script.
    **`Error: Unable to connect to cluster endpoint`** — Verify network connectivity to the cluster nodes and confirm the ACS_ENDPOINT environment variable is correctly set.
    **`Error: Authentication failed - invalid credentials`** — Check that your ACS credentials are valid and the NEXUS_USER and NEXUS_PASSWORD environment variables are properly configured.
```bash
# Upload an upgrade image
acs upgrade upload /tmp/aci-nd-dk9.3.1.1.ova

# List uploaded upgrade images
acs upgrade images

# Start cluster upgrade
acs upgrade start --version 3.1.1

# Monitor upgrade progress
acs upgrade status

# Show upgrade history
acs upgrade history
```

```text title="Expected output"
Uploading image: /tmp/aci-nd-dk9.3.1.1.ova
Progress: ████████████████████████████████ 100%
Image uploaded successfully. Size: 2847MB, Checksum: a3f7e2c91d4b5e8f9a2b3c4d5e6f7g8h

Available upgrade images:
  Version    Size      Uploaded              Status
  3.1.1      2847MB    2024-01-15 14:32:15   ready
  3.0.2      2756MB    2024-01-10 09:18:42   ready

Initiating cluster upgrade to version 3.1.1...
Upgrade job created: upgrade-20240115-143245
Estimated duration: 45 minutes
Starting upgrade process...

Upgrade Status:
  Job ID: upgrade-20240115-143245
  Current Version: 3.0.2
  Target Version: 3.1.1
  Progress: 35% (Node 2 of 3 upgraded)
  Elapsed Time: 18 minutes
  Estimated Remaining: 27 minutes
  Status: IN_PROGRESS

Upgrade History:
  Date                Version    Duration    Status      Nodes
  2024-01-15 14:32   3.0.2→3.1.1 42m 18s    COMPLETED   3/3
  2023-12-20 08:15   3.0.1→3.0.2 38m 45s    COMPLETED   3/3
  2023-11-05 16:42   3.0.0→3.0.1 41m 12s    COMPLETED   3/3
```

!!! warning "Common errors"
    **`Error: Image file not found at /tmp/aci-nd-dk9.3.1.1.ova`** — Verify the image file path and ensure it exists with `ls -lh /tmp/aci-nd-dk9*.ova`.
    **`Error: Upgrade already in progress. Job ID: upgrade-20240115-120000`** — Wait for the current upgrade to complete or cancel it with `acs upgrade cancel <job-id>` before starting a new one.
    **`Error: Insufficient disk space. Required: 5GB, Available: 2.3GB`** — Free up disk space on the Nexus Dashboard nodes or remove older upgrade images with `acs upgrade images delete --version <old-version>`.
```bash
# Show node network configuration
acs network show

# Show NTP status
acs system ntp show

# Show DNS configuration
acs system dns show

# Test connectivity to a host
acs network test --host 10.20.1.5 --port 22
```

```text title="Expected output"
Node Network Configuration:
  Interface: eth0
  IP Address: 192.168.100.42/24
  Gateway: 192.168.100.1
  MTU: 1500
  Status: up

NTP Status:
  NTP Service: enabled
  Sync Status: synchronized
  Current Time: 2024-01-15 14:32:18 UTC
  Stratum: 2
  Reference Clock: 10.20.1.10

DNS Configuration:
  Primary DNS: 8.8.8.8
  Secondary DNS: 8.8.4.4
  Search Domain: corp.local
  Timeout: 5 seconds

Connectivity Test to 10.20.1.5:22
  Status: reachable
  Response Time: 12ms
  Port 22: open
```

!!! warning "Common errors"
    **`Error: NTP service is not running`** — Enable NTP with `acs system ntp enable` and verify connectivity to the configured NTP server.
    **`Error: DNS resolution failed for 10.20.1.5`** — Verify DNS servers are reachable and correctly configured with `acs system dns show`, or use IP addresses directly.
    **`Error: Connection timeout to 10.20.1.5:22`** — Check network connectivity and firewall rules allow traffic from the Nexus Dashboard node to the target host on port 22.
```bash
# Show current TLS certificate details
acs certificates show

# Import a new certificate (key + cert bundle)
acs certificates import \
  --key /tmp/nd.key \
  --cert /tmp/nd-bundle.crt \
  --name nd-dc1-cert

# Set the imported certificate as active
acs certificates activate --name nd-dc1-cert
```

```text title="Expected output"
Certificate Details:
  Name: nd-default-cert
  Subject: CN=nexus-dashboard.dc1.local,O=Cisco,C=US
  Issuer: CN=Cisco Root CA,O=Cisco,C=US
  Valid From: 2023-01-15 10:22:33 UTC
  Valid Until: 2025-01-15 10:22:33 UTC
  Fingerprint (SHA256): a7f3e9c2b1d4f6e8a9c3b5d7f1e3a5c7b9d1f3e5a7c9b1d3f5e7a9c1b3d5f7

Importing certificate from /tmp/nd.key and /tmp/nd-bundle.crt...
Certificate imported successfully.
  Name: nd-dc1-cert
  Subject: CN=nexus-dashboard-dc1.local,O=Cisco,C=US
  Issuer: CN=Cisco Root CA,O=Cisco,C=US
  Valid From: 2024-06-20 14:45:12 UTC
  Valid Until: 2026-06-20 14:45:12 UTC

Activating certificate: nd-dc1-cert
Certificate nd-dc1-cert is now active.
Dashboard will restart to apply changes. This may take 2-3 minutes.
```

!!! warning "Common errors"
    **`Error: Certificate file not found: /tmp/nd.key`** — Verify the key file path exists and is readable with `ls -la /tmp/nd.key`.
    **`Error: Certificate validation failed - certificate and key do not match`** — Ensure the certificate and key pair are from the same generation by re-exporting them together from your CA.
    **`Error: Certificate nd-dc1-cert is already active`** — Skip the activate command if the certificate is already in use, or deactivate the current certificate first.
```bash
# Show all pod status (run as ndadmin — kubectl is available)
kubectl get pods --all-namespaces

# Show pods with issues only
kubectl get pods --all-namespaces | grep -Ev "Running|Completed|Terminating"

# Show pod logs (replace <pod-name> and <namespace>)
kubectl logs -n ndfc <pod-name> --tail=100

# Describe a failing pod (shows events and resource constraints)
kubectl describe pod -n ndfc <pod-name>

# Show persistent volume usage
kubectl get pv
kubectl get pvc --all-namespaces
```

```text title="Expected output"
NAMESPACE     NAME                                    READY   STATUS    RESTARTS   AGE
kube-system   coredns-558bd4d5db-2k8vx                1/1     Running   0          45d
kube-system   etcd-ndash-master-01                    1/1     Running   2          45d
ndfc          ndfc-controller-0                       1/1     Running   0          42d
ndfc          ndfc-postgres-0                         1/1     Running   1          42d
ndfc          ndfc-redis-0                            1/1     Running   0          42d
ndfc          ndfc-ui-deployment-7c4f9b2d8-kp9qr      1/1     Running   0          15d
ndfc          ndfc-api-gateway-5d8c6f3a1-m2xvl        1/1     Running   0          8d
monitoring    prometheus-operator-0                   1/1     Running   0          30d
...

NAME                                    READY   STATUS             RESTARTS   AGE
ndfc          ndfc-backup-job-abc123                  0/1     CrashLoopBackOff   5          2h
ndfc          ndfc-collector-pod-xyz789               0/2     ImagePullBackOff   0          1h

NAME                                 READY   STATUS    RESTARTS   AGE
ndfc-controller-0                    1/1     Running   0          42d
ndfc-postgres-0                      1/1     Running   1          42d
ndfc-redis-0                         1/1     Running   0          42d

NAME                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM
pv-ndfc-data-001           100Gi      RWO            Delete           Bound    ndfc/ndfc-postgres-pvc
pv-ndfc-backup-002         500Gi      RWO            Delete           Bound    ndfc/ndfc-backup-pvc
pv-ndfc-logs-003           50Gi       RWO            Delete           Bound    ndfc/ndfc-logs-pvc

NAMESPACE   NAME                      STATUS   VOLUME              CAPACITY   ACCESS MODES   STORAGECLASS
ndfc        ndfc-postgres-pvc         Bound    pv-ndfc-data-001    100Gi      RWO            fast-ssd
ndfc        ndfc-backup-pvc           Bound    pv-ndfc-backup-002  500Gi      RWO            fast-ssd
monitoring  prometheus-pvc            Bound    pv-prometheus-004   200Gi      RWO            standard
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "pods" in API group ""`** — Verify kubectl is configured correctly with `kubectl cluster-info` and your kubeconfig points to the Nexus Dashboard cluster.
    **`Error from server (Forbidden): pods is forbidden: User "ndadmin" cannot get resource "pods" in API group "" in the namespace "ndfc"`** — Add RBAC permissions for the ndadmin user with `kubectl create rolebinding ndadmin-pods --clusterrole=view --user=ndadmin -n ndfc`.
```bash
# Show system resource usage per node
acs system resources

# Show system logs (platform-level)
acs system logs --tail 100

# Generate a diagnostic support bundle for Cisco TAC
acs techsupport --output /tmp/nd-support-$(date +%Y%m%d).tar.gz

# Collect support bundle and transfer to your workstation
scp ndadmin@nd-dc1.corp.example.com:/tmp/nd-support-*.tar.gz ./
```

```text title="Expected output"
Node: nd-dc1
  CPU Usage: 45.2%
  Memory Usage: 62.8% (28.4 GB / 45.2 GB)
  Disk Usage: 71.3% (/var/lib/nd)
  Network I/O: RX 2.4 Mbps / TX 1.8 Mbps

Node: nd-dc2
  CPU Usage: 38.7%
  Memory Usage: 58.1% (26.2 GB / 45.2 GB)
  Disk Usage: 68.9% (/var/lib/nd)
  Network I/O: RX 1.9 Mbps / TX 2.1 Mbps

2024-01-15T14:32:18.456Z [INFO] Platform initialized successfully
2024-01-15T14:33:02.123Z [WARN] High memory pressure detected on nd-dc1
2024-01-15T14:35:41.789Z [INFO] Cluster health check passed
2024-01-15T14:38:15.234Z [ERROR] Transient connection loss to fabric node 10.48.12.5 (recovered)
2024-01-15T14:40:09.567Z [INFO] Configuration sync completed across cluster
...
(100 lines total)

Generating support bundle...
Collecting system logs...
Collecting configuration snapshots...
Collecting cluster state information...
Support bundle created: /tmp/nd-support-20240115.tar.gz (847 MB)

nd-support-20240115.tar.gz                    100%  847MB   12.4MB/s   01:08
```

!!! warning "Common errors"
    **`scp: /tmp/nd-support-*.tar.gz: No such file or directory`** — Verify the techsupport command completed successfully and check the actual filename with `ssh ndadmin@nd-dc1.corp.example.com ls -la /tmp/nd-support-*.tar.gz`.
    **`Permission denied (publickey,password)`** — Ensure SSH key-based authentication is configured for the ndadmin user or add `-o PubkeyAuthentication=no` to use password authentication.
    **`Disk quota exceeded`** — Free up space on the Nexus Dashboard node by archiving or deleting old support bundles, or redirect output to a different filesystem with more capacity.
```bash
# Authenticate — returns a bearer token
TOKEN=$(curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{
    "userName": "svc-automation",
    "userPasswd": "<password>",
    "domain": "local"
  }' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

echo "Token obtained"

# Refresh token (before expiry)
TOKEN=$(curl -sk -X POST https://nd-dc1.corp.example.com/login/refresh \
  -H "Authorization: Bearer ${TOKEN}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Logout (invalidate token)
curl -sk -X POST https://nd-dc1.corp.example.com/logout \
  -H "Authorization: Bearer ${TOKEN}"
```

```text title="Expected output"
Token obtained
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl (already present) or import the Nexus Dashboard CA certificate into your system trust store.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Verify the username, password, and domain are correct; check that the Nexus Dashboard API endpoint is reachable and responding with valid JSON.
    **`curl: (7) Failed to connect to nd-dc1.corp.example.com port 443: Connection refused`** — Confirm the Nexus Dashboard hostname/IP and port are correct, and that the service is running and accessible from your network.
```bash
ND="https://nd-dc1.corp.example.com"

# List registered sites
curl -sk "${ND}/nexus/api/v1/sites" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List cluster nodes
curl -sk "${ND}/nexus/api/v1/nodes" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List installed apps
curl -sk "${ND}/nexus/api/v1/apps" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List users
curl -sk "${ND}/nexus/api/v1/users" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool
```

```text title="Expected output"
{
  "sites": [
    {
      "siteId": "site-001",
      "name": "dc1-primary",
      "status": "HEALTHY",
      "fabricType": "ACI",
      "lastHeartbeat": "2024-01-15T14:32:18Z"
    },
    {
      "siteId": "site-002",
      "name": "dc2-secondary",
      "status": "HEALTHY",
      "fabricType": "ACI",
      "lastHeartbeat": "2024-01-15T14:31:52Z"
    }
  ]
}
{
  "nodes": [
    {
      "nodeId": "node-1",
      "hostname": "nd-node-01.corp.example.com",
      "ipAddress": "192.168.100.41",
      "role": "LEADER",
      "status": "READY",
      "version": "3.2.1.1a"
    },
    {
      "nodeId": "node-2",
      "hostname": "nd-node-02.corp.example.com",
      "ipAddress": "192.168.100.42",
      "role": "FOLLOWER",
      "status": "READY",
      "version": "3.2.1.1a"
    },
    {
      "nodeId": "node-3",
      "hostname": "nd-node-03.corp.example.com",
      "ipAddress": "192.168.100.43",
      "role": "FOLLOWER",
      "status": "READY",
      "version": "3.2.1.1a"
    }
  ]
}
{
  "apps": [
    {
      "appId": "app-aci-001",
      "name": "ACI Multi-Site Orchestrator",
      "version": "5.1.2",
      "status": "RUNNING"
    },
    {
      "appId": "app-dcnm-001",
      "name": "Data Center Network Manager",
      "version": "12.1.3",
      "status": "RUNNING"
    },
    {
      "appId": "app-assurance-001",
      "name": "Nexus Dashboard Assurance",
      "version": "6.2.1",
      "status": "RUNNING"
    }
  ]
}
{
  "users": [
    {
      "userId": "admin",
      "username": "admin",
      "role": "SUPER_ADMIN",
      "lastLogin": "2024-01-15T13:45:22Z"
    },
    {
      "userId": "user-noc-001",
      "username": "noc-team",
      "role": "ADMIN",
      "lastLogin": "2024-01-15T12:18:09Z"
    },
    {
      "userId": "user-readonly-001",
      "username": "monitoring-svc",
      "role": "VIEWER",
      "lastLogin": "2024-01-15T14:29:33Z"
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL
```bash
NDFC_BASE="${ND}/appcenter/cisco/ndfc/api/v1"

# List all fabrics
curl -sk "${NDFC_BASE}/san/fabrics" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List all switches (inventory)
curl -sk "${NDFC_BASE}/inventory/switches" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List VSANs for a fabric
curl -sk "${NDFC_BASE}/san/vsans?fabricName=DC1-SAN" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List active zone sets
curl -sk "${NDFC_BASE}/san/zoning/activezonesets?fabricName=DC1-SAN" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List device aliases
curl -sk "${NDFC_BASE}/san/devicealias?fabricName=DC1-SAN" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List active alarms
curl -sk "${NDFC_BASE}/alarms/activealarms" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List firmware images in NDFC repository
curl -sk "${NDFC_BASE}/fm/image" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool
```

```text title="Expected output"
{
  "fabrics": [
    {
      "fabricName": "DC1-SAN",
      "fabricType": "SAN",
      "fabricId": "1",
      "status": "HEALTHY",
      "switchCount": 4
    },
    {
      "fabricName": "DC2-SAN",
      "fabricType": "SAN",
      "fabricId": "2",
      "status": "HEALTHY",
      "switchCount": 2
    }
  ]
}
{
  "switches": [
    {
      "switchName": "SAN-SWITCH-01",
      "switchIp": "10.50.20.11",
      "switchRole": "Principal",
      "model": "Nexus 5672UP",
      "serialNumber": "JAE2345ABCD",
      "fabricName": "DC1-SAN"
    },
    {
      "switchName": "SAN-SWITCH-02",
      "switchIp": "10.50.20.12",
      "switchRole": "Principal",
      "model": "Nexus 5672UP",
      "serialNumber": "JAE2345ABCE",
      "fabricName": "DC1-SAN"
    }
  ]
}
{
  "vsans": [
    {
      "vsanId": 100,
      "vsanName": "PROD-VSAN",
      "status": "ACTIVE",
      "memberCount": 4
    },
    {
      "vsanId": 101,
      "vsanName": "TEST-VSAN",
      "status": "ACTIVE",
      "memberCount": 2
    }
  ]
}
{
  "activeZoneSets": [
    {
      "zoneSetName": "PROD-ZONESET",
      "vsanId": 100,
      "zoneCount": 8,
      "status": "ACTIVE"
    }
  ]
}
{
  "deviceAliases": [
    {
      "aliasName": "PROD-STORAGE-01",
      "pwwn": "50:00:14:40:5a:2b:c1:e0",
      "vsanId": 100
    },
    {
      "aliasName": "PROD-HOST-01",
      "pwwn": "50:00:09:73:a2:1b:d4:f2",
      "vsanId": 100
    }
  ]
}
{
  "activeAlarms": [
    {
      "alarmId": "ALM-2024-001",
      "severity": "CRITICAL",
      "message": "Switch SAN-SWITCH-03 unreachable",
      "timestamp": "2024-01-15T14:32:18Z"
    },
    {
      "alarmId": "ALM-2024-002",
      "severity": "WARNING",
      "message": "VSAN 101 utilization at 85%",
      "timestamp": "2024-01-15T13:45:22Z"
    }
  ]
}
{
  "images": [
    {
      "imageName": "nx
```
```bash
NDI_BASE="${ND}/appcenter/cisco/ndinsight/api/v1"

# List all anomalies (last 24 hours)
curl -sk "${NDI_BASE}/anomalies?timeRange=LAST_DAY&severity=CRITICAL,MAJOR" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# Get anomaly details
curl -sk "${NDI_BASE}/anomalies/<anomaly-id>" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# List flows (SAN Insights)
curl -sk "${NDI_BASE}/san/flows?fabricName=DC1-SAN&timeRange=LAST_HOUR" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool
```

```text title="Expected output"
{
  "anomalies": [
    {
      "id": "anom-2024-0847-fc1",
      "severity": "CRITICAL",
      "type": "PortErrorRate",
      "fabricName": "DC1-SAN",
      "affectedDevice": "switch-core-01",
      "affectedPort": "fc1/42",
      "detectedTime": "2024-01-15T14:32:18Z",
      "description": "FC port error rate exceeded 5% threshold"
    },
    {
      "id": "anom-2024-0846-fc2",
      "severity": "MAJOR",
      "type": "LinkLatency",
      "fabricName": "DC1-SAN",
      "affectedDevice": "switch-edge-03",
      "affectedPort": "fc2/8",
      "detectedTime": "2024-01-15T13:47:52Z",
      "description": "ISL latency increased to 2.8ms"
    }
  ],
  "totalCount": 2,
  "timeRange": "LAST_DAY"
}
{
  "anomalyId": "anom-2024-0847-fc1",
  "severity": "CRITICAL",
  "status": "ACTIVE",
  "rootCause": "CRC errors on FC port",
  "recommendedAction": "Check transceiver health and cable integrity",
  "impactedFlows": 47,
  "estimatedImpact": "HIGH"
}
{
  "flows": [
    {
      "flowId": "flow-dc1-san-001",
      "initiator": "10.48.12.45",
      "target": "10.48.12.89",
      "protocol": "SCSI",
      "throughput": "8.2 Gbps",
      "packetLoss": "0.02%",
      "latency": "1.2ms"
    },
    {
      "flowId": "flow-dc1-san-002",
      "initiator": "10.48.12.67",
      "target": "10.48.12.91",
      "protocol": "SCSI",
      "throughput": "6.8 Gbps",
      "packetLoss": "0.00%",
      "latency": "1.1ms"
    }
  ],
  "totalFlows": 156,
  "timeRange": "LAST_HOUR"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the Nexus Dashboard CA certificate into your system trust store.
    **`{"error": "Invalid or expired token", "code": 401}`** — Regenerate the Bearer token in Nexus Dashboard UI (System > Settings > API Tokens) and ensure `$TOKEN` variable is set correctly.
    **`curl: (7) Failed to connect to <host>: Connection refused`** — Verify the Nexus Dashboard hostname/IP in `$ND` variable is reachable and the API service is running with `curl -sk https://<nd-host>/appcenter/cisco/ndinsight/api/v1/health
```bash
# Count switches by management state
curl -sk "${NDFC_BASE}/inventory/switches" \
  -H "Authorization: Bearer ${TOKEN}" \
  | python3 -c "
import sys, json, collections
data = json.load(sys.stdin)
states = collections.Counter(s.get('managementState','unknown') for s in data)
print(dict(states))
"

# List all non-healthy ND pods
kubectl get pods --all-namespaces --no-headers \
  | awk '{if ($4 != "Running" && $4 != "Completed") print $0}'

# Export NDFC switch inventory to CSV
curl -sk "${NDFC_BASE}/inventory/switches" \
  -H "Authorization: Bearer ${TOKEN}" \
  | python3 -c "
import sys, json, csv
data = json.load(sys.stdin)
fields = ['switchName','ipAddress','model','release','managementState','fabricName']
w = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction='ignore')
w.writeheader()
for s in data: w.writerow(s)
" > ndfc-switches-$(date +%Y%m%d).csv
```


```text title="Expected output"
{'managed': 48, 'unmanaged': 3, 'offline': 1}
kube-system          coredns-558bd4d5db-7x9k2                    0/1       CrashLoopBackOff   12         3h22m
kube-system          etcd-ndfc-master-01                         1/1       Error              2          2d14h
monitoring           prometheus-operator-6d8f4c9b-8xk2l           0/1       ImagePullBackOff   0          1d8h
ndfc-system          ndfc-api-server-0                           1/2       Running            0          5d2h
ndfc-system          ndfc-postgres-backup-28156789-abc12          0/1       Completed          0          6h15m
switchName,ipAddress,model,release,managementState,fabricName
leaf-01,10.200.1.45,N9K-C93180YC-EX,10.1(2),managed,DC1-Fabric
spine-01,10.200.1.10,N9K-C9508,10.2(1),managed,DC1-Fabric
spine-02,10.200.1.11,N9K-C9508,10.2(1),managed,DC1-Fabric
leaf-02,10.200.1.46,N9K-C93180YC-EX,10.1(2),managed,DC1-Fabric
border-01,10.200.1.80,N9K-C9504,10.1(2),unmanaged,DC1-Fabric
...
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command or configure proper CA certificates in your environment.
    **`jq: command not found` or `python3: command not found`** — Install the required JSON parser (python3 or jq) on the Nexus Dashboard host or bastion server.
    **`401 Unauthorized`** — Verify the Bearer token is valid and not expired by re-authenticating with `ndfc-login.sh` or checking token expiration time.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Nexus Dashboard — Procedures](../procedures/)
- [Nexus Dashboard — Scripts](../scripts/)
- [Nexus Dashboard — Health Checks](../health-checks/)
