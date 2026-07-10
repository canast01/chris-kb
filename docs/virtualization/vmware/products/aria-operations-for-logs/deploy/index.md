---
tags:
  - aria-logs
  - deployment
  - vmware
search:
  boost: 1.5
---
# Aria Operations for Logs — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Aria Operations for Logs (vRLI). Covers prerequisites, master node OVA deployment, worker cluster setup, syslog and CFAPI agent configuration, content pack installation, and end-to-end validation.

*Applies to: Aria Logs 8.x*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_predeployment_prerequisites: "Phase 1 — Pre-Deployment Prerequisites" {shape: rectangle}
phase_2_master_node_deployment: "Phase 2 — Master Node Deployment" {shape: rectangle}
phase_3_worker_node_deployment: "Phase 3 — Worker Node Deployment" {shape: rectangle}
phase_4_log_sources_and_agent_instal: "Phase 4 — Log Sources and Agent Installation" {shape: rectangle}
phase_5_content_packs_alerts_and_for: "Phase 5 — Content Packs, Alerts, and Forwarding" {shape: rectangle}
phase_6_endtoend_validation: "Phase 6 — End-to-End Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_predeployment_prerequisites
phase_1_predeployment_prerequisites -> phase_2_master_node_deployment
phase_2_master_node_deployment -> phase_3_worker_node_deployment
phase_3_worker_node_deployment -> phase_4_log_sources_and_agent_instal
phase_4_log_sources_and_agent_instal -> phase_5_content_packs_alerts_and_for
phase_5_content_packs_alerts_and_for -> phase_6_endtoend_validation
phase_6_endtoend_validation -> validate
```

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1 — Pre-Deployment Prerequisites

**Exit criterion:** DNS resolves with PTR records, firewall ports are open, NTP is confirmed, and ingest rate is estimated.

```bash
# Verify DNS from management workstation
nslookup vrli-master.example.local && nslookup <planned-master-ip>
nslookup vrli-worker-01.example.local && nslookup vrli-vip.example.local
```


```text title="Expected output"
Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	vrli-master.example.local
Address: 192.168.1.100

Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	192.168.1.100
Address: 192.168.1.100

Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	vrli-worker-01.example.local
Address: 192.168.1.101

Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	vrli-vip.example.local
Address: 192.168.1.110
```

!!! warning "Common errors"
    **`** server can't find vrli-master.example.local: NXDOMAIN`** — Verify the DNS zone is configured on your DNS server and the hostname is registered in DNS.
    **`nslookup: command not found`** — Install bind-utils (RHEL/CentOS) or dnsutils (Debian/Ubuntu) package on the management workstation.
    **`connection timed out; no servers could be reached`** — Confirm the DNS server IP (10.0.0.53) is reachable and correct in /etc/resolv.conf.
Required firewall ports:

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| 514 | UDP/TCP | Inbound to VIP | Syslog ingestion (plaintext) |
| 6514 | TCP | Inbound to VIP | Syslog over TLS (encrypted) |
| 9543 | TCP | Inbound to master | CFAPI agent forwarding |
| 443 | TCP | Inbound to master | Admin UI and REST API |

```bash
# Test from a log source before deployment
nc -vzu vrli-master.example.local 514    # UDP syslog
nc -vz vrli-master.example.local 9543   # CFAPI agent port
```


```text title="Expected output"
Connection to vrli-master.example.local 514 [udp/syslog] succeeded!
Connection to vrli-master.example.local 9543 [tcp/*] succeeded!
```

!!! warning "Common errors"
    **`nc: getaddrinfo for host "vrli-master.example.local" port 514/udp failed: Name or service not known`** — Verify DNS resolution with `nslookup vrli-master.example.local` or use the IP address directly instead of the hostname.
    **`Connection refused`** — Confirm the Aria Operations for Logs syslog receiver (port 514) and CFAPI agent (port 9543) are running on the target host with `netstat -tuln | grep -E '514|9543'`.
Ingest sizing:

