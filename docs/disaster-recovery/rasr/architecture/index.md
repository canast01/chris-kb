# RASR — Architecture

<div class="kb-summary">
Dell RASR (Recovery and System Restore) bare-metal recovery for Windows Server — WinPE boot media, sector-level image capture, and iDRAC virtual media integration.
</div>

```
┌───────────────────────────────────────── RASR — Architecture ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 RASR — Component Architecture                                 │   │
│   │          Vault Appliance      — air-gapped PowerStore/DD in isolated network segment          │   │
│   │         CyberSense Engine    — ML-based malware and corruption detection on vault data        │   │
│   │         PowerProtect Manager — orchestrates replication jobs, retention, and recovery         │   │
│   │               Ports: 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Three-tier component model — control plane, data plane, and management                             │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Control Plane        │  │          Data Plane         │  │          Management         │   │
│   │ Vault Appliance      — air-g│  │ CyberSense Engine    — ML-ba│  │ Vault Lock           — immut│   │
│   │          Scheduling         │  │      Replication/Backup     │  │     443 (PPDM REST API)     │   │
│   │         Policy mgmt         │  │        Data movement        │  │           REST API          │   │
│   │          Catalog/DB         │  │        Dedup/compress       │  │             RBAC            │   │
│   │          Job engine         │  │       2049 (NFS vault)      │  │           Alerting          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────── RASR — Architecture ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 RASR — Component Architecture                                 │   │
│   │          Vault Appliance      — air-gapped PowerStore/DD in isolated network segment          │   │
│   │         CyberSense Engine    — ML-based malware and corruption detection on vault data        │   │
│   │         PowerProtect Manager — orchestrates replication jobs, retention, and recovery         │   │
│   │               Ports: 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Three-tier component model — control plane, data plane, and management                             │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Control Plane        │  │          Data Plane         │  │          Management         │   │
│   │ Vault Appliance      — air-g│  │ CyberSense Engine    — ML-ba│  │ Vault Lock           — immut│   │
│   │          Scheduling         │  │      Replication/Backup     │  │     443 (PPDM REST API)     │   │
│   │         Policy mgmt         │  │        Data movement        │  │           REST API          │   │
│   │          Catalog/DB         │  │        Dedup/compress       │  │             RBAC            │   │
│   │          Job engine         │  │       2049 (NFS vault)      │  │           Alerting          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![RASR Architecture](../../../assets/rasr-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Recovery workflow, WinPE environment, Dell hardware integration, and RASR vs alternatives.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>iDRAC virtual media, OpenManage, and network share integration.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Image naming, share layout, rotation policy, and testing schedule.</span></a>
</div>

| Component | Role |
|---|---|
| RASR Agent | Windows service on protected server; orchestrates image capture |
| RASR Boot Media | WinPE USB or ISO with PERC/NIC drivers; used for bare-metal recovery |
| Recovery Image | Compressed sector-level snapshot stored on SMB share |
| Network Recovery Share | SMB share where images are stored and retrieved |
| iDRAC Virtual Media | Mounts RASR ISO remotely — enables headless bare-metal recovery |


