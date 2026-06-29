---
tags:
  - aria-networks
  - operations
  - cli
  - vmware
---
# Aria Operations for Networks — CLI Reference

<div class="kb-summary">
CLI and API reference for Aria Operations for Networks (vRNI): SSH appliance service management, collector operations, IPFIX diagnostics, REST API authentication, flow and data-source queries, application security group export, and VAMI management.

*Applies to: Aria Operations for Networks 6.x*
</div>
![Aria Operations for Networks — CLI Reference](../../../../assets/virtualization-vmware-aria-operations-for-networks-operation.svg)

## Before you begin

- **Access:** SSH to platform VM as `ubuntu` user; sudo to root for service commands
- **Collector access:** SSH to each collector VM separately — collector and platform are separate appliances
- **API token lifetime:** 24 hours by default; re-authenticate if commands return 401

---

## SSH Access

```bash
# Platform VM
ssh ubuntu@aon-platform.corp.local
sudo -i   # become root for service management

# Collector VM
ssh ubuntu@aon-collector.corp.local
sudo -i
```


```text title="Expected output"
ubuntu@aon-platform.corp.local's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-42-generic x86_64)

 System load: 0.45             Processes: 187
 Usage of /: 42.3% of 19.50GB   Users logged in: 2
 Last login: Mon Jan 15 14:22:18 2024 from 10.20.30.45

root@aon-platform:~# 
root@aon-platform:~# ssh ubuntu@aon-collector.corp.local
ubuntu@aon-collector.corp.local's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-42-generic x86_64)

 System load: 0.28             Processes: 156
 Usage of /: 38.1% of 19.50GB   Users logged in: 1
 Last login: Mon Jan 15 13:55:02 2024 from 10.20.30.45

root@aon-collector:~#
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname aon-platform.corp.local: Name or service not known`** — Verify DNS resolution with `nslookup aon-platform.corp.local` or update `/etc/hosts` with the correct IP address.
    **`Permission denied (publickey,password).`** — Confirm the ubuntu user credentials and that SSH key-based authentication is configured, or ensure the user has sudo privileges on the target VM.
    **`Connection refused`** — Check that SSH service is running on the target VM with `systemctl status ssh` and verify the VM is powered on and network-accessible.
---

## Platform Service Management

```bash
# Check all platform services at once
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres

# Individual service status
sudo systemctl status vrni-platform      # Main AON application
sudo systemctl status nginx              # Reverse proxy (UI/API entry point)
sudo systemctl status cassandra          # Flow data store
sudo systemctl status kafka              # Internal message bus
sudo systemctl status elasticsearch      # Search index
sudo systemctl status postgres           # Config/metadata database

# Restart a service
sudo systemctl restart vrni-platform

# View platform application log (first stop for errors)
sudo tail -f /var/log/app.log
sudo journalctl -u vrni-platform -f --since "1 hour ago"
```


```text title="Expected output"
● vrni-platform.service - VMware Aria Operations for Networks Platform
     Loaded: loaded (/etc/systemd/system/vrni-platform.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:18 UTC; 2 days ago
   Main PID: 4821 (java)
      Tasks: 47 (limit: 4915)
     Memory: 2.3G
     CGroup: /system.slice/vrni-platform.service
             └─4821 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xmx4g...

● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:25 UTC; 2 days ago
   Main PID: 5104 (nginx)
      Tasks: 8 (limit: 4915)
     Memory: 45.2M
     CGroup: /system.slice/nginx.service
             └─5104 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;

● cassandra.service - Apache Cassandra
     Loaded: loaded (/etc/systemd/system/cassandra.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:31 UTC; 2 days ago
   Main PID: 5287 (java)
      Tasks: 52 (limit: 4915)
     Memory: 3.8G
     CGroup: /system.slice/cassandra.service

● kafka.service - Apache Kafka Message Broker
     Loaded: loaded (/etc/systemd/system/kafka.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:40 UTC; 2 days ago
   Main PID: 5456 (java)
      Tasks: 38 (limit: 4915)
     Memory: 1.2G

● elasticsearch.service - Elasticsearch
     Loaded: loaded (/etc/systemd/system/elasticsearch.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:48 UTC; 2 days ago
   Main PID: 5678 (java)
      Tasks: 41 (limit: 4915)
     Memory: 2.1G

● postgres.service - PostgreSQL Database Server
     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:33:02 UTC; 2 days ago
   Main PID: 5891 (postgres)
      Tasks: 12 (limit: 4915)
     Memory: 156.3M

Restarting vrni-platform.service...
Job for vrni-platform.service started successfully.

=== Logs begin at Wed 2024-01-17 14:32:18 UTC, end at Fri
```
---