| Environment | Daily Volume | Recommended Config |
|---|---|---|
| < 500 VMs | 5–20 GB/day | Master only (530 GB) |
| 500–2000 VMs | 20–100 GB/day | Master + 2 workers |
| 2000+ VMs | 100 GB+/day | Master + 3+ workers |

Use SSD-backed storage. Minimum 530 GB per node for production.

---

## Phase 2 — Master Node Deployment

**Exit criterion:** Master node is in Running state; admin UI is accessible at port 443; setup wizard is complete.

```text
vSphere Client → Deploy OVF Template → select Aria Ops for Logs OVA
→ Target: cluster → SSD-backed datastore
→ Customise:
    Hostname: vrli-master.example.local  ·  IP: 10.0.1.30/24
    Gateway: 10.0.1.1  ·  DNS: 10.0.1.5  ·  NTP: ntp.example.local
    Root password: <strong password>
→ Power on (first-boot takes 5–10 min; Cassandra index initialises)
```

Setup wizard at `https://vrli-master.example.local`:

1. Accept EULA → set admin email and password.
2. Deployment type: **New Deployment** (first node).
3. Enter licence key (free tier: 25 OSI; production licence for scale).
4. Master initialises log index → transitions to **Running** state.

```bash
ssh root@vrli-master.example.local
li-admin status          # cluster status: MASTER
li-admin cluster         # single node: Active
df -h /storage/core      # confirm disk mounted
```


```text title="Expected output"
root@vrli-master.example.local's password: 
Welcome to vRealize Log Insight
vrli-master:~# li-admin status
Cluster Status: MASTER
Node Role: ACTIVE
Cluster Size: 1
vrli-master:~# li-admin cluster
Node Name: vrli-master.example.local
Node UUID: 550e8400-e29b-41d4-a716-446655440000
Status: ACTIVE
Role: MASTER
vrli-master:~# df -h /storage/core
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       500G  245G  255G  49% /storage/core
```

!!! warning "Common errors"
    **`li-admin: command not found`** — Ensure you are logged in as root and the VRLI service is running; check `/opt/vmware/var/log/` for startup errors.
    **`/storage/core: No such file or directory`** — Verify the storage mount completed successfully by running `mount | grep storage` and check `/etc/fstab` for mount configuration.
---

## Phase 3 — Worker Node Deployment

**Exit criterion:** All worker nodes show Active in Administration → Cluster; no Missing Shards warning; ingestion is distributed.

Deploy each worker OVA with the same customisation parameters, but in the setup wizard select **Join Cluster**:

```text
Setup wizard → Deployment Type: Join Cluster
→ Master node IP: 10.0.1.30  ·  Admin credentials: admin / <password>
→ Worker joins and synchronises from master automatically
```

```bash
# From master — confirm all nodes joined and active
curl -sk -u 'admin:<password>' \
  "https://vrli-master.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {hostname: .hostname, state: .state, role: .role}'
# Expected: all nodes state: ACTIVE
```


```text title="Expected output"
{
  "hostname": "vrli-master.example.local",
  "state": "ACTIVE",
  "role": "MASTER"
}
{
  "hostname": "vrli-worker-01.example.local",
  "state": "ACTIVE",
  "role": "WORKER"
}
{
  "hostname": "vrli-worker-02.example.local",
  "state": "ACTIVE",
  "role": "WORKER"
}
{
  "hostname": "vrli-worker-03.example.local",
  "state": "ACTIVE",
  "role": "WORKER"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag (already present) or import the master's CA certificate into your system trust store.
    **`jq: parse error: Invalid JSON text at line 1`** — Verify the API endpoint is correct and the cluster service is fully started; check `systemctl status aria-ops-logs` on the master node.
    **`401 Unauthorized`** — Confirm the admin password is correct and URL-encoded if it contains special characters; test with `curl -sk -u 'admin:password' https://vrli-master.example.local/api/v2/cluster/nodes`.
Configure VIP for HA (if using a load balancer):

```text
Administration → Cluster → Configuration → Set VIP: 10.0.1.35
(point all log sources at the VIP, not individual node IPs)
```

---

