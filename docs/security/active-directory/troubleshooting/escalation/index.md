# Active Directory — Escalation

Active Directory support is provided through the Microsoft Support portal at support.microsoft.com, with Service Requests (SRs) raised under the Windows Server or Microsoft 365/Entra product family. For critical AD outages (authentication down, replication split-brain, FSMO role loss), use the Severity A case classification and request an on-call engineer; Microsoft Premier or Unified Support contracts include faster SLA and proactive engagement. Microsoft FastTrack is available for AD-to-Entra ID migration projects at qualifying licence levels.

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