## Collector Service Management

```bash
# On each collector VM:
sudo systemctl status ni-collector
sudo systemctl restart ni-collector

# Collector logs — shows flow receipt and forwarding status
sudo journalctl -u ni-collector -f --since "1 hour ago"
sudo journalctl -u ni-collector -n 200

# View proxy.log — confirms IPFIX/NetFlow packets received
sudo tail -f /var/log/proxy.log

# Re-pair collector to Platform VM (run if collector shows as offline after IP/cert change)
sudo /home/ubuntu/support/pairing.sh
# Prompts:
#   Platform FQDN: aon-platform.corp.local
#   Pairing key:   <paste from AON UI → Settings → Infrastructure → Collectors>
```


```text title="Expected output"
● ni-collector.service - Aria Operations for Networks Collector
     Loaded: loaded (/etc/systemd/system/ni-collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2h 45min ago
   Main PID: 2847 (java)
      Tasks: 42 (limit: 4915)
     Memory: 1.2G
        CPU: 18min 32.456s
   CGroup: /system.slice/ni-collector.service
           └─2847 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xmx2g...

Jan 18 16:18:42 collector-01.corp.local ni-collector[2847]: [INFO] Flow batch received: 1247 records from 10.45.12.5
Jan 18 16:18:43 collector-01.corp.local ni-collector[2847]: [INFO] Forwarding 1247 flows to platform (aon-platform.corp.local:443)
Jan 18 16:18:44 collector-01.corp.local ni-collector[2847]: [INFO] Batch acknowledged by platform, seq=8847291
Jan 18 16:18:50 collector-01.corp.local ni-collector[2847]: [INFO] Flow batch received: 892 records from 10.45.12.6
Jan 18 16:18:51 collector-01.corp.local ni-collector[2847]: [INFO] Forwarding 892 flows to platform (aon-platform.corp.local:443)
Jan 18 16:19:02 collector-01.corp.local proxy[3124]: IPFIX packet received from 10.45.12.5:54821 (1024 bytes)
Jan 18 16:19:03 collector-01.corp.local proxy[3124]: IPFIX packet received from 10.45.12.6:54822 (1156 bytes)
Jan 18 16:19:04 collector-01.corp.local proxy[3124]: NetFlow v5 packet received from 10.45.12.7:12345 (512 bytes)

Pairing script started...
Enter Platform FQDN [aon-platform.corp.local]: aon-platform.corp.local
Enter Pairing Key: ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
[SUCCESS] Collector paired successfully. Certificate installed: /etc/ni-collector/certs/collector.crt
[SUCCESS] Collector registered with platform. Status will update within 60 seconds.
```

!!! warning "Common errors"
    **`ni-collector.service - Unit not found.`** — Verify the collector package is installed with `sudo apt list --installed | grep ni-collector` and reinstall if missing.
    **`[ERROR] Failed to connect to platform at aon-platform.corp.local:443: Name or service not known`** — Confirm DNS resolution with `nslookup aon-platform.corp.local` and verify network connectivity to the platform VM.
    **`[ERROR] Certificate validation failed: peer certificate cannot be authenticated with given CA certificates`** — Regenerate
---

## Disk Usage

High disk usage stops flow data collection. Alert at 80%, critical at 90%.

```bash
# Overall disk usage
df -hT

# Data partitions (Cassandra flow store + Elasticsearch index)
df -h /var/lib/cassandra
df -h /var/lib/elasticsearch
df -h /var/log

# Top disk consumers by directory
du -sh /var/lib/cassandra/*
du -sh /var/lib/elasticsearch/*

# Free journal space (safe operation)
sudo journalctl --vacuum-size=1G
```


