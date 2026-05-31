# SRM Troubleshooting — Escalation

```text
┌────────────────────────────────────────── SRM — Escalation ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     SRM — Escalation Path                                     │   │
│   │              L1 Triage: review logs, match to known issues in runbook (0–30 min)              │   │
│   │         L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)         │   │
│   │             Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)             │   │
│   │            Sev1 (data loss / production impact): page on-call + open critical case            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Information to Collect Before Escalating                           │   │
│   │                 Product version: SRM version string from About / version command              │   │
│   │                                Full log bundle: srm-cli plan test                             │   │
│   │                     Symptom timeline: when first occurred; any changes made                   │   │
│   │                Scope: single job / all jobs / all components — narrows root cause             │   │
│   │                    Error codes: exact error messages and exit codes from logs                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
VMware SRM support cases are opened via the Broadcom Support Portal (support.broadcom.com) under the VMware vSphere product family. For production DR failures, open a Critical (Severity 1) case to engage 24×7 response. Collect the SRM support bundle before calling — it includes SRM server logs, vSphere Replication logs, and configuration exports.

**Required information for SR:**

| Item | How to Collect |
|---|---|
| SRM version | SRM UI → Summary tab or `SRM-support-bundle` |
| vCenter version | vCenter UI → About |
| SRA name and version | SRM UI → Array Managers |
| Protection group count and states | SRM UI → Protection Groups (screenshot or export) |
| SRM support bundle | vCenter UI → SRM plugin → Support Bundle → Generate |
| vSphere Replication logs | vSphere Replication appliance → Support → Download Log Bundle |

**Support process:**
- **Broadcom Support Portal**: support.broadcom.com → My Cases → Create Case.
- **Severity 1 (Critical)**: Production DR system down; 24×7 engineer engagement; 30-minute callback SLA.
- **Severity 2 (Major)**: DR degraded with workaround; business hours response.
- **Premier Support**: Designated support account manager; faster escalation path for P1.
