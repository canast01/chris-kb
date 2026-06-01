# Nexus Dashboard — Health Checks


<div class="kb-summary">
> Part of the [Nexus Dashboard](../../index.md) reference.
</div>

---

## Overview

Run these checks on a scheduled basis — daily for active SAN environments, weekly minimum for all production ND clusters. Checks are performed via the Nexus Dashboard UI, CLI (`ndadmin`), and REST API.

---

## 1. ND Cluster Node Health

### UI

Navigate to **Admin Console > Infrastructure > Cluster Configuration** or **Admin Console > System > Nodes**:
- All nodes should show **Healthy** status (green)
- No node should be in **Unknown**, **Unavailable**, or **Degraded** state
- CPU and memory usage per node should be below 80%

### CLI (ndadmin)

```bash
# SSH to any cluster node
ssh ndadmin@nd-dc1-1.corp.example.com

# Show cluster health summary
acs health

# Show all nodes
acs nodes list
# Expected: all nodes in Active or Standby state, no Unhealthy

# Show app deployment status
acs apps status
# Expected: all apps in Running state (NDFC, NDI if installed)

# Show any failing Kubernetes pods
kubectl get pods --all-namespaces | grep -Ev "Running|Completed"
# Zero output = all pods healthy; any output needs investigation
```
┌────────────────────────── Cisco Nexus Dashboard — Operations Health Checks ───────────────────────────┐
│                                                                                                       │
│  Routine health verification covering cluster nodes, hosted apps, and connected sites.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Cluster Health Checks             │  │              App Health Checks              │   │
│   │         acs health: all nodes green          │  │          NDFC: SAN services running         │   │
│   │            Node CPU/memory < 70%             │  │         NDI: telemetry collection on        │   │
│   │         Disk usage < 80% on all vols         │  │           NDO: site sync status OK          │   │
│   │          NTP: all nodes synced < 1s          │  │        Pods: all Running, none Error        │   │
│   │        etcd: leader elected + healthy        │  │        App version: check for updates       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cluster health verified before app health; failing node impacts all apps                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Site Connectivity Checks           │  │            Security Health Checks           │   │
│   │         All sites: Connected status          │  │         SSL certs: expiry > 30 days         │   │
│   │         Fabric site: APIC version OK         │  │            AAA servers: reachable           │   │
│   │         Telemetry: data flowing NDI          │  │           RBAC: review user access          │   │
│   │           Latency: < 150ms to site           │  │           Audit log: no anomalies           │   │
│   │          Backup: last success < 24h          │  │         Backup: encryption verified         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · management switch · NTP server · APIC · AAA server · backup target                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  acs health     = ND CLI command showing cluster node and service health summary                      │
│  etcd leader    = Elected node managing all etcd writes; loss blocks cluster updates                  │
│  NTP sync       = All nodes must agree on time within 1 second for TLS to work                        │
│  Pod state      = Kubernetes pod lifecycle: Pending → Running → Error/CrashLoopBackOff                │
│  NDO site sync  = Verification that template state matches deployed APIC config                       │
│  NDI telemetry  = Streaming flow and latency data from switches to NDI analytics                      │
│  SSL expiry     = TLS cert expiration causing connection failures if not renewed                      │
│  AAA reachable  = RADIUS/TACACS+ server responds; local fallback active if not                        │
│  Audit log      = Records of all user actions and API calls for compliance review                     │
│  Disk usage     = Storage consumed on each ND node; Elasticsearch fills fast                          │
│  Latency 150ms  = Recommended maximum RTT between ND cluster and remote site                          │
│  Backup success = Verification that scheduled backup completed and is retrievable                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## 3. Fabric Discovery Status (NDFC)

Navigate to **NDFC > Fabrics > [Fabric Name]**:
- All switches should be in **Manageable** or **Managed** state
- Switch count should match expected
- No switches in **Unmanageable** or **Unreachable** state

If switches are unmanageable:
1. Verify SSH from ND data network to switch management IP
2. Verify SNMPv3 credentials match switch configuration
3. Check NDFC discovery logs:
   ```bash
   kubectl logs -n ndfc deployment/ndfc-discovery-manager --tail=100 | grep -i "error\|fail"
   ```

---

## 4. NDI Anomaly Review