```text title="Expected output"
Filesystem     Type      Size  Used Avail Use% Mounted on
/dev/sda1      ext4      500G  342G  158G  69% /
/dev/sda2      ext4      200G  156G   44G  78% /var
/dev/sdb1      ext4     1000G  892G  108G  89% /data
tmpfs          tmpfs      32G  4.2G   28G  13% /dev/shm

Filesystem     Size  Used Avail Use%
/dev/sda2      200G  156G   44G  78%

Filesystem     Size  Used Avail Use%
/dev/sdb1     1000G  892G  108G  89%

Filesystem     Size  Used Avail Use%
/dev/sda2      200G   89G  111G  45%

12G	/var/lib/cassandra/data
8.4G	/var/lib/cassandra/commitlog
3.2G	/var/lib/cassandra/saved_caches
1.1G	/var/lib/cassandra/hints

45G	/var/lib/elasticsearch/nodes
8.7G	/var/lib/elasticsearch/snapshots

Vacuumed journals from 2.3G down to 1.0G.
```

!!! warning "Common errors"
    **`df: '/var/lib/cassandra': No such file or directory`** — Verify Cassandra is installed and the service has started at least once to create the data directory structure.
    **`du: cannot access '/var/lib/elasticsearch/*': Permission denied`** — Run the du commands with `sudo` or ensure your user is in the elasticsearch group with `sudo usermod -aG elasticsearch $USER`.
---

## Network Connectivity Diagnostics

```bash
# Test TCP 443 connectivity to a collector from the platform VM
nc -zv aon-collector.corp.local 443

# Test connectivity to data sources
curl -sk https://vcenter.corp.local/rest/com/vmware/cis/session \
  -X POST -u 'svc-aon:PASSWORD' -o /dev/null -w "HTTP %{http_code}\n"

curl -sk https://nsxmgr.corp.local/api/v1/cluster \
  -u 'svc-aon:PASSWORD' -o /dev/null -w "HTTP %{http_code}\n"

# Check which ports are listening on platform VM
ss -tlnp | grep -E '443|8080|9042|2181|9200'

# DNS resolution test
nslookup aon-collector.corp.local
dig aon-collector.corp.local
```


```text title="Expected output"
Connection to aon-collector.corp.local 443 port [tcp/https] succeeded!
HTTP 200
HTTP 200
LISTEN    0      128                0.0.0.0:443            0.0.0.0:*    users:(("nginx",pid=2847,fd=6))
LISTEN    0      128                0.0.0.0:8080           0.0.0.0:*    users:(("java",pid=3156,fd=42))
LISTEN    0      128                0.0.0.0:9042           0.0.0.0:*    users:(("cassandra",pid=1924,fd=156))
LISTEN    0      128                0.0.0.0:2181           0.0.0.0:*    users:(("zookeeper",pid=2104,fd=28))
LISTEN    0      128                0.0.0.0:9200           0.0.0.0:*    users:(("elasticsearch",pid=2456,fd=9))

Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	aon-collector.corp.local
Address: 10.20.15.42

; <<>> DiG 9.16.1-Ubuntu <<>> aon-collector.corp.local
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54821
;; QUESTION SECTION:
;aon-collector.corp.local. IN	A

;; ANSWER SECTION:
aon-collector.corp.local. 300 IN	A	10.20.15.42

;; Query time: 2 msec
```

!!! warning "Common errors"
    **`Connection refused`** — Verify the collector VM is running and port 443 is not blocked by firewall rules between platform and collector.
    **`HTTP 401`** — Confirm the service account credentials are correct and the account has API access permissions on vCenter/NSX Manager.
    **`nslookup: can't resolve 'aon-collector.corp.local': No address associated with hostname`** — Add the collector hostname and IP to /etc/hosts or ensure DNS server has the A record configured.
---

## IPFIX / NetFlow Diagnostics

```bash
# Verify UDP 2055 (NetFlow/IPFIX) is being received from switches/vDS
# Run on the collector VM:
sudo tcpdump -i eth0 -n udp port 2055 -c 50

# Count packets per second arriving
sudo tcpdump -i eth0 -n udp port 2055 --immediate-mode -q 2>/dev/null | \
  awk 'BEGIN{c=0; t=systime()} {c++; if(systime()-t>=5){print c/5 " pps"; c=0; t=systime()}}'

# Expected: 10–1000+ pps on a busy network; 0 pps = IPFIX not reaching collector
```


