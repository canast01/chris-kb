# Cisco Nexus Dashboard — Troubleshooting Escalation

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# 1. Platform version
acs version

# 2. Installed app versions
acs apps status

# 3. Cluster health at time of issue
acs health
acs nodes list

# 4. Support bundle (primary artifact for TAC)
acs techsupport --output /tmp/nd-support-$(date +%Y%m%d).tar.gz
# Transfer to workstation:
scp ndadmin@nd-dc1-1.corp.example.com:/tmp/nd-support-$(date +%Y%m%d).tar.gz ./

# 5. Resource state
acs system resources

# 6. Kubernetes event log
kubectl get events --all-namespaces --sort-by='.lastTimestamp' > /tmp/k8s-events-$(date +%Y%m%d).txt
```
```text
┌───────────────────────── Cisco Nexus Dashboard — Troubleshooting Escalation ──────────────────────────┐
│                                                                                                       │
│  Escalation path for ND: internal triage → Cisco TAC → cluster restore or rebuild.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Internal Triage (L1/L2)            │  │                Cisco TAC (L3)               │   │
│   │         Confirm impact: cluster/app          │  │            Open SR: severity 1-4            │   │
│   │           Collect: acs techsupport           │  │          Upload bundle to CX Cloud          │   │
│   │         Check: recent config changes         │  │          TAC WebEx: remote session          │   │
│   │        Check: Cisco PSIRT advisories         │  │         Patch or restore if directed        │   │
│   │         Try: acs restart failing app         │  │         Rebuild cluster: last resort        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Collect tech-support before any restart; TAC needs state data from failure moment                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Criteria              │  │               Recovery Actions              │   │
│   │         Sev 1: all apps unavailable          │  │           App restart: acs restart          │   │
│   │            Sev 2: one app failed             │  │         Backup restore: full cluster        │   │
│   │          Sev 3: degraded telemetry           │  │         Node replace: rejoin cluster        │   │
│   │            Sev 4: config question            │  │          Rebuild: deploy + restore          │   │
│   │           Always document timeline           │  │          Post-mortem: RCA document          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · backup storage · management network · spare node for rebuild                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SR             = Service Request; Cisco TAC case number                                              │
│  TAC            = Technical Assistance Center; Cisco L3 support                                       │
│  CX Cloud       = Cisco portal for SR management and tech-support file upload                         │
│  PSIRT          = Cisco security advisory team; check for relevant CVEs first                         │
│  acs restart    = Gracefully restarts a named ND app without rebooting the node                       │
│  Backup restore = Full cluster config recovery from most recent scheduled backup                      │
│  Node replace   = Remove failed node, add new node, rejoin cluster automatically                      │
│  Rebuild        = Deploy fresh cluster and restore from backup; last-resort recovery                  │
│  Severity 1     = Production down; Cisco SLA: 1-hour initial response                                 │
│  RCA            = Root Cause Analysis; post-incident document for future prevention                   │
│  Timeline       = Chronological log of symptoms, actions, and outcomes for TAC                        │
│  Tech-support   = Collected before any recovery action; preserves failure state                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# etcd health (collect from each node)
for node in nd-dc1-1 nd-dc1-2 nd-dc1-3; do
  ssh ndadmin@${node}.corp.example.com \
    "ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \
     --key=/etc/kubernetes/pki/etcd/server.key \
     endpoint status --write-out=table" > /tmp/etcd-${node}.txt 2>&1
done
```
```bash
# Upgrade log
acs upgrade history > /tmp/upgrade-history.txt
acs system logs --component upgrade --tail 200 > /tmp/upgrade-log.txt

# Include: source ND version, target version, app versions pre-upgrade
# Include: exact error message shown during upgrade
```
```yaml
Product: Cisco Nexus Dashboard
Platform version: 3.x.x (acs version output)
NDFC version: 12.x.x (acs apps status output)
NDI version: 6.x.x (if installed)
Deployment type: 3-node VMware OVA / 3-node physical (UCS C220 M6)
Managed switches: [MDS 9710 x2, MDS 9396T x4, NX-OS 8.4(2a)]

Problem description:
[Concise description of the symptom — what is failing or degraded]

Business impact:
[e.g., "NDFC cannot push zone changes to any fabric; fabric is operational
 but all SAN management operations are blocked"]

When did the issue start:
[Date and time — timezone — what was happening at that time]

What changed before the issue:
[e.g., "ND platform upgraded from 3.0.1 to 3.1.1 at 14:00 UTC on 2026-05-07"]

Troubleshooting already performed:
1. [what was checked]
2. [what was tried]
3. [result]

Attachments:
- nd-support-20260508.tar.gz (ND support bundle)
- ndfc-support-20260508.tar.gz (NDFC support bundle)
- k8s-events-20260508.txt
- [any screenshots of error messages]
```
