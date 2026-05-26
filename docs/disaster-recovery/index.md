# Disaster Recovery

## Site Topology
```
┌────────────────────────────────────────── Disaster Recovery ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Disaster Recovery — overview of all DR tools, replication methods, and recovery procedures  │   │
│   │                   See product-specific sub-sections for detailed procedures                   │   │
│   │          DR success depends on: documented runbooks · tested failover · validated RTO         │   │
│   │          Minimum DR posture: defined RPO/RTO · tested backups · known escalation path         │   │
│   │        Test DR procedures quarterly; document results; update runbooks after each test        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Production site · DR site · Replication link · Management network · Vault network                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO           = Recovery Point Objective; max acceptable data loss window                            │
│  RTO           = Recovery Time Objective; max acceptable downtime before restore                      │
│  Failover      = activating the DR site; redirecting hosts to replica resources                       │
│  Failback      = returning operations to production site after DR resolved                            │
│  Runbook       = step-by-step documented procedure for a specific DR scenario                         │
│  IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery                    │
│  Clean Room    = isolated vCenter + workstations for cyber recovery validation                        │
│  Air Gap       = network isolation preventing attacker lateral movement to vault                      │
│  DR Test       = planned failover test; validates RTO without real disaster                           │
│  Replication   = continuous or periodic data copy to secondary site or vault                          │
│  Recovery Tier = classification: hot/warm/cold based on RTO requirement                               │
│  BIA           = Business Impact Analysis; drives RPO/RTO targets per system                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="srdf-s/"><strong>SRDF/S</strong><span>Dell SRDF Synchronous — zero RPO replication between PowerMax arrays.</span></a>
<a class="kb-card" href="srdf-a/"><strong>SRDF/A</strong><span>Dell SRDF Asynchronous — configurable RPO replication with delta-set consistency.</span></a>
<a class="kb-card" href="recoverpoint/"><strong>RecoverPoint</strong><span>Dell continuous data protection and journal-based replication for VMware and physical workloads.</span></a>
<a class="kb-card" href="srm/"><strong>SRM</strong><span>VMware Site Recovery Manager — orchestrated VM failover and failback across vSphere sites.</span></a>
<a class="kb-card" href="superna-eyeglass/"><strong>Superna Eyeglass</strong><span>DR orchestration and failover automation for Dell PowerScale (Isilon) NAS environments.</span></a>
</div>

## Backup Platforms

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="veeam/"><strong>Veeam</strong><span>VM backup, replication, and instant recovery for VMware, Hyper-V, and cloud workloads.</span></a>
<a class="kb-card" href="netbackup/"><strong>NetBackup</strong><span>Veritas enterprise backup for VMs, databases, physical servers, and cloud workloads.</span></a>
<a class="kb-card" href="commvault/"><strong>CommVault</strong><span>Enterprise data protection platform for VMs, databases, NAS, and cloud with IntelliSnap integration.</span></a>
</div>

## Procedures

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="failover-procedure/"><strong>Failover Procedure</strong><span>Steps to activate DR site and restore service during a primary site outage.</span></a>
<a class="kb-card" href="failback-procedure/"><strong>Failback Procedure</strong><span>Steps to return workloads to primary site after a DR failover event.</span></a>
<a class="kb-card" href="runbook/"><strong>Runbook</strong><span>Step-by-step DR execution guide covering failover, validation, failback, and communication.</span></a>
<a class="kb-card" href="isolated-recovery-environment-ire/"><strong>Isolated Recovery Environment</strong><span>Air-gapped recovery environment for ransomware and cyber recovery scenarios.</span></a>
<a class="kb-card" href="rasr/"><strong>RASR</strong><span>Dell Rapid Appliance Self Recovery for bare-metal OS and appliance recovery.</span></a>
</div>