```text title="Expected output"
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
22:14:33.445821 IP 10.50.12.45.54321 > 192.168.1.100.2055: UDP, length 1472
22:14:33.446102 IP 10.50.12.46.54322 > 192.168.1.100.2055: UDP, length 1472
22:14:33.446445 IP 10.50.12.47.54323 > 192.168.1.100.2055: UDP, length 1472
22:14:33.447891 IP 10.50.12.45.54321 > 192.168.1.100.2055: UDP, length 1472
22:14:33.448234 IP 10.50.12.48.54324 > 192.168.1.100.2055: UDP, length 1472
...
50 packets captured
50 packets received by filter
0 packets dropped by kernel
245.6 pps
248.2 pps
251.8 pps
```

!!! warning "Common errors"
    **`tcpdump: eth0: No such device`** — Verify the correct interface name with `ip link show` and replace eth0 with the appropriate NIC (e.g., ens0, ens160).
    **`0 pps` (no packets captured)** — Confirm NetFlow/IPFIX is enabled on source switches/vDS and verify firewall rules allow UDP 2055 inbound with `sudo ufw status` or check security groups.
    **`tcpdump: Permission denied`** — Run the command with `sudo` or add your user to the pcap group with `sudo usermod -aG pcap $USER` and restart your session.
---

## REST API — Authentication

```bash
AON="https://aon.corp.local"

# Authenticate and store token
TOKEN=$(curl -sk -X POST "${AON}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

echo "Token acquired: ${TOKEN:0:20}..."

# Export for use in subsequent commands
export AON_TOKEN="$TOKEN"
export AON_URL="$AON"

# Create a long-lived service account token
curl -sk -X POST "${AON}/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-monitoring@local","password":"<password>"}' \
  | python3 -m json.tool

# Revoke a token
curl -sk -X DELETE "${AON}/api/ni/auth/token" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}"
```


```text title="Expected output"
Token acquired: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdmMtbW9uaXRvcmluZ0Bsb2NhbCIsImlhdCI6MTcwNDY3MjAwMCwiZXhwIjoxNzA0NzU4NDAwfQ.a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "username": "svc-monitoring@local",
  "expiresAt": "2024-01-08T16:00:00Z",
  "tokenType": "Bearer"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl to skip certificate verification, or install the AON CA certificate in your system trust store.
    **`json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Verify the AON API endpoint is reachable and responding with valid JSON; check credentials and network connectivity to `aon.corp.local`.
    **`curl: (7) Failed to connect to aon.corp.local port 443: Connection refused`** — Confirm the AON appliance is running and the hostname resolves correctly with `nslookup aon.corp.local` or `ping aon.corp.local`.
---

## REST API — Data Sources

```bash
# List all configured data sources with sync status
curl -sk -X GET "${AON_URL}/api/ni/datasources" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
ds = json.load(sys.stdin)
for d in ds.get('results', []):
    print(f\"{d.get('nickname','?'):<30} {d.get('datasource_type','?'):<20} {d.get('enabled','')}\")"

# Get details of a specific data source
DS_ID="datasource-vcenter-001"
curl -sk -X GET "${AON_URL}/api/ni/datasources/${DS_ID}" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" | python3 -m json.tool

# Trigger a manual re-sync on a data source
curl -sk -X POST "${AON_URL}/api/ni/datasources/${DS_ID}/sync" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}"
```


