# RASR — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Architecture, Network Recovery Share Requirements, RASR vs Alternative Methods.
</div>

## Overview

RASR (Recovery and System Restore) is Dell's bare-metal recovery tool for Windows Server, shipped as part of the Dell OpenManage suite. It captures a full sector-level system image — including the OS volume, boot partition, and system state — and restores it to original or replacement hardware via a WinPE boot environment, without requiring a pre-installed OS. RASR is the last-resort bare-metal recovery mechanism for physical Dell PowerEdge servers.

## Architecture

| Component | Description |
|---|---|
| RASR Agent | Windows service (`RASRAgent`) on each protected server; orchestrates image capture |
| RASR Console | GUI within Windows for initiating backups and managing recovery media |
| Recovery Image | Sector-level snapshot of system volume(s) in `.wim` or proprietary RASR format |
| Recovery Media | Bootable WinPE USB drive or ISO; contains RASR engine and Dell hardware drivers |
| Network Recovery Share | SMB share where recovery images are stored and retrieved |

```text
Protected Windows Server
├── RASR Agent (RASRAgent Windows service)
├── RASR Console (GUI in Windows)
└── Captured Image → Network Recovery Share (SMB)

Recovery Media (USB / iDRAC virtual ISO)
└── WinPE boot environment
      └── RASR Recovery Engine + Dell hardware drivers
```
┌───────────────────────────────────────── RASR — How It Works ─────────────────────────────────────────┐
│                                                                                                       │
│    RASR data flow — from source to target through the protection pipeline:                            │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 1  Source / Production System                                 │   │
│   │            Vault Appliance      — air-gapped PowerStore/DD in isolated network segment        │   │
│   │                Host writes are intercepted or snapshotted by the RASR agent/proxy             │   │
│   │                  Changed blocks tracked via CBT / journal / delta-set mechanism               │   │
│   │                 Consistency ensured at quiesce point before data transfer begins              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Changed data forwarded to the RASR engine — compression and encryption applied in transit          │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                         2  RASR Engine                                        │   │
│   │          CyberSense Engine    — ML-based malware and corruption detection on vault data       │   │
│   │                    Data compressed, deduplicated, and encrypted before storage                │   │
│   │                  Metadata catalog updated; job status reported to control plane               │   │
│   │                                         cr_vault_cli sync                                     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     3  Target / Repository                                    │   │
│   │           PowerProtect Manager — orchestrates replication jobs, retention, and recovery       │   │
│   │                  Recovery point written; retention policy applied automatically               │   │
│   │                                   Restore: cr_vault_cli status                                │   │
│   │                     RTO driven by target storage performance and data volume                  │   │
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

## Network Recovery Share Requirements

| Requirement | Detail |
|---|---|
| Protocol | SMB 2.0 or later |
| Permissions | Read/write for RASR service account; read for recovery operators |
| Path example | `\\nas01\rasr-images\server01\` |
| Minimum free space | 2× the compressed image size (image + staging) |

## RASR vs Alternative Methods

| Capability | RASR | Windows Server Backup | Commvault BMR | Veeam BMR |
|---|---|---|---|---|
| Bare-metal to physical | Yes | Yes | Yes | Yes |
| Dell hardware driver integration | Native | Manual | Manual | Manual |
| iDRAC boot integration | Yes | No | No | No |
| Application-aware backup | No | Limited | Yes | Yes |
| Granular file restore | No | Yes | Yes | Yes |
| Suitable for DR-only physical | Yes | Yes | No (licensed) | No (licensed) |
