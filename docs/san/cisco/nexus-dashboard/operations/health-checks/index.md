# Cisco Nexus Dashboard — Operations Health Checks

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
```text
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
```

## Run This Routine

1. Nexus Dashboard UI → System → Services — verify all platform services show **Running**; any Stopped or Error state needs investigation
2. Nexus Dashboard → Sites — confirm all registered sites show **Connected**; Disconnected sites block policy deployment
3. NDFC → Fabric Builder → switch inventory — verify all fabric switches appear as **Managed** with no discovery errors
4. NDFC → Fabric → deployment status — check for any switches with **pending** or **failed** configuration deployments; resolve before next change window
5. Nexus Dashboard → Alerts → open alarms — filter Critical and Major severity; review, assign, and escalate unacknowledged alarms
6. NDFC → Operations → Backup — confirm last successful backup timestamp is within the last 24 hours; trigger manual backup if overdue
7. SSH to each ND node: `df -h /data` — alert and escalate if any node filesystem usage exceeds **80%** (Elasticsearch fills fast)

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# List recent backups
acs backup list

# Check backup destination
acs backup remote show
```
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
