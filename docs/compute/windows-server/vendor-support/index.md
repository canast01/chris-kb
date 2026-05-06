# Windows Server Vendor Support

Microsoft support for Windows Server is accessed through the Microsoft admin portal or Azure portal, with support tickets created under the appropriate subscription or support plan. Before opening a case, collect a System Information report (`msinfo32 /report`), relevant Event Log exports, and output from `sfc /scannow` and `DISM /Online /Cleanup-Image /CheckHealth`. Premier/Unified support customers have access to designated support engineers and faster SLAs than standard pay-per-incident support.

- **Support portal:** [support.microsoft.com](https://support.microsoft.com) or Microsoft 365 Admin Center
- **Ticket creation:** Requires subscription ID or support contract number; select Windows Server product area
- **Diagnostic data to collect:**
  - `msinfo32 /report msinfo.txt` — system configuration snapshot
  - Event Logs: System, Application, Security (exported as .evtx)
  - `sfc /scannow` — system file integrity check
  - `DISM /Online /Cleanup-Image /ScanHealth` — image health check
- **Support tiers:** Standard (pay-per-incident), Developer, Professional Direct, Unified (Premier)
- **ESU:** Extended Security Updates available for Windows Server 2012/2012 R2 and 2016 post-mainstream EOL; requires ESU license and MAK key or Azure Arc enrollment
