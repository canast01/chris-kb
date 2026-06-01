# CyberArk Vendor Support


<div class="kb-summary">
CyberArk support is accessed through the CyberArk Support Portal at support.cyberark.com, where Service Requests (SRs) are raised by product area (Vault, CPM, PSM, PVWA).
</div>

 For Severity 1 issues (Vault down, authentication unavailable), call the CyberArk emergency support line referenced in the portal after creating the SR online. CyberArk Blue Team services provide incident response for PAM-related security incidents under a separate engagement.

**Data to collect before opening a case:**

- CyberArk `DiagnosticTool` output — run from the Vault server to collect component versions, logs, and configuration summary
- Vault version, CPM version, PSM version, PVWA version (from PVWA → Administration → System Health)
- Safe count and account count (from PVWA Dashboard)
- Windows Event logs from Vault server (Application and System, last 48 hours)
- PrivateArk Server log (`%ProgramFiles(x86)%\CyberArk\Password Vault\Logs\`)
- Error messages and exact steps to reproduce the issue

| Support Tier | Sev 1 Response | Portal |
|---|---|---|
| Standard Support | 4 hours | support.cyberark.com |
| Premium Support | 1 hour | support.cyberark.com + phone line |
| CyberArk Blue Team | Project/incident SLA | Separate engagement via account team |
