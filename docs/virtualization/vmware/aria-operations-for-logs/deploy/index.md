---
tags:
  - aria-logs
  - deployment
  - vmware
---
# Aria Operations for Logs — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Aria Operations for Logs (vRLI). Covers prerequisites, master node OVA deployment, worker cluster setup, syslog and CFAPI agent configuration, content pack installation, and end-to-end validation.

*Applies to: Aria Logs 8.x*
</div>

```text
┌──────────────────────────── Aria Operations for Logs — Deployment Phases ─────────────────────────────┐
│                                                                                                       │
│  Six phases from prerequisites to a fully operational log analytics cluster. Each phase has a clear   │
│  exit criterion. Do not proceed until the current phase validates clean.                              │
│                                                                                                       │
│   ┌───────────────────────────┐  ┌────────────────────────────┐  ┌────────────────────────────────┐   │
│   │   Phase 1: Pre-Deploy     │  │   Phase 2: Master Node     │  │  Phase 3: Worker Nodes         │   │
│   │  DNS: A + PTR for nodes   │  │  Deploy OVA in vCenter     │  │  Deploy worker OVAs            │   │
│   │  NTP: confirmed on net    │  │  VAMI first-boot wizard    │  │  Join Cluster via setup wizard │   │
│   │  Firewall: 514/6514 open  │  │  Role: New Deployment      │  │  Active-active cluster mode    │   │
│   │  Datastore: ≥530 GB/node  │  │  Accept EULA + licence     │  │  Verify all nodes: Active      │   │
│   │  Ingest rate estimated    │  │  Master node: Running      │  │  No missing shards             │   │
│   └───────────────────────────┘  └────────────────────────────┘  └────────────────────────────────┘   │
│                                                                                                       │
│                ▼                              ▼                                ▼                      │
│                                                                                                       │
│   ┌───────────────────────────┐  ┌────────────────────────────┐  ┌────────────────────────────────┐   │
│   │  Phase 4: Log Sources     │  │  Phase 5: Content Packs    │  │  Phase 6: Validation           │   │
│   │  & Agent Install          │  │  Alerts & Forwarding       │  │                                │   │
│   │  vSphere integration      │  │  Install vSphere/NSX packs │  │  li-admin cluster status       │   │
│   │  ESXi syslog auto-config  │  │  Configure alert queries   │  │  Ingest rate: non-zero         │   │
│   │  CFAPI agents on VMs      │  │  Set notification channels │  │  Explore Logs shows data       │   │
│   │  Syslog: switches/FWs     │  │  Log forwarding to SIEM    │  │  Alert test notification sent  │   │
│   │  TLS syslog on port 6514  │  │  Retention policy set      │  │  Retention policy confirmed    │   │
│   └───────────────────────────┘  └────────────────────────────┘  └────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure: Aria Logs VMs (master + workers) · large /storage/core disk                 │
│  Syslog network paths from all sources · vCenter for agent auto-deploy · DNS/NTP                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CFAPI agent  = Log agent on VMs; forwards structured logs to master on TCP 9543                      │
│  Content pack = Pre-built dashboards, queries, and alerts for a specific product                      │
│  li-admin     = Aria Logs admin CLI on master; cluster status, disk usage, configuration              │
│  VIP          = Virtual IP; single ingestion endpoint shared across all cluster nodes                 │
│  OSI          = Operationally Significant Instance; licensed unit (one OSI = one log-sending host)    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

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

### CFAPI Agent on Linux VMs

```bash
# Download agent: Administration → Agents → Download Agent
chmod +x VMware-Log-Insight-Agent-<version>.bin
./VMware-Log-Insight-Agent-<version>.bin -- \
  --ip vrli-master.example.local --port 9543 --ssl=yes
/etc/init.d/vmware-log-insight-agent status
```

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

```bash
# Confirm version and node health via API
curl -sk -u 'admin:<password>' \
  "https://vrli-master.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {hostname: .hostname, state: .state, version: .version}'
# Expected: all nodes state ACTIVE, versions identical
```

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

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
