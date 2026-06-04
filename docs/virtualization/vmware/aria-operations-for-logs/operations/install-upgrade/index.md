# Aria Operations for Logs — Install and Upgrade

```bash
# From master node — confirm all cluster members
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, role: .role}'
```text
┌─────────────────────────── Aria Operations for Logs — Install and Upgrade ────────────────────────────┐
│                                                                                                       │
│  vRLI is installed via OVA in vCenter; upgrades use PAK file uploaded to VAMI or LCM.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Pre-Install Requirements           │  │                Install Steps                │   │
│   │          DNS: FQDN fwd+rev for vRLI          │  │            Deploy OVA in vCenter            │   │
│   │          NTP: appliance time synced          │  │       VAMI first-boot: set IP/FQDN/NTP      │   │
│   │         Storage: 1 TB+ for log data          │  │          License: activate in VAMI          │   │
│   │       Firewall: 514/6514/443/9543 open       │  │       vSphere integration: add vCenter      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Upgrade via PAK file in VAMI or managed by LCM; take VM snapshot before upgrading.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Process                │  │           Post-Upgrade Validation           │   │
│   │       1. Snapshot master (and workers)       │  │           Cluster: all nodes green          │   │
│   │       2. Upload PAK to VAMI or use LCM       │  │        Ingestion: events/sec resumed        │   │
│   │    3. Upgrade master first, then workers     │  │        Alerts: all enabled and firing       │   │
│   │       4. Monitor VAMI upgrade progress       │  │       SSO and forwarding: verified OK       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI OVA/PAK · vCenter · datastore ≥1 TB · DNS/NTP · LCM (optional managed upgrade)                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA               = Open Virtual Appliance; initial install format for vRLI                          │
│  PAK file          = vRLI upgrade package; upload to VAMI Administration → Upgrade                    │
│  VAMI              = Virtual Appliance Management Interface; configure vRLI at :9543                  │
│  LCM managed       = Aria Suite LCM can install and upgrade vRLI in managed environments              │
│  vSphere integration= Add vCenter to vRLI; auto-deploys vSphere agent to ESXi hosts                   │
│  Syslog ports      = UDP/TCP 514 (plaintext) and TCP 6514 (TLS); must be open in firewall             │
│  Upgrade sequence  = Master upgraded first; workers must be on same version as master                 │
│  VM snapshot       = Pre-upgrade rollback point; delete after 48h if upgrade successful               │
│  License           = vRLI license activated in VAMI; free tier: 25 OSI included                       │
│  Post-upgrade check= Verify cluster, ingestion, alerts, and forwarding all functional                 │
│  Worker join       = Worker nodes re-join cluster automatically after upgrade                         │
│  OSI               = Operationally Significant Instance; licensed unit in vRLI                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Confirm version
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/version" | jq '.version'

# Confirm cluster health
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, version: .version}'

# Confirm ingestion is running
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/stats" | \
  jq '.eventsIngested'
```