```text title="Expected output"
vcenter-prod-01                vCenter              true
vcenter-dr-site                vCenter              true
nsxt-cluster-primary           NSX-T                true
aws-account-prod               AWS                  false
netflow-collector-01           NetFlow              true

{
  "id": "datasource-vcenter-001",
  "nickname": "vcenter-prod-01",
  "datasource_type": "vCenter",
  "enabled": true,
  "last_sync_time": "2024-01-15T14:32:18Z",
  "sync_status": "COMPLETED",
  "connection_status": "CONNECTED",
  "version": "7.0.3"
}

{"status": "SYNC_INITIATED", "datasource_id": "datasource-vcenter-001", "sync_job_id": "job-8f4c2a91-7e3d-4d9f-b1a2-5c6d9e0f1a2b"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification, or import the AON server's certificate into your system trust store.
    **`jq: parse error: Invalid JSON text at line 1`** — Verify `${AON_TOKEN}` and `${AON_URL}` are set correctly by running `echo $AON_TOKEN` and `echo $AON_URL`.
    **`{"error": "Unauthorized", "message": "Invalid or expired token"}`** — Regenerate the API token in Aria Operations for Networks UI and update the `AON_TOKEN` environment variable.
---

## REST API — Flow Queries

```bash
# Get flows from a specific VM in the last hour
curl -sk -X POST "${AON_URL}/api/ni/search" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "flows where source vm name = '\''web-01'\'' and time_range = '\''last 1 hour'\''",
    "page": {"start_index": 0, "end_index": 100}
  }' | python3 -m json.tool

# Get all East-West flows on port 3306 (MySQL)
curl -sk -X POST "${AON_URL}/api/ni/search" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "flows where destination port = 3306 and flow type = East-West",
    "page": {"start_index": 0, "end_index": 200}
  }' | python3 -m json.tool

# List open problems/anomalies
curl -sk -X GET "${AON_URL}/api/ni/problems?status=OPEN" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data.get('results', []):
    print(f\"{p.get('severity',''):<10} {p.get('name',''):<60}\")"
```


```text title="Expected output"
{
  "results": [
    {
      "source_vm": "web-01",
      "destination_ip": "10.24.15.88",
      "destination_port": 443,
      "protocol": "tcp",
      "bytes_sent": 2847291,
      "packets": 1523,
      "flow_start_time": "2024-01-15T14:32:18Z"
    },
    {
      "source_vm": "web-01",
      "destination_ip": "10.24.15.89",
      "destination_port": 443,
      "protocol": "tcp",
      "bytes_sent": 1924847,
      "packets": 987,
      "flow_start_time": "2024-01-15T13:45:22Z"
    }
  ],
  "total_count": 2
}
{
  "results": [
    {
      "source_ip": "10.20.5.42",
      "destination_ip": "10.20.6.18",
      "destination_port": 3306,
      "protocol": "tcp",
      "bytes_sent": 5234891,
      "flow_type": "East-West",
      "flow_start_time": "2024-01-15T15:12:44Z"
    },
    {
      "source_ip": "10.20.5.43",
      "destination_ip": "10.20.6.19",
      "destination_port": 3306,
      "protocol": "tcp",
      "bytes_sent": 3847291,
      "flow_type": "East-West",
      "flow_start_time": "2024-01-15T15:08:12Z"
    }
  ],
  "total_count": 47
}
CRITICAL   Anomalous data exfiltration detected on host db-prod-02
HIGH       Port scan activity from 10.20.8.15 to subnet 10.20.9.0/24
MEDIUM     Unusual East-West traffic spike on port 445
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present; if still failing, verify AON_URL uses https and certificate is valid on the Aria Operations appliance).
    **`jq: error (at <stdin>:1): Cannot index string with string "results"`** — Ensure the API response is valid JSON by checking AON_TOKEN is correct and the endpoint is accessible; verify with `curl -sk "${AON_URL}/api/ni/search" -H "Authorization: NetworkInsight ${AON_TOKEN}"` first.
    **`bash: AON_URL: unbound variable`** — Export the environment variables before running the script: `export AON_URL="https://aria-ops.example.com" AON_TOKEN="your-api-token"`.
---

## REST API — Applications and Security Groups

```bash
# List all defined applications
curl -sk -X GET "${AON_URL}/api/ni/groups/applications" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for app in data.get('results', []):
    print(f\"{app['entity_id']:<40} {app.get('name','')}\")"

# Get NSX-T security group recommendations for an application
APP_ID="application-12345"
curl -sk -X GET "${AON_URL}/api/ni/applications/${APP_ID}/security-groups" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" | python3 -m json.tool

# Push security group recommendations to NSX-T
NSX_DS_ID="datasource-nsx-001"
curl -sk -X POST "${AON_URL}/api/ni/applications/${APP_ID}/security-groups/export" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"nsx_manager_id\": \"${NSX_DS_ID}\"}" | python3 -m json.tool
```


