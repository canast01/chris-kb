# Veeam — Escalation

Veeam support is accessed via the Veeam Customer Support Portal at my.veeam.com. Cases are raised by selecting the product (Veeam Backup & Replication), specifying the version, and classifying severity. ProSupport tiers provide enhanced SLAs and a designated technical account manager for enterprise customers. Before opening a case, export the Veeam log bundle from the console to provide the full diagnostic context immediately.

**Collecting log export**

1. In the VBR console: Main Menu > Help > Support Information
2. Click "Export Logs" — select the job or time range relevant to the issue
3. The wizard packages logs from the Backup Server and relevant proxies into a single ZIP archive

**Required information for a support case**

- VBR version (Help > About)
- Infrastructure type (VMware / Hyper-V / Agent)
- Job name and session ID of the failing job
- Error message from the job statistics view (copy the full text)
- Log export ZIP from the console

**Support tiers**

| Tier | Sev 1 SLA | Availability | Notes |
|---|---|---|---|
| Production | 2 hours | 24x7 | Standard enterprise |
| ProSupport | 1 hour | 24x7 | Designated engineer |
| ProSupport Plus | 30 minutes | 24x7 | TAM + proactive monitoring |
