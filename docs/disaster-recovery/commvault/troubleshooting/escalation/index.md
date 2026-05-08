# Commvault — Escalation

CommVault support is accessed via the CommVault Support Portal at support.commvault.com. Cases are raised by selecting the product component, severity, and providing initial diagnostic information. Before opening a case, collect the support bundle using the `qsystem log export` command on the CommServe — this packages CommServe, MediaAgent, and client logs into a single archive for upload. Metallic SaaS support escalation follows a separate path via the Metallic portal for cloud-managed deployments.

**Collecting the diagnostic bundle**

```bash
# On CommServe (run as administrator)
qsystem log export -path C:\cv_support_bundle

# Alternatively via Command Center:
# Settings > Support > Generate Support Bundle
```

**Required information for a support case**

- CommServe version and Feature Release number (Command Center > Settings > Version)
- MediaAgent version(s) for affected storage pools
- Failing job ID(s) and error code from the Job Controller
- Client name, OS version, and CommVault agent version
- Storage policy and subclient configuration (screenshots or export)
- Log bundle from `qsystem log export`

**Support tiers**

| Tier | Sev 1 SLA | Availability | Notes |
|---|---|---|---|
| Standard | 4 hours | Business hours | Per-incident or subscription |
| Priority | 2 hours | 24x7 | Enterprise subscription |
| Premium | 1 hour | 24x7 | TAM + proactive health checks |

## Escalation Workflow

```mermaid
flowchart TD
    issue(["Issue identified\nby ops team"])
    issue --> internal["Internal triage\nCheck Job Controller\n+ collect log paths"]
    internal --> selfResolve{Resolved\ninternally?}
    selfResolve -->|Yes| document["Document root cause\n+ update runbook"]
    selfResolve -->|No| bundle["Collect support bundle\nqsystem log export\n-path C:\\cv_support_bundle"]
    bundle --> openCase["Open case on\nsupport.commvault.com\nAttach bundle + job ID"]
    openCase --> sev{Severity?}
    sev -->|"Sev 1\nproduction down"| sev1["Sev 1: 24x7 response\nRequest phone bridge\nEscalate to Premium if SLA missed"]
    sev -->|"Sev 2/3\ndegraded / informational"| sev23["Sev 2/3: portal updates\nMonitor case queue"]
    sev1 --> track["Track in incident\nmanagement system"]
    sev23 --> track
    track --> resolve(["Resolution\n+ post-incident review"])

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    class internal,bundle,openCase,sev1,sev23,track,document action
    class selfResolve,sev decision
    class issue,resolve terminal
```
