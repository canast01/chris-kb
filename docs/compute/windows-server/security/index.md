# Windows Server Security

Windows Server builds are hardened to the CIS Microsoft Windows Server benchmark, applied via Group Policy Objects linked at the server OU level. Windows Defender is enabled and centrally managed via Microsoft Defender for Endpoint or SCCM; local exclusions are documented and approved per application. Local administrator accounts are managed through CyberArk PAM with LAPS providing rotating passwords for the built-in Administrator account where CyberArk is not yet deployed.

- **CIS benchmark:** Level 1 baseline applied via GPO; Level 2 controls reviewed and applied where operationally feasible
- **Windows Defender:** Real-time protection enabled; exclusions documented and tracked in CMDB
- **Windows Firewall:** Domain profile active; rules managed via GPO; host-based firewall logs forwarded to SIEM
- **CyberArk:** Local admin accounts onboarded to CyberArk; break-glass procedure documented
- **LAPS:** Deployed where CyberArk not available; password complexity and rotation interval configured via GPO
- **Audit policy:** Success and failure auditing enabled for logon, privilege use, object access, and policy change
- **SMB signing:** Required on all servers via GPO (`RequireSecuritySignature = 1`)
