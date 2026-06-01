# SRM Troubleshooting — Common Issues


<div class="kb-summary">
Common Issues reference covering Triage Decision Tree, Recovery Plan Fails at Network Mapping Step, SRA Communication Failure, Recovery Plan Stuck `Running`, Site Pair Shows `Error`.
</div>

## Triage Decision Tree

Use this flowchart to quickly route to the correct troubleshooting section.

```mermaid
flowchart TD
    start(["SRM alert or failure"])
    start --> q1{Where is\nthe failure?}

    q1 -->|"VM shows Not Ready\nor missing from PG"| vmNotReady["VM Not in PG\n/ Not Ready State"]
    q1 -->|"Recovery plan\nfailed mid-run"| planFailed{Which step\nfailed?}
    q1 -->|"Array Manager\nshows Error"| sraFail["SRA Communication\nFailure"]
    q1 -->|"Site Pair shows Error"| sitePair["Site Pair Error\n(cert / connectivity)"]

    planFailed -->|"Network mapping"| netMap["Recovery Plan\nNetwork Mapping step"]
    planFailed -->|"Plan stuck Running"| stuck["Recovery Plan\nStuck Running"]

    vmNotReady --> vr["Check vSphere Replication\nstatus + disk space + RPO"]
    sraFail --> sraLog["Check SRA service\n+ array API reachability"]
    sitePair --> cert["Check cert validity\n+ vCenter reachability port 443"]
    netMap --> netCheck["Verify all source networks\nhave target mappings"]
    stuck --> script["Check custom script\nexit code or VM power-on error"]

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    class vr,sraLog,cert,netCheck,script action
    class q1,planFailed decision
    class start terminal
```
┌───────────────────────────────────────── SRM — Common Issues ─────────────────────────────────────────┐
│                                                                                                       │
│   │     Symptom      │   Likely Cause   │    First Check    │       Fix        │      Verify      │   │
│   │    Plan fails    │   SRA timeout    │ check array repli │re-run or fix SRA │  srm-cli histor  │   │
│   │     VM no IP     │customization err │ check IP customiz │ fix NIC mapping  │    vmware.log    │   │
│   │    Test stuck    │snapshot not rele │    srm cleanup    │  force cleanup   │  srm-cli cleanu  │   │
│   │   Pair broken    │  cert mismatch   │ check SRM pairing │  re-pair sites   │  srm-cli site i  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     General Triage Pattern                                    │   │
│   │          Is the issue new or recurring? New = recent change; Recurring = config problem       │   │
│   │             Is it isolated to one source or all? Isolated = agent; All = server/repo          │   │
│   │                               Check logs first: srm-cli plan test                             │   │
│   │                    If unresolved in 2h: open vendor case with full log bundle                 │   │
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
```powershell

1. SRM → Configure → Array Managers → check status
2. Verify SRA service is running:
   ```powershell
   Get-Service vmware-sra-*   # Windows SRM
   ```
3. Re-test array credentials: Array Manager → Edit → Test Connection
4. Check SRA log for specific error (Dell SRA logs: see above path)
5. Verify Unisphere/FlashArray/ONTAP API is accessible from SRM server:
   ```powershell
   Invoke-WebRequest -Uri "https://<array-ip>/univmax/restapi/system/version" -SkipCertificateCheck
   ```

## Recovery Plan Stuck `Running`

```text
Cause: Custom script step timed out, or a VM failed to power on
```

1. SRM → Recovery Plans → running plan → Steps tab — identify which step is stuck
2. If a custom script step: check the script exit code in task details; a non-zero exit causes indefinite wait
3. If a VM power-on step: check vCenter tasks for that VM — may have a configuration issue (missing network, snapshot)
4. As a last resort (during actual DR): manually advance the plan past the stuck step using "Force Next Step"

## Site Pair Shows `Error`

```text
Cause: Certificate mismatch, vCenter connectivity, or credential expiry
```

1. From SRM server, verify vCenter is reachable:
   ```powershell
   Test-NetConnection -ComputerName <vcenter-fqdn> -Port 443
   ```
2. Check certificate validity:
   ```powershell
   $cert = [Net.ServicePointManager]::ServerCertificateValidationCallback
   Invoke-WebRequest "https://<vcenter-fqdn>" -UseBasicParsing
   ```
3. Re-enter site pair credentials: SRM → Sites → Edit Credentials
