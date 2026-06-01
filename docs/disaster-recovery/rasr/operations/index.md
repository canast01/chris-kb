# RASR — Operations



<div class="kb-summary">
RASR — Operations reference.
</div>

```
┌────────────────────────────────────────── RASR — Operations ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  RASR — Day-to-Day Operations                                 │   │
│   │          Daily: review job status · check health alerts · verify last backup/replica          │   │
│   │            Weekly: review capacity trends · test restore sample · review error logs           │   │
│   │             Monthly: full restore test · review retention · audit service accounts            │   │
│   │              Quarterly: DR failover test · firmware review · update documentation             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Backup/Replicate      │  │           Monitor           │  │           Recover           │   │
│   │      cr_vault_cli sync      │  │       cybersense scan       │  │     cr_vault_cli status     │   │
│   │        Schedule jobs        │  │        Health checks        │  │       Instant restore       │   │
│   │        Retention mgmt       │  │       Capacity alerts       │  │        Failover test        │   │
│   │       Consistency grp       │  │          Log review         │  │          DR runbook         │   │
│   │        Policy updates       │  │         SLA tracking        │  │         Validate RTO        │   │
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
┌────────────────────────────────────────── RASR — Operations ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  RASR — Day-to-Day Operations                                 │   │
│   │          Daily: review job status · check health alerts · verify last backup/replica          │   │
│   │            Weekly: review capacity trends · test restore sample · review error logs           │   │
│   │             Monthly: full restore test · review retention · audit service accounts            │   │
│   │              Quarterly: DR failover test · firmware review · update documentation             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Backup/Replicate      │  │           Monitor           │  │           Recover           │   │
│   │      cr_vault_cli sync      │  │       cybersense scan       │  │     cr_vault_cli status     │   │
│   │        Schedule jobs        │  │        Health checks        │  │       Instant restore       │   │
│   │        Retention mgmt       │  │       Capacity alerts       │  │        Failover test        │   │
│   │       Consistency grp       │  │          Log review         │  │          DR runbook         │   │
│   │        Policy updates       │  │         SLA tracking        │  │         Validate RTO        │   │
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
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>RASR boot and recovery command reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Media validation and recovery readiness checks.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>RASR recovery procedures and restore workflows.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install &amp; Upgrade</strong>
  <span>RASR media creation and version management.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup &amp; Restore</strong>
  <span>Appliance restore and recovery procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for RASR operations.</span>
</a>

</div>
