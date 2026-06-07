# Active Directory — Escalation


<div class="kb-summary">
Active Directory support is provided through the Microsoft Support portal at support.microsoft.com, with Service Requests (SRs) raised under the Windows Server or Microsoft 365/Entra product family.
</div>
```text
┌─────────────────────── Security Active Directory Troubleshooting — Escalation ────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Active Directory escalation: severity triage, vendor support contact, and required artifacts │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Active Directory Troubleshooting infrastructure · management network · monitor  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Active Directory   = Security Active Directory Troubleshooting platform overview and core concept  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


 For critical AD outages (authentication down, replication split-brain, FSMO role loss), use the Severity A case classification and request an on-call engineer; Microsoft Premier or Unified Support contracts include faster SLA and proactive engagement. Microsoft FastTrack is available for AD-to-Entra ID migration projects at qualifying licence levels.

**Data to collect before opening a case:**

- `dcdiag /v /f:dcdiag.txt` — full diagnostic output from all affected DCs
- `repadmin /showrepl * /csv > repl.csv` — replication status across forest
- `netlogon.log` from `%SystemRoot%\debug\` on affected DCs
- Security and System event logs (last 72 hours) from affected DCs
- `ipconfig /all` and `nslookup` output to confirm DNS configuration
- AD domain and forest functional level (`Get-ADDomain`, `Get-ADForest`)

| Support Tier | SLA (Sev A) | Portal |
|---|---|---|
| Microsoft Unified Support | < 2 hours callback | admin.microsoft.com / support.microsoft.com |
| Microsoft Premier Support | < 1 hour callback | Premier portal |
| FastTrack (migration) | Project-based | fasttrack.microsoft.com |