## Phase 4 — Log Sources and Agent Installation

**Exit criterion:** vSphere content pack is active, ESXi syslog is auto-configured on all hosts, CFAPI agents are reporting, and at least one syslog source is sending events to Explore Logs.

### vSphere Integration (Auto-configures ESXi syslog)

```text
Administration → vSphere Integration → Add vCenter
→ FQDN: vcenter.example.local
→ Credentials: svc-vrli-ro@example.local (read-only)
→ Enable: Configure ESXi Syslog Automatically
→ Save
```

Aria Logs pushes the syslog target to every ESXi host via vCenter — no manual per-host configuration needed.

```bash
# Verify on any ESXi host
esxcli system syslog config get
# RemoteHost: udp://vrli-master.example.local:514
esxcli system syslog reload
```


```text title="Expected output"
Hostname: esxi-host-01.example.local
RemoteHost: udp://vrli-master.example.local:514
DefaultRotate: 10
DefaultSize: 1024
LogDir: /scratch/log
DefaultFormat: [%b %d %H:%M:%S %s] %b %d %H:%M:%S %hostName %syslog-tag
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unable to parse options.`** — Verify the syslog configuration syntax matches the format `udp://hostname:port` without extra spaces or special characters.
    **`Connection refused`** — Confirm that vrli-master.example.local is reachable on port 514 and that the Aria Operations for Logs collector is running and listening on that port.
### CFAPI Agent on Linux VMs

```bash
# Download agent: Administration → Agents → Download Agent
chmod +x VMware-Log-Insight-Agent-<version>.bin
./VMware-Log-Insight-Agent-<version>.bin -- \
  --ip vrli-master.example.local --port 9543 --ssl=yes
/etc/init.d/vmware-log-insight-agent status
```


```text title="Expected output"
Unpacking Agent Installer...
Verifying archive integrity... All good.
Extracting files...
Installing VMware Log Insight Agent version 8.8.1.21057892
Configuring agent for host: vrli-master.example.local:9543 (SSL enabled)
Creating user account 'liagent'...
Setting up log collectors...
Starting VMware Log Insight Agent service...
vmware-log-insight-agent is running (PID: 4827)
Agent successfully registered with master at vrli-master.example.local
```

!!! warning "Common errors"
    **`./VMware-Log-Insight-Agent-<version>.bin: Permission denied`** — Run `chmod +x VMware-Log-Insight-Agent-<version>.bin` before executing the installer.
    **`Error: Unable to connect to vrli-master.example.local:9543 (Connection refused)`** — Verify the VRLI master hostname/IP is correct and the service is listening on port 9543 with `telnet vrli-master.example.local 9543`.
    **`ERROR: Agent failed to register - SSL certificate verification failed`** — Add `--ssl-verify=no` flag to the installer command or ensure the VRLI master's SSL certificate is trusted on the agent host.
Syslog from network devices: point switches and firewalls at the VIP on UDP 514. For TLS syslog on port 6514, download the Aria Logs CA cert from Administration → SSL and install it on each source before enabling TCP 6514.

---

## Phase 5 — Content Packs, Alerts, and Forwarding

**Exit criterion:** VMware content packs are installed and dashboards show data. Alert queries are active. Log forwarding is configured if a SIEM is in scope.

```text
Administration → Content Packs → Marketplace
→ Install: VMware - vSphere      (ESXi, vCenter, vSAN log patterns)
→ Install: VMware - NSX-T        (DFW events, manager audit logs)
→ Install: Linux                 (auth, kernel, syslog patterns)
→ Install: Windows               (event log, application logs)
```

Configure alert queries:

```text
Alerts → Alert Definitions → New Alert
→ Name: ESXi-NFS-Latency
→ Query: text CONTAINS "NFS: Waiting too long for response"
→ Condition: Count > 5 per 5 minutes  ·  Severity: Warning

→ Name: vCenter-Auth-Failure
→ Query: appname = vpxd AND text CONTAINS "Login failure"
→ Condition: Count > 10 per 1 minute  ·  Severity: Critical

Notifications → Add: Email smtp.example.local:25 · Webhook Slack/PagerDuty
Forwarding → splunk-hf.example.local:514 · filter: tags CONTAINS "security"
Archiving → Active retention: 30 days · NFS archive for 90-day compliance tier
```