Navigate to **NDI > Dashboard**:
- Review the anomaly count by severity (Critical, Major, Warning)
- Drill into Critical anomalies — these require active investigation
- Review the anomaly trend over the past 24 hours (increase may indicate an emerging issue)

Navigate to **NDI > Explore > Anomalies**:
- Filter by time: Last 24 Hours
- Sort by severity
- For each Critical or Major anomaly: confirm whether it is a known/acknowledged condition or a new finding

---

## 5. VSAN and Zone Set Health (NDFC SAN)

Navigate to **NDFC > Fabrics > [Fabric] > VSANs**:
- All production VSANs should be **Active** on all member switches
- No VSAN isolation events in the last 24 hours

Navigate to **NDFC > Fabrics > [Fabric] > Zoning**:
- The correct zone set is active in each VSAN
- Zone member counts match expectations

```bash
# Cross-check zone set on MDS switch directly
# (NX-OS CLI)
show zoneset active vsan 10
# Verify against NDFC-reported active zone set
```

---

## 6. ISL Utilization Review (NDFC)

Navigate to **NDFC > Fabrics > [Fabric] > ISLs**:
- All ISLs should be in **Up** state
- Review utilization columns — any ISL consistently above 70% requires capacity review

For historical trending:
- Navigate to **NDFC > Monitor > Performance > ISLs**
- Set time range to **Last 7 Days**
- Identify peak utilization periods and whether they are growing

---

## 7. Active Alarms (NDFC)

Navigate to **NDFC > Monitor > Alarms > Active Alarms**:

| Severity | Action |
|---|---|
| Critical | Immediate investigation |
| Major | Investigate within 4 hours |
| Minor | Review daily |

Acknowledge alarms that are actively being investigated. Clear alarms where the underlying condition has been resolved. Unacknowledged alarms accumulate and mask new events.

---

## 8. Backup Status

Navigate to **Admin Console > Operations > Backup & Restore**:
- Confirm the last scheduled backup completed successfully
- Backup age should be within the configured frequency window (weekly = should be ≤ 8 days old)
- Remote backup destination should be configured (not local-only)

From CLI:
```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# List recent backups
acs backup list

# Check backup destination
acs backup remote show
```

---

## 9. Certificate Expiry Check

```bash
# Check ND UI certificate expiry
openssl s_client -connect nd-dc1.corp.example.com:443 \
  -servername nd-dc1.corp.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -dates

# Days until expiry
python3 -c "
from datetime import datetime
import subprocess, re
r = subprocess.run(['openssl','s_client','-connect','nd-dc1.corp.example.com:443',
  '-servername','nd-dc1.corp.example.com'], capture_output=True, input=b'')
c = subprocess.run(['openssl','x509','-noout','-enddate'], input=r.stdout, capture_output=True).stdout.decode()
d = re.search(r'notAfter=(.*)', c).group(1).strip()
exp = datetime.strptime(d, '%b %d %H:%M:%S %Y %Z')
print(f'Expires in {(exp - datetime.utcnow()).days} days ({exp.date()})')
"
# Alert if < 60 days remaining
```

---

## 10. NTP Synchronization

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Check NTP status
acs system ntp show
# Expected: all configured NTP servers reachable, synchronized

# Check cluster time consistency across nodes
acs nodes list --format json | python3 -c "
import sys, json
nodes = json.load(sys.stdin)
for n in nodes:
    print(n.get('hostname'), n.get('currentTime'))
"
# All nodes should show times within 1 second of each other
```

---

## Weekly Health Check Summary

| Check | Pass Criterion | Location |
|---|---|---|
| All ND nodes healthy | All: Healthy | Admin Console > Nodes |
| All NDFC app pods Running | 0 non-Running pods | kubectl / Admin Console |
| All switches manageable | 0 Unmanageable | NDFC > Fabrics |
| All VSANs active | 0 Isolated VSANs | NDFC > VSANs |
| All ISLs up | 0 ISL down | NDFC > ISLs |
| ISL utilization | No ISL > 70% sustained | NDFC > Performance |
| NDI anomalies reviewed | 0 unacknowledged Critical | NDI > Anomalies |
| No unacknowledged NDFC critical alarms | 0 | NDFC > Alarms |
| Backup successful | ≤ 8 days old | Admin Console > Backup |
| NTP synchronized | Yes, < 50ms offset | ndadmin CLI |
| TLS certificate | > 60 days remaining | openssl CLI |
