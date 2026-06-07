# RASR

<div class="kb-summary">
Dell RASR (Recovery and System Restore) bare-metal recovery for Windows Server — WinPE boot media, sector-level image capture, and iDRAC virtual media for headless recovery.
</div>

```text
┌─────────────────────────────────────────── RASR — Overview ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                              RASR                                             │   │
│   │         Ransomware Air-gap Secure Recovery — isolated vault with CyberSense analytics         │   │
│   │          Vault Appliance      — air-gapped PowerStore/DD in isolated network segment          │   │
│   │         CyberSense Engine    — ML-based malware and corruption detection on vault data        │   │
│   │         PowerProtect Manager — orchestrates replication jobs, retention, and recovery         │   │
│   │   Management: 443 (PPDM REST API) · Auth: Vault operator role; 2-person integrity for unlock  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture: components work together to deliver RASR capabilities                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                  Operations                 │   │
│   │ Vault Appliance      — air-gapped PowerStor  │  │              cr_vault_cli sync              │   │
│   │ CyberSense Engine    — ML-based malware and  │  │             cr_vault_cli status             │   │
│   │ PowerProtect Manager — orchestrates replica  │  │               cybersense scan               │   │
│   │ Vault Lock           — immutable WORM lock   │  │             vault lock / unlock             │   │
│   │ Clean Room           — isolated vCenter + w  │  │               ppdm recover vm               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
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

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Recovery workflow, WinPE environment, Dell hardware integration, and RASR vs alternatives.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, recovery procedures, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