---

## Phase 6 — End-to-End Validation

**Exit criterion:** All checks below pass. Retention policy confirmed. Hand off to operations.

```bash
ssh root@vrli-master.example.local
li-admin cluster   # all nodes: ACTIVE, no MISSING_SHARDS
li-admin stats     # eventsPerSecond: > 0
li-admin disk      # /storage/core usage: < 80%
```


```text title="Expected output"
root@vrli-master.example.local's password: 
Welcome to vRealize Log Insight 8.14.0
vrli-master:~# li-admin cluster
Node Name                Status          Shards
vrli-master.example.local ACTIVE          128/128
vrli-node-2.example.local ACTIVE          128/128
vrli-node-3.example.local ACTIVE          128/128
Cluster Health: GREEN
vrli-master:~# li-admin stats
Events Per Second: 2847
Indexing Rate: 98.2%
Query Latency (avg): 342ms
Memory Usage: 62%
vrli-master:~# li-admin disk
Filesystem              Size    Used    Available   Use%
/storage/core          2.0T    1.4T    598G       72%
/storage/analytics     1.5T    892G    608G       59%
/var/log               50G     18G     32G        36%
```

!!! warning "Common errors"
    **`li-admin: command not found`** — SSH to the correct vRealize Log Insight master node or verify the admin CLI tools are installed in the PATH.
    **`MISSING_SHARDS detected on vrli-node-2.example.local`** — Run `li-admin cluster repair` and wait for shard rebalancing to complete before proceeding.
    **`/storage/core usage: 87%`** — Increase storage capacity or implement log retention policies to reduce disk usage below 80%.
```bash
# Confirm version and node health via API
curl -sk -u 'admin:<password>' \
  "https://vrli-master.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {hostname: .hostname, state: .state, version: .version}'
# Expected: all nodes state ACTIVE, versions identical
```


```text title="Expected output"
{
  "hostname": "vrli-master.example.local",
  "state": "ACTIVE",
  "version": "8.14.0.21567890"
}
{
  "hostname": "vrli-worker-01.example.local",
  "state": "ACTIVE",
  "version": "8.14.0.21567890"
}
{
  "hostname": "vrli-worker-02.example.local",
  "state": "ACTIVE",
  "version": "8.14.0.21567890"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the CA certificate into your system trust store.
    **`jq: parse error: Invalid JSON text at line 1`** — Verify the API endpoint is correct and the vRLI service is fully started; check logs with `tail -f /var/log/aria/vrli/api.log`.
    **`curl: (401) Unauthorized`** — Confirm the admin password is correct and URL-encoded if it contains special characters; test with `curl -sk -u 'admin:password' https://vrli-master.example.local/api/v2/system/info`.
| Check | Command / Location | Expected |
|---|---|---|
| All nodes Active | `li-admin cluster` | All nodes: ACTIVE, no missing shards |
| Ingestion rate > 0 | `li-admin stats` | eventsPerSecond non-zero |
| Disk < 80% | `li-admin disk` | Usage below threshold |
| ESXi syslog configured | `esxcli system syslog config get` | Remote host set on all hosts |
| CFAPI agents reporting | Administration → Agents | Agents visible and Active |
| vSphere content pack | Content Packs → Installed | VMware - vSphere present |
| NSX content pack | Content Packs → Installed | VMware - NSX-T present |
| Dashboards showing data | Dashboards → vSphere | Widgets populated |
| Alert test notification | Notifications → Test | Alert received at destination |
| SIEM forwarding active | Forwarding → Destinations | Status: Active |
| Retention policy set | Administration → Archiving | Days configured |

---

## See also

- [Aria Operations for Logs — How It Works](../architecture/how-it-works/)
- [Aria Operations for Logs — Health Checks](../operations/health-checks/)
- [Aria Operations for Logs — Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