```text title="Expected output"
app-uuid-550e8400-e29b-41d4-a716-446655440000 Production-Web-Tier
app-uuid-6ba7b810-9dad-11d1-80b4-00c04fd430c8 Database-Backend
app-uuid-6ba7b811-9dad-11d1-80b4-00c04fd430c8 Cache-Layer
app-uuid-6ba7b812-9dad-11d1-80b4-00c04fd430c8 API-Gateway

{
  "results": [
    {
      "entity_id": "sg-rec-001",
      "name": "Prod-Web-to-DB",
      "rules": [
        {
          "source": "10.20.1.0/24",
          "destination": "10.20.2.0/24",
          "protocol": "tcp",
          "port": "5432"
        }
      ],
      "confidence": 0.94
    }
  ]
}

{
  "task_id": "export-task-789abc",
  "status": "SUBMITTED",
  "nsx_manager": "nsx-manager-prod.corp.local",
  "application_id": "application-12345",
  "timestamp": "2024-01-15T14:32:18Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification, or import the AON server's CA certificate into your system trust store.
    **`jq: parse error: Invalid JSON text at line 1`** — Verify `${AON_TOKEN}` and `${AON_URL}` are set correctly and the API endpoint is accessible by running `curl -sk -I "${AON_URL}/api/ni/groups/applications"` first.
    **`{"error": "Unauthorized", "code": 401}`** — Ensure the NetworkInsight token has not expired and includes the correct `Authorization: NetworkInsight` header format.
---

## REST API — Collectors and Alerts

```bash
# List all collectors and their status
curl -sk -X GET "${AON_URL}/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('results', []):
    print(f\"{c.get('nickname',''):<30} {c.get('status',''):<15} {c.get('ip_address','')}\")"

# List all active alerts
curl -sk -X GET "${AON_URL}/api/ni/alerts" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" | python3 -m json.tool

# Acknowledge an alert
ALERT_ID="alert-789"
curl -sk -X PUT "${AON_URL}/api/ni/alerts/${ALERT_ID}/acknowledge" \
  -H "Authorization: NetworkInsight ${AON_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Acknowledged by ops team"}' | python3 -m json.tool
```


```text title="Expected output"
collector-us-east-1       ACTIVE          192.168.1.45
collector-us-west-2       ACTIVE          192.168.1.46
collector-eu-central-1    STANDBY         192.168.1.47
collector-apac-01         ACTIVE          192.168.1.48
{
    "results": [
        {
            "id": "alert-789",
            "severity": "CRITICAL",
            "title": "High packet loss detected on vlan-456",
            "status": "OPEN",
            "created_at": "2024-01-15T09:23:14Z",
            "entity_id": "dvswitch-prod-01"
        },
        {
            "id": "alert-790",
            "severity": "WARNING",
            "title": "Interface utilization above 85%",
            "status": "OPEN",
            "created_at": "2024-01-15T08:45:22Z",
            "entity_id": "esx-host-12"
        }
    ],
    "total": 2
}
{
    "id": "alert-789",
    "severity": "CRITICAL",
    "status": "ACKNOWLEDGED",
    "acknowledged_by": "ops-user@corp.local",
    "acknowledged_at": "2024-01-15T10:12:47Z",
    "comment": "Acknowledged by ops team"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification (already present in the example, but ensure it's not removed).
    **`jq: command not found`** — Install `python3-json.tool` or use `python3 -m json.tool` instead of piping to `jq`.
    **`401 Unauthorized`** — Verify that `${AON_TOKEN}` is set correctly and has not expired; regenerate the API token in Aria Operations for Networks UI if needed.
---

## See also

- [AON Operational Procedures](../procedures/)
- [AON Scripts](../scripts/)
- [AON Health Checks](../health-checks/)

## Verify

- **Service status:** `sudo systemctl status vrni-platform` shows `active (running)`
- **Flow data:** AON UI → Flow Map — flows visible for known workloads
- **API test:** `curl -sk -H "Authorization: NetworkInsight $AON_TOKEN" "$AON_URL/api/ni/datasources" | python3 -m json.tool` returns datasource list
