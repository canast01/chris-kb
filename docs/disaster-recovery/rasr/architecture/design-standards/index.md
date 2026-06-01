# RASR — Standards


<div class="kb-summary">
> Part of the [RASR Architecture](../index.md) reference.
</div>

---

Standards for RASR deployment, image management, testing, and recovery readiness across Dell PowerEdge environments.

## Backup Frequency Standards

| Server criticality | Capture frequency | Retention |
|---|---|---|
| **Tier 1** — production database/app servers | Daily, after patch events | 7 daily + 4 weekly |
| **Tier 2** — secondary production servers | Weekly | 4 weekly + 2 monthly |
| **Tier 3** — non-production | Monthly or post-build | 3 monthly |
| **Any tier** — after OS change | Within 24 hours of change | Retain indefinitely until next planned capture |

Always capture immediately after:
- OS patching and reboot
- Driver or firmware updates
- Application installation on the OS volume
- System configuration changes

## Image Naming Convention

```text
Format: <hostname>_<environment>_<date>_<sequence>

Examples:
  app01_prod_20260510_001.wim
  db02_prod_20260503_weekly.wim
  dc01_prod_20260101_post-patch.wim
```
```
┌─────────────────────────────────────── RASR — Design Standards ───────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Sizing Guidelines               │  │               HA Requirements               │   │
│   │         Deduplicate where supported          │  │           N+1 component redundancy          │   │
│   │          Bandwidth: 10 GbE minimum           │  │          Heartbeat / health monitor         │   │
│   │          Storage: 130% of raw data           │  │          Separate mgmt / data VLANs         │   │
│   │         Latency: < 10 ms to storage          │  │          Out-of-band access (IPMI)          │   │
│   │           CPU: 8+ vCPU for engine            │  │          Anti-affinity VM placement         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Ports: 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)                                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Standard RASR Design Rules                                  │   │
│   │            RPO target drives snapshot/cycle frequency — document in service design            │   │
│   │            RTO target drives recovery tier: instant, warm standby, or cold restore            │   │
│   │                  Dedicated backup network VLAN — no shared production traffic                 │   │
│   │  Encryption: AES-256 at rest on vault; TLS 1.3 for all mgmt; vault lock enforces immutability │   │
│   │               Service accounts: minimum privilege; rotate credentials quarterly               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
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
```

## Access Control Standards

| Access type | Who | Permission level |
|---|---|---|
| Recovery share — write | RASR service account only | Write to server-specific subfolder |
| Recovery share — read | Recovery operators, DR team | Read-only across all subfolders |
| iDRAC virtual media | DR team, platform leads | Map/mount virtual media |
| RASR Console | Server administrators | Local admin on protected server |
| Boot media ISO | All operators | Read from share |

The RASR service account must not have local admin rights beyond what RASR requires. It should not have interactive logon rights.

## Documentation Requirements

For each protected server, maintain:

1. **Recovery card** — physical or digital record containing:
   - Server hostname and iDRAC IP
   - Recovery share path
   - Last successful backup date
   - Recovery operator contact

2. **Image log** — spreadsheet or CMDB entry tracking:
   - Image filename
   - Capture date
   - OS version and patch level at time of capture
   - Capture trigger (scheduled / post-patch / manual)

3. **Test evidence** — for each test:
   - Date, tester name, test type
   - Pass/fail result
   - Time to complete restore
   - Issues found and resolution

## Monitoring and Alerting

| Alert | Threshold | Destination |
|---|---|---|
| Backup not completed | > 26 hours since last successful image | Email to platform team |
| Agent service not running | RASRAgent stopped | SNMP trap + email |
| Share space < 20% | Recovery share below 20% free | Email to storage team |
| Test overdue | > 90 days since last boot test | Ticketing system (auto-created) |
